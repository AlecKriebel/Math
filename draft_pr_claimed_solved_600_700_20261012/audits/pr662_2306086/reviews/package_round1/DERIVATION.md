# Independent whole-package mathematical reconstruction

Reviewer identity: `/root/pr662_package_round1`. Target: PR662 / 2306086, original head e31701151c331a6eed9224fb37a75a374ea1043e. This is a fresh package review, not an author or earlier-family endorsement. Publication files and earlier reports were read-only. The proof and scope were assessed before using the earlier review conclusions for corroboration. This file gives the checkable analytic reasoning; exact controls are supporting checks, not a formal proof certificate.

## Exact target and interpretation

The complete original Hayman–Lingham printed p114 defines S as normalized holomorphic injections of the disk. Complete printed p147 fixes z0 and asks whether the displayed centered derivative disk improves when f is real on the real axis. Its wording does not demand a sharp formula or numerical effectiveness. The source does not explicitly define rho at that display; the standard contextual rho=|z0| is consistent with the classical formula and is the packet's stated interpretation. A meromorphic interpretation would not support that formula without more assumptions.

Thus a qualitative positive answer at each fixed nonreal point is responsive, provided the real-axis exception, zero-point degeneracy, quantitative unknowns and historical-intent limit remain explicit. The paper does all of this. Neither the 2018 no-progress update nor the new proof establishes present literature openness or historical firstness.

For S_R, put A_f(z)=(1−|z|²)f''/f'−2 conjugate(z). The exact claim is an attained maximum M(z)<4 for nonreal z, M(x)=4 for real x, and one positive gap on every compact subset of the nonreal disk. This quantifier order is stronger than separate strictness for each f. At zero the original source expression is zero, while A_f(0)=f''(0) is not necessarily zero.

## Area theorem and equality: no hidden equality assumption

For F in S, F(z)/z extends zero-free across zero, so a normalized logarithm L exists on the simply connected disk. H(w)=w exp(−L(w^−2)/2) is a single-valued odd exterior function, H²=1/F(w^−2), and H=w−a2/(2w)+O(w^−3). Equality of H values implies arguments differ by sign; oddness and H≠0 eliminate the minus sign. This establishes exterior injectivity independently of any area estimate.

For R>1 the image circle is a Jordan curve. Holomorphic orientation and the unbounded component at infinity give the positive enclosed-area integral. Fourier orthogonality yields π(R²−Σ n|bn|²R^−2n)≥0. Laurent and differentiated Laurent series converge uniformly on each such circle. Each finite partial sum of the nonnegative coefficient series is at most R². Taking R down to1 first and then the number of terms to infinity gives Σn|bn|²≤1. The proof does not assume a truncated Laurent map remains injective.

Consequently |a2|≤2. Saturation forces b1 to consume the entire area sum; all other negative coefficients vanish and oddness removes b0. It follows exactly that H=w−λ/w, |λ|=1, and F=z/(1−λz)². Conversely, equality of two values of that rational function has factor (z−w)(1−λ²zw), proving injectivity inside the disk and the equality case. No appeal to numerical closeness or an unproved extremal classification occurs.

## Original equality domains and real symmetry

The normalized Koebe transform has second coefficient A_f(a)/2. Thus |A|≤4, and equality makes the transform a Koebe rotation. This identifies the original image as a complex affine one-ray complement, not necessarily the original function as a Koebe rotation. The distinction is essential. My separate inverse-transform control uses a=(1+i)/4 and λ=i: it is normalized, attains A(a)=4i, and violates the coefficient identity 4a3−3a2²=0 of Koebe rotations. Its a2 is not real, so it does not refute the target.

For a real-coefficient function, the image and its omitted ray are conjugation invariant. The ray has a unique finite endpoint, forcing that endpoint to be real; invariance then forces its outgoing direction to be real too. Zero belongs to the image, so the omitted set is either (−infinity,c] with c<0 or [c,infinity) with c>0. Comparing f with g=4|c|k_plus or 4|c|k_minus by inverse composition yields a zero-fixing disk automorphism. Its derivative has modulus1 and is also1/(4|c|), hence |c|=1/4. Positive normalized derivatives remove the remaining rotation. Only here does the original map become k_plus or k_minus.

Direct differentiation gives |A_k(z)|²=16−48(Im z)²/|1−z²|² for both real Koebe maps. This excludes equality at every nonreal point and gives opposite values ±4 on the real diameter. The latter pair also rules out a smaller disk obtained by recentering: any disk containing two opposite endpoints has radius at least half their distance. Negative real affine normalization derivatives pose no exception because f''/f' is affine-postcomposition invariant.

## Compactness closes the central quantifier gap

The already established universal bound gives |P_f(re^{i theta})|≤(4+2r)/(1−r²). Integrating the radial logarithmic derivative from f'(0)=1 yields |f'|≤(1+r)/(1−r)³; integration once more gives |f|≤r/(1−r)². Thus S is locally bounded and Montel-normal without using the strict theorem being proved.

