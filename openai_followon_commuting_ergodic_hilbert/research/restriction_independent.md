# Independent fixed-width restriction and commuting transference

Written 2026-10-06 22:12 PDT (2026-10-07 05:12 UTC). This reconstruction
starts from the original request, the definitions, and the October 5
continuous theorem statement. It does not assume the correctness of the
upstream proof. The exact verified result here is the implication
**continuous pointwise annular variation => discrete variation => commuting
ergodic variation and convergence**. Whether its continuous premise has a
valid proof is a separate dependency audit.

Checkpoint estimate: restriction/transference reconstruction 100%; full
mathematical resolution remains dependent on the continuous audit;
publication package 0% in this independent workstream. These percentages
are estimates, not evidence.

## 1. Precise conditional premise and variation convention

Fix a real number r>2 and put p=3/2. The only analytic premise used below is
the following statement, denoted (CV_r). For bounded compactly supported
simple complex functions F,G on R^2, set

    B_(a,b)(F,G)(u,v)
      = integral_(a<|t|<b) F(u+t,v)G(u,v+t) dt/t.

Define

    W_r(F,G)(u,v)
      = sup_(m>=1, 0<t_0<...<t_m, t_j rational)
          ( sum_(j=1)^m |B_(t_(j-1),t_j)(F,G)(u,v)|^r )^(1/r).

The supremum is taken **at each output point**, before its L^p norm. Assume

    ||W_r(F,G)||_(L^p(R^2)) <= C_r ||F||_(L^3) ||G||_(L^3).        (CV_r)

The annular theorem stated in the upstream October 5 manuscript is stronger
than this premise, because it permits all L^3 inputs. The present reduction
uses only the simple functions just specified. An estimate for a fixed
common partition, a supremum outside the norm, or dyadic radii does not
suffice for this proof.

For any complex sequence h=(h_N)_(N>=0) with h_0=0, define

    V_M^r(h) = sup_(0=N_0<N_1<...<N_m<=M)
                    (sum_(j=1)^m |h_(N_j)-h_(N_(j-1))|^r)^(1/r),
    V^r(h)   = sup_(M>=0) V_M^r(h),

where the empty partition has value 0. At finite M the menu of partitions
is finite. This anchored convention equals the usual homogeneous variation
allowing arbitrary N_0>=0: a partition starting later can be prefixed with
0, which only adds a nonnegative term. In particular

    sup_(N>=0) |h_N| <= V^r(h).

## 2. The lattice operators

For complex arrays A,B on Z^2, define

    D_N(A,B)(i,j)
       = sum_(0<|k|<=N) A(i+k,j) B(i,j+k)/k,
    D_0(A,B)=0.

Under (CV_r), the claim proved below is

    ||V^r(D_N(A,B):N>=0)||_(ell^p(Z^2))
       <= D_r ||A||_(ell^3) ||B||_(ell^3),                      (DV_r)

with the explicit (nonoptimal) constant

    D_r = 8 * 4^(2/3) * C_r + pi^2/13.

All ell^q norms use counting measure. The derivation first treats arrays
of finite support, and then extends to all ell^3 arrays.

## 3. Fixed positive-area cell embedding

Set

    h=1/8,   q=1/16,   rho=h+q=3/16.

Inside each unit lattice cell use the input box

    Q_(i,j) = (i-h,i+h) x (j-h,j+h),

of area m_in=(2h)^2=1/16, and the smaller output box

    P_(i,j) = (i-q,i+q) x (j-q,j+q),

of area m_out=(2q)^2=1/64. The input boxes are pairwise disjoint, as are the
output boxes. These widths are fixed once and for all.

For finite-support arrays set

    F(u,v) = sum_(i,j) A(i,j) 1_(Q_(i,j))(u,v),
    G(u,v) = sum_(i,j) B(i,j) 1_(Q_(i,j))(u,v).

These are bounded compactly supported simple functions. Their exact norms
are

    ||F||_3 = m_in^(1/3) ||A||_(ell^3),
    ||G||_3 = m_in^(1/3) ||B||_(ell^3).

