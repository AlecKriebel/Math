# A verification of the known counterexample to Problem 5.28

## Scope and attribution

The negative answer is due to L. A. Rubel, A. L. Shields and B. A. Taylor,
*Journal of Approximation Theory* **15** (1975), 23–40, Proposition 4.3.
This is a self-contained verification of that known result, not a claim of
new resolution. The argument below uses their two-power function and
rescaling idea, with an explicit fixed cutoff and error budget in place of
their small-scale asymptotic estimates.

Write D = {z : |z| < 1} and T = {z : |z| = 1}. For a continuous function
on the closed disk define

\[
 \Omega_f(t)=\sup_{z,w\in\overline D,\ |z-w|\le t}|f(z)-f(w)|,
 \qquad
 B_f(t)=\sup_{z,w\in T,\ |z-w|\le t}|f(z)-f(w)|.
\]

**Theorem.** There is a nonconstant function F, continuous on the closed disk
and holomorphic on D, for which

\[
 \limsup_{t\downarrow0}\frac{\Omega_F(t)}{B_F(t)}
 \ge \frac{1668}{1667}>1.
\]

The numerical lower bound is merely a convenient certificate; it is not
claimed to be sharp or to improve the literature.

## 1. A boundary calculation in a half-plane

On the closed right half-plane H use the continuous principal powers and set

\[
 a=\tfrac14,\quad b=\tfrac13,\qquad g(z)=z^a+z^b.
\]

For t > 0 the modulus on the imaginary axis is exactly

\[
 \sup_{|u-v|\le t}|g(iu)-g(iv)|=|g(it)|.                 \tag{1}
\]

Here and below powers at zero are zero. We prove (1), including the
maximization over all real u and v.

First, for y > 0 both coordinates of g(iy) are positive and increasing:

\[
 \Re g(iy)=y^a\cos(a\pi/2)+y^b\cos(b\pi/2),\quad
 \Im g(iy)=y^a\sin(a\pi/2)+y^b\sin(b\pi/2).
\]

Thus |g(iy)| increases. Its argument also increases, since its tangent is

\[
 \frac{\sin(a\pi/2)+y^{b-a}\sin(b\pi/2)}
      {\cos(a\pi/2)+y^{b-a}\cos(b\pi/2)},
\]

whose derivative with respect to y^(b-a) has positive numerator
sin((b-a)π/2). In particular the argument lies between aπ/2 and bπ/2 = π/6.
Also g(-iy) is the complex conjugate of g(iy).

Fix a separation s > 0. If 0 ≤ y ≤ s, the two values g(iy) and g(i(y-s))
belong to the sector of radius |g(is)| and arguments between
-arg g(is) and arg g(is). This sector has angular width at most π/3
and diameter |g(is)|. To verify the diameter assertion, the squared
distance of radii r ≥ q with angle θ ≤ π/3 is at most
r² + q² - rq ≤ r². The bound is attained by the origin and g(is).

For y ≥ s put h_p(y) = y^p - (y-s)^p. For p = a,b, h_p is nonnegative
and decreasing, by differentiating on (s,∞) and using p < 1. The squared
difference is

\[
 h_a(y)^2+h_b(y)^2+2h_a(y)h_b(y)\cos((b-a)\pi/2).
\]

All terms are nonincreasing, so its maximum is at y = s. The case y ≤ 0
reduces to y ≥ s by conjugation and interchanging the endpoints. This
proves that the maximum at separation s is |g(is)|. Finally maximize over
0 ≤ s ≤ t, using its monotonicity. This proves (1).

At t = 1, abbreviate

\[
 G=|g(i)|=2\cos(\pi/48)<2=g(1).                       \tag{2}
\]

## 2. Make the function bounded without destroying the strict gap

Let R = 2^24 and define

\[
 h(z)=\frac{R}{R+z}g(z)\qquad(z\in H).
\]

This function is holomorphic in the open half-plane, continuous on H,
bounded, and tends to zero uniformly as |z| tends to infinity within H.
For z in H,

\[
 |R+z|\ge\max(R,|z|),\qquad
 \frac{|z|^p}{|R+z|}\le R^{p-1}\quad(0<p<1).
\]

Consequently

\[
 M:=R^a+R^b=320\quad\hbox{satisfies}\quad |h(z)|\le M,
\]

and

\[
 A:=\sup_{z\in H}\frac{|g(z)|}{|R+z|}
 \le R^{a-1}+R^{b-1}=\frac5{2^{18}}.                 \tag{3}
\]

Let B be the modulus of h on the imaginary axis at distance 1.
The identity

\[
 h(z_1)-h(z_2)=\frac R{z_2+R}(g(z_1)-g(z_2))
 +\frac{R(z_2-z_1)g(z_1)}{(z_1+R)(z_2+R)}
\]

and (1) give B ≤ G + A. Meanwhile h(0) = 0 and h(1) = 2R/(R+1).
We will use the strict estimate

\[
 \frac{h(1)}{B}>\lambda:=\frac{1001}{1000}.           \tag{4}
\]

For completeness this has a rational certificate. If x = π/48 then
1/16 < x < 1, since 3 < π < 4. The alternating cosine bound gives
cos x ≤ 1 - x²/2 + x⁴/24. This polynomial decreases on (0,1), so

\[
 G<2\left(1-\frac{(1/16)^2}{2}+\frac{(1/16)^4}{24}\right)
 =\frac{1569793}{786432}.
\]

Using this and (3),

\[
 \frac{h(1)}B>
 \frac{1649267441664}{1646063091521}>
 \frac{1001}{1000}.
\]

