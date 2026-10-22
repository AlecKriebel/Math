# Exact target and source scope

## Disposition

Target: rank 1091, 30000127 / OWR-757-005, Oleinik entropy conditions for the Leroux hydrodynamic limit. The full three-state, infinite-line problem is **not solved**. Five new distinct substantive approaches are recorded. Starting inherited count was 0/5; final substantive count is 5/5. Literature retrieval and readiness auditing are excluded from that count. These elementary partial results and obstructions are not claimed novel.

## Model and scales

A configuration is omega in {−1,0,1}^Z. The unaccelerated generator is L_epsilon=L_0+sigma_micro(epsilon) S. L_0 exchanges ordered adjacent pairs (1,0) and (0,−1) at rate1 and (1,−1) at rate2; it has no other effective transitions. S exchanges neighbors at rate1. There are no spin flips or creation/annihilation events. Set eta=1−omega² and xi=−omega. The empirical fields use space epsilon k and time t/epsilon.

The associated state is U=(rho,u) in

D={rho>=0, rho+|u|<=1}.

The flux is f(U)=(rho u,rho+u²), up to the immaterial constant −1 in the second microscopic expected current. Thus

rho_t+(rho u)_x=0,    u_t+(rho+u²)_x=0.                 (L)

Use epsilon sigma_micro→0 and epsilon sigma_micro²→infinity; take (sigma_micro/epsilon)^(1/3)<<ell<<sigma_micro. Here x<<y means x/y→0. The illustrative OWR choice is sigma_micro≈epsilon^(−1/2)log(1/epsilon), ell≈epsilon^(−1/2)sqrt(log(1/epsilon)). Its three ratios are epsilon sigma_micro→0, sigma_micro/(epsilon ell³)≈log(1/epsilon)^(−1/2)→0, ell/sigma_micro≈log(1/epsilon)^(−1/2)→0.

In Fritz–Toth's periodic notation n=epsilon^(−1), sigma_paper=sigma_micro/n, and G_n=n L_n+n² sigma_paper K_n. Their two inequalities n^(−1/2)<<sigma_paper<<1 and n^(2/3)sigma_paper^(1/3)<<ell<<n sigma_paper become the displayed infinite-line scales. Their spin sign and asymmetric orientation differ; these conventions are not mixed.

For an infinite-line formulation, let U_0 be measurable and D-valued, and require initial empirical pairings against every continuous compactly supported vector test to converge in probability to the pairing with U_0. No small-BV assumption, positive hole-density lower bound, or invariant rectangle is added. The OWR note does not state a complete initial-law theorem. Fritz2012 §4 states infinite-line strong local L1 compactness and concentration on entropy weak solutions, and refers to Fritz–Nagy2006 for localization beyond periodic space. That paper's proved uniqueness theorem concerns a different, spin-flip scalar relaxation. Accordingly, any use below of a Cauchy equation with the prescribed weak initial value is expressly an input, rather than an independently re-proved full infinite-line convergence theorem.

## Riemann coordinates and the inequality

Define on the entire closed physical triangle

a=(u+sqrt(u²+4rho))/2,    b=(u−sqrt(u²+4rho))/2.

Then a∈[0,1], b∈[−1,0], rho=−ab, u=a+b. The characteristic speeds are lambda_+=2a+b and lambda_−=a+2b. In the smooth strictly hyperbolic region,

a_t+lambda_+ a_x=0,    b_t+lambda_− b_x=0.

Both a and b increase along their own positively oriented genuinely nonlinear family. The requested Oleinik convention is therefore an **upper** bound on each invariant, not an upper bound on a and a lower bound on b:

a(t,y)−a(t,x)<=C(y−x)/t,
b(t,y)−b(t,x)<=C(y−x)/t,    x<y, t>0.                 (O)

For measurable limits the precise meaning is D_x a(t,.)<=C/t dx and D_x b(t,.)<=C/t dx in distributions for almost every t>0. Equivalently, for every nonnegative compactly supported smooth space test phi, −∫a phi_x<=C/t ∫phi, and similarly for b. One may then choose appropriate representatives for the pointwise inequality.

The OWR prose specifies neither a numerical C nor its allowed dependence on data. A full uniform theorem would specify a finite deterministic C for the declared initial-data/state class, independent of the microscopic scale and chosen subsequence. A weaker local target has C=C_{R,T} on |x|<R and 0<t<=T. The program proves neither target for general three-state limits. In particular, it does not silently assert that C=1/2 works in the coupled interior. The sharp value1/2 is proved only for the invariant scalar faces below.

## Boundary and uniqueness are separate issues

The map (a,b)→(rho,u) is smooth, but its inverse loses differentiability at a=b=0, equivalently (rho,u)=(0,0). This is zero **hole density** with balanced spins, not the empty-particle state. Empty particles correspond to (rho,u)=(1,0). The rest of the rho=0 edge is strictly hyperbolic. Formula(O) still makes distributional sense at the degenerate point because a and b are continuous there.

The inspected Bressan–Goatin author preprint, Theorems1–2 and(2.5), proves an Oleinik semigroup characterization on a convex compact Riemann rectangle E in a smooth strictly hyperbolic region satisfying strengthened cross-state condition(SH). For a rectangle a∈[A0,A1], b∈[B0,B1], a sufficient explicit version is

A1+2B1 < 2A0+B0,   A0>B1.

It also requires strong L1 time continuity and L1 perturbations of a reference state. The entire D fails these hypotheses: it contains the degenerate point and its speed ranges overlap. The 2025 Bressan–Marconi–Vaidya Temple semigroup theorem is a prior existence/stability result; it does not identify every stochastic entropy limit with that semigroup. Neither theorem supplies a microscopic invariant rectangle or an initial trace for this problem.

The source-v2 trace audit and its precise limitations are in SOURCE_SCOPE_AUDIT.md. A full proof must separately justify the prescribed initial trace and any deterministic uniqueness theorem's state-domain hypotheses, even after proving(O).

## Sources

1. J. Fritz, Hyperbolic scaling problems The method of compensated compactness, OWR43/2004, printed pp.2260–2262: https://ems.press/content/serial-article-files/45959
2. J. Fritz and B. Toth, Derivation of the Leroux system as the hydrodynamic limit of a two-component lattice gas, arXiv:math/0304481v2; journal DOI10.1007/s00220-004-1103-x: https://arxiv.org/abs/math/0304481
3. J. Fritz, Compensated compactness and relaxation at the microscopic level, Ann.Math.Informaticae39(2012),83–108, §§3.3–4: https://publikacio.uni-eszterhazy.hu/3223/1/AMI_39_from83to108.pdf
4. J. Fritz and K. Nagy, On Uniqueness of the Euler Limit of One-Component Lattice Gas Models, ALEA1(2006),367–392: https://alea.impa.br/articles/v1/01-16.pdf
5. A. Bressan and P. Goatin, Stability of L-infinity Solutions of Temple Class Systems, author preprint1998, published Differential Integral Equations13(2000),1503–1528: https://www.math.ntnu.no/conservation/1998/039.html
6. A. Bressan, E. Marconi and G. Vaidya, Uniqueness Domains for L-infinity Solutions of 2 by 2 Hyperbolic Conservation Laws,2025, §4: https://arxiv.org/abs/2505.00420
7. G.-Q. Chen and M. Rascle, Initial Layers and Uniqueness of Weak Entropy Solutions to Hyperbolic Conservation Laws, author preprint, published Arch.Ration.Mech.Anal.153(2000),205–220: https://people.maths.ox.ac.uk/chengq/preprints/rascle99/rascle99.pdf
