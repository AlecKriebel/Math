# Hostile audit of the post-freeze conic-double-cover bridge

**Audited row:** `Q2-E0-A1-B4-D2-N2`
**Recorded (UTC):** 2026-07-25T20:50:37Z
**Verdict:** **PASS**

The post-freeze bridge covers every point of the frozen inclusive row
`Q2-E0-A1-B4-D2-N2`, and the previously audited lower-degree calculation
then excludes every quartic Keller counterexample in that row.  This audit
promotes exactly one frozen row.  It does not alter the denominator, any
hashed freeze file, or the status of any other row.

The audit was reconstructed from the frozen tuple and the raw normal-form
problem, rather than by treating the bridge author's normal-form conclusion
as an input.  The work was AI-assisted, is not peer review, and makes no
priority claim.  Exact checks are evidence only for the encoded identities.

## 1. Audited inputs

The versions attacked here have the following SHA-256 hashes:

```text
41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d  FROZEN_TAXONOMY_v1.md
8aa1931b3c2ccd38c70408e15dc877b02ecf0f1656c3ecd27cc817dc51862b6d  BRIDGE_Q2_E0_A1_B4_D2_N2_v1.md
087f682b708e3c339eb6f315d517e861fac8af1a8d754620520da0cb76cedbad  ../WORKING_CONIC_DOUBLE_COVER_EXIT.md
884b37ffd54c4f27f834139cefd6ce345548f4f24f376f967201572537060577  ../verify_conic_double_cover_exit_sympy.py
bed2c80f1b73dcc92aac81e21148bf6cfa4584feea4a240dfef2e655c5985b33  ../audit_conic_double_cover_hostile/audit_conic_double_cover_pari.gp
823589455e7a812a1de24df5ce2b2e743f93b363a77ca5c2e8987db22b57d8d6  audit_bridge_q2_e0_a1_b4_d2_n2_sympy.py
```

The supplied bridge verifier is useful for hash and manifest replay, but by
itself it checks only the canonical endpoint and the presence of coverage
tokens.  It does not prove that every degree-two cover is in the asserted
orbit.  The independent derivation and exact Wronskian calculation below
were therefore required.

## 2. Independent reconstruction of the leading normal form

The frozen tuple is
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)=(2,0,1,4,2,2).
\]
The frozen canonical-pencil result gives
\[
H_4=A(p,q),
\]
where \(p,q\) are coprime homogeneous forms of degree \(a=1\), and \(A\) is
a primitive basepoint-free binary triple of degree four.  Coprime linear
forms are linearly independent.  Complete them by a form \(r\) to a basis
of the three-dimensional space of linear forms.  The corresponding source
matrix is in \(\operatorname{GL}_3\) and sends \((p,q,r)\) to \((x,y,z)\).
This proves that the \(a=1\) factorization becomes a binary quartic triple
without selecting or dividing by a frozen coefficient.

The reduced image has degree \(\delta=2\), so it is an irreducible plane
conic.  Over \(\mathbb C\), such a conic is smooth and a projective target
change identifies it with
\[
\operatorname{Ver}([u:v])=[u^2:uv:v^2].
\]
The remaining map \(f:\mathbb P^1\to\mathbb P^1\) has degree
\(\nu=2\).  Riemann--Hurwitz gives total ramification two.  Since every
ramification index is at most two, there are exactly two distinct simple
ramification points.  Their branch values are distinct: if both lay over
one value, the two local degrees would already give a fibre of degree four.

Independent source and target projectivities send the ramification points
and their branch values to the two coordinate points.  The following direct
calculation confirms that this leaves no modulus.  Write
\[
\begin{aligned}
B_0&=\lambda x^2+\rho xy+\sigma y^2,\\
B_1&=\tau x^2+\eta xy+\mu y^2.
\end{aligned}
\]
The two specified fibres give \(\sigma=\tau=0\), and basepoint freeness
gives \(\lambda\mu\ne0\).  The exact binary Wronskian is then
\[
\det
\begin{pmatrix}
\partial_x B_0&\partial_y B_0\\
\partial_x B_1&\partial_y B_1
\end{pmatrix}
=2\lambda\eta x^2+4\lambda\mu xy+2\rho\mu y^2.
\]
Ramification at both coordinate points forces
\(\lambda\eta=\rho\mu=0\), hence \(\eta=\rho=0\).  Therefore
\[
f([x:y])=[\lambda x^2:\mu y^2].
\]
An invertible target rescaling removes \(\lambda,\mu\) directly; no square
root choice is needed.  Composing with the Veronese embedding gives
\[
(\lambda^2x^4,\lambda\mu x^2y^2,\mu^2y^4),
\]
and the diagonal target matrix
\[
\operatorname{diag}(\lambda^{-2},(\lambda\mu)^{-1},\mu^{-2})
\]
gives exactly
\[
(x^4,x^2y^2,y^4).
\]

The target projectivity used on the parameter of the conic really extends
to \(\mathbb P^2\): for
\(M=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)\), its
symmetric-square matrix has determinant
\[
\det(\operatorname{Sym}^2 M)=(\det M)^3.
\]
Thus it is an allowed \(\operatorname{GL}_3\) target change whenever \(M\)
is invertible.

