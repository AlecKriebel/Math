# The complete-ray critical transfer for the true fitness-two sign

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note gives an exact all-order reduction of the true active-tree
numerator along the ray from the complete replacement kernel to an arbitrary
loopless row-stochastic kernel.  It also isolates a concrete coloured-tree
order which would prove the global fitness-two theorem.

The matrix identities and the equivalence of the proposed signs are
**PROVED**.  The coloured-tree order and complete-ray monotonicity are
**EXACTLY REFUTED** by an undirected five-vertex graph.  The weaker
no-downcrossing statement, fixed-colour root sign, and global sign remain
**OPEN**.  Exact boundary calculations reported below are finite hostile
evidence only.

Joint convexity is not used.  In fact it is false already for directed
three-vertex kernels.  The ray question survives that counterexample.

## 1. Exact ray and determinant ratio

Use the active state space, complete law, and reward from
`COMPLETE_REFRESH_FOREST.md`.  Thus

\[
 K_\alpha=K_0+\alpha\Delta,\qquad
 q=H-c_0\mathbf 1,\qquad 0\leq\alpha\leq1,
\tag{1}
\]

and put

\[
 B_0=I-K_0+\mathbf1\nu_0,
 \qquad G=B_0^{-1},
 \qquad h=Gq,
 \qquad r=\mathbf1-h.                              \tag{2}
\]

Since `nu_0 q=0`, one has

\[
 \nu_0h=0,\qquad \nu_0r=1,
 \qquad (I-K_0)h=q.                                \tag{3}
\]

Define

\[
 T=G\Delta,qquad Q=I-r\nu_0.                     \tag{4}
\]

Then direct multiplication gives the two factorizations

\[
 I-K_\alpha+\mathbf1\nu_0=B_0(I-\alpha T),          \tag{5}
\]

\[
 I-K_\alpha+q\nu_0=B_0(Q-\alpha T).                \tag{6}
\]

Let

\[
 Z(\alpha)=\det(I-K_\alpha+\mathbf1\nu_0),\qquad
 N(\alpha)=\det(I-K_\alpha+q\nu_0).                \tag{7}
\]

For `0<=alpha<1`, the complete component makes `K_alpha` irreducible, so
`Z(alpha)>0`.  If `nu_alpha` is its stationary row, the determinant lemma
and the tree theorem give

\[
 \boxed{
 f(\alpha):=\nu_\alpha q={N(\alpha)\over Z(\alpha)}
 =1-\nu_0(I-\alpha T)^{-1}r.}                      \tag{8}
\]

At `alpha=1`, the identity holds by continuity whenever the endpoint active
chain is irreducible.  Thus the global fitness-two target is `f(1)>=0`.

## 2. The exact critical-point scalar

Write

\[
 R_\alpha=(I-\alpha T)^{-1}.                       \tag{9}
\]

Differentiating (8) gives

