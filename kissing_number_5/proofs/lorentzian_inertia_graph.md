# Lorentzian inertia, a Perron bound, and the exact missing compatibility

## Scope

This note investigates the transformation
\[
 A=2G-J,\qquad W=I-A=I+J-2G                         \tag{1}
\]
for a hypothetical 41-point kissing code in \(S^4\).  It proves new exact
spectral and circuit consequences and gives a finite six-vertex
star-complement formulation.

It does **not** prove \(\tau(5)\leq40\).  An exact rational countermodel at
the end shows that the rank, inertia, sign pattern, scalar entry interval,
local graph bounds, deep origin position, and two positive circuits can all
coexist when the single common-source compatibility is weakened.  The
countermodel is explicitly indefinite and is not a spherical code.

## 1. Exact inertia and the nonnegative Perron matrix

Let \(X\) be the \(5\)-by-\(41\) coordinate matrix, with columns \(x_i\),
and let \(G=X^{\mathsf T}X\).  The exact cap theorem \(B(5)\leq34\) has two
immediate consequences.

First, \(\operatorname{rank}X=5\).  Otherwise a nonzero vector orthogonal
to the span of the code puts all 41 points on the equator of a closed
hemisphere, contradicting \(B(5)\leq34\).

Second,
\[
 {\bf1}\notin\operatorname{range}G
       =\operatorname{range}X^{\mathsf T}.             \tag{2}
\]
Indeed, membership would give \(u\in\mathbb R^5\) such that
\(\langle u,x_i\rangle=1\) for every \(i\).  After normalizing \(u\), all
41 points would again lie in one closed hemisphere.

Since \(2G\succeq0\) has rank five and the vector subtracted in (1) is
outside its range, elementary congruence gives
\[
 \boxed{\operatorname{rank}A=6,\qquad
        \operatorname{inertia}A=(5,1,35).}             \tag{3}
\]
For completeness, on the 35-dimensional space
\(\ker G\cap{\bf1}^{\perp}\), \(A\) vanishes.  On the six-dimensional
space \(\operatorname{range}G+\mathbb R{\bf1}\), the hyperplane
\({\bf1}^{\perp}\) is positive definite for \(A\), while the component of
\({\bf1}\) in \(\ker G\) has negative quadratic form.  This proves (3)
without a nonsingularity or genericity assumption.

The kissing inequality says
\[
 A_{ii}=1,\qquad A_{ij}\leq0\quad(i\ne j),
\]
so \(W\) is symmetric, entrywise nonnegative, and has zero diagonal.
The exact contact-link bound gives contact degree at most 15.  Therefore
the positive-entry graph of \(W\) has minimum degree at least 25.  It is
connected: two components would each have at least 26 vertices.  Thus
\(W\) is irreducible.

Write the nonzero eigenvalues of \(A\) as
\[
 -t,\ p_1,\ldots,p_5,\qquad t,p_i>0.
\]
Perron--Frobenius and (3) give the complete spectral template
\[
 \operatorname{Spec}W
 =\{\rho,\underbrace{1,\ldots,1}_{35},
                 \mu_1,\ldots,\mu_5\},                 \tag{4}
\]
where
\[
 \rho=1+t,\qquad \mu_i=1-p_i<1.                        \tag{5}
\]
The Perron root \(\rho\) is simple and has a strictly positive
eigenvector.

## 2. A new exact Perron interval

Taking the trace in (4) gives
\[
 \sum_{i=1}^5\mu_i=-(\rho+35).                         \tag{6}
\]
Every eigenvalue of a symmetric nonnegative matrix is at least
\(-\rho\).  Hence (6) first gives
\[
 \rho\geq\frac{35}{4}.                                 \tag{7}
\]

We need the following elementary maximization.

**Lemma.**  Suppose \(\rho\geq35/4\), that
\(-\rho\leq z_i\leq1\), and that
\(\sum_{i=1}^5z_i=-(\rho+35)\).  Then
\[
 \sum_{i=1}^5z_i^3
 \leq -\frac{(\rho+35)^3}{25}.                         \tag{8}
\]

