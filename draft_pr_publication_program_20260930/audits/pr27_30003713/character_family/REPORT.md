# PR27 character/sign-family independent adversarial report

**Mathematics: PASS for the explicitly known partial scope. Publication packet: REPAIR_METADATA. Full OWR target: unresolved in this investigation.**

Audit UTC: 2026-10-01T22:29:47.105184+00:00. Exact reviewed head: `84d7f6103b087e431d7afb751501380ebd7ffd42`; base `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`. The thirteen attempt files were independently read from Git, hashed, and compared with the frozen source snapshot. Every comparison passes. The separate QUEUE change is also reviewed. No original bytes, canonical state, Git refs, PR, release, or publication settings were changed by this family.

## Independence and exact criterion

The source-first reconstruction was sealed before reading PARTIAL.md, historical reviews, their scripts, basis/QUEUE, root notes, or sibling work. See SEALED_RECONSTRUCTION.md, SHA256 `8f4a25bd60b680368201857ce3445054a3665688bf6f81e6058aa97556b480db`; evidence/seal.json records the order. Source PDF scratch and replayed copies are ignored. This family did not import supplied code or request outside input.

[OWR 2/2018](https://ems.press/content/serial-article-files/46724), printed p.118, Question13, asks for all homology of Lie(V) tensor (C direct-sum E), square-zero E, arbitrary finite-dimensional complex E,V, expressed as a sum of polynomial functors in both variables. This is stronger than the imported record's “preferably.” A named action-map kernel, Euler character, fixed-dimension rank table, or bounded homogeneous band is insufficient. The entire note preserves this distinction.

The ordinary free Lie algebra and ordinary tensor/exterior powers are used. Fixed V-degree pieces are finite, but their sum over degrees is the analytic functor evaluated on V; no completed product, completed tensor power, or topological Lie homology is silently introduced. The target contains no completion hypothesis.

## Universal representation mechanism

Write g=Lie(V), I=g tensor E. Since I is abelian, CE(g semidirect I) decomposes as the direct sum of CE(g;exterior^r I) shifted by r. Brackets of two ideal entries vanish; brackets of a quotient entry with an ideal entry preserve the ideal count. The actual direct decomposition avoids any unexamined spectral-sequence extension.

The augmentation resolution of T(V)=U(g) has length one. For coefficient module M, the homology is kernel/cokernel of V tensor M -> M and vanishes above coefficient homological degree one. For M=g^tensor r, the map is the sum of ordinary adjoint actions on the r tensor positions, with S_r acting by ordinary place permutations. Calling the kernel K_r and cokernel Q_r, one gets the actual current-algebra groups by the exact characteristic-zero coinvariant operation

    (K_r or Q_r tensor E^tensor r tensor sgn_r)_(S_r).

The exterior sign has exactly one copy. Trivial S_r coefficient representations produce exterior^r E; sign S_r representations produce Sym^r E. This is a derived identification, rather than an inference from dimensions.

[Powell v4](https://arxiv.org/abs/2507.03453v4), pp.1–2 and 5–6, uses this ordinary coefficient-permutation action. Proposition3.3 gives K_r[d]=0 for d<=r, and K_r[r+1]=Sym^(r+1)V tensor triv_r. Theorem1 gives, for r>1,

    K_r[r+2] = exterior^(r+2)V tensor sgn_r
               direct-sum S_(r,1,1)V tensor triv_r.

The exceptional r=1 has only exterior^3 V; r=0 has zero at V-degree2. After exteriorization, the note's equations(4)–(5) are exactly

    exterior^r E tensor Sym^(r+1)V,
    Sym^r E tensor exterior^(r+2)V
      direct-sum exterior^r E tensor S_(r,1,1)V  (r>1).

At r=1 the sole next-band term is E tensor exterior^3 V. The second summand cannot be retained by formal substitution: both partitions coincide and that substitution doubles the answer. Vanishing when the partition length exceeds dim(E) or dim(V) follows automatically upon evaluation. Scalar extension from Q to C is exact in every homogeneous piece.

[Powell's Example3.1](https://arxiv.org/abs/2507.03453v4) supplies the exact bracket sequence. For d>=2, Jacobi and antisymmetry rewrite Lie monomials as sums of brackets with a generator, so V tensor Lie_(d-1)V -> Lie_d V is surjective. Its kernel is CycLie_d, with Frobenius characteristic p1*l_(d-1)-l_d, where l_d=(1/d)sum_(a|d)mu(a)p_a^(d/a). This is an actual kernel character, not a cancellation assumption. The d=2,3,4 modules are S_(2), S_(1,1,1), S_(2,2). E-degree1 gives E tensor CycLie(V) in H2 and E tensor V in H1, for any dimension of E. It does not determine the full dim(E)=1 specialization; higher ideal counts still occur there.

The character identity [Q_r]=[g^tensor r]-[V tensor g^tensor r]+[K_r] becomes sufficient for Q_r only after K_r is independently known. It cannot compute both unknown groups from Euler data. The note correctly stops at the general Schur-kernel problem.

## Source conventions and attribution

[Powell's 2023 paper](https://arxiv.org/abs/2309.07607), introduction and principal DG-category/two-term-complex statements, describes structure rather than a claimed all-degree irreducible decomposition. [Gadish–Hainaut2024](https://ahl.centre-mersenne.org/item/10.5802/ahl.213.pdf), sections1.3,4.4 and Conjecture6.7, describes complete computed composition factors through n<=10 and additional families. It includes its associated-graded/extension qualification. Its Phi1[r+2,r] convention carries conjugate partitions on both group factors relative to Powell's Lie-homology convention; Powell explicitly explains the two sign changes. That dictionary must not be copied into the present exterior answer without translation.

The publication metadata [publisher page](https://www.tandfonline.com/doi/abs/10.1080/10586458.2025.2608243) gives online4March2026, DOI10.1080/10586458.2025.2608243. [Powell's author homepage](https://math.univ-angers.fr/~powell/home/publi/) corroborates Experimental Mathematics(2026). Publisher full-body retrieval returned403. The mathematical body audited here is the exact 16December2025 author v4, not a purported independently checked publisher PDF. That author's PDF reproduces the old packet hash exactly.

The [2017 primary question and comments](https://mathoverflow.net/questions/273196/homology-of-an-interesting-lie-algebra) already contain the exterior/Schur coefficient reformulation and the tensor-algebra two-term resolution/Whitehouse observation. The package's nonnovel attribution is supported. This bounded source audit provides no exhaustive literature absence or worldwide novelty claim.

Two historical-source qualifications remain. The GH2024 and Powellv4 PDF hashes reproduce exactly. The presently retrieved OWR URL gives734914bytes, SHA25691efb3f45550efd99cbae32c72001ea6b8d40fd0a9c1301c2f524398f9530de5; the historical receipt lists654519bytes, SHA2569d4c4b3ece921051f15c24c23b911839ed968607225fe9244b409960658065be. The historical file is absent and the receipt supplies no per-file URL, so the discrepancy is unclassified: a source variant can explain it, but it is not an exact reproduced historical download. The original printed claim is independently confirmed. Preserve the historical receipt and add current per-URL provenance rather than silently replacing it.

## Independent computation and falsification

Both historical scripts were replayed only in ignored exact-Git copies using /usr/bin/python3 and SymPy1.14.0. The author receipt (nine adjoint ranks plus52 abelian identities) and reviewer receipt (nine exterior-action models plus three character identities) both reproduce byte-for-byte. Commands, receipt hashes and execution logs are preserved in evidence/replay_results.json and the two replay logs.

The new character_controls.py has no author/reviewer imports. It uses multilinear right-comb Lie bases ending in the least label; their distinct associative words ending in that label give coordinates. Antisymmetry/Jacobi give spanning, and the number of independent right-combs is (k-1)!, the multilinear Witt dimension. Every coordinate reduction used in the check is verified by rebuilding the full tensor-algebra expansion.

It builds ordered coefficient tensor products with every generator label used once, constructs the action matrix, and computes its exact rational kernel. It then independently implements S_d relabeling (including the distinguished source generator) and ordinary S_r place permutations, checks action-map equivariance for every pair of conjugacy classes, verifies kernel invariance, computes restricted traces, and decomposes them by exact character inner products using the Murnaghan–Nakayama rule. This checks representation structure rather than merely specializing E,V and counting dimensions.

Thirteen models pass153 simultaneous class-pair controls:

| r | d | kernel dimension | actual S_d x S_r decomposition |
|---|---|---|---|
|1|2|1|S_(2) x triv1|
|1|3|1|sgn3 x triv1|
|1|4|2|S_(2,2) x triv1|
|1|5|6|full cyclic-Lie character and exact inner products|
|1|6|24|full cyclic-Lie character and exact inner products|
|2|2|0|zero|
|2|3|1|triv3 x triv2|
|2|4|4|S_(2,1,1) x triv2 plus sgn4 x sgn2|
|3|3|0|zero|
|3|4|1|triv4 x triv3|
|3|5|7|S_(3,1,1) x triv3 plus sgn5 x sgn3|
|4|4|0|zero|
|4|5|1|triv5 x triv4|

Full class values and multiplicities appear in character_results.json. Multilinear coefficients determine each tested characteristic-zero homogeneous functor; nevertheless the finite list does not establish unrestricted d,r. General formulas still rest on the sealed derivation and the cited theorem.

Four deliberate mutants are rejected: omit the exterior sign, introduce a sign into the ordinary coefficient-place action, permute coefficient labels while freezing the distinguished source generator, and add a second r=1 next-band summand. The first two have explicit nonzero transposition-character witnesses; the third fails multilinear preservation/equivariance; the fourth predicts2 instead of the actual1. The initial local checker run hit a Python float-zero bookkeeping error in an empty-kernel inner product; it was repaired by enforcing exact SymPy Rational. The failure log is preserved. No supplied artifact was modified during that repair.

## Complete packet and workflow audit

| Attempt file | Result |
|---|---|
|PARTIAL.md|All displayed mathematical claims and boundary distinctions match the independent reconstruction; qualified unresolved disposition retained.|
|README.md|Correct partial scope, reproduction commands, AI/unrefereed limitations; model information is historical self-report.|
|RESEARCH_LOG.md|Timestamped5%,10%,15% checkpoints; one substantive attempt and later audit checkpoint; percentages are planning estimates.|
|readiness.json|Exact stronger target and unresolved gap; current basis review hash matches; one-of-five ledger claim is local, not authoritative queue recording.|
|review/REVIEW.md|Mathematical arguments and finite-scope limitations valid; independent reviewer receipt replayed.|
|review/independent_checks.py|Exact rational exterior-action checks; no novel general calculation claimed.|
|review/independent_results.json|Reproduces byte-for-byte; its script hash matches the exact Git blob.|
|review/review_summary.json|Document/review hashes match; PASS_PARTIAL and no required math changes consistent.|
|source_checksums.json|GH/Powell exact; OWR historical source hash unreproduced, preserve with qualification.|
|source_record.json|Exact object match with current read-only basis; inherited2019 citation and “preferably” are stale metadata corrected in note, not authoritative source wording.|
|turns.jsonl|One blocked original attempt at2026-09-30T04:40:14Z,1/5, remaining gap explicit. This audit is not another proof-search attempt.|
|verification.json|Author receipt byte-for-byte replay passes.|
|verify.py|Correct finite adjoint/abelian sanity scope; no full decomposition certificate.|

Evidence/blob_provenance.json records every exact blob SHA1, SHA256 and byte length, snapshot comparison, the two-commit history, and complete changed-path list. PR base-to-head has only these13 files plus QUEUE. The document/review/script hash links match. Full runtime identity of historical model/reasoning settings is not independently proved by metadata alone; those labels should remain attributed self-reports.

The current read-only basis has review_hash0fb4d607f5e9cce2db158be17ff5c02f3b64ff2510ea911ed9b5c18490812ca6, matches readiness, and has empty prior_research. The historical desk note proposed exterior coinvariant calculations as a route; this audit confirms that naming those functors transfers the central difficulty to an equivalent unevaluated kernel. No independent complete mechanism appears in the note. Related-target metadata has no matching group.

A concrete bookkeeping defect exists at the exact PR head: QUEUE renders this target unsolved1/5, but state.json has no selected entry; history.jsonl is empty; catalog/ranking remain queued0/5; selected assessment history is absent. Regenerating QUEUE can therefore lose the purported used-turn count. The Git diff never modified those authoritative records. This is not a mathematical counterexample, but the publication packet should not claim a reproducible synchronized research ledger until the owner repairs it without resetting or spending an additional original research turn. See evidence/head_state_check.json and basis_budget_check.json.

## Exact verdict and remaining gap

No substantive mathematical correction is required for the frozen partial note. Do not promote this to a solution. The strongest verified result is the correct known semidirect/two-term reduction, all-V-degree E-weight-one CycLie layer, and explicitly credited relative-degree-one/two bands with the correct exterior sign and r=1 exception. The unrestricted Schur kernels remain unevaluated.

Required packet repairs: synchronize authoritative queue/state/history with the genuine historical attempt1/5, and append current source retrieval/body qualifications preserving all historical bytes. Any amended candidate needs a fresh current gate from the root reviewer. An optional wording improvement is to restrict the note's broad “current literature still computes...” sentence explicitly to the cited papers inspected; no worldwide absence conclusion is certified.

Audit complete100%; original discovery estimate15% is retained only as the historical planning estimate, not as evidence. No independent external individual was contacted, and no release/DOI was created.
