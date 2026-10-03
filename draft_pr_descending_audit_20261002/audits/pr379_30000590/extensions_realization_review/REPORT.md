# PR379: focused source-first extension and realization audit

Verdict: **PASS for the stated scoped results in Turns 4–5; no new mathematical repair required.** The original question is unresolved by this packet. The proposed five-turn count and `unsolved, 5/5` packet disposition are supported. This is an independent mathematical audit, not a certificate of current unsolved status, novelty, priority, human peer review, or a full solution.

Frozen target: PR379, problem 30000590 / OWR-1381-005, head `90794508688ec07f598e0871bbd1eb38aaf466ce`. SNAPSHOT_RECEIPT.json verifies all 56 supplied paths: 55 target artifacts and one QUEUE file, 515,878 bytes total. Every size and SHA-256 matches. The private copy was used for replay and remained unchanged. Recorded historical Git blob hashes also agree with the 43 supplied author/correction file bytes. No live Git ref, remote publication or service state was altered or independently certified.

## Independence, sources, and timing

The literal primary https://ems.press/content/serial-article-files/46073 was fetched first and the complete Davis contribution visually inspected at printed 2588–2590 / physical PDF 10–12. It fixes total cohomology with left regular coefficients and the commuting **right** group-ring action. Type FP is finite length with finitely generated projective LEFT terms resolving the trivial integral module. It is not merely FP-infinity or finite presentation; the target is neither abelian-group finite generation nor an ordinary cup-product algebra.

Before candidate mathematical inspection, the independently derived proofs, newly written exact code, complete 21,633-byte output, source bytes and research log were sealed at **2026-10-03T04:04:12.326557Z**. INDEPENDENT_SEAL_VERIFICATION.json confirms all ten sealed files remain unchanged. Before that seal, only the literal source, own source downloads, and SOURCE_MANIFEST/SOURCE_ADDITION_T4 source URL/hash metadata were read. The latter source metadata was accessed only after the literal primary pages. No candidate proof/code, final/historical verdict, root judgment or sibling judgment informed the sealed derivation. The root received only a progress message after sealing; no root or sibling verdict was received during this audit.

Fresh source hashes independently match four bound PDFs: EMS 46073; Sharifi Homological Algebra; Davis Infinite group actions on polyhedra; Davis Poincare duality groups. Relevant printed/physical source pages were read and rendered. SOURCE_RECEIPT.json records exactly what was and was not freshly verified. DDJO's companion paper and Davis–Okun's 2012 paper were not freshly fetched by this focused agent; their packet metadata was read and their source/priority coverage is outside this focused verdict. No historical literature completeness is inferred.

Both existing additive page corrections are correct and must stay effective:

- Sharifi Theorem 4.3.12 and its proof: printed **97**, physical PDF **97**, not the historical 86 in SOURCE_ADDITION_T4.json.
- Davis book FP definition: printed **229**, physical PDF **233**, not the historical printed 223 in SOURCE_SCOPE.md.

The Davis PD survey definition and finite-cd/direct-limit criterion were freshly checked on printed/physical 4–5. None of these locators changes the source hashes or the mathematics. Frozen historical notes were preserved.

## Extension closure: all high-risk obligations pass

Assume 1 -> N -> G -> Q -> 1, N is finite-length FP with finitely generated total regular cohomology, and Q is finite-length FP whose regular cohomology is concentrated in degree d, with Z-flat dualizing module D_Q. Candidate Turn 4 establishes this exact conditional theorem; it does not remove the flatness or concentration hypotheses.

The canonical action on A_q=H^q(N;ZN) is m*g=C_{g^{-1}}m, with C_g conjugating both inputs and coefficient values. The homogeneous inner-action prism implies C_n(m)=mn^{-1}, so this genuinely extends the original right N action. It obeys the needed semilinearity. The balanced bimodule map

    ZQ tensor_Z A_q -> A_q tensor_ZN ZG,
    q tensor m -> (m*lift(q)^{-1}) tensor lift(q)

has inverse m tensor h -> bar(h) tensor (m*h), is independent of lift, and retains both the left Q action and commuting right G action. This handles nonsplit extensions. Its right action is (q tensor m)g=q bar(g) tensor (m*g).

The finite-projective dual complex for Q is Z-free termwise. Its universal coefficient sequence has Tor_1^Z(H^{p+1}(Q;ZQ),A_q) in exactly the adjacent degree. Z-flat D_Q kills this term even if A_q has torsion, leaving only p=d. Naturality gives a spectral sequence of right G-modules. Every d_r, r>=2, has a source/target outside that sole column; no transgression survives. Each total degree has one associated-graded term, so an equivariant isomorphism follows without an unproved module splitting:

    H^{d+q}(G;ZG) = D_Q tensor_Z A_q,
    (u tensor m)g=(u bar(g)) tensor (m*g).

The dualizing module's finite generation follows by splitting the exact projective tail above degree d. The diagonal tensor is finitely generated from right Q generators of D_Q and right N generators of A_q using inverse lift transport. Finite cd and filtered-colimit compatibility prove G is finite-length FP by the explicitly bound Davis criterion. Thus none of the theorem's FP or module-action obligations is circular.

The independently derived pre-seal mechanism agrees with every material step. Post-seal mathematics extends its initially length-d phrasing to the candidate's arbitrary bounded quotient resolution through the same valid tail splitting. A further actual nonsplit Heisenberg extension computation gives regular cohomology Z in degree 3 with trivial right action. Ordinary trivial coefficients have a nonzero transgression and H^1 rank 2, falsifying a counterfeit coefficient-independent collapse. The toy nonflat tensor control is expressly algebraic and is not presented as an actual group counterexample.

