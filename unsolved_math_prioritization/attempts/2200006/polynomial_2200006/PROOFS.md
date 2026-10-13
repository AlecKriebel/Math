# Proofs and exact scope

## 1. Definition and degree convention

Fix integers (k,l\ge1). Let (M(k,l)) denote the maximum number of isolated
points of (Z_\mathbb R(P)), over polynomials

\[
P(x)=\sum_{i=1}^r q_i(x)^2,\qquad q_i\in\mathbb R[x_1,\ldots,x_l],
\quad \deg q_i\le k,\quad\deg P=2k.
\]

The number of summands is unrestricted. An isolated zero is isolated in the
real zero set, not necessarily in the complex zero set of the summands. Other,
nonisolated real zeros are allowed. All counts are of distinct points.

The degree-exactly and degree-at-most conventions have the same extremal value.
Indeed, if a nonzero SOS has degree (2e\le2k), multiply it by

\[
(1+x_1^2+\cdots+x_l^2)^{k-e}.
\]

This factor is strictly positive on \(\mathbb R^l\), is SOS by its multinomial
expansion, and has degree (2(k-e)). Products of sums of squares are sums of
squares, and the new summands have degree at most (k). The product has degree
exactly (2k) and exactly the same real zero set. A sum of real squares has
degree twice the largest summand degree because its highest homogeneous terms
cannot cancel: a sum of squares of real homogeneous polynomials is identically
zero only if every one is zero. A zero polynomial has no isolated zeros when
(l\ge1), so it does not affect the maximum.

## 2. Elementary sharp cases and grid lower bound

For arbitrary (k,l\ge1), take

\[
g(u)=\prod_{j=1}^{k}(u-j),\qquad
P(x)=\sum_{a=1}^l g(x_a)^2.
\]

Its zero set is precisely \(\{1,\ldots,k\}^l\), so (M(k,l)\ge k^l).
For (l=1), the zero set of an SOS is contained in the zero set of any one
nonzero summand, which has at most (k) real roots. Therefore (M(k,1)=k).
For (k=1), the summands are affine-linear, so their common zero set is an
affine subspace or is empty. Such a set has either one isolated point or none.
The grid example attains one, hence (M(1,l)=1).

The equality (M(k,2)=k^2) is recorded by Shapiro with credit to Choi, Lam and
Reznick (1980). This packet does not claim a new proof of that historical planar
theorem. None of the later proofs depends on it.

## 3. What a valid complex Bézout reduction actually gives

For real (x), (P(x)=0) if and only if all (q_i(x)=0).
Suppose additionally that

\[
V=\{z\in\mathbb C^l:q_1(z)=\cdots=q_r(z)=0\}
\]

