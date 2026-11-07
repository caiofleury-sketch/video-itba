We are producing a short presentation about the features we added. We need controlled, interpretable business results in millions of Argentine pesos, rather than trying to convert AUC into money. Locate the artifacts locally or in the cloud, prepare the comparisons below, and submit exactly two new CSVs to Kaggle.

## Sources and existing reference

Read these files and reconcile them with the actual stored artifacts:

- `Feature engineering parameters and public outcomes.md`, especially sections 3 (HT5955) and 4 (HT5956).
- `published_configuration_parameters.csv`, `public_recipe_outcomes.csv`, and `all_tested_parameter_configurations.csv` under `research_notes/Feature engineering public outcome audit/`.
- `z526_HT5955_Ingenieria_Variables_HPO.ipynb`.
- `z527_HT5956_Drift_History_Pilot.ipynb` and its executed `E_funds6` definition. Use that executed feature definition, not the broader unapproved `HT5956_EXPERIMENT_PLAN.json`.

The competition is **`data-mining-inicial-2026-c`**, not Senior. Predict BAJA+2 for the September 2021 snapshot: Premium-package exit during November 2021.

The existing reference is HT5955 `relative3_funds_HPO_winner`: 152 repaired raw predictors plus four relative3-funds columns, 156 predictors total. Reuse **`HT5955_contacts_11500.csv`**, submission **57852532**, public score **401.915**, as the middle/control recipe. It selected exactly **11,500 contacts**. Do not spend a submission reuploading an identical file.

The notebook specifies these lookup locations; discover their actual local/cloud equivalents rather than assuming they all exist:

- Cloud output: `/content/buckets/b1/exp/HT5955/feature_development_v1/`.
- Bucket equivalent: `gs://cfleuryrangelteixei_buckito2026/exp/HT5955/feature_development_v1/`.
- Local output: `exp/HT5955/local_full_v1/`.
- Artifacts: `contract.rds`, `feature_freeze.rds`, `feature_comparison.rds`, `hpo/winner.rds`, `september_ensemble.rds`, `submission_manifest.rds`, `submissions/HT5955_contacts_11500.csv`, and native models/results indexed by `seed_keys`.
- Input configured in the cloud: `/content/buckets/b1/datasets/analistasr_competencia_2026.csv`; local equivalent: `analistasr_competencia_2026.csv`.

## The two new submissions

**1. Matched snapshot-only ablation — 152 predictors.**

Start from the exact HT5955 final recipe, remove only the four `relative3_funds` additions, and retrain with the same final learner settings, training rows, repair policy, and five seeds. Keep the raw balance/payroll predictors. This is the executed `snapshot152_repaired` feature view evaluated under the frozen HT5955 final settings.

Suggested filename: `HT5955_ablation_snapshot152_matched_contacts_11500.csv`.

Compare its public score with existing submission 57852532 to measure the added relative3-funds package under that fixed recipe.

**2. Matched funds3 + funds6 extension — 160 predictors.**

Start from the same 156-predictor reference and add only the four relative6/near-zero balance/payroll columns from HT5956 **`E_funds6`**, whose reference was **`B_funds3`**. Preserve relative3 and append the relative6 additions. Use the same frozen final learner settings and five seeds as the reference.

Suggested filename: `HT5955_ablation_funds3_funds6_matched_contacts_11500.csv`.

Compare its public score with existing submission 57852532 to measure the incremental six-month package on top of relative3.

## Freeze the comparison

