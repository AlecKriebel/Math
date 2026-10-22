# Independent universal proof review: PR1309 /2450EP1039

The claim is quantified over every positive integer n and every monic complex
polynomial f=prod(z−z_i), with all listed roots in the closed unit disk, including
repetitions. The inradius uses unrestricted centers and open disks in the strict
set |f|<1. The accepted assertions are R_n≥log(2)/n, R_n≤pi/(2n), a root-centered
open endpoint disk for each f, and maximum individual inradius exactly 1.
This resolves the explicitly posed uniform c/n subquestion and its worst-case
order. It does not assert that every individual inradius is O(1/n).

I read all mathematical steps in the actual pinned 8,601-byte reconstruction and
the full 18,102-byte audit. I independently derived the chain below. The previous
39,357-check receipts are historical metadata; I did not run their unavailable
checker or treat those counts as independent evidence.

## Kernel and conjugation

For auxiliary |u_i|<1, the reproducing kernels in H² are
k_u(w)=sum conj(u)^k w^k, with inner product linear in the first variable.
They are square summable and reproduce evaluation by Cauchy–Schwarz.
The finite Blaschke product B=prod(w−u_i)/(1−conj(u_i)w) is analytic past the
closed unit disk and has unit boundary modulus. Parseval gives norm(B)²=1 and
<B,1>=Lambda=B(0), without needing an almost-everywhere boundary-value theorem.
For g=1−conj(Lambda)B, direct expansion gives norm(g)²=1−|Lambda|², and
g(u_i)=1 even when the u_i repeat. The vector h=sum k_(u_i) satisfies <g,h>=n
and norm(h)²=S=sum_(i,j)1/(1−u_i conj(u_j)), after exchanging the finite indices.
Thus S is real, and n²≤(1−prod|u_i|²)S. The denominator is strictly positive.
No inverse Gram matrix or distinctness hypothesis is hidden. Removing the
conjugate on Lambda changes the norm and invalidates this argument.

## Torus bound and the permitted extension

For |x_i|=1 and 0<a<1, set
G=n log(1−a^n)−sum_(i,j)log|1−a x_i conj(x_j)|.
The derivative identity is
aG'=S_a−n²/(1−a^n), with S_a the kernel sum at sqrt(a)x_i.
In particular the n² constant terms from a q/(1−a q)=1/(1−a q)−1 must not
be lost. The kernel estimate implies G'≥0, and G→0 at a↓0. Exponentiating
gives the full ordered-pair bound (1−a^n)^n on the torus.

Only after dividing by its torus diagonal factors (1−a)^n do we extend:
T=prod_(i≠j)|1−a x_i conj(x_j)| ≤ ((1−a^n)/(1−a))^n.
Pairing opposite ordered factors expresses T as a product of squared moduli.
With one coordinate x_k variable, its incident factors are exactly
|prod_(j≠k)(1−a x_k conj(x_j))|². All other factors are fixed and nonnegative.
Coordinatewise maximum modulus on the closed disk moves each coordinate to the
circle without decreasing T. This proves the bound for the whole polydisk.
Applying this argument to the diagonal-inclusive expression would be false:
two zero coordinates give full product 1>(1−a²)². The candidate never does so.

## Separation and perturbations

Scale v_i=A x_i, A>0, and choose alpha=arsinh(sigma/(2A)), a=e^(−2alpha),
sigma>0. All divisions have 0<a<1. Expansion gives the exact nonnegative defect

  |1−a x conj(y)|²/a−|x−y|²−(1−a)²/a
  =(1−a)(2−|x|²−|y|²)+a(1−|x|²)(1−|y|²).

Multiplication over m=n(n−1)/2 unordered pairs gives
Q(v,sigma)≤A^(2m) a^(−m)((1−a^n)/(1−a))^n.
The geometric sum equals e^(−(n−1)alpha)sinh(n alpha)/sinh(alpha).
Its n-th power exactly cancels a^(−m); there is no residual exponential or
missing A power. Thus Q≤A^(n(n−1))(sinh(n alpha)/sinh(alpha))^n.
For n=1 the empty product and right side both equal 1.

For |w_i−z_i|≤t, t>0, the exact complex pairing is
(w_i−z_j)(w_j−z_i)=(w_i−z_i)(w_j−z_j)+(w_i−w_j)(z_j−z_i).
Writing d=|w_i−w_j|, e=|z_i−z_j|, triangle inequality and
(d²+t²)(e²+t²)−(de+t²)²=t²(d−e)²≥0 yield
V=prod|f(w_i)|≤t^n sqrt(Q(w,t)Q(z,t)). Zero factors are harmless.
Apply the separation estimate with A=1+t to w and A=1 to z. Taking the
nonnegative n-th root gives precisely

  V^(1/n)≤2(1+t)^(n/2)
    sqrt(sinh(n arsinh(t/2)) sinh(n arsinh(t/(2(1+t))))).

The estimates log(1+t)≤t, arsinh(s)≤s and monotonicity of sinh on nonnegative
arguments give V^(1/n)≤2e^(nt/2)sinh(nt/2)=e^(nt)−1. No small-t expansion,
floating-point bound or asymptotic uniformity is assumed. For n=1 it is simply
|w_1−z_1|≤t≤e^t−1. Boundary and repeated roots were permitted at each step.

## Disks, endpoint, upper witness and maximum

For each 0<t<log(2)/n, independently maximize |f| on each root-centered compact
closed t-disk. If all n maxima were ≥1, their maximizing points would violate
V≤(e^(nt)−1)^n<1. Therefore one whole closed disk has maximum <1.
Letting t increase to log(2)/n proves the supremum bound. For the stronger open
endpoint disk, a fixed index succeeds on an infinite subsequence of the radii,
because there are only finitely many listed roots. Every point strictly within
that endpoint disk belongs to a smaller successful closed disk. This argument
retains strictness without taking a limit of strict inequalities. It requires
neither attainment of the inradius supremum nor the same index at every radius.
It does not infer containment of a closed endpoint disk from this limiting step.

For p=z^n−1, every point w in |p|<1 is nonzero and has |w|<2^(1/n). When
|w|≤1, among the 2n rays at angles (2k+1)pi/(2n), one is within pi/(2n) of
arg(w). The point q on that ray with modulus |w| satisfies Re(q^n)=0,
|p(q)|≥1, and |q−w|≤|w| times that angular distance. When |w|>1, take q on
the same radial ray with modulus 2^(1/n); reverse triangle gives |p(q)|≥1,
and |q−w|<2^(1/n)−1≤1/n<pi/(2n). The binomial first two terms prove the
middle comparison, also for n=1. Each point is therefore within pi/(2n) of
the actual complement, so a larger contained disk is impossible. This does not
assume connectedness of the lemniscate or convexity of its lobes.

For any monic polynomial and a hypothetical contained disk of radius R>1,
choose 1<r<R. Continuity on its concentric compact circle gives maximum M<1.
The leading coefficient after translation remains 1. Cauchy's estimate yields
1≤M/r^n<1. Therefore every individual inradius is ≤1; z^n attains 1.
In particular an individual Theta(1/n) assertion would fail on this same family.

Verdict: the full asserted ordinary-mathematics theorem passes. Own small exact
diagnostics cover selected zero, repeated, boundary, complex and roots-of-unity
configurations, and reject three deliberate normalization/extension errors.
They supplement this universal written proof. No source program, Lean build,
dependency fetch, cache update or formal-axiom certification was performed.
