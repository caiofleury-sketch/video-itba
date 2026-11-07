# Feature-engineering parameters and actual public outcomes

Reviewed November 7, 2026. Live Kaggle history queried at **01:20:57 UTC**:
61 Inicial submissions and 79 Senior submissions, with neither query truncated.
Notebook source was searched directly; 28 relevant notebook/source/executed-copy
records were indexed. Aggregate exports reference 120 hashed source artifacts.

## Findings

1. The dedicated feature-engineering notebook is
   **`z526_HT5955_Ingenieria_Variables_HPO.ipynb`**, followed by
   **`z527_HT5956_Drift_History_Pilot.ipynb`** and the rich-model
   **`z528_HT5957_Champion_Refinement.ipynb`**/recovery notebooks.
2. **HT5958 is already the product of broad feature engineering.** Its underlying
   HT5954 model uses 1,914 raw/calendar-history predictors, not the raw 152-column
   snapshot. Its winning feature/model recipe came from the 68-design five-family
   study in `z524_Five_Family_Champion_Search.ipynb`, building on `z523`.
3. Many feature/HPO trials have **no public score**. Only selected final recipes
   were trained for September and submitted. Assigning their scores to every
   historical configuration or constituent feature would invent outcomes.
4. **Inicial and Senior are separate competition tracks.** HT5955's 401.915 is
   Inicial. HT5958's 453.831 is Senior. The same HT5954 B file was submitted to both
   and scored 437.081 in each, but that observed equality does not authorize
   treating every unsubmitted cross-competition recipe as scored.

## Complete evidence tables

All supporting files are under
[`research_notes/Feature engineering public outcome audit/`](../research_notes/Feature%20engineering%20public%20outcome%20audit/).

| File | Contents |
|---|---|
| [`published_configuration_parameters.csv`](../research_notes/Feature%20engineering%20public%20outcome%20audit/published_configuration_parameters.csv) | Selected parameter/feature recipes linked to public scores, contact counts, competition and submission IDs |
| [`public_recipe_outcomes.csv`](../research_notes/Feature%20engineering%20public%20outcome%20audit/public_recipe_outcomes.csv) | All **92 relevant submitted files**, including every cutoff, seed-prefix/blend and calibration outcome |
| [`public_recipe_summary.csv`](../research_notes/Feature%20engineering%20public%20outcome%20audit/public_recipe_summary.csv) | Best submitted score and score at 9,000 contacts, grouped by recipe and competition |
| [`all_tested_parameter_configurations.csv`](../research_notes/Feature%20engineering%20public%20outcome%20audit/all_tested_parameter_configurations.csv) | **260 configuration records** across studies, including historical-only trials and explicit publication lineage; not a count of independent models |
| [`notebook_inventory.csv`](../research_notes/Feature%20engineering%20public%20outcome%20audit/notebook_inventory.csv) | Notebook hashes, source-match cells and executed-copy identification |
| `HT5955_all_hpo_trials.csv`, `HT5957_all_hpo_trials.csv`, `HT5959_all_hpo_trials.csv`, `HT5960_all_hpo_trials.csv` | Every recovered HPO setting: **20 / 8 / 76 / 50** historical evaluations, respectively |
| `source_manifest.json`, `verification.json`, `public_query_receipt.json` | Original paths/hashes, reconciliation assertions and fresh public-query coverage |

The collector scripts are `review_feature_engineering_history.R`,
`review_feature_public_submissions.py`, and `summarize_feature_public_history.py`.
They perform read-only historical/submission queries and write isolated audit
exports. No learner, Kaggle POST, or current-study change is involved.

## 1. Early controlled feature ablations — HT5945 / z500

`z500_Champion_Feature_Ablations.ipynb` held the binary learner fixed at
192 rounds, 52 leaves, minimum leaf 443, eta .04666, feature fraction .545,
bagging .786 and L2 8.7465. Six-month training windows, three original seeds and
four historical origins were used.

| Feature view | Width | Feature parameters | Public outcome |
|---|---:|---|---|
| Base | 278 | Existing calendar lags, deltas, prior summaries and coverage | No submission from this study |
| Relative | 326 | Relative deviations from prior means at windows 3/6, denominator floor 1, clipping ±10, near-zero flags | No submission |
| Trend | 314 | Relative three-month slope, acceleration and count of sequential declines | No submission |
| Combined | 362 | Relative + trend packages | No submission |

