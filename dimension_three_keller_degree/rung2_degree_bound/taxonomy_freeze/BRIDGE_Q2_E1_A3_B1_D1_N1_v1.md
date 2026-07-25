# Post-freeze coverage bridge candidate for `Q2-E1-A3-B1-D1-N1`

**Recorded (UTC):** 2026-07-25T22:17:26Z.

**Coverage verdict:** **PASS as an unconditional candidate.**  Every point
of every frozen coefficient-pivot stratum is either routed through an exact
hostile-audited theorem or lies in one of the fifteen division-free empty
strata `C30`--`C44`.

**Certification status:** unchanged.  This bridge does **not** promote the
row in `CERTIFIED_EXCLUSION_STATUS.md` until a fresh hostile reconstruction
of this post-freeze bridge itself passes.  The \(s=0,W_0\ne0\) theorem and
the quadratic-component exit now both have standalone PASS reports.

This note was produced with substantial AI assistance and is not peer
reviewed.  Exact checks verify the encoded algebra and coverage ledger; they
are evidence, not peer review.

## 1. Exact frozen scope

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have exact total degree four, with
\(L_0\in\operatorname{GL}_3(\mathbb C)\) and \(H_i\) homogeneous of
degree \(i\).  Assume that \(H_4\) belongs to the frozen inclusive row
\[
R=\texttt{Q2-E1-A3-B1-D1-N1}.
\]
Its canonical leading tuple is
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)
  =(2,1,3,1,1,1).                                    \tag{1}
\]
No condition is imposed on \(H_2,H_3\), on their incidences with \(H_4\),
or on the first nonzero coefficient of \(H_4\).

The internal frozen split is
\[
\begin{array}{c|l}
\texttt{L01}&\text{horizontal: no pencil member is divisible by the
fixed line},\\
\texttt{L02}&\text{vertical: a pencil member is divisible by the fixed
line}.
\end{array}                                           \tag{2}
\]
The purpose of this bridge is to derive the normal form used by the retained
theorems directly from (1), prove that (2) is intrinsic and exhaustive, and
route all multiplicities, companion types, lower rank divisors, and frozen
coefficient pivots.

## 2. Uniform leading normal form from the frozen tuple

### Lemma 1

Every \(H_4\) satisfying (1) admits an invertible target change \(T\) for
which
\[
T H_4=h(p,q,0)^T,                                    \tag{3}
\]
where:

- \(h\) is a nonzero ternary linear form;
- \(p,q\) are coprime, nonproportional ternary cubics; and
- \(\mathbb C(p/q)\) is relatively algebraically closed in
  \(\mathbb C(\mathbb P^2)\).

The construction divides by no frozen coefficient \(c_i\).

### Proof

The canonical-pencil theorem in `FROZEN_TAXONOMY_v1.md` gives the exact
factorization
\[
H_4=hA(p,q),                                          \tag{4}
\]
where \(\deg h=e=1\), \(\deg p=\deg q=a=3\), and
\(A=(A_0,A_1,A_2)\) is a basepoint-free binary triple of degree \(b=1\).
Write
\[
A(u,v)=\mathbf a\,u+\mathbf b\,v,
\qquad \mathbf a,\mathbf b\in\mathbb C^3.             \tag{5}
\]
Basepoint freeness is equivalent to linear independence of
\(\mathbf a,\mathbf b\).  Complete them by any \(\mathbf c\) to a target
basis, put \(B=(\mathbf a\ \mathbf b\ \mathbf c)\), and take
\(T=B^{-1}\).  Then
\[
TA(u,v)=(u,v,0)^T,
\]
which proves (3).

For a finite chart version, use the ordered first nonzero minor among
\[
\Delta_{01}=a_0b_1-a_1b_0,\quad
\Delta_{02}=a_0b_2-a_2b_0,\quad
\Delta_{12}=a_1b_2-a_2b_1.                            \tag{6}
\]
At least one is nonzero, and on its chart the unused standard basis vector
can be chosen as \(\mathbf c\).  The determinant of \(B\) is, up to sign,
the selected nonzero minor.  Thus the normalization uses only an intrinsic
rank-two chart determinant, never a frozen coefficient pivot.

The exact factorization theorem also gives \(\gcd(p,q)=1\).  Its
relative-closure definition says precisely that
\[
\mathbb C(p/q)\subset\mathbb C(\mathbb P^2)
\]
is relatively algebraically closed.  This is the retained theorems'
“minimal primitive cubic pencil” hypothesis, not an additional genericity
assumption. \(\square\)

Independent source and target linear changes preserve the Keller property,
exact total degree, and polynomial-automorphism property.  They also carry
arbitrary \(H_2,H_3,L_0\) bijectively to arbitrary lower jets and an
invertible linear part.  Hence every lower-term theorem below has exactly
the required scope after (3).

