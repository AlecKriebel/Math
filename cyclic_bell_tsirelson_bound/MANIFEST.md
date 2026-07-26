# Claim and artifact manifest

## Headline theorem

For every integer \(d\ge 2\),

\[
\beta_{\mathrm Q}(\mathcal I_d)
=2\csc\!\left(\frac{\pi}{2d}\right).
\]

The complete analytic proof is in `main.tex` and the rendered PDF. Its logical
dependencies are:

1. the exact polar positive-factor identity;
2. the sharp scalar roots-of-unity maximum and equality set;
3. continuous functional calculus for \(U=A_0^\dagger A_1\); and
4. the known matching strategy, with a self-contained admissibility proof.

## Scope

- **Proved:** a dimension-independent operator upper bound for arbitrary
  unitary observables.
- **Proved:** exact quantum value under the original order-\(d\) constraints.
- **Proved:** exact value of the barred functional after adding one aligned
  unitary correlator.
- **Not proved:** uniqueness of the maximizing strategy or correlation.
- **Not proved:** self-testing in arbitrary dimension.
- **Not proved:** all-dimensional maximal global randomness.
- **Not claimed:** discovery of the Bell family, formula, or attaining
  strategy.

## Artifacts

| Artifact | Role |
|---|---|
| `main.tex` | Source of the analytic paper |
| `output/pdf/cyclic_bell_tsirelson_bound.pdf` | Publication PDF |
| `verify_certificate.py` | Deterministic symbolic and matrix sanity checks |
| `tests/test_certificate.py` | Regression suite independent of the CLI |
| `certificate.json` | Machine-readable claims and formulas |
| `PRIORITY_AUDIT.md` | Public-literature and scope audit |
| `RESEARCH_LOG.md` | Timestamped decisions and checkpoints |
| `SOURCE_SNAPSHOT.md` | Provenance for the supplied package |
| `SHA256SUMS` | Release integrity manifest |

## Verification boundary

The finite computations check exact low-dimensional identities and
floating-point matrix realizations over a documented range. They are
independent sanity checks of the formulas, not a formal proof of the quantified
all-dimensional theorem. The latter is established by the symbolic argument
in the manuscript.
