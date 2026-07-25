# Sparse Deep-Pair Graphs and a Rank-Twenty Barrier

This note strengthens the exact negative-tail graph result in two ways.  It
classifies the cases of 23 and 24 deep pairs, and it records exact angular
and polynomial-weight restrictions on those cases.  It also gives an exact
countermodel showing that these restrictions, even when supplemented by the
degree-four projective kernel and all of its subset inequalities, do not by
themselves force a twenty-fourth deep pair.

Throughout, \(X=\{x_1,\ldots,x_{41}\}\subset S^4\) is a hypothetical kissing
code and

\[
 ij\in E(H)\quad\Longleftrightarrow\quad
 \langle x_i,x_j\rangle<-\frac12 .
\]

The earlier negative-tail argument proves that \(H\) is triangle-free,
\(\alpha(H)\leq20\), and \(e(H)\geq23\).

## 1. Exact classification at 23 and 24 edges

### Theorem 1

Let \(H\) be a triangle-free graph on 41 vertices with
\(\alpha(H)\leq20\).

1. If \(e(H)=23\), then
   \[
   H\cong C_5\sqcup18K_2.
   \]
2. If \(e(H)=24\), then \(H\) is isomorphic to exactly one of
   \[
   C_7\sqcup17K_2,\qquad
   (C_5\text{ with a pendant path of length }2)\sqcup17K_2,
   \qquad
   C_5\sqcup P_4\sqcup16K_2.
   \]

No geometric realizability is asserted.

### Proof

For a connected component \(A\), write

\[
 v_A=|V(A)|,\quad e_A=|E(A)|,\quad
 r_A=e_A-v_A+1,
\]

where \(r_A\) is its cyclomatic number, and define

\[
 q_A=\alpha(A)+e_A-v_A=\alpha(A)+r_A-1,\qquad
 s_A=2e_A-v_A.
\]

Both independence number and \(e-v\) are additive over components, so

\[
 \sum_A q_A=\alpha(H)+e(H)-41.                    \tag{1}
\]

Every \(q_A\) is nonnegative.  The components with \(q_A\leq3\) that can
matter here have the following elementary description.

| \(q_A\) | possible component type | upper bound for \(s_A\) |
|---:|---|---:|
| 0 | \(K_1\) or \(K_2\) | \(0\), with \(s(K_1)=-1\) |
| 1 | \(P_3\) or \(P_4\) | \(2\), attained only by \(P_4\) |
| 2 | a tree with \(\alpha=3\), or \(C_4,C_5\) | \(5\), attained only by \(C_5\) |
| 3 | a tree with \(\alpha=4\), or a triangle-free unicyclic graph with \(\alpha=3\) | \(7\) |

Here are the details behind the table.  If \(r_A=0\), then \(A\) is a tree
and \(q_A=\alpha(A)-1\).  Its two bipartition classes are independent, so
\(v_A\leq2\alpha(A)\) and \(s_A=v_A-2\leq2q_A\).  This also shows directly
that the \(q=1\) trees are \(P_3,P_4\).

If \(r_A=1\), then \(A\) is unicyclic and \(q_A=\alpha(A)\).  Every
unicyclic graph on \(v\) vertices has
\(\alpha\geq\lfloor v/2\rfloor\): remove a leaf together with its neighbor
and induct, with a cycle as the leafless base case.  Triangle-freeness rules
out 3-cycles.  Thus the \(q=2\) possibilities are \(C_4,C_5\); an attached
leaf would increase the independence number.  For \(q=3\), one has
\(v_A\leq7\) and \(s_A=v_A\).

If \(r_A=2\) and \(q_A\leq3\), the only new numerical possibility is
\(\alpha(A)=2,q_A=3\).  Ramsey's elementary \(R(3,3)=6\) argument gives
\(v_A\leq5\).  A bicyclic graph would have \(e_A=v_A+1\); Mantel's theorem
rules this out for \(v_A\leq4\), while for \(v_A=5\) equality would force
\(K_{2,3}\), whose independence number is 3.  Larger \(r_A\) would require
\(\alpha(A)=1\), impossible for a nontrivial triangle-free connected graph.
This proves the table.

