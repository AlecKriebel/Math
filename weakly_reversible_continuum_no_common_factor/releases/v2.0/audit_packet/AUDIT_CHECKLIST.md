# Specialist failure-point checklist

The packet is designed to make the following likely failure modes easy to
attack. The listed checks are exact; decimal approximations are never used as
evidence.

| Failure point | Exact test or certificate | Primary replay layer |
|---|---|---|
| A rate is attached to the wrong directed edge | Fixed 20-edge order is cross-checked against the CSV before reconstructing the field | v2 wrapper, family verifier |
| A rate is zero, negative, or only numerically positive | Integer positivity for both specializations; coefficientwise rational proof of the full positive cone | family and strengthening verifiers |
| The graph is not reversible or has multiple linkage classes | Reverse-edge dictionary and exact graph traversal | frozen and independent v2 verifiers |
| Stoichiometric rank is below three | Exact integer rank; determinant \(-3\) from three displayed reaction differences | frozen and independent v2 verifiers |
| The asserted curve is not in one class | \(S=\mathbb R^3\), so the class is the positive orthant | graph/stoichiometry checks |
| The parametrization misses positivity or distinctness | Exact substitution into \(L,Q\); positive quadratics; monotonicity of \(z(t)\) on \((-1,1)\) | frozen verifier |
| The conic is reducible, singular, noncompact, or partly nonpositive | Nonsingular homogenized conic matrix, irreducibility, and exact circle-form identity | frozen and clean-room verifiers |
| Vanishing on the conic is a numerical accident | Exact Gröbner reduction and identities \(F_i=A_iL+B_iQ\) | frozen, family, strengthening verifiers |
| The coordinate gcd is hidden over \(\mathbb R\) or \(\mathbb C\) | Exact gcd over \(\mathbb Q\), homogenized gcd, and Galois-norm scalar-extension argument | family and strengthening verifiers |
| The continuum is produced by a common scalar multiplier | gcd is exactly one; the conic has height two; Jacobian rank is two at a conic point | frozen and strengthening verifiers |
| The four-parameter family is incomplete | Canonical \(21\times20\) remainder matrix, nonzero 16-minor, and four independent kernel vectors | family verifier |
| Positivity inequalities are sufficient only heuristically | Orthant substitution turns every rate into a nonzero linear form with nonnegative rational coefficients | family verifier |
| “Generic gcd one” ignores degree drops or the zero field | Homogenized common-factor cones include the origin and degree-drop limits; explicit point lies outside | family theorem/verifier |
| The residual 15-point component is nonreduced or intersects the conic | Exact triangular Gröbner basis, irreducible separable eliminant, comaximality, and product reductions | frozen, clean-room, strengthening verifiers |
| The clean integer optimum is based on floating point | Divisibility reductions and bounded exhaustive rational enumeration | strengthening and independent v2 verifiers |
| Frozen and clean rates were accidentally mixed | Separate rate columns and separate reconstructed fields; cross-layer equality checks | v2 wrapper and independent v2 audit |
| Stability is claimed for the wrong specialization | Stability section and Sturm verifier explicitly use frozen v1 rates only | strengthening and independent v2 verifiers |
| Ten complexes or ten reversible pairs are called globally minimal | Manuscript and packet explicitly restrict optimality to integral rates on the fixed support/family | scope audit |
| The repository concept DOI is misrepresented as paper-specific | Packet states that `10.5281/zenodo.21753404` groups unrelated monorepo releases and directs paper citations to the pending Version 2 DOI | metadata audit |
| A DOI is represented as peer review or proof | Packet labels DOI metadata as disclosure, not correctness certification | metadata audit |

## Independent replay

The principal one-command wrapper is

```sh
.venv/bin/python weakly_reversible_continuum_no_common_factor/manuscript_v2_draft/verify_v2_claims.py
```

A substantively independent audit is also available:

```sh
.venv/bin/python weakly_reversible_continuum_no_common_factor/audit_v2/verify_v2_independent.py
```

The independent audit reconstructs its own field and ideal data rather than
treating agreement with displayed formulas as sufficient.

## Scope boundary

The following are not certified by this packet:

- global minimality in complexes, reactions, molecularity, or deficiency;
- persistence of the conic under arbitrary perturbations outside the
  four-dimensional family;
- mathematical priority beyond the stated narrow audit; or
- correctness by virtue of repository or DOI timestamps.
