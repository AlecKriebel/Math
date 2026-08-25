# Independent D3+ simplex audit log

## 2026-08-25 00:00 PDT — scope and claim discipline

- Scope: independently test the 24 one-active target directions left unresolved
  by the unit-cube cut-minor search.
- Target claim is treated as a hypothesis.  A successful certificate must be an
  exact identity derived from the graph-compiled K3P map and a sufficient sign
  argument on the true principal domain
  `conv{O,C,G,T,U}`.
- The proposed homogeneous coefficient test is only sufficient.  Failure of
  the test is not evidence that a target minor vanishes in the physical domain.
- No external communication was made.
- Best-guess completion for this bounded audit at start: 15%.

## Mathematical audit of the proposed method

For one edge write positive barycentric coordinates
`(wO,wC,wG,wT,wU)` summing to one and substitute

`c=wC+wU`, `g=wG+wU`, `t=wT+wU`.

Every interior point of the five-vertex polytope admits a representation with
all five weights positive: subtract a sufficiently small positive multiple of
the vertex centroid, represent the remaining point in the polytope, then add
the centroid weights back.  Therefore every nonzero homogeneous monomial in
the five weights is strictly positive at a suitable representation of every
strict-domain spectrum.

For each edge separately, terms of lower total edge degree can be multiplied
by `(wO+wC+wG+wT+wU)^k=1` to reach a common degree.  Inheritance powers are
similarly homogenized with `lambda=L1` and `L0+L1=1`.  Hence a weakly
one-signed homogeneous coefficient array with at least one nonzero coefficient
is a valid strict sign certificate.  Multinomial normalization used to call
this a simplex Bernstein array is positive and does not affect signs.

No logical flaw was found in this sufficiency argument.  It is not a complete
positivity decision procedure.

## 2026-08-25 07:11 PDT — first minimal-degree coefficient run

- Implemented `search_simplex_homogeneous.py` with exact integer expansion,
  exact rational substitution identity checks, and deterministic hashes.
- On target direction 117, 72 of 144 minors were expanded under a two-million
  sparse-coefficient cap; the other 72 exceeded it.  None of the 72 had a
  one-signed minimal-degree homogeneous array.  The best tested array still
  had 486 negative and 39,339 positive nonzero coefficients.
- This is only a negative result for that bounded sufficient test, not a
  mathematical obstruction to a signed polynomial.
- Best-guess completion for this bounded audit: 45%.

## 2026-08-25 07:19 PDT — exact strategy-level obstruction

- A deterministic rational search was followed by exact replay at every
  retained point.
- For every one of the 24 residue directions and every one of its 144 Fourier
  block 2x2 minors, two strict rational physical points were found where the
  actual full minor has opposite signs.
- Total exact result: 24 targets, 3,456 minors, 6,912 nonzero rational witness
  values.  All edge spectra are generated from strictly positive integer
  weights on `O,C,G,T,U`; all inheritance probabilities are strictly between
  zero and one.
- This proves that **no one of these 3,456 minors can serve as a universally
  strictly signed cut separator**, regardless of simplex degree elevation or
  another valid positivity proof.
- It does *not* prove that all 144 minors can vanish simultaneously.  Thus it
  neither supplies a rank-four counterexample nor refutes pointwise cut
  recovery.  Positive combinations, a matrix-level argument, or a joint
  infeasibility certificate remain possible.

Artifacts:

- `certify_single_minor_sign_changes.py`
- `SINGLE_MINOR_SIGN_CHANGE_WITNESSES.json`
- `verify_single_minor_sign_changes.py`

## 2026-08-25 07:21 PDT — independent replay and adversarial checks

- Replay rebuilt all graph-derived K3P polynomials, revalidated every rational
  point in the strict principal domain, and recomputed all 6,912 exact values.
- Result: PASS for 24 targets and 3,456 minors.
- Eight mutations were all rejected: schema, target count, descriptor hash,
  nonpositive barycentric weight, polynomial hash, coordinate rows, witness
  value, and witness sample identifier.
- No external communication was made.
- Best-guess completion for this bounded audit: 100%.

## 2026-08-25 07:43 PDT — six zero-block principal equations do not suffice

- Follow-up scope: target 117 / record 39, zero-character block only.
- Derived the six principal-minor system directly from the graph-compiled K3P
  map.  After positive row/column factors, write
  `p=lambda1*B*X`, `q=(1-lambda1)*B*A`,
  `V=p+q*Y`, and `W=q+p*Y`.  The three minors indexed by `(0,s)` vanish when
  `Y_s=V_s W_s`.
- For distinct nonzero sectors `i,j,k=i xor j`, set
  `d_ij=(q_k Y_j+p_k Y_i)/(W_i V_j)-1`.  The remaining three principal minors
  reduce to
  `(1+theta_i d_ij)(1+theta_j d_ji)=1`.
- Solved the generic three-equation bilinear system for `theta`, then chose
  rational `V,W` for which the nonzero solution lies strictly in `(0,1)^3`.
  All auxiliary triples were realized by explicit rational D3+ edges.
- Exact result: all six principal minors vanish at a strict rational point with
  11 D3+ edge triples and two strict inheritance probabilities.  The minimum
  exact domain margin is approximately `0.00132237936`.
- Every one of the four complete Fourier blocks has exact rank 4 at the same
  point, and an explicitly recorded nonprincipal minor is nonzero.  Therefore
  this is **not** a pointwise cut counterexample.  It proves only that the six
  diagonal equations cannot carry the joint infeasibility proof.
- Replay PASS; eight adversarial mutations were all rejected.

Artifacts:

