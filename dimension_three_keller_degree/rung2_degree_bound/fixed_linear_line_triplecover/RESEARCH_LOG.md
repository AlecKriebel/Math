# Research log

## 2026-07-25T05:29:53Z

- Opened the taxonomy row
  \((e,a,b,\delta,\nu)=(1,1,3,1,3)\).
- On the transverse fixed-divisor locus, normalized
  \(H_4=r(A(p,q),B(p,q),0)\).
- Derived the exact dehomogenized Jacobian derivation
  \[
  D(G)=p^{d+5}s(ab'-a'b)(4s g_s-dg).
  \]
- The residue classes \(4j=3\) and \(4j=2\) have no integral solution, so
  the degree-eight and degree-seven identities kill the cubic and quadratic
  normal components.
- Reduced the remaining map to a degree-at-most-four plane Keller map over
  \(\mathbb C(r)\), hence to the birational Keller theorem.
- Kept the binary fixed-divisor locus explicitly outside the theorem.
- Added exact SymPy and PARI/GP verification.  Promotion is withheld pending
  an independent hostile audit.

## 2026-07-25T05:47:58Z

- Independent hostile reconstruction returned PASS.
- The audit retained all degree-three cover moduli and confirmed that no
  cubic left-right normal form was assumed.
- It recomputed the \(p^6\) cross product, the \(p^{d+5}\) derivation,
  both top polarizations, and the complete eigenvalue obstruction.
- It verified that the nonunit Wronskian cancels in the integral domain,
  that generic degree descends after the plane-field base change, and that
  optimized Python and injected GP failures are rejected.
- The transverse/nonbinary subrow is promoted.  The binary fixed line
  remains open.