## 3. The horizontal/unique-vertical split is intrinsic

Let
\[
\mathcal P=\langle p,q\rangle\subset
\operatorname{Sym}^3((\mathbb C^3)^*)
\]
be the canonical cubic pencil, and let
\[
\rho_h:\mathcal P\longrightarrow
\mathbb C[x,y,z]_3/(h)
\]
be restriction to the fixed line \(h=0\).  Then
\[
\ker\rho_h
=\{g\in\mathcal P:h\mid g\}.                          \tag{7}
\]
There are exactly three formal ranks:

- \(\operatorname{rank}\rho_h=2\): no nonzero member is divisible by
  \(h\), the horizontal leaf `L01`;
- \(\operatorname{rank}\rho_h=1\): the kernel is one-dimensional, so
  there is a unique projective vertical member, the vertical leaf `L02`;
- \(\operatorname{rank}\rho_h=0\): \(h\mid p\) and \(h\mid q\), contrary
  to \(\gcd(p,q)=1\).

Thus the first two cases are disjoint and exhaustive.  The construction is
intrinsic: the component gcd \(h\) is unique up to a scalar, while a change
of the canonical pencil generator acts on \(\mathcal P\) by
\(\operatorname{GL}_2\) and does not change the rank of \(\rho_h\).

After a source change set \(h=z\).  On the vertical leaf choose the unique
vertical member as the first pencil generator.  It has the exact form
\[
p=z^m r_{3-m},\qquad
1\le m\le3,\qquad z\nmid r_{3-m}q.                    \tag{8}
\]
The integer \(m=v_z(p)\) is intrinsic and exhaustive because \(p\) is a
nonzero cubic.  A second vertical member cannot appear on a specialization
inside this row: it would make \(z\) divide both pencil generators and
change the component gcd.

## 4. Horizontal route

If \(\operatorname{rank}\rho_h=2\), the point lies exactly in the scope of
`../fixed_linear_cubic_pencil/WORKING_HORIZONTAL_FIXED_LINEAR_CUBIC_PENCIL.md`.
That theorem uses the relative-algebraic-closure condition already supplied
by Lemma 1 and makes no extra genericity assumption.  Its divisor argument
forces
\[
(H_3)_3=(H_2)_3=0,
\]
so the third component is linear and the proved bounded-degree plane
theorem gives an automorphism.  The standalone hostile report
`../fixed_linear_cubic_pencil/audit_hostile/REPORT.md` passed on precisely
this full horizontal scope, including arbitrary lower jets.

## 5. Vertical multiplicities \(m=1,2,3\)

Write
\[
G=(H_3)_3.
\]
The degree-eight identity is
\[
\operatorname{Jac}(z p,zq,G)=0.                       \tag{9}
\]
The retained vertical multiplicity theorem in
`../fixed_linear_cubic_pencil/vertical_locus/WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md`
and its standalone hostile reconstruction
`../fixed_linear_cubic_pencil/vertical_locus/audit_vertical_hostile/REPORT.md`
give:

\[
\begin{array}{c|c|l}
m&\text{complete cubic kernel}&\text{route}\\ \hline
1&0&G=0\text{, then quadratic-component exit},\\
2&0&G=0\text{, then quadratic-component exit},\\
3&\langle z^3,q\rangle&
G=0\text{ or one of two nonzero companion orbits}.
\end{array}                                           \tag{10}
\]

When \(G=0\), the third target component has degree at most two because its
quartic and cubic homogeneous pieces vanish.  The theorem
`../WORKING_QUADRATIC_COMPONENT_EXIT.md` then makes the map an
automorphism.  This handles all \(m=1,2\) points and the zero companion on
\(m=3\).

For \(m=3\), scale \(p=z^3\).  If
\[
G=\alpha z^3+\beta q\ne0,
\]
the residual pencil change \(q\mapsto aq+bz^3\), followed by scaling of the
third target coordinate, gives exactly
\[
\begin{array}{c|c}
\beta=0&G=z^3\quad\text{(vertical companion)},\\
\beta\ne0&G=q\quad\text{(nonvertical companion)}.
\end{array}                                           \tag{11}
\]
These orbits cannot merge because divisibility by the unique fixed line
\(z\) is preserved: \(z\mid z^3\) while \(z\nmid q\).  The hostile
vertical-multiplicity audit independently checked both the normalization
and this separation.

## 6. The nonvertical cubic companion \(G=q\)

Because \(\gcd(z^3,q)=1\), the binary cubic
\[
q_0=q|_{z=0}
\]
is nonzero.  Over \(\mathbb C\) its root multiplicity is exactly one of
\[
1+1+1,\qquad2+1,\qquad3.                              \tag{12}
\]
The first two partitions are excluded by
`../fixed_linear_cubic_pencil/vertical_locus/NONVERTICAL_NONTRIPLE_LEMMA.md`;
the triple-root partition is excluded by
`../fixed_linear_cubic_pencil/vertical_locus/NONVERTICAL_TRIPLE_ROOT_LEMMA.md`.
The latter's three source charts retain all continuous moduli, and its
fourth coefficient shape is exactly the nonminimal boundary, hence outside
the frozen row rather than an omitted case.

