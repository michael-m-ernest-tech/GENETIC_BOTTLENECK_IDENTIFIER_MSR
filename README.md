# EcoGen Diagnostics

EcoGen Diagnostics is a small conservation-genomics screening app. Upload a CSV of diploid genotypes to calculate observed heterozygosity (Ho), expected heterozygosity (He), and the requested Fis summary, then view a rule-based status card.

This folder is the GitHub repository root and the Vercel project root. Keep `api/`, `index.html`, `requirements.txt`, and `vercel.json` at the top level of the repo (do not nest them in a second folder).

## CSV format

Use one individual per row. Name each allele column `LocusX_A1` and `LocusX_A2`, where `X` is a locus number. The optional `Individual_ID` column is ignored by the calculations; other non-locus columns are also ignored. Missing calls are omitted for that locus, and every locus must have at least one complete genotype.

```csv
Individual_ID,Locus1_A1,Locus1_A2,Locus2_A1,Locus2_A2
IND-001,A,A,C,T
IND-002,A,G,C,C
IND-003,G,G,T,T
```

An example is included as [`sample-data.csv`](sample-data.csv). The upload limit is 4 MiB.

## Calculations and interpretation

- **Ho:** At each locus, the fraction of complete genotypes with different alleles; reported as an unweighted mean across loci.
- **He:** At each locus, `1 − Σ(pᵢ²)` from the pooled allele calls; reported as an unweighted mean across loci.
- **Fis:** `(He − Ho) / He`, calculated from the global Ho and He means. When He is zero, Fis is undefined and returned as JSON `null`.
- **Classification:** The app follows the requested rules: Ho > He → CRITICAL; otherwise Fis > 0.15 → WARNING; otherwise STABLE.

**Scientific limitation:** This is a screening demonstration, not a validated bottleneck test or conservation assessment. Ho > He here is not the same as a formal bottleneck heterozygosity-excess test. Published bottleneck methods compare observed heterozygosity against an expectation conditional on allele count under a mutation-drift equilibrium model, often across loci; this app does not model that expectation, test statistical significance, account for population structure or relatedness, or infer habitat condition. Fis can also be affected by population structure, sampling, null alleles, and genotyping error. Interpret the status with population-genetics expertise and independent evidence. See [Cornuet & Luikart (1996)](https://doi.org/10.1093/genetics/144.4.2001) for a formal heterozygosity-excess framework.

## Run locally

Install Python 3.10+ and the pinned packages:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

For local development, run the Flask app through a WSGI server or use the Vercel CLI (`vercel dev`) after linking the project. The API function is `api/index.py`; the browser UI is `index.html`.

## Publish with GitHub and deploy to Vercel

### 1. Create the GitHub repository

From this folder, after Git is initialized:

```bash
git init -b main
git add .
git commit -m "Initial commit: EcoGen Diagnostics Vercel app"
```

Create an empty public repository on GitHub named `ecogen-diagnostics` (no README, no .gitignore, no license — those files are already here). Then:

```bash
git remote add origin https://github.com/<your-username>/ecogen-diagnostics.git
git push -u origin main
```

### 2. Import the repo in Vercel

1. Sign in at [vercel.com](https://vercel.com) with the same GitHub account.
2. Choose **Add New → Project** and import `ecogen-diagnostics`.
3. Keep **Root Directory** at `./` (repository root).
4. Leave **Build Command** and **Output Directory** empty.
5. Framework preset can stay **Other**. Vercel uses `api/index.py` as a Python function and `requirements.txt` for dependencies (`runtime.txt` requests Python 3.12).
6. Deploy.

### 3. Confirm the live app

Open the deployment URL and upload [`sample-data.csv`](sample-data.csv). Then open `/api/health` on the same domain. A working backend returns `{"ok":true,"service":"EcoGen Diagnostics"}`.

Later pushes to `main` trigger a new Vercel production deploy automatically.

The project uses a Vercel rewrite for `/api/*` and a static `index.html` fallback. See [Vercel's Flask deployment guide](https://vercel.com/docs/frameworks/backend/flask) and [rewrite configuration reference](https://vercel.com/docs/routing/rewrites).

### Troubleshooting an upload

After deployment, open `/api/health` on the same domain. A working backend returns `{"ok":true,"service":"EcoGen Diagnostics"}`. A 404 or HTML page means the Python function or API rewrite is missing from that deployment. A 500 means the function started but failed; inspect the Vercel Function Logs. The upload UI reports the HTTP status and response content type when the server does not return JSON.

## Repository contents

```text
api/index.py                 Flask upload endpoint and analysis engine
index.html                   Responsive Tailwind-based interface
requirements.txt             Pinned Python dependencies
runtime.txt                  Python 3.12 for Vercel
vercel.json                  API and static-page rewrites
sample-data.csv               Example input file
generate_test_population.py  Optional larger test CSV generator
LICENSE                      MIT license
```