There is a useful bookkeeping interpretation of \(s_A\).  After the
components with \(q_A>0\) have been fixed, every remaining non-isolated
\(q=0\) component is a \(K_2\).  Therefore their total vertex saving
relative to disjoint edges must satisfy

\[
 \sum_{q_A>0}s_A\geq 2e(H)-41,                    \tag{2}
\]

with equality precisely when there are no isolated vertices.

Suppose first that \(e(H)=23\).  Equation (1) says
\(\sum q_A=\alpha(H)-18\).  The cases \(\alpha=18\) and \(\alpha=19\)
have total \(q\) respectively 0 and 1, whose largest possible savings are
0 and 2.  Both contradict the required saving \(2e-41=5\).
Consequently \(\alpha=20\) and \(\sum q_A=2\).  Two \(q=1\) components save
at most 4.  A single \(q=2\) component saves 5 only when it is \(C_5\).
Equality in (2) then leaves exactly 18 copies of \(K_2\), proving part 1.

Now let \(e(H)=24\).  Equation (1) gives
\(\sum q_A=\alpha(H)-17\), and (2) requires saving at least 7.  Total
\(q=0,1,2\) can save at most \(0,2,5\), respectively, so
\(\alpha(H)=20\) and \(\sum q_A=3\).  The partition \(1+1+1\) saves at
most 6.  The partition \(2+1\) saves 7 only for \(C_5\sqcup P_4\), leaving
16 copies of \(K_2\).  A single \(q=3\) component saves 7 only if it is a
seven-vertex unicyclic graph with independence number 3, leaving 17 copies
of \(K_2\).

Such a unicyclic graph has an odd cycle: an even-cycle unicyclic graph is
bipartite on seven vertices and hence has an independent set of size 4.
The odd cycle is therefore \(C_7\), or it is \(C_5\) with two additional
vertices.  In the latter case the two vertices must form one pendant path
of length 2.  Two separate leaves, including two leaves at the same cycle
vertex, give an independent set of size 4.  Both listed graphs have
independence number 3.  This proves part 2. \(\square\)

## 2. Angular frustration and exact edge weights

For a deep edge \(ij\), define its antipodal deviation

\[
 \delta_{ij}=\arccos(-\langle x_i,x_j\rangle)
 \in[0,\pi/3).
\]

Let

\[
 h(t)=t^2\left(t^2-\frac14\right),\qquad
 W(\delta)=h(\cos\delta).
\]

Thus \(W(\delta)\) is the positive contribution of a deep edge to the
degree-four projective polynomial.

### Lemma 2 (incident edges)

If \(ij,ik\in E(H)\), then

\[
 \delta_{ij}+\delta_{ik}\geq\frac{\pi}{3}.          \tag{3}
\]

Indeed, both \(x_j,x_k\) lie respectively
\(\delta_{ij},\delta_{ik}\) away from \(-x_i\).  The spherical triangle
inequality bounds their mutual angular distance from above by the sum of
those deviations.  Since \(H\) is triangle-free, \(jk\notin E(H)\), and
the code inequalities give
\(-1/2\leq\langle x_j,x_k\rangle\leq1/2\).  Their angular distance is
therefore at least \(\pi/3\), proving (3).

### Lemma 3 (odd-cycle sign frustration)

For every odd deep cycle \(v_0v_1\cdots v_{2r}v_0\),

\[
 \sum_{i=0}^{2r}\delta_{v_i v_{i+1}}\geq\pi.        \tag{4}
\]

Put \(y_i=(-1)^i x_{v_i}\).  Consecutive \(y_i\)'s are separated by the
corresponding antipodal deviation.  Because the cycle length is odd, this
forms a path from \(x_{v_0}\) to \(-x_{v_0}\).  Its length is at least the
spherical distance \(\pi\), proving (4).

### Lemma 4 (an exact two-edge weight bound)

If \(0\leq u,v\leq\pi/3\) and \(u+v\geq\pi/3\), then

