#!/usr/bin/env python3
"""Petit bot BTC/EUR pour Crypto.com Exchange, avec garde-fous codés en dur.

  python3 bot/cdc_bot.py backtest   rejoue la stratégie sur les semaines passées (sans clé)
  python3 bot/cdc_bot.py dry-run    décision sur le marché actuel avec 30 € fictifs (sans clé)
  python3 bot/cdc_bot.py check      lit le solde et les trades avec la clé, ne passe aucun ordre
  python3 bot/cdc_bot.py live       applique la décision (vrais ordres)

La clé et le secret sont lus dans CDC_API_KEY et CDC_API_SECRET, jamais dans le code.
BOT_START (ISO 8601, UTC) marque le début de la semaine : à chaque passage, la position
est reconstruite depuis l'historique des trades, aucun fichier n'est gardé entre deux passages.
"""
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from decimal import ROUND_DOWN, Decimal

API = "https://api.crypto.com/exchange/v1/"
INSTRUMENT = "BTC_EUR"
BUDGET = 30.0        # € engagés au maximum
TRANCHE = 10.0       # € par achat
DIP = 0.02           # 1er achat si le prix est 2 % sous le plus haut des dernières 24 h
AVG_DOWN = 0.025     # renfort si le prix est 2,5 % sous le prix moyen d'achat
TAKE_PROFIT = 0.02   # tout revendre dès +2 % sur le prix moyen
MAX_LOSS = 5.0       # à -5 € de résultat, on vend tout et le bot s'arrête
DURATION = timedelta(days=7)
QTY_TICK = Decimal("0.00001")
PRICE_TICK = Decimal("0.01")


def http(method, body=None, query=""):
    url = API + method + ("?" + query if query else "")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            res = json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method}: HTTP {e.code} {e.read().decode()[:300]}")
    if res.get("code") != 0:
        raise RuntimeError(f"{method}: {res}")
    return res["result"]


def private(method, params=None):
    key, secret = os.environ["CDC_API_KEY"], os.environ["CDC_API_SECRET"]
    params = params or {}
    req_id = nonce = int(time.time() * 1000)
    payload = method + str(req_id) + key + "".join(f"{k}{params[k]}" for k in sorted(params)) + str(nonce)
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return http(method, {"id": req_id, "method": method, "api_key": key,
                         "params": params, "nonce": nonce, "sig": sig})


def market():
    t = http("public/get-tickers", query="instrument_name=" + INSTRUMENT)["data"][0]
    return float(t["b"]), float(t["k"]), float(t["h"])


def balances():
    free = {}
    for b in private("private/user-balance")["data"][0].get("position_balances", []):
        free[b["instrument_name"]] = float(b["quantity"]) - float(b.get("reserved_qty") or 0)
    return free.get("EUR", 0.0), free.get("BTC", 0.0)


def fetch_trades(start, now):
    data = private("private/get-trades", {
        "instrument_name": INSTRUMENT, "limit": 100,
        "start_time": int(start.timestamp() * 1000), "end_time": int(now.timestamp() * 1000),
    })["data"]
    if len(data) >= 100:
        raise RuntimeError("plus de 100 trades : pagination non gérée, arrêt par sécurité")
    return data


def position(trades):
    """Quantité, coût de la position ouverte et cash net (€ reçus - € dépensés) depuis BOT_START."""
    qty = cost = cash = 0.0
    for t in sorted(trades, key=lambda t: int(t["create_time"])):
        q, p, fee, ccy = (float(t["traded_quantity"]), float(t["traded_price"]),
                          abs(float(t["fees"])), t["fee_instrument_name"])
        if ccy not in ("BTC", "EUR"):
            print(f"attention : frais payés en {ccy}, non comptés")
        fee_btc, fee_eur = (fee if ccy == "BTC" else 0.0), (fee if ccy == "EUR" else 0.0)
        if t["side"] == "BUY":
            qty += q - fee_btc
            cost += q * p + fee_eur
            cash -= q * p + fee_eur
        else:
            sold = q + fee_btc
            cost -= cost * min(sold / qty, 1.0) if qty > 0 else 0.0
            qty -= sold
            cash += q * p - fee_eur
    return max(qty, 0.0), max(cost, 0.0), cash


def decide(bid, ask, high24, qty, cost, cash, eur_free, now, end):
    """Retourne (action, montant, raison) : BUY en €, SELL en BTC, HOLD ou STOP."""
    held = qty >= float(QTY_TICK)
    avg = cost / qty if held else 0.0
    pnl = cash + qty * bid
    if now >= end:
        return ("SELL", qty, "fin de la semaine") if held else ("STOP", 0, "semaine terminée")
    if pnl <= -MAX_LOSS:
        if held:
            return "SELL", qty, f"stop-loss ({pnl:+.2f} €)"
        return "STOP", 0, f"arrêté après stop-loss ({pnl:+.2f} €)"
    if held and bid >= avg * (1 + TAKE_PROFIT):
        return "SELL", qty, f"prise de profit (+{(bid / avg - 1) * 100:.1f} %)"
    can_buy = eur_free >= TRANCHE and cost + TRANCHE <= BUDGET + 0.01
    if can_buy and not held and ask <= high24 * (1 - DIP):
        return "BUY", TRANCHE, f"achat sur repli ({(ask / high24 - 1) * 100:.1f} % sous le plus haut 24 h)"
    if can_buy and held and ask <= avg * (1 - AVG_DOWN):
        return "BUY", TRANCHE, f"renfort ({(ask / avg - 1) * 100:.1f} % sous le prix moyen)"
    return "HOLD", 0, "rien à faire"


