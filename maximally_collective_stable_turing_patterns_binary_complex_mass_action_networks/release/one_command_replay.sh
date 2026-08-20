#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FROZEN_BASE="${FROZEN_BASE:-/mnt/data}"
cd "$ROOT"
export PYTHONOPTIMIZE=0

# Preflight before opening replay.log: a failed launch must not truncate the
# archived successful replay.  These five archives certify historical lineage;
# no proof, data-generation, build, or packaging stage reads or extracts them.
required_commands=(python bash pdflatex biber pdfinfo pdffonts unzip sha256sum rsync awk grep find sort xargs tee mktemp tail)
missing_commands=()
for command_name in "${required_commands[@]}"; do
  command -v "$command_name" >/dev/null 2>&1 || missing_commands+=("$command_name")
done
if ((${#missing_commands[@]})); then
  printf 'Replay preflight failed: missing executables:' >&2
  printf ' %s' "${missing_commands[@]}" >&2
  printf '\nInstall requirements before retrying. release/replay.log was not changed.\n' >&2
  exit 2
fi
if ! python - <<'PY' >/dev/null 2>&1
import importlib
import re
import sys

if sys.flags.optimize:
    raise SystemExit("Python assertions are disabled")
minimums = {
    "matplotlib": (3, 7),
    "numpy": (1, 24),
    "pandas": (2, 0),
    "pypdf": (6, 0),
    "pytest": (8, 0),
    "scipy": (1, 10),
    "sympy": (1, 12),
}
for name, required in minimums.items():
    module = importlib.import_module(name)
    match = re.match(r"(\d+)\.(\d+)", module.__version__)
    if match is None or tuple(map(int, match.groups())) < required:
        raise SystemExit(f"{name} {module.__version__} is below {required}")
PY
then
  printf '%s\n' 'Replay preflight failed: Python packages, versions, or assertion mode are incompatible.' >&2
  printf '%s\n' 'Install requirements.txt before retrying. release/replay.log was not changed.' >&2
  exit 2
fi

frozen_archives=(
  'e3c116643e566f905ae72aa2556874319db1845d88520e646c2c88f295dd1e0e|qbio_mass_action_turing_final_flagship.zip'
  '56db8bb8b3e2f23bfa4066a7f1a0c6432f75e50cf71ae742713d23d406cf9b96|qbio_mass_action_turing_all_spectrum_paper.zip'
  'd084e646181f455b80aa336e8448f52cdb9afdb6e3351575f1442595ef65e861|qbio_mass_action_turing_all_spectrum_stable.zip'
  '61d9ff96b0c5bbf74d80bc2b640afcdc23a7f429e8abb0478cd35903b3df0d90|qbio_mass_action_turing_diffusion_design.zip'
  '816dbb043f859d60cf6a32af45bfc7ab2ec46edd75cf51b56eae5bed5345077c|qbio_mass_action_turing_nonlinear_frontier.zip'
)
archive_failures=()
for archive_spec in "${frozen_archives[@]}"; do
  IFS='|' read -r expected_hash archive_name <<< "$archive_spec"
  archive_path="$FROZEN_BASE/$archive_name"
  if [[ ! -f "$archive_path" ]]; then
    archive_failures+=("MISSING $archive_name")
    continue
  fi
  actual_hash="$(sha256sum "$archive_path" | awk '{print $1}')"
  if [[ "$actual_hash" != "$expected_hash" ]]; then
    archive_failures+=("HASH_MISMATCH $archive_name expected=$expected_hash actual=$actual_hash")
  fi
done
if ((${#archive_failures[@]})); then
  printf '%s\n' 'Replay preflight failed: historical-lineage archive prerequisites are incomplete:' >&2
  printf '  %s\n' "${archive_failures[@]}" >&2
  printf 'Looked in FROZEN_BASE=%s\n' "$FROZEN_BASE" >&2
  printf '%s\n' 'These archives are used only for lineage verification; current proofs and builds do not read them.' >&2
  printf '%s\n' 'Portable fallback: cd public/repository && bash replay.sh' >&2
  printf '%s\n' 'release/replay.log was not changed.' >&2
  exit 2
fi

export PYTHONHASHSEED=0 MPLBACKEND=Agg SOURCE_DATE_EPOCH=1786752000 FORCE_SOURCE_DATE=1 TZ=UTC LC_ALL=C
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
mkdir -p release/verification_outputs release/build_logs data/network_instances data/exact_instances
exec > >(tee "$ROOT/release/replay.log") 2>&1

echo '=== FINAL RELEASE REPLAY ==='
python - <<'PY'
import platform
import matplotlib, numpy, pandas, pypdf, pytest, scipy, sympy
print("PYTHON=" + platform.python_version())
for module in (matplotlib, numpy, pandas, pypdf, pytest, scipy, sympy):
    print(f"PYTHON_PACKAGE={module.__name__}=={module.__version__}")
PY
echo '[1/9] historical-lineage archive integrity (startup preflight)'
printf 'FROZEN_BASE=%s\n' "$FROZEN_BASE"
printf 'VERIFIED_LINEAGE_ARCHIVE=%s\n' "${frozen_archives[@]#*|}"
echo FROZEN_SOURCE_HASHES_PASS

echo '[2/9] exact current-profile source, tables, and provenance'
python computation/generate_current_profile_data.py > release/verification_outputs/current_profile_generation.txt
python computation/generate_tables.py > release/verification_outputs/generated_tables.txt
python computation/generate_sign_certificate_tables.py > release/verification_outputs/generated_sign_tables.txt
python independent_verifier/verify_current_numerical_provenance.py > release/verification_outputs/detached_numerical_provenance.txt
python computation/audit_numerical_provenance.py > release/verification_outputs/numerical_provenance.txt
echo NUMERICAL_PROVENANCE_PASS
echo TABLE_REGENERATION_PASS

echo '[3/9] exact tests and theorem/scope audits'
python -m pytest -q computation/tests > release/verification_outputs/pytest.txt
python computation/audit_manuscript.py > release/verification_outputs/manuscript_audit.txt
python independent_verifier/verify_principal_minor_diffusion_ray.py > release/verification_outputs/principal_minor_diffusion_ray.txt
echo MATRIX_THEOREM_GENERALIZATION_PASS
echo STABLE_DOMAIN_SCOPE_PASS

echo '[4/9] all-dimensional symbolic and integrated-design verification'
python independent_verifier/verify_symbolic_certificates.py > release/verification_outputs/symbolic_certificates.txt
rm -f release/verification_outputs/integrated_designs.txt
python independent_verifier/verify_improved_profile.py >> release/verification_outputs/integrated_designs.txt
python independent_verifier/frontier_verify_family.py 3 4 5 6 8 10 >> release/verification_outputs/integrated_designs.txt
python independent_verifier/frontier_verify_normal_form.py 3 >> release/verification_outputs/integrated_designs.txt
python independent_verifier/frontier_verify_pareto.py 3 4 5 6 8 10 149 >> release/verification_outputs/integrated_designs.txt
python independent_verifier/verify_exchange_of_stability.py >> release/verification_outputs/integrated_designs.txt
python independent_verifier/verify_branch_stability.py >> release/verification_outputs/integrated_designs.txt
echo SCC_EXHAUSTION_PASS
echo OMISSION_MINOR_PASS
echo SYMBOLIC_CERTIFICATE_VISIBILITY_PASS

echo '[5/9] exact finite regression instances and current-profile simulations'
for m in 3 4 5 6 8 10; do python computation/export_instance.py "$m" --out "data/network_instances/Nhat_m${m}.json" >/dev/null; done
python computation/export_pareto_instance.py 3 --out data/exact_instances/pareto_m3_L0.json >/dev/null
python computation/export_pareto_instance.py 4 --out data/exact_instances/pareto_m4_L0.json >/dev/null
rm -rf data/simulations
python computation/simulations.py --outdir data/simulations --jobs 3 > release/verification_outputs/simulations.txt
python computation/audit_numerical_provenance.py > release/verification_outputs/numerical_provenance_after_simulation.txt
echo SIMULATION_CONVERGENCE_PASS

echo '[6/9] figures and documents'
rm -rf release/build_logs
mkdir -p release/build_logs
python figures/stable_tradeoff.py > release/build_logs/stable_tradeoff.log
python figures/stable_profiles.py > release/build_logs/stable_profiles.log
python figures/amplitude_scaling.py > release/build_logs/amplitude_scaling.log
(cd figures && pdflatex -interaction=nonstopmode -halt-on-error network_family_standalone.tex > "$ROOT/release/build_logs/network_family.log" && cp network_family_standalone.pdf network_family.pdf)
(
 cd manuscript
 pdflatex -interaction=nonstopmode -halt-on-error main.tex > "$ROOT/release/build_logs/main1.log" 2>&1
 biber main > "$ROOT/release/build_logs/biber.log" 2>&1
 pdflatex -interaction=nonstopmode -halt-on-error main.tex > "$ROOT/release/build_logs/main2.log" 2>&1
 pdflatex -interaction=nonstopmode -halt-on-error main.tex > "$ROOT/release/build_logs/main3.log" 2>&1
 pdflatex -interaction=nonstopmode -halt-on-error supplement.tex > "$ROOT/release/build_logs/supp1.log" 2>&1
 pdflatex -interaction=nonstopmode -halt-on-error supplement.tex > "$ROOT/release/build_logs/supp2.log" 2>&1
 pdflatex -interaction=nonstopmode -halt-on-error supplement.tex > "$ROOT/release/build_logs/supp3.log" 2>&1
)
(
 cd external_audit
 pdflatex -interaction=nonstopmode -halt-on-error theorem_summary.tex > "$ROOT/release/build_logs/summary1.log" 2>&1
 pdflatex -interaction=nonstopmode -halt-on-error theorem_summary.tex > "$ROOT/release/build_logs/summary2.log" 2>&1
 pdflatex -interaction=nonstopmode -halt-on-error proof_skeleton.tex > "$ROOT/release/build_logs/skeleton1.log" 2>&1
 pdflatex -interaction=nonstopmode -halt-on-error proof_skeleton.tex > "$ROOT/release/build_logs/skeleton2.log" 2>&1
)
for f in manuscript/main.log manuscript/supplement.log external_audit/theorem_summary.log external_audit/proof_skeleton.log; do
  ! grep -Eiq 'undefined references|undefined citations|LaTeX Warning: Reference|Overfull \\hbox' "$f"
done
python computation/audit_pdfs.py --profile full
echo FIGURE_REGENERATION_PASS
echo DOCUMENT_BUILD_PASS

echo '[7/9] rebuild all portable, audit, and submission bundles'
bash release/refresh_packages.sh >/dev/null
for z in public/data_archive/final_release_data.zip submission/biorxiv/source_package.zip submission/arxiv/arxiv_source.zip submission/journal/source_package.zip external_audit/packets/reaction_network_audit_packet.zip external_audit/packets/pde_audit_packet.zip external_audit/packets/symbolic_audit_packet.zip; do unzip -tq "$z" >/dev/null; done
sha256sum -c release/BUNDLE_SHA256.txt >/dev/null
# Build each source package in a detached temporary directory.
for z in submission/biorxiv/source_package.zip submission/arxiv/arxiv_source.zip submission/journal/source_package.zip; do
  td="$(mktemp -d)"; unzip -q "$z" -d "$td"; (
    cd "$td"
    pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
    biber main >/dev/null
    pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
    pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
    pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
    pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
  ); rm -rf "$td"
done
FINAL_RELEASE_QUICK=1 bash public/repository/replay.sh > release/public_quick_replay.log
grep -q PUBLIC_REPLAY_PASS release/public_quick_replay.log
echo SUBMISSION_BUNDLE_FRESHNESS_PASS

echo '[8/9] stale-source, PDF, font, and portability audit'
python computation/audit_manuscript.py >/dev/null
python computation/audit_numerical_provenance.py >/dev/null
for f in manuscript/main.pdf manuscript/supplement.pdf external_audit/theorem_summary.pdf external_audit/proof_skeleton.pdf figures/network_family.pdf figures/stable_tradeoff.pdf figures/stable_profiles.pdf figures/amplitude_scaling.pdf; do test -s "$f"; done
for f in manuscript/main.pdf manuscript/supplement.pdf external_audit/theorem_summary.pdf external_audit/proof_skeleton.pdf; do pdffonts "$f" | tail -n +3 | awk 'NF && $5!="yes" {bad=1} END{exit bad}'; done
python computation/audit_stale_claims.py > release/verification_outputs/stale_claim_audit.txt
python computation/audit_pdfs.py --profile full > release/verification_outputs/pdf_semantic_audit.txt
grep -q STALE_CLAIM_AUDIT_PASS release/verification_outputs/stale_claim_audit.txt
if grep -RIl --include='*.py' --include='*.md' --include='*.tex' --include='*.json' --include='*.sh' '/mnt/data/' public/repository | grep -v 'public/repository/replay.sh' | grep .; then exit 1; fi
echo CLEAN_ARTIFACT_AUDIT_PASS

echo '[9/9] immutable manifest'
rm -rf .pytest_cache
find . -type d -name '__pycache__' -prune -exec rm -rf {} +
find manuscript external_audit figures -type f \( -name '*.aux' -o -name '*.bcf' -o -name '*.blg' -o -name '*.fls' -o -name '*.fdb_latexmk' -o -name '*.run.xml' -o -name '*.out' -o -name '*.toc' -o -name '*.xdv' \) -delete
find . -type f ! -path './release/replay.log' ! -path './release/sha256_manifest.txt' ! -path '*/.pytest_cache/*' ! -path '*/__pycache__/*' ! -name '*.pyc' \( ! -name '*.log' -o -path './release/build_logs/*.log' -o -path './release/public_full_replay.log' \) ! -name '*.aux' ! -name '*.bcf' ! -name '*.blg' ! -name '*.fls' ! -name '*.fdb_latexmk' ! -name '*.run.xml' ! -name '*.out' ! -name '*.toc' ! -name '*.xdv' -print0 | sort -z | xargs -0 sha256sum > release/sha256_manifest.txt
grep -Fq '  ./RESEARCH_LOG.md' release/sha256_manifest.txt
sha256sum -c release/sha256_manifest.txt >/dev/null
printf 'MANIFEST_ENTRIES=%s\n' "$(wc -l < release/sha256_manifest.txt)"
echo ALL_FINAL_RELEASE_REPLAY_CHECKS_PASS
