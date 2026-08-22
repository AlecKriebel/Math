#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PUB="$ROOT/public/repository"
DATAZIP="$ROOT/public/data_archive/final_release_data.zip"
export SOURCE_DATE_EPOCH=1786752000 TZ=UTC LC_ALL=C PYTHONOPTIMIZE=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1

copy_files() {
  local srcroot="$1" dstroot="$2"; shift 2
  for rel in "$@"; do
    mkdir -p "$dstroot/$(dirname "$rel")"
    cp -a "$srcroot/$rel" "$dstroot/$rel"
  done
}

# ---------- portable public repository: strict allowlist ----------
rm -rf "$PUB" "$ROOT/public/data_archive"
mkdir -p "$PUB" "$ROOT/public/data_archive"
copy_files "$ROOT" "$PUB" LICENSE CITATION.cff RESEARCH_LOG.md requirements.txt

cat > "$PUB/README.md" <<'EOF'
# Exact Diffusion Design for Maximally Collective Stable Turing Patterns

Portable exact source, proof certificates, independent verifiers, current-profile numerical illustrations, and manuscript sources for the corrected final release.

The immutable version 1.0.7 snapshot is published at
<https://github.com/AlecKriebel/Math/releases/tag/maximally-collective-stable-turing-v1.0.7>;
archived versions share <https://doi.org/10.5281/zenodo.21753404>.  The exact
preceding version 1.0.6 snapshot has DOI <https://doi.org/10.5281/zenodo.22058969>;
the v1.0.7 release record carries its own immutable version DOI once minted.

## Replay

```bash
bash replay.sh
```

The full command regenerates the current exact finite data, verifies the all-dimensional certificates, reruns mutation tests and numerical illustrations, rebuilds all four figures, and compiles the manuscript and supplement. Numerical illustrations are not used in any proof.

`verification_outputs/` records the current repair campaign, and
`sha256_manifest.txt` verifies the initially downloaded tree. Running the
replay regenerates both for the local toolchain.
EOF
cat > "$PUB/CERTIFICATES.md" <<'EOF'
# All-dimensional proof certificates

The all-dimensional arguments are human-readable in `proof_audit/` and checked by these exact commands:

- `python independent_verifier/verify_all_spectrum.py`
- `python independent_verifier/verify_principal_minor_diffusion_ray.py`
- `python independent_verifier/verify_network_one_bad_minor.py`
- `python independent_verifier/dd_verify_order_m_minors.py`
- `python independent_verifier/dd_verify_diffusion_criterion.py`
- `python independent_verifier/dd_verify_contrast_bounds.py`
- `python independent_verifier/dd_verify_mode_isolation.py`
- `python independent_verifier/dd_verify_harmonic_corrections.py`
- `python independent_verifier/dd_verify_cubic_sign.py`
- `python independent_verifier/frontier_verify_mode_certificates.py`
- `python independent_verifier/frontier_verify_master_certificate.py`
- `python independent_verifier/frontier_verify_near_threshold.py`
- `python independent_verifier/frontier_verify_cubic_bound.py`
- `python independent_verifier/frontier_verify_determinant_identity.py`
- `python independent_verifier/frontier_verify_exposition_identities.py`
- `python independent_verifier/verify_symbolic_certificates.py`

Printed coefficient tables are `data/certificate_tables.tex`, `data/sign_certificate_tables.tex`, and `data/triad_routh_gap.tex`. The single exact source for all displayed finite values is `data/current_profile_exact.json`. Finite instances are regression checks, not replacements for the symbolic proof.
EOF

COMPUTATION=(
  computation/audit_manuscript.py
  computation/audit_numerical_provenance.py
  computation/audit_pdfs.py
  computation/audit_stale_claims.py
  computation/generate_current_profile_data.py
  computation/generate_tables.py
  computation/generate_sign_certificate_tables.py
  computation/export_instance.py
  computation/export_pareto_instance.py
  computation/simulations.py
  computation/tests/test_flagship.py
)
copy_files "$ROOT" "$PUB" "${COMPUTATION[@]}"

mkdir -p "$PUB/independent_verifier"
rsync -a --delete --exclude='__pycache__/' --exclude='*.pyc' "$ROOT/independent_verifier/" "$PUB/independent_verifier/"
mkdir -p "$PUB/proof_audit" "$PUB/literature"
rsync -a --delete "$ROOT/proof_audit/" "$PUB/proof_audit/"
rsync -a --delete "$ROOT/literature/" "$PUB/literature/"