\[
 W(u)+W(v)\leq\frac{49}{64}.                         \tag{5}
\]

The function \(W\) is decreasing on this interval, so it suffices to set
\(v=\pi/3-u\).  If \(c=\cos(2u-\pi/3)\), direct trigonometric reduction gives

\[
 W(u)+W(\pi/3-u)
 =\frac58+\frac38c-\frac14c^2
 =\frac{49}{64}-\frac{(4c-3)^2}{64}.
\]

This proves (5), including both endpoints exactly.

### Lemma 5 (residual-PSD row-energy envelope)

Let \(x\) have \(m\) deep neighbors \(y_1,\ldots,y_m\), and put

\[
 p_i=-\langle x,y_i\rangle,\qquad
 v_i=y_i+p_i x\in x^\perp,\qquad z_i=p_i^2.
\]

Then

\[
 \sum_{i=1}^m z_i\leq\frac{m+1}{2}.                  \tag{6}
\]

Moreover, if
\[
 R_m=\sup\sum_{i=1}^m h(p_i)
\]
is taken over every row satisfying the residual PSD and pair constraints,
then the following exact certified envelope holds:

\[
 R_1\leq\frac34,\qquad R_2\leq\frac{49}{64},          \tag{7}
\]

and, for \(m\geq3\),

\[
 R_m\leq
 \begin{cases}
 (3m+9)/16,&m\ \text{odd},\\[2mm]
 (3m+8)/16,&m\ \text{even}.
 \end{cases}                                         \tag{8}
\]

This is an upper envelope, not a claim that equality is geometrically
attained.

To prove (6), use both the PSD residual Gram matrix and the upper pair
constraint:

\[
\begin{aligned}
0
&\leq\left\|\sum_i p_i v_i\right\|^2\\
&=\sum_i p_i^2(1-p_i^2)
  +2\sum_{i<j}p_ip_j
       \bigl(\langle y_i,y_j\rangle-p_ip_j\bigr)\\
&\leq\frac{Q+S^2}{2}-Q^2,
\end{aligned}
\]

where \(Q=\sum_i p_i^2\) and \(S=\sum_i p_i\).  Since
\(S^2\leq mQ\), this gives \(Q\leq(m+1)/2\).

Lemma 2 also shows that at most one \(z_i\) can exceed \(3/4\): two such
values would give two deviations strictly below \(\pi/6\).  We may therefore
relax to

\[
\frac14\leq z_1\leq1,\qquad
\frac14\leq z_i\leq\frac34\ (i\geq2),\qquad
\sum_i z_i\leq\frac{m+1}{2}.                          \tag{9}
\]

The objective is
\[
\sum_i\phi(z_i),\qquad \phi(z)=z^2-\frac14z,
\]
which is increasing and convex on \([1/4,1]\).  Its maximum over (9) is
therefore obtained by filling the exceptional coordinate to \(1\), then
filling ordinary coordinates to \(3/4\), with at most one intermediate
coordinate.  If \(m\) is odd, the extremal relaxed list is

\[
1,\quad
\underbrace{\frac34,\ldots,\frac34}_{(m-1)/2},\quad
\underbrace{\frac14,\ldots,\frac14}_{(m-1)/2}.
\]

If \(m\) is even, it is

\[
1,\quad
\underbrace{\frac34,\ldots,\frac34}_{(m-2)/2},\quad
\frac12,\quad
\underbrace{\frac14,\ldots,\frac14}_{(m-2)/2}.
\]

Evaluating \(\phi\) gives (8).  For \(m=2\), Lemma 4 improves the relaxed
value \(7/8\) to \(49/64\).

For example, (3)--(5) imply

\[
\sum_{e\in E(P_4)}W(\delta_e)\leq\frac{49}{32},
\qquad
\sum_{e\in E(C_\ell)}W(\delta_e)\leq
\frac{49\ell}{128}.                                \tag{10}
\]

For a deep \(C_5\), (4) allows a modest strengthening.  Leave an edge of
largest deviation unpaired and partition the other four cycle edges into
two incident pairs.  The left-over deviation is at least \(\pi/5\), hence

