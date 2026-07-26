# Full symmetric monodromy throughout Gallagher's weighted-lift family

**First draft (UTC):** 2026-07-25T19:47:04Z
**First public release (UTC):** 2026-07-25T20:15:16Z
**Status:** theorem passed an independent hostile audit; priority remains
source-specific and the work is not peer reviewed.

## Statement

### Theorem

Let \(p\in\mathbb C[w]\) be any admissible seed in Gallagher's
weighted-lift construction, and suppose \(\deg p=d-1\ge2\).  Then the
associated Keller counterexample has generic degree \(d\) and geometric
monodromy group \(S_d\) in its natural action on the generic fibre.

Consequently, every symmetric group \(S_d\), \(d\ge3\), occurs as the
geometric monodromy group of a Keller counterexample
\(\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}\).

The candidate addition is family-wide: it applies to every admissible
Gallagher seed, not only to one example in each degree.

## 1. Gallagher's weighted lift and exact root recovery

Fix \(b,c\in\mathbb C^\times\).  An admissible seed is a polynomial
\(p\in\mathbb C[w]\) satisfying
\[
p(0)=0,\qquad p(1)=-c,\qquad \int_0^1p(s)\,ds=0,
\tag{1}
\]
and, with
\[
\kappa=\frac{p'(1)}c,
\]
the nondegeneracy condition \(\kappa\ne-2\).  Define
\[
q(0)=0,\qquad q'(w)=\frac{w\,p'(w)}c,\qquad
a=-\frac{1+\kappa}{2+\kappa}.
\tag{2}
\]
In source quotient coordinates put
\[
v=xy,\quad t=x^2z,\quad u=1+v,\quad
\gamma=1+av+bt,\quad w=u\gamma,
\]
\[
\beta=c+\frac{p(w)}{\gamma},\qquad
\alpha=u+\frac{q(w)}{\gamma^2}.
\]
Gallagher's map is
\[
F_p=(A,B,C)=
\left(\frac{\alpha}{x^2},\frac{\beta}{x},x\gamma\right).
\tag{3}
\]

The apparent divisions cancel.  Indeed, \(p(0)=0\) and the double zero
of \(q\) at zero first make \(\alpha,\beta\) polynomial in \(u,\gamma\).
The endpoint and integral conditions give
\(\beta(0,0)=\alpha(0,0)=0\) in the variables \((v,t)\), and the choice
of \(a\) gives \(\partial\alpha/\partial v(0,0)=0\).  Hence division by
\(x\) and \(x^2\) leaves polynomials.  Gallagher's Jacobian identity is
\[
\det JF_p=bc\ne0.
\tag{4}
\]

Set
\[
P=BC,\qquad Q=AC^2,\qquad
\Phi(w)=\int_0^w p(s)\,ds.
\]
Then
\[
P=c\gamma+p(w),\qquad Q=w\gamma+q(w).
\tag{5}
\]
The derivative identity in (2) gives
\[
\Phi(w)=wp(w)-cq(w),
\]
so eliminating \(\gamma\) from (5) yields the exact inverse equation
\[
\Phi(w)-Pw+cQ=0.
\tag{6}
\]

Conversely, a generic root \(w\) recovers the source rationally:
\[
\gamma=\frac{P-p(w)}c,\qquad
x=\frac C\gamma,\qquad
u=\frac w\gamma,\qquad v=u-1,
\]
\[
y=\frac vx,\qquad
t=\frac{\gamma-1-av}{b},\qquad z=\frac t{x^2}.
\tag{7}
\]
There is also a compact denominator certificate:
\[
\frac{d}{dT}\bigl(\Phi(T)-PT+cQ\bigr)\bigg|_{T=w}
=p(w)-P=-c\gamma.
\tag{8}
\]
Thus a root with \(\gamma=0\) would be a repeated root of the generic
inverse polynomial, which is impossible in characteristic zero.  After
also restricting to the generic open set \(C\ne0\), every denominator in
(7) is valid.  Denominator clearing has introduced no extra branch.  Since
\(\det JF_p\ne0\), the target coordinates are algebraically independent,
and
\[
\mathbb C(A,B,C)=\mathbb C(P,Q,C).
\tag{9}
\]
Writing \(K\) for this target field and \(L=\mathbb C(x,y,z)\), equations
(6)--(7) show
\[
L=K(w).
\tag{10}
\]
If \(\deg p=d-1\), then \(\deg\Phi=d\).  Equation (6) is irreducible over
\(\mathbb C(P,Q)\): in \(\mathbb C[P,T][Q]\) it is linear in \(Q\)
with unit leading coefficient \(c\), hence prime; it is primitive as a
polynomial in \(T\), so Gauss's lemma applies.  Therefore \([L:K]=d\).

