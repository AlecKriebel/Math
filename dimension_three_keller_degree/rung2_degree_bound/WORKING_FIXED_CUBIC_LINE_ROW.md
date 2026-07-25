# Working theorem: the nonbinary fixed-cubic line stratum

**Status:** proved by exact determinant elimination, checked by two exact
implementations, and independently adversarially reconstructed from the raw
systems.  This is not peer reviewed.  The source-specific priority search
found no exact prior statement and is not a guarantee of worldwide priority.

**Recorded:** 2026-07-25T04:14:00Z.

**Promoted after audit:** 2026-07-25T04:41:47Z.

## 1. Statement and scope

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four, with \(H_i\) homogeneous of degree \(i\), and
suppose that after independent linear source and target changes
\[
\boxed{H_4=h(p,q,r)(p,q,0)^T}
\tag{1}
\]
for a nonzero homogeneous cubic \(h\).  This is the taxonomy row
\[
(e,a,b,\delta,\nu)=(3,1,1,1,1).
\]

Assume
\[
h\notin\mathbb C[p,q].
\tag{2}
\]
Thus the cubic fixed divisor is not contained in the minimal source
pencil.  Put
\[
t=q/p,\qquad s=r/p,\qquad h=p^3H(t,s)
\tag{3}
\]
on \(p\ne0\), and regard \(H\) as an element of
\(\mathbb C(t)[s]\).

### Theorem

If (1)--(2) hold and \(F\) is Keller, then \(F\) is a polynomial
automorphism.  In particular, no degree-four Keller counterexample lies in
the entire nonbinary part of this taxonomy row.

The proof does not treat the binary locus \(h\in\mathbb C[p,q]\).

## 2. A rank-one adjugate identity

Let
\[
A=(p,q,0)^T,\qquad C=J(hA),\qquad
k=(ph_r,qh_r,rh_r-4h)^T,
\tag{4}
\]
where \(h_r=\partial_rh\).  Euler's identity for the cubic \(h\) gives
\[
D_kh=-hh_r,\qquad D_kp=ph_r,\qquad D_kq=qh_r.
\tag{5}
\]
Consequently \(Ck=0\).  Since the third row of \(C\) is zero, direct
cofactor expansion gives
\[
\boxed{\operatorname{adj}C=-h\,k e_3^T,}
\qquad e_3=(0,0,1)^T.
\tag{6}
\]

For bookkeeping, put
\[
\mathcal J(z)=L_0+zJH_2+z^2JH_3+z^3JH_4,\qquad
E_j=[z^j]\det\mathcal J(z).
\tag{7}
\]
The Keller condition says \(E_j=0\) for \(j>0\).

Write
\[
G_3=(H_3)_3.
\]
The degree-eight identity and (5) give
\[
E_8=\operatorname{tr}(\operatorname{adj}C\,JH_3)
    =-hD_kG_3.
\tag{8}
\]
Thus
\[
\boxed{D_kG_3=0.}
\tag{9}
\]

## 3. Logarithmic valuations kill the normal components

More generally, if \(G=p^dg(t,s)\) is homogeneous of degree \(d\), then
(2)--(4) give
\[
\boxed{
D_kG=p^{d+2}\bigl(dH_sg-4Hg_s\bigr).
}
\tag{10}
\]
For \(G=G_3\), equations (9)--(10) become
\[
4Hg_s=3H_sg.
\tag{11}
\]
Let \(\phi^m\Vert H\) be any \(s\)-dependent irreducible factor in
\(\mathbb C(t)[s]\).  Taking the \(\phi\)-adic residue after division by
\(Hg\) gives
\[
4v_\phi(g)=3m.
\tag{12}
\]
Because \(H\) has degree at most three in \(s\), one has
\(m\in\{1,2,3\}\), none of which makes (12) integral.  Since \(H\)
depends on \(s\), this proves
\[
\boxed{(H_3)_3=0.}
\tag{13}
\]