\[
\sum_{e\in E(C_5)}W(\delta_e)
\leq \frac{49}{32}+W(\pi/5)
=\frac{53+2\sqrt5}{32}.                             \tag{11}
\]

If \(e(H)=23\), Theorem 1 and the trivial single-edge bound \(W\leq3/4\)
therefore give

\[
\sum_{e\in E(H)}h(-\langle x_i,x_j\rangle)
\leq \frac{485+2\sqrt5}{32}.                        \tag{12}
\]

The Gegenbauer expansion

\[
 h(t)=\frac1{28}P_0(t)+\frac13P_2(t)+\frac8{21}P_4(t)
\]

gives, on 41 points,

\[
 \sum_{i<j}h(\langle x_i,x_j\rangle)\geq\frac{205}{14}.
\]

Writing

\[
 D=-\sum_{ij\notin E(H),\,i<j}h(\langle x_i,x_j\rangle)\geq0,
\]

equation (12) yields the exact stability restriction

\[
D\leq\frac{115+14\sqrt5}{224}.                       \tag{13}
\]

This is universal in the 23-edge case, but it is not a contradiction.

## 3. An exact countermodel to the scalar/projective-kernel route

The remaining gap in (13) is genuine for the present mechanism.  Consider
the following exact 41-point code in dimension 20:

- 18 mutually orthogonal antipodal pairs;
- in an orthogonal two-plane, a regular pentagon.

Its Gram matrix \(\widehat G\) is positive semidefinite of rank 20.  All
off-diagonal entries are at most \(1/2\).  Its deep graph is exactly
\(C_5\sqcup18K_2\).  For the pentagon, consecutive deep-graph vertices have
inner product

\[
 -\cos(\pi/5)=-\frac{1+\sqrt5}{4},
\]

and pentagon chords have inner product

\[
 \cos(2\pi/5)=\frac{\sqrt5-1}{4}.
\]

All cross-component inner products are zero.  Consequently the entrywise
matrix

\[
 F=h[\widehat G]
\]

has 18 matching blocks \((3/4)J_2\), and its pentagon block has diagonal
\(3/4\), cycle entries

\[
 w=\frac{2+\sqrt5}{16},
\]

and chord entries

\[
 q=\frac{2-\sqrt5}{16}.
\]

All other entries are zero.  The positive-entry graph of \(F\) is therefore
exactly \(C_5\sqcup18K_2\).

This matrix passes more than the all-ones projective inequality:

\[
 F-\frac1{28}J_{41}\succeq0.                          \tag{14}
\]

Here is an exact proof.  The pentagon block has eigenvalues

\[
 \frac54,\quad \frac{15}{16},\frac{15}{16},
 \quad\frac5{16},\frac5{16},
\]

while a matching block has eigenvalues \(3/2,0\).  On the nonconstant
subspaces, (14) follows immediately.  If \(s_1,\ldots,s_{18},s_P\) are the
coordinate sums on the matching blocks and pentagon block, respectively,
the constant-block contribution satisfies

\[
 z^\mathsf TFz\geq
 \frac34\sum_{i=1}^{18}s_i^2+\frac14s_P^2
 \geq\frac1{28}\left(\sum_{i=1}^{18}s_i+s_P\right)^2,
\]

where the last step is weighted Cauchy--Schwarz and

\[
 18\left(\frac43\right)+4=28.
\]

Thus (14) is exact.

In particular, for every subset \(S\) of \(m\) vertices,

\[
 \sum_{\{i,j\}\subset S}F_{ij}
+\frac34m
=\frac12\left(\mathbf1_S^\mathsf TF\mathbf1_S
               +\frac34m\right)
\geq\frac{m^2}{56}+\frac38m,
\]

or, in the usual off-diagonal form,

\[
 \sum_{\{i,j\}\subset S}F_{ij}\geq\frac{m(m-21)}{56}. \tag{15}
\]