Fix an output point (u,v)=(i+a,j+b) with |a|,|b|<q. The unshifted second
coordinate v lies in the input strip indexed by j and no other such strip;
the unshifted first coordinate u lies in the strip indexed by i and no
other. Therefore

    F(u+t,v) = sum_k A(i+k,j) 1_((-h-a,h-a))(t-k),
    G(u,v+t) = sum_l B(i,j+l) 1_((-h-b,h-b))(t-l).

The intervals associated to k and l cannot meet when k!=l. Indeed their
centers differ by (k-l)-(a-b), whose absolute value is at least

    1-|a-b| >= 1-2q = 7/8 > 2h = 1/4.

Thus only the diagonal k=l contributes to their product. The common
offset interval, independent of k, is

    I_(a,b) = (-h-min(a,b), h-max(a,b)) = (L,U).

Its length and location obey

    ell(a,b) = U-L = 2h-|a-b| >= h = 1/8,
    ell(a,b) <= 2h = 1/4,
    I_(a,b) subset (-rho,rho),  rho=3/16.

Consequently, almost everywhere in t,

    F(i+a+t,j+b)G(i+a,j+b+t)
      = sum_k A(i+k,j)B(i,j+k) 1_(k+I_(a,b))(t).                (3.1)

Using open boxes changes only interval endpoints and has no effect on
the integrals. Every output point in each P_(i,j) satisfies the geometry;
the proof never evaluates a representative on a measure-zero phase slice.

## 4. Half-integer radii, including negative k

For N>=1 use the continuous annulus

    1/2 < |t| < N+1/2.

The k=0 window is contained in |t|<rho<1/2, so it is excluded. For k!=0,
every t=k+s with s in I_(a,b) satisfies

    |k|-rho < |t| < |k|+rho.

Since rho<1/2 and |k| is an integer, this entire window is included if
1<=|k|<=N and excluded if |k|>=N+1. There is no partial window.

For k>0 the window has t>0 and |t|=k+s; for k=-m<0 it has t<0 and
|t|=m-s. Both have their radial support strictly inside
(|k|-1/2,|k|+1/2). The denominator in the latter case remains **-m+s**;
one must not replace it by the positive radial coordinate.

Define the coefficient

    K_k(a,b) = integral_(I_(a,b)) ds/(k+s),    k!=0.

Formula (3.1) now gives the exact identity

    B_(1/2,N+1/2)(F,G)(i+a,j+b)
       = sum_(0<|k|<=N) A(i+k,j)B(i,j+k) K_k(a,b).             (4.1)

More generally, for integers 0<=M<N,

    B_(M+1/2,N+1/2)(F,G)(i+a,j+b)
       = sum_(M<|k|<=N) A(i+k,j)B(i,j+k) K_k(a,b).             (4.2)

All radii in these identities are positive rational numbers, as required
by the countable continuous variation definition.

## 5. The exact coefficient error

Let ell=ell(a,b). The identity

    1/(k+s) - 1/k = -s/[k(k+s)]

holds for every positive or negative integer k!=0 and every s in I_(a,b).
It implies

    K_k(a,b) = ell/k + delta_k(a,b),
    delta_k(a,b) = -integral_(I_(a,b)) s/[k(k+s)] ds.

Since |k+s|>=|k|-rho and |k|>=1,

    |delta_k|/ell
      <= rho/[|k|(|k|-rho)]
      <= [rho/(1-rho)]/k^2
      = 3/(13k^2).                                           (5.1)

This proves the uniform O(k^-2) remainder directly, without an asymptotic
limiting argument and without shrinking widths.

As an independently checkable exact formula,

    K_k = log|k+U| - log|k+L|.

For k<0 it is negative. Generally K_(-k)(a,b) need not equal -K_k(a,b),
because the overlap interval can be asymmetric; the valid symmetry is
K_(-k)(a,b)=-K_k(-a,-b). The estimate (5.1) requires neither symmetry.

## 6. Pointwise full variation of the error

Write P_k(i,j)=A(i+k,j)B(i,j+k), and set

    E_N(i,j;a,b)=sum_(0<|k|<=N) delta_k(a,b)P_k(i,j),
    E_0=0.

At the chosen output point, (4.1) is

    C_N := B_(1/2,N+1/2)(F,G) = ell D_N + E_N,   C_0:=0.

