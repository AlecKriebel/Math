#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PUB="$ROOT/public/repository"
DATAZIP="$ROOT/public/data_archive/flagship_data.zip"

# ---------- portable public repository ----------
rm -rf "$PUB"
mkdir -p "$PUB" "$ROOT/public/data_archive"
cp "$ROOT/LICENSE" "$ROOT/CITATION.cff" "$ROOT/requirements.txt" "$PUB/"
cat > "$PUB/README.md" <<'EOF'
# Maximally Collective Stable Turing Patterns

Portable source, exact certificates, independent verifiers, numerical illustrations, and manuscript files for

**Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks**  
*Exact Diffusion Design and Exponent-Optimal Heterogeneity Trade-Offs*

The central all-dimensional proof objects are listed in `CERTIFICATES.md`. Finite values of `m` are regression checks only.

## Replay

```bash
bash replay.sh
```

The command reconstructs the reaction family, verifies the all-spectrum and diffusion-design theorems, regenerates exact tables and instances, runs mutation tests and numerical illustrations, rebuilds the figures, and compiles the manuscript and supplement.

Numerical illustrations are not used in any proof.
EOF
cat > "$PUB/CERTIFICATES.md" <<'EOF'
# All-dimensional proof certificates

The following files, together with their human-readable derivations in `proof_audit/`, constitute the all-dimensional certificates.

- `independent_verifier/improved_modulus_certificate.json`: 35-term homogeneous and 77-term improved-profile spatial half-plane certificates.
- `independent_verifier/pareto_all_m_certificate.json`: 34-term homogeneous and 84-term equilibrium-scaled spatial certificates.
- `independent_verifier/frontier_certificate.json`: master stable trade-off and gauge-comparison data.
- `data/certificate_tables.tex`: exact coefficient tables printed in the supplement.
- `independent_verifier/verify_symbolic_certificates.py`: aggregate exact symbolic checker.
- `independent_verifier/verify_one_bad_minor.py`: independent one-bad-minor interface and stationary-band audit.
- `independent_verifier/verify_pareto_family.py`: physical equilibrium-scaling and contrast checks.
- `independent_verifier/verify_exchange_of_stability.py` and `verify_branch_stability.py`: nonlinear stability checks.

Finite JSON instances in `data/network_instances/` and `data/exact_instances/` are regression artifacts, not substitutes for the symbolic proof.
EOF

for d in computation independent_verifier data figures proof_audit literature; do
  mkdir -p "$PUB/$d"
  rsync -a --delete \
    --exclude='__pycache__/' --exclude='*.pyc' --exclude='.pytest_cache/' \
    --exclude='*.aux' --exclude='*.log' --exclude='*.fls' --exclude='*.fdb_latexmk' \
    --exclude='*.bcf' --exclude='*.blg' --exclude='*.run.xml' --exclude='*.out' --exclude='*.toc' \
    "$ROOT/$d/" "$PUB/$d/"
done
mkdir -p "$PUB/manuscript"
cp "$ROOT/manuscript/main.tex" "$ROOT/manuscript/supplement.tex" "$ROOT/manuscript/references.bib" \
   "$ROOT/manuscript/main.pdf" "$ROOT/manuscript/supplement.pdf" "$PUB/manuscript/"
cat > "$PUB/replay.sh" <<'EOF'
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
EOF
chmod +x "$PUB/replay.sh"

# ---------- open data archive ----------
rm -f "$DATAZIP"
(cd "$ROOT/data" && zip -qr "$DATAZIP" .)

# ---------- self-contained submission sources ----------
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
  cp "$ROOT/data/contrast_table.tex" "$ROOT/data/certificate_tables.tex" "$base/data/"
  python - "$base" <<'PY'
from pathlib import Path
import sys
base=Path(sys.argv[1])
for fn in ('main.tex','supplement.tex'):
    p=base/fn
    s=p.read_text().replace('../figures/','figures/').replace('../data/','data/')
    p.write_text(s)
PY
}
for base in "$ROOT/submission/biorxiv/source" "$ROOT/submission/arxiv/source" "$ROOT/submission/journal/source"; do
  prepare_source "$base"
