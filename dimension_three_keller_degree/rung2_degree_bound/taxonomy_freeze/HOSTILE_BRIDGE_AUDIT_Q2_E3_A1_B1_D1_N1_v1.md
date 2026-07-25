# Hostile audit of the post-freeze fixed-cubic-line bridge

**Audited artifact:** `BRIDGE_Q2_E3_A1_B1_D1_N1_v1.md`

**Frozen row:** `Q2-E3-A1-B1-D1-N1`

**Audit recorded (UTC):** 2026-07-25T21:37:16Z

**Auditor relation:** the auditor did not author the bridge candidate.

**Overall verdict:** **PASS**, with the provenance correction in Section 2.

The bridge covers all 45 frozen pivot strata.  The first 30 are routed
pointwise, not merely through the displayed witnesses, to an intrinsic and
exhaustive binary/nonbinary split.  The last 15 are empty by a
division-free rank argument.  Both legacy branches replay exactly.

The earlier assertion that the nonbinary legacy theorem had already received
an independent hostile reconstruction was not supported by a retained
standalone artifact.  That historical provenance assertion therefore fails
as documentary evidence.  This audit repairs the gap by retaining a fresh
reconstruction from the unrestricted coefficient systems in
`verify_hostile_bridge_q2_e3_a1_b1_d1_n1_v1.py`.  The new checker is
dependency-free and does not call SymPy, PARI/GP, or either legacy verifier.

This audit was produced with substantial AI assistance and is not peer
reviewed.  Exact checks establish facts about the encoded algebra; they are
evidence, not peer review.

## 1. Pinned scope

The hostile checker pins the exact bridge, freeze, legacy theorem statements,
legacy exact programs, and retained binary hostile report by SHA-256.  The
principal hashes are

```text
4fc9de9d57164997ab528aad08a5ccf704ccc9b8e1cb8c4adcb9c099153c7b2c  BRIDGE_Q2_E3_A1_B1_D1_N1_v1.md
41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d  FROZEN_TAXONOMY_v1.md
5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23  frozen_manifest_v1.json
9a10c1c103b60eb21405518074086168330a435bb5aa1770d51463a881a926ca  ../WORKING_FIXED_CUBIC_LINE_ROW.md
51818647fa7f57942761ca31ed80dc9dde4363ebe83166d87fc80f07861a9607  ../WORKING_BINARY_FIXED_CUBIC_LINE_ROW.md
fdcf31dc44bda116c0e81da6a9d96abf0b92798eb8d56ec25d6c124b31d4b8b8  ../verify_fixed_cubic_line_sympy.py
aeded24439435f5db31d2e702fe357ec0799b62a326761e514727ff77dcc61e1  ../verify_fixed_cubic_line_pari.gp
4cea6002ca7639cf8e04aea80b86daa76655c7359e041e2e7707e50418fa7fc4  ../audit_binary_fixed_cubic_hostile/REPORT.md
```

The checker refuses optimized Python, so its assertions cannot be disabled
with `python -O`.

## 2. Provenance finding

Commit `9a604df789534b1af300eef59ce3544f18f41bb3`, titled
`exclude nonbinary fixed-cubic line stratum`, introduced:

- `WORKING_FIXED_CUBIC_LINE_ROW.md`;
- the SymPy and PARI/GP verifiers and the strict GP wrapper; and
- aggregate prose in `VERIFICATION.md` saying that an adversarial audit had
  reconstructed the omitted mathematical steps.

Inspection of that commit's tree, the present tree, and the path history finds
no standalone nonbinary hostile report or independent raw-solve program.
Thus the aggregate sentence is not independently inspectable provenance.
The two exact legacy programs remain useful and mutually independent checks
of the normalized determinant identities, but they do not themselves prove
the completeness of the raw normalizations: both begin those parts with the
claimed normalized families.

The retained binary branch is different.  It has a standalone hostile report,
two clean-room exact programs, and a false-pass suite.  All of them replayed.

The present report and dependency-free checker are therefore the first
retained standalone hostile reconstruction of the missing nonbinary steps in
this repository.  This statement is about retained project artifacts, not
about who may have reasoned through the calculation in an earlier ephemeral
agent context.

## 3. Reconstruction of the bridge

### 3.1 Uniform normal form