For any partition 0=N_0<...<N_m, its increment index sets

    {k: N_(j-1)<|k|<=N_j}

are pairwise disjoint. Thus, for r>=1, the triangle inequality and the
elementary inequality ||z||_(ell^r)<=||z||_(ell^1) give

    (sum_j |E_(N_j)-E_(N_(j-1))|^r)^(1/r)
      <= sum_j |E_(N_j)-E_(N_(j-1))|
      <= sum_(k!=0) |delta_k(a,b)| |P_k(i,j)|.

Taking the supremum over **all** partitions therefore gives

    V^r(E_N)/ell
      <= (3/13) sum_(k!=0) |A(i+k,j)B(i,j+k)|/k^2.             (6.1)

The same argument works for any finite disjoint collection of integer
radial annuli: no single coefficient is counted twice. This is a total
variation bound for the error, not a bound for one selected partition.

Put

    J(A,B)(i,j)=sum_(k!=0) |A(i+k,j)B(i,j+k)|/k^2.

Hölder on Z^2, followed by translation invariance, gives for each k

    ||A(i+k,j)B(i,j+k)||_(ell^p)
       <= ||A||_(ell^3)||B||_(ell^3).

Since p>=1, Minkowski and monotone convergence yield

    ||J(A,B)||_(ell^p)
      <= (sum_(k!=0) k^-2) ||A||_3||B||_3
      = (pi^2/3) ||A||_3||B||_3.                              (6.2)

This step uses absolutely summable errors only; it never takes the
absolute value of the nonsummable principal kernel 1/k.

## 7. Integrating over the output fractions

For any finite partition, the ell^r triangle inequality applied to
C_N=ell D_N+E_N gives

    ell V_M^r(D_N) <= V_M^r(C_N)+V_M^r(E_N).

Formula (4.2) shows that the C_N increments occur among the rational
annular partitions defining W_r(F,G). Hence for each (u,v) in P_(i,j),

    V_M^r(D_N)(i,j)
       <= 8 W_r(F,G)(u,v) + (3/13) J(A,B)(i,j).                (7.1)

The same inequality holds with M=infinity by monotonicity. Integrate its
p-th-power norm over the disjoint union of all P_(i,j). The lattice
quantities are constant across their corresponding boxes, so Minkowski
gives

    m_out^(1/p) ||V_M^r(D_N)||_(ell^p)
      <= 8 ||W_r(F,G)||_(L^p(R^2))
           + (3/13)m_out^(1/p)||J(A,B)||_(ell^p).

Using (CV_r), the embedding norms, and (6.2), and dividing by
m_out^(1/p), gives

    ||V_M^r(D_N)||_(ell^p)
      <= [8(m_in/m_out)^(2/3)C_r + pi^2/13] ||A||_3||B||_3
      = D_r ||A||_3||B||_3.

Here 1/p=2/3 and m_in/m_out=4. The same inequality holds for V^r by
monotone convergence. The output has positive fixed area 1/64 in every
lattice cell, so there is no diagonal evaluation or divergent shrinking
factor.

For general A,B in ell^3, truncate both arrays to [-R,R]^2. For each fixed
M and each fixed (i,j), every D_N with N<=M eventually agrees exactly with
the untruncated array value. Thus the finite-menu V_M agrees eventually
pointwise. Fatou on counting measure and the finite-support estimate give
the estimate for V_M(A,B), with the same constant. Finally let M increase
and apply monotone convergence. This proves (DV_r) for all ell^3 inputs.

## 8. Representatives on a general probability space

Let (X,Sigma,mu) be a probability space and let S,T be commuting invertible
measurable measure-preserving transformations, with measurable inverses.
The proof needs no topological model, separability assumption, joint flow,
or suspension. Select measurable representatives f,g of the L^3 classes,
changing any infinite values to zero on their null sets. The resulting
representatives are finite everywhere; in particular every finite sum
below is a measurable complex function.