Its gain tables are explicitly retrospective historical diagnostics. They are not
public results for the four feature sets. The submitted earlier 278-feature
baseline is a separate recipe, not a public ablation of these additions.

## 2. Broad feature/model search — HT5954 / z523–z524

The actual five-family design contains **68 completed configurations**:
16 LightGBM binary, 16 LightGBM multiclass, 16 XGBoost binary, 16 XGBoost
multiclass and four ranger configurations, evaluated over four historical origins.
The retained run contains no fitted glmnet arm and no active RF-leaf feature arm.

### Feature variants actually present in the design

| Mode | Width | Definition |
|---|---:|---|
| `snapshot` | 152 | Original snapshot predictors |
| `base` | 278 | Original temporal representation |
| `semantic` | 290 | Base plus per-card utilization, minimum-payment/consumption ratios and status flags |
| `trend` | 314 | Base plus normalized slope/acceleration/decline features |
| `relative` | 326 | Base plus relative history and near-zero flags at windows 3/6 |
| `combined` | 362 | Relative + trend |
| `broad_history` | 638 | Expanded calendar history on the declared broad field set |
| `all_lags` | 850 | Broad lag1/2 and delta1/2 view derived from full-history cache |
| `full_history` | 1,914 | Expanded history over all 152 raw fields |
| `full_history_pruned` | Up to 640 | Training-only canary pruning retaining the 278-column base |

Full history adds lag1/2, delta1/2, OLS6, SMA3/6, min/max6 and EMA3/6 across raw
fields, avoiding duplicate base columns. Rich rolling statistics include the
current observation where declared; base `prior3/prior6` summaries exclude it.
All are causal covariate transformations, not future-label inputs.

Learner settings varied jointly with feature mode: rounds, eta, leaves/minimum
leaf (LightGBM), depth/minimum child weight/L1 (XGBoost), feature/row sampling,
L2, bins31/63 and forest settings. Training compared six-month controls with
expanding history from January2019; some designs used a three-month recency
half-life. The full design and actual observed ranges are exported separately.

**Important parameter-reading correction:** shared design rows contain generic
columns unused by a given backend. For example, a LightGBM row's `depth`,
`minchild` and `alpha` are XGBoost placeholders. They were not an applied
LightGBM depth/L1 search. The champion's actual native `max_depth` is −1 and
`lambda_l1` is 0. The combined configuration catalog filters backend-specific
parameters rather than treating every design column as effective.

### Selected recipe and public outcomes

The winning B model is LightGBM multiclass `full_history`, 192 rounds,
48 leaves, minimum leaf914, eta **.07591**, feature fraction **.815**,
bagging **.702**, L2 **28.7807**, max-bin31 and three original seeds
333803/333903/334003.

| Submitted complete recipe | Competition | Contacts | Public score | Submission |
|---|---|---:|---:|---:|
| A: five-family rank combination | Inicial | 11555 | 415.581 | 57871594 |
| **B: selected rich multiclass** | Inicial | 8277 | **437.081** | 57871595 |
| C: binary/multiclass probability combination | Inicial | 8878 | 426.831 | 57871596 |
| D: conservative multiclass policy | Inicial | 9769 | 417.748 | 57871599 |
| Same B file, original contact policy | Senior | 8277 | 437.081 | 57951977 |
| **Same B ranking, HT5958 contact policy** | Senior | 9000 | **453.831** | 57952401 |

HT5958's improvement is a contact-policy result on the same fitted ranking.
The remaining 67 design settings cannot each be assigned B's public score.
Likewise, the eventual success of the full-history recipe does not isolate the
causal contribution of every lag/statistic from learner/target/history changes.

## 3. Dedicated engineering and HPO — HT5955 / z526

The common baseline is **152 repaired raw predictors**, not the rich 1,914-column
champion. Six field/month outages were converted to NA before history creation.
All five packages were compared separately against this baseline with five paired
seeds on May. The probe was the fixed 192-round/52-leaf binary learner.