DATA_FILES=(
 data/README.md
 data/current_profile_exact.json
 data/contrast_table.tex
 data/certificate_tables.tex
 data/sign_certificate_tables.tex
 data/triad_routh_gap.tex
 data/branch_amplitudes.csv
 data/refinement_checks.csv
 data/simulation_parameters.json
 data/network_instances/Nhat_m3.json
 data/network_instances/Nhat_m4.json
 data/network_instances/Nhat_m5.json
 data/network_instances/Nhat_m6.json
 data/network_instances/Nhat_m8.json
 data/network_instances/Nhat_m10.json
 data/exact_instances/pareto_m3_L0.json
 data/exact_instances/pareto_m4_L0.json
)
copy_files "$ROOT" "$PUB" "${DATA_FILES[@]}"
mkdir -p "$PUB/data/simulations"
rsync -a --delete "$ROOT/data/simulations/" "$PUB/data/simulations/"

FIG_FILES=(
 figures/network_family.tex
 figures/network_family_standalone.tex
 figures/network_family.pdf
 figures/stable_tradeoff.py
 figures/stable_tradeoff.pdf
 figures/stable_profiles.py
 figures/stable_profiles.pdf
 figures/amplitude_scaling.py
 figures/amplitude_scaling.pdf
)
copy_files "$ROOT" "$PUB" "${FIG_FILES[@]}"

MANUSCRIPT_FILES=(
 manuscript/main.tex manuscript/supplement.tex manuscript/references.bib
 manuscript/main.bbl manuscript/main.pdf manuscript/supplement.pdf
)
copy_files "$ROOT" "$PUB" "${MANUSCRIPT_FILES[@]}"
copy_files "$ROOT" "$PUB" external_audit/theorem_summary.tex external_audit/proof_skeleton.tex

cat > "$PUB/replay.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
export PYTHONOPTIMIZE=0
export PYTHONHASHSEED=0 MPLBACKEND=Agg SOURCE_DATE_EPOCH=1786752000 FORCE_SOURCE_DATE=1 TZ=UTC LC_ALL=C
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
required_commands=(python pdflatex biber pdffonts sha256sum awk grep find sort xargs tail)
for command_name in "${required_commands[@]}"; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'missing required command: %s\n' "$command_name" >&2
    exit 2
  fi
done
python - <<'PY'
import importlib
import re
import sys

if sys.flags.optimize:
    raise SystemExit("replay requires Python assertions; do not use -O")
minimums = {
    "matplotlib": (3, 7), "numpy": (1, 24), "pandas": (2, 0),
    "pypdf": (6, 0), "pytest": (8, 0), "scipy": (1, 10), "sympy": (1, 12),
}
for name, required in minimums.items():
    module = importlib.import_module(name)
    match = re.match(r"(\d+)\.(\d+)", module.__version__)
    if match is None or tuple(map(int, match.groups())) < required:
        raise SystemExit(f"{name} {module.__version__} is below {required}")
    print(f"PYTHON_PACKAGE={name}=={module.__version__}")
PY
OUT="$ROOT/verification_outputs"
mkdir -p "$OUT" data/network_instances data/exact_instances

echo '[1/8] current exact source and tables'
python computation/generate_current_profile_data.py
python computation/generate_tables.py
python computation/generate_sign_certificate_tables.py

echo '[2/8] exact tests and source audits'
python -m pytest -q computation/tests > "$OUT"/pytest.txt
python computation/audit_manuscript.py > "$OUT"/manuscript_audit.txt
python independent_verifier/verify_current_numerical_provenance.py > "$OUT"/detached_numerical_provenance.txt
python independent_verifier/verify_symbolic_certificates.py > "$OUT"/symbolic_certificates.txt

echo '[3/8] integrated exact designs'
rm -f "$OUT/integrated_designs.txt"
python independent_verifier/verify_improved_profile.py >> "$OUT"/integrated_designs.txt
python independent_verifier/frontier_verify_family.py 3 4 5 6 8 10 >> "$OUT"/integrated_designs.txt
python independent_verifier/frontier_verify_normal_form.py 3 >> "$OUT"/integrated_designs.txt
python independent_verifier/frontier_verify_pareto.py 3 4 5 6 8 10 149 >> "$OUT"/integrated_designs.txt
python independent_verifier/verify_exchange_of_stability.py >> "$OUT"/integrated_designs.txt
python independent_verifier/verify_branch_stability.py >> "$OUT"/integrated_designs.txt

