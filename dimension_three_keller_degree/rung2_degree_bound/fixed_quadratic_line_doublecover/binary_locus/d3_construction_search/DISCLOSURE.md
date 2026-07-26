# AI assistance and verification disclosure

This note and its verification software were produced with substantial
AI assistance under human direction.

The full `D3-BB-21` descent and both structural-origin blocks were
checked in two independent implementations:

1. direct exact determinant expansion and coefficient extraction in
   SymPy; and
2. a separate direct PARI/GP reconstruction sharing no SymPy code.

The strict wrapper also contains required-failure mutations.  These
checks are evidence about the encoded algebra, not peer review.  The
coordinate and bounded-degree plane exits use established theorems and
remain subject to specialist review of their hypotheses.

The full `D3-BS-N2-Z` descent was also reconstructed directly in PARI/GP
by a hostile auditor.  That implementation rebuilds the weighted
determinant, tangent kernels, chart pivots, and origin solve without
calling the primary SymPy verifier.  Its fail-closed runner caught and
rejected a real GP syntax-error transcript that also contained a forged
success marker.

The result is deliberately narrow: it excludes a Keller counterexample
only in frozen families `D3-BB-21` and `D3-BS-N2-Z`.  It is not a proof
that all quartic Keller maps in dimension three are automorphisms, and it
does not improve the currently certified total-degree floor of four.