The frozen tuple is
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)=(2,3,1,1,1,1).
\]
By the frozen canonical-pencil factorization,
\[
H_4=hA(p,q),
\]
where \(h\) is a cubic, \(p,q\) are independent linear forms, and
\(A(u,v)=a u+b v\) is a degree-one basepoint-free triple.  Basepoint
freeness forces the two coefficient columns \(a,b\in\mathbb C^3\) to be
independent.  Completing \(a,b\) to a target basis and \(p,q\) to a source
basis gives, without reference to a pivot coefficient,
\[
H_4=h'(x,y,z)(x,y,0)^T.
\]

The three nonzero \(2\times2\) minors of each rank-two coefficient matrix
give a finite chart cover.  An inverse is taken only on the chart where its
determinant is known to be nonzero.  Thus the normalization does not discard
a pivot boundary.

### 3.2 Intrinsic binary/nonbinary split

The minimal pencil determines
\[
U=\langle p,q\rangle\subset(\mathbb C^3)^*
\]
intrinsically: a second minimal generator differs by a Möbius
transformation.  The component gcd \(h\) is unique up to scalar.  Therefore
\[
h\in\operatorname{Sym}^3U
\]
is independent of the pencil basis and of the completion by \(r\).  Replacing
\(r\) by \(\lambda r+\alpha p+\beta q\), with \(\lambda\ne0\), preserves the
largest positive \(r\)-degree and hence cannot turn a nonbinary cubic into a
binary one.  A basis change in \(U\) acts invertibly because
\[
\det(\operatorname{Sym}^3 M)=(\det M)^6.
\]
The dependency-free checker recomputes this determinant from the \(4\times4\)
coefficient matrix.  Hence the binary and nonbinary conditions are disjoint,
exhaustive, and intrinsic.

### 3.3 Frozen pivots

For every quartic monomial \(m_i\) in the frozen order, choose a coordinate
linear factor \(\ell_i\mid m_i\), an independent coordinate \(n_i\), and
put \(h_i=m_i/\ell_i\).  The triples
\[
(m_i,h_i n_i,0),\qquad (0,m_i,h_i n_i)
\]
have cubic component gcd, residual line degree one, residual birational
degree one, and Jacobian rank two.  The checker constructs all 30 triples
directly from exponent vectors, verifies the gcd degree and a nonzero
\(2\times2\) Jacobian minor, and confirms that their first coefficient
positions are exactly `C00`--`C29`.

These witnesses only show that the frozen leading invariants do not
themselves empty an early pivot.  Routing of an arbitrary point does not use
the witness: it uses the uniform normal form and intrinsic split above.

For `C30`--`C44`, the first two complete fifteen-coefficient target blocks
vanish.  Thus only the third component of \(H_4\) can be nonzero, so
\(JH_4\) has at most one nonzero row and rank at most one.  This contradicts
the frozen rank-two condition.  This proves all 15 emptiness statements
without division.

Therefore the frozen denominator is exactly
\[
30\ \text{pointwise routed potential strata}
\quad+\quad
15\ \text{forced-empty strata}
=45.
\]

## 4. Fresh reconstruction of the nonbinary legacy theorem

This section records the mathematical completeness argument whose earlier
standalone provenance was missing.

### 4.1 Valuations and the sole exceptional cubic

For
\[
H_4=h(p,q,r)(p,q,0)^T,\qquad
k=(ph_r,qh_r,rh_r-4h)^T,
\]
direct cofactors give
\[
\operatorname{adj}JH_4=-h\,k e_3^T.
\]
The top two nonconstant determinant identities imply
\[
D_kG_3=0,\qquad D_kG_2=0,
\]
where \(G_j=(H_j)_3\).  On \(p\ne0\), write
\[
h=p^3H(t,s),\qquad G_j=p^jg_j(t,s).
\]
Then
\[
D_kG_j=p^{j+2}(jH_sg_j-4H(g_j)_s).
\]

If \(g_3\ne0\) and \(\phi^m\Vert H\) is an \(s\)-dependent irreducible
factor, logarithmic valuation gives
\[
4v_\phi(g_3)=3m.
\]
Here \(1\le m\le3\), so no integer valuation is possible.  Hence \(G_3=0\).
For \(g_2\ne0\), the same argument gives
\[
2v_\phi(g_2)=m.
\]
Every \(s\)-dependent factor of \(H\) therefore has even multiplicity.
Because \(h\) has total degree three, localization and rehomogenization show
that the only possibility is
\[
h=\ell(p,q)m(p,q,r)^2
\]
with \(\ell\) a binary linear form and \(m\) a nonbinary linear form.
There is no hidden higher-degree \(m\): \(m^2\mid h\) in the homogeneous
UFD forces \(2\deg m\le3\).

