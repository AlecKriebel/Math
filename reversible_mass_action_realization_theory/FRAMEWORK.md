# Exact framework for reversible realization of a plane conic

This note fixes the first restricted realization problem and separates what is
already a theorem of elementary exact algebra from what remains a research
target.  It uses no literature-dependent assertions.

Let `K=Q`, let `R=K[x,y,z]`, and let

\[
I=(L,Q),
\]

where `L` is affine linear and `Q` has degree at most two.  The desired real
curve is

\[
C=V_{\mathbb R}(I)\subset \mathbb R_{>0}^3.
\]

The target realization is a finite connected reversible support on integer
complexes, with every directed rate positive, stoichiometric rank three,
`F_i in I`, a reduced conic component, and `gcd(F_1,F_2,F_3)=1`.

## 1. Exact geometric input certificate

Choose a rational affine parametrization of the plane

\[
x=p+Bu,\qquad p\in\mathbb Q^3,\quad
B\in\mathbb Q^{3\times2},\quad \operatorname{rank}B=2.
\]

After symmetrizing its quadratic part, write the restriction of `Q` as

\[
q(u)=u^TAu+2b^Tu+c,
\]

with rational symmetric `A`.  Multiplying `Q` by `-1` if necessary, the
following exact conditions certify a nonempty nonsingular ellipse:

\[
A\succ0,\qquad
\rho=b^TA^{-1}b-c>0.
\]

Indeed, with `u_0=-A^{-1}b`, the equation becomes

\[
(u-u_0)^TA(u-u_0)=\rho.
\]

Positive definiteness is certified over `Q` by Sylvester minors.  The curve is
compact and smooth: a zero of its `u`-gradient would be `u_0`, which does not
lie on the equation because `rho>0`.

There is also a sharp rational test that the entire ellipse lies in the open
positive orthant.  If row `i` of `B` is `r_i^T` and

\[
\mu_i=p_i+r_i^Tu_0,
\]

then the minimum of coordinate `x_i` on the ellipse is

\[
\mu_i-\sqrt{\rho\,r_i^TA^{-1}r_i}.
\]

Thus strict positivity is equivalent, for each `i`, to

\[
\mu_i>0,
\qquad
\mu_i^2>\rho\,r_i^TA^{-1}r_i,
\]

with the evident interpretation when `r_i=0`.  These are exact strict
polynomial inequalities after clearing known-positive denominators.  A
rational point on the conic additionally yields a rational line-slope
parametrization, but rational parametrizability is not needed for the real
continuum itself.

## 2. The fixed-support linearization theorem

Fix distinct complexes

\[
Y=\{y_1,\ldots,y_m\}\subset\mathbb Z_{\ge0}^3
\]

and undirected pairs `E`.  Each pair contributes both directed reactions.  In
a fixed order, let `k in K^{2|E|}` be their rates.  The mass-action field is

\[
F(k)=\sum_{i\to j} k_{ij}x^{y_i}(y_j-y_i).
\]

Fix a Groebner basis `G` of `I`.  Reduce every coordinate contribution of
every unit-rate reaction modulo `G` and expand the remainders in the finite
set of standard monomials that occurs.  Stacking their coefficients produces
a rational matrix

\[
M_{Y,E,I}:K^{2|E|}\longrightarrow K^N.
\]

**Fixed-support theorem.**  For every rate vector `k`,

\[
F_i(k)\in I\quad(i=1,2,3)
\quad\Longleftrightarrow\quad
M_{Y,E,I}k=0.
\]

**Proof.**  Each coordinate of `F` is linear in `k`, and normal-form
reduction is `K`-linear.  A polynomial belongs to `I` exactly when its normal
form is zero.  Equality of every standard-monomial coefficient is precisely
the displayed matrix equation.  No positivity or genericity assumption is
used.  `remainder_map.py` implements this construction exactly.  □

Consequently the full conic-preserving rate space on a fixed support is the
rational vector space `ker M`, not merely a locally fitted family.

