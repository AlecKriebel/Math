# Adversarial audit of the verifier and second proof

Checkpoint: 2026-09-23 04:12 UTC. Completion estimate: **100% for this audit**. Scope: the two artifacts below, not literature priority. No correctness defect was found.

Audited SHA-256 values:

- `verification/verify.py`: `f1d0b9755c3dab689878c0e8af758ea3f5e58ebcc86eb36afaed5f67b67dc82f`
- `audit/independent-geometry.md`: `a9d13998e41de80c3197dd019a78906244dc74b243c9feeb73e0ea8d8896b6e3`

## Verifier: correct finite certificate checks

The program was read in full and executed successfully. It reports 12 certificates, 120 symmetric coefficient classes, 110 independent inclusion-exclusion cross-checks, 23 quadratic identity checks (degrees 2 through 24 inclusive), and two rejected negative controls. The sample cases include degree two, dimension one, negative determinant, a nonconvex positive quartic, and a positive quartic requiring a coordinate change.

The transformation convention is internally consistent: `basis_rows` stores the matrix `S` by rows, so the basis consists of its columns. The substitution routine expands `p(S t)` using its row linear forms. The independent polarization routine is passed those same columns in the appropriate multiplicities.

For a monomial exponent vector `alpha`, expansion produces the ordinary coefficient `c_alpha`. The code correctly divides it by `d! / product(alpha_i!)` to obtain the symmetric ordered-tensor entry `a_alpha`. Sequential integer divisions in `multinomial` are exact: every partial product of the component factorials divides their full product, which divides `d!`. Checking one entry per exponent vector covers all ordered tuples because the polarization is symmetric.

The checked power gap is exactly

\[
\prod_i p(x_i)^{\alpha_i}-a_\alpha^d.
\]

Since `d` is even and the diagonal values are positive, nonnegativity of this gap is equivalent to the desired absolute-value inequality. The script deliberately checks the stronger certificate property: every entry is positive, every mixed gap is strictly positive, and pure gaps vanish. Thus it may reject a basis satisfying only the weak theorem conclusion; this is accurately disclosed in its README.

The determinant implementation performs exact rational Gaussian elimination with row pivoting. Although it leaves old entries below a pivot nonzero, those entries are never used again: subsequent elimination and pivots use only the current trailing submatrix. The product of pivots and row-swap signs therefore gives the determinant correctly. Input entries are converted to `Fraction` before this routine is called.

The finite-difference polarization cross-check uses the independent identity

\[
A(v_1,\ldots,v_d)=\frac1{d!}
\sum_{S\subseteq\{1,\ldots,d\}}(-1)^{d-|S|}
 p\left(\sum_{i\in S}v_i\right).
\]

Inclusion-exclusion annihilates all terms omitting at least one of the `d` argument slots. Homogeneity leaves precisely the `d!` copies of the multilinear term. Repeated argument vectors cause no problem because the slots remain separately indexed. This checks the tensor multiplicity and the matrix orientation through a computational mechanism different from polynomial substitution.

Additional independent checks were run in memory with deterministic random seed `17293016`: 500 rational matrices of sizes 1 through 5 were compared with the full Leibniz determinant formula, including duplicate-row singular cases; 20 signed polynomial/argument examples with `(m,d)` equal to `(1,2)`, `(2,2)`, `(2,4)`, or `(3,4)` compared inclusion-exclusion polarization against direct summation over all ordered tensor indices. All passed. In the latter check the multiplicity was counted by enumerating index tuples, without calling the verifier's multinomial routine.

The limits are stated honestly: the script neither proves the universal theorem nor decides positivity of an arbitrary input form, constructs its minimizer, or selects a universally valid epsilon. The finite identity checks are diagnostics of the algebraic identity, not a proof for every degree. Its documented input uses rational strings; use that representation for exact certificate data. No floating-point tolerance enters the supported workflow.

## Second proof: the cone and Cauchy–Schwarz route is sound

The geometric proof was checked independently of its existing audit statement. Its argument closes every step of the stronger claim: a nonempty open cone exists on which the inequality holds for every `d`-tuple, with equality exactly for positively proportional arguments.

1. If `e` is a sphere minimizer with `P=p(e)>0`, then `p(x)-P|x|^d` has a global minimum of zero at `e`. Its positive semidefinite Hessian gives

   \[
   A(e^{d-2},u,u)\ge
   \frac{P}{d-1}\bigl(|u|^2+(d-2)\langle e,u\rangle^2\bigr)>0
   \quad(u\ne0).
   \]

   The radial and tangent eigenvalue bounds are respectively `P` and `P/(d-1)`. No global convexity is assumed.

2. Joint continuity and openness of positive definiteness supply one cap around `e` in which **every** independently chosen `(d-2)`-tuple conditions `A` to a positive definite bilinear form. Shrinking the cap also gives positivity of all `d`-linear values. Positive scaling extends these facts to a cone. No convexity of the cone and no closure under addition are needed.

3. For a finite normalized collection, conditioned Cauchy–Schwarz gives `c_alpha^2 <= c_(alpha+e_i-e_j)c_(alpha-e_i+e_j)`. The finite maximum argument is complete: if a maximizer has two positive coordinates, both neighboring entries also attain the maximum. Their squared-coordinate sums change by `2(alpha_i-alpha_j)+2` and `2(alpha_j-alpha_i)+2`; at least one increases. Choosing a maximizer with maximal squared-coordinate sum therefore forces it to be pure, with value one. There is no unproved iteration, limiting argument, or imported generalized Hölder theorem.

4. Strict Cauchy–Schwarz for a nonproportional pair, together with the already proved weak bound for its neighboring entries, yields strictness. The hemisphere condition excludes negative proportionality. Zero arguments are excluded from the cone, and the note correctly records that allowing them would change the equality characterization.

5. The explicit clustered vectors lie in the cone for small positive displacement and have determinant equal to the corresponding positive displacement to power `m-1` in the indicated orthonormal coordinates. The dimension-one and degree-two cases remain valid.

This route shares the sphere-minimum source of a positive bilinear slice with the candidate proof, but its core inequality mechanism is different: exact conditioned Cauchy–Schwarz and a finite maximum replace the Taylor expansion and remainder argument. It also rigorously supports the stronger uniform cone statement, which should not be inferred from the candidate's raywise Taylor calculation alone.

**Remaining gap:** none found in either audited artifact within its stated scope. Bibliographic priority, final manuscript consistency, and packaging remain separate checks.