The dependency-free hostile reconstruction
`../fixed_linear_cubic_pencil/vertical_locus/audit_nonvertical_companion/REPORT.md`
rederived the legal gauge, all three root partitions, every lower modulus,
and all seven constant minors.  Therefore the entire nonvertical companion
is routed with no pending subcase.

## 7. The vertical cubic companion \(G=z^3\)

The complete legal degree-seven gauge is
\[
H_4=(z^4,zq,0)^T,\qquad
H_3=\left(\frac43zW+\sigma q,\ V,\ z^3\right)^T,
\qquad [z^3]V=0.                                     \tag{13}
\]
The rank ledger calls the coefficient \(\sigma\) by \(a\); later theorem
files call it \(s\).  These are the same parameter.  The split
\(\sigma\ne0\) versus \(\sigma=0\) is exhaustive and does not divide by a
lower-jet coefficient.

### 7.1 The branch \(\sigma\ne0\)

Again use the three partitions (12).

If \(q_0\) is squarefree or has one double root, the raw degree-six
restriction first forces
\[
W|_{z=0}=0.
\]
Write
\[
W=z(\ell+\omega z),\qquad \ell\in\mathbb C[x,y]_1.
\]
The two exhaustive routes are:

\[
\begin{array}{c|l}
\ell=0&
\texttt{VERTICAL_ELL_ZERO_NONTRIPLE_LEMMA.md},\\
\ell\ne0&
\texttt{VERTICAL_NONZERO_ELL_NONTRIPLE_LEMMA.md}.
\end{array}                                           \tag{14}
\]

The second theorem explicitly includes all squarefree root collisions,
the double-root noncollision kernel, and both double-root collision
kernels.  Both theorems have standalone dependency-free hostile reports.
Thus (14) loses no discriminant or collision divisor.

If \(q_0\) has a triple root, normalize it to \(x^3\).  The same
degree-six restriction gives
\[
W|_{z=0}=\gamma x^2.
\]
The exhaustive split is:

\[
\begin{array}{c|l}
\gamma\ne0&
\texttt{VERTICAL_TRIPLE_GAMMA_NONZERO_EXCLUSION.md},\\
\gamma=0&
\texttt{VERTICAL_TRIPLE_GAMMA0_REDUCTION.md}
\ \longrightarrow\
\texttt{VERTICAL_TRIPLE_GAMMA0_ELL0_LEMMA.md}.
\end{array}                                           \tag{15}
\]

The zero-\(\gamma\) reduction forces the full \(z\)-linear form in \(W\)
to vanish before invoking the terminal theorem.  The nonzero-\(\gamma\)
theorem and both zero-\(\gamma\) inputs have standalone dependency-free
hostile reports on all three minimal triple-root charts.  Their omitted
binary shape is exactly the nonminimal \((a,b)=(1,3)\) boundary.

Equations (14)--(15) therefore close the complete
\(\sigma\ne0\) vertical companion.

### 7.2 The branch \(\sigma=0\)

Put \(W_0=W|_{z=0}\).  There are exactly two routes:

\[
\begin{array}{c|l}
W_0=0&
\texttt{VERTICAL_A0_W0_ZERO_EXCLUSION.md},\\
W_0\ne0&
\texttt{a0_w0_nonzero_attack/NOTE.md}.
\end{array}                                           \tag{16}
\]

The first theorem covers the squarefree, double-root, and all three
minimal triple-root charts with every lower jet.  It passed the independent
hostile reconstruction in
`audit_vertical_a0_w0_zero/REPORT.md`; the independently derived
`VERTICAL_SZERO_W0_EXCLUSION.md` supplies a second exact
SymPy/PARI route to the same statement.

The second theorem is stronger than a root-type case split: from
\(E_6=0\) and \(W_0\ne0\) it derives
\[
q\in\operatorname{Sym}^3\langle z,L\rangle,
\]
which is exactly the nonminimal boundary.  Hence no point of the frozen
minimal row survives.  Its supplied raw-SymPy and dependency-free sparse
implementations pass.  The later independent reconstruction in
`audit_a0_w0_nonzero/REPORT.md` also passed without a scope change.

Thus (16) closes the complete \(\sigma=0\) family, and Sections 4--7 close
both frozen internal leaves `L01` and `L02`.

## 8. Frozen coefficient pivots

