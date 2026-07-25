# Adversarial audit: centered skew and the local-five separator

This audit independently checked the two arguments in
`harmonic_combination_centered_skew.md` and
`local5_degree5_necessary_rank_separator.md`.  No correctness defect was
found.  The scope remains a fixed-support nonexistence theorem, not a global
upper bound for the five-dimensional kissing number.

The checks covered:

- the constrained extremization in the centered-skew lemma, including
  \(V=0\), \(r=2\), padded zero eigenvalues, and the two-value
  multiplicity formula;
- the dimension-five Gegenbauer normalization, harmonic dimensions,
  signed harmonic combinations, and every diagonal/two-equal/all-distinct
  term in the three trace formulas;
- the direction of the C047 and both harmonic outer bands;
- inclusion of determinant-zero triangle types by the `>= 0` feasibility
  test and the non-strict kissing inequality (the fixed support itself has
  maximum \(499/1000<1/2\));
- the common-margin LP with nonnegative triangle variables and free \(z\),
  including the signs of the inequality multipliers, equality on the free
  column, and the required `combined <= objective` direction on every
  nonbasic column; and
- the absence of any symmetry, rigidity, integrality, or presumed
  \(\tau(5)=40\) hypothesis.

`tests/test_rank_skew_local5_degree5_adversarial_audit.py` additionally
evaluates both universal harmonic-rank inequalities on the exact normalized
\(D_5\) Gram matrix.  The rank-six combination exercises the degenerate
case \(V=D=0\), while the degree-two kernel has exact positive residual
\(10546875/896\).  Two tamper tests confirm rejection of a reversed
outer-band label and a corrupted active basis.
