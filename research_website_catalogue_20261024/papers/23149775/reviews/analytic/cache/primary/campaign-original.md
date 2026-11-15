# k403,b: the focal pedal–antipedal area product

**5100021 / AMR-050-0021. Complete source-matched candidate, author turn 1.
Independent review pending.** Classical and shared campaign inputs are
credited below; no novelty or priority claim is made.

## 1. Exact statement and real domain

Let $E$ be a noncircular ellipse with semiaxes $a>b>0$, with a fixed
strictly nested nondegenerate confocal elliptical caustic. Let $P_i$ run
through a primitive billiard orbit of least period $N\equiv0\pmod4$,
including the primitive star winding classes. Fix either original focus $F$.

The pedal vertices are the perpendicular feet from $F$ to the original
chord side lines $P_iP_{i+1}$. The antipedal vertices are intersections of
consecutive lines

$$
 \ell_i(F)=\{X:(P_i-F)\cdot(X-P_i)=0\}.                         \tag{1}
$$

All areas are ordered signed shoelace areas. Denote the pedal area by $A_F$
and the antipedal area by $A_F^*$. Neither construction is made from the
outer tangent polygon or the inner contact polygon.

**Theorem.** All real intersections (1) are finite. The product

$$
                         A_F(w)A_F^*(w)
$$

is independent of the orbit phase $w$. It has the same value at the two
foci. The pedal area is strictly positive for positive traversal; the
antipedal area may have either sign or be identically zero. No division by
either area is required. Reversal negates both signed areas and preserves
the product.

Both original sources agree with the pinned target: Table 5, k403,b,
$A_MA_M^*$, $N\equiv0\pmod4$, $M=f_1,f_2$. They are arXiv
2004.12497v11 (29 October 2020), printed p. 7, and the final *Fifty New
Invariants*, Arnold Mathematical Journal 7 (2021), printed p. 348. The
origin/odd entry is the different row k403,a. There is no source correction
to the pinned focal target; the initial assignment shorthand was corrected
against the actual sources before this proof attempt.

## 2. Coordinates, periods and credit

Scale the caustic major semiaxis to 1. A uniform rescaling multiplies the
product by the fourth power of that scale and does not affect invariance.
Put

