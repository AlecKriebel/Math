# An exact \(3/4\)-covering lemma

Let \(S\) be the fixed 12-point support and let \(V\) be the other 28
normalized \(D_5\) roots.

## Lemma

Every unit vector \(y\) satisfying
\[
\langle s,y\rangle\le\frac12\qquad(s\in S)
\]
satisfies
\[
\boxed{\max_{v\in V}\langle v,y\rangle\ge\frac34.}
\tag{1}
\]
Equality is attained.  In the scaled coordinates \(z=\sqrt2y\), all equality
points are
\[
z=(\epsilon_1/2,\ 1/2,\ \epsilon_3,\ 1/2,\ \epsilon_5/2),
\qquad \epsilon_1,\epsilon_3,\epsilon_5\in\{-1,1\}.
\tag{2}
\]

## Proof

Assume in addition that
\(\langle v,y\rangle\le3/4\) for every \(v\in V\).  In scaled coordinates
this gives
\[
r\cdot z\le1\quad(r/\sqrt2\in S),\qquad
r\cdot z\le\frac32\quad(r/\sqrt2\in V).
\tag{3}
\]
It suffices to prove that every point satisfying (3) has
\(\|z\|^2\le2\).

Put
\[
a=|z_1|,\quad b=|z_3|,\quad c=|z_5|,\quad
U=|z_2|,\quad V_0=|z_4|,
\]
and fix the two signs
\(\sigma=\operatorname{sgn}(z_2)\),
\(\tau=\operatorname{sgn}(z_4)\).  Zero coordinates may be assigned either
sign.  For each of the four choices
\((\sigma,\tau)\in\{-1,1\}^2\), (3) is exactly the following 19 rational
linear inequalities in the five nonnegative variables
\((a,b,c,U,V_0)\):
\[
\begin{array}{rclrcl}
-a&\le&0,&-b&\le&0,\\
-c&\le&0,&-U&\le&0,\\
-V_0&\le&0,\\[2mm]
a+\tau V_0&\le&1,&b-\sigma U&\le&1,\\
c+\sigma U&\le&1,&b-\tau V_0&\le&1,\\
a+c&\le&1,\\[2mm]
a+U&\le&3/2,&a+b&\le&3/2,\\
a-\tau V_0&\le&3/2,&b+\sigma U&\le&3/2,\\
U+V_0&\le&3/2,&c-\sigma U&\le&3/2,\\
b+\tau V_0&\le&3/2,&b+c&\le&3/2,\\
c+V_0&\le&3/2.
\end{array}
\tag{4}
\]
The equivalence follows by taking the maximum over the signs present among
the relevant \(D_5\) roots.

The polytope (4) is compact.  The convex function
\[
Q=a^2+b^2+c^2+U^2+V_0^2
\]
attains its maximum at a vertex.  Every vertex has five linearly independent
active inequalities, so enumerating the \(\binom{19}{5}=11628\) possible
bases in each sign case covers every vertex.  Exact rational elimination
gives:

| \(\sigma\) | \(\tau\) | distinct vertices | maximum \(Q\) |
|---:|---:|---:|---:|
| \(-1\) | \(-1\) | 46 | \(29/16\) |
| \(-1\) | \(1\) | 46 | \(29/16\) |
| \(1\) | \(-1\) | 46 | \(29/16\) |
| \(1\) | \(1\) | 60 | \(2\) |

The only magnitude vertex with \(Q=2\) is
\[
(a,b,c,U,V_0)=(1/2,1,1/2,1/2,1/2).
\]
The exact enumerator `verify_covering_lemma.py` independently constructs all
four inequality systems, solves every basis over `fractions.Fraction`, checks
feasibility against all 19 closed inequalities, and reproduces this table.
Thus (3) implies \(\|z\|^2\le2\).  On the sphere \(\|z\|^2=2\), equality
forces (2).  This proves (1), including all boundary cases.

## A local consequence

For a fixed \(v\in S^4\), a kissing code contains at most five points \(y\)
with \(\langle v,y\rangle\ge3/4\).

Indeed, if one of the heights is \(1\), no other such point is compatible
with it.  Otherwise write
\[
y=h v+\sqrt{1-h^2}\,u,\qquad u\in S^3.
\]
For two points of heights \(h,k\ge3/4\), the kissing inequality implies
\[
\langle u,u'\rangle
\le \frac{1/2-hk}{\sqrt{(1-h^2)(1-k^2)}}\le-\frac17.
\tag{5}
\]
For the last inequality, both sides have the appropriate sign and
\[
49(hk-1/2)^2-(1-h^2)(1-k^2)\ge0;
\]
the left side is increasing in each of \(h,k\) on \([3/4,1]\) and vanishes
at \(h=k=3/4\).

There are at most five pairwise negatively correlated unit vectors in
\(\mathbb R^4\).  Otherwise, an affine dependence among six of them has
coefficients summing to zero.  Splitting the positive and negative
coefficients gives two equal vectors whose mutual inner product is strictly
negative, a contradiction.

This cap bound and the 28-cap cover yield only \(m\le140\) by naive double
counting.  A natural Hall-type strengthening would ask whether, for a kissing
code \(Y\) in the polar region, the sets
\[
N(y)=\{v\in V:\langle v,y\rangle\ge3/4\}
\]
always admit distinct representatives.  Such a statement would immediately
give \(m\le28\), but it is false: `hall_counterexample.md` gives two exact
compatible algebraic points for which both neighborhoods are the same
singleton.  Thus no matching conclusion may be inferred from the covering
lemma.
