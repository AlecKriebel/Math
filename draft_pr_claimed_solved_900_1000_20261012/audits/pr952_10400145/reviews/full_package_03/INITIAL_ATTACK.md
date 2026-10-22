# Independent attack before assessment intake

Saved at 2026-10-16T19:06:31.033185+00:00. No candidate proof, earlier proof, reviewer verdict, helper source text, integration assessment, or captured preflight output has been opened. Prior intake was directory names, neutral JSON schema types/key names, mechanical hashing, compilation, and one executed preflight with all output captured unopened. Preflight returned 0. The original-mode comparison first reported a representational 0o644 versus 0644 mismatch; that report is retained privately and numerical comparison gives 33/33.

## Exact question reconstructed from the primary

Ohtsuki (editor), Problems on invariants of knots and 3-manifolds, printed pp.490--492, defines R1 as the inverse limit of Z[q,q^{-1}]/((q-1)...(q^n-1)). It injects into Z[[q-1]]. Conjecture7.30 defines R1' = lim R1[t]/P_N(t), P_N=product_{j=1}^N(t-q^j), and asks for values I^{sl_n}(M) at t=q^n for every n>=1, with assigned I^{sl_1}(M)=1. The preceding update says Conjecture7.29 has been proved; perturbative matching is part of the preceding normalization. I read the actual displayed formulas visually, not just extracted text. Note that local pdftotext page118 is printed490, page119 printed491, page120 printed492; the assignment's zero-based118--120 label does not match all these printed labels. I included both its requested extraction range and the actual printed490--492.

## Mechanism: collapse of all interpolation nodes over dual numbers

Put h=q-1. Every F in this completion has a representative f_N(t) at a finite stage N containing any chosen finite ranks. Mod h^2, write f_N(t)=f_{N,0}(t)+h f_{N,1}(t). At t=q^r = 1+r h mod h^2 one gets
F(q^r) = A + h(B+r C) mod h^2,
where A=f_{N,0}(1), B=f_{N,1}(1), C=f'_{N,0}(1). Thus any three distinct ranks must have affine first Taylor coefficients. This deduction uses only finite-stage polynomial representatives, avoiding any infinite-series interchange or inverse Vandermonde matrix.

For ranks1,2,3 and assigned rank1=1, the coefficient sequence must satisfy c_3=2c_2. More generally c_a-2c_{a+d}+c_{a+2d}=0 for arbitrary positive a,d. A second difference of first jets is a possible complete obstruction, stronger than a divisibility sample. All coefficients remain integral; even a rational coefficient extension would retain this first-jet condition.

## Attempted topological counterexample and exact remaining gap

The primary gives the Poincare sphere as -1 surgery on a left-hand trefoil and its sl2/SO3 perturbative expansion (1/(1-q)) sum_{m>=0} q^m product_{j=m+1}^{2m+1}(1-q^j). The m=0 contribution is1; m=1 has first coefficient -6h; m>=2 is O(h^2). Hence c_2=-6 in the primary's orientation. A conventional degree-one LMO/weight-system calculation predicts c_r = lambda(M) r(r^2-1), with lambda(M)=-1 in this orientation, so c_3=-24 rather than the required -12. The nonzero second difference would be -12.

This is currently an attempted counterexample, conditional on confirming the exact sl_n perturbative normalization/LMO bridge from established sources. I have not treated that bridge as proved from memory. A web search located Le, On Perturbative PSU(n) Invariants of Rational Homology3-Spheres (arXiv math/9802032,1998), whose abstract establishes a relevant perturbative construction, but I have not yet opened its body or used it as a coefficient proof. The theta contraction can also be calculated from the trace form on sl_n: the adjoint Killing form is2n times trace and contraction should be2n(n^2-1); combining this with a theta coefficient lambda/2 yields the predicted formula. The topology and normalization are external inputs, while the affine-jet obstruction is my deduction here.

## Boundary and falsification plan

1. Test that the finite-stage representative really evaluates to the specified completed value; if N>=all ranks, P_N(q^r)=0 exactly, so it does.
2. Check possible orientation inversion q->q^{-1}: it negates all first coefficients and cannot remove a nonzero second difference.
3. Assigned rank1 is a convention, not a genuine simple Lie algebra. Use ranks2,3,4 as a separate obstruction if needed; the cubic produces a nonzero second difference there too.
4. Vanishing Casson/first coefficient gives no conclusion. S3 should pass with constant1. No statement about all homology spheres follows from this obstruction alone.
5. At higher orders the coefficient of h^k should have rank degree at most k, by formal substitution in a finite representative. This general filtration test is a possible route when the first coefficient vanishes, but topological nonvanishing at higher orders would require additional evidence.
6. For general abstract node families, the affine assertion fails if the coefficient ring permits h^{-1}; verify the candidate uses the literal coefficient ring. A modified completion or rank scaling is a different question.

Strongest verified result at this boundary: every literal interpolant must satisfy affine first-jet compatibility, and the primary's Poincare sl2 jet is -6. Exact remaining mathematical gap: independently confirm the sl3 (or general sl_n) jet in the same q and orientation normalization. No novelty or priority claim has been made. Completion estimate for the entire audit:8%.