$$
 0<k<1,\quad k'=\sqrt{1-k^2},\quad K=K(k),\quad K'=K(k'),
 \quad v=\frac{2K\tau}{N},\quad\delta=2v,
$$

where $0<\tau<N/2$ and $\gcd(\tau,N)=1$. Use modulus $k$ in all Jacobi
functions and abbreviate

$$
 s=\operatorname{sn}v,\quad c=\operatorname{cn}v,\quad
 d=\operatorname{dn}v,\quad a=d/c,\quad b=k'/c.
$$

Stachel's published Theorem 4.3 and equation (4.9), p. 1614, give

$$
 P(u)=(-a\operatorname{sn}u,b\operatorname{cn}u),\quad
 P_i(w)=P(w+i\delta),\quad F_\pm=(\pm k,0).                    \tag{2}
$$

The contact of chord $P_iP_{i+1}$ with the caustic has parameter
$x=w+v+i\delta$ and coordinates
$(-\operatorname{sn}x,k'\operatorname{cn}x)$.

Write $N=2m$. Then $m$ is even, $\tau$ is odd, and
$\gcd(\tau,m)=1$. Opposite vertices are paired by central inversion since
$m\delta=2K\tau\equiv2K\pmod {4K}$. Every cyclic area considered here has
real periods $2K$ and $\delta$, hence real period

$$
                         h=2K/m.                              \tag{3}
$$

All complex dot products below are bilinear, not Hermitian.

The standard Jacobi addition, pole, period and derivative formulas are the
ones in DLMF §§22.4, 22.8 and 22.13. The compact-torus trace framework and
original-pedal argument have prior campaign treatments in k203,a / PR203,
with shared input from k203,b / PR204, and k204 / PR250. Their method is
credited; the exact focal and parity specialization is proved below.

During this turn the parallel k404 / 5100022 packet independently supplied
the same focal antipedal vertex formula and its evenness/anti-periodicity
argument. Its frozen proof hash at coordination was
`b8edd78d03dac33a7be77837649eef7a8558900b3499774725174836fa54d462`.
The overlapping even-period antipedal lemma is explicitly shared mathematical
input, reproduced here with all hypotheses. That coordination is not counted
as independent review. k404 has a different, $2\pmod4$ ratio target; its
final parity conclusion is not relabeled as the present product theorem.

## 3. Actual focal antipedal vertices and pole completeness

First take $F=F_+$. For the chord with midpoint parameter $x$, write

$$
 S=\operatorname{sn}x,\quad C=\operatorname{cn}x,\quad
 D=\operatorname{dn}x,\quad
 L=1-k^2s^2S^2,\quad H=1-2k^2s^2+k^2s^4.
$$

The intersection of the two actual lines (1) at $P(x-v),P(x+v)$ is

$$
 R_x(x)=-\frac{HS+k(c^2-d^2S^2)}{c^2L},\qquad
 R_y(x)=\frac{C[2k'^2-H(1+kS)]}{k'c^2L}.                       \tag{4}
$$

This formula can be obtained directly from Cramer's rule. Use

$$
 \operatorname{sn}(x\pm v)=\frac{Scd\pm sCD}{L},\qquad
 \operatorname{cn}(x\pm v)=\frac{Cc\mp SsDd}{L}.
$$

Substitute those endpoints into (1), and reduce using
$C^2=1-S^2$, $D^2=1-k^2S^2$, $c^2=1-s^2$, $d^2=1-k^2s^2$.
The apparent extra focal factor $1+kS$ cancels. The exact checker verifies
both original line incidences as polynomial identities modulo these
relations; no numerical root test is used to obtain (4).

The determinant of the two line normals is

$$
 \det(P(x-v)-F,P(x+v)-F)
       =\frac{2bs d D(1+kS)}{L}
       =\frac{2k's d D(1+kS)}{cL}.                            \tag{5}
$$

The second expression substitutes
$b=k'/c$. For real $x$, all factors except the displayed positive
constants are positive as well: $D>0$, $1+kS>0$, and $L>0$. Thus
the intersections are finite. Geometrically, the focus is inside the caustic,
so no tangent chord passes through it.

For complex $x$, (4) has only possible nonremovable poles at the zeros of
$L$. On the lattice $2K\mathbb Z+2iK'\mathbb Z$, these are

$$
                         x=iK'\pm v.                          \tag{6}
$$

Indeed, $\operatorname{sn}(iK'+z)=1/(k\operatorname{sn}z)$.
The two roots are distinct and simple: there $S=\pm1/(ks)$, while $C,D$
are nonzero because $0<k,s<1$. Completeness follows because `sn²` has one
double pole on that lattice and thus degree two. At a common pole of `sn`
and `cn`, the numerators in (4) have order at most two, as does $L$, and
the leading denominator coefficient is nonzero. Those apparent singularities
are removable. Each $R(x)$ therefore has at most simple poles at (6).

Define the meromorphic antipedal area

$$
 B(w)=\frac12\sum_i\det(R(w+v+i\delta),R(w+v+(i+1)\delta)).     \tag{7}
$$

It has at most double poles. By (6), their locations are among
$w=iK'-j\delta$, modulo $2K,2iK'$. On the reduced torus with periods
$h,4iK'$, this is exactly the allowed pair of classes $iK'$ and $3iK'$.
No claim that those poles or the resulting area must be nonzero is needed.

## 4. Double-pole cancellation, uniformly including N=4

Central inversion interchanges the foci. Because it is a cyclic relabeling
of this even orbit, the two focal antipedal areas agree. Reflection in the
$y$-axis maps $P(w)$ to $P(-w)$, interchanges foci, and reverses the
cyclic traversal. Reflection and reversal each negate signed area. Thus

$$
                             B(-w)=B(w).                       \tag{8}
$$

The imaginary Jacobi shift $2iK'$ fixes `sn` and negates `cn`. It is
reflection in the $x$-axis on (2), fixes $F_+$, and retains cyclic order.
The rational construction (1) consequently gives

$$
                    B(w+2iK')=-B(w).                           \tag{9}
$$

These identities extend meromorphically from the nonsingular domain, using
the bilinear dot product in the complexified line equations.

At $p=iK'$, (8)–(9) imply

$$
                         B(p+z)=-B(p-z).
$$

Its Laurent expansion there has only odd powers. Since (7) gives pole order
at most two, the possible double-pole coefficient vanishes. The same holds
at every translate and at the other imaginary row. All poles of $B$ are
therefore at most simple.

This includes $N=4$: every antipedal vertex can be singular at once, but
each has pole order at most one, so each area summand still has order at most
two. The global odd-germ argument removes the double coefficient without
assuming separated pairs of singular indices. An independent local check is
also available: at an original-vertex pole, the two adjacent antipedal
residues are interchanged with their negatives at the antipodal original
pole, so the two double coefficients cancel. Edges incident to a finite
original vertex have parallel singular residues. The proof does not rely on
omitting any cyclic edge in the four-period case.

## 5. The two complementary area traces

Set

$$
                     T(w)=\sum_{j=0}^{N-1}\operatorname{dn}(w+j\delta).
                                                                    \tag{10}
$$

It has real period $h$, imaginary period $4iK'$, and anti-period
$2iK'$. On that compact torus it has exactly two simple poles, at $iK'$
and $3iK'$. At the first, the $j=0,m$ terms have identical nonzero
residues and add. The other real translates are distinct before quotienting;
there is no residue cancellation.

Match one residue of $B$ by a scalar $b_F T$. Anti-periodicity matches
the other. The difference is holomorphic on the compact torus and is
constant, while (9) forces this constant to be zero. Hence

$$
                         A_F^*(w)=B(w)=b_F T(w).                \tag{11}
$$

The constant $b_F$ is real, the same for the two foci, and may be zero.
For reference, the ordinary original-orbit area is
$A(w)=absc\,T(w)/d$, by the Jacobi addition identity for the two endpoint
`dn` values. Thus (11) is the shared even-period proportionality of focal
antipedal area to original area.

For the pedal, the actual tangent line to the caustic at parameter $x$ has
normal $n=(-S,C/k')$ and equation $n\cdot X=1$. Its foot from $F_+$ is

$$
 q(x)=F_++\frac{1-n\cdot F_+}{n\cdot n}n
       =\left(\frac{k-S}{1-kS},\frac{k'C}{1-kS}\right).          \tag{12}
$$

The possible poles of $q$ have order at most two and lie where
$\operatorname{sn}x=1/k$, a subset of the translates of $r=K+iK'$.
Common Jacobi poles are removable in (12). Near $r$, the quarter-shift
identities are

$$
 \operatorname{sn}(r+z)=\frac{\operatorname{dn}z}{k\operatorname{cn}z},
 \qquad \operatorname{cn}(r+z)=-\frac{ik'}{k\operatorname{cn}z}.
$$

They are even in $z$. The neighbors at $r\pm\delta$ are regular because
$0<\delta<2K$. The two incident area terms combine as

$$
 \frac12\det\big(q(r+z),q(r+z+\delta)-q(r+z-\delta)\big).
$$

The second vector is odd and holomorphic in $z$, so the area has at most a
simple pole there. The same reasoning applies at every possible singular
vertex; no adjacent two-pole product occurs. This also covers $N=4$, where
the neighboring formula may have removable common-Jacobi expressions.

The cyclic pedal area as a function of the contact phase has period $h$,
anti-period $2iK'$, and the same two possible simple poles as $T(x+K)$.
The identical compact-torus residue argument yields a real constant $p_F$
such that, in the original vertex phase,

$$
                         A_F(w)=p_F T(w+K+v).                  \tag{13}
$$

No division by a pedal or antipedal area was used in obtaining either trace.
The opposite focus gives the same area and constant by central inversion.

## 6. The required 0-modulo-4 product

Since $m$ is even and $\tau$ is odd,

$$
                  K+v=\frac{m+\tau}{2}h\equiv h/2\pmod h.
$$

Thus (13) is $A_F(w)=p_F T(w+h/2)$, rather than a multiple of $T(w)$.
The parity shift cannot be dropped or borrowed from k404's ratio case.

The trace $T$ is even, by reindexing the sum in (10). At
$z_0=h/2+iK'$, it is regular and

$$
 T(z_0)=T(-z_0)=T(z_0-h-2iK')=-T(z_0),
$$

so it vanishes. Anti-periodicity gives a second zero at $z_0+2iK'$.
There are precisely two zeros counted with multiplicity, because the trace
has exactly two simple poles on the compact torus. The zeros just found are
distinct and therefore simple. Consequently

$$
                         T(w)T(w+h/2)=\mathcal C               \tag{14}
$$

has no poles and is constant. On the real line `dn` is positive, so
$\mathcal C>0$.

Combining (11), (13) and (14) proves the source product:

$$
                         A_F(w)A_F^*(w)=p_F b_F\mathcal C.
$$

It remains valid if $b_F=0$. Restoring a caustic scale $\alpha$ multiplies
the constant by $\alpha^4$. This establishes the full specified target.

## 7. Positivity, degeneracies and checks

The real focus lies strictly inside the caustic. For every contact phase,
$q(x)-F$ is a positive multiple of the outward caustic normal. The normal
angle increases strictly and gains $\pi$ in parameter length $2K$.
Thus any consecutive step $0<\delta<2K$ turns that normal by an angle
strictly between 0 and $\pi$. Every consecutive determinant of the vectors
$q_i-F$ is positive, including for a star winding class. Translating a
shoelace polygon does not change its area, so $A_F>0$ and $p_F>0$.

Antipedal self-intersections and zero signed area cause no defect in the
product theorem. All vertices remain finite by (5); there is no centroid or
raw quotient to define at a zero. The theorem does not cover degenerate or
hyperbolic caustics, a moving center, unsigned lobe areas, or repeated
lower-period orbits used to change parity.

As a direct exact low-period check, take $a=2,b=1$, focus $(\sqrt3,0)$,
and the common four-period caustic with semiaxes $4/\sqrt5,1/\sqrt5$.
The axis diamond has pedal/antipedal areas $32/25,8$; the axis-aligned
billiard rectangle with vertices $(\pm4/\sqrt5,\pm1/\sqrt5)$ has areas
$8/5,32/5$. Both products are $256/25$. These are direct original-line
calculations, not a relabeled outer-polygon construction.

The exact checker verifies (4), (5), (12), reflection/period arithmetic and
low-period controls. Separately labeled high-precision diagnostics use direct
line intersections and side-line projections for real and complex phases.
They supplement the analytic argument and do not certify the all-period
statement by finite sampling. The complete proof requires a separate
uninvolved adversarial review before any PR or status promotion.
