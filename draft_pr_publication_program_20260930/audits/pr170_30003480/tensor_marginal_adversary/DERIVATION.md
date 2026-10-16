# Independent tensor and marginal derivation for PR170

This derivation uses the frozen submitted claim as the hypothesis to audit. It
does not use the author's checker or review, ROOT or sibling conclusions, or PR
discussion. All mathematical statements below concern real binary tensors and
the closed Frobenius unit ball. No priority or current literature-status claim
is made.

## 1. Objects, assumptions and success criterion

For $T\in(\mathbb R^2)^{\otimes n}$, let $M_i$ be its mode-$i$ matrix,
let $\rho_i=M_iM_i^t$, and write
\[
s=\|T\|_F^2=\operatorname{tr}\rho_i,\qquad d_i=\det\rho_i.
\]
The trace is independent of the mode because every tensor coefficient occurs
once in the diagonal trace. The Gram matrices are positive semidefinite, so

\[
0\le d_i\le s^2/4\le1/4 \quad (s\le1).
\]

The audited locus is

\[
G_n=\{(d_1,\ldots,d_n):\|T\|_F\le1\}\subset C_n=[0,1/4]^n.
\]

The success criterion is a proof or a counterexample for every spectral,
realization and slice step used in the submission's nonexistence argument,
with exact verification of its separate four-factor witness. A finite grid or
tensor sample is supplementary evidence only.

The smaller eigenvalue of a trace-$s$ Gram matrix is

\[
a_s(d)=\frac{s-\sqrt{s^2-4d}}2,
\quad 0\le a_s(d)\le s/2.
\]

For $s=1$, write $\lambda(d)=a_1(d)$. The function

\[
f(t)=t(1-t),\qquad 0\le t\le1/2,
\]

is continuous and strictly increasing onto $[0,1/4]$, with inverse
$\lambda$. Its derivative can vanish at the endpoint without destroying
strict monotonicity. Its inverse is smooth on the open intervals.

