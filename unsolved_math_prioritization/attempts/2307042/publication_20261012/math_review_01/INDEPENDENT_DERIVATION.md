# Independent mathematical audit: PR810 / problem2307042

This review starts from the frozen authored proof and does not use earlier
reviewer conclusions. Numerical experiments below are falsification checks,
not proof substitutes. No priority or historical-novelty conclusion is made.

## Claim and scope

Let C=(0,1)×(R/2πZ), a=(1/2,0), and ξ=(0,π). Let H be the supremum of
positive harmonic functions h with h(a)≤1. The exact tested claim is that the
normalized minimal Martin kernel Kξ has Kξ<H in an entire punctured
neighborhood of a. This implies absence of any nontrivial initial equality
curve, in particular absence of an equality Green line.

The original source is Hayman–Lingham, Research Problems in Function Theory,
arXiv:1809.07200v2, Problem 7.42, printed p.173, with its update on p.174:
https://arxiv.org/pdf/1809.07200v2 . The source introduces the positive harmonic
supremum, gives equality of a disc kernel and that supremum along the radius,
then asks whether the resulting Green-line property extends to multiply
connected domains. The frozen proof correctly states the equality-along-line
interpretation and does not claim to rule out isolated contact farther away.
No assumption about a particular Green trajectory is necessary for the local
counterexample. (The source's displayed notation contains typographical
inconsistencies; those do not change the definition or the radius example.)

## 1. Independent Poisson and Green derivation

Use the strip complex coordinate w=y+ix and T(w)=exp(πw). Its image is the
upper half-plane. The boundary point η+0i maps to b=exp(πη), with Jacobian
db/dη=πb. If T(w)=R exp(iπx), the upper-half-plane Poisson density times this
Jacobian is

    (1/π) [R sin(πx)/|R exp(iπx)-b|²] πb
      = sin(πx) / [2(cosh(π(y-η))-cos(πx))].

This confirms the coefficient, argument scale, and boundary-coordinate
measure in formula (2). It is harmonic because it is the transformed harmonic
measure density, and is strictly positive for 0<x<1.

The Green function with logarithmic coefficient one follows from reflection
in the real axis in the upper half-plane. Written wholly in real coordinates,
the independent equivalent expression is

    gS(x,y;s,η) = (1/2) log
      [(cosh(π(y-η))-cos(π(x+s))) /
       (cosh(π(y-η))-cos(π(x-s)))].

The numerator minus denominator is 2 sin(πx) sin(πs)>0. Thus gS is positive.
At x=0 or x=1, the two cosines agree, so the boundary value is zero. At
(x,y)=(s,η), the denominator is asymptotic to
π²[(x-s)²+(y-η)²]/2 and the numerator has a positive limit, giving exactly
-log distance plus a smooth term. Hence the claimed normalization is right.
The expression is symmetric in its two points.

Differentiating at s=0 gives

    ∂s gS(x,y;0,η) = π sin(πx)/[cosh(π(y-η))-cos(πx)]
                     = 2π p(x,y-η).

Periodizing η by 2π yields the cylinder Green and Poisson formulas. For the
Green summands one may use the stable equivalent formula

    (1/2) log[1+2 sin(πx) sin(πs) /
                  (cosh(π(y-η))-cos(π(x-s)))].

For large |y-η| the denominator grows like exp(π|y-η|), giving exponential
decay. Derivatives of fixed order obey similar bounds when points avoid the
pole. This proves absolute uniform convergence on compact sets, permits
normal differentiation, and shows boundary vanishing uniformly locally.
Only one image pole occurs on the cylinder. The difference with the Dirichlet
Green function extends harmonically through that pole and continuously with
zero boundary values; the maximum principle gives uniqueness. Thus no
unaccounted constant, harmonic mode, or additional logarithmic pole appears.

For an independent Fourier check, separation of variables gives

    P(x,y)=(1-x)/(2π)+(1/π)∑_{n≥1}
                 sinh(n(1-x))/sinh(n) cos(n(y-π)).