For clarity, the simpler direct derivation of (15) is
\(\mathbf1_S^\mathsf TF\mathbf1_S\geq m^2/28\), followed by subtracting
the diagonal \(3m/4\) and dividing by two.  The full 41-point subset has

\[
\sum_{i<j}F_{ij}=\frac{59}{4}
=\frac{205}{14}+\frac3{28}.                           \tag{16}
\]

Thus it clears the required threshold by an exact positive margin.

The countermodel is not a five-dimensional code: its Gram rank is exactly
20.  It proves that the following information does not suffice to improve
\(e(H)\geq23\) to \(e(H)\geq24\):

- triangle-freeness and \(\alpha(H)\leq20\);
- all incident-edge angular inequalities (3), including the residual-PSD
  row envelope (6)--(8);
- odd-cycle frustration (4);
- the exact \(h\)-weights within every nontrivial component;
- the full aggregate kernel condition \(h[G]-J/28\succeq0\);
- every subset inequality (15).

Any successful continuation of this sparse-deep-graph route must use the
rank-five Gram geometry, separate degree-two and degree-four harmonic
constraints, or a cross-component compatibility inequality not implied by
the aggregate kernel.

## 4. What rank five adds

There is a useful exact way to expose the missing rank information.  For a
deep matching component \(\{a_i,b_i\}\), write

\[
 \langle a_i,b_i\rangle=-p_i,\qquad
 u_i=\frac{a_i-b_i}{\sqrt{2(1+p_i)}}\in S^4.
\]

If \(z\) lies in a different component of \(H\), then both
\(\langle a_i,z\rangle\) and \(\langle b_i,z\rangle\) belong to
\([-1/2,1/2]\).  Hence

\[
 |\langle u_i,z\rangle|
 \leq\frac1{\sqrt{2(1+p_i)}}.                         \tag{17}
\]

For two distinct matching components, the four cross inner products are all
in the same interval, and the Walsh difference gives

\[
 |\langle u_i,u_j\rangle|
 \leq\frac1{\sqrt{(1+p_i)(1+p_j)}}.                   \tag{18}
\]

These inequalities become the sharp projective-code bound \(1/2\) when the
matching edges are exactly antipodal.

In the 23-edge case, (12)--(13) also force an exact total antipodal-stability
estimate.  Since

\[
 \frac34-h(p)=(1-p^2)\left(\frac74-(1-p^2)\right)
 \geq1-p^2
\]

for \(p\in[1/2,1]\), one has

\[
 \sum_{i=1}^{18}(1-p_i^2)
 \leq\frac{115+14\sqrt5}{224},                        \tag{19}
\]

and therefore

\[
 \sum_{i=1}^{18}\|a_i+b_i\|^2
 =2\sum_i(1-p_i)
 \leq\frac{115+14\sqrt5}{112}.                        \tag{20}
\]

Thus every 23-edge counterexample would be quantitatively close, in total
matching midpoint energy, to 18 antipodal lines.  Equations (17)--(18) make
the corresponding approximate projective extension problem explicit.

At the exact antipodal boundary, this becomes particularly clean.  Collapse
the \(r\) matching components to \(r\) unoriented lines.  In each sparse graph
from Theorem 1, every maximum independent subset of the remaining core can
be appended to those lines, producing a 20-line projective code:

| deep graph | collapsed matching lines | core | core independence number |
|---|---:|---|---:|
| \(C_5\sqcup18K_2\) | 18 | \(C_5\) | 2 |
| \(C_7\sqcup17K_2\) | 17 | \(C_7\) | 3 |
| \(C_5\)-tail\(\sqcup17K_2\) | 17 | seven-vertex core | 3 |
| \(C_5\sqcup P_4\sqcup16K_2\) | 16 | \(C_5\sqcup P_4\) | 4 |

The first row, for example, asks whether the extension compatibility graph
of an 18-line projective code can contain an induced \(C_5\).  Every edge of
that compatibility \(C_5\) completes the same 18 base lines to an extremal
20-line code.  This overlapping-extremizer formulation uses rank five, but
the known projective bound of 20 alone does not exclude it: a \(C_5\) has
clique number two.

