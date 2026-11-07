The revised story is **added feature → rationale → controlled incremental comparison → selected addition → final recipe outcome → follow-up candidates**. The existing model serves only as the comparison baseline. Inflation/IPC normalization, drift analysis, existing feature inventories, and the original champion-retention narrative are outside the requested scope. Lags, rolling summaries, relative features, usage, ranks, and EMA remain in scope.

## What the sources establish

The review reconciles all **22 published-recipe aggregates against the 92 supplied submission rows**, checks the six HT5955 mean AUC records and feature definitions, confirms 20 HPO evaluations and selected trial 10, and inspects the notebook's feature code and selection rule. It never executes notebook cells. The supplied notebook has no executed outputs; it establishes definitions rather than a new successful execution.

These are checks within supplied evidence, not a fresh Kaggle query, retraining, or validation of unseen artifact hashes. Machine-readable results and hashes of all supplied files are in `source_verification.json`.

The baseline mean May AUC is **0.895958660563797**. Each package was added separately to 152 repaired predictors. The binary probe held learner settings fixed: 192 rounds, 52 leaves, minimum leaf size 443, the same training rules, and five matched seeds.

| Added package | New columns | Mean May AUC | Mean AUC difference |
|---|---:|---:|---:|
| Last-month values | 6 | 0.895450270 | −0.000508391 |
| Month-to-month changes | 6 | 0.896405244 | +0.000446584 |
| Prior-three-month means + coverage | 12 | 0.896636814 | +0.000678153 |
| Relative balance/payroll + near-zero flags | 4 | **0.897414631** | **+0.001455970** |
| Visa/Master utilization | 2 | 0.895789820 | −0.000168841 |

Differences are computed from catalog means. For the same paired seeds, the difference of means is the mean paired difference. The catalog flags only relative funds as selected, matching the declared source rule: positive mean paired AUC change and wins in at least four of five seeds. The original 1/3/3/5/2 seed-win counts cannot be independently reproduced without per-seed data, so the new video shows mean changes and the selection rule without those counts.

## Why these additions

- **Lag 1:** the previous exact-calendar-month value distinguishes a stable low level from a recent fall.
- **Delta 1:** current minus lag 1 exposes withdrawal or declining activity.
- **Prior-three-month summaries:** a prior-only mean plus known-value count estimates usual behavior and support. At least two finite observations are required.
- **Relative funds:** for balance and payroll, `clip((current − prior_mean) / max(abs(prior_mean), 1), −10, 10)` plus a near-zero-reference flag. The same absolute decrease has different meaning at different personal scales.
- **Utilization:** separate Visa/Master balance-to-positive-limit ratios, clipped to [−10, 10], express balances relative to available capacity.

The six common fields were balance, payroll, quarterly activity, debit transactions, Visa consumption, and Master consumption. Missing calendar observations are not zeros. The tests identify a useful package, not whether balance or payroll alone caused the gain.

## Ultimate outcome and the meaning of best

**Relative balance/payroll is the strongest added package in this controlled screen**: largest mean AUC gain and the only selected package. It is not a universally optimal feature or an isolated public-profit effect. May was reused for feature selection and HPO, so the winning AUC is development evidence rather than an untouched test. Five seeds capture stochastic variation, not five independent months.

The four added columns produced 156 predictors. HPO trial 10 selected 308 rounds, learning rate 0.0464871536065, 62 leaves, minimum leaf size 339, and feature fraction 0.600391357439. The final five-seed ensemble was submitted at nine contact policies. Its best Inicial score was **401.915 at 11,500 or 12,000 contacts**, submissions **57852532 / 57852534**. These are cutoff variations of one final recipe, not nine feature sets.

The public score belongs to the selected/tuned/refitted/ensembled recipe and its policy. It does not isolate the incremental public effect of a feature. The original 408.498 reference is removed because its cited submission is absent from the supplied outcome exports and report.

## Follow-up and source gaps

The report's HT5956 section corroborates longer funds history, relative usage, monetary ranks, and prior-only EMA definitions. It says funds history and usage improved historical profit in both May and July, while EMA's positive mean signal did not improve both months. None had a public score. The revision retains these qualitative findings.

The original exact profit deltas cannot be reproduced: the new catalog's eight HT5956 rows have empty historical metric/value fields. The report also does not establish the original ranks row's +1.76M / 2-of-2 result. Those values remain preserved as proposal claims but are omitted from the revised video. The displayed pilot findings are examples, not an exhaustive ranking or evidence that ranks failed.

The precise files needed for the omitted quantitative claims are **HT5955_feature_summary.csv** or its per-seed comparison export, and **HT5956_summary.csv** with month-level outcomes. Original training data/native artifacts would be required for rerunning models. The current draft uses supported claims without depending on those optional details.

## Visual and timing review

The original storyboard uses fixed SVG poses and a coarse timing map. Its renderer checks dimensions and one preview instant, not full animation quality or narration synchronization. Some semantic flags in its verifier are unconditional true values. Its 172-word count reproduces; spoken duration was not measured. At t=48–49 it still shows the EMA pose while the narration block also contains the result discussion: this is a coarse planning map, not a measured audio-sync failure.

The dark revision uses a feature-addition diagram, an explicitly illustrative relative-change example, a diverging AUC plot, and the actual nine-point contact-policy curve. Pilot findings use a compact qualitative graphic. There are six scene intervals and continuous time-driven reveals. The script has 187 written words; target segment rates are about 116–135 words/minute before compound/number expansion. Recording will determine actual timings.

A 200×200 headshot area at x1630/y80 replaces the large presenter column. The lower y940–1060 band stays clear for captions. All numeric results appear at their final values; no error bars, seed identities, customer records, or monthly values are invented. The relative example uses separate prior-mean reference heights, with numeric labels, and is explicitly schematic rather than a shared-scale magnitude comparison.

This is a review draft. Manim remains the production engine; no narration, final Manim build, or complete MP4 export is claimed.
