Working title: **The context behind the number**.

Audience: data science classmates. Target duration: 120 seconds. Format: 1920×1080, dark mathematical graphics, a small upper-right headshot, and narration recorded by the user. The script currently contains 244 written words, with target segment rates around 109–135 words/minute. These are planning rates, not measured speech timings.

| Time | Story beat | Main visual | What viewers should understand |
|---|---|---|---|
| 0–16s | Same balance, different story | Two illustrative balances unfold into 3D time layers; one history falls and one is steady. | Current values can hide behavior relative to a customer's normal level. |
| 16–62s | Features and hypotheses | All nine feature families share a stable 3×3 map, with a live glyph, a definition, and the hypothesized benefit. | What we added and why, in one scene. |
| 62–74s | A fair comparison | The same glyphs move to a reference-versus-addition diagram, with five matched retrainings. | Track incremental effect against the relevant reference, rather than attributing a whole recipe's result to a feature. |
| 74–108s | Results together | One consolidated chart, with aligned rows for all nine families and separate AUC/profit columns. | Contrast measured outcomes within the appropriate column. |
| 108–120s | Payoff and hold | Retain the exact same chart, emphasizing relative funds, longer-history funds, and usage. | Personal context gave the clearest ranking signal; the profit candidates are still historical evidence. |

## Feature map

| Family | Plain definition | Hypothesis |
|---|---|---|
| Last-month values | Previous exact-calendar-month level | Recent context helps distinguish usual levels from change. |
| Monthly changes | Current minus last month | Sudden movement could reveal withdrawal or reduced engagement. |
| Three-month averages | Mean of the prior three months, with coverage information | A more stable estimate of normal behavior. |
| Relative funds, 3 months | Balance/payroll change scaled to the customer's own prior mean, plus near-zero flags | The same absolute change has different meaning at different personal scales. |
| Card utilization | Separate card balance-to-positive-limit ratios | Pressure relative to available credit capacity. |
| Relative funds, 6 months | The relative-funds idea using a longer historical reference | A steadier personal baseline. |
| Relative usage | Debit/card activity relative to the customer's own three-month mean | Emerging disengagement in activity rather than amounts alone. |
| Monetary ranks | Position among same-month monetary values, respecting signed groups | Put amounts on comparable relative scales. |
| Recent-weighted history / EMA | Exponential average of prior observations, with more influence for recent values | React more strongly to recent behavior. |

These are nine families, not nine identical isolated training runs. Packages can contain multiple columns; a tested ranks-plus-usage combination is not a tenth family. The hypotheses are not causal findings.

## Consolidated chart contract

The user selected two labeled metric columns because a common metric/reference is not available in the supplied files. AUC differences are numerical effects versus the original repaired snapshot. Profit consistency is qualitative evidence across May/July versus snapshot plus three-month relative funds. Do not normalize them into a fabricated universal score or imply that a dot or color has the same effect size across columns.

The five mean AUC differences come from the supplied configuration catalog. Only relative funds passed the declared screening rule; smaller positive means alone were insufficient. Five seeds are stochastic repeats on a validation month, not five independent time holdouts.

The supplied audit report supports improved profit in both inspected months for longer funds history and usage, and mixed monthly benefit for EMA. It does not verify the original ranks result or exact pilot profit deltas. Keep ranks visible as unresolved, and use a dash for no comparable verified result. A dash is not zero or failure. The original full recipes, unsupported exact pilot values, and contextual public score stay in supporting notes, not in a second results chart.

The final public score of 401.915 applies to the selected, tuned, refitted, ensembled recipe and contact policy; it is not the isolated public contribution of a feature. No public score exists for the follow-up pilot variants. The ending therefore identifies the strongest controlled ranking package and promising profit candidates, not a global public winner.

## Scope and production status

Present one scientific study by question and outcome; do not claim the historical protocols were identical or simultaneous. Exclude inflation/IPC, drift analysis, existing model inventories, notebook IDs, search chronology, and tuning details from the main narrative. Existing predictors appear only as the reference or inputs to an added feature.

The review export is a silent Chromium/SVG animatic. Its time layers use projected 3D coordinates; they are not an unrun Manim scene being passed off as rendered. Final Manim production can retain the same geometry, feature identity, and chart data, then refine transitions and timing against the recorded voiceover.
