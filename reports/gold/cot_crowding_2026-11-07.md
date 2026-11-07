# COT Contrarian Crowding Report

Generated at: 2026-11-07 17:44:33
As-of date: 2026-11-07
COT data date: n/a
Universe: `explicit_symbols` (1 markets)
Lookback: 156w primary / 26w short
Extreme thresholds: high >= 90.0, low <= 10.0

## Summary

- Markets analyzed: 0
- Crowded long (fade candidates for SHORT setups): 0
- Crowded short (fade candidates for LONG setups): 0
- Skipped (insufficient/failed data): 1

## Crowded Long (COT Index >= high threshold)

Large speculators are near their most net-long extreme of the lookback window. This is a *candidate* for a contrarian SHORT — proceed to Shapiro steps 2-5 (news failure, price action, entry, exit) before trading. Crowdedness alone is not a signal.

None.

## Crowded Short (COT Index <= low threshold)

Large speculators are near their most net-short extreme of the lookback window. This is a *candidate* for a contrarian LONG — proceed to Shapiro steps 2-5 before trading.

None.

## Full Ranking (by extremity, |COT Index - 50| descending)

| SYMBOL | NAME | INDEX_3Y | INDEX_26W | NET_POS | NET/OI | %OI L/S | WoW |
|---|---|---|---|---|---|---|---|

## Biggest Week-over-Week Net Position Swings

| SYMBOL | NAME | WoW CHANGE | NET_POS | CLASSIFICATION |
|---|---|---|---|---|

## Skipped Markets

| SYMBOL | REASON | WEEKS AVAILABLE |
|---|---|---|
| GC | API fetch failed: HTTP 402 - Restricted Endpoint: This endpoint is not available under your current subscription please visit our subscription page to upgrade your plan at https://financialmodelingprep.com/ | 0 |

## Methodology

COT Index = (current net large-speculator position - lookback minimum) / (lookback maximum - lookback minimum) * 100, computed from the CFTC legacy report's non-commercial long/short fields. See `references/cot-index-calculation.md` for the full formula and field glossary, and `references/shapiro-methodology.md` for the manual steps (news failure, price action, entry, exit) that must confirm any crowding signal before it becomes a trade.

**Disclaimer:** This report is a crowding-detection screen only. It is not investment advice and is not a standalone entry signal. COT data is published Fridays ~3:30pm ET with positions as of the prior Tuesday — always a few days old by the time it is read.