## 2. Brink's theorem and family-wide monodromy

Brink's Theorem 13 states that, in characteristic not dividing
\(d(d-1)\), a monic degree-\(d\) polynomial with arbitrary fixed higher
coefficients and independent linear and constant coefficients has Galois
group \(S_d\).  After dividing (6) by the leading coefficient of
\(\Phi\), its linear and constant coefficients are independent affine
rescalings of \(P\) and \(Q\).  Hence
\[
\operatorname{Gal}\bigl(\Phi(T)-PT+cQ\,/\,\mathbb C(P,Q)\bigr)=S_d.
\tag{11}
\]
Adjoining the independent target coordinate \(C\) does not change the
splitting-field group.  Rational recovery (7) identifies the root field
with the extension induced by \(F_p\), proving
\[
\operatorname{Mon}(F_p)=S_d.
\tag{12}
\]
As \(d>1\), the generic fibre has more than one point, so \(F_p\) is a
Keller counterexample rather than an automorphism.  This proves the
theorem.

## 3. A simple seed and a direct Morse check

For each \(d\ge3\), take \(b=c=1\) and
\[
p_d(w)=\frac{2w-dw^{d-1}}{d-2}.
\tag{13}
\]
It obeys (1), has \(\kappa=-(d+1)\), and gives
\[
a=-\frac d{d-1},\qquad
q_d(w)=\frac{w^2-(d-1)w^d}{d-2}.
\]
Formula (3) becomes the explicit family
\[
u=1+xy,\qquad
\gamma=1-\frac d{d-1}xy+x^2z,
\]
\[
A_d=
\frac{(d-2)u+u^2-(d-1)u^d\gamma^{d-2}}{(d-2)x^2},
\]
\[
B_d=
\frac{(d-2)+2u-du^{d-1}\gamma^{d-2}}{(d-2)x},
\qquad C_d=x\gamma.
\tag{14}
\]
With
\[
U=(d-2)P,\qquad V=-(d-2)Q,
\]
the inverse equation (6) is
\[
f_d(T)=T^d-T^2+UT+V.
\tag{15}
\]

The lemma below is a direct special case of David Brink's Theorem 13 in
*On Alternating and Symmetric Groups as Galois Groups* (Israel J. Math.
142 (2004), 47--60): fixing all coefficients except the linear and constant
terms in a monic degree-\(d\) polynomial gives Galois group \(S_d\) in
characteristic zero.  We include the short critical-value calculation to
make the specialization and its branch geometry explicit.

### Lemma

For every \(d\geq3\),
\[
\operatorname{Gal}\bigl(T^d-T^2+UT+V\,/\,\mathbb C(U,V)\bigr)=S_d.
\tag{16}
\]

### Proof

Regard (15) as the fibre equation of the polynomial cover
\[
g_U:\mathbb P^1_T\longrightarrow\mathbb P^1_s,\qquad
g_U(T)=T^d-T^2+UT,
\]
where \(s=-V\).  Its critical points satisfy
\[
g_U'(T)=dT^{d-1}-2T+U=0.
\tag{17}
\]
At a critical point \(t\), equations (17) and \(g_U(t)\) become
\[
U=\psi(t):=2t-dt^{d-1},\qquad
g_U(t)=\phi(t):=t^2-(d-1)t^d.
\tag{18}
\]

First, the critical points are simple over
\(\overline{\mathbb C(U)}\).  A multiple critical point would also obey
\[
d(d-1)t^{d-2}-2=0.
\]
This makes \(t\), and then \(U=\psi(t)\), algebraic over \(\mathbb C\),
contradicting the transcendence of \(U\).

Second, distinct critical points have distinct critical values.  Suppose
\(x\ne y\) satisfy (17) and \(\phi(x)=\phi(y)\).  The case \(y=0\)
would give \(U=0\), again impossible.  Put \(r=x/y\ne1\), and write
\[
S_m(r)=1+r+\cdots+r^m.
\]
Subtracting the two critical equations and the two critical-value
equations gives
\[
d\,y^{d-2}S_{d-2}(r)=2,
\tag{19}
\]
\[
(d-1)y^{d-2}S_{d-1}(r)=r+1.
\tag{20}
\]
Eliminating \(y^{d-2}\) yields
\[
N_d(r):=(d-2)r^d-dr^{d-1}+dr-(d-2)=0.
\tag{21}
\]
This is a nonzero polynomial.  Hence \(r\) is algebraic over
\(\mathbb C\); equation (19) then makes \(y\), and finally
\(U=\psi(y)\), algebraic over \(\mathbb C\), a contradiction.