The coefficients are dictated by a periodic unit point mass on x=0 and zero
data on x=1. In particular the boundary mass is ∫Pdy=1-x. The Green Fourier
formula, for x≠s, is

    gC = x_< (1-x_>) + 2∑_{n≥1}
         sinh(n x_<) sinh(n(1-x_>))/(n sinh(n)) cos(n(y-η)).

Its derivative jump is -1 in the constant mode and -2 in each nonzero cosine
mode, yielding ΔgC=-2πδ. The numerical audit compares these genuinely
different expansions with the image series.

## 2. Unrestricted boundary approach

Fix any compact first-variable set B⊂C. When η is near π and 0≤s≤ε,
the second-variable Green function is smooth up to s=0, uniformly for the
first variable in B. This follows either from the exponential image bounds
or reflection and the fact that the pole stays away from B. Since gC=0 on
the entire boundary segment, the uniform expansion is

    gC(w;η+is)=s [2πPη(w)+O(s)],

where Pη is the periodized density with boundary coordinate η. Pη(a) tends
to Pπ(a)>0. Dividing numerator and denominator gives Pπ(w)/Pπ(a), uniformly
on B, for every approach η→π, s→0 through s>0. There is no required relation
between s and |η-π|. In particular extremely tangential paths are covered.
The existence of the limit is therefore a valid Martin-limit statement.

## 3. Minimality: singularity and reflection stress test

Let 0≤v≤P be harmonic. At every boundary point other than ξ, P tends uniformly
locally to zero, so v has a continuous zero extension there. In coordinates
t=y-π near ξ, Taylor expansion of the elementary denominator gives

    cosh(πt)-cos(πx)=π²(x²+t²)/2 + O((x²+t²)²),
    sin(πx)=πx+O(x³).

Thus, uniformly for half-disc approaches,

    P(x,π+t)=x/[π(x²+t²)]+O(x).

The noncentral image terms vanish linearly in x and form a smooth remainder.
In particular P=O(1/r), r²=x²+t². This uniform remainder is stronger than
an estimate only on the normal axis and is sufficient for cancellation.

Odd reflection of v across the zero-value straight boundary is harmonic on
the punctured full disc. It has the same O(1/r) bound. To avoid assuming an
unsupported Laurent theorem, take angular Fourier coefficients U_n(r) of
the reflected harmonic function. They solve

    U_0''+r⁻¹U_0'=0;
    U_n''+r⁻¹U_n'-n²r⁻²U_n=0, n≥1.

Consequently U_0=A_0+B_0 log r and U_n=A_n r^n+B_n r^(-n). Each angular
coefficient is bounded by O(1/r); multiplying by r^n and taking r→0 gives
B_n=0 for every n≥2. The remaining negative first mode is a linear
combination of x/r² and t/r². Oddness under x↦-x kills log r, the constant,
and t/r², leaving only A x/r² and a regular harmonic remainder v0, odd in x.
Equivalently, after removing that dipole all Fourier modes are regular and
the remainder extends harmonically through the origin. This expansion does
not presume positivity or a single-valued harmonic conjugate. To check
convergence of the regular part, fix a circle of radius R inside the
punctured disc. Its bounded Fourier coefficients bound |A_n| by a constant
times R^(-n), so the positive-power series converges uniformly for r<R.

Comparison on t=0 gives 0≤A≤1/π. The difference v-πAP has cancelled dipole
and is O(x) near ξ; its regular part has value zero at the origin by oddness.
It is harmonic on C and continuous with zero boundary data everywhere on
the compact annular closure. Apply the maximum principle to this difference
and its negative. Therefore v=πAP, which is exactly minimality. This check
excludes possible logarithmic mass, higher-order dipoles, and hidden boundary
measure contributions. The Martin-limit and minimality arguments together
identify the claimed admissible kernel, without invoking the assertion being
proved about H.

