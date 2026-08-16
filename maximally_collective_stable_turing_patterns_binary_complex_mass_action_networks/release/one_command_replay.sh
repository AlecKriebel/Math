#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FROZEN_BASE="${FROZEN_BASE:-/mnt/data}"
cd "$ROOT"
export PYTHONHASHSEED=0 MPLBACKEND=Agg SOURCE_DATE_EPOCH=1786752000 FORCE_SOURCE_DATE=1 TZ=UTC
exec > >(tee "$ROOT/release/replay.log") 2>&1
mkdir -p release/verification_outputs

echo '=== FINAL FLAGSHIP REPLAY ==='
echo '[1/6] frozen source archive integrity'
echo '56db8bb8b3e2f23bfa4066a7f1a0c6432f75e50cf71ae742713d23d406cf9b96  '"$FROZEN_BASE"'/qbio_mass_action_turing_all_spectrum_paper.zip' | sha256sum -c -
echo 'd084e646181f455b80aa336e8448f52cdb9afdb6e3351575f1442595ef65e861  '"$FROZEN_BASE"'/qbio_mass_action_turing_all_spectrum_stable.zip' | sha256sum -c -
echo '61d9ff96b0c5bbf74d80bc2b640afcdc23a7f429e8abb0478cd35903b3df0d90  '"$FROZEN_BASE"'/qbio_mass_action_turing_diffusion_design.zip' | sha256sum -c -
echo '816dbb043f859d60cf6a32af45bfc7ab2ec46edd75cf51b56eae5bed5345077c  '"$FROZEN_BASE"'/qbio_mass_action_turing_nonlinear_frontier.zip' | sha256sum -c -

echo '[2/6] exact verification and data regeneration (parallel)'
(
  python -m pytest -q computation/tests > release/verification_outputs/pytest.txt
  python computation/audit_manuscript.py > release/verification_outputs/manuscript_audit.txt
) & p1=$!
python independent_verifier/verify_symbolic_certificates.py > release/verification_outputs/symbolic_certificates.txt & p2=$!
(
  python independent_verifier/verify_improved_profile.py
  python independent_verifier/frontier_verify_family.py 3 4 5 6 8 10
  python independent_verifier/frontier_verify_normal_form.py 3
  python independent_verifier/frontier_verify_pareto.py 3 4 5 6 8 10
  python independent_verifier/verify_exchange_of_stability.py
  python independent_verifier/verify_branch_stability.py
) > release/verification_outputs/integrated_designs.txt & p3=$!
(
  for m in 3 4 5 6 8 10; do
    python computation/export_instance.py "$m" --out "data/network_instances/Nhat_m${m}.json" >/dev/null
  done
  python computation/export_pareto_instance.py 3 --out data/exact_instances/pareto_m3_L0.json >/dev/null
  python computation/export_pareto_instance.py 4 --out data/exact_instances/pareto_m4_L0.json >/dev/null
  python computation/generate_tables.py > release/verification_outputs/generated_tables.txt
) & p4=$!
(
  rm -rf data/simulations
  python computation/simulations.py --outdir data/simulations --jobs 4 > release/verification_outputs/simulations.txt
) & p5=$!
wait "$p1" "$p2" "$p3" "$p4" "$p5"
echo VERIFICATION_AND_DATA_PASS

echo '[3/6] rebuild figures, manuscripts, and audit summaries'
python figures/stable_tradeoff.py & p1=$!
python figures/stable_profiles.py & p2=$!
python figures/amplitude_scaling.py & p3=$!
(
 cd figures
 pdflatex -interaction=nonstopmode -halt-on-error network_family_standalone.tex >/dev/null
 cp network_family_standalone.pdf network_family.pdf
) & p4=$!
wait "$p1" "$p2" "$p3" "$p4"
(
 cd manuscript
 pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
 biber main >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
) & p1=$!
(
 cd manuscript
 pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
) & p2=$!
(
 cd external_audit
 pdflatex -interaction=nonstopmode -halt-on-error theorem_summary.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error theorem_summary.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error proof_skeleton.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error proof_skeleton.tex >/dev/null
) & p3=$!
wait "$p1" "$p2" "$p3"
for f in manuscript/main.log manuscript/supplement.log; do
  ! grep -Eiq 'undefined references|undefined citations|LaTeX Warning: Reference|Overfull \\hbox' "$f"
done
test "$(pdfinfo external_audit/theorem_summary.pdf | awk '/Pages/{print $2}')" = 2
test "$(pdfinfo external_audit/proof_skeleton.pdf | awk '/Pages/{print $2}')" = 5
echo DOCUMENT_BUILD_PASS

echo '[4/6] refresh portable, audit, and submission packages'
bash release/refresh_packages.sh >/dev/null
for z in public/data_archive/flagship_data.zip submission/biorxiv/source_package.zip submission/arxiv/arxiv_source.zip submission/journal/source_package.zip external_audit/packets/reaction_network_audit_packet.zip external_audit/packets/pde_audit_packet.zip external_audit/packets/symbolic_audit_packet.zip; do unzip -tq "$z" >/dev/null; done
echo PACKAGE_INTEGRITY_PASS

echo '[5/6] PDF, source, and project-tree audit'
PDFS=(manuscript/main.pdf manuscript/supplement.pdf external_audit/theorem_summary.pdf external_audit/proof_skeleton.pdf figures/network_family.pdf figures/stable_tradeoff.pdf figures/stable_profiles.pdf)
for f in "${PDFS[@]}"; do test -s "$f"; done
for f in manuscript/main.pdf manuscript/supplement.pdf; do pdffonts "$f" | tail -n +3 | awk 'NF && $5!="yes" {bad=1} END{exit bad}'; done
required=(STATE.md CLAIM_LEDGER.md CHANGELOG.md DEPENDENCY_GRAPH.md FEEDBACK_DISPOSITION.md FINAL_DECISION.md manuscript/main.pdf manuscript/supplement.pdf external_audit/theorem_summary.pdf external_audit/proof_skeleton.pdf public/repository/replay.sh public/repository/CERTIFICATES.md submission/biorxiv/manuscript.pdf submission/biorxiv/source_package.zip submission/arxiv/arxiv_source.zip submission/journal/source_package.zip release/FINAL_REPORT.md release/reproducibility.md)
for f in "${required[@]}"; do test -e "$f" || { echo "MISSING $f"; exit 1; }; done
python - <<'PYPORT'
from pathlib import Path
root=Path('public/repository')
bad=[]
for p in root.rglob('*'):
    if not p.is_file() or p.name=='replay.sh' or p.suffix not in {'.py','.md','.tex','.json','.sh'}:
        continue
    if '/mnt/data/' in p.read_text(errors='ignore'):
        bad.append(str(p))
if bad:
    raise SystemExit('nonportable paths: '+', '.join(bad))
PYPORT
echo PDF_AND_TREE_AUDIT_PASS

echo '[6/6] immutable release manifest'
find . -type f ! -path './release/replay.log' ! -path './release/sha256_manifest.txt' ! -path '*/.pytest_cache/*' ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '*.aux' ! -name '*.log' ! -name '*.bcf' ! -name '*.blg' ! -name '*.fls' ! -name '*.fdb_latexmk' ! -name '*.run.xml' ! -name '*.out' ! -name '*.toc' -print0 | sort -z | xargs -0 sha256sum > release/sha256_manifest.txt
sha256sum -c release/sha256_manifest.txt >/dev/null
printf 'MANIFEST_ENTRIES=%s\n' "$(wc -l < release/sha256_manifest.txt)"
echo ALL_FINAL_FLAGSHIP_REPLAY_CHECKS_PASS
