# A four-parameter family of reversible three-species mass-action continua without a common factor

## Abstract

We exhibit a four-dimensional exact rate family on a fixed reversible
three-species reaction graph with one linkage class, ten complexes, and ten
reversible pairs.  Every positive member of the family has full
stoichiometric rank and vanishes on the same compact positive algebraic
ellipse.  The positive part of rate space is a rational open polyhedral cone,
and a nonempty Zariski-open subset of the family has geometrically coprime
coordinate polynomials.  Thus the equilibrium continuum is generically a
height-two component within this constrained family, not a common-factor
hypersurface.

We give a primitive positive integer specialization with largest rate
$10296$ and rate sum $52464$.  Within the fixed support and conic-preserving
family, it simultaneously minimizes both quantities among positive integral
rate vectors.  Its steady ideal is radical: over $\mathbb Q$ its two minimal
primes are the conic prime and a degree-fifteen maximal ideal.  We also retain
the original frozen integer specialization and determine its transverse
linear stability along the ellipse.  The ellipse has one normally attracting
arc and one saddle-type arc, separated by two exactly isolated transition
points.  All algebraic, integer-optimality, and Sturm claims are accompanied
by exact symbolic verifiers.

## 1. Introduction

For a finite reaction network with complexes
$y\in\mathbb Z_{\geq0}^n$, positive rates
$\kappa_{y\to y'}$, and concentrations $x\in\mathbb R_{>0}^n$, the
mass-action vector field is

\[
F(x)=\sum_{y\to y'}\kappa_{y\to y'}x^y(y'-y).
\tag{1}
\]

A network is weakly reversible if every directed reaction belongs to a
directed cycle, and reversible if every reaction is paired with its reverse.
The stoichiometric subspace is

\[
S=\operatorname{span}_{\mathbb R}\{y'-y:y\to y'\},
\]

and the positive compatibility class through $x_0$ is
$(x_0+S)\cap\mathbb R_{>0}^n$.

Boros, Craciun, and Yu asked whether a weakly reversible mass-action system
can have infinitely many positive steady states without a polynomial common
factor in the right-hand side [BCY20].  The frozen first version of this work
answered that question with a reversible, one-linkage, three-species example
whose coordinate gcd is one and whose steady variety contains a positive
conic.  The present version keeps that theorem unchanged and develops the
larger exact structure surrounding it.

The additions are fourfold.

1. We determine all rate vectors on the fixed directed support for which the
   same conic remains an equilibrium component.
2. We identify the strict positive rate cone and prove that geometric
   coprimality holds on a nonempty Zariski-open subset.
3. We give a substantially smaller primitive integer specialization and an
   exact fixed-support optimality certificate.
4. For the frozen first specialization, we classify the two transverse
   eigenvalues everywhere on the equilibrium ellipse.

No claim of global minimality in complexes or reactions is made.  The integer
optimality result is explicitly restricted to this fixed support and this
conic-preserving rate family.

## 2. Fixed support and conic

### 2.1 Complexes and reversible graph

Use species $X,Y,Z$, with concentration variables $x,y,z$, and index the
complexes as follows.

| index | exponent vector | complex |
|---:|:---:|:---|
| 0 | $(0,0,0)$ | $0$ |
| 1 | $(0,0,1)$ | $Z$ |
| 2 | $(0,0,3)$ | $3Z$ |
| 3 | $(0,1,1)$ | $Y+Z$ |
| 4 | $(0,3,0)$ | $3Y$ |
| 5 | $(1,0,1)$ | $X+Z$ |
| 6 | $(1,1,0)$ | $X+Y$ |
| 7 | $(1,1,1)$ | $X+Y+Z$ |
| 8 | $(2,1,0)$ | $2X+Y$ |
| 9 | $(3,0,0)$ | $3X$ |

The ten undirected edges are

\[
01, 04, 06, 17, 24, 27, 29, 34, 59, 89,
\tag{2}
\]

and both orientations of every edge are reactions.  The complete rate tables
for the two integer specializations appear in Appendix A.

The graph is connected: from $0$ one reaches $1,4,6$, then $7,2,9$,
and finally $3,5,8$.  Hence there is one linkage class.  The three reaction
differences

\[
0\to Z=(0,0,1),\qquad
0\to3Y=(0,3,0),\qquad
0\to X+Y=(1,1,0)
\]

have determinant $-3$.  Therefore the stoichiometric subspace is

\[
S=\mathbb R^3,
\tag{3}
\]

independently of the positive rate values.  There are no conservation laws,
and the unique positive compatibility class is the full positive orthant.

### 2.2 The common equilibrium conic

Define

\[
L=z-x-y+1
\tag{4}
\]

and

\[
Q=7x^2-2xy-16x+7y^2-16y+16.
\tag{5}
\]

The ideal

\[
\mathfrak p=(L,Q)\subset\mathbb Q[x,y,z]
\tag{6}
\]

is a height-two prime.  Indeed, eliminating $z$ leaves a nonsingular plane
conic.  The symmetric matrix of its homogenization is

\[
\begin{pmatrix}
7&-1&-8\\
-1&7&-8\\
-8&-8&16
\end{pmatrix},
\]

with determinant $-256$, so the projective conic is nonsingular and
geometrically irreducible.

An exact rational parametrization is

\[
\begin{aligned}
d(t)&=t^2-t+1,\\
x(t)&=\frac{t^2+3}{2d(t)},\\
y(t)&=\frac{3t^2+1}{2d(t)},\\
z(t)&=\frac{t^2+t+1}{d(t)}.
\end{aligned}
\tag{7}
\]

Direct substitution gives $L=Q=0$.  All coordinates are positive for every
real $t$, since

\[
d(t)=\left(t-\frac12\right)^2+\frac34,
\qquad
t^2+t+1=\left(t+\frac12\right)^2+\frac34,
\]

and the other numerators are $t^2+3$ and $3t^2+1$.  On $(-1,1)$,

\[
z'(t)=\frac{2(1-t^2)}{d(t)^2}>0,
\]

so the parametrized equilibria there are pairwise distinct.

The entire real conic is a compact positive ellipse.  On $L=0$, set
$s_0=x+y=z+1$ and $u=x-y$.  Equation $Q=0$ becomes

\[
4\bigl(u^2+(z-1)^2\bigr)=(z+1)^2.
\tag{8}
\]

It follows that $1/3\leq z\leq3$ and
$|u|\leq(z+1)/2$, which gives $x,y,z>0$.

## 3. The exact four-parameter rate family

Order the twenty directed rates as

\[
\begin{gathered}
k_{01},k_{10},k_{04},k_{40},k_{06},k_{60},k_{17},k_{71},
k_{24},k_{42},\\
k_{27},k_{72},k_{29},k_{92},k_{34},k_{43},k_{59},k_{95},
k_{89},k_{98}.
\end{gathered}
\tag{9}
\]

Here the subscripts are complex indices, not species indices.

**Theorem 3.1 (complete conic-preserving family).**
Let $F(k)$ be the mass-action field on the support (2).  All three
coordinates of $F(k)$ belong to $\mathfrak p=(L,Q)$ if and only if, for
some $a,b,c,d\in\mathbb Q$, the rates in the order (9) are

\[
\begin{aligned}
k_{01}&=(62d-15c)/48,&
k_{10}&=33(58d-45c)/160,\\
k_{04}&=16d/15,&
k_{40}&=(c-b)/3,\\
k_{06}&=(154d-221c)/224,&
k_{60}&=(9856d-3315c)/1470,\\
k_{17}&=45(154d-221c)/3136,&
k_{71}&=5c/14,\\
k_{24}&=(15a+16d)/15,&
k_{42}&=(62d-15b-15c)/45,\\
k_{27}&=(154d-192a-221c)/64,&
k_{72}&=11(58d-45c)/60,\\
k_{29}&=a,&
k_{92}&=2(31d-15c)/45,\\
k_{34}&=88d/15,&
k_{43}&=b,\\
k_{59}&=88d/15,&
k_{95}&=c,\\
k_{89}&=33d/5,&
k_{98}&=d.
\end{aligned}
\tag{10}
\]

The conic-preserving rate space has dimension four, and
$(a,b,c,d)=(k_{29},k_{43},k_{95},k_{98})$ are free coordinates.

*Proof.*  Use lexicographic order $z>y>x$.  The reduced Gröbner basis of
$\mathfrak p$ is

\[
z-x-y+1,\qquad
y^2-\frac27xy+x^2-\frac{16}{7}(x+y)+\frac{16}{7}.
\tag{11}
\]

Every degree-at-most-three normal form has a unique coefficient vector in the
ordered monomial list

\[
(1,x,y,x^2,xy,x^3,x^2y).
\]

Reduce the contribution of each unit directed rate modulo (11), and stack
these seven coefficients for the three field coordinates.  This constructs a
canonical rational matrix $M\in\mathbb Q^{21\times20}$ such that

\[
F_i(k)\in(L,Q)\quad(i=1,2,3)
\quad\Longleftrightarrow\quad Mk=0.
\tag{12}
\]

The $16\times16$ minor with zero-based rows

\[
0,1,2,4,5,6,7,8,9,12,13,14,15,16,18,19
\]

and columns

\[
0,1,2,3,4,5,6,7,8,9,10,11,13,14,16,18
\]

has determinant

\[
\frac{7255941120}{823543}
=\frac{2^{13}3^{11}5}{7^7}\neq0.
\tag{13}
\]

Thus $\operatorname{rank}M\geq16$.  Substitution of (10) gives four
linearly independent kernel vectors, since their entries in positions
$12,15,17,19$ form the identity matrix.  Hence
$\operatorname{rank}M=16$, the nullity is four, and (10) is exhaustive.
The complete matrix and an integer-vector kernel basis are included with the
exact family verifier.  $\square$

**Corollary 3.2 (strict positive cone).**
All twenty rates in (10) are positive exactly when

\[
a>0,\quad b>0,\quad c>0,\quad d>0,\quad b<c,\quad
192a+221c<154d.
\tag{14}
\]

The cone is rationally parametrized by an open positive orthant via

\[
c=b+h,\qquad
d=\frac{192a+221(b+h)+s}{154},\qquad a,b,h,s>0.
\tag{15}
\]

*Proof.*  Necessity follows from the four free rates and the two entries

\[
k_{40}=\frac{c-b}{3},\qquad
k_{27}=\frac{154d-192a-221c}{64}.
\]

Conversely, substitute (15) into (10).  Every rate becomes a nonzero linear
form in $a,b,h,s$ with nonnegative rational coefficients.  This proves
sufficiency.  The inverse coordinates are
$h=c-b$ and $s=154d-192a-221c$, so (15) is a bijection.  $\square$

Every rate vector in (14) retains the connected reversible support and full
stoichiometric rank.  Its unique positive compatibility class contains the
entire ellipse (6).

## 4. Generic geometric coprimality

The conic constraint is linear in rate space, but it does not generically
force a coordinate common factor.

**Lemma 4.1 (scalar extension).**
Let $f_1,\ldots,f_r\in\mathbb Q[x_1,\ldots,x_n]$.  If they have a
nonconstant common factor over $\mathbb C$, then they have a nonconstant
common factor over $\mathbb Q$.

*Proof.*  Choose a normalized irreducible complex common factor.  Its
coefficients are algebraic over $\mathbb Q$, because it is a factor of a
rational polynomial.  Rationality of every $f_i$ forces every distinct
Galois conjugate of the chosen factor to divide every $f_i$.  Their product,
after multiplication by a scalar, is a nonconstant rational polynomial
dividing every $f_i$.  $\square$

**Theorem 4.2 (generic geometric gcd one).**
There is a nonempty Zariski-open subset of the four-dimensional rate family
(10) on which

\[
\gcd(F_1,F_2,F_3)=1
\]

over $\mathbb Q$, $\mathbb R$, and $\mathbb C$.

*Proof.*  Homogenize all three coordinates to degree three in variables
$x,y,z,w$.  Let $V_j$ denote the vector space of degree-$j$ forms in
these variables.  For $e=1,2,3$, triples with a common homogeneous factor
of degree $e$ form the image

\[
\Sigma_e=\operatorname{im}\left(
\mathbb P(V_e)\times\mathbb P(V_{3-e}^{\oplus3})
\longrightarrow\mathbb P(V_3^{\oplus3})
\right)
\tag{16}
\]

of the multiplication morphism.  The source is projective, so
$\Sigma_e$ is closed.  Its affine cone
$\widehat\Sigma_e\subset V_3^{\oplus3}$, including the zero triple, is
closed.  The finite union of these cones pulls back along the linear rate map
$\mathbb A^4\to V_3^{\oplus3}$ to a closed subset of parameter space.  This
formulation explicitly includes the origin, at which projectivization is
undefined.

Every affine common factor homogenizes to a homogeneous common factor.  The
clean integer specialization in Section 5 has both affine and homogenized
coordinate gcd equal to one over $\mathbb Q$, as checked by exact
factorization.  Lemma 4.1 excludes a factor after scalar extension.  Hence
this specialization lies outside the pulled-back closed set, whose complement
is the required nonempty Zariski-open set.  $\square$

The theorem is deliberately a generic statement *inside the constrained
four-dimensional family*.  It does not assert persistence of a continuum
under arbitrary perturbations of all rates: leaving (10) generally destroys
the conic component, consistently with generic-finiteness results such as
[FHP26].

For every parameter outside the closed common-factor locus, the steady ideal
is nonzero, is contained in the height-two prime $(L,Q)$, and is contained in
no height-one prime.  It therefore has height exactly two, and $(L,Q)$ is a
minimal prime over it.  Thus the same ellipse is genuinely an irreducible
steady-state component throughout this Zariski-open subset, not merely at the
two integer specializations below.

## 5. A clean fixed-support-optimal integer specialization

Set

\[
(a,b,c,d)=(653,1,70,915).
\tag{17}
\]

Its positive-orthant coordinates from (15) are

\[
(a,b,h,s)=(653,1,69,64),
\tag{18}
\]

which provide a compact strict-interiority certificate.

**Theorem 5.1 (clean integer construction).**
The rates obtained from (17), listed in Appendix A, are primitive positive
integers.  They define a reversible, one-linkage mass-action system with ten
complexes, twenty directed reactions, and $S=\mathbb R^3$.  Its unique
positive compatibility class contains the entire ellipse $\mathcal C=V(L,Q)$,
but its coordinate polynomials have gcd one over
$\mathbb Q[x,y,z]$, and therefore also over $\mathbb R$ and
$\mathbb C$.

The vector field is

\[
\begin{aligned}
F^{\mathrm c}_1={}&-4697x^3+6039x^2y-9177xyz-5977xy+10736xz\\
&+1960z^3+1800z+560,\\[1mm]
F^{\mathrm c}_2={}&915x^3-6039x^2y-9177xyz-5977xy-3782y^3\\
&+10736yz+4888z^3+1800z+3488,\\[1mm]
F^{\mathrm c}_3={}&3712x^3+18304xyz-5368xz+3712y^3-5368yz\\
&-6848z^3-10296z+1160.
\end{aligned}
\tag{19}
\]

Its steady ideal is radical of dimension one.  Over $\mathbb Q$ it has
exactly two minimal primes: the conic prime $\mathfrak p=(L,Q)$ and a
degree-fifteen maximal ideal disjoint from $\mathfrak p$.  Over the algebraic
closure, the latter component consists of fifteen reduced isolated points.

*Proof.*  Formula (10) and (17) give the twenty rates exactly.  Positivity
also follows directly from (18).  The graph and rank statements were proved
in Section 2, and Theorem 3.1 gives
$F_i^{\mathrm c}\in(L,Q)$.  Exact expansion of (1) gives (19).  Exact
multivariate gcd computation gives

\[
\gcd(F^{\mathrm c}_1,F^{\mathrm c}_2)
=\gcd(F^{\mathrm c}_1,F^{\mathrm c}_3)
=\gcd(F^{\mathrm c}_2,F^{\mathrm c}_3)=1.
\tag{20}
\]

Lemma 4.1 upgrades this to geometric coprimality.

For the radical statement, put

\[
D=y^2-yz-y+\frac7{16}z^2-\frac18z+\frac7{16},
\tag{21}
\]

so $\mathfrak p=(L,D)$.  The exact reduced lexicographic Gröbner basis of
$K_{\mathrm c}=(F^{\mathrm c}_1,F^{\mathrm c}_2,F^{\mathrm c}_3)$, for
$x>y>z$, has the form

\[
G_0,\qquad DH,\qquad DR,
\tag{22}
\]

where $G_0$ is monic linear in $x$, $H$ is linear in $y$ with
nonzero constant leading coefficient, and $R\in\mathbb Q[z]$ is irreducible
of degree fifteen.  Let $\mathfrak q=(G_0,H,R)$.  Its reduced basis is
triangular,

\[
x+r_x(z),\qquad y+r_y(z),\qquad R(z),
\]

so $\mathfrak q$ is maximal of degree fifteen.  Exact reduction gives
$D\notin\mathfrak q$, hence
$\mathfrak p+\mathfrak q=(1)$, and every product of a generator of
$\mathfrak p$ with a generator of $\mathfrak q$ reduces to zero modulo
(22).  Conversely, each generator of $K_{\mathrm c}$ lies in both primes.
Therefore

\[
K_{\mathrm c}=\mathfrak p\mathfrak q
=\mathfrak p\cap\mathfrak q
=\sqrt{K_{\mathrm c}}.
\tag{23}
\]

Characteristic zero makes $R$ separable, yielding fifteen reduced points
after scalar extension.  Every reduction and factorization in this argument
is replayed by the exact verifier.  $\square$

### 5.1 Fixed-support integer optimality

The clean vector has

\[
\max_j k_j=10296,\qquad \sum_j k_j=52464,\qquad
\gcd(k_0,\ldots,k_{19})=1.
\tag{24}
\]

**Proposition 5.2 (bounded exact optimum).**
Among all positive integral vectors in the fixed-support family (10), the
clean vector simultaneously attains the smallest possible largest entry and
the smallest possible sum of entries.

*Proof.*  Integrality of
$k_{04}=16d/15$ and $k_{71}=5c/14$ forces

\[
15\mid d,\qquad 14\mid c.
\tag{25}
\]

If $\max_j k_j<10296$, then $k_{34}=88d/15$ gives $d<1755$.  If
$\sum_j k_j<52464$, then

\[
k_{34}+k_{59}+k_{89}+k_{98}=\frac{58}{3}d
\]

gives $d<2714$.  These bounds reduce both strict-improvement questions to
finite exact searches.

For each multiple $d$ of $15$ in the relevant range and each multiple
$c$ of $14$, positivity permits the safe bounds $c<d$, $1\le b<c$,
and $1\le a<d$.  The formulas (10) separate into entries depending only on
$(c,d)$, on $(a,c,d)$, and on $(b,c,d)$.  The verifier enumerates these
finite integer sets using rational arithmetic, rejects every nonintegral or
nonpositive entry, and computes the exact minimum of the maximum and of the
sum.  It returns respectively $10296$ and $52464$, both attained at
(17).  No floating-point optimization or rational reconstruction enters the
certificate.  $\square$

This proposition is not a network-wide minimality theorem.  It fixes the
twenty directed reactions, the conic, and primitive integer normalization.
A common positive scaling of all rates merely rescales time.

## 6. The frozen first specialization

The original theorem remains valid without alteration.  Its free parameters
are

\[
(a,b,c,d)=(3920,3920,15680,658560)
=3920(1,1,4,168),
\tag{26}
\]

and its positive-orthant coordinates are

\[
(a,b,h,s)=(3920,3920,11760,97200320).
\tag{27}
\]

Thus the frozen rate vector is also a strict interior point of the exact
family, not a boundary specialization.

**Theorem 6.1 (frozen v1 construction).**
The original rates in Appendix A define a reversible, one-linkage,
three-species mass-action system with $S=\mathbb R^3$, the full positive
ellipse $\mathcal C$ as an equilibrium component, and

\[
\gcd(F^{0}_1,F^{0}_2,F^{0}_3)=1.
\]

Its steady ideal is radical and equals the intersection of the conic prime
with a disjoint degree-fifteen maximal ideal over $\mathbb Q$.

Its vector field is

\[
\begin{aligned}
F^0_1={}&-3380608x^3+4346496x^2y-6878928xyz-4380128xy\\
&+7727104xz+1530515z^3+1405575z+437290,\\[1mm]
F^0_2={}&658560x^3-4346496x^2y-6878928xyz-4380128xy\\
&-2722048y^3+7727104yz+3637907z^3+1405575z+2544682,\\[1mm]
F^0_3={}&2706368x^3+13746656xyz-3863552xz+2706368y^3\\
&-3863552yz-5168422z^3-7732494z+845740.
\end{aligned}
\tag{28}
\]

*Proof.*  Equations (26) and (10) reproduce the frozen rates exactly, and
Theorem 3.1 proves conic containment.  Exact factorization makes the three
primitive coordinate cubics irreducible and pairwise nonassociate, hence
pairwise coprime.  The radical decomposition follows by the same triangular
Gröbner-basis certificate used in (21)--(23).  In the frozen case, the
degree-fifteen eliminant is independently certified irreducible by its
reduction modulo the prime $19$.  The exact v1 verifier reconstructs every claim from
the directed reaction table.  $\square$

At $x_0=(3/2,1/2,1)$, the compatibility class is all of
$\mathbb R_{>0}^3$, and (7) on $(-1,1)$ gives infinitely many distinct
positive equilibria in that class.  The continuum is genuinely height two:
all coordinates lie in $(L,Q)$, but their gcd is one.

## 7. Transverse stability of the frozen ellipse

This section concerns $F^0$, not the clean specialization.  Let
$J(t)=DF^0(x(t),y(t),z(t))$.  Differentiating
$F^0(x(t),y(t),z(t))=0$ shows that the tangent direction is a zero
eigenvector.  Write the other two eigenvalues as
$\lambda_1(t),\lambda_2(t)$.

**Theorem 7.1 (exact transverse classification).**
There are exactly two real numbers

\[
\alpha\in(-4,-3),\qquad \beta\in(9/10,1)
\tag{29}
\]

at which normal hyperbolicity is lost.  The finite-$t$ portion of the
ellipse is normally attracting for

\[
\alpha<t<\beta,
\]

and is transversely saddle-type for $t<\alpha$ or $t>\beta$.  At each of
$\alpha,\beta$, one transverse eigenvalue is zero and the other is strictly
negative.  The point omitted by the affine parameter $t\in\mathbb R$,
namely the limit $t=\infty$, is also saddle-type.

*Proof.*  Exact characteristic-polynomial reduction gives

\[
\det(\lambda I-J(t))
=\lambda\bigl(\lambda^2-\tau(t)\lambda+\pi(t)\bigr),
\tag{30}
\]

where

\[
\tau(t)=-\frac{8T(t)}{d(t)^2},
\qquad
\pi(t)=-\frac{6272N(t)}{d(t)^4},
\tag{31}
\]

with

\[
T(t)=5399367t^4+1602005t^3+11579010t^2+1602005t+6979911
\tag{32}
\]

and

\[
\begin{aligned}
N(t)={}&5730530769t^8+20026244073t^7+29613209084t^6\\
&+118245415239t^5-38238695578t^4+127692520263t^3\\
&-127590858244t^2+10579139049t-79465564719.
\end{aligned}
\tag{33}
\]

The transverse discriminant is

\[
(\lambda_1-\lambda_2)^2
=\frac{64E(t)}{d(t)^4},
\tag{34}
\]

where

\[
\begin{aligned}
E(t)={}&31399532062137t^8+25149913538286t^7
+139213446954293t^6\\
&+100751092465458t^5+199590946186248t^4
+109518436416306t^3\\
&+114191722124597t^2+26510727150318t
+17568656198073.
\end{aligned}
\tag{35}
\]

Exact Sturm counts give no real roots for $T$ or $E$; evaluation at zero
shows both are positive on $\mathbb R$.  Thus the trace is always negative
and the two transverse eigenvalues are real and distinct.

The same exact Sturm procedure gives precisely two real roots of $N$, one
in each interval (29) and none elsewhere.  Define these roots to be
$\alpha,\beta$.  The sign checks

\[
N(-4)>0,\quad N(-3)<0,\quad N(9/10)<0,\quad N(1)>0
\]

show that $N<0$ between the roots and $N>0$ outside.  Hence
$\pi>0$ on $(\alpha,\beta)$ and $\pi<0$ outside.  Negative trace,
positive product, and real roots give two negative transverse eigenvalues on
the inner interval; negative product gives one eigenvalue of each sign on the
outer intervals.  At a root of $N$, equation (30) has transverse roots
$0$ and $\tau<0$.  Finally, the leading coefficients in (31)--(35) give
$\pi(\infty)<0$, proving saddle type at the omitted point.  $\square$

For orientation only,

\[
\alpha\approx-3.8135049145,
\qquad
\beta\approx0.9130496953.
\]

These decimals play no role in the proof.  On the interval $(-1,1)$ used
to display the v1 continuum, the normally attracting part is
$(-1,\beta)$, the point $\beta$ is nonhyperbolic, and
$(\beta,1)$ is saddle-type.

## 8. Why the mechanism is genuinely height two

For every rate vector in the family,

\[
F_i\in(L,Q).
\]

For the two exact specializations, no nonconstant polynomial divides all
three coordinates.  Consequently their equilibrium continuum is not
obtained by multiplying a smaller vector field by a common scalar
polynomial.  In addition:

- the stoichiometric class is three-dimensional, not a plane on which the
  field vanishes identically;
- all species occur, and reaction differences span all three directions;
- the coordinate fields are not artificial duplicates;
- the vector fields are nonzero off the conic; and
- the Jacobian has rank two at $(3/2,1/2,1)$ for both specializations.

Since $(L,Q)$ is a height-two prime and the coordinate gcd is one, the
steady ideal has height exactly two.  The equilibrium conic is therefore an
actual irreducible component, not merely a sampled subset of a hidden
hypersurface.

## 9. Minimality and structural obstructions

### 9.1 Three species are necessary

No one- or two-species system can have a positive-dimensional equilibrium
continuum in one compatibility class while retaining coordinate gcd one.  In
one species, a positive-dimensional zero set forces the single coordinate
polynomial to vanish identically.  In two species:

- if $\dim S=1$, all reaction vectors are collinear, so $F=vf(x,y)$ for a
  fixed vector $v$ and scalar polynomial $f$;
- if $\dim S=2$, a positive-dimensional common zero set gives a height-one
  prime over the steady ideal, and factoriality of
  $\mathbb Q[x,y]$ supplies a nonconstant common divisor.

Thus three species are globally minimal for the stated phenomenon.

### 9.2 One linkage class forces full rank in three species

Suppose a three-species, one-linkage network has $\dim S=2$.  Let a primitive
integer vector $w$ span $S^\perp$.  Connectivity makes
$w\cdot y=m$ constant over all complexes.  The torus action

\[
T_\rho(x_1,x_2,x_3)
=(\rho^{w_1}x_1,\rho^{w_2}x_2,\rho^{w_3}x_3)
\]

satisfies $F_i(T_\rho x)=\rho^mF_i(x)$.  Its infinitesimal direction at a
positive point $p$ has inner product

\[
\sum_iw_i^2p_i>0
\]

with the compatibility-class normal $w$, so it is transverse to the class.
A one-dimensional equilibrium stratum in one class therefore sweeps out a
two-dimensional equilibrium set.  The steady ideal then has height at most
one (unless the whole field is zero), and factoriality of
$\mathbb Q[x,y,z]$ forces a common irreducible divisor.  Rank one is already
excluded by collinearity.  Hence full rank is necessary under the
one-linkage hypothesis.

### 9.3 Deficiency and a global five-complex bound

Write $m$ for the number of active complexes, $\ell$ for the number of
linkage classes, $s=\dim S$, and $\delta=m-\ell-s$.  Every weakly reversible
target system has $\delta\geq1$.  Here is a direct proof.  Let $Y$ be the
complex matrix, let $A_\kappa$ be the kinetic Laplacian, and let $H$ be the
subspace of vectors whose coordinates sum to zero separately on each linkage
class.  Then $Y(H)=S$ and

\[
\delta=\dim\ker(Y|_H).
\]

If $\delta=0$, the equilibrium identity
$YA_\kappa\Psi(x)=0$ and $A_\kappa\Psi(x)\in H$ imply
$A_\kappa\Psi(x)=0$: every positive equilibrium is complex-balanced.
Weak reversibility makes the kernel of each linkage Laplacian
one-dimensional and positive.  Hence two positive equilibria $x,x'$ have
proportional monomial vectors on each linkage class, giving

\[
\log x-\log x'\in S^\perp.
\]

If they lie in one compatibility class, then $x-x'\in S$, and strict
monotonicity of the logarithm yields

\[
0=(x-x')\mathbin\cdot(\log x-\log x')
=\sum_i(x_i-x_i')(\log x_i-\log x_i'),
\]

whose summands are nonnegative and vanish only when $x_i=x_i'$.  Thus a
deficiency-zero weakly reversible system has at most one positive equilibrium
per class and cannot have the target continuum.

Now $s\geq2$ by Section 9.1 and $\delta\geq1$, so $m\geq4$.  Equality would
force $(m,\ell,s,\delta)=(4,1,2,1)$, which Section 9.2 excludes.  Therefore
every three-species weakly reversible realization of the target, even with
multiple linkage classes, has at least five complexes.  Under one linkage it
must also have $s=3$ and $\delta=m-4\geq1$.

The construction uses ten complexes, ten reversible pairs, maximum complex
degree three, and deficiency

\[
10-1-3=6.
\]

No claim that these complex, reaction, or deficiency counts are globally
minimal is made.

## 10. Relation to earlier work and scope

The construction and exact verifier were completed before the targeted
literature audit.  Boros, Craciun, and Yu constructed weakly reversible
systems with continua of positive equilibria and explicitly asked whether
such a continuum can occur without a coordinate common factor [BCY20].  Their
examples use a common-factor hypersurface.  Their displayed parametrization
also contains a positive-dimensional fixed-support family preserving the same
curve, so rate flexibility by itself is not new; every member of that family
retains the displayed common scalar factor.  The systems here answer their
question by a height-two prime component and add a fixed-support family that
is geometrically gcd one on a nonempty Zariski-open subset.

Feliu, Henriksson, and Pascual-Escudero prove generic-finiteness results for
steady-state varieties and revisit fine-tuned common-factor examples
[FHP26].  Those results concern generic changes in ambient rate and total
parameters.  They do not preclude the exact codimension-sixteen linear family
inside the twenty-dimensional fixed-support rate space found here.

A narrow primary-source audit through 1 August 2026 found no earlier weakly
reversible fixed-support positive rate family preserving a continuum in one
compatibility class while being generically free of a coordinate common
factor within that family.  Thus, to our knowledge, this is the first explicit
example with that conjunction.  The four-dimensional family has codimension
sixteen in ambient rate space, so the statement is relative rather than a
claim of robustness under arbitrary rate perturbations.  This is a
conservative audit conclusion, not an exhaustive universal priority claim.

## 11. Exact verification

Four exact replay layers support the claims.

1. The frozen verifier reconstructs the original network, conic identities,
   gcd, graph, stoichiometry, and radical decomposition.
2. The family verifier reconstructs the canonical $21\times20$ remainder
   matrix, rank minor, integer-vector kernel basis, positive cone, and
   homogenized gcd-one witness.
3. The strengthening verifier reconstructs the clean field and radical
   decomposition, performs the bounded integer enumeration, derives the
   characteristic polynomial, and executes all Sturm counts.
4. A separate 993-line v2 audit independently reconstructs the family matrix,
   both rate specializations, both radical decompositions, the two integer
   optima, and hand-built Sturm chains, then checks a frozen machine-readable
   result file.

Appendix B gives one command that runs all four layers and additional
cross-checks.  All polynomial identities use exact rational arithmetic.  The
decimal approximations in Section 7 are explicitly non-evidentiary.

Generative-AI systems were used substantively in discovery, exact
computation, adversarial review, verifier development, and manuscript
preparation.  The named human author accepts responsibility for the released
claims and artifacts.  Neither exact replay nor public timestamping is a
substitute for independent expert review.

## References

**[BCY20]** B. Boros, G. Craciun, and P. Y. Yu, “Weakly Reversible
Mass-Action Systems With Infinitely Many Positive Steady States,” *SIAM
Journal on Applied Mathematics* 80 (2020), 1936--1946.
[doi:10.1137/19M1303034](https://doi.org/10.1137/19M1303034).

**[FHP26]** E. Feliu, O. Henriksson, and B. Pascual-Escudero, “The Generic
Geometry of Steady State Varieties,” *SIAM Journal on Applied Algebra and
Geometry* 10 (2026), 519--548.
[doi:10.1137/25M1731289](https://doi.org/10.1137/25M1731289).

\appendix

## Appendix A. Complete directed rate tables

The rows below use the directed order (9).  The v1 and clean columns are two
distinct exact members of the same family; they are not combined in one
system.

| $j$ | directed reaction | frozen v1 rate | clean rate |
|---:|:---|---:|---:|
| 0 | $0\to1$ | 845740 | 1160 |
| 1 | $1\to0$ | 7732494 | 10296 |
| 2 | $0\to4$ | 702464 | 976 |
| 3 | $4\to0$ | 3920 | 23 |
| 4 | $0\to6$ | 437290 | 560 |
| 5 | $6\to0$ | 4380128 | 5977 |
| 6 | $1\to7$ | 1405575 | 1800 |
| 7 | $7\to1$ | 5600 | 25 |
| 8 | $2\to4$ | 706384 | 1629 |
| 9 | $4\to2$ | 900816 | 1237 |
| 10 | $2\to7$ | 1518755 | 1 |
| 11 | $7\to2$ | 6873328 | 9152 |
| 12 | $2\to9$ | 3920 | 653 |
| 13 | $9\to2$ | 896896 | 1214 |
| 14 | $3\to4$ | 3863552 | 5368 |
| 15 | $4\to3$ | 3920 | 1 |
| 16 | $5\to9$ | 3863552 | 5368 |
| 17 | $9\to5$ | 15680 | 70 |
| 18 | $8\to9$ | 4346496 | 6039 |
| 19 | $9\to8$ | 658560 | 915 |

The clean vector is primitive because it contains entries equal to one.  Its
maximum and sum are $10296$ and $52464$.  The frozen vector has maximum
$7732494$ and sum $39165070$.

## Appendix B. Reproduction commands

In the released archive, run

```text
./reproduce.sh
```

to create the locked local environment and replay every exact layer.  From a
repository checkout with the dependencies already installed, the combined
wrapper is

```text
.venv/bin/python weakly_reversible_continuum_no_common_factor/manuscript_v2_draft/verify_v2_claims.py
```

to replay the v1, family, clean-rate, integer-optimality, radical, and
stability checks.  To compile this manuscript to PDF, run

```text
sh weakly_reversible_continuum_no_common_factor/manuscript_v2_draft/build_pdf.sh
```

The build command only renders the manuscript; it does not create a release,
DOI, or external publication.
