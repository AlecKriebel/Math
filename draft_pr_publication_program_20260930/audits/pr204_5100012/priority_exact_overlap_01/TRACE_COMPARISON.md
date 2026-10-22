# Comparing the centered trace factors

Authored derivation, 2026-10-16 10:06:26 UTC. This is a priority-comparison note, not a manuscript and not a novel-formula claim. Root supplied the candidate identity; this audit checked the algebra independently against the complete original Ferudun PDF and PR204's original proof.

Use outer semiaxes a>b>0, caustic semiaxes a_c=sqrt(a²-lambda), b_c=sqrt(b²-lambda), k²=(a²-b²)/(a²-lambda), k'=b_c/a_c. Let 0<v<K satisfy sn²v=lambda/b². Then

    cn²v=(b²-lambda)/b²,
    dn²v=a²(b²-lambda)/(b²(a²-lambda)),
    W(u)=a²-(a²-b²)sn²u,
    delta=2v.

Addition and the real quarter-period identities give the meromorphic identity

    dn(u+K-v)+dn(u+K+v)
      = 2k' dn(v) dn(u)
        / [dn²u-k²cn²u sn²v]
      = 2ab dn(u)/W(u).                              (1)

The denominator in the middle expression equals cn²v W(u)/(a²-lambda). The remaining positive constant k' dn(v)(a²-lambda)/cn²v equals ab. These equalities follow by direct substitution of the three displayed parameter relations. They hold first away from poles and then meromorphically.

For a closed physical N-orbit, delta=4K tau/N, so shifting the summation index by one shows

    sum_j dn(w+j delta)/W(w+j delta)
      = (1/(ab)) sum_j dn(w+K+v+j delta).              (2)

Indeed the two sums from the left side of (1) become equal after the index shift j -> j+1, since the arguments differ by delta and N delta=4K tau. This step needs closure, but no parity restriction.

Ferudun's centered Lemma 3, equations (4) and (8), gives

    A_O(w) = sqrt(lambda) sqrt(a²-lambda)
             [(a²+b²)a²b²-lambda(a⁴+b⁴)]/(2a²b²)
             * sum_j dn(w+j delta)/W(w+j delta).

Combining it with (2) gives PR204's normalization

    A_O(w) = C_T S(w+K+v),
    S(z)=sum_j dn(z+j delta),

    C_T = sqrt(lambda) sqrt(a²-lambda)
          [(a²+b²)a²b²-lambda(a⁴+b⁴)]/(2a³b³).        (3)

This is exactly the coefficient in T(u)=C_T S(u+K), because the original proof's contact phase is u=w+v. Its bracket exceeds b⁴(a²-b²)>0 because lambda<b², so C_T>0 throughout the admitted domain. The original proof allows zero C_T without harming its argument; the explicit primary formula shows that zero does not occur here.

The finite diagnostic compare_trace.py checks two exact symbolic residuals, sixteen real pointwise evaluations, and direct original-Q signed areas for nine closed parameter pairs: (N,tau)=(3,1),(4,1),(5,1),(5,2),(6,1),(8,1),(8,3),(10,3),(12,5). The latter include wrong-parity cases to check the trace identity separately from product constancy. At 75 decimal digits all coefficient discrepancies are below 6e-72. These are noninterval diagnostics; the derivation above supplies the general identity. Existing read-only SymPy/mpmath runtime was reused with bytecode disabled. The initially selected bundled PDF runtime lacked mpmath; no installation or package copy was performed.

Priority consequence: an explicit residue evaluation or formula (3) is not presently supportable as a new mathematical contribution; it follows from the exact overlapping primary preprint by a standard Jacobi addition identity. The direct-Q/local-Laurent proof and the reflection-telescope proof are differently organized proofs of the same trace relation. The later arbitrary-point paper also explicitly uses the adjacent-term cancellation (Lemma 4.3, pp.9–10), further limiting any new-method claim.
