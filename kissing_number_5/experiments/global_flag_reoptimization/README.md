# Reoptimizing the global rooted-edge flag obstruction

## Exact result

The negative rooted-edge flag row in
`../global_flag_exchangeability/` is an exact obstruction to the *stored*
local lifts, but it is not an obstruction to every lift of the same
pair/triple data.

Two exact repairs are recorded here.

1. `psd4_repair_certificate.json` is a positive mixture of 57 rank-five
   \(K_6\) atoms.  It matches the fixed triangle marginal and makes the
   four-feature block
   \[
     (e,\ e(a+c),\ qe,\ ad+bc)
   \]
   positive definite.  In particular, it strictly repairs the former
   separator \(8e-3e(a+c)\).
2. `centered_degree2_repair_certificate.json` is a positive mixture of 73
   rank-five \(K_6\) atoms.  It matches the same triangle marginal and
   makes the **entire centered, symmetric, degree-at-most-two rooted-edge
   block** positive semidefinite.

Both statements are over the rationals and have independent exact
verifiers.  The second certificate has SHA-256

```text
7b8dd73bfdaced21fe6a6f6acd74231a976b7359bce600cf45c0d1c44db895d6
```

This is a counter-witness inside a local relaxation, not a spherical
41-code.  Compatibility between overlapping \(K_6\) samples is not imposed.

## Flag block

For an ordered root \((i,j)\) and an unordered residual pair
\(\{p,r\}\), put
\[
\begin{aligned}
q&=4g_{ij},& a&=4g_{ip},& b&=4g_{jp},\\
c&=4g_{ir},& d&=4g_{jr},& e&=4g_{pr}.
\end{aligned}
\]
The 18-dimensional basis is
\[
\begin{split}
(&1,q,e,a+c,b+d,q^2,qe,e^2,q(a+c),q(b+d),\\
 &e(a+c),e(b+d),a^2+c^2,b^2+d^2,ab+cd,ac,bd,ad+bc).
\end{split}                                                    \tag{1}
\]
It spans every polynomial of degree at most two in
\((q,a,b,c,d,e)\) that is invariant under swapping \(p\) and \(r\).

For a local \(K_6\) atom \(X\), let \(v_{ij,A}\) be (1), and define
\[
 M_X=\sum_{i\ne j}\sum_{A,B}
 \lambda_{|A\cup B|}v_{ij,A}v_{ij,B}^{\mathsf T},              \tag{2}
\]
where \(A,B\) range over residual pairs and
\[
(\lambda_2,\lambda_3,\lambda_4)=(494,9139,329004)
=4\left(
\frac{\binom{39}{2}}{\binom42},
\frac{\binom{39}{3}}{\binom43},
\frac{\binom{39}{4}}{\binom44}
\right).                                                       \tag{3}
\]
Multiplying all coefficients by four clears denominators and does not
change positive semidefiniteness.

The certificate gives positive rational weights \(w_X\), summing to one,
such that
\[
M=\sum_X w_XM_X                                                   \tag{4}
\]
has rank seven and is positive semidefinite.

## The centered radical

For a centered 41-point array, \(\sum_x x=0\).  At a fixed ordered root
there are 39 residual vertices.  The elementary root-sum identities include
\[
\sum_p a_p=\sum_p b_p=-4-q,\qquad
\sum_{\{p,r\}}e_{pr}=q-74.                                      \tag{5}
\]
Taking first and second moments of (5), and using
\[
\sum_{r\ne p}e_{pr}=-4-a_p-b_p,                                 \tag{6}
\]
gives 11 exact linear identities in the basis (1).  Their coefficient
vectors are stored in `centered_kernel_vectors`.

The verifier checks directly that:

- those 11 vectors are independent;
- all 11 lie in the radical of \(M\);
- together with coordinate vectors
  \[
  (1,q,q^2,e^2,a^2+c^2,b^2+d^2,ab+cd),                          \tag{7}
  \]
  they span the full 18-dimensional feature space; and
- the \(7\times7\) principal matrix on (7) is positive definite.

The last point is certified both by all 127 nonempty principal minors and,
independently, by an exact \(LDL^{\mathsf T}\) factorization with seven
positive pivots.  Therefore (4) is exactly positive semidefinite with
radical precisely the 11 forced centered identities.

Every atom is also checked from scratch: its scaled Gram matrix has
diagonal four, off-diagonal entries in \(\{-4,-3,\ldots,2\}\), is positive
semidefinite, and has rank exactly five.

## Scope

The theorem-strength conclusion is negative but useful:

> The fixed centered triangle marginal cannot be eliminated by any
> positive-semidefiniteness test using only the complete symmetric
> degree-at-most-two rooted-edge block on an independently sampled \(K_6\).

This does **not** establish a global 41-vertex Gram matrix.  A distribution
on one \(K_6\) does not automatically give consistent distributions on two
overlapping \(K_6\)'s.  It also does not address noncentered codes.  A
genuinely stronger flag route must impose overlap consistency (for example
through rooted-triangle \(K_7\) data), use higher degree, or introduce
independent global information.

The catalog used during discovery is incomplete.  Completeness is not
needed to verify a feasible counter-witness: the 73 listed atoms and their
positive rational weights suffice.  Conversely, failure of a search over
this catalog would not have proved infeasibility.

## Artifacts

- `generate_psd4_repair.py`: deterministic exact generator for the
  57-atom certificate.
- `verify_psd4_repair.py`: primary exact verifier for the four-feature
  repair.
- `independent_psd4_audit.py`: independent direct-loop and exact-LDL audit.
- `generate_centered_degree2_repair.py`: deterministic exact generator for
  the 73-atom certificate.
- `verify_centered_degree2_repair.py`: primary exact verifier, including
  source authentication, atom PSD/rank, triangle marginal, radical, and all
  quotient principal minors.
- `independent_centered_degree2_audit.py`: independent direct-loop moment
  recomputation and exact-LDL audit.
- `search_degree2_psd.py` and `search_centered_degree2_psd.py`: numerical
  discovery programs only.  Their output is not trusted by either exact
  verifier.

The discovery run used Python 3.14.6, NumPy 2.5.1, SciPy 1.18.0, and
`scipy.optimize.linprog(method="highs")`.  Certificate generation and both
verification paths use only Python 3.10-or-later standard-library exact
arithmetic.

## Reproduction

From the repository root:

```sh
PYTHONPATH=. python3 \
  experiments/global_flag_reoptimization/generate_centered_degree2_repair.py

PYTHONPATH=. python3 \
  experiments/global_flag_reoptimization/verify_centered_degree2_repair.py

PYTHONPATH=. python3 \
  experiments/global_flag_reoptimization/independent_centered_degree2_audit.py

PYTHONPATH=. python3 -m unittest \
  experiments.global_flag_reoptimization.test_psd4_repair \
  experiments.global_flag_reoptimization.test_centered_degree2_repair \
  -v
```

All proof-critical checks are implemented with always-on verification
exceptions.  The tests run all four proof checkers under `python -O` and
confirm that optimized mode rejects deliberately tampered certificates.