echo '[4/8] finite regression instances'
for m in 3 4 5 6 8 10; do python computation/export_instance.py "$m" --out "data/network_instances/Nhat_m${m}.json" >/dev/null; done
python computation/export_pareto_instance.py 3 --out data/exact_instances/pareto_m3_L0.json >/dev/null
python computation/export_pareto_instance.py 4 --out data/exact_instances/pareto_m4_L0.json >/dev/null

echo '[5/8] current-profile numerical illustrations'
if [[ "${FINAL_RELEASE_QUICK:-0}" == 1 ]]; then
  rm -rf data/simulations_quick
  python computation/simulations.py --quick --outdir data/simulations_quick > "$OUT"/simulations_quick.txt
else
  rm -rf data/simulations
  python computation/simulations.py --outdir data/simulations --jobs 3 > "$OUT"/simulations.txt
  python computation/audit_numerical_provenance.py > "$OUT"/numerical_provenance.txt
fi

echo '[6/8] figures'
python figures/stable_tradeoff.py
if [[ "${FINAL_RELEASE_QUICK:-0}" != 1 ]]; then
  python figures/stable_profiles.py
  python figures/amplitude_scaling.py
fi
(cd figures && pdflatex -interaction=nonstopmode -halt-on-error network_family_standalone.tex >/dev/null && cp network_family_standalone.pdf network_family.pdf)

echo '[7/8] manuscript and supplement'
(
 cd manuscript
 pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
 biber main >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
)
for f in manuscript/main.log manuscript/supplement.log; do
  ! grep -Eiq 'undefined references|undefined citations|LaTeX Warning: Reference|Overfull \\hbox' "$f"
done

echo '[8/8] portability, PDF, and manifest'
for f in manuscript/main.pdf manuscript/supplement.pdf figures/network_family.pdf figures/stable_tradeoff.pdf figures/stable_profiles.pdf figures/amplitude_scaling.pdf; do test -s "$f"; done
for f in manuscript/main.pdf manuscript/supplement.pdf; do pdffonts "$f" | tail -n +3 | awk 'NF && $5!="yes" {bad=1} END{exit bad}'; done
python computation/audit_pdfs.py --profile public > "$OUT"/pdf_semantic_audit.txt
if grep -RIl --include='*.py' --include='*.md' --include='*.tex' --include='*.json' --include='*.sh' '/mnt/data/' . | grep -v '^./replay.sh$' | grep .; then exit 1; fi
if [[ "${FINAL_RELEASE_QUICK:-0}" == 1 ]]; then
  rm -rf data/simulations_quick data/branch_amplitudes_quick.csv data/refinement_checks_quick.csv
  rm -f "$OUT/simulations_quick.txt"
fi
rm -f figures/contrast_table.csv figures/stable_tradeoff.png \
  figures/stable_profiles.png figures/amplitude_scaling.png \
  figures/network_family_standalone.pdf
rm -rf .pytest_cache
find . -type d -name '__pycache__' -prune -exec rm -rf {} +
find . -type f \( -name '*.aux' -o -name '*.log' -o -name '*.bcf' -o -name '*.blg' -o -name '*.fls' -o -name '*.fdb_latexmk' -o -name '*.run.xml' -o -name '*.out' -o -name '*.toc' -o -name '*.xdv' \) -delete
find . -type f ! -path './.pytest_cache/*' ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '*.aux' ! -name '*.log' ! -name '*.bcf' ! -name '*.blg' ! -name '*.fls' ! -name '*.fdb_latexmk' ! -name '*.run.xml' ! -name '*.out' ! -name '*.toc' ! -name '*.xdv' ! -name 'sha256_manifest.txt' -print0 | sort -z | xargs -0 sha256sum > sha256_manifest.txt
grep -Fq '  ./RESEARCH_LOG.md' sha256_manifest.txt
sha256sum -c sha256_manifest.txt >/dev/null
echo PUBLIC_REPLAY_PASS
EOF
chmod +x "$PUB/replay.sh"