Use the frozen quartic monomial order
\[
\begin{split}
(m_0,\ldots,m_{14})={}&(
x^4,x^3y,x^3z,x^2y^2,x^2yz,x^2z^2,xy^3,xy^2z,xyz^2,xz^3,\\
&y^4,y^3z,y^2z^2,yz^3,z^4).
\end{split}                                           \tag{17}
\]

### Potential pivots `C00`--`C29`

For every \(i\), choose a coordinate \(h_i\) dividing \(m_i\), put
\[
p_i=m_i/h_i,\qquad q_*=x^3+y^3+z^3,
\]
and consider
\[
(m_i,h_iq_*,0)^T=h_i(p_i,q_*,0)^T                    \tag{18}
\]
and
\[
(0,m_i,h_iq_*)^T=h_i(0,p_i,q_*)^T.                   \tag{19}
\]
They have first frozen pivots `C\(i\)` and `C\(15+i\)`, respectively.
Their component gcd is exactly \(h_i\), because \(q_*\) is divisible by
no coordinate.  The cubic \(q_*\) has three linearly independent first
derivatives, so it is not a binary cubic in any two-dimensional space of
linear forms.  A nonminimal cubic pair would be binary in such a space;
hence \((p_i,q_*)\) is minimal.  The two quartic components are
nonproportional homogeneous forms and therefore algebraically independent,
so their Jacobian has rank two in characteristic zero.  Thus (18)--(19)
have exactly the tuple (1).

These are leading-term witnesses, not claimed Keller completions.  Their
role is only to show that none of `C00`--`C29` is forced empty by the frozen
leading tuple.  For an arbitrary point of any nonempty one of these thirty
strata, Lemma 1 and the complete intrinsic tree in Sections 3--7 apply
without dividing by its pivot coefficient.

### Empty pivots `C30`--`C44`

If the first pivot were `C30` or later, then
\[
H_{4,1}=H_{4,2}=0.
\]
The Jacobian \(JH_4\) would have at most one nonzero row and therefore rank
at most one, contradicting (1).  This is a division-free coefficient
vanishing argument.  Hence
\[
R/\mathrm C_i=\varnothing\qquad(30\le i\le44).        \tag{20}
\]

The frozen routing is therefore
\[
\begin{array}{c|l}
R/\mathrm C_{00},\ldots,R/\mathrm C_{29}&
\text{if nonempty, Lemma 1 followed by Sections 3--7},\\
R/\mathrm C_{30},\ldots,R/\mathrm C_{44}&
\varnothing\text{ by (20)}.
\end{array}                                           \tag{21}
\]

## 9. Provenance and scope audit

The retained input audit found no mathematical scope mismatch in the
routes above, but it found the following certification facts that must not
be blurred:

1. **Final \(W_0\ne0\) audit.**  The independent report
   `audit_a0_w0_nonzero/REPORT.md` reconstructs the literal determinant,
   every parameter divisor, and the exact nonminimal boundary.  Its verdict
   is PASS.
2. **Quadratic-exit provenance repaired.**
   `../audit_quadratic_component_exit/REPORT.md` independently reconstructs
   the coordinate/fibre proof, checks Vistoli's exact unconditional
   degree-\(\le12\) plane theorem on journal pp. 79--80, and gives PASS.
   The maps here have plane degree at most eight.
3. **Status labels repaired.**  The parent vertical theorem, both
   nonvertical companion lemmas, the \(W_0\ne0\) theorem, and the rank
   ledger now cite their later standalone PASS reports.
4. **Overlapping \(W_0=0\) notes.**  The hostile PASS attaches to
   `VERTICAL_A0_W0_ZERO_EXCLUSION.md`.  The separate
   `VERTICAL_SZERO_W0_EXCLUSION.md` is an independent reconstruction, not
   a second hostile verdict.
5. **Bridge audit is separate.**  Exact leaf exclusions do not certify the
   post-freeze assembly.  A hostile auditor must independently reconstruct
   Lemma 1, the restriction-rank split, all thirty potential pivot routes,
   the fifteen empty pivots, and the complete terminal-route ledger.

No claim of row exclusion should be made before item 5 receives its own
PASS report.

## 10. Deterministic replay

From `dimension_three_keller_degree/rung2_degree_bound`, run

```text
/usr/bin/python3 taxonomy_freeze/verify_bridge_q2_e1_a3_b1_d1_n1_v1.py
```

The checker pins the frozen and theorem inputs, reconstructs the target
normalization charts, verifies all thirty leading-tuple witnesses and the
fifteen empty pivots, checks the restriction-rank trichotomy and companion
normalization, and compares the complete route tree with a fixed terminal
ledger.

Its success marker certifies **candidate coverage only**.  Every terminal
is now audited, but this supplied checker cannot promote the frozen status
ledger without the independent bridge audit.

The latest exact replay time and the SHA-256 digests of this note and its
checker are recorded in
`RESEARCH_LOG_Q2_E1_A3_B1_D1_N1_BRIDGE.md`.