## 3. Strict positivity is an exact cone problem

For the fixed support, define

\[
\mathcal C_{Y,E,I}=\ker(M_{Y,E,I})\cap\mathbb R_{>0}^{2|E|}.
\]

The following facts are immediate and useful.

1. A single rational vector `k>0` with `Mk=0` proves nonemptiness.
2. If nonempty, `C` is relatively open in `ker M`, has dimension
   `nullity(M)`, and contains rational points densely.
3. Strict feasibility can be decided by the normalized rational linear
   program

   \[
   Mk=0,\quad \sum_jk_j=1,\quad k_j\ge\epsilon,
   \]

   maximizing `epsilon`.  Strict feasibility is equivalent to an optimum
   `epsilon_*>0`; a basic optimum gives an exact rational certificate.
4. Equivalently, Stiemke's alternative says strict feasibility fails exactly
   when there exists `w` with

   \[
   M^Tw\ge0,\qquad M^Tw\ne0.
   \]

   For rational `M`, a nonempty dual certificate cone has a rational point.

The last formulation is especially useful for proof-producing rejection of a
candidate support.

## 4. Network conditions that are independent of rates

Once all directed rates are strictly positive, several requirements depend
only on the chosen support.

- Listing both orientations of every pair proves reversibility.
- Connectivity of the undirected graph proves one linkage class.
- The stoichiometric subspace is the span of the pair displacements
  `y_j-y_i`; an exact nonzero `3 x 3` minor proves full rank.
- At full rank, the positive compatibility class through every positive point
  is the whole positive orthant.  Hence every positive conic point lies in the
  same class.  The affine plane `L=0` containing the conic is not a
  conservation plane in this case.

At a source complex `y`, the coefficient of `x^y` in `F` lies in the strict
positive cone generated by outgoing displacements.  This local outgoing-cone
condition is a useful necessary filter, but paired reverse rates couple the
conditions at different sources; it is not by itself sufficient.

## 5. A local criterion for a reduced conic component

Assume `I=(L,Q)` is a smooth height-two prime.  For a conic-preserving rate
vector, choose polynomial identities

\[
F_i=A_iL+B_iQ,
\]

and form the `3 x 2` coefficient matrix

\[
H=\begin{pmatrix}A_1&B_1\\A_2&B_2\\A_3&B_3\end{pmatrix}.
\]

**Local reducedness lemma.**  If a `2 x 2` minor of `H` is nonzero at
`p in C`, then

\[
(F_1,F_2,F_3)_{\mathfrak m_p}=I_{\mathfrak m_p},
\]

and `rank DF(p)=2`.  Thus the steady scheme is reduced and equals the conic in
a neighborhood of `p`.

**Proof.**  The nonzero minor is a unit in the local ring.  Inverting its two
chosen rows expresses `L,Q` as local combinations of the corresponding two
`F_i`; the reverse containment follows from `F_i in I`.  Along `C`,

\[
DF(p)=H(p)D(L,Q)(p).
\]

Smoothness gives rank two for `D(L,Q)(p)`, while the minor gives rank two for
`H(p)`, so their product has rank two.  □

If one minor is nonzero in the coordinate ring `R/I`, the criterion holds at
the generic point of the conic and fails at only finitely many complex conic
points.  In a polynomial rate family, the condition that every minor vanish
in `R/I` is algebraic in the parameters.  Therefore one exact witness proves
generic reducedness along the conic within that family.

This lemma does **not** rule out a second curve elsewhere in the steady-state
variety.  That requires a saturation, dimension, or primary-decomposition
argument and remains a separate check.

## 6. Why coprimality is an open algebraic condition

Let `D` bound the degrees of all three coordinate fields on the support, and
homogenize each coordinate to degree `D`.  For `1<=e<=D`, triples sharing a
homogeneous factor of degree `e` form the affine cone over the image of

\[
\mathbb P(V_e)\times\mathbb P(V_{D-e}^{\oplus3})
\longrightarrow
\mathbb P(V_D^{\oplus3}),
\qquad (h,(q_i))\longmapsto(hq_i).
\]

