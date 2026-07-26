# Post-freeze bridge audit: `Q2-E1-A1-B3-D3-N1`

**Verdict: PASS.**

The frozen row is exhaustively covered, including arbitrary lower
homogeneous terms.  It is safe to certify the row as excluded from a
degree-four Keller counterexample.  This means counterexample exclusion:
the aligned nodal proof allows Keller maps but proves that every one is a
polynomial automorphism.

No status ledger was edited.  No commit or push was made.

## 1. Audit scope and order

The audit began only from `FROZEN_TAXONOMY_v1.md` and
`frozen_manifest_v1.json`.  Before any legacy exclusion note was opened, it
derived and retained:

1. the intrinsic leading normal form;
2. the exhaustive node/cusp and aligned/transverse split;
3. the exact division-free map to every frozen coefficient pivot.

That clean-room phase is timestamped in `RESEARCH_LOG.md` and retained in
`PRELEGACY_DERIVATION.md`.  Only after it closed were the four legacy
theorems and their eight exact implementations inspected.

The frozen row is the canonical tuple
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)
=(2,1,1,3,3,1).
\]
The frozen source identifies it as the fixed-line rational-plane-cubic row,
and requires any local normal form to map back to the 45 coefficient pivots.

## 2. Intrinsic normal form

The tuple gives
\[
H_4=\ell A(p,q),
\]
where \(\ell\) is the exact linear component gcd, \(p,q\) are independent
linear forms spanning the canonical minimal pencil, and \(A\) is a
basepoint-free linearly independent triple of binary cubics birational onto
an irreducible plane cubic.

Equivalently, \(A\) is a projection of the rational normal cubic in
\(\mathbb P^3\).  A projection centre on the rational normal cubic gives a
basepoint and is forbidden.  A centre on its tangent developable but not
on the curve gives a cusp; a centre off the tangent developable gives a
node.  Over \(\mathbb C\), target and pencil-coordinate changes give
\[
\begin{aligned}
B_{\rm cusp}(u,v)&=(u^3,uv^2,v^3),\\
B_{\rm node}(u,v)&=(u^2v,uv^2,u^3-v^3).
\end{aligned}
\]
Thus, intrinsically,
\[
H_4=\ell\,M B_\tau(p,q),\qquad
M\in\operatorname{GL}_3(\mathbb C),\quad
\tau\in\{\mathrm{node},\mathrm{cusp}\}.
\]

There are exactly two incidences of the nonzero linear factor with the
two-dimensional pencil:
\[
\ell\in\langle p,q\rangle\quad\text{or}\quad
\ell\notin\langle p,q\rangle.
\]
These are respectively aligned and transverse.  Hence the four-way split
\[
\{\mathrm{node},\mathrm{cusp}\}
\times\{\mathrm{aligned},\mathrm{transverse}\}
\]
is disjoint and exhaustive.  It is independent of \(H_2,H_3\).

The legacy representatives use
\[
(p^2q,pq^2,p^3+q^3)
\quad\text{and}\quad
(p^2q,p^3,q^3),
\]
which are equivalent to the two clean-room representatives by a pencil
change and an invertible target permutation/scaling.

## 3. Exact frozen-pivot routing

Let \(g\) be the first component of \(M B_\tau(p,q)\), and write
\[
\ell=L_xx+L_yy+L_zz.
\]
The fifteen first-component coefficients \(d_0,\ldots,d_{14}\), in frozen
order, are the explicit bilinear polynomials displayed in
`PRELEGACY_DERIVATION.md`, equations (5)--(7).  They are obtained by direct
multiplication \(\ell g\) and use no division.

For \(0\le i\le14\),
\[
R/\mathrm C_i=
\{d_0=\cdots=d_{i-1}=0,\ d_i\ne0\}.
\]
For \(15\le i\le44\),
\[
R/\mathrm C_i=\varnothing.
\]
Indeed, \(M\) is invertible and the three binary cubic coordinates are
linearly independent, so the first row of \(M\) gives a nonzero cubic
\(g\).  Since \(\ell\ne0\) and the polynomial ring is a domain,
\(\ell g\ne0\).  A pivot therefore occurs in the first target component.

This is an exact coverage map to `C00`--`C44`; it is not a claim that all
of `C00`--`C14` are nonempty.

## 4. Four-way lower-term audit

All source/target changes used to normalize \(H_4\) preserve the Keller
property.  After them, the linear part is an arbitrary invertible matrix
\(L_0\).  The calculations below either start with fully general \(H_2,H_3\)
or prove the complete degree-eight form before introducing their
parameters.

### 4.1 Transverse nodal

`WORKING_NODAL_CUBIC_CURVE_EXIT.md` uses
\[
H_4=r(p^2q,pq^2,p^3+q^3).
\]
The degree-eight kernel gives the complete six-parameter form
\[
H_3=A_p(\ell+\alpha r)+A_q(m+\beta r).
\]
The \(r=0\) degree-seven square forces
\[
H_3=\lambda A+r(\alpha\partial_p+\beta\partial_q)A.
\]

The original two checkers only substitute the claimed later families,
despite the working note saying that they solve the raw systems.  This was
the smallest retained-evidence gap.  The new bridge checker closes it from
unrestricted coefficients:

- a general 30-coefficient cubic \(H_3\) gives an \(E_8\) matrix of rank
  \(24\); the displayed six-parameter family has rank six and spans its
  kernel;
