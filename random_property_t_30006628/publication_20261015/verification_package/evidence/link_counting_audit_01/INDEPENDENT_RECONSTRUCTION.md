# Independent reconstruction before inherited audit verdicts

2026-10-15 UTC; initial checkpoint: 25% of this assigned verification audit.

Read only frozen PROOF.md and the source manifest. No inherited AUDIT, SECOND review, checker, or verdict was read before this note.

For an original corner {u^{-1},v}, the ordered assignment x=u^{-1}, y=v makes the joining constraint A[f(x),f(y)]; the third block completes between l(y) and l(x), giving T_h(l(y),l(x)). Reversing the edge ordering gives T_h(l(x),l(y)); reversal preserves the inverse-fixed deletion and supplies symmetry. Thus each oriented type incidence contributes the same kernel. The coefficients are 6 in the equal case and [[2,2],[2,0]] or [[0,2],[2,2]] otherwise. Coincident formal vertices cannot be a loop because then A[f(x),f(x)]=0. Need independently enumerate to detect a missed orientation/multiplicity factor.

For fixed t,u, summation over a destination class gives lambda^{u-1} r_c r_f times lambda^{ell-t-u+1} r_b r_f times A[a,c]. The f sum is one; the c sum is lambda r_a. Hence degree scale lambda^{ell-t+1} r_a r_b h_t, and the class-walk ratio tends to (c_tu/h_t) P[a,c] r_f^2. This factorization cancels the differing exponential class sizes; using a uniform type measure instead would be wrong.

The type walk has eigenvalues 1 and -1/2 in either unequal residue. A has at most one positive eigenvalue by its quadratic form on sum(z)=0; connected nonbipartite complete multipartite A is primitive. Consequently P's nonprincipal eigenvalues are in (-1,0], and multiplying by -1/2 creates positive eigenvalues below 1/2. The maximum nonprincipal limit is rho/2, not zero in general. Equal residue's upper bound is zero, including the many zero eigenvalues off endpoint classes.

For odd length 2s+1 an inverse-fixed word has prefix s and a self-inverse middle letter; its endpoints are inverse in the same factor. Even length is impossible because its central pair would violate reduction. Thus the total deletion is O(lambda^s), and entrywise relative error against every positive Perron endpoint class is exponentially small for fixed A. This is not uniform in A: severely unequal part sizes can make rho close to one and finite-length convergence slow.

Remaining checks: construct independent direct relator enumeration with arbitrary within-factor inversion including torsion; compare every kernel entry for all three residues; verify endpoint compression/reversibility and limiting eigenvalue bounds; check explicit finite estimates and counterexamples to tempting shortcuts. No central proof search is being undertaken.