def dec(x, tick):
    return Decimal(str(x)).quantize(tick, rounding=ROUND_DOWN)


def place(side, amount, bid, ask, btc_free):
    # Ordre limite immédiat ou annulé, 0,2 % au-delà du carnet : jamais de glissement plus grand.
    if side == "BUY":
        price = dec(ask * 1.002, PRICE_TICK)
        qty = dec(amount / float(price), QTY_TICK)
    else:
        price = dec(bid * 0.998, PRICE_TICK)
        qty = dec(min(amount, btc_free), QTY_TICK)
    if qty <= 0:
        return "quantité trop petite, rien envoyé"
    return private("private/create-order", {
        "instrument_name": INSTRUMENT, "side": side, "type": "LIMIT", "price": str(price),
        "quantity": str(qty), "time_in_force": "IMMEDIATE_OR_CANCEL",
        "client_oid": f"bot-{int(time.time())}",
    })


def candles(hours):
    out, end = [], int(time.time() * 1000)
    while len(out) < hours:
        page = http("public/get-candlestick", query=f"instrument_name={INSTRUMENT}"
                    f"&timeframe=1h&count=300&end_ts={end}")["data"]
        if not page:
            break
        out = page + out
        end = min(c["t"] for c in page) - 1
    out = sorted({c["t"]: c for c in out}.values(), key=lambda c: c["t"])
    return out[-hours:]


def backtest(weeks=4, step=3, fee=0.005):
    """Rejoue chaque semaine passée, un passage toutes les `step` heures, frais supposés de 0,5 %."""
    c = candles(weeks * 168 + 24)
    total = 0.0
    for w in range(weeks):
        first, last = 24 + w * 168, 24 + (w + 1) * 168 - 1
        eur, qty, cost, cash, n = BUDGET, 0.0, 0.0, 0.0, 0
        for i in list(range(first, last, step)) + [last]:
            price = float(c[i]["c"])
            bid, ask = price * 0.9998, price * 1.0002
            high24 = max(float(x["h"]) for x in c[i - 23:i + 1])
            action, amount, _ = decide(bid, ask, high24, qty, cost, cash, eur, i, last)
            if action == "BUY":
                q = float(dec(amount / ask, QTY_TICK))
                spent = q * ask * (1 + fee)
                qty, cost, cash, eur, n = qty + q, cost + spent, cash - spent, eur - spent, n + 1
            elif action == "SELL":
                got = qty * bid * (1 - fee)
                qty, cost, cash, eur, n = 0.0, 0.0, cash + got, eur + got, n + 1
        p0, p1 = float(c[first]["c"]), float(c[last]["c"])
        hold = BUDGET * (p1 / p0) * (1 - fee) ** 2 - BUDGET
        day = datetime.fromtimestamp(c[first]["t"] / 1000, timezone.utc)
        print(f"semaine du {day:%d/%m} : bot {cash:+.2f} € en {n} ordres | "
              f"BTC {(p1 / p0 - 1) * 100:+.1f} % | acheter-et-garder {hold:+.2f} €")
        total += cash
    print(f"total bot sur {weeks} semaines : {total:+.2f} €")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "dry-run"
    if mode == "backtest":
        return backtest()
    now = datetime.now(timezone.utc)
    bid, ask, high24 = market()
    if mode == "dry-run":
        eur, btc, qty, cost, cash, end = BUDGET, 0.0, 0.0, 0.0, 0.0, now + DURATION
    elif mode in ("check", "live"):
        start = datetime.fromisoformat(os.environ["BOT_START"])
        end = start + DURATION
        eur, btc = balances()
        qty, cost, cash = position(fetch_trades(start, now))
    else:
        sys.exit(f"mode inconnu : {mode}")

    action, amount, why = decide(bid, ask, high24, qty, cost, cash, eur, now, end)
    # Garde-fou indépendant des trades : jamais plus de BUDGET en BTC selon le solde réel.
    if action == "BUY" and btc * bid + amount > BUDGET + 1:
        action, why = "HOLD", f"achat bloqué : déjà {btc * bid:.2f} € de BTC sur le compte"

    avg = cost / qty if qty else 0.0
    print(f"{now:%Y-%m-%d %H:%M} UTC | BTC {bid:.2f} / {ask:.2f} € | plus haut 24 h {high24:.2f} | "
          f"position {qty:.5f} BTC (prix moyen {avg:.2f}) | résultat {cash + qty * bid:+.2f} € | "
          f"EUR libres {eur:.2f} | {action} : {why}")
    if mode == "live" and action in ("BUY", "SELL"):
        print("ordre :", place(action, amount, bid, ask, btc))


if __name__ == "__main__":
    main()
