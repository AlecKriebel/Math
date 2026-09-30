# 2840 / KP-3.42: Giroux-torsion finiteness

The original question for each fixed closed tight contact 3-manifold remains unresolved. The package records two stopped approaches and their precise limitations.

- [Scoped deductions and remaining gap](PARTIAL.md)
- [Source audit](SOURCE_AUDIT.md)
- [Exact checker](verify.py) and [receipt](verification.json)
- [Readiness evidence](readiness.json) and [research log](RESEARCH_LOG.md)

The partial proof gives an L² degeneration bound for embedded torsion layers, a conditional metric bound, and a local contact-dilation obstruction to a uniform pointwise conformal-factor bound over all embeddings. Standard torus examples distinguish changing closed structures, coverings, and noncompact infinite torsion.

Run the verifier with Python and SymPy 1.14.0. It rewrites its sibling verification.json. All 372 exact controls pass; they do not establish tightness or resolve the original question.

Status: unsolved, two substantive approaches used, separate adversarial review pending. The standard tightness and fillability results are credited. Historical priority for the elementary deductions is unconfirmed.