We also have B > 1: indeed
|h(i)| = 2 cos(π/48) R/sqrt(R²+1) > 1, because
cos(π/48) > cos(π/4) = 1/sqrt(2) and R > 1.

## 3. Transfer the gap to arbitrarily small disk scales

For N > 1 let C_N be the circle |z-N| = N, and put

\[
 B_N=\sup_{z,w\in C_N,\ |z-w|\le1}|h(z)-h(w)|.
\]

We need the precise convergence

\[
 B_N\longrightarrow B\qquad(N\longrightarrow\infty). \tag{5}
\]

For the upper bound, consider any sequence of admissible pairs on C_N.
If their norms tend to infinity along a subsequence, both function values
tend to zero. Otherwise one can pass to a subsequence on which both
points converge, because their mutual distances are at most 1. The circle
equation Re z = |z|²/(2N) shows that both limits lie on the imaginary
axis. Their distance is at most 1 and their h-difference is at most B.
This compactness argument, applied to pairs attaining B_N, proves
limsup B_N ≤ B.

For the lower bound, take any two points iu,iv with |u-v| < 1. For N
larger than |u| and |v|, points of C_N approaching them are

\[
 z_N(u)=N-\sqrt{N^2-u^2}+iu,\qquad z_N(v)=N-\sqrt{N^2-v^2}+iv.
\]

Their distance is eventually less than 1, so liminf B_N is at least
|h(iu)-h(iv)|. Pairs with |u-v| = 1 can first be multiplied by a real
number tending upward to 1; continuity recovers their differences.
Taking the supremum proves (5).

In view of (4), (5), and B > 1, choose N_0 > 1 such that for every
N ≥ N_0,

\[
 h(1)\ge\lambda B_N,\qquad B_N\ge B/2>1/2.
\]

Set t_* = 1/N_0 and c = 1/640. For each 0 < t ≤ t_* let N = 1/t and

\[
 k_t(z)=\frac{h(N(1-z))}{M}\quad (z\in\overline D).
\]

The affine image of the closed disk is contained in H and its boundary
is C_N. Each k_t belongs to the disk algebra, and

\[
 \|k_t\|_\infty\le1,\quad
 B_{k_t}(t)=B_N/M\ge c,\quad
 |k_t(1-t)-k_t(1)|=h(1)/M\ge\lambda B_{k_t}(t).       \tag{6}
\]

The equality of boundary moduli follows because the affine map multiplies
all distances by N. This creates a uniform gap at every sufficiently small
scale; a different k_t is permitted at each scale so far.

## 4. Produce one function with infinitely many bad scales

Set

\[
 \eta=1/10000,\quad q=\eta c/4=1/25600000,\quad
 \varepsilon_n=q^{n-1}.
\]

The geometric tail satisfies

\[
 2\sum_{j>n}\varepsilon_j
 =\frac{2q}{1-q}\varepsilon_n\le\eta c\varepsilon_n. \tag{7}
\]

Choose 0 < t_1 ≤ t_* and put k_1 = k_{t_1}. Recursively, after
k_1,...,k_(n-1) have been fixed, choose

\[
 0<t_n<\min(t_*,t_{n-1}/2,1/n)
\]

so small that

\[
 \sum_{j<n}\varepsilon_j\Omega_{k_j}(t_n)
 \le\eta c\varepsilon_n,                            \tag{8}
\]

and put k_n = k_{t_n}. The choice is possible by uniform continuity of
each of the finitely many previous k_j. The use of the full disk modulus
in (8), not just the boundary modulus, controls radial differences too.

The series

\[
 F(z)=\sum_{n\ge1}\varepsilon_n k_n(z)
\]

converges uniformly on the closed disk, since ||k_n||∞ ≤ 1 and the
coefficients are summable. Hence F is continuous there and holomorphic
on D. Write b_n = B_{k_n}(t_n), so b_n ≥ c. At scale t_n, inequalities
(7) and (8) bound the sum of all differences from terms other than the
nth term by 2η c ε_n ≤ 2η b_n ε_n, for both radial and boundary pairs.
Thus (6) implies

\[
 |F(1-t_n)-F(1)|\ge(\lambda-2\eta)\varepsilon_n b_n,
 \qquad B_F(t_n)\le(1+2\eta)\varepsilon_n b_n.
\]

The radial lower bound is positive, so F is nonconstant. For any
nonconstant disk-algebra function, B_F(t) > 0 when t > 0: otherwise
constancy propagates by short arcs around T and the maximum principle
makes the function constant in D. Division is therefore legitimate, and

\[
 \frac{|F(1-t_n)-F(1)|}{B_F(t_n)}
 \ge\frac{\lambda-2\eta}{1+2\eta}
 =\frac{1668}{1667}>1.                              \tag{9}
\]

As t_n → 0, the theorem follows.

## 5. Match the exact problem convention

The problem defines the numerator using points of the open disk. This
has the same supremum as Ω_F(t): for any closed-disk pair z,w at distance
at most t, the points rz,rw lie in D for 0 < r < 1, have distance at most
t, and their function values converge to those of z,w as r tends to 1.
In particular the boundary endpoint 1 in (9) creates no convention gap.
The denominator is exactly the stated chord-distance boundary modulus.

Thus one fixed admissible function violates the proposed limit 1. The
failure is not merely a finite-scale inequality or a sequence of different
functions. Constant functions have an undefined 0/0 ratio, but the
counterexample is nonconstant and does not rely on that degeneracy.

## Verification limits

The accompanying standard-library script checks the exact rational
inequalities and geometric-series budget. The half-plane maximization,
compactness limit, uniform convergence, and holomorphy are proved above;
the script is not a formal verification of those analytic arguments.
