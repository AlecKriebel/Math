# Independent derivation before historical review

Timestamp: 2026-10-13T04:05:47.429722+00:00

Inputs consulted so far: the hashed round-3 note.tex, governing AGENTS.md, and the live primary https://arxiv.org/pdf/1809.07200v2. No earlier review, verdict, audit, supplemental archive or package_review directory has been opened. The fetched primary PDF and its hash receipt are in this review directory; printed pages 173–174 were extracted and visually inspected.

## Exact target and quantifiers

The primary item defines the envelope of strictly positive harmonic functions normalized by h(a) ≤ 1. It states the disc example as equality along the radius aimed at the selected boundary pole, then asks if the associated property persists for multiply connected D, for each specified Martin kernel. I interpret this as a universal claim over domains, bases and prescribed minimal kernels, with a nontrivial Green line issuing from the base carrying equality. Equality merely at the base cannot be the nontrivial question because every normalized kernel and envelope equals 1 there. The wording does not uniquely specify whether contact somewhere farther along a line is enough; the candidate expressly selects the equality-along-line interpretation. The deduction below refutes equality on any initial nontrivial curve segment, and even equality on a sequence of distinct points converging to the base. It does not settle arbitrary isolated contact elsewhere.

The annulus 1 < |z| < e is a bounded connected doubly connected smooth Green domain. x=log|z| is global, y=arg z modulo 2π. The map exp(x+iy) induces a conformal cylinder-to-annulus equivalence; the reversed strip variable w=y+ix differs only by a conformal/anti-conformal linear convention, preserving harmonicity and Green functions.

## Direct construction and arbitrary Martin approach

For 0<x<1, the map exp(π(y+ix)) maps the strip bijectively to the upper half-plane. Pulling back the upper-half-plane boundary density Im Z/(π|Z−T|²) dT, with T=exp(πη) on the positive axis, gives
p(x,y−η)=sin(πx)/(2[cosh(π(y−η))−cos(πx)]).
Thus p>0, Δp=0, with zero continuous side values except its pole on x=0. Its compact-interior derivatives decay exponentially for |y−η|→∞. Periodizing η=π by period 2π gives P>0, periodic and harmonic, with one inner-boundary singularity at (0,π) on the quotient and continuous zero values on the rest of both boundary circles. No simply connected topology is asserted for the quotient.

The pulled-back Green function is
(1/2)log{[cosh π(y−η)−cos π(x+s)]/[cosh π(y−η)−cos π(x−s)]}.
Its numerator minus denominator is 2sinπx sinπs>0. It vanishes on x=0 and x=1 and has exactly the required −log|w−w'| pole. Its 2π periodization has one pole on the quotient; the boundary is compact, and uniqueness follows by applying the maximum principle to the bounded removable difference with any Green function. The remote image terms and their s derivatives decay exponentially uniformly with w in an interior compact set, η near π, s near 0. A Taylor expansion in s yields g_C(w,η+is)=2πsP_η(w)+O(s²), uniformly in η and locally uniformly in w. P_η(A) remains bounded away from zero. Dividing by s before normalization proves the Green ratios converge to P/P(A) even for tangential or highly uneven approaches, including s=o(|η−π|^N) for all N. Continuity of P_η as η→π completes this identification without a nontangential restriction.

## Minimality, with growth classification made explicit

For t=y−π, r²=x²+t², the local formula is
p(x,t)=x/(πr²)+O(x), uniformly through the half-disc, since the numerator is πx(1+O(x²)) and the denominator is π²r²(1+O(r²)). All other images are smooth and vanish on x=0, hence their sum is O(x). Therefore P=x/(πr²)+O(x).