A local-uniform limit retains derivative1 at zero, so it is nonconstant. For any fixed w, the divided differences (f_n(z)−f_n(w))/(z−w), extended at w, are zero-free holomorphic functions. Hurwitz makes the limit either zero-free or identically zero. The latter would force the limiting f to be constant. Thus the limit is injective and has nonzero derivative everywhere. S is closed and compact in the local-uniform topology; reality is a closed condition. Cauchy derivative convergence and nonvanishing limiting derivative make |A_f(z)| jointly continuous for interior moving points. The maximum over S_R, or S_R×K for compact nonreal K, is attained. Equality exclusion now yields a genuine strict maximum, not only a strict pointwise value. This resolves the possible nonattainment/circularity attack.

## Covariance, orbit parameter and limiting cases

For real a, chain-rule substitution in T_a gives exactly phase (1+a conjugate(w))/(1+aw). Its modulus is1, and inverse normalization gives T_−a T_a f=f. These are bijections of S_R, so the M values are constant on real-automorphism orbits and conjugate points. The invariant δ=|Im z|/|1−z²| lies in[0,1/2) because |1−z²|²=(1−|z|²)²+4(Im z)².

For x=Re z and r=|z|, the displayed a=2x/[1+r²+sqrt((1+r²)²−4x²)] has |a|<1: its denominator is strictly larger than2|x| since1+r²>2|x| in the disk. The discriminant is positive and the quadratic xa²−(1+r²)a+x=0 makes Re((z−a)/(1−az))=0. The disk automorphism preserves the disk, so the transformed nonreal point is ±it with0<t<1. The function t/(1+t²) is strictly increasing there and its stated inverse is correct. The real case δ=0 has M=4 by the previous theorem. Thus the one-variable reduction is complete without supplying M(it).

The real Koebe deficit gives the first lower bound. The map h=z/(1−z²) is injective by its exact difference factorization; its imaginary-axis A value is8it/(1+t²). The same bijections transport this example to every orbit, giving the second bound8δ. The branches cross atδ=1/sqrt7. At i/2 their squares208/25 and256/25 are exact. Asδ→0 orδ→1/2 the respective lower bound approaches4, so no global positive gap is possible. Along z=1−epsilon+i epsilon, δ²→1/8, independently checked; Im z→0 near an endpoint alone cannot replace the invariant condition.

## Fresh stronger check of the linear extreme-point shortcut

Koepf's Section4 lists functions F_u(z)=z/(1−2uz+z²), −1≤u≤1, as the real class's extreme points. A theorem for linear functionals does not assert that the nonlinear quotient attains its maximum there. I tested that possible bridge on the entire listed family, rather than on only k_plus and k_minus.

At z=i/2, direct symbolic differentiation gives

    |A_Fu(i/2)|² = 16(289u²+36) / [25(16u²+9)],
    208/25 − |A_Fu(i/2)|² = 1296(1−u²) / [25(16u²+9)] ≥0.

The admissible map h=z/(1−z²) instead has |A_h(i/2)|²=256/25>208/25. Hence evaluating this nonlinear functional on that entire extreme family misses even this exact admissible value. This is a direct counterexample to that shortcut, not a claim that Koepf cannot be combined with further mathematics. The existing convex-hull critical-point obstruction independently agrees. This new check is not needed as an extra assertion in the paper.

## Rodemich and priority limits

I visually read the recovered complete original A68 and Jenkins's complete own-survey p7, and read all five pages of Koepf's source text, including the original Section4 image. Rodemich's actual quantity is |arg((1−z²)f')|, with q=|z−conjugate(z)|/(1−|z|²) and the piecewise bound recorded in the supplement. Different formulas alone would not establish nonimplication. The analytic addendum supplies the missing precise test: in strip coordinates w=log((1+z)/(1−z)), h=a sin100w, a=10exp(−50π), the induced normalized real locally univalent f satisfies the whole continuous argument envelope. The central interval follows from monotonicity of sinh(100v)/v; the outer intervals use the exact exponential/logarithm margins stated there. At v=π/2−1/100 its |A|² is strictly greater than81/5>16. The example is consequently not globally univalent. It disproves the proposed argument-envelope-plus-local-normalization shortcut, not the target theorem and not every possible deduction with global univalence. The paper states these boundaries correctly.

Jenkins's own p7 explicitly includes derivative bounds in the 1960 work. The full relevant 1960 formulas and Aleksandrov–Popova1973 solved cases remain uninspected. No secondary function-value summary can eliminate those possible overlaps; nor can a general reference to derivative bounds establish one. Four additional targeted searches in this fresh review found no verified exact earlier implication. That is a bounded search outcome, not a novelty certificate. The paper, current-status document, README, machine-readable scope and metadata retain the precise source gaps and make no firstness/current-openness/exhaustive-novelty claim.

## Verification boundary

The written proof is sufficient for its qualitative claim. The source candidate's exact algebraic controls and saved numerical checks reproduce from temporary copies. Optional RK45 and independent alternative-state DOP853 values agree at the reported floating-point scale; no optimizer runs, interval enclosure, certified extra strict lower bound, upper bound or general extremizer follows. The numerical examples do not enter the proof.

No remaining mathematical or package-scope defect was identified. The accepted statement remains a qualitative, classically credited application note. It is not an adjudication that this is the first solution of an historically open problem, and it leaves the explicit/sharp radius, extremizers and full variability region undetermined. Those already disclosed limits remain attached to the verdict.