done

cp "$ROOT/manuscript/main.pdf" "$ROOT/submission/biorxiv/manuscript.pdf"
cp "$ROOT/manuscript/supplement.pdf" "$ROOT/submission/biorxiv/supplement.pdf"
cp "$ROOT/manuscript/main.pdf" "$ROOT/submission/journal/manuscript.pdf"
cp "$ROOT/manuscript/supplement.pdf" "$ROOT/submission/journal/supplement.pdf"

rm -f "$ROOT/submission/biorxiv/source_package.zip" \
      "$ROOT/submission/arxiv/arxiv_source.zip" \
      "$ROOT/submission/journal/source_package.zip"
(cd "$ROOT/submission/biorxiv/source" && zip -qr "$ROOT/submission/biorxiv/source_package.zip" .)
(cd "$ROOT/submission/arxiv/source" && zip -qr "$ROOT/submission/arxiv/arxiv_source.zip" .)
(cd "$ROOT/submission/journal/source" && zip -qr "$ROOT/submission/journal/source_package.zip" .)

# ---------- external specialist packets ----------
MIN="$ROOT/external_audit/minimal_verifier"
rm -rf "$MIN"
mkdir -p "$MIN"
rsync -a --exclude='__pycache__/' --exclude='*.pyc' "$ROOT/independent_verifier/" "$MIN/"
cat > "$MIN/replay.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python verify_symbolic_certificates.py
if [[ "${MINIMAL_FAST:-0}" == "1" ]]; then
  python frontier_verify_family.py 3 4
  python frontier_verify_pareto.py 3 4
else
  python verify_improved_profile.py
  python frontier_verify_family.py 3 4 5 6 8 10
  python frontier_verify_normal_form.py 3
  python frontier_verify_pareto.py 3 4 5 6 8 10
  python verify_exchange_of_stability.py
  python verify_branch_stability.py
fi
echo MINIMAL_VERIFIER_PASS
EOF
chmod +x "$MIN/replay.sh"
cat > "$MIN/README.md" <<'EOF'
# Minimal exact verifier

Run `bash replay.sh`. The verifier reconstructs the reaction family and checks the topology-wide block theorem, one-bad-minor interface, omission table, exact diffusion law, contrast bounds, improved unit profile, equilibrium-scaled stable family, cubic signs, and branch stability. It imports no discovery-side module.
EOF

PACKROOT="$ROOT/external_audit/packets"
rm -rf "$PACKROOT"
mkdir -p "$PACKROOT"
for kind in reaction_network pde symbolic; do
  p="$PACKROOT/$kind"
  mkdir -p "$p"
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
3. Are the order-(n-1) omission table and exact factor-eight diffusion law correct?
4. Is the topology-wide `n-1` sharpness statement positioned correctly relative to fixed-J unstable-subsystem theory?
EOF
cat > "$PACKROOT/pde/questions.md" <<'EOF'
# PDE bifurcation and stability audit questions

1. Is the physical scaling `z=Hx`, `D_phys=H Delta` correct?
2. Is the semipositive fixed-integrated-mass Fredholm and zero-mode gauge formulation correct?
3. Are the Fourier factors and cubic contraction normalized correctly?
4. Do the branch spectrum and sectorial hypotheses justify local exponential convergence in fixed-mass `H^1`?
EOF
cat > "$PACKROOT/symbolic/questions.md" <<'EOF'
# Symbolic and algebraic audit questions

1. Is the one-bad-minor derivative monotonicity proof valid under exactly its hypotheses?
2. Are the equality cases in the 34-, 35-, 77-, and 84-term certificates correct?
3. Is the four-factor second-harmonic recurrence exact at both chain boundaries?
4. Is the gauge comparison `N_m(L)>1/200` a valid all-m cubic sign proof?
EOF
for kind in reaction_network pde symbolic; do
  rm -f "$PACKROOT/${kind}_audit_packet.zip"
  (cd "$PACKROOT/$kind" && zip -qr "../${kind}_audit_packet.zip" .)
done

echo PACKAGES_REFRESHED
