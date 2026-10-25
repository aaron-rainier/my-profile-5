#!/usr/bin/env python3
"""Petit bot BTC/EUR pour l'app Crypto.com, avec garde-fous codés en dur.

  python3 bot/cdc_bot.py backtest   rejoue la stratégie sur les semaines passées (sans clé)
  python3 bot/cdc_bot.py check      lit les soldes et affiche la décision, sans passer d'ordre
  python3 bot/cdc_bot.py live       applique la décision (vrais ordres)

Les ordres passent par l'API de l'app (wapi.crypto.com), signée comme les scripts officiels
de crypto-com/crypto-agent-trading. Les signaux de prix viennent du marché public BTC_EUR
de Crypto.com Exchange. Clé et secret : CDC_API_KEY et CDC_API_SECRET, jamais dans le code.
L'état du bot (BTC achetés par lui, coût, cash) est dans le fichier BOT_STATE : il ne vend
jamais d'autres BTC que ceux qu'il a achetés.
"""
import base64
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

APP_API = "https://wapi.crypto.com"
MARKET_API = "https://api.crypto.com/exchange/v1/"
BUDGET = 30.0        # € engagés au maximum dans la position
TRANCHE = 5.0        # € par achat
DIP = 0.03           # 1er achat si le BTC est 3 % sous son plus haut des dernières 24 h
AVG_DOWN = 0.04      # renfort si le BTC est 4 % sous le prix moyen d'entrée
TAKE_PROFIT = 0.01   # revendre si la vente rapporte 1 % de plus que le coût (écart de l'app compris)
MAX_LOSS = 2.0       # à -2 € de résultat, on vend tout et le bot s'arrête
DURATION = timedelta(days=7)
APP_SPREAD = 0.015   # écart mesuré de l'app de chaque côté, pour le backtest seulement
BTC_STEP = Decimal("0.0000001")


def http_json(req):
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{req.full_url}: HTTP {e.code} {e.read().decode()[:300]}")


def app(method, path, body=None):
    key, secret = os.environ["CDC_API_KEY"], os.environ["CDC_API_SECRET"]
    ts = str(int(time.time() * 1000))
    raw = json.dumps(body, separators=(",", ":")) if body else ""
    sig = hmac.new(secret.encode(), (ts + method + path.split("?")[0] + raw).encode(), hashlib.sha256)
    headers = {"Cdc-Api-Key": key, "Cdc-Api-Timestamp": ts, "User-Agent": "cdc-bot/1.0",
               "Cdc-Api-Signature": base64.b64encode(sig.digest()).decode()}
    if body:
        headers["Content-Type"] = "application/json"
    res = http_json(urllib.request.Request(APP_API + path, data=raw.encode() if body else None,
                                           method=method, headers=headers))
    if res.get("ok") is not True:
        raise RuntimeError(f"{method} {path}: {res.get('error')} {res.get('error_message')}")
    return res


def market():
    t = http_json(urllib.request.Request(
        MARKET_API + "public/get-tickers?instrument_name=BTC_EUR"))["result"]["data"][0]
    return (float(t["b"]) + float(t["k"])) / 2, float(t["h"])


def balances():
    eur = sum(float(b["amount"]["amount"]) for b in app("GET", "/v1/fiat-account")["account"]["balances"]
              if b["currency"] == "EUR")
    btc = sum(float(w["available"]["amount"]) for w in app("GET", "/v1/crypto-account")["account"]["wallets"]
              if w["currency"] == "BTC")
    return eur, btc


def quote_sale(qty):
    return app("POST", "/v1/crypto-sales/quotations", {
        "from_currency": "BTC", "from_amount": qty, "to_currency": "EUR", "fixed_side": "from"})["quotation"]


def quote_purchase(eur):
    return app("POST", "/v1/crypto-purchase/quotations", {
        "from_currency": "EUR", "to_currency": "BTC", "from_amount": f"{eur:.2f}"})["quotation"]


def confirm(kind, quotation):
    return app("POST", f"/v1/{kind}/orders", {"quotation_id": quotation["id"]}).get("transaction")


def decide(mid, high24, qty, cost, cash, sell_value, avg_mid, eur_free, now, end):
    """Retourne (action, raison) : BUY (une tranche), SELL (toute la position), HOLD ou STOP."""
    held = qty > 0
    pnl = cash + sell_value
    if now >= end:
        if held and sell_value > cost:
            return "SELL", "fin de la semaine, en gain"
        return "STOP", "semaine terminée" + (", BTC gardé pour ne pas vendre à perte" if held else "")
    if pnl <= -MAX_LOSS:
        if held:
            return "SELL", f"stop-loss ({pnl:+.2f} €)"
        return "STOP", f"arrêté après stop-loss ({pnl:+.2f} €)"
    if held and sell_value >= cost * (1 + TAKE_PROFIT):
        return "SELL", f"prise de profit ({sell_value:.2f} € pour {cost:.2f} € investis)"
    can_buy = eur_free >= TRANCHE and cost + TRANCHE <= BUDGET + 0.01
    if can_buy and not held and mid <= high24 * (1 - DIP):
        return "BUY", f"achat sur repli ({(mid / high24 - 1) * 100:.1f} % sous le plus haut 24 h)"
    if can_buy and held and mid <= avg_mid * (1 - AVG_DOWN):
        return "BUY", f"renfort ({(mid / avg_mid - 1) * 100:.1f} % sous le prix moyen d'entrée)"
    return "HOLD", "rien à faire"


