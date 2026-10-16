# Fresh final disposition adversarial review: PR104 / problem600008

Completed 2026-10-06 UTC. **Verdict: PASS for the proposed bounded analytic prior-result / classical-corollary disposition. No required correction and no unresolved concern within that disposition.** Closing PR104 without merging or preparing a new paper is supported. This review does not execute that closure or authorize a novelty claim. Original effort remains 1/5, with zero extra central proof-search turns.

## Claim, sources, and independence

I treated the proposed conclusion as a hypothesis: the submitted analytic result is sound but recoverable from earlier same-problem quadratures and a classical third-kind identity; no substantive new contribution has been established for publication in this program. The success condition was an independently checkable reconstruction without a fixed ambient billiard-period substitution, assumed existence of closed approximating billiards, unsupported ordinary elliptic torsion, or extension beyond positive axes and the actual null-chain count conventions.

I read the preserved original `ANALYTIC_CRITERION.md` first, followed by the actual problem in GKT2007 §§4–5 and Tabachnikov2015 §7. I then challenged ROOT's proposed adjudication and closing note against the full relevant DR2019 §§2–4, including Eq3.2, Proposition3.5, Proposition4.2, and Remark4.4, and the official DLMF19.7.8. The local DR file's first page identifies arXiv:1909.08154v1, 18 September2019; its lawful retrieval ledger records a public arXiv HTTP200 and the same file hash. I inspected PDF views of the count and source-question passages to avoid extraction sign errors. All three priority reports and three mathematical reports were read only after my independently written comparison was pinned at 03:45:24 UTC. I additionally checked Ivory's printed metric and Tejada's printed rotational example.

The source question permits all strictly positive parameters. GKT's precise map is equator-to-North-tropic-to-equator; Tabachnikov's later wording counts individual alternating full tropic arcs. Cayley's theorem supplies a motivating algebraic precedent, but the problem sentence asks for axis conditions without explicitly restricting them to a finite determinant. An analytic answer and a finite algebraic Cayley output must therefore remain distinct.

## Exact singular-limit challenge: surviving counts and signs

Set a1=a>b=a2>0 and a3=c>0. After the lightlike infinite-caustic limit, with remaining ellipsoidal caustic 0<gamma<b, the printed polynomial becomes

P_gamma(x)=(a-x)(b-x)(c+x)(gamma-x).

Let A_k, B_k, C_k integrate x^k/sqrt(P_gamma(x)) on [-c,0], [0,gamma], [b,a], respectively, with positive radicals. Eq3.2's first integral runs from 0 to -c. Thus its signs are exactly

-m1 A_k+n1 B_k-n2 C_k=0, k=0,1.

For x=gamma*s,

B0=2sqrt(gamma)/sqrt(abc)*(1+O(gamma)),
B1=4gamma^(3/2)/(3sqrt(abc))*(1+O(gamma)),
B1/B0=(2/3)gamma+O(gamma²).

The estimates use the integrals of (1-s)^(-1/2) and s(1-s)^(-1/2), equal to 2 and 4/3. A0 remains uniformly bounded near0 because 1/sqrt(gamma+v)<=1/sqrt(v); its other endpoint singularity is integrable. C0 is uniformly bounded for gamma<=b/2 by an integrable constant times [(x-b)(a-x)]^(-1/2). Both have finite positive limits.

Eliminating n1 through k=0 gives

n1 B1=(m1 A0+n2 C0)*(B1/B0) ->0

when the finite polar/coordinate counts m1,n2 are fixed. The belt count n1 grows as gamma^(-1/2). This is a formal necessary period relation or a relation along any appropriately counted closed approximation, not a proof that an integer-count closed approximation exists for each gamma. A fixed total count m1+n1 cannot be identified with the finite surface arc count, and the finite Cayley matrices cannot simply be evaluated at gamma=0.

At gamma=0, x=-v gives A1(0)=-I_v, while x=-u on [b,a] gives C1(0)=I_u. The surviving condition is therefore

m1 I_v=n2 I_u.

The sign is positive on both sides. No divergent term, orientation minus sign, or factor of two is discarded.

## Sufficiency and topology on the actual surface

A limiting necessary condition alone would be insufficient. The candidate independently supplies a bijective closed-belt chart, a smooth signed equator continuation, and a homeomorphic degenerate-tropic boundary. Its open-belt metric is

g=(v+f²)(dS²-dY²), f²=a sin²t+b cos²t>0.