**Proof.**  A maximizer exists on the compact box section.  If one
coordinate \(z\) were nonnegative, one of the other four coordinates
\(y\) would satisfy
\[
 y\leq-\frac{\rho+35+z}{4}<-z.
\]
Thus \(y+z<0\).  Replacing \(y,z\) by their common average stays in the
box and strictly increases their cube sum, because, with
\(m=(y+z)/2<0\) and \(d=(y-z)/2\),
\[
 y^3+z^3=2m^3+6md^2<2m^3.
\]
So every coordinate of a maximizer is negative.  The same averaging
argument applied to any unequal pair then shows that all five coordinates
are equal.  Their common value is \(-(\rho+35)/5\), proving (8). \(\square\)

Because \(W\geq0\),
\[
 \operatorname{tr}W^3
 =\sum_{i,j,k}W_{ij}W_{jk}W_{ki}\geq0.
\]
The inequality is strict here.  The positive-entry graph has at least
\(\lceil41\cdot25/2\rceil=513\) edges, more than the triangle-free maximum
\(\lfloor41^2/4\rfloor=420\), so it contains a triangle with positive
weight product.  Equations (4) and (8) now imply
\[
 0<\operatorname{tr}W^3
 \leq \rho^3+35-\frac{(\rho+35)^3}{25}.                \tag{9}
\]
The right side is strictly increasing for \(\rho>35/4\), since after
multiplication by 25 its derivative is
\[
 3(4\rho-35)(6\rho+35).
\]
At \(\rho=18\) it equals \(-2202/25\), while at \(\rho=73/4\) it equals
\(29457/400\).  If \(\rho_\star\) denotes its unique zero above \(35/4\),
then
\[
 18<\rho_\star<\frac{73}{4},\qquad
 \boxed{\rho>\rho_\star>18.}                           \tag{10}
\]

There is also a sharp elementary upper endpoint.  Let \(q>0\) be a Perron
eigenvector of \(W\).  Since \(Aq=-(\rho-1)q\) and \(A+J=2G\succeq0\),
\[
 0\leq q^{\mathsf T}(A+J)q
 =-(\rho-1)\|q\|^2+({\bf1}^{\mathsf T}q)^2
 \leq(42-\rho)\|q\|^2.
\]
Consequently
\[
 \boxed{18<\rho\leq42,\qquad17<t\leq41.}               \tag{11}
\]
Equality \(\rho=42\) is possible in these inequalities only when \(q\)
is constant and \(G{\bf1}=0\), i.e. the code centroid is zero.  Thus the
upper endpoint cannot be discarded by assuming asymmetry.

There is a further exact order-statistic constraint on the Perron vector.
Normalize \({\bf1}^{\mathsf T}q=1\), and put
\[
 v=Xq,\qquad t=\rho-1.
\]
The Perron equation and the PSD lift give
\[
 tq_i=1-2\langle x_i,v\rangle,\qquad
 1=t\|q\|^2+2\|v\|^2.                                 \tag{11a}
\]
If \(v=0\), then \(q_i=1/t\) for every \(i\), whence \(t=41\) and
\(\rho=42\).  If \(v\ne0\), the exact open-hemisphere depth seven applied
to the axis \(v/\|v\|\) shows that at least seven coordinates satisfy
\[
 q_i<\frac1t
\]
and at least seven satisfy \(q_i>1/t\).

Every normalized positive circuit \(\alpha\) obeys an additional
compatibility with the same threshold.  Taking the scalar product of
\(Aq=-tq\) with \(A\alpha=-{\bf1}\) gives
\[
 \boxed{q^{\mathsf T}\alpha=\frac1t.}                  \tag{11b}
\]
Thus both disjoint circuits guaranteed by origin depth have exactly the
same Perron-weighted average.  Equations (11a)--(11b) are universal and
boundary-safe, but by themselves do not force the two circuit supports to
meet both strict order-statistic classes.