def load_state(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"start": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "qty": "0", "cost": 0.0, "cash": 0.0, "mid_cost": 0.0, "trades": []}


def save_state(path, state):
    with open(path, "w") as f:
        json.dump(state, f, indent=1)


def run(mode):
    path = os.environ["BOT_STATE"]
    state = load_state(path)
    now = datetime.now(timezone.utc)
    end = datetime.fromisoformat(state["start"]) + DURATION
    mid, high24 = market()
    eur, btc = balances()
    held = min(Decimal(state["qty"]), Decimal(str(btc)).quantize(BTC_STEP, rounding=ROUND_DOWN))
    qty, cost, cash = float(held), state["cost"], state["cash"]
    sale = quote_sale(str(held)) if held > 0 else None
    sell_value = float(sale["to_amount"]["amount"]) if sale else 0.0
    avg_mid = state["mid_cost"] / qty if qty else 0.0

    action, why = decide(mid, high24, qty, cost, cash, sell_value, avg_mid, eur, now, end)
    print(f"{now:%Y-%m-%d %H:%M} UTC | BTC {mid:.0f} € (plus haut 24 h {high24:.0f}) | "
          f"position {qty:.7f} BTC pour {cost:.2f} €, revendable {sell_value:.2f} € | "
          f"résultat {cash + sell_value:+.2f} € | EUR libres {eur:.2f} | {action} : {why}")
    if mode != "live" or action not in ("BUY", "SELL"):
        return

    if action == "BUY":
        q = quote_purchase(TRANCHE)
        tx = confirm("crypto-purchase", q)
        got = Decimal(q["to_amount"]["amount"])
        state["qty"] = str(Decimal(state["qty"]) + got)
        state["cost"] += TRANCHE
        state["cash"] -= TRANCHE
        state["mid_cost"] += mid * float(got)
        trade = {"side": "BUY", "eur": TRANCHE, "btc": str(got)}
    else:
        q = quote_sale(str(held))  # nouvelle cotation : la précédente ne vaut que 15 s
        tx = confirm("crypto-sales", q)
        got = float(q["to_amount"]["amount"])
        state["qty"] = str(Decimal(state["qty"]) - held)
        state["cash"] += got
        state["cost"] = state["mid_cost"] = 0.0
        trade = {"side": "SELL", "eur": got, "btc": str(held)}
    trade.update(time=now.isoformat(timespec="seconds"), reason=why, tx=(tx or {}).get("id"))
    state["trades"].append(trade)
    save_state(path, state)
    print("ordre exécuté :", json.dumps(trade, ensure_ascii=False))


def candles(hours):
    out, end = [], int(time.time() * 1000)
    while len(out) < hours:
        page = http_json(urllib.request.Request(
            MARKET_API + f"public/get-candlestick?instrument_name=BTC_EUR&timeframe=1h&count=300&end_ts={end}"
        ))["result"]["data"]
        if not page:
            break
        out = page + out
        end = min(c["t"] for c in page) - 1
    out = sorted({c["t"]: c for c in out}.values(), key=lambda c: c["t"])
    return out[-hours:]


def backtest(weeks=8, step=3, eur=10.0):
    """Rejoue chaque semaine passée avec `eur` € disponibles, un passage toutes les `step` heures."""
    c = candles(weeks * 168 + 24)
    total = 0.0
    for w in range(weeks):
        first, last = 24 + w * 168, 24 + (w + 1) * 168 - 1
        free, qty, cost, cash, mid_cost, n = eur, 0.0, 0.0, 0.0, 0.0, 0
        for i in list(range(first, last, step)) + [last]:
            mid = float(c[i]["c"])
            high24 = max(float(x["h"]) for x in c[i - 23:i + 1])
            sell_value = qty * mid * (1 - APP_SPREAD)
            action, _ = decide(mid, high24, qty, cost, cash, sell_value,
                               mid_cost / qty if qty else 0.0, free, i, last)
            if action == "BUY":
                q = TRANCHE / (mid * (1 + APP_SPREAD))
                qty, cost, cash, free, mid_cost, n = (qty + q, cost + TRANCHE, cash - TRANCHE,
                                                      free - TRANCHE, mid_cost + mid * q, n + 1)
            elif action == "SELL":
                qty, cost, cash, free, mid_cost, n = 0.0, 0.0, cash + sell_value, free + sell_value, 0.0, n + 1
        p0, p1 = float(c[first]["c"]), float(c[last]["c"])
        kept = qty * p1 * (1 - APP_SPREAD)
        day = datetime.fromtimestamp(c[first]["t"] / 1000, timezone.utc)
        print(f"semaine du {day:%d/%m} : bot {cash + kept:+.2f} € en {n} ordres"
              f"{f' (dont {kept:.2f} € de BTC gardé)' if qty else ''} | BTC {(p1 / p0 - 1) * 100:+.1f} %")
        total += cash + kept
    print(f"total bot sur {weeks} semaines avec {eur:.0f} € : {total:+.2f} €")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode == "backtest":
        backtest()
    elif mode in ("check", "live"):
        run(mode)
    else:
        sys.exit(f"mode inconnu : {mode}")