The line Gram matrix in this reduction has rank at most five.  In particular,
for \(r\) collapsed matching directions the elementary frame inequality
gives

\[
 \sum_{i<j}\langle u_i,u_j\rangle^2
 \geq\frac{r(r-5)}{10}.                               \tag{21}
\]

For \(r=18,17,16\), the right sides are respectively
\(117/5,102/5,88/5\).  These inequalities and all vanishing \(6\times6\)
line-Gram minors are absent from the rank-20 countermodel.  They are the
natural next cross-component constraints; (21) by itself is not yet a
contradiction.

There is nevertheless an exact equality obstruction that is invisible in
the rank-20 model.

### Lemma 6 (root-system zero-slack obstruction)

Let \(r\in\{16,17,18\}\).  Suppose \(u_1,\ldots,u_r\in S^4\) satisfy
\(|\langle u_i,u_j\rangle|\leq1/2\), and let
\[
 z_1,\ldots,z_{41-2r}\in S^4
\]
be core code points satisfying
\[
\langle z_a,z_b\rangle\leq1/2\qquad(a\ne b)
\]
and
\(|\langle u_i,z_a\rangle|\leq1/2\).  Put

\[
 A=\sum_{i<j}h(\langle u_i,u_j\rangle),\qquad
 B=\sum_{i,a}h(\langle u_i,z_a\rangle).
\]

Then

\[
 A+B<0.                                               \tag{22}
\]

Both sums are nonpositive.  If equality held, every inner product occurring
in them would belong to \(\{0,\pm1/2\}\).  Scale the \(u_i\)'s by \(\sqrt2\)
and let \(L\) be their integral span.  The vectors of norm squared 2 in
\(L\) form a finite crystallographic simply-laced root system: integrality
is clear, and reflection in a norm-two vector preserves \(L\).

This root system contains at least \(2r\geq32\) roots.  The simply-laced
root-system classification in rank at most five gives the following largest
irreducible counts:

\[
 |A_5|=30,\qquad |D_5|=40,
\]

while every rank-at-most-four or reducible rank-five system has at most 30
roots.  Consequently the system generated by the \(u_i\)'s has rank five
and type \(D_5\).

Now adjoin \(\sqrt2z_a\) to \(L\), one point at a time.  All of its inner
products with the generating roots are integral and its norm squared is 2.
The enlarged norm-two root system still has rank five and already contains
the 40 \(D_5\) roots.  The same classification forces it to have type
\(D_5\) with exactly those same 40 roots.  Thus each \(z_a\) lies on one of
the 20 \(D_5\) root lines.

It cannot lie on one of the \(r\) base lines, because then a cross inner
product would have absolute value 1.  Only \(20-r\) lines remain, supporting
at most \(2(20-r)=40-2r\) distinct oriented unit points.  But the core
contains \(41-2r\) points, one too many.  This contradiction proves (22).

Because these closed code and cross constraints make the constraint set in
Lemma 6 compact, the proof actually gives
the existence of a dimension-dependent constant \(\varepsilon_r>0\) such
that

\[
 A+B\leq-\varepsilon_r.                               \tag{23}
\]

The present argument does not give an explicit value.  In the exact
antipodal 23-edge case, pair-pair terms occur four times and pair-core terms
twice in the original 41-point \(h\)-sum, so (22) proves an unavoidable
strict cross-component loss \(4A+2B<0\).  To finish the sparse-graph route
one would need a certified lower bound for this loss large enough to exceed
the remaining margin in (13), together with a robust version for the
near-antipodal deviations controlled by (19).  That quantitative
root-stability statement is the exact unresolved gap.

For the 23-edge case one can strengthen the zero-slack statement: once the
18 base lines are \(D_5\) roots, there are no non-root extensions at all.

### Lemma 7 (\(D_5\) minus two lines is saturated)

Delete any two lines from the 20 \(D_5\) root lines.  If a unit vector
\(z\in S^4\) has absolute inner product at most \(1/2\) with all 18
remaining lines, then the line of \(z\) is one of the two deleted lines.