The interval (11) is a genuine rank-and-sign constraint, but it is not a
contradiction.

## 3. Exact six-vertex star complement

Every real symmetric rank-six matrix has a nonsingular principal
six-by-six submatrix.  Choose an index set \(S\) for such a submatrix
\(C=A[S]\), and put \(T=[41]\setminus S\).  Interlacing and (3) imply
\[
 \operatorname{inertia}C=(5,1,0).                     \tag{12}
\]
Since \(\operatorname{rank}A=\operatorname{rank}C\), its Schur complement
vanishes:
\[
 A[T]=A[T,S]C^{-1}A[S,T].                              \tag{13}
\]

For \(i\in T\), define the nonnegative anchor-weight vector
\[
 b_i=(W_{is})_{s\in S}\in[0,3]^6.                     \tag{14}
\]
The upper endpoint 3 follows from
\(-1\leq G_{is}\leq1/2\).  Equations (13)--(14) become
\[
 \boxed{
 b_i^{\mathsf T}C^{-1}b_i=1,\qquad
 b_i^{\mathsf T}C^{-1}b_j=-W_{ij}\leq0\quad(i\ne j).
 }                                                     \tag{15}
\]
Thus every hypothetical code gives 35 nonnegative points on one
signature-\((5,1)\) quadric, with pairwise nonpositive Lorentz products,
all reconstructed from a six-vertex core.  Conversely, (13) reconstructs
the full rank-six matrix from such data.

This is a finite-core structural theorem, not a finite enumeration: the
core \(C\) and the 35 vectors \(b_i\) vary continuously.  Omitting their
common PSD lift would lose essential information, as Section 5 shows.

## 4. A positive circuit exactly recovers the PSD lift

The origin-depth theorem supplies a positive circuit.  Let
\(\alpha\geq0\), \({\bf1}^{\mathsf T}\alpha=1\), and \(G\alpha=0\).
Then (1) gives the unusually rigid identity
\[
 A\alpha=-{\bf1}.                                     \tag{16}
\]

In fact, for a matrix already satisfying the Lorentzian inertia, (16) is
not a mild extra constraint: it recovers the entire omitted PSD condition.

**Lift-equivalence lemma.**  Let \(A\) be symmetric with inertia
\((5,1,n-6)\).  If a vector \(\alpha\) satisfies
\[
 {\bf1}^{\mathsf T}\alpha=1,\qquad A\alpha=-{\bf1},    \tag{17}
\]
then
\[
 A+J\succeq0,\qquad \operatorname{rank}(A+J)=5.        \tag{18}
\]

**Proof.**  Equation (17) gives
\(\alpha^{\mathsf T}A\alpha=-1\), so \(\alpha\) is a negative vector.
For every \(x\in{\bf1}^{\perp}\),
\[
 x^{\mathsf T}A\alpha=-x^{\mathsf T}{\bf1}=0.
\]
The \(A\)-orthogonal complement of a negative vector is nonnegative
because \(A\) has only one negative eigenvalue.  Hence
\(x^{\mathsf T}Ax\geq0\) on \({\bf1}^{\perp}\).

For arbitrary \(y\), put
\(x=y-({\bf1}^{\mathsf T}y)\alpha\), so
\({\bf1}^{\mathsf T}x=0\).  Also
\((A+J)\alpha=0\).  Therefore
\[
 y^{\mathsf T}(A+J)y=x^{\mathsf T}Ax\geq0.
\]
The five positive directions of \(A\) remain, its unique negative
direction is killed, and (17) supplies one additional kernel direction.
More explicitly, if \(z\in\ker A\), then
\({\bf1}^{\mathsf T}z=-z^{\mathsf T}A\alpha=0\), so
\(\ker A\subseteq\ker(A+J)\); also
\(\alpha\in\ker(A+J)\setminus\ker A\).  Hence
\(\operatorname{rank}(A+J)\leq5\).  On the other hand, subtracting the
rank-one PSD matrix \(J\) from \(A+J\succeq0\) cannot create five positive
eigenvalues unless \(\operatorname{rank}(A+J)\geq5\).  Thus the rank is
exactly five. \(\square\)