is finite. Then (\#V\le k^l).

To see this, choose successively (l) complex linear combinations (h_j) of
the (q_i). At each step, every positive-dimensional irreducible component of
the current intersection is not contained in the finite base locus (V).
Some (q_i) is consequently nonzero on that component. The combinations
identically zero on it form a proper linear subspace of coefficient choices.
Avoiding the finitely many such subspaces makes intersection with (h_j=0)
reduce every positive-dimensional component by at least one dimension. Existing
zero-dimensional components can remain or disappear. After (l) choices the
intersection is finite and still contains (V). The affine isolated-intersection
form of Bézout's theorem bounds its points, with multiplicities, by the product
of the degrees, hence by (k^l). A constant nonzero (h_j) makes the intersection
empty, which also satisfies the claim.

This argument uses the standard Bézout theorem; it does not supply a proof of
that theorem. More importantly, the additional complex-finiteness hypothesis is
absent from Problem 3. Even (q=x^2+y^2) has an isolated real zero and a complex
curve of zeros. Section 5 gives an example for which the missing hypothesis
causes the proposed numerical conclusion itself to fail.

## 4. A universal upper bound by perturbation and degree

**Proposition.** A globally nonnegative real polynomial of degree at most (2k)
in (l\ge1) variables has at most

\[
U(k,l)=\frac{(2k-1)^l+1}{2}
\]

isolated real zeros. Consequently (M(k,l)\le U(k,l)).

**Proof.** Let (a_1,\ldots,a_N) be any finite selection of distinct isolated
zeros of (f\ge0). Choose pairwise disjoint closed Euclidean balls (B_j)
centered at these points such that each boundary contains no zero of (f).
Compactness gives (\delta=\min_{\cup_j\partial B_j} f>0).
Set (R(x)=\sum_{i=1}^l x_i^{2k}), and first choose (\epsilon>0) sufficiently
small and then a vector (b\in\mathbb R^l) sufficiently small that

\[
|\epsilon R(x)-b\cdot x|<\delta/3
\]

on the union of all balls. The polynomial (g=f+\epsilon R-b\cdot x) is then
less than (\delta/3) at each center and greater than (2\delta/3) on every
boundary. It attains a local minimum in the interior of each (B_j).

Write (G=\nabla(f+\epsilon R)) and (D=2k-1). The degree-(2k) homogeneous
part (h) of (f+\epsilon R) is positive away from zero: the degree-(2k)
homogeneous part of (f) is nonnegative (or zero when \(\deg f<2k\)), as follows
by sending (t\to+\infty) in (t^{-2k}f(tx)\ge0). On the unit sphere (h\ge c>0).
Euler's identity therefore gives

\[
x\cdot G(x)=2k h(x)+O(\|x\|^{2k-1})>0
\]

outside a sufficiently large ball; moreover

\[
\|G(x)\|\ge (2kc+o(1))\|x\|^{2k-1}.
\]

Thus (G:\mathbb R^l\to\mathbb R^l) is proper. On a sufficiently large sphere,
the normalized map (G/\|G\|) is homotopic to the identity sphere map by
normalizing \((1-s)G(x)+s x\), which never vanishes there because its scalar
product with (x) is positive. The Brouwer degree of (G) is consequently (1).
Equivalently, the degree of (G-b) is (1) for every fixed bounded (b) and
a sufficiently large sphere.

We may choose the small vector (b) to be a regular real value of (G), by
Sard's theorem. Every real solution of (G(x)=b) then has invertible Jacobian.
It is also an isolated complex solution, by the complex inverse function
theorem applied to the polynomial extension of (G-b). Properness and
regularity make the real solution set finite. Bézout's bound on isolated
complex zeros of (l) polynomials of degrees at most (D), even when other
complex components are present, implies that its cardinality (T\le D^l).
The local Brouwer degree at a real solution is the sign of \(\det DG\). Let
(T_+\) and (T_-\) count the two signs. The degree formula yields

\[
T_+-T_-=1,\qquad T_++T_-=T,\qquad T_+=(T+1)/2.
\]

At each of the (N) local minima constructed above, the Hessian of (g) is
positive semidefinite and invertible, hence positive definite. Each minimum
therefore contributes a positive determinant. The balls are disjoint, so

\[
N\le T_+\le(D^l+1)/2.
\]

The bound holds for every finite selection of isolated zeros, which also proves
that the total number cannot exceed it. This completes the proof. \(\square\)

The standard external inputs are Sard's theorem, the local and global degree
formula, and the isolated-complex-zero form of Bézout. No numerical
optimization or assumption that the original critical locus is finite is used.
The coarser bound ((2k-1)^l) already follows before the signed-degree step.
These are classical methods; no originality claim is made for this bound.

## 5. Credited prior quartic counterexample

This construction is DannyExperiments' 2026 public result, not a discovery of
this investigation. In ten variables (t,x_0,\ldots,x_8), define

\[
q_0=x_0^2+t(t-8),\qquad
q_i=x_i^2-(t-i+1)(t-i)\quad(1\le i\le8),\qquad
P=\sum_{i=0}^{8}q_i^2.
\]

Every summand has degree two, and the coefficient of (x_0^4) in (P) is one,
so (P) is a nonnegative polynomial of degree exactly four. A real zero must
satisfy (x_0^2=t(8-t)\ge0), hence (0\le t\le8). The equation for (x_i)
excludes the interval (i-1<t<i). These eight intervals exhaust the
nonintegral part of ([0,8]), leaving only (t=0,\ldots,8).

At (t=0) exactly the radicands for (x_0,x_1) vanish; at (t=8) exactly those
for (x_0,x_8) vanish; and at (t=j\in\{1,\ldots,7\}) exactly those for
(x_j,x_{j+1}\) vanish. Every remaining radicand is positive. Thus each of the
nine slices has exactly (2^7) points, independently choosing the seven signs.
All 1,152 zeros are isolated because the real zero set is finite. Therefore

\[
1152\le M(2,10),\qquad 1152>2^{10}=1024.
\]

This refutes the proposed universal formula but cannot give the maximum.
Together with Section 4, the verified interval here is

\[
1152\le M(2,10)\le(3^{10}+1)/2=29525.
\]

The complex obstruction can be seen without a Gröbner-basis computation.
In the quotient of \(\mathbb C[t,x_0,\ldots,x_8]\) by the nine displayed
equations, monic division in the separate (x_i)'s gives a free
\(\mathbb C[t]\)-module with basis \(\prod_i x_i^{e_i}\), (e_i\in\{0,1\}).
Uniqueness follows by adjoining one variable at a time and dividing by its
monic quadratic. This quotient has dimension one: it is an integral finite
extension of \(\mathbb C[t]\), with that ring injected by the displayed free
basis. Thus the original equations do not have a finite complex zero set.

## 6. Credited general even-degree selector family

The following family also appears in the same prior release. Its reproduction
here is a proof verification with full boundary cases, not a novelty claim.

Let (k=2d\ge2), (l\ge3), (m=l-1\ge2), and (n=md). Use variables
(t,y_1,\ldots,y_m\). Define

\[
A_1(t)=-(t-d)(t-n)\prod_{r=1}^{d-1}(t-r)^2,
\]
\[
A_i(t)=(t-(i-1)d)(t-id)
       \prod_{r=(i-1)d+1}^{id-1}(t-r)^2\quad(2\le i\le m).
\]

All degrees are (2d). Their simultaneous nonnegative set is exactly
\(\{1,\ldots,n\}\). For (t<d), (A_1<0) except at its integer roots
(1,\ldots,d-1); for (t>n), (A_1<0). Within (d<t<n), a nonboundary
point lies in a unique block \(((i-1)d,id)\), (i\ge2), and (A_i<0) there
except at the internal integer roots. At every retained integer all factors
have nonnegative resulting signs. This also proves necessity at all real
nonintegers, not just at a finite sample.

There are (m(d-1)) internal integer points with exactly one zero among the
(A_i), and (m) boundary points (d,2d,\ldots,md) with exactly two zeros.
For (m=2,d=1), both polynomials vanish at both endpoints; the same count
applies, and there are no positive radicands at retained points.

Let

\[
F(y)=\prod_{r=1}^d(y-r)^2,\qquad
\eta=\min_{1\le r\le d,\ \sigma=\pm1} F(r+\sigma/3)>0.
\]

Let (B=\max_{1\le i\le m,1\le j\le n} A_i(j)\ge0) and choose
\(\epsilon=\eta/[2(1+B)]>0\). Put

\[
Q_i=F(y_i)-\epsilon A_i(t),\qquad S=\sum_{i=1}^m Q_i^2.
\]

This SOS has exact degree (4d=2k), since (y_1^{4d}) occurs with coefficient
one. At a real zero, (F(y_i)\ge0) forces (t\in\{1,\ldots,n\}).
When (A_i(j)=0), there are exactly (d) choices for (y_i). When (A_i(j)>0),
the constant (c=\epsilon A_i(j)) satisfies (0<c<\eta). The polynomial
(F-c) is negative at each (r\in\{1,\ldots,d\}) and positive at
(r\pm1/3\). The (2d) disjoint intervals \((r-1/3,r)\) and
\((r,r+1/3)\) therefore each contain a root. Its degree is (2d), so those
are all of its roots and are distinct. There are exactly (k) real choices.

Independence of the variables now gives the exact finite zero count

\[
m(d-1)d k^{m-1}+m d^2 k^{m-2}
=\frac{m(k-1)}4 k^m.
\]

Consequently

\[
M(k,l)\ge\frac{(l-1)(k-1)}4 k^{l-1}
\quad(k\text{ even},\ l\ge3).
\]

Strict violation of (k^l) occurs whenever \((l-1)(k-1)>4k\). The boundary
(k=2,l=3) gives exactly two zeros and is not competitive with the grid;
there is no claim that every member is an extremizer.
For odd (k\ge3), the even family for (e=k-1) transfers by the positive
degree-raising multiplier in Section 1. Simply forgetting the exact-degree
condition would not by itself justify that transfer.

## 7. Products and a finite exact optimization

If (P(x)\) and (Q(y)\) are SOS with finite zero sets in disjoint variable
sets, then

\[
Z_\mathbb R(P+Q)=Z_\mathbb R(P)\times Z_\mathbb R(Q).
\]

Thus their zero counts multiply, and (P+Q) still has degree at most the
larger degree. Degree raising from Section 1 can impose exact degree if needed.
For the quartic case, the even selector family yields a block in (s\ge3)
variables with \(c_s=(s-1)2^{s-3}\) zeros. In one variable the polynomial
\((u^2-1)^2\) contributes two zeros. These are prior mechanisms explicitly
acknowledged in the release; combining them is not claimed as new.

For an exact, restricted comparison define (b_0=1), and for (n\ge1),

\[
b_n=\max\bigl(2b_{n-1},\ \max_{3\le s\le n} c_s b_{n-s}\bigr).
\]

Induction constructs quartic SOS examples with exactly (b_n) finite zeros.
The same induction proves that (b_n) is optimal **among products of these
specific blocks and one-variable grids**: take the last block of any such
product. This recurrence does not give an upper bound for (M(2,n)).
The checker compares it with an independent exhaustive partition search
through (n=20), and records deterministic values through (n=60).

## 8. Homogenization does not restore the conjecture

Homogenize the quadratics of Section 5 to degree two using a new variable (z):

\[
q_0^h=x_0^2+t(t-8z),\qquad
q_i^h=x_i^2-(t-(i-1)z)(t-iz).
\]

At a real projective common zero with (z=0), the first equation gives
(x_0^2+t^2=0), so (x_0=t=0); the remaining equations then force every
(x_i=0). No projective point is represented by the all-zero vector, so
there are no real zeros at infinity. The homogeneous SOS therefore has exactly
1,152 real projective zeros, all in the affine chart (z=1).
Replacing affine zeros by projective zeros is not an escape from this
counterexample. This observation does not settle any lower-dimensional case.

## 9. Precise unresolved part

The exact value (M(k,l)) for all positive integers (k,l) is not obtained.
In particular, none of the arguments identifies (M(2,10)), shows that the
selector or product examples are globally optimal, classifies extremizers, or
controls all isolated real points on positive-dimensional complex base loci
with a sharp degree bound. A false (k^l) conjecture and a verified construction
are not a solution to the request to find the exact extremal function.

The later low-dimensional claims recorded in `SOURCES.md` are not premises of
this packet. The first-order gap is a sharp universal upper bound matching
a construction, rather than more numerical root counting in the displayed family.
