#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
export PYTHONOPTIMIZE=0
export PYTHONHASHSEED=0 MPLBACKEND=Agg SOURCE_DATE_EPOCH=1787443200 FORCE_SOURCE_DATE=1 TZ=UTC LC_ALL=C
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
required_commands=(python bash pdflatex biber kpsewhich pdffonts pdftotext sha256sum awk grep find sort xargs tail cmp mktemp)
for command_name in "${required_commands[@]}"; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'missing required command: %s\n' "$command_name" >&2
    exit 2
  fi
done
bash environment/check_toolchain.sh

# Verify and preserve the downloaded release manifest before any generators
# run.  Exact regenerated artifacts are later checked against selected entries
# from this baseline; local tree hashes go to a different file.
BASELINE_MANIFEST="$ROOT/sha256_manifest.txt"
if [[ ! -f "$BASELINE_MANIFEST" ]]; then
  printf '%s\n' 'missing shipped sha256_manifest.txt' >&2
  exit 2
fi
sha256sum -c "$BASELINE_MANIFEST" >/dev/null
grep -Fq '  ./RESEARCH_LOG.md' "$BASELINE_MANIFEST"
REPLAY_STATE="$(mktemp -d "${TMPDIR:-/tmp}/exact-diffusion-public-replay.XXXXXX")"
trap 'rm -rf "$REPLAY_STATE"' EXIT
cp "$BASELINE_MANIFEST" "$REPLAY_STATE/downloaded_manifest.txt"
EXACT_BASELINE="$REPLAY_STATE/exact_artifacts.sha256"
: > "$EXACT_BASELINE"
exact_artifacts=(
  data/current_profile_exact.json
  data/contrast_table.tex
  data/certificate_tables.tex
  data/sign_certificate_tables.tex
  data/triad_routh_gap.tex
  data/network_instances/Nhat_m3.json
  data/network_instances/Nhat_m4.json
  data/network_instances/Nhat_m5.json
  data/network_instances/Nhat_m6.json
  data/network_instances/Nhat_m8.json
  data/network_instances/Nhat_m10.json
  data/exact_instances/pareto_m3_L0.json
  data/exact_instances/pareto_m4_L0.json
)
for relative_path in "${exact_artifacts[@]}"; do
  manifest_line="$(awk -v target="./$relative_path" '$2 == target {print}' "$REPLAY_STATE/downloaded_manifest.txt")"
  if [[ -z "$manifest_line" ]]; then
    printf 'baseline lacks exact artifact: %s\n' "$relative_path" >&2
    exit 2
  fi
  printf '%s\n' "$manifest_line" >> "$EXACT_BASELINE"
done
echo RELEASE_BASELINE_MANIFEST_PASS
OUT="$ROOT/verification_outputs"
mkdir -p "$OUT" data/network_instances data/exact_instances

echo '[1/8] current exact source and tables'
python computation/generate_current_profile_data.py > "$OUT"/current_profile_generation.txt
python computation/generate_tables.py > "$OUT"/generated_tables.txt
python computation/generate_sign_certificate_tables.py > "$OUT"/generated_sign_tables.txt

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
python independent_verifier/frontier_verify_pareto.py 3 4 5 6 8 10 149 200 >> "$OUT"/integrated_designs.txt
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
python computation/audit_stale_claims.py > "$OUT"/stale_claim_audit.txt
grep -q STALE_CLAIM_AUDIT_PASS "$OUT"/stale_claim_audit.txt
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
cat > "$OUT"/PROVENANCE.tsv <<'PROVENANCE'
artifact	command	evidence_class	scope	release_version	status
current_profile_generation.txt	python computation/generate_current_profile_data.py	exact-generation	portable-public	1.0.9	current
generated_tables.txt	python computation/generate_tables.py	exact-generation	portable-public	1.0.9	current
generated_sign_tables.txt	python computation/generate_sign_certificate_tables.py	exact-generation	portable-public	1.0.9	current
all_verifier_entrypoints.txt	39 direct verifier commands listed in the file	exact-and-spectral-entrypoint-coverage	full-source	1.0.9	current-release-qualification
all_verifier_optimized_rejections.txt	39 direct verifier commands under python -O	assertion-mode-negative-control	full-source	1.0.9	current-release-qualification
manifest_mutation_test.txt	detached baseline and self-manifest mutation controls	manifest-negative-control	portable-public-copy	1.0.9	current-release-qualification
detached_numerical_provenance.txt	python independent_verifier/verify_current_numerical_provenance.py	exact-finite-provenance	portable-public	1.0.9	current
integrated_designs.txt	integrated verifier commands in replay.sh	mixed-exact-and-spectral-regression	m=3,4,5,6,8,10,149,200 as applicable	1.0.9	current
manuscript_audit.txt	python computation/audit_manuscript.py	source-semantic-audit	portable-public	1.0.9	current
numerical_provenance.txt	python computation/audit_numerical_provenance.py	numerical-tolerance-audit	portable-public	1.0.9	current-full-only
pdf_semantic_audit.txt	python computation/audit_pdfs.py --profile public	PDF-semantic-font-layout-audit	portable-public	1.0.9	current
journal_pdf_semantic_audit.txt	python computation/audit_pdfs.py --profile journal	PDF-semantic-font-layout-audit	journal-submission	1.0.9	current-release-qualification
pytest.txt	python -m pytest -q computation/tests	mutation-and-regression-tests	portable-public	1.0.9	current
simulations.txt	python computation/simulations.py --outdir data/simulations --jobs 3	numerical-illustration	portable-public	1.0.9	current-full-only
stale_claim_audit.txt	python computation/audit_stale_claims.py	stale-string-audit	portable-public	1.0.9	current
symbolic_certificates.txt	python independent_verifier/verify_symbolic_certificates.py	exact-aggregate	portable-public	1.0.9	current
PROVENANCE
cmp -s "$BASELINE_MANIFEST" "$REPLAY_STATE/downloaded_manifest.txt"
sha256sum -c "$EXACT_BASELINE" >/dev/null
echo RELEASE_EXACT_ARTIFACT_BASELINE_PASS
SELF_MANIFEST="$OUT/replay_self_consistency_manifest.txt"
find . -type f ! -path './.pytest_cache/*' ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '*.aux' ! -name '*.log' ! -name '*.bcf' ! -name '*.blg' ! -name '*.fls' ! -name '*.fdb_latexmk' ! -name '*.run.xml' ! -name '*.out' ! -name '*.toc' ! -name '*.xdv' ! -name 'sha256_manifest.txt' ! -path './verification_outputs/replay_self_consistency_manifest.txt' -print0 | sort -z | xargs -0 sha256sum > "$SELF_MANIFEST"
sha256sum -c "$SELF_MANIFEST" >/dev/null
echo REPLAY_SELF_CONSISTENCY_PASS
echo PUBLIC_REPLAY_PASS