Put \(B=JH_3\).  Its third row is now zero.  Hence
\(\operatorname{adj}B\) has only a third column, while \(C\) has zero third
row, and therefore
\[
\operatorname{tr}(\operatorname{adj}B\,C)=0.
\tag{14}
\]
The degree-seven identity is consequently
\[
\begin{aligned}
E_7
&=\operatorname{tr}(\operatorname{adj}C\,JH_2)
  +\operatorname{tr}(\operatorname{adj}B\,C)\\
&=-hD_k(H_2)_3.
\end{aligned}
\tag{15}
\]
Let \(G_2=(H_2)_3=p^2g(t,s)\).  Equations (10) and (15) yield
\[
2Hg_s=H_sg.
\tag{16}
\]
At an \(s\)-dependent factor \(\phi^m\Vert H\),
\[
\boxed{2v_\phi(g)=m.}
\tag{17}
\]
If no \(s\)-dependent factor has multiplicity two, multiplicities one and
three are incompatible with (17).  Therefore
\[
\boxed{(H_2)_3=0.}
\tag{18}
\]

No division by \(h_r\), \(H_s\), or a possibly zero normal component has
been used.

## 4. Birational plane exit

Equations (1), (13), and (18) say that the third component of \(F\) is a
nonzero linear form, up to an irrelevant constant target translation.
It is nonzero because
\[
\det L_0=\det JF(0)\ne0.
\]
After linear source and target changes, write
\[
F=(P(p,q,r),Q(p,q,r),r).
\tag{19}
\]
Then
\[
\frac{\partial(P,Q)}{\partial(p,q)}=\det JF\in\mathbb C^\times.
\tag{20}
\]

Regard \(P,Q\) as a plane Keller map over the characteristic-zero field
\(\mathbb C(r)\).  Its total degree in \(p,q\) is at most four.  The
unconditional plane degree bound, which is far stronger than four, applies
after base change to an algebraic closure of \(\mathbb C(r)\); hence
\[
\mathbb C(r)(p,q)=\mathbb C(r)(P,Q).
\tag{21}
\]
Thus the three-dimensional map (19) is birational.  The classical
birational Keller theorem makes \(F\) a polynomial automorphism.

This step uses an established low-degree plane theorem only as an input; it
does not assume the plane Jacobian Conjecture.  Polynomial invertibility
descends from an algebraic closure of \(\mathbb C(r)\), so only the
function-field equality (21) is needed for the three-dimensional exit.

## 5. Classification of the residual double-factor locus

Suppose now that \((H_2)_3\ne0\).  Equation (17) says that every
\(s\)-dependent factor of \(H\) has even multiplicity.  Since \(H\) has
degree at most three in \(s\), unique factorization and homogeneity give
\[
h=\ell(p,q)m(p,q,r)^2,
\tag{22}
\]
where \(\ell\) is a binary linear form and \(m\) is a nonbinary linear
form.  A parabolic source change preserving
\(\langle p,q\rangle\), followed by its induced target change, normalizes
\[
\boxed{h=pr^2.}
\tag{23}
\]
For this normal form, (17) has the complete homogeneous solution
\[
(H_2)_3=r(\alpha p+\beta q).
\tag{24}
\]
The zero solution returns to Section 4.  The stabilizer has exactly two
nonzero orbits:
\[
(H_2)_3=qr,\qquad (H_2)_3=pr.
\tag{25}
\]

## 6. The \(qr\) orbit

A raw degree-six and degree-five solve, followed by source translations
that preserve \(H_4\), gives
\[
\begin{aligned}
H_3={}&
\bigl(2cpqr,\ r(ap^2+bpq+cq^2),\ 0\bigr)^T,\\
H_2={}&
\bigl((2x-2ac)p^2+(2y-2bc)pq+c^2q^2+dpr+eqr,\\
&\hspace{27mm}xpq+yq^2+fpr+gqr,\ qr\bigr)^T,
\end{aligned}
\tag{26}
\]
and the third row of \(L_0\) is \((a,b,0)\).  These forms retain all
solutions of the two identities; no coefficient has been divided by a
possibly zero parameter.

Write the third column of \(L_0\) as
\((\lambda_{13},\lambda_{23},0)^T\).  Two degree-four coefficients are
\[
[qr^3]E_4=\lambda_{13},\qquad
[pr^3]E_4=-2\lambda_{23}.
\tag{27}
\]
Their vanishing makes the entire third column of \(L_0\) zero.  Hence
\(\det L_0=0\), so this orbit contains no Keller map.