## 4. Gradient and exact directional gap

Set q_k=sech((2k-1)π²), S1=∑q_k, S2=∑q_k². Direct differentiation of the
Poisson expression at x=1/2 gives p=q_k/2 and px=-πq_k²/2. Symmetric pairing
of image terms cancels py. Hence

    ∇K(a)=(-c,0),  c=πS2/S1>0.

S2/S1 is a weighted mean of the q_k with weights q_k/S1, and every q_k is
at most sech(π²). Consequently

    c ≤ πsech(π²) < 4/(83/2)=8/83 < 1/10,

using only 3<π<4 and cosh(π²)>1+π⁴/2>83/2. All signs and rational constants
in the authored calculation agree with this independent derivation. No
finite truncation is needed for the proof.

The four competitors have values 1±(x-1/2) and
1±b sin y cosh(x-1/2), b=1/[2cosh(1/2)]. They are single-valued after
exponentiation, since they are 2π-periodic in y. The Euclidean Laplacian in
logarithmic coordinates annihilates each, and the annular Laplacian differs
only by the positive conformal factor. The first pair is >1/2 and the second
pair is >1/2 in the interior. Each equals one at a. Thus global positivity,
global harmonicity, and normalization are all verified.

cosh(1/2)≤∑(1/4)^n=4/3<2, so 1/4<b<1. With displacement d=(u,v),
ρ=|d|, and M=max(|u|,b|v|), the exact first-order advantage is M+cu. Since
|u|≤M,

    M+cu≥(1-c)M,
    M≥(|u|+b|v|)/2≥b(|u|+|v|)/2>ρ/8.

Therefore the advantage exceeds (75/664)ρ>ρ/10, uniformly over all
directions, including nearly tangential directions and switching points
between the maximizing competitors. This is not just a pointwise-in-direction
limit; the lower bound is uniform. The finite smooth family provides a
common quadratic Taylor remainder. Taking any sufficiently small radius
with C0ρ<1/20 gives a strict positive gap at every nonzero displacement.
There is no use of differentiability of H, a fixed maximizing competitor,
or interchange of a supremum and a derivative.

An independent sharper diagnostic checks the limiting mesh value. Write the
unit displacement in the half-plane u≤0 as (-cos α, sin α), 0≤α≤π/2,
using symmetry in v. Before tan α=1/b the slope is (1-c)cos α and decreases;
after that switching angle it is b sin α-c cos α and increases. Thus its
minimum is (1-c)b/sqrt(1+b²). In the half-plane u≥0 the corresponding
piecewise slopes have their minimum at an axis or a switching point, both
strictly larger. This verifies the exact global first-order minimum reported
by the script, approximately 0.405216489. It is not needed for the proof's
conservative lower bound 1/10.

## 5. Consequence, boundary cases, and verdict

K(a)=H(a)=1. Since exponentiation is a local diffeomorphism at a, the
punctured-cylinder neighborhood yields the asserted annular neighborhood.
A continuous nontrivial equality curve that starts at a must contain distinct
points arbitrarily close to a when it leaves a; those points violate the
strict gap. Constant initial pieces do not rescue a nontrivial equality
curve. Green trajectories require no separate regularity calculation.

Boundary tests checked: either side of the strip; the exceptional point by
all half-disc approaches; highly tangential Martin approach; normal and
tangential base-point displacements; maximizing-competitor switches; the
constant and logarithmic harmonic modes; cancellation at the singular
boundary point; normalization at a; conformal passage back to the annulus.

Mathematical verdict: **PASS for the stated local strict-gap theorem and its
equality-along-a-Green-line consequence. No mathematical repair is required.**

Publication limitations: this proof establishes no statement about contact
farther from a and contains no historical priority theorem. The final paper
should retain the source interpretation and the limited local claim, and
priority must be audited separately. An explicit contact-free radius could
be added, but its absence is not a mathematical gap: the existing smoothness
and uniform Taylor argument proves existence rigorously.
