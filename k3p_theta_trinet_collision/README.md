# Theorem

The K3P model of a binary semi-directed strict level-two theta trinet with a genuine nontrivial 3-blob intersects the K3P model of a three-leaf tree at an interior stochastic point. The fixed theta-trinet map has rank fifteen at the explicit collision, and the collision persists after moving every network edge into the strict continuous-time K3P cone with all three instantaneous substitution rates positive.

Paper page (unlisted, not linked from the site's paper listing): https://aleckriebel.github.io/Math/papers/k3p-theta-trinet-collision/

```bash
python3 verify.py
```

The expected final line is

```text
ALL EXACT CHECKS PASSED
```

The verifier uses only the Python standard library. It reads the machine-readable certificate and independently rebuilds the topology, root suppression, stochastic edge data, four displayed trees, all sixty-four Fourier coordinates, all sixty-four leaf-pattern probabilities, the selected full-rank Jacobian minor, and the exact tangent identity and strict-margin signs used in the real-analytic implicit-function argument. The existence of the nearby branch is the analytic conclusion of the implicit-function theorem.

## Main files

- `paper.pdf` / `paper.tex`: complete self-contained proof.
- `technical-summary.pdf` / `technical-summary.tex`: two-page mathematical overview.
- `AUTHOR_HANDOFF.md`: author-facing explanation, scope, verification instructions, and follow-up questions.
- `certificate.json`: complete machine-readable construction.
- `jacobian_certificate.json`: the exact 15x15 minor and determinant metadata.
- `continuous_time_certificate.json`: the exact fixed-output tangent identity and strict-rate margin derivatives used in the analytic implicit-function argument.
- `verify.py`: dependency-free exact verifier.
- `verification_report.txt`: successful verifier transcript from the distributed package.
- `CHANGELOG.md` and `PROVENANCE.md`: revision history and reproducibility record.

## Compiling the documents

A standard LaTeX installation with TikZ is sufficient:

```bash
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error technical-summary.tex
pdflatex -interaction=nonstopmode -halt-on-error technical-summary.tex
```

The figure source is `figures/theta_network.tikz`; no proprietary graphics software is used. `references.bib` records the citation metadata even though the distributed TeX source uses a self-contained bibliography.

## Regenerating the certificates

The distributed JSON files can be regenerated with

```bash
python3 src/generate_certificate.py
```

The main verifier does not import this generator. Optional SymPy scripts in `src/` record separate Jacobian and fixed-output tangent audits; they are not required for verification.

## Continuous-time status

The strict continuous-time strengthening is proved. The explicit closed-form witness itself lies on two boundary faces of the strictly positive generator-rate cone, while remaining strictly inside the stated stochastic space Theta_0. A real-analytic implicit-function argument produces nearby theta-network parameters with every substitution rate strictly positive and exactly the same fixed tree distribution; the verifier checks the Jacobian, tangent identity, strict slack, and margin signs used in that theorem.