| Package | Added columns | Actual feature parameters | Public outcome for package alone |
|---|---:|---|---|
| `lag1_core` | 6 | Previous exact calendar month on six core fields | Not submitted |
| `delta1_core` | 6 | Current minus exact lag1 on those fields | Not submitted |
| `prior3_core` | 12 | Prior-only mean over 3 months, minimum2 known, plus coverage count | Not submitted |
| **`relative3_funds`** | **4** | Balance/payroll relative3, minimum2, floor1, clip±10, near-zero flags | Selected; final HPO/ensemble recipe submitted |
| `card_utilization` | 2 | Separate Visa/Master balance÷positive limit, clip±10 | Not submitted |

The six core fields were balance, payroll, quarterly activity, debit-card
transactions, Visa consumption and Master consumption. Near-zero flags apply to
the balance/payroll historical means. These are fixed definitions: this study
did **not** sweep every lag length, ratio clipping bound or support minimum.

### HPO and selected final recipe

All **20** actual parameter sets are in `HT5955_all_hpo_trials.csv`. Search bounds
were rounds64–384, eta.02–.10, leaves16–64, minimum leaf300–1500 and
feature fraction.5–1. Selected trial10:

| Parameter | Selected value |
|---|---:|
| Rounds | 308 |
| Learning rate | .0464871536065 |
| Leaves | 62 |
| Minimum leaf rows | 339 |
| Feature fraction | .600391357439 |
| Bagging / L2 / bins | .786 / 8.7465 / 31 |
| Final predictor count | 156 |
| Final ensemble | Five fixed master333803-derived seeds |

The selected recipe was refitted through July for September. **Only this final
ensemble** was public-scored; the nine files change contacts, not feature/HPO
configuration.

| Contacts | Inicial public score | Submission |
|---:|---:|---:|
|8000|366.081|57852521|
|8500|380.831|57852522|
|9000|389.998|57852524|
|9500|386.998|57852527|
|10000|390.081|57852528|
|10500|388.748|57852529|
|11000|396.581|57852530|
|**11500**|**401.915**|57852532|
|**12000**|**401.915**|57852534|

No HT5955 Senior submission appears in the complete queried history. The 86-item
proposal mentioned in older files was superseded before execution; it is not 86
publicly evaluated feature variants.

## 4. Drift/history extension — HT5956 / z527

The actual completed pilot used eight views, five paired seeds and May/July:
80 logical evaluations, including ten imported controls. It kept the same binary
192-round probe; no HPO or September/public stage was permitted.

| View | Width | Feature variation | Public score |
|---|---:|---|---|
|A_snapshot|152|Repaired raw control|None|
|B_funds3|156|Frozen relative3 funds package|None|
|C_snapshot_rank|156|Raw + signed within-month ranks of four monetary fields|None|
|D_funds3_rank|160|Funds3 + ranks|None|
|E_funds6|160|Funds3 + relative6/near-zero funds; minimum3 prior observations|None|
|F_usage3|162|Funds3 + relative3/near-zero debit/Visa/Master usage|None|
|G_prior_ema3|166|Funds3 + prior-only adjusted EMA3 and six-month coverage|None|
|H_rank_usage3|166|Funds3 + ranks + usage3|None|

Relative clipping stayed±10, floor1, relative3 minimum2 and relative6 minimum3.
EMA decay was.5, current observation excluded, minimum2 known past values;
exact calendar gaps determined decay. Ranks preserved sign/zero/NA and averaged
ties within same-month signed groups. These do not constitute an IPC experiment.

Longer funds history and usage were positive in both pilot origins; EMA's mean
historical signal was positive but not positive in both origins. **These are
historical findings only. No public score was measured for any of these eight
variants.** The broader `HT5956_EXPERIMENT_PLAN.json` is explicitly an unapproved
proposal, separate from this executed pilot.

## 5. Transfer onto the rich champion — HT5957 and HT5959

HT5957 tested R0(original), R1(repairs), R2(repairs+funds3/6),
R3(repairs+funds3+priorEMA3) and R4(the union) on the 1,914-column foundation.
R2 was selected, yielding1,922 columns. Eight subsequent multiclass HPO settings
are retained in `HT5957_all_hpo_trials.csv`. Winner8 used290rounds, eta
.083848810361,59leaves, minimumleaf805 and featurefraction.657992904354.
The study's final historical gate failed: **no HT5957 public submissions**.

The R2 representation/parameters were subsequently reused in HT5959, alongside
fresh B controls and B2/B12 targets. Both binary target winners selected V1,
the repaired1,922-column funds3/6 view. HT5959 ran76historical HPO tasks; it did
not publicly submit all76configurations.