- Reuse the actual HT5955 HPO winner, trial 10: binary LightGBM, `num_iterations=308`, `learning_rate=0.04648715360654122`, `num_leaves=62`, `min_data_in_leaf=339`, `feature_fraction=0.6003913574386388`, `bagging_fraction=0.786`, `bagging_freq=1`, `lambda_l2=8.7465`, and `max_bin=31`. Recover every other native setting from the stored contract/models. Do not substitute the HT5956 192-round pilot probe.
- Recover the exact five seeds from the original HT5955 contract/final tasks, derived from master 333803. Preserve all seed-related native parameters. Average the five predicted probabilities as the original notebook does; do not average ranks or choose the best seed.
- Keep the original eligible training rows/labels through July 2021 and September scoring population. Preserve preprocessing, feature order within each defined view, missing-value treatment, and the six approved field/month outage repairs applied before feature construction. No inflation/IPC normalization or unrelated repairs/features.
- Relative3 uses the prior three calendar months, at least two finite observations, scale floor 1, clipping ±10, and near-zero flags for balance/payroll. Relative6 uses the executed prior-six-calendar-month definition, minimum three known observations, the same floor/clipping, and its near-zero flags. Preserve the original exclusion of the current observation in these historical references and the existing handling of calendar gaps/missingness.
- Fix exactly 11,500 selected contacts for all three recipes. Use the original `h55_submissions()` ordering: descending ensemble probability, tie-break ascending `numero_de_cliente`; write all rows sorted by customer ID, with columns `numero_de_cliente,Predicted` and binary predictions. Derive the required customer population from the actual data/submission schema; the pasted competition description contains inconsistent row counts.
- Reuse compatible cached predictions/models where possible; fit only missing matched final ensembles. No new HPO, seed search, cutoff sweep, target change, calibration, blending, or additional feature bundles. Document that the settings were originally selected for relative3: these ablations measure feature changes conditional on those settings, not each view after separate tuning.

Verify that the recovered reference reproduces its original predictions, ranking, contact selection, and recorded file hash before treating its existing score as a matched control. If its provenance cannot be established, report the exact gap before uploading; do not silently substitute an unrelated baseline or consume extra submission slots.

Use a new output namespace, preserving original artifacts, notebooks, checkpoints, and running jobs. Do not run the original notebook unchanged with uploads enabled: its normal upload path sends nine cutoff files. Submit only the two specifically named new files. Reuse existing Kaggle authentication. Check for identical already-submitted files and never blindly retry an ambiguous submission.

## Return the evidence

1. `public_feature_ablation_results.csv`: three rows, including the existing reference, with recipe, feature count, contact count, submission ID, status, public score in million ARS, whether it was newly submitted, and artifact path/hash.
2. Report these contrasts explicitly:
   - Relative3 package: `401.915 − matched_snapshot_public_score`.
   - Additional relative6 package: `matched_funds3_funds6_public_score − 401.915`.
   - Optionally, combined change versus snapshot: `matched_funds3_funds6_public_score − matched_snapshot_public_score`.
3. A compact manifest of full native parameters, seeds, training/data identity, exact predictor lists, reference checks, and submission receipts. Describe both the direction and size of observed score differences without claiming statistical significance or actual realized retention profit.
4. Recover and export the existing historical feature-profit evidence as well, without additional Kaggle submissions or another experiment search. Use HT5955 `feature_comparison.rds` / `HT5955_feature_summary.csv`, and HT5956 `HT5956_summary.csv` plus available per-month/per-seed results. Include all tested views, especially monetary ranks, funds6, usage3, and EMA. Export study, feature view, reference view, month, seed (when available), population size, contact policy/count, profit and reference profit in ARS, paired difference, AUC, and source artifact. If cached predictions/labels permit common-policy rescoring, identify it explicitly; never compare amounts across different populations, policies, or references without labeling them. Preserve absent values as missing rather than zero.

The competition defines gain as +975,000 ARS for contacting a BAJA+2, −25,000 ARS for contacting another class, and zero for not contacting. Report the Kaggle public score as returned: it is already expressed in million ARS and scaled from the public subset. Do not apply another 1/0.30 adjustment, infer an exact customer-retention count, or invent an AUC-to-pesos conversion. The two new submissions can support monetary contrasts for these specific packages; they do not establish public outcomes for all nine feature families.