A parabolic source change and induced target change normalize \(h=pr^2\).
The complete quadratic kernel of \(D_k\) is
\[
G_2=r(\alpha p+\beta q).
\]
If \(\beta\ne0\), a shear and scaling of \(q\) sends this to \(qr\); if
\(\beta=0\), scaling the third target coordinate sends it to \(pr\).
The vanishing/nonvanishing of \(\beta\) is preserved by the stabilizer of
the distinguished binary factor \(p\), so these are exactly two nonzero
orbits.

If \(G_2=0\), the third component of the full map is linear.  The remaining
two components form a plane Keller map of degree at most four over
\(\mathbb C(r)\).  The unconditional low-degree plane theorem, after
algebraic base change, makes its function-field degree one.  The birational
Keller theorem then makes the original map an automorphism.  This uses a
proved bounded-degree plane theorem, not the plane Jacobian Conjecture.

### 4.2 Unrestricted `qr` raw solve

Use the cubic monomial order
\[
(p^3,p^2q,pq^2,q^3,p^2r,pqr,q^2r,pr^2,qr^2,r^3)
\]
and the analogous six-term quadratic order.  Write the first two components
of \(H_3\) with coefficients \(u_0,\ldots,u_{19}\), the first two
components of \(H_2\) with coefficients \(v_0,\ldots,v_{11}\), and the
third row of \(L_0\) as \((l_0,l_1,l_2)\).  Set only
\((H_2)_3=qr\); all other displayed coefficients are initially
unrestricted.

The dependency-free determinant expansion finds that the complete \(E_6\)
linear system has rank \(14\) in the 23 variables \(u_i,l_j\).  Its
nine-dimensional kernel is
\[
\begin{gathered}
u_0=2u_{11},\ u_1=2u_{12},\ u_2=2u_{13},\ u_3=0,\\
u_4=-2l_1+2u_{15},\ u_5=2u_{16},\ u_6=0,\\
u_7=2u_{18},\ u_8=u_9=u_{10}=0,\\
u_{14}=l_0,\qquad u_{17}=l_2,\qquad u_{19}=0.
\end{gathered}
\]
After this substitution, the full sixteen-coefficient \(E_5\) table is
retained in the checker.  Its triangular square coefficients are
\[
6u_{11}^2,\qquad 6u_{13}^2,\qquad
6(2u_{11}u_{13}+u_{12}^2),
\]
so characteristic zero forces
\[
u_{11}=u_{12}=u_{13}=0.
\]
The remaining nonzero equations make exactly the six assignments
\[
\begin{aligned}
v_6&=l_0(u_{15}-l_1),\\
v_0&=2v_7-2l_0u_{16}+3l_1^2-4l_1u_{15}+u_{15}^2,\\
v_1&=2v_8-4l_1u_{16}+2u_{15}u_{16},\\
v_{11}&=l_2u_{18},\qquad
v_2=u_{16}^2,\qquad v_5=u_{18}^2.
\end{aligned}
\]
No parameter is divided out.

The source translation
\[
(p,q,r)\longmapsto
(p-u_{18},q-l_2,r+l_1-u_{15})
\]
means translation by the vector
\((-u_{18},-l_2,l_1-u_{15})\); its Taylor action leaves \(H_4\) fixed and
puts the solution into
\[
\begin{aligned}
H_3&=(2cpqr,\ r(ap^2+bpq+cq^2),0)^T,\\
H_2&=((2x-2ac)p^2+(2y-2bc)pq+c^2q^2+dpr+eqr,\\
&\hspace{28mm}xpq+yq^2+fpr+gqr,\ qr)^T,\\
(L_0)_{3\bullet}&=(a,b,0).
\end{aligned}
\]
The checker verifies the Taylor formulas coefficient by coefficient.  Thus
this is a quotient of the complete raw solution, not an ansatz.

With the first two rows of \(L_0\) still arbitrary, \(E_4\) contains
\[
[qr^3]E_4=(L_0)_{13},\qquad
[pr^3]E_4=-2(L_0)_{23}.
\]
Their vanishing kills the third column of \(L_0\), contradicting
\(\det L_0\ne0\).

### 4.3 Unrestricted `pr` raw solve

