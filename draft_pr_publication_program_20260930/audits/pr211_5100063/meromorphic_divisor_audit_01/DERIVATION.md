# Independent reconstruction of the outer focal-inverse product

Author: independent meromorphic/divisor audit family, PR211/5100063. This is an initial scientific source-body audit, subject to Root integration. It is not an acceptance of a manuscript, archive, release, priority claim, or earlier review verdict. Claim and falsification plan were frozen in `CLAIM_FREEZE.json` before custody acceptance or previous review reports were read. No previous scientific review report or other family's mathematical conclusion was used.

## 1. Claim and published input

Let the billiard ellipse have semiaxes (a>b>0), original foci (f_\pm=(\pm c,0)), and a strictly nested nondegenerate confocal elliptical caustic with semiaxes (\alpha>\beta>0). For an odd least period (N\geq3), choose the orientation with coprime turning number (0<\tau<N/2). The outer polygon has vertices given by intersections of the tangents at consecutive billiard vertices. Invert those **outer vertices** in unit circles about each **original focus**, and connect consecutive inverted vertices by straight segments. Let (B_\pm) be the signed shoelace areas. The claim is that (B_+B_-) is independent of the phase of this fixed Poncelet family.

The directly read primary table is Reznik--Garcia--Koiller, arXiv:2004.12497v11, Table 10, printed p12: the odd product is (k904,a), with primed dagger areas. Their Section 3.9, pp9--10, defines the vertex inversions and the primed outer symbols; Section 2, p3, defines signed cross-product area. The same product is (k808,a) in v10, Table 9, p11. These are source-identification statements, not a priority conclusion. Complete relevant table/definition pages were inspected as text and as rendered PDF pages; private source hashes and precise reading limits are in `PRIMARY_READINGS.md` and `PRIVATE_PRIMARY_MANIFEST.json`.

The published Stachel Theorem 4.3/(4.9), p1614, supplies the canonical parameter, with modulus equal to the caustic eccentricity. Put