To prove this without enumeration, scale \(z\) to \(y=\sqrt2z\).  A retained
root line represented by \((e_i\pm e_j)/\sqrt2\) imposes

\[
 |y_i\pm y_j|\leq1.
\]

When both signs on a support are retained, this is
\(|y_i|+|y_j|\leq1\).  Up to signed coordinate permutations, two deleted
lines have one of three forms:

\[
\begin{array}{ll}
\text{same support:}&e_1+e_2,\ e_1-e_2,\\
\text{disjoint supports:}&e_1+e_2,\ e_3+e_4,\\
\text{intersecting supports:}&e_1+e_2,\ e_1+e_3.
\end{array}                                           \tag{24}
\]

Let \(a=\max_i|y_i|\).  If \(a\leq1/2\), then
\(\|y\|^2\leq5/4<2\).  Suppose \(a\geq1/2\).  The retained inequalities
also give \(a\leq1\).  In the first two cases of (24), if a largest
coordinate belongs to a deleted support, at most one
other coordinate is unconstrained from it.  Hence

\[
 \|y\|^2\leq2a^2+3(1-a)^2\leq2.                       \tag{25}
\]

If the largest coordinate belongs to no deleted support, the stronger bound
\[
 \|y\|^2\leq a^2+4(1-a)^2<2                           \tag{26}
\]
holds.  Both right sides are convex in \(a\in[1/2,1]\), so their maxima are
checked at the endpoints.  Equality in (25) requires \(a=1\), the one
unconstrained mate also to have absolute value 1, and every other coordinate
to vanish.  The retained opposite-sign inequality forces the two signs to
be the deleted-line signs.

In the intersecting-support case, if the common coordinate \(y_1\) is
largest, the other two exceptional coordinates satisfy
\(|y_2|+|y_3|\leq1\).  Their squared contribution is at most
\(a^2+(1-a)^2\), and the remaining two coordinates are at most \(1-a\).
This again gives (25).  If \(y_2\) or \(y_3\) is largest, it has only one
unconstrained mate and (25) applies directly; if \(y_4\) or \(y_5\) is
largest, (26) applies.  The equality analysis is the same.  Since a unit
\(z\) has \(\|y\|^2=2\), equality forces exactly one of the four orientations
of the two deleted lines.  This proves the lemma.

Consequently, in the exact-antipodal 23-edge reduction, the 18-line base
energy \(A\) cannot vanish.  If it did, Lemma 6 would identify the base with
\(D_5\) minus two lines, and Lemma 7 would leave only four oriented extension
points for a five-point core.  Thus any induced \(C_5\) in the extension
compatibility graph forces \(A<0\), not merely \(A+B<0\).  Compactness again
gives a strict but presently unquantified gap.

The obstruction scale in Lemma 7 has a useful exact test configuration.
It is not a code extension, but it is a sharp-looking target for any
quantitative stability argument.

### Lemma 8 (an exact hypercube \(C_5\) probe)

Let
\[
\begin{split}
s_0&=(1,1,1,1,1),\\
s_1&=(1,-1,-1,-1,-1),\\
s_2&=(-1,1,1,1,-1),\\
s_3&=(1,1,-1,-1,1),\\
s_4&=(-1,-1,1,-1,-1),
\end{split}
\]
and put \(z_i=s_i/\sqrt5\).  In cyclic order their Gram matrix has

\[
 \langle z_i,z_{i+1}\rangle=-\frac35,\qquad
 \langle z_i,z_{i+2}\rangle=\frac15.                 \tag{27}
\]

Thus the deep graph is exactly \(C_5\).  Moreover, for every \(D_5\) root
line \(u=(e_j\pm e_k)/\sqrt2\),

\[
 |\langle u,z_i\rangle|\in
 \left\{0,\sqrt{\frac25}\right\}.                    \tag{28}
\]

Indeed, the unnormalized numerator in (28) is \(0\) or \(\pm2\), while
the product of the two normalizing factors is \(\sqrt{10}\).  Hence the
same five-point core lies within common cross slack

