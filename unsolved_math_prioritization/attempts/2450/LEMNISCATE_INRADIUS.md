# Polynomial lemniscate inradius: credited sharp-order reconstruction

## Attribution and exact scope

This is database problem 2450 / EP-1039. For f(z)=product_(i=1)^n(z-z_i), n>=1, with |z_i|<=1, write rho(f) for the supremum of radii of open disks contained in {|f|<1}. We prove

(log 2)/n <= inf_f rho(f) <= pi/(2n),
and sup_f rho(f)=1.

Thus the explicit question rho(f)>>1/n is affirmative, and the minimum has order 1/n. This does not determine an exact limiting constant for the minimum, or say every individual polynomial has inradius of order 1/n.

The lower-bound strategy is credited to Liam Price's May 2026 GPT-assisted proposed proof, as documented in the public EP1039 discussion, and to Kenta Kitamura's corresponding May 2026 Lean development:
https://www.erdosproblems.com/forum/thread/1039
https://github.com/KitaKen1/erdos1039-lean

The advertised natural-language Overleaf project was inaccessible in this inspection. The current 7093-line Erdos1039.lean source was read statically at Git blob efc244f5d31674970b4ea0370b20c31955c779ea. Its product-inequality definitions, Hardy/Szego mechanism, main lower-bound bridge, and upper-bound theorem were inspected; this is not a claim to have read every tactic line or executed or verified that development. The proof below reconstructs the mechanism in ordinary mathematics, with no formal-code dependency or novelty claim.

The original Erdős–Herzog–Piranian 1958 Problem 3, printed p.134 (physical p.10), explicitly asks for a uniform c/n inradius. Its original scan is captured and was viewed:
https://users.renyi.hu/~p_erdos/1958-05.pdf

## 1. A finite Szego-kernel inequality

For u_1,...,u_n in the open unit disk, define

S = sum_(i,j=1)^n 1/(1-u_i conjugate(u_j)),
P = product_i |u_i|^2.

Then S is real and S >= n^2/(1-P).

Proof. Work in the elementary Hardy Hilbert space H2 of power series h(w)=sum h_k w^k with norm squared sum |h_k|^2, with inner product linear in its first argument. Its kernel k_u(w)=1/(1-conjugate(u)w) satisfies <h,k_u>=h(u), directly by the geometric series. Let

B(w)=product_i (w-u_i)/(1-conjugate(u_i)w),
Lambda=B(0), and g(w)=1-conjugate(Lambda) B(w).

B is analytic on a neighborhood of the closed unit disk and has modulus one on the unit circle. Parseval on that circle gives ||B||=1 and <B,1>=Lambda. Therefore ||g||^2=1-|Lambda|^2=1-P. Also g(u_i)=1 for every i, including repetitions. Put h=sum_i k_(u_i). Then <g,h>=n and ||h||^2=S (possibly with indices conjugated, the same real sum). Cauchy–Schwarz gives n^2<=S(1-P), proving the assertion. All functions used are rational and analytic beyond the closed disk, so the kernel/Parseval calculations require no boundary-limit theorem.

## 2. An off-diagonal product on the polydisk

For 0<a<1 and |x_i|<=1,

product_(i!=j) |1-a x_i conjugate(x_j)|
 <= ((1-a^n)/(1-a))^n.                                (1)

First suppose every |x_i|=1. Define

G(a)=n log(1-a^n)-sum_(i,j) log|1-a x_i conjugate(x_j)|.

All denominators are nonzero. Direct differentiation gives

a G'(a)=sum_(i,j) Re[1/(1-a x_i conjugate(x_j))]
          - n^2/(1-a^n).

Apply Section 1 to u_i=sqrt(a)x_i. Their product P is a^n, so G'(a)>=0. Since G(a) tends to 0 as a tends to 0+, G(a)>=0. Thus the product over all ordered pairs is at most (1-a^n)^n. Its n diagonal factors are each 1-a, proving (1) on the torus.

For general |x_i|<=1, group each unordered pair to write the left side as product_(i<j)|1-a x_i conjugate(x_j)|^2. Holding the other coordinates fixed, its dependence on x_k is a fixed nonnegative factor times

|product_(j!=k) (1-a x_k conjugate(x_j))|^2.

For pairs ordered the other way the modulus is unchanged by conjugation. The ordinary maximum-modulus principle therefore permits replacing x_k by a point on the unit circle without decreasing the product. Do this successively for the finitely many coordinates. The final torus bound proves (1). This also covers coincident coordinates.

## 3. Quadratic separation bound

For A>0, sigma>0 and |v_i|<=A, let alpha=arsinh(sigma/(2A)). Then

Q(v,sigma):=product_(i<j)(|v_i-v_j|^2+sigma^2)
 <= A^(n(n-1)) (sinh(n alpha)/sinh(alpha))^n.            (2)

To prove this scale v_i=A x_i and put a=exp(-2alpha). Then sigma^2/A^2=(1-a)^2/a. For |x|,|y|<=1 an exact calculation gives