### Actual Senior public outcomes

| Final ranking | Seeds | Feature/parameter bundle | Public @9000 | Best submitted public / contacts |
|---|---:|---|---:|---|
|Legacy B / HT5958|3 original|1914;192rounds/48leaves;eta.07591|**453.831**|**453.831 /9000**|
|Fresh B, W2|3 fresh|Same1914recipe,newseedensemble|439.081|441.914 /8500|
|Fresh B, W3|10 fresh|Same1914recipe,newseedensemble|449.248|449.248 /9000|
|R2, W2|3 fresh|1922;290rounds/59leaves;eta.0838488|439.331|439.331 /8500or9000|
|R2, W3|10 fresh|SameR2recipe,morefreshseeds|436.581|440.914 /10000|
|B2, W2|3 fresh|V1;512rounds/119leaves;eta.0160572,minleaf192|431.581|431.581 /9000|
|B2, W3|10 fresh|SameB2recipe|436.248|436.248 /9000|
|B12, W2|3 fresh|V1;405rounds/184leaves;eta.0288218,minleaf32|435.581|435.581 /9000|
|B12, W3|10 fresh|SameB12recipe|430.748|434.498 /8500|
|B+R2, W2|3/component|Blend of1914and1922recipes|446.164|446.164 /9000|
|B+R2, W3|10/component|Same recipe pair,morefreshseeds|447.081|448.831 /8500|
|B+B2, W3|10/component|RichMC + repaired/funds B2|449.414|449.414 /9000|

Full native parameter sets and all60public outcomes are in the linked tables.
In particular, more seeds were not uniformly better. The fresh ten-seed B was
not simply the old three champion models plus seven additions.

These public results evaluate complete recipes: R2 also changes learner
parameters, B2/B12 change targets, and seed schedules differ. They do not isolate
the public contribution of repairs or funds features alone.

## 6. Full Senior feature workflow — HT5960 / z535

This actually ran the full reference bundle:47-field/93-field-month NA repairs,
IPC normalization before feature construction, manual card/product/status ratios,
observed-row lags/deltas/trends,20×16 RF-leaf encoding and canary filtering.
The fitted representation retained **296 predictors, including21RF indicators**.

Fifty HPO configurations were evaluated. Selected transformed settings:
**1010rounds,2045leaves,eta.0161446376695,featurefraction.564485732367,
minimumHessian5.36913438594**. Main targetB12; final ensembletenfixedprime seeds.
See `HT5960_all_hpo_trials.csv` for all50actual configurations and transformed
parameters rather than mistaking log2 optimizer coordinates for native values.

Its nine Senior public scores, by contacts8000→12000 in500steps, were:
**431.581,436.248,447.998,445.831,439.164,439.748,432.914,428.164,421.831**.
Best **447.998@9000**, submission58036095, below HT5958 by5.833.

This is one complete-pipeline public test, not separate public tests of IPC,
repairs, product ratios, RF leaves or canary filtering.

## What this means for further feature work

- Generic lags, deltas, relative3/6, slopes, acceleration, EMA3/6, card ratios,
  monetary ranks, repairs and rich feature pruning have already appeared in
  executed studies. They should not be introduced as entirely unexplored ideas.
- We **do not have a public score for every feature family or parameter value**.
  In particular, funds6/rank/usage/EMA pilot variants were never individually
  public-scored. Missing public feedback is not an observed public failure.
- The strongest observed submitted recipe remains the rich HT5954/HT5958
  multiclass ranking. Its1,914features already contain substantial temporal
  engineering; the current HT5964 augmented stream adds14predictors to that base.
- Current HT5964 definitions are not identical reruns of HT5955: pooled rather
  than separate card ratios, clipping±20 rather than±10, and different historical
  support/near-zero treatment. Parameter/definition identity matters when using
  earlier outcomes to choose a next experiment.
- Many feature parameters were constants rather than searched dimensions:
  clip/floor/support rules and specific horizon choices were mostly fixed.
  The large prior searches predominantly tuned learner capacity/regularization
  and selected a feature bundle, rather than exhaustively tuning those formulas.

The catalog is therefore a concrete starting point for choosing nonduplicate
feature/parameter work, with public evidence attached only where it exists.
