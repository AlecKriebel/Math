# Approach ledger and scope audit

Five substantive mathematical routes were considered. Retrieval, duplicate screening, tests, and packaging are not counted as proof-search approaches. The fifth route yielded the explicit conditional counterexample in PROOF.md. No sixth independent proof-search route was started. The companion certificate for an alternative source repair checks the same witness.

1. **Balanced-functional reduction.** The entire parameterized inclusion is equivalent to the center case Sigma_1(z) subset S*. A violating convolution functional can be rescaled to produce a zero exactly. This supplies both the reduction in Section 6 of PROOF.md and the final scalar L normalization. It is not by itself a proof of the center inclusion.

2. **Explicit kernel and convex-hull route.** Put E_{epsilon,v}(z)=sum_{n>=1}[(n+1)+epsilon(n-1)]v^(n-1)z^n/2, where |epsilon|=|v|=1. Exact coefficient multiplication gives (h*E)(z)/z=[P_h(vz)+epsilon M_h(vz)]/2. Hence the symmetric norm already controls this entire test family and its closed convex hull. Hallenbeck's Theorem 8 at k=1 identifies the relevant classical close-to-convex hull via the derivative kernels. That imported theorem does not identify the full univalent class S with this hull; no such extension was assumed. The route explains why testing only Koebe and close-to-convex extremals cannot resolve the target.

3. **Coefficient and Hardy-space route.** The symmetric condition s_h<delta implies |h'|<delta. If h=sum c_n z^n, Parseval on circles and passage to the limit give sum n^2|c_n|^2<=delta^2. The imported de Branges bound |a_n(F)|<=n and Cauchy–Schwarz then give |(h*F)(z)/z|<=delta r/sqrt(1-r^2), r=|z|. Combined with the classical growth lower bound, this ensures no zero whenever delta^2 r^2(1+|x|r)^4<1-r^2; in the requested parameter range it covers r<1/sqrt(2). It leaves a genuine outer-annulus gap.

   There is also an exact obstruction to replacing Sigma by the coefficient neighborhood. For h=z^2/5+2z^3/15-z^4/10, the coefficient distance is 6/5. On the unit circle, |h'|^2<=4/5 and |h/z|<=13/30, so s_h^2<=|h'|^2+|h/z|^2<=889/900<1. The maximum-modulus argument extends the bound to the disk. Thus z+h belongs to Sigma_1(z) but not N_1(z). With only one or two nonzero coefficients, alignment of their two phases at one boundary point instead gives equality between the Sigma supremum and the weighted coefficient sum. This rules out one- and two-term polynomial perturbations as a way to exceed the known coefficient neighborhood argument.

4. **Direct starlikeness margin.** This route proves the weaker geometric statement for the specified centers. If a=xz, t=|a|, f_x=z/(1-xz), then

       |f_x'+f_x/z|-|f_x'-f_x/z|
          = (|2-a|-t)/|1-a|^2 >= 2/(1+t)^2.

   To verify the bound, set s=|2-a| in [2-t,2+t]. The expression becomes 2(s-t)/(s^2+t^2-2). Its derivative has numerator -s^2+2st+t^2-2=-(s-t)^2+2t^2-2<0 for t<1. Its minimum is therefore at s=2+t and equals 2/(1+t)^2. Adding a perturbation with |h'-h/z|+|h'+h/z|<2gamma preserves a positive margin, since t<=rho and gamma=(1+rho)^(-2). This excludes zeros of g and gives Re(zg'/g)>0. It proves starlikeness, which is insufficient for membership in the Hadamard dual S*. The final counterexample is fully compatible with this conclusion.

5. **Slit-composition separation and exact certification.** A deterministic floating-point search used three constant radial driving phases, with seed 2306113, and optimized degree-10 perturbations on 192 angular points. Of 24 terminal-Koebe cases, case 21 suggested a strict separating functional; the optimizer's success flag was false, so it was not accepted as evidence of a theorem. The parameters were replaced by simple exact rationals, the function by an elementary composition of explicit injective slit maps, and the global neighborhood bound by an exact rational covering certificate. The resulting proof no longer depends on the ODE solver, optimizer, its success flag, or floating-point arithmetic. The optional search code records the exploratory algorithm; only the exact certificate is used in the proof.

## Source and duplicate gate

The exact mathematical scope was recovered from Hayman–Lingham Problems 6.111–6.113 and their adjacent updates. The inspected 2018 updates do not report a solution of 6.112 or 6.113. A bounded exact-label and semantic screen found no substantive previous center-case attempt. A related authored Janowski study, [PR #562](https://github.com/AlecKriebel/Math/pull/562), was read at its cited exact commit; it addresses coefficient neighborhoods and starlikeness for Problem 6.111, not the center-case Sigma/Hadamard-dual assertion. This is a bounded duplication screen, not a novelty certificate.

The source-definition repair remains explicitly separated from mathematical validity. The main proof handles the symmetric formula displayed in PROOF.md. Any additionally verified alternative is stated in its own supplement, without inferring that these exhaust all possible interpretations of malformed typography.