## 7. The \(pr\) orbit

After the same exact solves and affine normalizations, write
\[
\begin{aligned}
H_3&=(2\tau pqr,\ U,\ 0)^T,\\
H_2&=(\tau^2q^2+Dpr+Kqr,\ V,\ pr)^T,\\
(L_0)_{3\bullet}&=(0,\tau,0),
\end{aligned}
\tag{28}
\]
where \(U=\sum_{i=0}^9u_iM_i\) is a general cubic in the monomial order
\[
(M_0,\ldots,M_9)=
(p^3,p^2q,pq^2,q^3,p^2r,pqr,q^2r,pr^2,qr^2,r^3),
\tag{29}
\]
and \(V\) is a general quadratic.  The complete degree-four coefficient
table is
\[
\begin{array}{c|c}
r^4&3Ku_9\\
qr^3&Ku_8\\
pr^3&Ku_7-\lambda_{13}\\
q^2r^2&K(\tau-u_6)\\
pqr^2&-\tau D-Ku_5+\lambda_{12}\\
p^2r^2&-Ku_4+\lambda_{11}\\
q^3r&-3Ku_3\\
pq^2r&-3Ku_2\\
p^2qr&-3Ku_1\\
p^3r&-3Ku_0.
\end{array}
\tag{30}
\]

If \(K=0\), (30) forces
\[
\lambda_{13}=0,\qquad \lambda_{12}=\tau D,\qquad
\lambda_{11}=0.
\]
The first and third rows of \(L_0\) are then both supported in the second
column, so \(\det L_0=0\).

Assume \(K\ne0\).  Equation (30) gives
\[
\begin{gathered}
u_0=u_1=u_2=u_3=u_8=u_9=0,\qquad u_6=\tau,\\
(\lambda_{11},\lambda_{12},\lambda_{13})
=(Ku_4,\tau D+Ku_5,Ku_7).
\end{gathered}
\tag{31}
\]
Put \(A=u_4,B=u_5,C=u_7\).  Degree three forces
\[
V=A\tau pq+B\tau q^2+Epr+Gqr.
\tag{32}
\]
Writing the second row of \(L_0\) as \((m,n,o)\), degree two forces
\[
\begin{aligned}
m&=A(G-C\tau),\\
n&=E\tau+B(G-C\tau),\\
o&=C(G-C\tau).
\end{aligned}
\tag{33}
\]
The determinant is now
\[
\det L_0=K\tau(-Ao+Cm)=0.
\tag{34}
\]
This excludes the second orbit and finishes the nonbinary theorem.

The binary locus \(h\in\mathbb C[p,q]\) remains separate: equation (8)
forces only that \((H_3)_3\) be binary, not zero.

## 8. Verification boundary and disclosure

`verify_fixed_cubic_line_sympy.py` checks (5)--(10), the exact polarization
(14)--(15) with general cubic and quadratic parts, the homogeneous
derivation formula (10) for degrees three and two, the complete
double-factor invariant space (24), the \(qr\)-orbit exit (26)--(27), and
the \(pr\)-orbit tables and lower identities (28)--(34).

`verify_fixed_cubic_line_pari.gp` independently expands the adjugate,
kernel, degree-eight and degree-seven identities, and both normalized
double-factor exits in PARI/GP.  Run it through
`verify_fixed_cubic_line_pari_strict.sh`, which rejects any GP diagnostic
and requires the unique terminal pass marker; this prevents GP's file
reader from continuing to a false pass after an unexpected runtime error.

The factor-multiplicity classification, raw degree-six/degree-five solves,
affine-translation and orbit completeness, and plane birational exit are
mathematical inputs, not computer checks.  An independent adversarial audit
reconstructed the factor classification, the two stabilizer orbits, both
raw normalized solves, and the low-degree plane-field exit; it also tested
the strict GP wrapper against injected diagnostics, extra output, and
nonzero exit status.  The exact calculations are evidence about the encoded
algebra only and are not peer review.  This proof and its regressions were
developed with AI assistance.