The source is projective, so its image is closed.  The finite union over `e`,
including the origins of the affine cones, is closed.  Pulling this union back
along the linear rate-to-field map gives a Zariski-closed bad subset of
`ker M`.  Every affine common factor produces a homogeneous common factor, so
the complement consists of affine-coprime triples.

For rational coordinate forms, gcd one over `Q` also excludes a common factor
over `C`: all Galois conjugates of a common complex factor divide the rational
coordinates, and their product supplies a nonconstant rational common factor.
Thus a single geometrically coprime positive witness proves that coprimality
holds on a nonempty Zariski-open subset of the positive rate cone.

This is genericity only inside the conic-preserving kernel.  It says nothing
about arbitrary perturbations in the full rate space.

## 7. Exact bounded-support search program

For a maximum complex degree `D`, there are finitely many complexes
`(i,j,k)` with `i+j+k<=D`.  A proof-producing search can therefore proceed as
follows.

1. Enumerate complex subsets and connected undirected graphs only after
   applying the known rank and linkage lower bounds.
2. Reject supports whose displacement matrix has rank below three.
3. Build `M_{Y,E,I}` exactly and retain its row labels, rank minor, and kernel
   basis.
4. Solve the normalized strict-feasibility LP.  Save either a rational
   positive kernel point or a rational Stiemke certificate.
5. For feasible supports, compute the coordinate gcd of an exact positive
   point and the conic remainder of every field coordinate.
6. Obtain `F=HL+KQ` from exact division and test a minor of `[H K]` modulo
   `I` for local reducedness.
7. Only then compute saturations or residual components.  Those calculations
   refine the geometry but are not needed to certify the basic realization.

Enumeration must be staged: the number of graphs grows much faster than the
number of complexes.  Outgoing displacement cones, graph automorphisms,
rank-minor filters, and incremental remainder ranks should be applied before
full symbolic elimination.

For a parameterized family of conics `I_theta`, the entries of `M(theta)` are
rational functions after fixing leading terms of the Groebner basis.
Positivity of its kernel is then a semialgebraic condition in `theta`.  A
useful intermediate theorem would exhibit one support and explicit rational
rate functions positive on a nonempty semialgebraic region of ellipse space.

## 8. What the seed establishes

The independent seed verifier proves, for one positive ellipse and one fixed
ten-complex support:

- a `21 x 20` remainder matrix of rank `16` and nullity `4`;
- a full-dimensional strict positive kernel cone;
- connected reversibility and stoichiometric rank three;
- a clean primitive integral kernel point;
- a positive rationally parametrized continuum; and
- coordinate gcd one, with Jacobian rank two at an exact conic point.

This validates every layer of the proposed architecture in one instance.  It
does not show that this support realizes other ellipses.

## 9. Next lemmas and decision points

The next work should resolve these in order.

1. **Normalization lemma.** Determine which affine normalizations of a
   positive plane ellipse preserve the mass-action monomial structure.  A
   general affine change of concentration coordinates does not, so Euclidean
   equivalence of conics cannot simply be assumed.
2. **Open-region lemma.** For the seed support, vary the coefficients of
   `L,Q`, stratify by Groebner leading terms, and decide exactly whether
   positive kernels persist on a nonempty region of conic space.
3. **Support-extension lemma.** Find graph operations that preserve a positive
   realization while adding controlled monomial coefficients.  Such moves
   could build a universal support theorem without blind graph enumeration.
4. **Local-to-global lemma.** Identify tractable hypotheses ensuring that a
   locally reduced conic is the only positive-dimensional steady component.
5. **Universality decision.** Either prove that one bounded-degree support (or
   a finite catalog) realizes every ellipse satisfying explicit positivity
   inequalities, or extract an invariant that disproves such a statement.

Until one of these is proved, “every positive rational ellipse is realizable”
remains a stated target rather than a theorem.