\[
 \boxed{f'(\alpha)=-\nu_0R_\alpha T R_\alpha r,}   \tag{10}
\]

\[
 \boxed{f''(\alpha)=-2\nu_0R_\alpha T R_\alpha
                         T R_\alpha r.}            \tag{11}
\]

Consequently, at a zero of `f`,

\[
 \nu_0R_\alpha r=1,                               \tag{12}
\]

and a downward crossing is exactly the sign

\[
 \nu_0R_\alpha T R_\alpha r>0.                    \tag{13}
\]

Likewise, at a critical point, an interior local minimum is exactly the
strict reverse of

\[
 \nu_0R_\alpha T R_\alpha T R_\alpha r\geq0.       \tag{14}
\]

Equations (12)--(14) are the minimal resolvent form of the proposed
no-downcrossing/no-interior-minimum route.  They do not assume convexity.

There is an equivalent polynomial form.  Put

\[
 J(\alpha)=N'(\alpha)Z(\alpha)-N(\alpha)Z'(\alpha).
\tag{15}
\]

Then

\[
 \boxed{f'(\alpha)={J(\alpha)\over Z(\alpha)^2}.}   \tag{16}
\]

Thus `J>=0` on the physical interval is a sufficient complete-ray
monotonicity theorem.  The weaker statement needed for the endpoint theorem
only has to exclude a first zero of `N` with `J<0`.

## 3. Rank projection and the double-root transfer

The complete rank projection `S` satisfies `S Delta S=0`.  Since `r` is a
rank function and `nu_0=nu_0S`,

\[
 \nu_0Tr=\nu_0\Delta r=0.                           \tag{17}
\]

This recovers `f(0)=f'(0)=0` directly from (8).

For a more literal transfer function, decompose the state space as

\[
 \operatorname{span}\{r\}\oplus\ker\nu_0.
\]

In this decomposition write

\[
 T=\begin{pmatrix}0&b\\ c&D\end{pmatrix},
 \qquad Q=\begin{pmatrix}0&0\\0&I\end{pmatrix}.   \tag{18}
\]

Whenever `I-alpha D` is invertible, block elimination in (6) gives

\[
 \boxed{
 N(\alpha)=-\det(B_0)\alpha^2
 \det(I-\alpha D)\,b(I-\alpha D)^{-1}c.}           \tag{19}
\]

The adjugate version of (19) is polynomial and therefore holds without the
invertibility qualification.  Formula (19) explains the universal double
root and reduces every higher forest order to one scalar input-output
transfer.  Its internal matrix is signed; no positivity of `D` is claimed.

## 4. A second exact quadratic-observable form

The same algebra gives a useful state-space identity.  Put

\[
 W=\Delta G\Delta h.                               \tag{20}
\]

Stationarity implies

\[
 \nu_\alpha-\nu_0=\alpha\nu_\alpha\Delta G.
\tag{21}
\]

Using `(I-K_0)h=q` and `nu_0 Delta h=0`, one obtains

\[
 \boxed{f(\alpha)=\alpha^2\nu_\alpha W.}           \tag{22}
\]

Thus a nontrivial zero on the complete ray is exactly a stationary
zero-average of the fixed quadratic observable `W`.  Pointwise positivity
of `W` would prove the theorem, but it is false.  For

\[
 P=\begin{pmatrix}
 0&1/2&1/2\\
 1/3&0&2/3\\
 1/4&3/4&0
 \end{pmatrix},                                    \tag{23}
\]

the active state `({0},1)` has

\[
 W(\{0\},1)=-{1\over3564}.                         \tag{24}
\]

Hence any proof of (22) must use stationary cancellation or an additional
Poisson/forest lift.

## 5. A sufficient coloured-tree order

Every active in-tree has `d=|Y|-1` edges.  Expand each edge as complete or
actual coloured.  Write the natural Bernstein expansions

\[
 N(\alpha)=\sum_{j=0}^d n_j {d\choose j}
              \alpha^j(1-\alpha)^{d-j},            \tag{25}
\]

\[
 Z(\alpha)=\sum_{j=0}^d z_j {d\choose j}
              \alpha^j(1-\alpha)^{d-j}.            \tag{26}
\]

Here `z_j>=0` is the total weight of coloured in-trees with exactly `j`
actual edges, while `n_j` is the same root sum weighted by `q(root)`.
Whenever `z_j>0`, put

\[
 \theta_j={n_j\over z_j}
 =E\{q(\text{root})\mid j\text{ actual-coloured edges}\}.          \tag{27}
\]

The following order would close the complete-ray theorem:

\[
 \boxed{\theta_0\leq\theta_1\leq\cdots\leq\theta_d.}             \tag{CT}
\]

Indeed, under the probability weights proportional to
`z_j binom(d,j) alpha^j(1-alpha)^(d-j)`, equation (8) reads
`f(alpha)=E_alpha theta_J`.  Differentiation gives the exact covariance
identity

\[
 \boxed{
 f'(\alpha)={\operatorname{Cov}_\alpha(\theta_J,J)
                   \over\alpha(1-\alpha)}.}         \tag{28}
\]

Thus `(CT)` implies `f'(alpha)>=0`.  Since `theta_0=theta_1=0`, it also
implies every `theta_j>=0` and hence the original forest-coefficient
conjecture.

The condition `(CT)` is **EXACTLY REFUTED** in Section 8.  Its covariance
consequence is exact, but it is not a viable universal lemma.  The surviving
fixed-colour target is only

\[
 \boxed{\theta_j\geq0\quad\hbox{for every }j,}       \tag{FC}
\]

equivalently nonnegativity of every true numerator control `n_j`.  This is
strictly weaker than ordering the controls across colours and is still
**OPEN**.

## 6. Hostile audit and convexity separation

The independent verifier establishes the following exact finite facts.

1. The factorizations (5)--(8), derivatives (10)--(11), compressed transfer
   (19), and quadratic-observable identity (22) hold on independent rational
   active chains.
2. Every deterministic directed endpoint on `n=3` and `n=4` satisfies the
   adjacent cross-product form of `(CT)` in the natural tree degree.  This is
   `8+81=89` endpoints.  Reducible endpoint zero coefficients are omitted
   only when the conditional ratio is undefined.
3. For the same 89 rays, every Bernstein coefficient of the exact derivative
   numerator `J` is nonnegative.
4. The recorded directed three-vertex Jensen witness has a strictly
   negative joint-convexity gap, while both of its complete rays pass the
   exact coloured-tree and derivative tests.
5. The simple matrix (23) exactly refutes pointwise positivity of `W`.

Items 2--4 are finite evidence, not a reduction in population order, and
Section 8 shows that neither pattern persists universally.  The remaining
theorem is an all-order proof of `(FC)`, or a still weaker exclusion of a
downward zero through (12)--(13).

## 7. Exact obstruction to a literal Stieltjes realization

The compressed transfer in (19) suggests trying to make `D` substochastic
by a diagonal/sign similarity, with `b,c` in opposite positive cones.  That
literal route is exactly false.

Take

\[
 P=\begin{pmatrix}
 0&1/3&2/3\\
 2/5&0&3/5\\
 4/7&3/7&0
 \end{pmatrix}.                                    \tag{29}
\]

In the canonical coordinates used by the verifier, `D` has both positive
and negative diagonal entries, and

\[
 D_{01}D_{10}=-{63985\over276623424}<0.             \tag{30}
\]

Diagonal similarity preserves diagonal entries and every two-cycle
product.  Hence neither `D` nor `-D` can be made entrywise nonnegative by a
diagonal/sign similarity, and `I-alpha D` cannot be made a `Z`-matrix by
such a similarity.  Moreover

\[
 \operatorname{tr}(D^3)=-{256\over114345}<0,        \tag{31}
\]

whereas every entrywise nonnegative matrix has nonnegative trace of every
positive power.  Thus `D` is not similar to a nonnegative matrix even by an
unrestricted similarity.  Its characteristic polynomial is

\[
 {x^2\over24012450}
 \{24012450x^6-1045605x^4+17920x^3+1420x^2-9\},    \tag{32}
\]

and an exact Sturm count gives only three distinct real roots.  In
particular `D` is not oscillatory.

The obstruction survives at the scalar transfer level.  Exact cancellation
in (19) gives

\[
 b(I-\alpha D)^{-1}c=
 {9\alpha^4-1594\alpha^2-23040\alpha+561649
  \over
  3(9\alpha^6-1420\alpha^4-17920\alpha^3
      +1045605\alpha^2-24012450)}.                 \tag{33}
\]

The denominator has exactly two real roots and four nonreal roots.  Hence
this transfer is not a rational Stieltjes transform with real atoms, even
though it has the required sign on the physical interval.

Finally, the endpoint vectors do not possess a universal opposite-orthant
orientation.  For

\[
 P=\begin{pmatrix}
 0&11/26&15/26\\
 4/5&0&1/5\\
 19/39&20/39&0
 \end{pmatrix},                                    \tag{34}
\]

one canonical coordinate has

\[
 b_6c_6={83\over9034740}>0.                        \tag{35}
\]

This product is invariant under diagonal sign changes, so no such change
can put `b` and `c` in coordinatewise opposite orthants.  These facts close
the naive substochastic/oscillatory/Stieltjes proof.  They do not refute a
larger positive realization or a grouped forest injection; the exact
fixed-colour route `(FC)` remains viable.

## 8. Exact undirected refutation of monotonicity and colour order

On five vertices, take the symmetric edge weights in lexicographic order

\[
 (w_{01},w_{02},w_{03},w_{04},w_{12},w_{13},w_{14},w_{23},w_{24},w_{34})
 =(10,100,10,1000,10000,1,1,1,1,10000).             \tag{36}
\]

This is a connected complete-support undirected weighted graph.  Exact
rational stationary sensitivity gives

\[
 0.098<f(97/100)<0.099,
 \qquad -0.017<f'(97/100)<-0.016,                   \tag{37}
\]

and

\[
 0.075<f(1)<0.076,
 \qquad -3.580<f'(1)<-3.579.                       \tag{38}
\]

Every quantity in (37)--(38) is computed over `QQ`; the verifier retains the
full rational fractions.  Thus complete-ray monotonicity and `J>=0` are
false even in the admissible undirected class.

The natural tree degree is 74.  The adjacent colour-ratio inequalities fail
exactly at

\[
 j=70,71,72,73.                                     \tag{39}
\]

The derivative numerator has degree 138.  Its Bernstein controls have the
exact sign pattern

\[
 0,\quad +\ (1\leq j\leq131),\quad
 -\ (132\leq j\leq138).                            \tag{40}
\]

By variation diminution, this particular ray has exactly one interior
critical point, a strict maximum; it has no interior minimum.

Most importantly, every true numerator control in degree 74 is
nonnegative: the first two vanish and all controls 2 through 74 are strictly
positive.  Hence the witness is not a counterexample to `(FC)`, to the
no-downcrossing statement, or to the endpoint theorem.  It proves that an
all-order forest argument must pair roots separately at each fixed colour
count; comparing consecutive colour counts is unnecessarily strong.