The same argument gives a useful one-parameter version.  If instead
\[
 {\bf1}^{\mathsf T}\alpha=1,\qquad
 A\alpha=-c{\bf1}\quad(c>0),                           \tag{18a}
\]
then
\[
 A+cJ\succeq0,\qquad\operatorname{rank}(A+cJ)=5.       \tag{18b}
\]
Moreover \(c\) is the unique critical rank-one shift:
\[
\begin{array}{c|c}
\lambda<c&A+\lambda J\text{ has a negative direction},\\
\lambda=c&A+\lambda J\succeq0\text{ has rank }5,\\
\lambda>c&A+\lambda J\succeq0\text{ has rank }6.
\end{array}                                             \tag{18c}
\]
Indeed,
\(\alpha^{\mathsf T}(A+\lambda J)\alpha=\lambda-c\)
handles \(\lambda<c\); for \(\lambda>c\), add the PSD matrix
\((\lambda-c)J\) to (18b).  This removes the circuit kernel direction
because \({\bf1}^{\mathsf T}\alpha=1\), while the
\((n-6)\)-dimensional kernel of \(A\), which lies in
\({\bf1}^{\perp}\), remains.

This lemma precisely identifies the bottleneck: retaining both the exact
Lorentzian inertia and even one correctly normalized circuit identity is
equivalent to retaining \(G=(A+J)/2\succeq0\) of rank five.  A
counterexample satisfying all of them would itself be a 41-point kissing
code.

There are nevertheless useful graph consequences of (16).  Put
\(w_{ij}=W_{ij}=1-2G_{ij}\in[0,3]\), and let \(S\) be the positive support
of \(\alpha\).  Componentwise,
\[
 \sum_{j\in S}\alpha_jw_{ij}
 =\begin{cases}
 1+\alpha_i,&i\in S,\\
 1,&i\notin S.
 \end{cases}                                           \tag{19}
\]
It follows exactly that:

1. every circuit weight satisfies \(\alpha_i\leq1/2\);
2. an outside point can contact circuit vertices of total
   \(\alpha\)-weight at most \(2/3\);
3. if an outside point has no negative inner product with a circuit
   vertex, then all its inner products with the circuit are zero; and
4. every circuit vertex has a negative-inner-product neighbor inside the
   circuit.

For (3), absence of a negative inner product means \(w_{ij}\leq1\);
the second line of (19) is then equality in a weighted average, forcing
\(w_{ij}=1\) for every \(j\in S\).  If the circuit has size \(m\), the
points orthogonal to all of it lie in dimension \(6-m\).  Using the exact
low-dimensional kissing numbers gives the coverage table
\[
\begin{array}{c|ccccc}
m&2&3&4&5&6\\ \hline
\text{outside points forced to have a negative edge into }S
&15&26&31&34&35.
\end{array}                                             \tag{20}
\]
These are universal circuit-to-graph constraints.  The known \(D_5\)
examples show that circuit sizes alone do not close the problem.

## 5. Exact rational countermodel to weakened surrogates

The certificate
[`lorentzian_rank6_interval_countermodel.json`](../certificates/lorentzian_rank6_interval_countermodel.json)
stores 41 rational points \(y_i\in S^4\) by stereographic coordinates.
Let \(K=(\langle y_i,y_j\rangle)\).  The standard-library verifier proves
exactly that
\[
 -\frac9{10}<K_{ij}<\frac{21}{40}\quad(i\ne j),\qquad
 \operatorname{rank}K=5,                              \tag{21}
\]
and that \({\bf1}\notin\operatorname{range}K\).  Its exact maximum inner
product is also strictly greater than \(1/2\), so these directions are not
a kissing code.

