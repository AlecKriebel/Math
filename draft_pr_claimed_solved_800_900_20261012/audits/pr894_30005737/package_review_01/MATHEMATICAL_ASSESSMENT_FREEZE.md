# Independent mathematical assessment, frozen before prior verdicts

UTC: 2026-10-16T08:24:07.276850+00:00. Review completion estimate: 20%. Candidate core: c06bf8dfd12c840d0f4af7af32ef6253de1c9f8d3b47f7a0618dedd7fd17ed2b. The complete 15348-byte note.tex was read, including every proof line and bibliography; no previous audit verdict has yet been read.

## Deduction checked independently

The transverse-pair theorem is correct under its stated finite-dimensional complex unimodular-source / semisimple-target assumptions. The proof does not rely on algebraicity of source images, source linearity, or surjectivity of either homomorphism. No unsupported equivalence substitutes for its central step.

Lemma 2: a nonzero solvable algebra has nonzero abelianization; choosing a functional on it gives an ideal of codimension one. Every one-dimensional complement is a subalgebra, giving the displayed semidirect sum. Exponentiating the derivation yields a C-action on the simply connected integration; uniqueness integrates composition, so the semidirect product is indeed simply connected. This proves contractibility by induction without asserting a globally bijective exponential map.

Theorem 1, integration: simply connected source integration is sufficient to integrate each homomorphism into simply connected N. The left-right formula is a true global action because right multiplication is by J2(h)^(-1) and multiplication reverses appropriately. No injectivity assumption is needed.

Infinitesimal formula: left-translating the curve exp(t j1(x)) p exp(-t j2(x)) by p^(-1) gives Ad(p^(-1))j1(x)-j2(x), with the signs as printed. At identity its derivative is the assumed isomorphism, so the identity orbit contains an open neighborhood and, by action translations, is open.

Covariance: for q=J1(h)pJ2(h)^(-1), q^(-1)=J2(h)p^(-1)J1(h)^(-1). Homomorphism equivariance gives j_i Ad_G(h^(-1))=Ad_N(J_i(h)^(-1))j_i. Multiplying B_p on the left by Ad_N(J2(h)) and on the right by Ad_G(h^(-1)) therefore gives exactly B_q, including the unchanged -j2 term. Taking determinant is valid between fixed equally dimensional vector spaces. A connected group character with zero Lie differential is identically one; unimodularity of g and perfectness of n give both required determinant characters. Thus f is invariant under the global action.

Global step: f is globally holomorphic even for nonalgebraic images. Its value is constant on the nonempty open identity orbit. The identity theorem on connected complex N proves global constancy; f(e) is nonzero. Thus all infinitesimal action maps are bijective and every orbit is open. More than one orbit would disconnect N because the complement of any orbit is a union of open orbits. This is a valid proof of transitivity rather than an assumption of completeness. It would not follow for an arbitrary smooth real function, which the note correctly excludes.

Covering: the stabilizer H is closed as inverse image of the identity under the continuous orbit map, and its Lie algebra is zero, so it is discrete. For sufficiently small U, U^(-1)U intersects H only in e, so quotient by right H is evenly covered by U h. A transitive smooth action identifies G/H with N. Connected total space over simply connected base makes this covering trivial. The resulting diffeomorphism is correctly not interpreted as a group homomorphism.

Topology: integrate the Levi action on simply connected R and S to reconstruct simply connected G as R semidirect S. This avoids unproved closedness of an arbitrarily selected Levi subgroup. R is contractible by Lemma 2, so G has the homotopy type of S and of its compact real form K_S. N similarly retracts onto K_N. Real dimensions of these compact forms are respectively complex dimensions s and d. Compact connected Lie groups are orientable by left frames, so H_d(K_N;Z)=Z. If rad(g) is nonzero, s<d and H_d(K_S;Z)=0. This contradicts the diffeomorphism. For s=0 the compact form is a point and d>0 still gives zero. For d=0 the separate case is correct.

Post-Lie corollary: PL2 makes L a homomorphism; PL3 puts L in Der(n). Innerness proof: tr([D,ad u]ad v)=tr(D[ad u,ad v]) identifies Du with [a,u] by nondegenerate Killing form. Center zero makes ad injective. Therefore R=ad^(-1)L is linear and R[x,y]_g={Rx,Ry}_n. PL1 says [x,y]_g={Rx,y}+{x,Ry}+{x,y}. Expanding {(R+I)x,(R+I)y} gives R[x,y]+[x,y], so both R+I and R are homomorphisms from g to n with difference I. No source/target reversal occurred. The adjoint trace vanishes on commutators, so perfect g is unimodular and the native statement follows.

Boundary example: for g=span(H,E,Z), [H,E]=2E and Z central, j1 maps its two-dimensional Borel part to H,E and kills Z; j2 maps only Z to F, an abelian line. Both preserve all brackets. Difference maps H,E,Z to H,E,-F and is invertible. Trace ad H=2, so unimodularity is essential. The example is not a counterexample to the theorem. Semisimple-source trivial products are allowed; reductive targets are not claimed.

## Assessment and remaining nonmathematical checks

No mathematical gap or counterexample was found. This is an independent informal proof check, not formal or human peer verification. Priority, reference accuracy, actual PDF correspondence, metadata, archive representation, and reproduction remain unassessed here. In particular, this assessment makes no novelty judgment, and no finite checker output is used as evidence of the global or topological deductions. Reading prior audits is now permitted for corroboration and adversarial comparison only.