- `construct_record39_six_diagonal_counterexample.py`
- `RECORD39_SIX_DIAGONAL_COUNTEREXAMPLE.json`
- `verify_record39_six_diagonal_counterexample.py`
- `RECORD39_SIX_DIAGONAL_VERIFICATION.json`

- Best-guess completion for the follow-up six-equation audit: 100%.

## 2026-08-25 07:49 PDT — distinct cyclic six-minor certificate passes

- Audited a different selection proposed after the zero-block counterexample:
  `F_C,F_G,F_T` are the three `(0,s)|(0,s)` minors in character sum zero;
  `H_C,H_G,H_T` use the same pairs in character sums `2,1,1` respectively.
- Rebuilt all six from target 117's graph descriptor and divided only exact
  monomial factors that are strictly positive throughout D3+.
- Exact sparse coefficient replay gives, sector by sector,

  `y*z*F - x*H = a*b*d^2*lambda*(1-lambda)*(y-x*z)*(x*y-z)`.

  Each side has the same ordered eight-term integer coefficient dictionary.
- The prefactor is strictly positive.  If `F=H=0`, then `x=y/z` or `x=z/y`.
  Applying this cyclically to three numbers in `(0,1)` is impossible: their
  positive negative-log coordinates would each equal the absolute difference
  of the other two, while the largest cannot equal such a smaller difference.
- The prior rational zero-block point was evaluated against the new selection:
  all three `F` vanish but all three cyclic `H` are exact positive and nonzero.
  Thus it does not falsify the cyclic proof.
- Symmetry nuance: for each selected sector, either of the two character sums
  outside `{0, selected character}` yields the same reduced `H` identity.  The
  proposed `2,1,1` representatives are correct.  Six invalid-sum mutations
  were rejected.
- Artifact: `RECORD39_CYCLIC_CERTIFICATE_AUDIT.json`.
- Best-guess completion for this cyclic-certificate audit: 100%.

## 2026-08-25 08:03 PDT — target 174 / record 60 closed exactly

- Rebuilt target 174 from the frozen record-60 signatures; descriptor SHA-256
  is `e7b4e9cc338a11ac481a26e097789ac753f0a1aba2a6b2bcbed057514709870a`.
- Isolated nine minors in the zero-character block.  After division only by
  strictly positive monomials, the three diagonal minors are
  `F_s=b_s-d_s^2*K_s*L_s`, and the six ordered cross minors are
  `E_st=d_r*M_st-d_s*d_t*K_s*L_t`, with `r=s xor t`.
- Verified exact sparse ideal membership

  `C_r = E_st*d_r*M_ts + d_s*d_t*K_s*L_t*E_ts`
  `      - b_s*F_t - b_t*F_s + F_s*F_t`

  and the exact cyclic factorization

  `b_r*C_r+b_s*b_t*F_r`
  `=d_r^2*p*(1-p)*a_r*c_r*(b_t-b_s*b_r)*(b_t*b_r-b_s)`.

- The prefactor is strictly positive on the true principal domain.  Vanishing
  would force each `b_r` in `(0,1)` to equal one of the two ratios of the
  other sector values.  Negative logarithms would then each equal the absolute
  difference of the other two; the largest gives an immediate contradiction.
- Therefore target 174 has flattening rank greater than four at every strict
  D3+ point.  No cube relaxation, floating-point inference, or unproved sign
  claim is used.
- Exact replay passes three diagonal formulas, six ordered cross formulas,
  three ideal eliminants, and three factorizations.  Eight mutations were
  rejected, including the neighboring target 175, wrong Fourier block, wrong
  edge class, wrong inheritance variable, transposed ordered minor, missing
  eliminant term, and altered factor sign.
- Artifacts:
  - `verify_record60_cyclic_certificate.py`
  - `RECORD60_CYCLIC_CERTIFICATE_AUDIT.json`
  - `RECORD60_CYCLIC_CERTIFICATE.md`
- No external communication was made.
- Best-guess completion for the bounded target-174 audit: 100%.

## 2026-08-25 08:10 PDT — target 127 / record 43 transported exactly

- Rebuilt target 127 from the frozen record-43 signatures; descriptor SHA-256
  is `6503a89a228ea032392c163208fc24158089ffef1fcf7847f0217e68130173c9`.
- For all nine zero-character-block minors with pairs `(0,s)|(0,t)`, removed
  the positive monomial gcd and then performed exact multivariate division by
  `1-lambda_0`.  Every remainder is identically zero.  This second divisor is
  strictly positive because the inheritance is strict.
- Bound the transported record-60 notation exactly as
  `p=lambda_1`, `a=edge1`, `b=edge4`, `c=edge8`, `d=edge9`.  The three diagonal
  quotients equal `F_s`; the minor with row sector `s` and column sector `t`
  equals `E_ts`, so the ordered cross indices are transposed.
- Replayed the three ideal-membership eliminants and three cyclic
  factorizations as integer coefficient-dictionary equalities.  Their positive
  prefactor forces the same cyclic ratio system, contradicted by the maximal
  negative logarithm.
- Consequently target 127 has flattening rank greater than four at every
  strict D3+ point.
- Nine mutations were rejected: omission and sign change of the strict
  `1-lambda_0` factor, omission of the ordered-index transpose, wrong
  inheritance and edge roles, wrong character block, neighboring target 128,
  an omitted eliminant term, and an altered ratio-factor sign.
- Artifacts:
  - `verify_record43_cyclic_transport.py`
  - `RECORD43_CYCLIC_TRANSPORT_AUDIT.json`
  - `RECORD43_CYCLIC_CERTIFICATE.md`
- No external communication was made.
- Best-guess completion for the bounded target-127 audit: 100%.