If transformations and their commutation are specified only modulo null
sets, choose versions with the corresponding almost-everywhere inverse
and commutation relations. Remove the union of the inverse images of their
exceptional sets under all finite words in S,S^-1,T,T^-1. This is a
countable null union, since all these maps preserve measure. On the
remaining invariant conull set the inverse and commutation relations hold
at every orbit point; every word can then be reduced to S^i T^j there.
All subsequent identities are on this set, which is enough for every
norm and almost-everywhere statement. When S,T are defined as commuting
maps to begin with, this extra restriction is unnecessary.

Changing f or g on a null set affects a term indexed by n only on the
inverse image of that null set under S^n or T^n. Removing their countable
union over n in Z makes every H_N simultaneously independent of the
chosen representatives. The countably many finite partitions used below
have the same property.

## 9. Finite-menu Calderón transference

Define

    H_N(f,g)(x)=sum_(0<|n|<=N) f(S^n x)g(T^n x)/n,
    H_0=0,
    V_M(x)=V_M^r(H_N(f,g)(x):0<=N<=M).

For each fixed M, V_M is measurable because it is the maximum over a
finite menu of continuous expressions in finitely many measurable H_N.
It is finite at every point where the chosen orbit values are finite.

Write W_L={-L,...,L}^2 and d_L=|W_L|=(2L+1)^2. For integers L>=0 and
M>=1, and for x in the conull invariant set, define the finite arrays

    A_x(i,j)=f(S^i T^j x) 1_(W_(L+M))(i,j),
    B_x(i,j)=g(S^i T^j x) 1_(W_(L+M))(i,j).

For (i,j) in W_L and 0<=N<=M, all necessary shifted indices remain in
W_(L+M). Commutation gives the exact identities

    A_x(i+n,j)=f(S^n S^i T^j x),
    B_x(i,j+n)=g(T^n S^i T^j x),

and therefore

    D_N(A_x,B_x)(i,j)=H_N(f,g)(S^i T^j x),
    V_M^r(D_N(A_x,B_x))(i,j)=V_M(S^i T^j x).                  (9.1)

Apply (DV_r), using the full lattice norm to dominate the sum over W_L:

    sum_((i,j) in W_L) V_M(S^i T^j x)^p
      <= D_r^p [sum_(W_(L+M)) |f(S^iT^j x)|^3]^(p/3)
                [sum_(W_(L+M)) |g(S^iT^j x)|^3]^(p/3).        (9.2)

Here p/3=1/2. Integrate in x. The left side is
d_L ||V_M||_p^p by invariance. Applying Cauchy-Schwarz on X to the right
side, and invariance again to each of its finite sums, bounds it by

    D_r^p [d_(L+M)||f||_3^3]^(1/2)
            [d_(L+M)||g||_3^3]^(1/2)
      = D_r^p d_(L+M)(||f||_3||g||_3)^p.

The right side is finite, so this argument also establishes integrability
of V_M without first assuming it. Consequently

    ||V_M||_p
      <= D_r [d_(L+M)/d_L]^(1/p) ||f||_3||g||_3.

For fixed M let L tend to infinity; d_(L+M)/d_L tends to 1. We obtain

    ||V_M||_p <= D_r ||f||_3||g||_3,                           (9.3)

uniformly in M. This is the required finite-window transference. It uses
finite invariant averaging, then increasing spatial windows; no ergodic
theorem, pointwise orbit average convergence, or assumption of ergodicity
is used.

## 10. Countable partitions, full variation, and maximal domination

The finite-menu V_M increases with M, and its limit is precisely the
anchored full variation over finite integer partitions. All such
partitions form a countable set. Thus

    V(x)=sup_M V_M(x)

is measurable. Monotone convergence applied to V_M^p and (9.3) gives

    ||V^r(H_N:N>=0)||_(L^(3/2)(X))
       <= D_r ||f||_(L^3(X))||g||_(L^3(X)).                   (10.1)

In particular V is finite almost everywhere. The countable maximal
function

    H^*(f,g)(x)=sup_(N>=0)|H_N(f,g)(x)|

satisfies H^*<=V, since the partition 0<N has the single increment H_N.
It therefore obeys

    ||H^*(f,g)||_(3/2)<=D_r||f||_3||g||_3.                    (10.2)

The same D_r works in (10.1) and (10.2). Choosing any one r>2 gives a
maximal estimate with a separately fixed numerical constant, if desired.