\[
k=c/\alpha\in(0,1),\quad k'=\beta/\alpha=\sqrt{1-k^2},\quad
v=2K\tau/N\in(0,K),\quad \delta=2v,
\]
\[
P(w)=(-a\,\operatorname{sn}w,b\,\operatorname{cn}w),\qquad
a=\alpha\frac{\operatorname{dn}v}{\operatorname{cn}v},\qquad
b=\frac{\alpha k'}{\operatorname{cn}v}.
\]

All Jacobi functions below have modulus (k); numerical libraries use parameter (m=k^2). Here (K=K(k)>0), (K'=K(k')>0), and (p=iK'). The published adjacent p1613 prints an erroneous alternating sign for the real (2K) shift of dn. It is not used: dn has real period (2K). The correct periods, shifts, addition identities, and derivatives are the standard NIST DLMF 22.4, 22.8, 22.13 facts, read directly. Theorem 4.3 and the independently checked identities are unaffected by the unused typo.

The coordinate input covers the whole stated domain. Indeed, for any strictly nested confocal pair, (\beta/b\in(0,1)) gives a unique (v\in(0,K)) with (\operatorname{cn}v=\beta/b), and confocality then gives the formula for (a\). The real curve (P(w)) is injective modulo (4K); closure with least period (N) means (N\delta=4K\tau) with (gcd(N,\tau)=1). Reversal replaces the rotation number by (1-\tau/N), so the indicated orientation covers every primitive star as well as convex orbits.

## 2. Tangents, outer points, and focal distance

Write

\[
h=\operatorname{sn}v>0,\ C=\operatorname{cn}v>0,\ d=\operatorname{dn}v>0,
\quad t=h^2\in(0,1),\ q=C^2=1-t,
\]
\[
U=1-2k^2t+k^2t^2,\quad V=1-2t+k^2t^2,\quad W=1-k^2t^2>0.
\]

For the centered parameter (u), set (s=\operatorname{sn}u), (e=\operatorname{cn}u), (n=\operatorname{dn}u), and (D=1-k^2t s^2). The addition identities explicitly give

\[
s_\pm:=\operatorname{sn}(u\pm v)=\frac{sCd\pm h e n}{D},\qquad
c_\pm:=\operatorname{cn}(u\pm v)=\frac{eC\mp s h n d}{D}.
\]

The tangent at (P(z)) is (-X\operatorname{sn}z/a+Y\operatorname{cn}z/b=1). Substitution of

\[
Q(u)=(-A\operatorname{sn}u,B\operatorname{cn}u),\qquad
A=\frac{ad}{C}=\frac{\alpha d^2}{q},\quad
B=\frac bC=\frac{\alpha k'}q
\]

satisfies both tangent equations because ((d/C)s s_\pm+(e/C)c_\pm=1). Moreover

\[
s_+c_--s_-c_+=\frac{2h C n}{D},
\]

so the magnitude of the tangent-coefficient determinant on the real axis is (2h C n/(abD)>0). This proves the finite intersection formula, rather than presuming the parametrized outer locus. The identities hold meromorphically elsewhere by continuation.

The real outer axes are positive, and (A>a), (B>b), since (d^2-C^2=k'^2t>0). Thus every real (Q) lies strictly outside the original billiard ellipse: (Q_x^2/a^2+Q_y^2/b^2=(A/a)^2s^2+(B/b)^2e^2>1). Neither focus lies on this locus. The locus can have (A<B); no major-axis ordering is used.

Take (f=f_+=(\alpha k,0)). Its bilinear squared distance is

\[
H(u)=(Q_x-\alpha k)^2+Q_y^2
=\frac{\alpha^2}{q^2}(1+k s)(U+kV s).
\tag{2.1}
\]

An independent coefficient expansion gives (A^2-B^2=\alpha^2k^2V/q^2), (B^2+\alpha^2k^2=\alpha^2U/q^2), and (U+V=2qd^2), which prove (2.1). This continuation contains no complex conjugation. On the real line it is the actual Euclidean distance squared and is positive. Translating the inverse polygon by (-f) gives (J(u)=(Q(u)-f)/H(u)), without changing signed area.

## 3. Independent edge rationalization and normalization

Let (E(u)=\frac12\det(J(u-v),J(u+v))). The addition formulas give the particularly simple identities

\[
s_-+s_+=\frac{2sCd}{D},\qquad s_-s_+=\frac{s^2-t}{D}.
\]

Consequently

\[
(1+ks_-)(1+ks_+)=\frac{(d+kCs)^2}{D}.
\tag{3.1}
\]

Define

\[
L_0=\frac{U^2-k^2V^2t}{d},\qquad
L_1=\frac{V^2-U^2t}{C}.
\]

The second pair of factors expands as

\[
(U+kVs_-)(U+kVs_+)
=\frac{dL_0+2kUV C d\,s+k^2C L_1s^2}{D}
=\frac{(d+kCs)(L_0+kL_1s)}D.
\tag{3.2}
\]

The only mixed-coefficient identity required for the last equality is

\[
d^2(V^2-U^2t)+q(U^2-k^2V^2t)=2UVqd^2.
\]

It follows by polynomial expansion using (q=1-t), (d^2=1-k^2t). Thus (3.2) is not fitted to values of (u).

The translated un-inverted edge determinant, including its factor (1/2), is

\[
\begin{aligned}
T(u)&=\tfrac12\det(Q(u-v)-f,Q(u+v)-f)\\
&=\tfrac{AB}{2}(s_+c_--s_-c_+)+\tfrac{\alpha kB}{2}(c_--c_+)\\
&=\frac{\alpha B h d\,n(d+kCs)}{CD}.
\end{aligned}
\tag{3.3}
\]

Here (c_--c_+=2s h n d/D). Multiplying the two copies of (2.1) and using (3.1)--(3.2) yields

\[
H(u-v)H(u+v)=\frac{\alpha^4}{q^4}
\frac{(d+kCs)^3(L_0+kL_1s)}{D^2}.
\]

Dividing (3.3) by this expression proves the exact edge formula

\[
E(u)=C_0\frac{\operatorname{dn}u\,(1-k^2t\operatorname{sn}^2u)}
{(d+kC\operatorname{sn}u)^2(L_0+kL_1\operatorname{sn}u)},\qquad
C_0=\frac{B h d q^4}{\alpha^3 C}>0.
\tag{3.4}
\]

In particular the (q^4) normalization is correct. Its physical dimension is inverse length squared, as required for the area after unit inversion. The product has dimension inverse length to the fourth power. No area has been divided out.

## 4. Triple angle and real positivity

Double angle gives (operatorname{sn}2v=2hCd/W), (operatorname{cn}2v=V/W), (operatorname{dn}2v=U/W). Set

\[
Z=W^2-4k^2t^2 qd^2=W^2(1-k^2t\operatorname{sn}^22v)>0,
\]
\[
D_3=UW-2k^2tqV,\qquad C_3=VW-2td^2U.
\]

Applying addition to (2v+v) gives, without a sign choice or square-root ambiguity,

\[
\operatorname{dn}3v=\frac{dD_3}Z,\qquad
\operatorname{cn}3v=\frac{CC_3}Z.
\]

Direct polynomial expansion gives (U^2-k^2V^2t=d^2D_3) and (V^2-U^2t=qC_3). Therefore

\[
L_0=Z\operatorname{dn}3v>0,\quad L_1=Z\operatorname{cn}3v,
\quad L_0^2-k^2L_1^2=k'^2 Z^2>0.
\tag{4.1}
\]

For real (u), (d>|kC|), because (d^2-k^2C^2=k'^2>0). Similarly (4.1) gives (L_0>|kL_1|). Both denominator factors in (3.4) are strictly positive on the real line, as are dn, (D\geq1-k^2t>0), and (C_0). Thus

\[
E(u)>0\quad(u\in\mathbb R).
\tag{4.2}
\]

Since (0<3v<3K), (L_1=0) would require (3v=K), apart from the excluded endpoint (3K). But (v=K/3) would give (N=6\tau), which is impossible for odd (N). Thus (L_1\ne0) throughout the stated domain.

## 5. Full periods, critical fibers, and edge divisor

The correct Jacobi transformations are

\[
\begin{array}{c|ccc}
\text{shift}&\operatorname{sn}&\operatorname{cn}&\operatorname{dn}\\\hline
2K&-&-&+\\
2p&+&-&-
\end{array}
\]

so (E) has full periods (4K,4p) and **anti**-period (2p). The sn torus with lattice (4K\mathbb Z+2p\mathbb Z) is useful only for finding its fibers; (E) itself must not be treated as a function on that smaller torus. On the sn torus, sn has two simple poles (p,2K+p) and degree two. Its finite critical values are (\pm1,\pm1/k), from (\operatorname{sn}'=\operatorname{cn}\operatorname{dn}). For (0<k<1), the cn and dn zeros are simple and disjoint, so these are quadratic critical points.

Put (r_0=3K+p). The standard quarter-shifts give

\[
\operatorname{sn}(r_0+z)=-\frac{\operatorname{dn}z}{k\operatorname{cn}z},\quad
\operatorname{cn}(r_0+z)=\frac{i k'}{k\operatorname{cn}z},\quad
\operatorname{dn}(r_0+z)=i k'\frac{\operatorname{sn}z}{\operatorname{cn}z}.
\tag{5.1}
\]

The factor (d+kC\operatorname{sn}u) has its two zeros at (a_\pm=r_0\pm v) on the sn torus. They are distinct since (0<2v<2K<4K). The value (-d/(kC)) has magnitude strictly greater than (1/k), so both are noncritical and simple. Degree two makes this fiber list exhaustive.

By (4.1), the factor (L_0+kL_1\operatorname{sn}u) has its zeros at (b_\pm=r_0\pm3v). If distinct, these are also simple. Its sn value has magnitude at least (1/k), and equality requires (operatorname{sn}3v=0). In (0<3v<3K) this occurs exactly at (3v=2K). Likewise (b_+=b_-) modulo the sn lattice requires (6v=4K). The canonical condition (3\tau=N) and primitivity then give exactly (N=3,\tau=1). There are no other critical second fibers.

In this (N=3) case, (L_0=Z,L_1=-Z), and both (b_\pm) represent (K+p). The denominator factor (Z(1-k\operatorname{sn}u)) has a quadratic zero there. Indeed (operatorname{sn}=1/k), (operatorname{cn}^2=-k'^2/k^2\ne0), dn has a simple zero, and (operatorname{sn}''=k'^2/k\ne0). Its product with the numerator leaves a **simple pole**. Here (D=q\ne0), and the first factor is (d+C\ne0). This is an actual simple pole, and no second double principal part has been omitted.

The (a)- and (b)-fibers never meet: equality would require (2v) or (4v) to be a multiple of (4K), forbidden for (0<v<K). This statement compares the two root sets within one edge before taking the cyclic quotient.

At each common sn/cn/dn pole, write (zeta=u-u_0). Each Jacobi function has a simple pole. The numerator of (3.4) has order three and its denominator has order three, with nonzero leading coefficient because (k,C,L_1\ne0). Hence all such points are removable. At (u_0=p), (5.1)'s imaginary shift form gives (operatorname{dn}/\operatorname{sn}\to-ik), and the finite nonzero value is

\[
E(p)=\frac{i C_0t}{qL_1}.
\tag{5.2}
\]

The value at (2K+p) has the opposite sign; translates by (2p) also reverse sign. This explicit limit rules out a hidden pole or zero at the Jacobi poles.

For completeness, the edge zeros can also be fully classified. The (D)-factor has simple zeros at

\[
u=p\pm v,\quad 2K+p\pm v
\quad\text{modulo }4K\mathbb Z+2p\mathbb Z.
\tag{5.3}
\]

This follows from (operatorname{sn}(p+z)=1/(k\operatorname{sn}z)); the values (\pm1/(kh)) are noncritical since (h\in(0,1)). A point in (5.3) could meet the (a)-fiber only at (v=K/2), and could meet the (b)-fiber only at (v/K\in\{1/4,1/2,3/4\}). These are obtained by equating (\pm v\) to (3K\pm v) or (3K\pm3v) modulo (2K); the resulting nontrivial differences are (2v) or (4v) equal to an odd multiple of (K). None can satisfy (v/K=2\tau/N) with (N) odd. Thus no numerator (D)-zero cancels a denominator zero in this domain.

On the full (4K\)-by-(4p) torus, dn has four simple zeros: (K+p,3K+p) and their (2p) translates. They do not meet (5.3), where dn is nonzero. For odd (N\geq5), none meets either denominator fiber. Thus (E) has four double (a)-poles, four simple (b)-poles, four simple dn zeros and eight simple (D)-zeros: total pole and zero orders both twelve. For (N=3), the two positive-sn dn zeros become the two simple (b)-poles described above; the other two dn zeros remain, together with all eight (D)-zeros. The total orders are then ten on each side. These counts are supplementary checks of completeness; the cyclic proof only needs the pole bounds and positivity.

## 6. Exact double coefficients and cyclic cancellation

The quarter shifts in (5.1) give, at (a_\pm),

\[
\operatorname{dn}a_\pm=\pm i k'h/C,\quad
\operatorname{sn}'a_\pm=\mp\frac{k'^2 h}{kq},\quad
D(a_\pm)=V/q,
\]
\[
(L_0+kL_1\operatorname{sn})(a_\pm)
=L_0-dL_1/C=4k'^2tdW>0.
\]

The latter identity follows from (U^2-V^2=4k'^2tqd^2). Substituting into (3.4), the coefficient of ((u-a_\pm)^{-2}) is

\[
A_{2,\pm}=\pm\frac{iVq^2}{4\alpha^2k'^4tW}.
\tag{6.1}
\]

Here (V=W\operatorname{cn}2v\ne0): its only zero in (0<v<K) is (v=K/2), incompatible with odd (N). Thus the listed double poles really are double before summation, and their coefficients have exactly opposite signs. Independently, sn parity and periods give (operatorname{sn}(2r_0-u)=\operatorname{sn}u) and (operatorname{dn}(2r_0-u)=-\operatorname{dn}u), so

\[
E(2r_0-u)=-E(u),
\tag{6.2}
\]

which also forces the opposite coefficients. The explicit (6.1) checks the normalization and the sign mechanism.

Now form (F(u)=\sum_{j=0}^{N-1}E(u+j\delta)). The element (\delta=4K\tau/N) has order exactly (N) modulo (4K), by coprimality. At any candidate pole (u=a_+-j\delta), exactly one translated edge contributes the (a_+) double coefficient and exactly one contributes the (a_-) double coefficient, because (a_+-a_-=\delta). No multiplicity is lost under reindexing. Formula (6.1), or (6.2), cancels the quadratic terms. The remaining terms have order at most one.

The two (b)-positions satisfy (b_+=a_++\delta), (b_-=a_+-2\delta), so they yield the same cyclic pole classes. They contribute only simple terms. When (N=3), the two labels (b_\pm) are one point in each individual edge, already proved to be simple in Section 5; they must not be double-counted. They cannot create a quadratic term. Translates by (2p) obey the same cancellation with the overall opposite sign. This covers every class collision for every coprime odd (N).

The finite sum has periods (4K) and (\delta): the latter follows by cycling the index and using (N\delta=4K\tau). Bezout's identity for (N,\tau) then gives the full real period (L=4K/N). It retains anti-period (2p) and period (4p). On

\[
X=\mathbb C/(L\mathbb Z+4p\mathbb Z),\qquad R=r_0+v,
\]

the only possible poles of (F) are simple poles at (R) and (R+2p). They are distinct because (K',L>0). Additional smaller periods, if any, are not assumed in deriving these bounds.

**The all-poles-cancel case is impossible universally.** If neither candidate were a pole, (F) would be holomorphic on the compact torus (X), hence constant. The anti-period (F(u+2p)=-F(u)) would then force (F\equiv0). But (4.2) implies (F(u)>0) for real (u). Also anti-periodicity pairs the two candidate poles, so either both occur or neither occurs. Therefore both occur with order exactly one. This establishes the total pole order two without relying on any nonzero finite residue sample.

## 7. Zero divisor, half shift, and the opposite focus

Reindexing (6.2) gives

\[
F(2r_0-u)=-\sum_jE(u-j\delta)=-F(u).
\]

Since (2R=2r_0+\delta) and (\delta) is a period, (F(2R-u)=-F(u)). The reflection has four fixed classes on (X):

\[
R,\quad R+L/2,\quad R+2p,\quad R+L/2+2p.
\]

The first and third are the poles. The other two are holomorphic points, distinct from these poles and from each other. Oddness forces a zero at each. A nonzero meromorphic function on a compact torus has the same total zero and pole order: integrating its logarithmic derivative along a fundamental parallelogram avoiding the divisor cancels opposite sides and counts zeros minus poles. Thus these are precisely the two zeros and both are simple. This handles hidden multiple zeros, constant zero, and a possibly reduced divisor.

For (G(u)=F(u)F(u+L/2)), every pole of one factor meets a simple zero of the other and conversely. There are no remaining poles. Thus (G) is holomorphic on compact (X) and is a constant. It is a positive real constant, because both factors are positive at real (u).

The outer vertices for phase (w) are (Q(w+j\delta)). Their successive translated inverse edge area is (E(w+v+j\delta)), hence (B_+(w)=F(w+v)). Since (Q(u+2K)=-Q(u)), the translated inverse at (f_-) is the negative of the translated inverse at (f_+) of (Q(u+2K)). Central reflection has determinant (+1), so

\[
B_-(w)=B_+(w+2K)=F(w+v+2K).
\]

Finally (2K=NL/2\equiv L/2\pmod L) because (N) is odd. Consequently

\[
B_+(w)B_-(w)=F(w+v)F(w+v+L/2)
\]

is constant for every family in the stated domain. Reversal negates both signed sums and preserves their product. This concludes the universal argument, conditional only on the explicitly cited standard parametrization and Jacobi facts.

## 8. Limits, repetitions, and scope

For (k=0), the foci coincide and the proof by compact elliptic torus is replaced by an elementary rotation argument. A circular billiard of radius (a) with step (2v=2\pi\tau/N\in(0,\pi)) has outer vertices on radius (R_o=a/\cos v). Inversion gives radius (1/R_o), so (B_+=B_-=N\sin(2v)/(2R_o^2)), independent of phase. For fixed (\alpha,N,\tau), the strict-(k) formulas tend continuously to this circle value as (k\to0); the torus representation itself degenerates at the endpoint.

At (k\to1), (k'\to0), the caustic degenerates, (K\to\infty), and the inequalities using (k'^2>0) lose strictness. The theorem does not assert a uniform finite product or an extension at this endpoint. For fixed (k), (v\to0) approaches equality of the two confocal ellipses, and (v\to K) sends outer tangent intersections to infinity as (C\to0). Neither endpoint belongs to the theorem. With fixed (N,\tau), (v/K=2\tau/N) is fixed; the limits (v/K\to0,1) require varying the period/turning data. Thus these limits do not create omitted fixed-period cases. The finite computations include approaches from within the strict domain, explicitly without interval bounds.

A fixed (r\)-fold traversal of a least-period orbit repeats each signed shoelace sum (r) times. The product is multiplied by (r^2). An odd total traversal length can only repeat an odd least period an odd number of times. This scaling does not change least-period parity or prove a new primitive case.

The proof concerns straight joins of inverted outer vertices, not inverted whole-edge arcs, original-vertex inversions, pedal points, outer-locus-foci inversions, unsigned filled-star areas, hyperbolic caustics, or collapsed caustics. No historical novelty or absolute priority is inferred.

## 9. Reproducible controls and their evidential limit

`audit_math.py` is wholly authored for this audit and imports only preinstalled Sympy 1.14.0/mpmath 1.3.0 under Python 3.11.8. It performs 21 exact polynomial reductions, finite exact rational class controls, and finite 100-decimal-digit noninterval diagnostics. The algebra controls verify the displayed identities after clearing denominators and reducing (h^2=t,C^2=1-t,d^2=1-k^2t,e^2=1-s^2,n^2=1-k^2s^2,k'^2=1-k^2). Denominator nonvanishing in the real scope and local order arguments are proved above, not inferred from the symbolic solver.

The numerical geometry path solves the two tangent equations directly, performs Euclidean inversion, and sums actual ordered signed determinants. It is compared with the independently rationalized edge function. Cases include all coprime turns for listed odd periods, (N=3), primitive stars, eccentricities near zero and one, period/turning endpoint approaches, imaginary anti-periodicity, reflection, pole fibers, opposite principal parts, removable sn poles, and cyclic half-period zeros. These are diagnostics rather than interval validation or a substitute for the universal proof. `RUN_RECEIPT.json`, `SYMBOLIC_RESULTS.json`, `LATTICE_RESULTS.json`, and `NUMERIC_RESULTS.json` record exact bounds of the executed finite set.

Strongest verified claim: the stated universal signed-area product follows from the reconstruction above. No mathematical gap was found in the source-body meromorphic proof. Root must decide whether to accept this scientific family and must independently apply all package/publication gates; this audit does not do so.
