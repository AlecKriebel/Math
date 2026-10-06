# Covering deduction and inverse linear lower bounds

This is an independently checked exposition for Hayman–Lingham Problem 3.23. The affirmative answer is already recorded in [Update 3.23](https://arxiv.org/pdf/1809.07200v2), printed p.67. The upper-bound proof imports the covering theorem identified below; the lower examples are derived directly here. No novelty is claimed.

## Upper bound

Let D={z∈C:|z|<1}. Let u be nonnegative superharmonic on D with u(0)=1, allowing the value +∞ away from the origin. Both nonnegative Green potentials and positive harmonic functions belong to this class.

The imported premise is the r=1 case of [Eiderman, Theorem 4.2 and the following paragraph](https://www.researchgate.net/publication/314806417_Ocenki_potencialov_i_delta-subgarmoniceskih_funkcij_vne_isklucitelnyh_mnozestv), printed p.1315, attributed there to Govorov: if v is subharmonic on D, v(0)>0 and 0<M=sup_D v<∞, then for every P>1 there are at most countably many disks with total radius at most 1/P, outside which v≥−9PM. This is an explicit external premise; this derivative does not perform a fresh source inspection, and Govorov's original proof is not reproduced or independently verified here.

Define g(t)=1 for 0≤t≤28, and g(t)=27/(t−1) for t>28. For the first range, D itself covers {u>t} with radius 1.

For t>28 put L=t+1 and

u_L=min(u,L),  v=2−u_L=max(2−u,2−L).

The functions 2−u and the constant 2−L are subharmonic. Their finite maximum is subharmonic, even where the first function is −∞. In particular v is finite everywhere. At the origin, v(0)=1. Nonnegativity of u gives v≤2, so its actual supremum satisfies 1≤M≤2. This verifies every hypothesis of the imported theorem without asserting that M=2 or that the supremum is attained.

Choose P=(t−2)/18>1. The theorem yields a disk family of total radius at most B=18/(t−2). At every point of D outside the disks,

u_L=2−v≤2+9PM≤2+18P=t.

If u≤t then min(u,L)≤t. If u>t, including u=+∞, both u and L are greater than t, hence min(u,L)>t. Therefore {u_L>t}={u>t} pointwise. The theorem's disks cover the entire target, with no additional polar exceptional set.

The difference between the requested and obtained budgets is

g(t)−B=27/(t−1)−18/(t−2)=9(t−4)/((t−1)(t−2))>0.

If closed disks must be replaced by open disks, set δ=(g(t)−B)/2. Enumerate the family starting at k=1 and increase its kth radius by δ2^(−k). Every original closed disk lies in the corresponding open enlarged disk, and the new total is at most B+δ<g(t), because the geometric series sums to 1. The same estimate holds for a finite initial segment. An empty cover remains empty. No limiting process for covers is involved.

Thus the specified g works for both original classes and, in fact, for every u in the larger class just considered. Its limit at infinity is zero.

## An elementary disk covering lower bound

If countably many disks of radii r_j cover an open disk of radius R, orthogonal projection onto a line covers an interval of length 2R by intervals of lengths at most 2r_j. Countable subadditivity of interval length gives 2R≤2Σr_j, so Σr_j≥R. This also covers closed or degenerate disks in a countable family. One disk of radius R supplies the matching upper bound for the open disk itself. Its least possible total covering radius is therefore exactly R.

The countability condition is the ordinary one in the problem's disk family and in the imported theorem. No unsupported lower bound for uncountably many zero-radius sets is being asserted.

## Positive harmonic example

Consider

h(z)=Re((1+z)/(1−z))=(1−|z|²)/|1−z|².

The analytic function in this formula has no pole in D, so h is harmonic there. Its displayed expression is positive, and h(0)=1. For z=x+iy and t≥0, completing the square in 1−x²−y²>t((1−x)²+y²) gives

{h>t}=D(t/(t+1), 1/(t+1)).

This disk is contained in D and tangent to its boundary at 1. At t=0 it is D itself; for positive t it has the stated smaller radius. The projection argument shows that every disk cover has total radius at least 1/(t+1), and the displayed disk attains that bound. Consequently any universal budget for the positive harmonic class must satisfy g(t)≥1/(t+1).

## Green potential examples

Choose a real pole a with 0<a<1. The unit-disk Green kernel with that pole is

G_D(z,a)=log |(1−az)/(z−a)|,

with value +∞ at z=a. It is positive in D, harmonic away from its logarithmic pole and zero at the boundary, so it is the usual nonnegative Green potential of a point mass. Any conventional common constant multiplying the Green kernel cancels in the normalization below. Define

u_a(z)=G_D(z,a)/log(1/a).

Then u_a(0)=1 and the underlying point-mass coefficient is positive. For t≥0, let q=a^t. Monotonicity of the logarithm gives

u_a(z)>t  if and only if  |z−a|<q|1−az|.

For t>0, 0<q<1. The same algebra also works for t=0, when q=1. Squaring and completing the square shows that this set is the open Euclidean disk with center and radius

c_a(t)=a(1−q²)/(1−a²q²),

R_a(t)=q(1−a²)/(1−a²q²).

For example, the exact polynomial identity behind the calculation is

q²|1−az|²−|z−a|²=(1−a²q²)(R_a(t)²−|z−c_a(t)|²).

Its prefactor is positive. The right and left real endpoints are (a+q)/(1+aq) and (a−q)/(1−aq); the disk lies inside D. At t=0 these formulas give center 0 and radius 1. The projection lemma now gives a lower bound of R_a(t) for every cover of {u_a>t}.

Fix t≥0 and write a=e^(−s), with s>0. The radius simplifies to

R_a(t)=sinh(s)/sinh((t+1)s).

Since sinh(cs)/s→c as s→0, it follows that

lim_(a→1−) R_a(t)=1/(t+1).

For a universal Green-potential budget, g(t)≥R_a(t) holds for every a. Taking this scalar limit, at the fixed threshold t, gives g(t)≥1/(t+1). This does not take a limit of covering families. It also does not claim the lower bound is attained by a fixed Green atom: the pole is allowed to vary with the threshold and approximation accuracy because the proposed budget must work for every normalized Green potential.

## Meaning of the lower bounds

For either original class, every universal budget is at least 1/(t+1), whereas the proved upper budget is O(1/t). Thus inverse-linear decay is the best possible order uniformly over the class. These examples neither determine the optimal coefficient in a general upper bound nor show that the displayed coefficient 27 is sharp.

The code in `verify_independent.py` checks the algebra and representative exact-rational cases. The projection argument, potential-theoretic properties, theorem applicability and fixed-threshold limit argument above are the mathematical justification; sample counts alone cannot establish them.
