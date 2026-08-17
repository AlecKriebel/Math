#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FROZEN_BASE="${FROZEN_BASE:-/mnt/data}"
cd "$ROOT"
export PYTHONHASHSEED=0 MPLBACKEND=Agg SOURCE_DATE_EPOCH=1786752000 FORCE_SOURCE_DATE=1 TZ=UTC
mkdir -p release/verification_outputs release/build_logs data/network_instances data/exact_instances
exec > >(tee "$ROOT/release/replay.log") 2>&1

echo '=== FINAL RELEASE REPLAY ==='
echo '[1/9] frozen source integrity'
echo 'e3c116643e566f905ae72aa2556874319db1845d88520e646c2c88f295dd1e0e  '"$FROZEN_BASE"'/qbio_mass_action_turing_final_flagship.zip' | sha256sum -c -
echo '56db8bb8b3e2f23bfa4066a7f1a0c6432f75e50cf71ae742713d23d406cf9b96  '"$FROZEN_BASE"'/qbio_mass_action_turing_all_spectrum_paper.zip' | sha256sum -c -
echo 'd084e646181f455b80aa336e8448f52cdb9afdb6e3351575f1442595ef65e861  '"$FROZEN_BASE"'/qbio_mass_action_turing_all_spectrum_stable.zip' | sha256sum -c -
echo '61d9ff96b0c5bbf74d80bc2b640afcdc23a7f429e8abb0478cd35903b3df0d90  '"$FROZEN_BASE"'/qbio_mass_action_turing_diffusion_design.zip' | sha256sum -c -
echo '816dbb043f859d60cf6a32af45bfc7ab2ec46edd75cf51b56eae5bed5345077c  '"$FROZEN_BASE"'/qbio_mass_action_turing_nonlinear_frontier.zip' | sha256sum -c -
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
python independent_verifier/frontier_verify_pareto.py 3 4 5 6 8 10 >> release/verification_outputs/integrated_designs.txt
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
python figures/stable_tradeoff.py
python figures/stable_profiles.py
python figures/amplitude_scaling.py
(cd figures && pdflatex -interaction=nonstopmode -halt-on-error network_family_standalone.tex >/dev/null && cp network_family_standalone.pdf network_family.pdf)
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
(
 cd external_audit
 pdflatex -interaction=nonstopmode -halt-on-error theorem_summary.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error theorem_summary.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error proof_skeleton.tex >/dev/null
 pdflatex -interaction=nonstopmode -halt-on-error proof_skeleton.tex >/dev/null
)
for f in manuscript/main.log manuscript/supplement.log external_audit/theorem_summary.log external_audit/proof_skeleton.log; do
  ! grep -Eiq 'undefined references|undefined citations|LaTeX Warning: Reference|Overfull \\hbox' "$f"
done
test "$(pdfinfo external_audit/theorem_summary.pdf | awk '/Pages/{print $2}')" = 2
test "$(pdfinfo external_audit/proof_skeleton.pdf | awk '/Pages/{print $2}')" = 5
echo FIGURE_REGENERATION_PASS
echo DOCUMENT_BUILD_PASS

echo '[7/9] rebuild all portable, audit, and submission bundles'
bash release/refresh_packages.sh >/dev/null
for z in public/data_archive/final_release_data.zip submission/biorxiv/source_package.zip submission/arxiv/arxiv_source.zip submission/journal/source_package.zip external_audit/packets/reaction_network_audit_packet.zip external_audit/packets/pde_audit_packet.zip external_audit/packets/symbolic_audit_packet.zip; do unzip -tq "$z" >/dev/null; done
# Build each source package in a detached temporary directory.
for z in submission/biorxiv/source_package.zip submission/arxiv/arxiv_source.zip submission/journal/source_package.zip; do
  td="$(mktemp -d)"; unzip -q "$z" -d "$td"; (cd "$td" && pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null && pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null); rm -rf "$td"
done
FINAL_RELEASE_QUICK=1 bash public/repository/replay.sh > release/public_quick_replay.log
grep -q PUBLIC_REPLAY_PASS release/public_quick_replay.log
echo SUBMISSION_BUNDLE_FRESHNESS_PASS

echo '[8/9] stale-source, PDF, font, and portability audit'
python computation/audit_manuscript.py >/dev/null
python computation/audit_numerical_provenance.py >/dev/null
for f in manuscript/main.pdf manuscript/supplement.pdf external_audit/theorem_summary.pdf external_audit/proof_skeleton.pdf figures/network_family.pdf figures/stable_tradeoff.pdf figures/stable_profiles.pdf; do test -s "$f"; done
for f in manuscript/main.pdf manuscript/supplement.pdf external_audit/theorem_summary.pdf external_audit/proof_skeleton.pdf; do pdffonts "$f" | tail -n +3 | awk 'NF && $5!="yes" {bad=1} END{exit bad}'; done
python computation/audit_stale_claims.py > release/verification_outputs/stale_claim_audit.txt
grep -q STALE_CLAIM_AUDIT_PASS release/verification_outputs/stale_claim_audit.txt
if grep -RIl --include='*.py' --include='*.md' --include='*.tex' --include='*.json' --include='*.sh' '/mnt/data/' public/repository | grep -v 'public/repository/replay.sh' | grep .; then exit 1; fi
echo CLEAN_ARTIFACT_AUDIT_PASS

echo '[9/9] immutable manifest'
find . -type f ! -path './release/replay.log' ! -path './release/sha256_manifest.txt' ! -path '*/.pytest_cache/*' ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '*.aux' ! -name '*.log' ! -name '*.bcf' ! -name '*.blg' ! -name '*.fls' ! -name '*.fdb_latexmk' ! -name '*.run.xml' ! -name '*.out' ! -name '*.toc' -print0 | sort -z | xargs -0 sha256sum > release/sha256_manifest.txt
sha256sum -c release/sha256_manifest.txt >/dev/null
printf 'MANIFEST_ENTRIES=%s\n' "$(wc -l < release/sha256_manifest.txt)"
echo ALL_FINAL_RELEASE_REPLAY_CHECKS_PASS
