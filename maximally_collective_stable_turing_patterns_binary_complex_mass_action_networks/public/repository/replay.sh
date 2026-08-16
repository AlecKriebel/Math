#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
export PYTHONHASHSEED=0
export MPLBACKEND=Agg
export SOURCE_DATE_EPOCH=1786752000
export FORCE_SOURCE_DATE=1
export TZ=UTC

mkdir -p verification_outputs
echo '[1/8] exact tests and manuscript audit'
python -m pytest -q computation/tests > verification_outputs/pytest.txt
python computation/audit_manuscript.py > verification_outputs/manuscript_audit.txt

echo '[2/8] independent symbolic and nonlinear verifiers'
python independent_verifier/verify_symbolic_certificates.py > verification_outputs/symbolic_certificates.txt
if [[ "${FLAGSHIP_QUICK:-0}" == "1" ]]; then
  { python independent_verifier/frontier_verify_family.py 3 4; python independent_verifier/frontier_verify_pareto.py 3 4; } > verification_outputs/quick_pareto.txt
else
  {
    python independent_verifier/verify_improved_profile.py
    python independent_verifier/frontier_verify_family.py 3 4 5 6 8 10
    python independent_verifier/frontier_verify_normal_form.py 3
    python independent_verifier/frontier_verify_pareto.py 3 4 5 6 8 10
    python independent_verifier/verify_exchange_of_stability.py
    python independent_verifier/verify_branch_stability.py
  } > verification_outputs/integrated_designs.txt
fi

echo '[3/8] exact finite regression instances and printed certificate tables'
if [[ "${FLAGSHIP_QUICK:-0}" == "1" ]]; then MS=(3 4); else MS=(3 4 5 6 8 10); fi
for m in "${MS[@]}"; do
  python computation/export_instance.py "$m" --out "data/network_instances/Nhat_m${m}.json" >/dev/null
done
python computation/export_pareto_instance.py 3 --out data/exact_instances/pareto_m3_L0.json >/dev/null
python computation/export_pareto_instance.py 4 --out data/exact_instances/pareto_m4_L0.json >/dev/null
python computation/generate_tables.py > verification_outputs/generated_tables.txt

echo '[4/8] deterministic numerical illustrations'
if [[ "${FLAGSHIP_QUICK:-0}" == "1" ]]; then
  rm -rf data/simulations_test
  python computation/simulations.py --quick --outdir data/simulations_test > verification_outputs/simulations_quick.txt
else
  rm -rf data/simulations
  python computation/simulations.py --outdir data/simulations --jobs 4 > verification_outputs/simulations.txt
fi

echo '[5/8] figures'
python figures/stable_tradeoff.py
if [[ "${FLAGSHIP_QUICK:-0}" != "1" ]]; then
  python figures/stable_profiles.py
  python figures/amplitude_scaling.py
fi
(
 cd figures
 pdflatex -interaction=nonstopmode -halt-on-error network_family_standalone.tex >/dev/null
 cp network_family_standalone.pdf network_family.pdf
)

echo '[6/8] manuscripts'
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

echo '[7/8] PDF and portability checks'
for f in manuscript/main.pdf manuscript/supplement.pdf figures/network_family.pdf figures/stable_tradeoff.pdf figures/stable_profiles.pdf; do
  test -s "$f"
  pdffonts "$f" | tail -n +3 | awk 'NF && $5!="yes" {bad=1} END{exit bad}'
done
! grep -RIl --include='*.py' --include='*.md' --include='*.tex' --include='*.json' --include='*.sh' '/mnt/data/' README.md CERTIFICATES.md computation independent_verifier proof_audit manuscript figures data | grep .

echo '[8/8] local source manifest'
find . -type f \
  ! -path './.pytest_cache/*' ! -path '*/__pycache__/*' ! -name '*.pyc' \
  ! -name '*.aux' ! -name '*.log' ! -name '*.bcf' ! -name '*.blg' \
  ! -name '*.fls' ! -name '*.fdb_latexmk' ! -name '*.run.xml' ! -name '*.out' ! -name '*.toc' \
  ! -name 'sha256_manifest.txt' -print0 | sort -z | xargs -0 sha256sum > sha256_manifest.txt
sha256sum -c sha256_manifest.txt >/dev/null

echo PUBLIC_REPLAY_PASS