- a general 18-coefficient quadratic \(H_2\) gives an \(E_7\) matrix of
  rank \(16\); the displayed two-parameter affine family solves it and its
  two tangent vectors span the full kernel;
- a general nine-entry \(L_0\) gives an \(E_6\) matrix of rank \(9\), so the
  displayed solution is unique;
- the determinant of that \(L_0\) and the full \(E_5\) square are reproduced.

The \(E_5\) square forces the parameter relation that makes
\(\det L_0=0\).  Hence no Keller map lies in this regime.

### 4.2 Aligned nodal

`WORKING_SCALAR_ALIGNED_NODAL_CUBIC_EXIT.md` keeps
\[
h=p+kq
\]
with arbitrary \(k\), plus the exchanged chart \(h=q\).  Thus it does not
silently identify inequivalent marked points.  Its degree-eight argument
gives
\[
H_3=V(p,q)+r(\alpha A_p+\beta A_q)
\]
with completely arbitrary binary cubic vector \(V\).

The full degree-seven system starts with all twelve coefficients of \(V\)
and all eighteen coefficients of \(H_2\).  Four polynomial left-null
certificates, valid at every specialization of \(k\), force
\(\alpha=\beta=0\).  The absence of a degree-one syzygy of the normal then
forces \(\partial_rH_2=0\).  Every nonlinear term is binary.

The resulting map is a degree-at-most-four plane Keller map plus a
triangular shear.  The established bounded-degree plane theorem makes it a
polynomial automorphism.  Thus this regime is excluded from counterexamples,
not asserted empty.

### 4.3 Transverse cuspidal

`WORKING_CUSPIDAL_CUBIC_CURVE_EXIT.md` uses
\[
H_4=r(p^2q,p^3,q^3).
\]
The ramified normal has a complete Hilbert--Burch module with syzygy degrees
one and two.  The note derives the complete degree-eight \(H_3\) family,
then starts the full degree-seven calculation with an arbitrary
18-coefficient \(H_2\).  Its raw matrix has rank \(14\), its three
compatibilities remove the two extra ramified parameters, and its
four-dimensional affine solution is recorded.  Degree six starts with all
nine entries of \(L_0\), has rank \(8\), and retains its one free entry.
The exact \(E_5\) and \(E_3\) factors then force \(\det L_0=0\).

Both supplied implementations reconstruct these raw matrices and lower
factors.  No Keller map lies in this regime.

### 4.4 Aligned cuspidal

`WORKING_SCALAR_ALIGNED_CUSPIDAL_CUBIC_EXIT.md` first computes the actual
stabilizer of the embedded cusp.  It is diagonal and has exactly three
orbits of a marked zero:
\[
h=p,\qquad h=q,\qquad h=p+q.
\]
This prevents an invalid full-\(\operatorname{PGL}_2\) normalization.

For every orbit the proof uses the complete degree-eight family
\[
H_3=V+r((ap+bq)S+cT)+dr^2S
\]
with arbitrary twelve-coefficient binary \(V\), and a general
eighteen-coefficient \(H_2\).  The raw rank-eight degree-seven systems and
their converses give:

- all binary-\(H_3\) leaves;
- one cusp-marked nonzero tangent leaf;
- two flex-marked nonzero tangent leaves;
- no general-marked nonzero tangent leaf.

The binary leaves retain the complete ten-parameter \(H_2\) family and end
either in a singular \(L_0\) or the constant \(E_5\) obstruction \(24\).
The three nonzero tangent leaves retain every free coefficient and end in
the parameter-free \(E_6\) obstructions
\[
-12,\qquad -48,\qquad 12.
\]
The SymPy checker reconstructs the raw systems, ranks, branch necessities
and converses; PARI/GP independently expands every terminal identity.  No
Keller map lies in this regime.

## 5. Fail-closed replay

`verify_bridge_q2_e1_a1_b3_d3_n1_v1.py` uses explicit failure checks rather
than Python `assert`.  It verifies:

- the frozen row tuple, all pivot IDs, and the frozen monomial order;
- the nodal/cuspidal implicit equations, singular tangent cones, component
  gcds, and coordinate independence;
- the division-free fifteen-coefficient routing formula and the empty
  `C15`--`C44` tail;
- the complete raw transverse-nodal \(E_8,E_7,E_6,E_5\) calculation.

`verify_strict.sh` then runs that checker, all four supplied SymPy
implementations, and all four PARI/GP implementations.  It requires exact
terminal markers, rejects a caller-supplied `PYTHONOPTIMIZE`, tests three
deliberate bridge mutations, and verifies that the bridge's explicit checks
remain active under optimized Python.

The retained strict result is

```text
Q2_E1_A1_B3_D3_N1_STRICT_PASS_V1
```

## 6. Conclusion and boundary

The intrinsic normal form reaches exactly four regimes.  The legacy proofs
cover all four, and their lower-term systems retain every allowed
coefficient.  The sole missing reproducible raw solve in the old evidence
was the transverse-nodal rank-\(16\)/rank-\(9\) calculation; the new bridge
checker reconstructs it and closes that gap.

Therefore:
\[
\boxed{\text{PASS: certify `Q2-E1-A1-B3-D3-N1` as counterexample-excluded.}}
\]

This is a retained exact audit, not peer review.