If 0≤v≤P is harmonic, squeeze gives v=0 continuously on each nonsingular boundary arc. Odd harmonic reflection across x=0 near the puncture is legitimate, since these arcs have zero continuous data. The reflected v is single-valued harmonic on a punctured disc and |v|≤C/r. To justify the Laurent claim without assuming it: the n-th circle Fourier coefficient satisfies the radial harmonic ODE and is a_n r^n+b_n r^(−n) (and n=0 gives a_0+b_0 log r). The C/r bound implies b_n=0 for n≥2 by multiplying that coefficient by r^n and letting r→0. No angular multivalued term is allowed. Oddness across x=0 kills the constant/log term and the tangential t/r² dipole, leaving Bx/r² plus a regular odd harmonic function. On t=0 domination gives 0≤B≤1/π. Subtract πBP: the dipole cancels; the difference extends with value 0 at the singular boundary point (both regular reflected remainders are odd), and is zero on every other boundary point. The compact annular maximum principle forces the difference to vanish. Consequently P is minimal; P/P(A) is a normalized minimal Martin kernel at the stated inner-boundary point.

## Exact gradient and global admissible competitors

At A=(1/2,0), let q_k=sech((2k−1)π²). Direct differentiation gives p=q_k/2 and p_x=−πq_k²/2. Symmetry k↔1−k kills the y derivative. Both infinite sums converge absolutely, so
∇K(A)=(−c,0), c=π Σq_k²/Σq_k.
The quotient is a weighted average bounded above by max q_k=sech π². Elementary bounds 3<π<4 and coshπ²>1+π⁴/2>83/2 give 0<c<8/83<1/10. This is an infinite-series analytic bound, with no truncation or cancellation dependence.

h_x±=1±(x−1/2) and h_y±=1±b sin y cosh(x−1/2), b=1/[2cosh(1/2)], descend globally to the cylinder. Δ[sin y cosh(x−1/2)]=0. The x pair lies strictly between 1/2 and 3/2; the y pair is ≥1/2 because |sin y|≤1 and cosh(x−1/2)≤cosh(1/2). All four equal 1 at A. These are admissible for the original positive-function envelope, including strict positivity globally. Their gradients are ±e_x and ±b e_y. The elementary series bound cosh(1/2)≤Σ(1/4)^n=4/3 proves 1/4<b≤1/2.

For d=(u,v) and M=max(|u|,b|v|), the maximum linear competitor advantage is M+cu. Since |u|≤M, it is ≥(1−c)M. Also M≥(|u|+b|v|)/2≥b(|u|+|v|)/2>|d|/8. Hence the maximum linear advantage is >75|d|/664>|d|/10 uniformly in every real direction. No finite directional sample is needed; directions with u<0 are the potentially adverse ones and are covered by the −c|u| term.

The finite family h_j−K is C² on a fixed small closed coordinate disc; a common Hessian norm bound gives a common C_0|d|² Taylor remainder. For 0<|d|<min(r_0,1/(20C_0)), some j has h_j(A+d)−K(A+d)>|d|/10−C_0|d|²>0. The conformal local coordinate map carries this disc to a neighborhood U of a=e^(1/2). H≥max_j h_j therefore proves strict local punctured inequality. No differentiability, attainment or harmonicity of H is invoked.

## Independent falsification routes and present status

1. Original-target interpretation: primary visual/text check supports the chosen equality-along-line interpretation; weaker contact elsewhere remains outside the theorem.
2. Topological/descent failure: all candidates and periodizations are periodic; one singularity per quotient; no branch cut enters the claim.
3. Tangential Martin approach: uniform s-Taylor expansion defeats the possible hidden nontangential assumption.
4. Nonminimal boundary singularity: growth/reflection/Fourier classification above eliminates higher multipoles and logarithmic leakage.
5. Competitor positivity and missed directions: exact global amplitude and convex-gradient estimates cover both.
6. Common-remainder failure: finite family and interior compactness provide one bound before choosing the competitor, so directional variation cannot invalidate the local conclusion.

Strongest independently verified result: the theorem stated in the candidate, including the punctured neighborhood inequality, follows from the constructions with the explicit elementary estimates above. Remaining tasks are independent numerical/formula cross-checks, source/priority assessment, supplemental provenance and reproducibility, visual package review and metadata/archive closure. Historical first resolution is not established and cannot follow from a failed literature search.