The monotone transverse-root equation covers each belt point exactly once. At the equator both signed height and physical z have nonzero first-order coefficients in the signed variable sqrt(c-v). At a tropic the coordinate change is continuous with normal order v^(3/2), which suffices for cusp chains but does not provide a nonsingular boundary Lorentz metric. Integral curves of the open-belt null line fields are unparameterized geodesics; they have dS/dY=±1. The opposite-family continuation at the next boundary is unique when positive S-advance is retained.

The restricted printed separated differential agrees with this surface metric: with lambda1=-v and lambda3=w=f², the magnitudes of x dx/sqrt(P0(x)) are 2dτ and 2dS. The remaining middle coordinate is zero. This directly recovers the real null branches rather than assuming a family of closed billiards converges. The surface dynamics themselves prove sufficiency of n I_v=rL for GKT returns, or N I_v=rL together with even N for full tropic arcs.

A lambda1 full excursion 0 ->-c ->0 spans one full tropic arc, so its finite coefficient is N. The source's proof of Theorem3.2, CaseS1, printed p7, explicitly identifies n2 with x2=0 crossings. A winding-r path crosses that plane 2r times. Lambda3 traces [b,a] monotonically 4r times, but two such traversals make a full excursion. The abbreviated wording below Eq3.2 must be read with the source's crossing convention, giving n2=2r, not 4r. Thus

N I_v=2r I_u=rL, L=2I_u.

Each full arc and each GKT North-return passage advances S by I_v=2H. The source maps have the same displacement but different state spaces. Full arcs alternate two distinct tropics and must close after even N; odd GKT return counts are allowed. If rho=p/q is reduced, least GKT period is q and least full-arc count is lcm(2,q). Doubling an odd return pair supplies an even full-chain closure, without calling that doubled count a least period without the reduced-fraction test. The winding is ordinary winding around the equator: positive axis rescalings in (x,y) preserve the angle's winding, and S(t+2pi)=S(t)+L. Reduction of rho modulo one would lose this actual-path information.

## Classical identity with independently checked normalization

For a>b define delta=(a-b)/(b+c), g=c/a, and k²=delta*g. All are positive and 0<k²<1. Substitutions

w=(a-c*delta*sin²theta)/(1+delta*sin²theta),
v=c*(1-sin²theta)/(1+g*sin²theta)

in the positive I_u and I_v integrals give, using ordinary complete Pi and K,

I_u=2sqrt(a/(b+c))*[(1+g)Pi(-delta,k)-g K(k)],
I_v=2sqrt(a/(b+c))*[(1+g)Pi(-g,k)-K(k)].