# Current portable evidence and an initial self-verifying manifest. The replay
# regenerates these files for a downloader's own toolchain.
VERIFICATION_FILES=(
  detached_numerical_provenance.txt
  integrated_designs.txt
  manuscript_audit.txt
  numerical_provenance.txt
  pdf_semantic_audit.txt
  principal_minor_diffusion_ray.txt
  pytest.txt
  simulations.txt
  stale_claim_audit.txt
  symbolic_certificates.txt
)
copy_files "$ROOT/release/verification_outputs" "$PUB/verification_outputs" "${VERIFICATION_FILES[@]}"
PUBLIC_PDF_PREFLIGHT_FILES=(
  SUMMARY.txt
  manuscript_main_pdf.txt
  manuscript_supplement_pdf.txt
  figures_network_family_pdf.txt
  figures_stable_tradeoff_pdf.txt
  figures_stable_profiles_pdf.txt
  figures_amplitude_scaling_pdf.txt
)
copy_files "$ROOT/release/pdf_preflight" "$PUB/verification_outputs/pdf_preflight" \
  "${PUBLIC_PDF_PREFLIGHT_FILES[@]}"
(
  cd "$PUB"
  find . -type f ! -path './.pytest_cache/*' ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '*.aux' ! -name '*.log' ! -name '*.bcf' ! -name '*.blg' ! -name '*.fls' ! -name '*.fdb_latexmk' ! -name '*.run.xml' ! -name '*.out' ! -name '*.toc' ! -name '*.xdv' ! -name 'sha256_manifest.txt' -print0 | sort -z | xargs -0 sha256sum > sha256_manifest.txt
  grep -Fq '  ./RESEARCH_LOG.md' sha256_manifest.txt
  sha256sum -c sha256_manifest.txt >/dev/null
)

# ---------- open data archive ----------
python "$ROOT/release/deterministic_zip.py" "$ROOT/data" "$DATAZIP"

# ---------- self-contained submission source bundles ----------
prepare_source() {
  local base="$1"
  rm -rf "$base"
  mkdir -p "$base/figures" "$base/data"
  cp "$ROOT/manuscript/main.tex" "$base/main.tex"
  cp "$ROOT/manuscript/supplement.tex" "$base/supplement.tex"
  cp "$ROOT/manuscript/references.bib" "$base/references.bib"
  cp "$ROOT/manuscript/main.bbl" "$base/main.bbl"
  cp "$ROOT/figures/network_family.tex" "$base/figures/"
  cp "$ROOT/figures/stable_tradeoff.pdf" "$ROOT/figures/stable_profiles.pdf" "$base/figures/"
  cp "$ROOT/data/contrast_table.tex" "$ROOT/data/certificate_tables.tex" "$ROOT/data/sign_certificate_tables.tex" "$ROOT/data/triad_routh_gap.tex" "$base/data/"
  python - "$base" <<'PY'
from pathlib import Path
import sys
base=Path(sys.argv[1])
for fn in ('main.tex','supplement.tex'):
    p=base/fn
    p.write_text(p.read_text().replace('../figures/','figures/').replace('../data/','data/'))
PY
}
for base in "$ROOT/submission/biorxiv/source" "$ROOT/submission/arxiv/source" "$ROOT/submission/journal/source"; do prepare_source "$base"; done
# Let arXiv's selected TeX Live toolchain run Biber against its own biblatex
# version rather than shipping a potentially format-incompatible .bbl file.
rm -f "$ROOT/submission/arxiv/source/main.bbl"
cp "$ROOT/manuscript/main.pdf" "$ROOT/submission/biorxiv/manuscript.pdf"
cp "$ROOT/manuscript/supplement.pdf" "$ROOT/submission/biorxiv/supplement.pdf"
cp "$ROOT/manuscript/main.pdf" "$ROOT/submission/journal/manuscript.pdf"
cp "$ROOT/manuscript/supplement.pdf" "$ROOT/submission/journal/supplement.pdf"
python "$ROOT/release/deterministic_zip.py" "$ROOT/submission/biorxiv/source" "$ROOT/submission/biorxiv/source_package.zip"
python "$ROOT/release/deterministic_zip.py" "$ROOT/submission/arxiv/source" "$ROOT/submission/arxiv/arxiv_source.zip"
python "$ROOT/release/deterministic_zip.py" "$ROOT/submission/journal/source" "$ROOT/submission/journal/source_package.zip"