## 11. Almost-everywhere and norm convergence

The following elementary fact is sufficient: a complex sequence with
finite r-variation, for any finite r>=1, is Cauchy. If a sequence were not
Cauchy, there would be an epsilon>0 such that, after every index, two
later terms differ by at least epsilon. Inductively choose ordered pairs

    a_1<b_1<a_2<b_2<...,
    |h_(b_j)-h_(a_j)|>=epsilon.

The partition 0,a_1,b_1,a_2,b_2,...,a_m,b_m has variation at least
m^(1/r)epsilon, contradicting finite variation as m tends to infinity.
The pairs may always be chosen with a_1>0. Completeness of C proves
convergence to a finite limit.

Apply this fact on the conull set where V is finite. There is therefore a
measurable limit H(f,g)=lim_N H_N(f,g) almost everywhere; define it to be
zero on the measurable exceptional set where convergence fails. Since
|H|<=H^* almost everywhere, both H and H_N lie in L^p. Furthermore

    |H_N-H|^p <= (2H^*)^p almost everywhere,

and the right side is integrable by (10.2). Dominated convergence gives

    ||H_N(f,g)-H(f,g)||_(3/2) -> 0.

This argument proves the requested convergence directly from pointwise
finite variation and maximal domination. It does not require a dense
class with previously established convergence, a one-sided ergodic
average theorem, or exchange of uncountable limits.

## 12. Falsification checklist and exact remaining dependency

* **Positive/negative support:** both radial supports lie strictly inside
  (|k|-1/2,|k|+1/2). A direct negative denominator is retained throughout.
* **Cross-cell terms:** impossible by the center separation 7/8>1/4.
* **k=0:** excluded because rho=3/16<1/2.
* **Overlap degeneration:** impossible on the output boxes; ell>=1/8.
* **Phase asymmetry:** no invalid assumption K_(-k)=-K_k is used.
* **Error accumulation:** disjoint annuli assign each k at most once;
  summability is k^-2, not |k|^-1.
* **Point-dependent menus:** preserved under the pointwise inequality
  (7.1) and the equality (9.1), then integrated. No common partition is
  chosen for all output points or all x.
* **Integration measure:** the output fraction has fixed positive area
  1/64. No shrinking widths or measure-zero diagonal appear.
* **Window boundary:** W_(L+M) contains all shifts with |n|<=M, for every
  central index in W_L, including negative shifts.
* **Null sets:** finitely many terms at each M, countably many indices,
  partitions, and group words suffice for a common conull set.
* **Convergence:** finite r-variation rules out any infinite sequence of
  separated jumps; maximal domination supplies an integrable envelope.
* **Degenerate systems:** S=T=id gives H_N=0 by symmetric cancellation,
  consistent with every estimate. Identity of only one transformation
  introduces no additional hypothesis in transference.
* **Scope:** no noncommuting action, no r=2 endpoint, no one-sided Cesàro
  convergence, and no extension beyond L^3 inputs is claimed.

The strongest verified statement in this file is the conditional theorem:
if (CV_r) holds, all the lattice and arbitrary commuting ergodic conclusions
above follow with D_r=8*4^(2/3)C_r+pi^2/13. The fixed-width construction
and transference introduce no further unproved analytic dependencies.
If the continuous estimate has a material proof gap, this file does not
close that gap and must not be advertised as an unconditional solution.

## 13. Reproduced finite bookkeeping checks

`python3 research/restriction_geometry_check.py` passed under Python 3.14.6.
The saved output is `research/restriction_geometry_check_result.json`.
Using 70-digit decimal logarithms, the check made 14,850 assertions across
25 phase pairs, positive and negative indices through absolute value 32,
and additional indices +-1,000,000. The largest sampled value of
`k^2 |K_k-ell/k|/ell` was approximately 0.0730383, below the proved upper
bound 3/13. It tested off-diagonal window exclusion, exact half-integer
radial inclusion, the signed coefficient and reflected-phase symmetry.
Thirty reproducible random complex increment sequences were tested against
every anchored partition menu through M=7 for the error total variation
and the comparison with the embedded sequence. These are support for
kernel bookkeeping only; they do not verify (CV_r) or establish a uniform
inequality by sampling.