\[
 \sigma=\sqrt{\frac25}-\frac12                       \tag{29}
\]

of all twenty \(D_5\) root lines, and therefore of every eighteen-line
deletion.  Its exact internal \(h\)-energy is

\[
 5h\left(-\frac35\right)+5h\left(\frac15\right)
 =\frac{39}{250}.                                    \tag{30}
\]

Lemma 8 is only an upper construction for the relaxed cross-slack problem;
no matching lower bound for (29) is claimed.  It does show that a
quantitative form of Lemma 7 based only on a common cross tolerance cannot
force a gap larger than \(\sqrt{2/5}-1/2\).  The standard-library verifier
checks (27)--(30) using integer dot products and rational squares.

There is also an exact continuum showing that the numerically conjectured
five-point core bound \(3/2\) would be sharp.  This does **not** prove that
bound in arbitrary rank.

### Lemma 9 (a planar \(3/2\)-energy family)

Put \(L=\pi/3\), choose \(a\in[0,L]\), and set \(b=L-a\).  In an oriented
Euclidean plane, let the five unit vectors \(w_i\) have arguments

\[
 0,\quad a,\quad L,\quad L+a,\quad 2L+a,
\]

and put \(z_i=(-1)^i w_i\).  Then the consecutive inner products of the
\(z_i\)'s are

\[
 -\cos a,\quad-\cos b,\quad-\cos a,\quad-\frac12,
 \quad-\cos b,
\]

while their five chord inner products are

\[
 \frac12,\quad\frac12,\quad\cos(L+a),\quad
 \cos(2L-a),\quad\frac12.
\]

Thus the consecutive pairs are deep (in the closed-cell sense), every
chord belongs to \([-1/2,1/2]\), and

\[
 \sum_{0\leq i<j\leq4}h(\langle z_i,z_j\rangle)=\frac32.          \tag{31}
\]

Indeed, write \(H(\theta)=h(\cos\theta)\).  Since
\[
 H(\theta)=\frac{2+3\cos(2\theta)+\cos(4\theta)}8,
\]
the identities
\[
\begin{aligned}
 &\cos(2a)+\cos(2L-2a)+\cos(2L+2a)=0,\\
 &\cos(4a)+\cos(4L-4a)+\cos(4L+4a)=0
\end{aligned}
\]
follow from \(\cos(2L)=\cos(4L)=-1/2\).  Consequently
\[
 H(a)+H(L-a)+H(L+a)=\frac34.
\]
Also \(H(2L-a)=H(L+a)\), because the two arguments sum to
\(\pi\).  Substitution of the displayed edge and chord lists now gives
\[
 2H(a)+2H(b)+H(L+a)+H(2L-a)=\frac32.
\]

Direct constrained Gram optimization repeatedly returns this rank-two
family as a global maximizer of the five-point \(C_5\) core energy.  That
global upper bound remains `NUMERICAL EVIDENCE ONLY`: local \(3\times3\)
PSD conditions together with odd-cycle angular frustration still permit
the larger relaxation value \(49/32\), so a proof must use a genuinely
five-point Gram relation.

An independent dependency-free numerical search imposed the isolated
matching components as exact antipodal pairs and optimized all remaining
rank-five graph-cell inequalities for all four rows of the table.  None of
64 deterministic starts per graph reached feasibility.  The best maximum
violations were between \(0.0429\) and \(0.0466\).  This is numerical
evidence only; the exact commands and hashes are recorded in
`experiments/sparse_deep_rank5_results.md`.

## Reproduction

The standard-library verifier checks the graph bookkeeping, all quadratic
field identities, the exact spectra in (14), the rank-20 Gram model, and
all subset inequalities:

```sh
python3 verifiers/verify_sparse_deep_graph_stability.py
python3 -m unittest tests.test_sparse_deep_graph_stability -v
```

The numerical rank-five search is separate discovery code:

```sh
SEEDS=64 STEPS=100 node experiments/sparse_deep_rank5_search.js
```