Starting instead with \((H_2)_3=pr\), the complete \(E_6\) system has rank
10.  It is equivalent to
\[
\begin{gathered}
u_0=u_1=u_2=u_3=u_6=u_8=u_9=0,\\
u_4=2l_0,\qquad u_5=2l_1,\qquad u_7=2l_2,
\end{gathered}
\]
with the entire second cubic component unrestricted.  The full \(E_5\)
table has only four nonzero coefficients and gives
\[
v_0=l_0^2,\qquad v_1=2l_0l_1,\qquad
v_2=l_1^2,\qquad v_5=l_2^2.
\]
Translation by \((-l_2,0,-l_0)\) produces exactly
\[
\begin{aligned}
H_3&=(2\tau pqr,U,0)^T,\\
H_2&=(\tau^2q^2+Dpr+Kqr,V,pr)^T,\\
(L_0)_{3\bullet}&=(0,\tau,0),
\end{aligned}
\]
where \(U\) and \(V\) remain arbitrary and
\[
\tau=l_1,\qquad D=v_3-4l_0l_2,\qquad K=v_4-2l_1l_2.
\]
Again the checker verifies the exact Taylor action.

The recomputed \(E_4\) table is exactly the ten-entry table in the legacy
note.  If \(K=0\), it forces the first and third rows of \(L_0\) to be
supported on the same single column, so \(\det L_0=0\).  If \(K\ne0\),
\(E_4\) gives
\[
U=r(Ap^2+Bpq+\tau q^2+Cpr)
\]
and
\[
(L_0)_{1\bullet}=(KA,\tau D+KB,KC).
\]
The complete \(E_3\) table has the four coefficients
\[
-2K w_0,\quad -2K(-A\tau+w_1),\quad
-2K(-B\tau+w_2),\quad 2K w_5,
\]
so
\[
V=A\tau pq+B\tau q^2+Epr+Gqr.
\]
Finally \(E_2\) gives
\[
\begin{aligned}
(L_0)_{21}&=A(G-C\tau),\\
(L_0)_{22}&=E\tau+B(G-C\tau),\\
(L_0)_{23}&=C(G-C\tau).
\end{aligned}
\]
The remaining \(E_1\) identity vanishes under these assignments, while
\[
\det L_0=K\tau\bigl(-A(L_0)_{23}+C(L_0)_{21}\bigr)=0.
\]
Thus both nonzero exceptional orbits are excluded.

## 5. Replay results

From `dimension_three_keller_degree/rung2_degree_bound`, the following
completed with their unique terminal pass markers:

```text
/usr/bin/python3 taxonomy_freeze/verify_bridge_q2_e3_a1_b1_d1_n1_v1.py
taxonomy_freeze/replay_bridge_q2_e3_a1_b1_d1_n1_v1.sh
/usr/bin/python3 taxonomy_freeze/verify_hostile_bridge_q2_e3_a1_b1_d1_n1_v1.py
```

The replay wrapper ran:

- the bridge candidate checker;
- the legacy nonbinary SymPy check;
- the strict legacy nonbinary PARI/GP check;
- both binary exact implementations;
- both retained binary hostile implementations; and
- the binary false-pass suite.

The new checker printed

```text
PASS: independent hostile bridge reconstruction; 45 pivots + complete nonbinary raw orbit solves
```

Running it under `/usr/bin/python3 -O` stopped with

```text
RuntimeError: refusing optimized Python: fail-closed checks required
```

One minor harness weakness remains in the legacy
`verify_fixed_cubic_line_sympy.py`: it uses bare `assert` statements and has
no `__debug__` guard, so that individual legacy file must not be run with
`python -O`.  The supplied replay wrapper invokes ordinary Python, the PARI
check is strict, and the new independent checker is fail closed; this does
not affect the algebraic verdict but should not be hidden.

## 6. Certification implication and limits

This audit supports promotion of the bridge itself:

- `C00`--`C29`: pointwise covered by the uniform normal form and the
  exhaustive intrinsic split;
- `C30`--`C44`: empty;
- binary branch: retained hostile provenance and exact replay pass;
- nonbinary branch: historical standalone provenance absent, but freshly
  reconstructed and now retained here with an independent exact checker.

No status ledger was edited by this audit.  Full-row or global-taxonomy
promotion still requires the parent assembly to verify that the frozen
canonical-pencil theorem and the two cited low-degree/birational exit
theorems are valid dependencies in the project-wide proof graph.  This audit
does not claim that any `C00`--`C29` witness extends to a Keller map, and it
does not change the frozen denominator.