The primary HSS paper states the marginal polygon criterion and gives a real
three-factor construction. Its necessity proof and three-factor equations were
inspected in the specified version. The arguments below independently check
the mechanism and all cases needed here.
[Higuchi--Sudbery--Szulc, arXiv version 2](https://arxiv.org/pdf/quant-ph/0209085v2).

## 2. Polygon necessity without an unproved spectral assumption

First take a unit tensor and fix a mode $i$. The real spectral theorem and
real Schmidt decomposition permit

\[
T=\sqrt a\,e_0\otimes u+\sqrt{1-a}\,e_1\otimes v,
\quad a=\lambda_i\in[0,1/2],
\]

where $u,v$ are orthonormal in the remaining tensor product if $a>0$.
The case $a=0$ already satisfies $a\le\sum_{j\ne i}\lambda_j$, so no
choice of a missing Schmidt vector is needed. If $a=1/2$, either orthonormal
eigenbasis is admissible and the same proof applies.

For each $j\ne i$, select a rank-one orthogonal projection $P_j$ onto a
smaller-eigenvalue eigenvector of the $j$-th marginal, acting as the identity
on all other remaining factors. These projections commute. Let $w$ be the
unit product of the complementary eigenvectors, and put $N=\sum P_j$.
In their joint product basis, $N$ has eigenvalues equal to the number of
selected smaller-eigenvector bits. The only basis vector with eigenvalue zero
is $w$. Therefore

\[
N\succeq I-ww^t.
\]

This includes a repeated marginal eigenvalue: any orthonormal eigenbasis
still gives the same diagonal joint-projector statement. Let

\[
p=|\langle w,u\rangle|^2,\qquad q=|\langle w,v\rangle|^2.
\]

Bessel's inequality for the orthonormal pair $u,v$ gives $p+q\le1$.
The cross terms in the expectation of $I\otimes N$ vanish because
$e_0\perp e_1$. Hence

\[
\begin{aligned}
\sum_{j\ne i}\lambda_j
 &=a\langle u,Nu\rangle+(1-a)\langle v,Nv\rangle\\
 &\ge a(1-p)+(1-a)(1-q)\\
 &\ge a(1-p)+a(1-q)\\
 &=a(2-p-q)\ge a.
\end{aligned}
\]

The second inequality uses both $1-a\ge a$ and $1-q\ge0$, rather than an
unstated sign assumption. Thus every normalized real tensor satisfies

\[
\lambda_i\le\sum_{j\ne i}\lambda_j.
\tag{A}
\]

For nonzero $T$ of trace $s$, normalize by $T/\sqrt{s}$. The normalized
Gram is $\rho_i/s$, with smaller eigenvalue $a_s(d_i)/s$ and determinant
$d_i/s^2$. Applying (A) and multiplying by $s$ proves

\[
a_s(d_i)\le\sum_{j\ne i}a_s(d_j).
\tag{B}
\]

The determinant normalization is $s^2$, not $s$: a determinant of a
two-by-two matrix scales quadratically when that matrix is divided by $s$.
When $T=0$, every $d_i=0$ and no division is made.

## 3. The unit-ball trace reduction, including its endpoints

The claim is a necessity implication about determinant tuples: feasibility at
some $0<s\le1$ implies (A) for $t_i=\lambda(d_i)$. It does not assert that
scaling the same tensor to norm one preserves its determinants.

For $d>0$ and $s>2\sqrt d$, differentiating
$a_s(s-a_s)=d$ gives

\[
(s-2a_s)a_s'+a_s=0,
\quad s-2a_s=\sqrt{s^2-4d},
\quad \frac{d}{ds}\log a_s(d)=-\frac1{\sqrt{s^2-4d}}.
\]

Suppose the desired trace-one inequality fails for $i$:

\[
\lambda(d_i)>\sum_{j\ne i}\lambda(d_j).
\tag{C}
\]

Then $d_i>0$ and $d_i>d_j$ for every $j\ne i$, since a term with an
equal or larger determinant alone would contradict (C). All permitted traces
lie in $[s_0,1]$, where $s_0=2\sqrt{d_i}$. For a positive $d_j<d_i$,

\[
\frac d{ds}\log\frac{a_s(d_j)}{a_s(d_i)}
=\frac1{\sqrt{s^2-4d_i}}-\frac1{\sqrt{s^2-4d_j}}>0
\quad(s>s_0).
\tag{D}
\]

Indeed the first radicand is smaller and positive. The denominator
$a_s(d_i)$ is positive throughout $[s_0,1]$, including its lower
endpoint, where it is $s_0/2>0$. For $d_j=0$, the numerator is exactly
zero, so define the ratio as zero rather than differentiating its logarithm.
Every ratio is continuous at $s=s_0$. Their sum is at most its value at
one, which is strictly below one by (C). Consequently

\[
\sum_{j\ne i}a_s(d_j)<a_s(d_i)
\]

at every permitted trace, contradicting (B). If $d_i=1/4$, the interval is
the singleton $s=1$, so the contradiction follows from (B) directly; no
derivative on an empty interval is required. If all determinants are zero,
the trace-one inequalities are immediate. A tie for largest determinant
cannot occur under (C), but may of course occur in feasible tuples. This
completes all zero, tie and discriminant-endpoint cases.

Thus every unit-ball determinant tuple satisfies

\[
\lambda(d_i)\le\sum_{j\ne i}\lambda(d_j).
\tag{E}
\]

## 4. A real construction proves exact closed $G_3$

Take $t_1,t_2,t_3\in[0,1/2]$ satisfying all triangle inequalities. Set

\[
\begin{array}{ll}
w_0=1-(t_1+t_2+t_3)/2,&w_1=(t_2+t_3-t_1)/2,\\
w_2=(t_1+t_3-t_2)/2,&w_3=(t_1+t_2-t_3)/2.
\end{array}
\]

The last three weights are nonnegative, the first is at least $1/4$, and
their sum is one. Define the actual real tensor

\[
S=\sqrt{w_0}e_{000}+\sqrt{w_1}e_{011}
  +\sqrt{w_2}e_{101}+\sqrt{w_3}e_{110}.
\tag{F}
\]

Any off-diagonal marginal entry pairs coefficients with the same other two
bits and opposite chosen bits. Such a pair has opposite parity, so the even
support of (F) contains at most one member. Every off-diagonal entry is zero.
The squared norms of the row indexed by one in the three flattenings are,
respectively,

\[
w_2+w_3=t_1,\qquad w_1+w_3=t_2,\qquad w_1+w_2=t_3.
\]

The other row norm is $1-t_i$. Since $t_i\le1/2$, the smaller
eigenvalue is exactly $t_i$, and the determinant is $f(t_i)$.

There is no positivity restriction on individual coefficients: a saturated
triangle merely sets a weight to zero. If $t_1=0$, the triangle conditions
force $t_2=t_3$, and $w_2=w_3=0$, so the first factor is fixed at zero.
At $t_i=1/2$, the corresponding marginal has repeated eigenvalues; its
determinant remains $1/4$. At $t=(0,0,0)$, (F) is the unit product tensor
with the same determinants as the zero tensor. At $t=(1/2,1/2,1/2)$, all
four weights are $1/4$. Thus all closed boundary cases are covered by a
norm-exactly-one real tensor.

Combining (E) with (F), with $t_i=\lambda(d_i)$, proves

\[
G_3=\{d\in C_3: \lambda(d_i)\le\lambda(d_j)+\lambda(d_k)
\text{ for }\{i,j,k\}=\{1,2,3\}\}.
\tag{G}
\]

In particular, the unit-ball locus and unit-sphere determinant image coincide
for three factors. This conclusion comes from a new realizing tensor, not
from an invalid determinant-preserving rescaling of the original tensor.

## 5. Rank-one peeling gives exact coordinate-zero faces

For any real matrix $M$,

\[
\ker(MM^t)=\ker(M^t),
\]

because $x^tMM^tx=\|M^tx\|^2$. Therefore a zero determinant of a
two-row Gram matrix is equivalent to rank at most one of that flattening.
For nonzero $T$, the rank is one, and rank-one matrix factorization,
followed by reshaping the other indices, yields $T=u\otimes S$ in that
mode. Divide $u$ by its nonzero norm and absorb its norm into $S$. Then

\[
\|u\|=1,\qquad \|T\|=\|S\|.
\]

For any retained mode $k$, write its row indices as $a,b$ and its
remaining indices in $S$ as $\beta$. The Gram entries of $T$ are

\[
(\rho_k(T))_{ab}
=\sum_{\beta,r} S_{a\beta}u_r S_{b\beta}u_r
=\sum_\beta S_{a\beta}S_{b\beta}\sum_r u_r^2
=(\rho_k(S))_{ab}.
\tag{H}
\]

This proves equality of the full retained Gram matrices, not just of their
determinants. Hence every other prescribed zero determinant is still zero
after peeling. Repeat for any set of modes $J$, leaving $m=n-|J|\ge1$
modes. Conversely, tensor a realizing $m$-mode tensor with unit real
vectors in all modes of $J$; (H) proves norm and determinant preservation.
The zero tensor gives no exception. Thus the exact closed slice is

\[
G_n\cap\{d_j=0:j\in J\}
=G_m\times\{0\}^{|J|},
\tag{I}
\]

with coordinates arranged according to the retained modes. In particular,
for $n\ge3$ the face $d_4=\cdots=d_n=0$ equals
$G_3\times\{0\}^{n-3}$. If every mode is peeled, the determinant tuple
is simply zero, also realized by a unit product tensor. This is an exact
rank statement, not a limit of approximate factorizations.

For completeness, $G_1=\{0\}$: its flattening has one column. For $n=2$,
the two determinants both equal $(\det M)^2$. Every diagonal tuple
$(d,d)$, $0\le d\le1/4$, is realized by the diagonal matrix with entries
$\sqrt{\lambda(d)},\sqrt{1-\lambda(d)}$, of norm one. Thus the stated
small-$n$ exceptions are exact. Inside their cubes they are cut out by
$-d_1^2\ge0$ and $-(d_1-d_2)^2\ge0$, respectively.

## 6. Independent check of the convex hull $H_n$

Let $H_n$ be the cube intersection with $d_i\le\sum_{j\ne i}d_j$.
We can verify the claimed convex-hull identity without importing the printed
three-factor formula. For $d\in G_n$, let $t_i=\lambda(d_i)$ and fix

\[
S=\sum_{j\ne i}t_j\ge t_i.
\]

If $S\le1/2$, the increasing function $f$ satisfies

\[
f(t_i)\le f(S)=S-S^2\le S-\sum_{j\ne i}t_j^2
=\sum_{j\ne i}f(t_j).
\]

The second inequality uses nonnegative cross terms. If $S>1/2$, each
$f(t_j)\ge t_j/2$, whence

\[
\sum_{j\ne i}f(t_j)\ge S/2>1/4\ge f(t_i).
\]

Therefore $G_n\subset H_n$, and $\operatorname{conv}G_n\subset H_n$.

To classify the vertices of $H_n$, put $x_i=4d_i$. A feasible positive
support cannot have size one. If it has size two, the two positive
coordinates must coincide, and a common value strictly between zero and one
can be perturbed in both directions, so it is not a vertex. If the positive
support has size at least three, at most one polygon equality can hold:
two equalities would give $x_i=x_j=(\sum x)/2$, leaving every other
coordinate zero. Let $k$ count the coordinates strictly between zero and
one, with all other box coordinates held fixed. If $k\ge2$, there is a
nonzero perturbation supported on those coordinates satisfying the at most
one active polygon equality. Small positive and negative perturbations
preserve all strict inequalities, so the point is not a vertex.

If $k=1$, let $x$ be the fractional coordinate and let $m$ count the
other positive coordinates, all equal to one. An active polygon equality
at the fractional coordinate would require $x=m$; an equality at a
coordinate one would require $x=2-m$. Both are integral. A zero
coordinate cannot have an equality because the total is positive. Thus no
polygon equality is active, and the fractional coordinate can again be
perturbed. The only vertices are zero and the zero-one vectors with at least
two ones. Each is indeed a vertex because it is already a cube vertex.

For a chosen subset $K$ of at least two factors, the real tensor

\[
\frac{e_{0\cdots0}+e_{1_K0_{K^c}}}{\sqrt2}
\]

has determinant $1/4$ in the factors of $K$ and zero in the others.
For $i\in K$, another differing bit ensures the two rows have disjoint
columns, so their Gram is diagonal with both entries $1/2$. Outside $K$
the bit is fixed at zero. A unit product tensor realizes vertex zero. Every
vertex of the bounded polytope $H_n$ therefore belongs to $G_n$, giving

\[
\operatorname{conv}G_n=H_n\quad(n\ge2).
\tag{J}
\]

This identity agrees with the primary paper's convex-hull theorem, inspected
at printed p.353, but the proof above is independent. Direct substitution
also gives $H_n\cap\{d_4=\cdots=d_n=0\}=H_3\times\{0\}^{n-3}$: the first
three inequalities become those of $H_3$, and the remaining ones are
automatic.

## 7. The local polynomial obstruction and its transfer

This check completes the link from the spectral family to the submitted
universal conclusion. Suppose $P$ defines $G_3$ inside $C_3$ by
nonnegativity. Put

\[
F(t)=P(f(t_1),f(t_2),f(t_3)),\quad D=(0,1/2)^3.
\]

The map $f$ is a diffeomorphism on these open intervals, and $F$ is a
polynomial invariant under every separate replacement $t_i\mapsto1-t_i$.
Within $D$, (G) turns membership into the three ordinary triangle
inequalities. Consider $L=t_1-t_2-t_3$, on the patch

\[
t_2=b>0,\quad t_3=c>0,\quad b+c<1/2.
\]

The other two triangle inequalities are strict. Locally $L<0$ is feasible
and $L>0$ is infeasible. Therefore $F\ge0$ on the first side and $F<0$
on the second. Continuity forces zero on the plane patch. Polynomial
division in the coordinate $L$ shows $L\mid F$: its constant term
restricts to a polynomial in $b,c$ vanishing on an open set, so that
polynomial is identically zero.

The polynomial $F$ is nonzero because an outside point in $D$ requires

$F<0$. Write $F=L^m R$ with exact multiplicity $m\ge1$. Exactness
means $R$ is not identically zero on the plane. A nonzero plane polynomial
cannot vanish on the whole open patch, so choose a patch point with $R\ne0$.
In a small neighborhood there $R$ has a fixed nonzero sign. The required
sign change then forces $m$ odd. This does not assume strict positivity
of $F$ throughout the locus; it only uses nonvanishing of $R$ at the
selected point.

The affine involution $t_1\mapsto1-t_1$ fixes $F$ and maps $L$ to

\[-L',\qquad L'=t_1+t_2+t_3-1.\]

It preserves exact multiplicity, so $L'$ has the same odd multiplicity

$m$. But an open patch of $L'=0$ about $(1/3,1/3,1/3)$ lies strictly
inside $D$ and all three triangle inequalities. Thus $F\ge0$ on a full
neighborhood. Select a patch point where the residual factor after removing
$(L')^m$ is nonzero, again by exactness. Odd $m$ forces opposite signs
on the two sides there, a contradiction. Hence no such $P$ exists.

The same local argument works inside $H_3$. On $t=(b+c,b,c)$, the three
determinant slacks are

\[
2bc,\qquad2c(1-b-c),\qquad2b(1-b-c),
\]

all strictly positive. On the positive plane $\sum t_i=1$ inside $D$,
the three slacks are $2t_jt_k>0$. Every coordinate is strictly between
zero and $1/4$. Consequently the two open neighborhoods needed for the
sign arguments can be chosen entirely in the interior of $H_3$, despite
the fact that the first plane is a boundary of the smaller locus $G_3$.

For $n>3$, restrict any alleged polynomial $P_n$ to the coordinate-zero
face, obtaining $P_n(d_1,d_2,d_3,0,\ldots,0)$. The exact slices (I) and
the corresponding $H_n$ slice make this a single-polynomial definition of
$G_3$ in $C_3$, or in $H_3$, respectively. It cannot be the zero
polynomial, since that would include all of the relevant face, including
points excluded by (G). Thus both universal nonexistence claims follow for
every $n\ge3$. The argument requires the closed coordinate-zero face;
no assertion about removing all zero coordinates follows automatically.

## 8. Exact all-positive four-factor obstruction

The specified primary paper defines the two products and proposes their
comparison for $n\ge4$; the normalization and formulas were read in the
published PDF, and printed p.354 was visually inspected.
[Seigal, published paper](https://seigal.github.io/seigal2018gram.pdf).

The audited products are precisely

\[
Q_1(d)=\prod_{i=1}^n\left(\sum_{j\ne i}d_j-d_i\right),\qquad
Q_2(d)=\frac12\prod_{\epsilon\in\{-1,1\}^n}
\left(\sum_i\epsilon_i\sqrt{d_i}\right).
\]

The prefactor is one half, and the product includes every global-sign
partner. The tested comparison is $Q_1\ge Q_2$.

For the submitted tuple

\[
d=(2401/10000,81/625,81/625,1/10000),
\quad \sqrt d=(49,36,36,1)/100,
\]

all coordinates lie strictly in the cube. The determinant-polygon slacks,
in coordinate order, are exactly

\[
12/625,\quad1201/5000,\quad1201/5000,\quad312/625.
\]

Evaluating all sixteen signed factors with exact rational arithmetic gives

\[
Q_1=\frac{168760917}{305175781250},\qquad
Q_2=\frac{23632249608}{2384185791015625},
\]

\[
Q_1-Q_2=\frac{2589624828909}{4768371582031250}>0.
\]

Independently certify nonmembership using the strictly increasing inverse
pair $f,\lambda$:

\[
d_1-f(2/5)=1/10000>0,
\quad f(1/6)-d_2=f(1/6)-d_3=209/22500>0,
\]

\[
f(1/100)-d_4=49/5000>0.
\]

Thus $\lambda(d_1)>2/5$, while the other three sum to less than
$1/6+1/6+1/100=103/300<2/5$. This violates (E), so the tuple cannot
arise from any real tensor with norm at most one, at any allowed trace.
This is a strict open-cube, strict-$H_4$ obstruction, separate from the
coordinate-zero face proof.

## 9. Independent printed-source caution

The actual real unit tensor

\[
T=(e_{000}+e_{111})/\sqrt2
\]

has each marginal $\operatorname{diag}(1/2,1/2)$, so its determinant tuple
is $(1/4,1/4,1/4)$. Exact evaluation of the printed products gives

\[
Q_1=1/64,\qquad Q_2=9/512.
\]

The first displayed region therefore fails. Each printed secondary pair
expression equals $1/4$, exceeding its printed bound $3/16$; the visual
inspection confirms that the displayed sign is $\le$. Consequently the
union as displayed excludes this actual tensor. The submitted caution is
correct. This check neither repairs that display nor invalidates other
theorems of the paper.

As a separate check against an endpoint-only explanation, take

\[
t=(9/20,9/20,9/20),\quad d=(99/400,99/400,99/400).
\]

Construction (F) realizes it with weights $(13/40,9/40,9/40,9/40)$, all
positive. For equal coordinates $d=x$, the printed products evaluate to
$Q_1=x^3$ and $Q_2=(9/2)x^4$. At $x=99/400$, their ratio is

$Q_2/Q_1=891/800>1$, and each secondary pair expression is
$99/400>3/16$. Thus the displayed union also excludes an explicitly
realized point in the open cube. This is additional scoped evidence of the
same display issue; it is not used in the main proof.

## 10. Reproducible falsification controls and exact remaining gap

`controls.py` uses only exact rational arithmetic and explicit rational
tensor coefficients (with a common rational squared scale where necessary).
It checks 65 feasible closed-grid parity tuples, an asymmetric actual real
tensor, subunit determinant normalization, boundary cases, contractions
through five additional real noncoordinate unit factors, 219 subset-GHZ
vertices, the strict-$H_3$ nonmember, and the two source arithmetic checks.
The written arguments, rather than these finite instances, prove the
universal claims.

Its supervisor requires ten materially wrong variants to fail with explicit
errors in each of ordinary Python and `python -O`: reversed derivative,
wrong trace power, wrong parity labels, wrong support, an unnormalized peeled
factor, annihilated retained Grams, replacing the locus by its hull, removing
the source product's half, removing global-sign partners, and asserting that
the displayed secondary union includes GHZ. It uses no language `assert`
statements. Both baseline executions pass and all twenty false-variant
executions return the expected explicit rejection.

No mathematical gap remains in the claims assigned to this tensor/marginal
family: necessity at all unit-ball traces, exact closed real $G_3$, exact
closed slices for every $n$, both stated nonexistence domains, the convex
hull identity, the rational $n=4$ obstruction and the scoped source caution.
This audit does not establish historical novelty, present literature status,
or anything about a punctured all-positive-domain replacement problem.