# ---------- external specialist packets ----------
MIN="$ROOT/external_audit/minimal_verifier"
rm -rf "$MIN"
mkdir -p "$MIN"
rsync -a --exclude='__pycache__/' --exclude='*.pyc' "$ROOT/independent_verifier/" "$MIN/"
cat > "$MIN/replay.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONOPTIMIZE=0
python - <<'PY'
import sys
if sys.flags.optimize:
    raise SystemExit("replay requires Python assertions; do not use -O")
PY
python verify_principal_minor_diffusion_ray.py
python verify_symbolic_certificates.py
python verify_improved_profile.py
python frontier_verify_family.py 3 4 5 6 8 10
python frontier_verify_normal_form.py 3
python frontier_verify_pareto.py 3 4 5 6 8 10 149
python verify_exchange_of_stability.py
python verify_branch_stability.py
echo MINIMAL_VERIFIER_PASS
EOF
chmod +x "$MIN/replay.sh"
cat > "$MIN/README.md" <<'EOF'
# Minimal exact verifier

Run `bash replay.sh`. It reconstructs the family and checks the generalized principal-minor diffusion-ray theorem, network-specific omission table and diffusion law, all-spectrum localization, current stable unit design, equilibrium-scaled stable family, cubic signs, and exchange of stability. It imports no discovery-side implementation.
EOF

PACKROOT="$ROOT/external_audit/packets"
rm -rf "$PACKROOT"
mkdir -p "$PACKROOT"
for kind in reaction_network pde symbolic; do
  p="$PACKROOT/$kind"; mkdir -p "$p"
  cp "$ROOT/external_audit/theorem_summary.pdf" "$ROOT/external_audit/proof_skeleton.pdf" "$p/"
  cp "$ROOT/figures/network_family.pdf" "$p/"
  cp "$ROOT/data/network_instances/Nhat_m3.json" "$ROOT/data/network_instances/Nhat_m4.json" "$p/"
  cp "$ROOT/data/exact_instances/pareto_m3_L0.json" "$ROOT/data/exact_instances/pareto_m4_L0.json" "$p/"
  cp -a "$MIN" "$p/minimal_verifier"
done
cat > "$PACKROOT/reaction_network/questions.md" <<'EOF'
# Reaction-network and Turing audit questions

1. Is the all-m SCC exhaustion complete, including the edge loss at `b=2a`?
2. Does the complete positive-flux parametrization capture every positive-equilibrium Jacobian?
3. Are the order-(n-1) omission table and exact factor-eight stationary diffusion law correct?
4. Is the endpoint `n-1` positioned accurately relative to published unstable-subsystem theory?
EOF
cat > "$PACKROOT/pde/questions.md" <<'EOF'
# PDE bifurcation and stability audit questions

1. Is the physical scaling `\widehat x=Hx`, `D_phys=H Delta`, and the placement of `(1-mu)` in the scaled PDE correct?
2. Is the semipositive fixed-integrated-mass Fredholm and zero-mode gauge formulation correct?
3. Are the Fourier factors and cubic contraction normalized correctly?
4. Do the sectorial and spectral hypotheses justify local exponential convergence in fixed-mass `H^1`?
EOF
cat > "$PACKROOT/symbolic/questions.md" <<'EOF'
# Symbolic and algebraic audit questions

1. Is the generalized principal-minor derivative monotonicity proof valid under its stated coefficient hypotheses?
2. Are the complete omission-minor table and factor-eight mechanism correct?
3. Does the 22-term homogeneous certificate control the actual determinant
   `QF-R`, and does it correctly reject the superseded `1/sqrt(3 nu)` endpoint?
4. Are the equality cases in the 22-, 35-, 77-, and 84-term certificates correct?
5. Is the gauge comparison `N_m(L)>1/200` a valid all-m cubic-sign proof?
EOF
for kind in reaction_network pde symbolic; do
  python "$ROOT/release/deterministic_zip.py" "$PACKROOT/$kind" "$PACKROOT/${kind}_audit_packet.zip"
done

(
  cd "$ROOT"
  sha256sum \
    public/data_archive/final_release_data.zip \
    submission/biorxiv/source_package.zip \
    submission/arxiv/arxiv_source.zip \
    submission/journal/source_package.zip \
    external_audit/packets/reaction_network_audit_packet.zip \
    external_audit/packets/pde_audit_packet.zip \
    external_audit/packets/symbolic_audit_packet.zip \
    > release/BUNDLE_SHA256.txt
  sha256sum -c release/BUNDLE_SHA256.txt >/dev/null
)

echo PACKAGES_REFRESHED
