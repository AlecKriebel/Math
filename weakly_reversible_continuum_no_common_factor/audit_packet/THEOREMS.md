# Version 2 theorem statements for specialist audit

Rates below use the directed order

\[
(01,10,04,40,06,60,17,71,24,42,27,72,29,92,34,43,59,95,89,98),
\]

where indices refer to the complexes

\[
(0,Z,3Z,Y+Z,3Y,X+Z,X+Y,X+Y+Z,2X+Y,3X).
\]

## Theorem A: explicit clean integer construction

Assign the rates

\[
\begin{aligned}
k={}&(1160,10296,976,23,560,5977,1800,25,1629,1237,\\
&1,9152,653,1214,5368,1,5368,70,6039,915)
\end{aligned}
\]

to the reversible edges

\[
01,04,06,17,24,27,29,34,59,89.
\]

Then the network is reversible and has one linkage class,
\(S=\mathbb R^3\), and positive integer rates. Its mass-action field is

\[
\begin{aligned}
F_1={}&-4697x^3+6039x^2y-9177xyz-5977xy+10736xz
       +1960z^3+1800z+560,\\
F_2={}&915x^3-6039x^2y-9177xyz-5977xy-3782y^3
       +10736yz+4888z^3+1800z+3488,\\
F_3={}&3712x^3+18304xyz-5368xz+3712y^3-5368yz
       -6848z^3-10296z+1160.
\end{aligned}
\]

The unique positive compatibility class \(\mathbb R_{>0}^3\) contains the
compact positive ellipse

\[
L=z-x-y+1=0,qquad
Q=7x^2-2xy-16x+7y^2-16y+16=0.
\]

In particular,

\[
(x,y,z)=\left(
\frac{t^2+3}{2(t^2-t+1)},
\frac{3t^2+1}{2(t^2-t+1)},
\frac{t^2+t+1}{t^2-t+1}
\right),\qquad -1<t<1,
\]

gives infinitely many distinct positive equilibria. Nevertheless,

\[
\gcd(F_1,F_2,F_3)=1
\]

over \(\mathbb Q[x,y,z]\), and hence also over \(\mathbb R\) and
\(\mathbb C\). The steady ideal is radical of dimension one. Over
\(\mathbb Q\) its two minimal primes are the conic prime \((L,Q)\) and a
disjoint degree-15 maximal ideal; after scalar extension the latter gives
fifteen reduced isolated points.

## Theorem B: complete conic-preserving fixed-support family

For the same twenty directed reactions, all rational rate vectors for which
\(F_i\in(L,Q)\) for \(i=1,2,3\), and no others, are parametrized by
\((a,b,c,d)\in\mathbb Q^4\) as follows:

\[
\begin{array}{rclcrcl}
k_{01}&=&(62d-15c)/48,&&k_{10}&=&33(58d-45c)/160,\\
k_{04}&=&16d/15,&&k_{40}&=&(c-b)/3,\\
k_{06}&=&(154d-221c)/224,&&k_{60}&=&(9856d-3315c)/1470,\\
k_{17}&=&45(154d-221c)/3136,&&k_{71}&=&5c/14,\\
k_{24}&=&(15a+16d)/15,&&k_{42}&=&(62d-15b-15c)/45,\\
k_{27}&=&(154d-192a-221c)/64,&&k_{72}&=&11(58d-45c)/60,\\
k_{29}&=&a,&&k_{92}&=&2(31d-15c)/45,\\
k_{34}&=&88d/15,&&k_{43}&=&b,\\
k_{59}&=&88d/15,&&k_{95}&=&c,\\
k_{89}&=&33d/5,&&k_{98}&=&d.
\end{array}
\]

This is a four-dimensional linear space. All twenty rates are strictly
positive exactly when

\[
a>0,\quad b>0,\quad c>0,\quad d>0,\quad b<c,
\quad 192a+221c<154d.
\]

For every such point the graph remains reversible and connected, its
stoichiometric space remains \(\mathbb R^3\), and the same entire positive
ellipse consists of equilibria. A nonempty Zariski-open subset of this family
has geometrically coprime coordinate polynomials. Thus gcd one is generic
inside the constrained family, although the continuum is not asserted to
persist under arbitrary rate perturbations outside it.

The canonical conic-remainder map is a rational \(21\times20\) matrix of rank
16. A displayed nonzero 16-minor and four independent kernel vectors certify
both completeness and dimension; see
[`../family/remainder_matrix.csv`](../family/remainder_matrix.csv) and
[`../family/README.md`](../family/README.md).

## Proposition C: fixed-support integer optimum

The specialization

\[
(a,b,c,d)=(653,1,70,915)
\]

is a primitive positive integer member of Theorem B. Among all positive
integral rate vectors in this fixed support and conic-preserving family, it
simultaneously minimizes

\[
\max_j k_j=10296,qquad \sum_jk_j=52464.
\]

The certificate is a bounded exact enumeration after the divisibility
reductions \(15\mid d\) and \(14\mid c\). This proposition is not a global
minimality theorem for reaction supports or networks.