(1/a)|1-a x conjugate(y)|^2-|x-y|^2-(1-a)^2/a
 =(1-a)(2-|x|^2-|y|^2)+a(1-|x|^2)(1-|y|^2)>=0.

Multiply this inequality over unordered pairs and use (1). The result is

Q(v,sigma) <= A^(n(n-1)) a^(-n(n-1)/2)
                   ((1-a^n)/(1-a))^n.

Since (1-a^n)/(1-a)=exp(-(n-1)alpha) sinh(n alpha)/sinh(alpha), the exponential powers cancel and give (2). For n=1 the empty product and the right side are both one.

## 4. Perturbed-root product inequality

Suppose |z_i|<=1 and |w_i-z_i|<=t, where t>0. Then

product_i |f(w_i)| <= (exp(nt)-1)^n.                   (3)

The diagonal factors |w_i-z_i| contribute at most t^n. For each i<j the complex-number identity

(w_i-z_j)(w_j-z_i)
 =(w_i-z_i)(w_j-z_j)+(w_i-w_j)(z_j-z_i)

and the triangle inequality give

|w_i-z_j| |w_j-z_i| <= t^2+|w_i-w_j| |z_i-z_j|
 <= sqrt((|w_i-w_j|^2+t^2)(|z_i-z_j|^2+t^2)).

The last step follows on squaring from t^2(d-e)^2>=0. Thus

product_i |f(w_i)| <= t^n sqrt(Q(w,t) Q(z,t)).

Apply (2) with A=1 to z and A=1+t to w. Using sinh(arsinh(t/(2A)))=t/(2A), this gives

(product_i |f(w_i)|)^(1/n)
 <= 2(1+t)^(n/2)
       sqrt(sinh(n arsinh(t/2)) sinh(n arsinh(t/(2(1+t)))))
 <= 2 exp(nt/2) sinh(nt/2)
 = exp(nt)-1.

Here log(1+t)<=t, arsinh(s)<=s for s>=0, and sinh is increasing on [0,infinity). These statements follow immediately by differentiating, with equality at zero. This proves (3).

## 5. The inradius lower bound

Fix 0<t<(log 2)/n. On each compact closed disk |w-z_i|<=t, choose w_i maximizing |f|. Such maximizers exist by continuity. If every maximum were at least one, the left side of (3) would be at least one. Its right side is less than one, a contradiction. Hence some root-centered closed disk of radius t satisfies |f|<1 throughout. In particular rho(f)>=t. Letting t increase to (log 2)/n proves rho(f)>=(log 2)/n.

There is even an open root-centered disk of the endpoint radius: choose a sequence t_j increasing to (log 2)/n and pass to an infinite subsequence with the same successful root center (there are only n choices). Every point in the open endpoint disk lies in one of those smaller successful disks. Thus it has |f|<1. This observation is not needed for the supremum definition but removes any largest-disk attainment ambiguity.

## 6. The upper witness and the maximum possible inradius

Let p_n(z)=z^n-1. Its roots have modulus one. Every point w in its lemniscate has |w|<2^(1/n) and w!=0.

If |w|<=1, select one of the rays arg(z)=(2k+1)pi/(2n) with angular distance at most pi/(2n) from arg(w), and let q be the point of that ray with |q|=|w|. Then Re(q^n)=0 and |q^n-1|^2=1+|q|^(2n)>=1. Also |q-w|<=|w| times the angular distance <=pi/(2n).

If |w|>1, choose q on the same radial ray with |q|=2^(1/n). Then |q^n-1|>=||q^n|-1|=1 and

|q-w|<2^(1/n)-1<=1/n<pi/(2n).

The middle inequality is (1+1/n)^n>=2, which follows from the first two nonnegative binomial terms (and is equality for n=1).

Thus each point in the lemniscate is within pi/(2n) of its complement. No open disk of larger radius can be contained in the lemniscate, proving rho(p_n)<=pi/(2n).

Finally every monic degree-n polynomial has rho(f)<=1, without any root-location hypothesis. Indeed if a disk of radius R>1 were contained in {|f|<1}, choose 1<r<R. On its concentric circle of radius r the maximum M is strictly less than one. Cauchy's coefficient estimate for the coefficient of (z-center)^n, which is one because f is monic, gives 1<=M/r^n<1, impossible. The polynomial z^n has lemniscate the open unit disk, so the supremum is exactly one.

## Conclusion and audit boundary

The original uniform positive-constant-over-n assertion and the sharp order of the worst-case inradius follow, with explicit constants log(2) and pi/2. The exact asymptotic constant of inf_f rho(f) is not determined. This is a complete ordinary-mathematics reconstruction of the credited 2026 product method, awaiting independent adversarial audit; it is not a claim to have verified the source Lean file. Standard dependencies have been stated and proved to the needed extent: finite Gaussian-free Hilbert-space calculations, Parseval for rational functions analytic past the circle, the maximum-modulus principle, elementary calculus, compact maxima, and Cauchy's coefficient estimate. No source-author program or proof-assistant code was run.