Set
\[
 \widetilde A=\frac{40K-21J}{19},\qquad
 \widetilde H=\frac{\widetilde A+J}{2}
              =\frac{20K-J}{19}.                      \tag{22}
\]
Then exact rational arithmetic gives
\[
\begin{aligned}
&\widetilde A_{ii}=1,\quad -3<\widetilde A_{ij}<0,\\
&\operatorname{rank}\widetilde A=6,\quad
  \operatorname{inertia}\widetilde A=(5,1,35),\\
&\widetilde H_{ii}=1,\quad -1<\widetilde H_{ij}<1/2,\\
&\operatorname{rank}\widetilde H=6,\quad
  \operatorname{inertia}\widetilde H=(5,1,35).
\end{aligned}                                          \tag{23}
\]
The pseudo-contact graph is empty, while the graph
\(\widetilde H_{ij}<0\) has minimum degree 21.  Hence all the recorded
contact-degree, common-contact-neighbor, clique, and minimum-negative-degree
conditions hold, usually with large slack.

The rational directions \(y_i\) themselves have open origin-hemisphere
depth 14.  They contain the following two disjoint positive circuits:
\[
 \{4,8,11,19,29,31\},\qquad
 \{3,13,25,26,28,36\},                                \tag{24}
\]
with zero-based indices.  Every sign and every one of the
\(\binom{41}{4}\) boundary hyperplanes is checked exactly.

What fails is explicit:
\[
 \widetilde H\not\succeq0.
\]
If \(\alpha\) is either positive \(K\)-circuit in (24), then
\[
 \alpha^{\mathsf T}\widetilde H\alpha
 =-\frac{({\bf1}^{\mathsf T}\alpha)^2}{19}<0.          \tag{25}
\]
Moreover \(\widetilde H\) has rank six, not five.  After normalizing a
circuit by \({\bf1}^{\mathsf T}\alpha=1\), its identity also has the wrong
scale:
\[
 \widetilde A\alpha=-\frac{21}{19}{\bf1},
\]
instead of the exact \(-{\bf1}\) in (16).  The lift-equivalence lemma
and the critical-shift formula (18a)--(18c) show that its exact PSD
threshold is \(21/19>1\).  Thus changing \(21/19\) to \(1\) cannot be a
harmless normalization.

The verifier also checks that the all-ones Rayleigh quotient of
\(\widetilde W=I-\widetilde A\) is strictly greater than 46.  Thus this
object fails the PSD-derived upper endpoint in (11), as it must.  It is a
countermodel to the listed *separate* rank, sign, interval, graph, depth,
and circuit-existence surrogates, not to consequences that already retain
the correctly normalized lift.

Thus (21)--(25) are a rigorous counterexample to any argument using only
separate Lorentzian rank/inertia, scalar entry bounds, graph degrees,
origin depth, and the existence of positive circuits.  The common matrix
identity (16), or an equivalent PSD/rank-five condition on
\((A+J)/2\), must enter essentially.

## 6. Reproduction and dependency map

From the project root:

```sh
python3 verifiers/verify_lorentzian_inertia_graph.py
python3 -m unittest tests.test_lorentzian_inertia_graph -v
```

The verifier uses only the Python standard library, integer determinants,
and `fractions.Fraction`.  The depth enumeration covers the full continuous
hemisphere problem because it verifies central general position exactly
and checks every four-point boundary hyperplane.

```text
exact B(5) <= 34 + contact degree <= 15
                    |
                    v
 rank/inertia (5,1,35), irreducible W, spectrum (4)
                    |
       trace W = 0 + trace W^3 > 0
                    |
                    v
             exact Perron interval (11)

rank(A)=6 --> nonsingular principal core --> star complement (15)

positive circuit --> A alpha = -1 --> lift-equivalence lemma
                                      |
                                      v
                              exact PSD rank-five lift

rational certificate --> weakened-surrogate countermodel (21)--(25)
```

The theorem-strength unresolved gap remains the original one: exclude the
continuous star-complement systems (15) while preserving the exact
lift-equivalent compatibility, rather than only its separate spectral and
graph shadows.