At amplitude pi/2, the official [DLMF19.7.8](https://dlmf.nist.gov/19.7#E8) has its auxiliary c=csc²(phi)=1 and characteristics -delta,-g, whose product is k². The official [DLMF19.20.1](https://dlmf.nist.gov/19.20#E1) gives RC(0,y)=pi/(2sqrt(y)). Therefore

Pi(-delta,k)+Pi(-g,k)-K(k)
=pi/(2sqrt((1+delta)(1+g))).

Since (1+delta)(1+g)=(a+c)²/[a(b+c)], the above I_u and I_v sum to pi exactly. The negative characteristics have positive denominators over the entire interval, so there is no hidden pole or principal-value condition. This is the third-kind parameter connection formula, not the bilinear K,E relation. It yields

rho=I_v/L=pi/L-1/2=(1-M)/(2M), M=L/(2pi),

and n rho=r yields M=n/(n+2r). The complementary positive-characteristic substitution h=(a-b)/a and j=c/(b+c), with hj=k², independently gives I_u=2b/sqrt(a(b+c))*Pi(h,k) and I_v=2b/sqrt(a(b+c))*[Pi(j,k)-K(k)]. This agrees with the negative form. One finite Simpson diagnostic at (4,1,2) produced I_u=2.26934153935842, I_v=0.8722511142313729, sum equal to pi to displayed float precision; it corroborates the exact derivation and is not certified quadrature.

## Boundaries and rejected algebraic shortcut

Interchange of a,b amounts to a quarter-period shift in t. At a=b=A, direct evaluation gives

M=sqrt(A/(A+c)), I_u(limit)=pi M,
I_v=pi(1-M), rho=(sqrt(1+c/A)-1)/2.

The shrinking negative cut is a limiting period, not a zero integral. These formulas give c=A[(1+2r/n)²-1], with the same count/parity rules. Thus the original all-positive-axis scope is covered; zero axes are excluded rather than claimed solved. Common scaling, monotonicity in c, uniqueness for prescribed n,r, and least-period arithmetic are elementary consequences and supply no independently established novelty.

Tejada2018's Example4.9 uses ordinary semi-axis lengths A,C and prints a return increment pi/Q, Q=sqrt(A²+C²)/A. This differs from the actual same-tropic increment 2pi(Q-1); the proposed adjudication correctly avoids endorsing that numerical normalization. Its rationality classification is nevertheless Q rational, identical to the candidate's rotational closed-set condition. It is legitimate evidence of an earlier rotational classification, not prior printing of the normalized triaxial mean formula.

For the imported quartic y²=(p-qw)(c+p-qw)(1-w²), dS=-(p-qw)dw/(2y), the two infinities have residues +i/2 and -i/2. The differential is third kind. A real integrated-coordinate translation does not establish an ordinary elliptic-group translation or division-polynomial criterion. DR's nondegenerate ambient Jacobian statements cannot be substituted for the degenerate surface's differential without another argument. Rejecting this route does not rule out all algebraic criteria; ROOT's closing note preserves that distinction.

## Disposition and exact scope of acceptance

The analytic result is mathematically verified, but the decisive mechanism is explicit separation, the prior invariant density/Poncelet structure, the previously stated exact-problem degeneration in [DR2019](https://arxiv.org/abs/1909.08154v1), and a classical connection identity. My checked reconstruction establishes recoverability of the scalar criterion and count mapping; it does not merely repeat the introduction's solution claim. The printed exact mean formula and normalized surface-count statement are absent from the inspected DR passages, and the proposed note explicitly does not claim otherwise.

No substantive new contribution has been demonstrated. That is a bounded evidentiary conclusion sufficient to decline a new paper under this program; it does not rule out every conceivable novel reformulation or future theorem. Useful exposition, clearer count conventions, and this independent recovery do not by themselves establish the program's required novel resolution. Keyword absence and inaccessible literature were not used to manufacture novelty or prove a global absence theorem. The unread Wüstholz2021 and DR2015/2017 bodies remain attribution/firstness limits; no firstness claim is proposed, so those limits do not obstruct this close-without-paper disposition.

Required corrections: none. Retain the proposed note's qualifications: no exact-earliest-printing assertion, no finite algebraic Cayley recovery, no complete singular-flow convergence certification, no conventional human peer-review claim, and no promotion of an earlier arithmetic announcement to a verified equivalent theorem. The original effort and frozen proof/source bytes remain preserved. The three completed mathematical-family reports and narrow checker-repair verdict support the note's description of extensive AI-assisted verification; I did not repeat their entire diagnostic programs. No paper was prepared by this review.

All writes are confined to this assigned review folder. No outreach or outreach draft, Git mutation, PR/native-editor action, Zenodo action, or tracker action occurred. Recommendation completion is 100% within this bounded disposition, not historical exhaustiveness or publication clearance. The compact manifest hashes input/output artifacts and separates private source views from authored research outputs.


## Precise future native classification and accounting

A fresh source-bound native assessment may classify problem600008 as **already_solved for the literal analytic classification**, using the verified prior reconstruction/classical-corollary rationale above. That label must not silently certify the motivated finite algebraic Cayley output or earliest/exact prior printing. ROOT reports that current main still shows queued with0/5, while the authenticated submitted PR head shows claimed_solved with original effort1/5. The submitted eligibility and effort are pinned by this audit's preserved status, source-pair authentication, proof, and one-entry turns ledger; the current queued projection must not reset that effort.

An exact suitable assessment note is:

> Already solved for the literal analytic null-chain parameter classification: the submitted theorem is mathematically verified, and its criterion is recovered from Dragović–Radnović2019 Eq3.2/Remark4.4 with the checked surface count mapping and the classical DLMF19.7.8 identity. No substantive new contribution is established. Exact earlier printing/earliest priority and a finite algebraic Cayley criterion remain unverified. Original submitted effort1/5 is preserved/imported; this source-bound assessment adds zero central proof-search turns. The authenticated original claimed proof remains in an immutable archive.

This is a recommended correction of one target and a new assessment, not a rewrite of the original historical claimed_solved assessment. Retain all other targets and earlier assessments, and pin the archive to the original proof SHA256608217a2ffc120a965b165f5b6065edd83f8cf94c5e77f0f95a0326640db2dae. No native changes have occurred in this review, and I did not design or execute integration machinery.