Thus \(g_U\) is a Morse polynomial: its \(d-1\) finite critical points
are simple and have pairwise distinct values.  Local inertia about each
finite branch value is consequently a transposition.  Infinity is
totally ramified of index \(d\), so its inertia is a \(d\)-cycle.

The cover has connected source and hence transitive monodromy.  Its
branch cycles generate the monodromy group, and the inertia at infinity
is the inverse of the product of the finite branch cycles.  The group is
therefore generated by its finite transpositions.  A transitive subgroup
of \(S_d\) generated by transpositions is \(S_d\): form the graph whose
edges are those transpositions; the generated group is the product of
the symmetric groups on the connected components, while transitivity
makes the graph connected.  This proves (16). \(\square\)

## 4. Direct conclusion for the simple seed

Let \(\Omega=\overline{\mathbb C(U)}\).  The preceding branch-cycle
argument computes the group after base change to \(\Omega(V)\) as
\(S_d\).  This group embeds in the Galois group over
\(\mathbb C(U,V)\), which is already a subgroup of \(S_d\); hence the
latter group is also \(S_d\).  Adjoining the independent target
coordinate \(C_d\) does not change the splitting field group.

The rational recovery (7) identifies this root extension with the
function-field extension induced by \(F_d\).  Therefore
\[
\operatorname{Mon}(F_d)=S_d
\]
in the natural degree-\(d\) action, for every \(d\geq3\).

## 5. Explicit collision certificate

For completeness, the cancellation in (14) follows by writing
\(v=xy\) and \(\tau=x^2z\).  The numerator of \(B_d\) has zero constant
term in \(v,\tau\); the numerator of \(A_d\) has zero constant and
linear-in-\(v\) terms.  The remaining monomials are divisible by \(x\)
and \(x^2\), respectively.

For the collision, set
\[
s_d=\frac{4-2^d}{d-2}.
\]
At the target \((A_d,B_d,C_d)=(s_d,s_d,1)\), equation (15) has the
distinct roots \(w=1,2\).  Formula (7) reconstructs two distinct source
points because
\[
\gamma(1)=\frac{d+2-2^d}{d-2}\ne0,\qquad
\gamma(2)=2^{d-1}\ne0.
\]
Thus each \(F_d\) is a Keller counterexample, rather than merely a
Keller map.

## 6. Scope and attribution

Gallagher proved the weighted-lift construction uniformly for every generic
degree at least three.  Brink's 2004 theorem already gives the required
two-parameter \(S_d\) Galois calculation for every fixed choice of the higher
coefficients.  Therefore the argument applies to every admissible Gallagher
seed.  The particularly simple seed
\[
\frac{2w-dw^{d-1}}{d-2},
\]
gives the displayed rational-coefficient representative in each degree.
No novelty is claimed for the polynomial-cover lemma.  The candidate new
statement is the combination of Gallagher's construction, exact root-field
recovery, and Brink's theorem: full symmetric monodromy throughout the
weighted-lift family, and hence realization of every \(S_d\), \(d\ge3\), by
a dimension-three Keller counterexample.

Before this note, a MathOverflow answer and its linked Note 19 had proved
\(S_d\) for Gallagher's canonical tower in the finite range
\(3\le d\le13\), with further finite symbolic evidence.  That is direct
prior overlap.  The statement here is the uniform all-degree,
all-admissible-seed corollary of Gallagher and Brink, not the finite table
and not a new abstract Galois theorem.

## References

- D. Brink, *On Alternating and Symmetric Groups as Galois Groups*,
  Israel J. Math. **142** (2004), 47--60,
  [doi:10.1007/BF02771527](https://doi.org/10.1007/BF02771527),
  especially Theorem 13.
- A. Gallagher, *An infinite family of counterexamples to the Jacobian
  Conjecture in dimension three: every generic fiber degree \(n\ge3\)
  occurs*, Zenodo (20 July 2026),
  [doi:10.5281/zenodo.21479195](https://doi.org/10.5281/zenodo.21479195).
- *Geometric degrees of counterexamples to the Jacobian conjecture in
  dimension three*, MathOverflow answer 513470 and linked Note 19,
  [mathoverflow.net/a/513470](https://mathoverflow.net/a/513470).
- J.-P. Serre, *Topics in Galois Theory*, 2nd ed., Research Notes in
  Mathematics 1, A K Peters (2008), Theorem 4.4.5 and Proposition 4.4.6.

This note was produced with substantial AI assistance.  The exact
scripts check the encoded algebra and finite specializations; they are
evidence against transcription errors, not peer review.  The result has
not been peer reviewed.
