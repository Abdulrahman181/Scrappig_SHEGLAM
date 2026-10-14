# Engineering review — Scrappig_SHEGLAM

**Review date:** 2026-10-14  
**Repository:** `Abdulrahman181/Scrappig_SHEGLAM`  
**Scope:** all tracked Python, Notebook, README, and repository-level dependency/config files.

## Executive summary

The repository contained a Streamlit dashboard and one large exploratory notebook, but no
requirements file, ignore rules, tests, or product CSV. The dashboard attempted to read
`sheglam_products.csv` at import time and would crash before showing an actionable message.
The notebook contained stale outputs and environment-specific paths from Windows and Colab.

The project is an exploratory scraping/analytics project, not a supervised ML training
pipeline. Consequently, there is no train/test split, model, or predictive metric to
validate. I did not invent a dataset, scrape the live site, or report analytics results.

## Work completed

- Added `data_utils.py` as the single CSV boundary. It resolves paths, checks the required
  six-column schema, rejects empty/unusable files, normalises prices and best-seller flags,
  bounds ratings to `0..5`, and converts invalid source values to missing rather than
  silently guessing replacements.
- Refactored `app.py` to use a repository-relative default or `SHEGLAM_DATA_PATH`, fail
  closed with a clear Streamlit message when data is missing/invalid, and guard empty
  selections, all-missing numeric columns, empty groupings, missing collection matches,
  and missing optional WordCloud support. Plot figures are closed after rendering.
- Replaced the 46-cell historical notebook with a seven-cell, output-free, reproducible
  analysis notebook using the same loader. Removed stale results, the Windows
  `chromedriver` path, `/content/SHEGLAM.csv`, local MongoDB insertion, and references to
  unavailable image artifacts. No credentials or generated data were retained.
- Added `requirements.txt` with bounded runtime dependencies. `pymongo` is documented as
  optional/commented because database export is not part of the supported dashboard path.
- Added `.gitignore` rules for scraped CSVs, generated images, notebook checkpoints,
  environments, caches, and local configuration.
- Added three offline tests in `tests/test_data_utils.py` covering type normalisation,
  missing-data messaging, and schema rejection.
- Added `validate_project.py` for lightweight AST and notebook-JSON checks.
- Rewrote `README.md` with the data contract, setup commands, reproducibility limitations,
  and explicit no-fabrication behavior.

## Findings and risk assessment

### Fixed — high impact

1. **Missing artifact crash:** the original `app.py` used a bare `pd.read_csv("sheglam_products.csv")`.
   The CSV is not present in the repository. The new loader stops with an actionable error.
2. **Missing dependency declaration:** imports included Streamlit, Plotly, Seaborn, and
   WordCloud without `requirements.txt`. A bounded requirements file is now present.
3. **Hard-coded local paths:** the notebook referenced a Windows ChromeDriver path and a
   Colab `/content` CSV path. Both were removed.
4. **Stale notebook state:** the original notebook had 46 cells, 40 stored outputs, image
   references, a localhost MongoDB insert, and stateful cells that produced undefined-name
   reports when checked independently. The notebook is now output-free and self-contained
   around the validated data boundary.
5. **Fragile empty-data behavior:** the dashboard used positional indexing (`iloc[0]`),
   `idxmin`, and unconditional WordCloud/chart generation. These paths are now guarded.
6. **Schema/type assumptions:** prices, ratings, and flags were cast without error handling.
   The loader now validates columns and performs explicit, non-fabricating coercion.

### Reviewed — no model leakage claim

- No model training, target construction, train/test split, cross-validation, or predictive
  metric exists in the repository. Therefore a leakage audit for a predictive pipeline is
  not applicable; the report and README do not claim model performance.
- The dashboard is descriptive and computes statistics only from the supplied CSV. Best
  Seller is treated as a source field, not as a model target.

### Security/API review

- No API keys, passwords, or committed credentials were found in the inspected source.
- The original notebook's MongoDB insertion was removed from the supported workflow; no
  network/database side effect occurs during dashboard import.
- The Streamlit app accepts only a configured local path through `SHEGLAM_DATA_PATH`; it
  does not execute CSV contents or build shell commands from user input.
- Selenium collection remains site-dependent and is not executed by the dashboard. Its
  selectors should be revalidated against SHEGLAM before a fresh collection.

## Validation performed

- `python -m pytest -q` — **3 passed**.
- `ruff check app.py data_utils.py validate_project.py tests /tmp/sheglam_notebook_combined.py` — **passed**.
- `python validate_project.py` — **passed** (AST and Notebook JSON).
- `python -m compileall -q app.py data_utils.py validate_project.py tests` — **passed**.
- Notebook inspection — **0 stored outputs**, no Windows/Colab paths, no MongoDB localhost
  reference, no image artifact references.
- `git diff --check` — **passed**.

## Limitations and unexecuted paths

- No `sheglam_products.csv` or `SHEGLAM.csv` exists in the checkout, so no full dashboard
  run or data-dependent analysis was performed. This is intentional; no data was invented.
- The sandbox has pandas, matplotlib, Seaborn, Plotly, and pytest, but does not have the
  declared `streamlit`, `wordcloud`, `selenium`, or `nbformat` packages installed. The
  dependency declaration was added, but those heavy/runtime paths were not claimed as
  executed.
- The live website was not scraped. Selenium behavior and current CSS selectors therefore
  remain unverified against the live site.
- The PDF was treated as a reference artifact and was not modified.

## Commit policy

A local commit was created only in this checkout. No changes were pushed to GitHub and no
other repository was modified.
