# Post-freeze bridge for `Q2-E0-A2-B2-D2-N1`

**Recorded (UTC):** 2026-07-26T09:20:40Z.

**Certified after independent hostile replay (UTC):**
2026-07-26T09:43:40Z.  This promotes exactly the frozen conic-embedding
row.  The mutable global count is now
\[
5/14\text{ certified},\ 3/14\text{ provisional},\ 6/14\text{ open}.
\]
It does not change the frozen denominator and does not improve the universal
total-degree floor of four.

This note was produced with substantial AI assistance and is not peer
reviewed.  Exact checks are evidence about the encoded algebra, not peer
review or a priority certificate.

## 1. Exact scope

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have exact total degree four, with \(L_0\in\operatorname{GL}_3(\mathbb C)\),
and suppose its leading term lies in
\[
R=\texttt{Q2-E0-A2-B2-D2-N1}.
\]
Thus its canonical tuple is
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)=(2,0,2,2,2,1).
\tag{1}
\]
No condition is imposed on \(H_2\) or \(H_3\).

The only purpose of this certificate is to route every point of every
frozen coefficient-pivot piece \(R/\mathrm C_i\) to the intrinsic scope of
`WORKING_CONIC_TYPE_22.md`.  The lower exclusion in that note retains
arbitrary lower terms.

## 2. Uniform leading form

The canonical-pencil theorem gives
\[
H_4=A(p,q),
\tag{2}
\]
where \(p,q\) are coprime ternary quadrics and \(A\) is a primitive
basepoint-free binary triple of degree two.  The map
\[
[A]:\mathbb P^1\longrightarrow C\subset\mathbb P^2
\]
has image degree two and degree \(\nu=1\).  Hence it is the normalization
of the reduced irreducible conic \(C\).  Such a conic is smooth over
\(\mathbb C\), so this finite birational map is an isomorphism.

The three entries of \(A\) are linearly independent: otherwise \(C\) would
lie in a target line.  Since
\(\dim H^0(\mathbb P^1,\mathcal O(2))=3\), they are a basis of all binary
quadratics.  An invertible target change therefore gives the exact
polynomial normal form
\[
T H_4=\operatorname{Ver}(p,q)=(p^2,pq,q^2)^t.
\tag{3}
\]
No coefficient of \(H_4\), \(H_3\), or \(H_2\) is divided by in this step.

## 3. Why there cannot be two double-line members

For this frozen row,
\[
K_G=\mathbb C(p/q)
\quad\text{and}\quad
[E_G:K_G]=\nu=1.
\tag{4}
\]
Thus \(\mathbb C(p/q)\) is relatively algebraically closed in
\(\mathbb C(\mathbb P^2)\).

Suppose the pencil \(\langle p,q\rangle\) contained two distinct
double-line members \(L_1^2,L_2^2\).  They form another basis of the same
pencil, so a Möbius change of \(p/q\) equals
\[
\frac{L_1^2}{L_2^2}=\left(\frac{L_1}{L_2}\right)^2.
\tag{5}
\]
The coprimality of \(p,q\) implies that \(L_1,L_2\) are nonproportional.
Consequently
\[
\mathbb C\!\left((L_1/L_2)^2\right)
\subsetneq
\mathbb C(L_1/L_2)
\subset \mathbb C(\mathbb P^2)
\tag{6}
\]
is a degree-two algebraic extension in characteristic zero.  Equation (6)
contradicts (4).  Therefore the canonical pencil has at most one
double-line member.

This argument also explains the boundary routing: a presentation with two
double lines is not a point of this canonical row.  Recomputing the
relative closure lowers the pencil degree from \(a=2\) to \(a=1\), and the
point routes to a different frozen row.  It is not an additional leaf
inside \(R\).

## 4. Routing all frozen pivots

The conic \(C\) spans \(\mathbb P^2\), so the three component forms of
\(H_4\) are linearly independent.  In particular its first component is
not the zero polynomial.  With the frozen blocks of fifteen coefficients,
this gives
\[
R/\mathrm C_i=\varnothing\qquad(15\le i\le44).
\tag{7}
\]

For any \(0\le i\le14\), take an arbitrary point of the nonempty piece
\(R/\mathrm C_i\).  Apply (2)--(3), which uses only the intrinsic row
conditions, and then (4)--(6).  The result is a pair of coprime
nonproportional ternary quadrics whose pencil has zero or one double-line
member.  Thus the full frozen routing is
\[
\begin{array}{c|c}
R/\mathrm C_{00},\ldots,R/\mathrm C_{14}
  &\text{if nonempty, route uniformly to (3), with at most one double line},\\
R/\mathrm C_{15},\ldots,R/\mathrm C_{44}
  &\varnothing .
\end{array}
\tag{8}
\]
The construction never divides by the first nonzero frozen coefficient.
Every specialization preserving (1) remains covered; a specialization
changing (1) is routed by the frozen boundary rule.

## 5. Transfer to the existing exclusion

Put \(F'=TF\).  Then
\[
\det JF'=\det(T)\det JF,
\]
so the Keller property, exact degree, and polynomial invertibility are
preserved.  The transformed \(H_2,H_3\) remain arbitrary.

The theorem in `WORKING_CONIC_TYPE_22.md` starts with exactly (3), with
arbitrary lower terms, and excludes every coprime quadratic pencil having
at most one double-line member.  Its no-double-line and unique-double-line
branches are checked by the exact SymPy and independently written PARI/GP
implementations `verify_conic_doubleline_sympy.py` and
`verify_conic_doubleline_pari.gp`.  The two-double-line presentation is
explicitly identified there as nonminimal; (4)--(6) give the missing
canonical frozen-row reason.

The independent hostile replay reconstructed the previously prose-only
rank, kernel, cokernel, compatibility-ideal, and full-solution assertions
in the lower proof.  Therefore every point of
`Q2-E0-A2-B2-D2-N1` is excluded.

## 6. Reproduction

Run

```sh
./verify_bridge_q2_e0_a2_b2_d2_n1_v1_strict.sh
```

from `taxonomy_freeze/`.  The wrapper pins the frozen inputs and both
lower exact implementations, checks all 45 pivot labels, reconstructs the
Veronese and relative-closure obstruction, runs both lower checks, and
requires deliberate bridge mutations to fail.

The independent hostile replay is:

```sh
audit_bridge_q2_e0_a2_b2_d2_n1_v1/verify_independent_bridge_q2_e0_a2_b2_d2_n1_v1_strict.sh
```

Its final markers are
`INDEPENDENT_Q2_E0_A2_B2_D2_N1_AUDIT_PASS` and
`INDEPENDENT_Q2_E0_A2_B2_D2_N1_STRICT_PASS`.