## Bad matrix versus actual group cohomology: all high-risk obligations pass

For G=F(a,b) x F(c,d), the candidate chooses the height-kernel generators t=ac^{-1}, u=ba^{-1}, v=dc^{-1}. The independent derivation instead chose x=ab^{-1}, y=cd^{-1}, z=bd^{-1}. Both reconstruct H=ker(chi), where chi sends each of a,b,c,d to 1. The two free height kernels are countably generated, and stable-letter conjugation shifts the first index up and the second down.

The H_2 coinvariant orbits are indexed by the sum of the two indices. Finite support kills the H_1 invariant term. Hence H_2(H;Z) is a free abelian group with countably infinite rank, proving H is not FP_2. This is stronger and more appropriate than merely showing it is not finitely presented.

The right augmentation presentation over ZH therefore has a non-finitely-generated kernel. The ambient ring ZG is a free, faithfully flat LEFT ZH-module. Tensoring preserves the kernel, and the finite-coordinate faithful-descent argument prevents it from becoming finitely generated over ZG. This proves the explicit three-entry right-linear matrix has a bad kernel over the group ring of an actual finite-length FP group.

The independent and candidate matrices are related by mutually inverse generator substitutions x=u^{-1}, y=v^{-1}, z=u t v^{-1}. POSTSEAL_ADVERSARIAL_MATHEMATICS.md displays explicit inverse 3x3 group-ring matrices T,U with TU=UT=I and M_old T=M_new. Complete exact output for this comparison is in REALIZATION_COMPARISON_OUTPUT.json. These are actual noncommuting words, not an abelianized approximation.

Crucially, the SAME ambient G has its genuine LEFT free augmentation resolution of ranks 1,4,4 from the product of trees. The regular dual RIGHT complex has

    delta_0(f)_s=(s-1)f,
    delta_1(f)_{s,t}=(s-1)f_t-(t-1)f_s.

Each factor's delta_0 is injective by finite support, and its cokernel is Z-torsion-free by reducing the differential modulo m. Thus integral Kunneth proves H^0=H^1=0 and H^2=D_{F2} tensor_Z D_{F2}, generated by four right group-ring generators. This universally verifies the ambient positive case. The bad matrix is an induced augmentation syzygy of the non-FP_2 subgroup H. It is neither an identified ambient cohomology group nor the missing syzygy in an ambient augmentation resolution.

New exact computations record each genuine 2-cell boundary and its dual maps, right equivariance on nontrivial coefficients, the bad-matrix Fox cycle vectors, their full zero residuals, and negative controls. A fake same-factor 2-cell has residual ab-ba != 0. Wrong coefficient order and omitted product signs produce nonzero residuals. These checks would fail under a faithful group-ring implementation but can be hidden by an exponent-vector counterfeit. The universal proofs of contractibility, flatness, homology and non-finite generation remain the reason the infinite conclusions hold; enumeration is only a control.

## Complete frozen proof/code and replay comparison

After sealing, all five TURN proofs, all five checkers, the historical review proof/checker, portable verifiers, final result, historical state/logs and relevant nested bindings were read. The target QUEUE row says unsolved 5/5 and agrees with the current packet state. Its historical attempt-absence claims were not promoted to a complete independent prior search.

All five candidate outputs replay **byte for byte**, totaling **747,103** assertions (300,681; 46,264; 79,346; 83,797; 237,015). The old independent checker also replays **byte for byte**, totaling **23,463**. Each complete stdout and stderr is retained under private/replay_outputs, with hashes and comparison in CANDIDATE_REPLAY_RECEIPT.json. No checker writes the candidate; replay ran only from an isolated byte-exact copy.

The packet, historical review and publication verifiers all succeed. The present candidate verifier was run WITHOUT source-dir: it reports **0** source files checked and 68 ordinary file bindings. The complete old FINAL_REPLAY and old AUTHOR_REPLAY reports had respectively 34 and 74 file bindings, with six sources checked. Their replay arrays, assertion totals and 28 historical bindings agree; source omission and final-manifest timing explain the changed aggregate counts. They are not literal byte-identical verifier reports, and the present replay is not raw-source verification. Four fresh source recoveries are separately documented. The full source report from the historical candidate is preserved as historical evidence, not asserted to be re-performed by this agent.

## Strongest result, gaps, and repairs

Strongest independently verified result: conditional extension closure with the full right action and Z-flat quotient duality module, plus an explicit non-finitely-generated finite-matrix kernel in Z[F2×F2] whose ambient group has finitely generated regular cohomology. The independent and submitted examples agree by an invertible generator matrix.

Exact original gap: construct an actual FP group's finite-projective LEFT augmentation resolution whose regular RIGHT dual cohomology is not finitely generated, or prove that augmentation-resolution constraints always prevent such failure. Arbitrary noncoherent matrices do not realize this. Arbitrary quotient spectral-sequence kernels and actual integral Tor modules also remain uncontrolled outside the stated hypotheses. Neither this audit nor the candidate fills these gaps.

Mandatory new mathematical repairs: **none found in the focused claims**. Required preservation: keep both additive locator corrections, maintain the explicit regular/right-module/finite-length FP scope, retain all flatness and augmentation-realization limitations, and label replay source omission accurately. These are already satisfied in the frozen candidate; this audit adds evidence rather than a mathematical correction.

Generic coherence and arbitrary bad-matrix realization routes are marked blocked for the original target in the post-seal route ledger. Reopening them requires a materially new group-specific theorem or realization mechanism. Scope: independently checked mathematics, with no novelty or global literature certification. No outside individual was contacted, no outreach was prepared, and no Git/index/ref/candidate/service write was made.