### Scalars, gcds, and the source basepoint

The original triple is primitive because \(e=0\), and invertible source and
target changes preserve primitivity.  The canonical triple is primitive as
well.  If two primitive triples over
\(\mathbb C[x,y,z]\) define the same projective rational map, all their
two-by-two cross-products vanish.  Writing their common fraction-field
ratio in lowest terms shows that its denominator divides every component
of one primitive triple and its numerator divides every component of the
other.  Both are therefore units.  The projective equality consequently
lifts to exact polynomial equality up to one nonzero constant, which an
invertible scalar target change removes.

There is an unavoidable codimension-two source basepoint:
\[
p=q=0,
\]
which becomes \([x:y:z]=[0:0:1]\).  The canonical triple has the same
basepoint.  This is not a hidden omitted case: it is not a component gcd,
does not affect the UFD argument, and is carried exactly by the source
change.  The phrase “basepoint-free” in the factorization applies to the
binary triple \(A\) on its parameter \(\mathbb P^1\), not to the induced
rational map from the source \(\mathbb P^2\).

This completes an independent proof of the exact leading normal form.

## 3. Frozen-pivot coverage

An irreducible plane conic spans \(\mathbb P^2\).  Hence the three component
quartics of any leading triple in this row are linearly independent.  In
particular, the first target component is nonzero in the fixed target
coordinates.  Its first nonzero monomial coefficient occurs among the
first block of fifteen coefficients, so
\[
R/\mathrm C_i=\varnothing\qquad(15\le i\le44).
\]

For every \(0\le i\le14\), take an arbitrary point of the stratum
\(R/\mathrm C_i\), if it is nonempty.  The reconstruction in Section 2
uses only:

- independence of \(p,q\);
- distinct ramification points and branch values;
- nonzero \(\lambda,\mu\); and
- invertibility of the selected projective transformations.

All are intrinsic consequences of the frozen tuple.  None is the condition
\(c_i\ne0\), and none can fail at a specialization that stays in the row.
The same pointwise construction therefore covers every nonempty
\(\mathrm C_{00}\)--\(\mathrm C_{14}\).

The construction does invert chosen \(\operatorname{GL}\) determinants, so
it is not a single division-free polynomial formula on the row.  That is
not a defect: the freeze expressly allows a coverage map as the alternative
to a division-free calculation.  Here every point of every nonempty pivot
stratum is covered, and the inverted determinants are nonzero by intrinsic
row conditions rather than by a hidden frozen-pivot assumption.

## 4. Transfer of the Keller and counterexample properties

Let \(S,T\in\operatorname{GL}_3(\mathbb C)\) be the source and target
matrices above and set
\[
F'(X)=T\,F(SX).
\]
The exact chain rule gives
\[
JF'(X)=T\,JF(SX)\,S,
\qquad
\det JF'(X)=\det(T)\det(S)\det JF(SX).
\]
Thus \(F\) is Keller if and only if \(F'\) is Keller.  Pre- and
postcomposition by polynomial automorphisms also gives
\[
F\text{ is a polynomial automorphism}
\iff
F'\text{ is a polynomial automorphism}.
\]
Invertible linear changes preserve exact total degree.  They send arbitrary
homogeneous lower terms of degrees two and three to arbitrary homogeneous
terms of the same degrees, and send the invertible linear part \(L_0\) to
\(TL_0S\).

Consequently the transformed map is exactly in the scope of
`WORKING_CONIC_DOUBLE_COVER_EXIT.md`: canonical leading term, arbitrary
quadratic and cubic terms, and arbitrary invertible linear part.  No lower
incidence condition is introduced by the bridge.

The pinned SymPy calculation and the independent PARI/GP reconstruction
were both replayed.  They exhaust the lower branches and end either in a
singular linear part or in the already banked bounded-degree plane theorem
plus a shear.  The latter theorem is unconditional and is not an assumption
of the plane Jacobian conjecture.

## 5. Exact replay

From `dimension_three_keller_degree/rung2_degree_bound`, the following
commands all passed:

```text
/usr/bin/python3 taxonomy_freeze/verify_bridge_q2_e0_a1_b4_d2_n2_v1.py
/usr/bin/python3 taxonomy_freeze/audit_bridge_q2_e0_a1_b4_d2_n2_sympy.py
/usr/bin/python3 verify_conic_double_cover_exit_sympy.py
audit_conic_double_cover_hostile/audit_conic_double_cover_pari_strict.sh
audit_conic_double_cover_hostile/audit_conic_double_cover_wrapper_selftest.sh
```

The independent bridge reconstruction emitted

```text
HOSTILE_BRIDGE_Q2_E0_A1_B4_D2_N2_SYMPY_PASS_5C1E7A
```

and a separate optimized-Python mutation test confirmed that it rejects
execution when Python assertions could be disabled.  The script itself uses
explicit fail-closed checks, not bare assertions.

## 6. Final disposition

No missing cover modulus, hidden scalar, component gcd, basepoint branch,
frozen coefficient chart, or lower-term specialization was found.  The
bridge is valid for the exact frozen row
`Q2-E0-A1-B4-D2-N2`.

\[
\boxed{\text{HOSTILE AUDIT PASS: this one row is certified excluded.}}
\]
