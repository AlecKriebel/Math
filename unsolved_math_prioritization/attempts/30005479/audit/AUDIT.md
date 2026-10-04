# Independent adversarial audit: 30005479

## Decision

PASS for the proposed `already_solved` disposition, with the existing attribution and qualification: a prior public affirmative argument by Alper Ferudun, dated 30 September 2026, is mathematically valid for every finite loopless matroid. The prior manuscript is expressly unrefereed and AI-assisted. This audit is an independent AI-assisted mathematical check, not human peer review or certification by a journal. No new theorem or priority is established here.

There are no required mathematical corrections to the frozen author packet. The equality for every nonoptimal partition is false, but the packet explicitly rejects that stronger statement and proves only the correct upper bound before obtaining equality for optimal partitions. This is not a counterexample to the selected theorem.

The proposed early stop after one substantive response is justified by the verified prior-resolution exception. It is not a claim that five distinct attempts were performed. The neighboring arbitrary-fan algorithm question is not resolved.

## Bound inputs and preservation

- Problem: 30005479 / OWR-12697711-015, queue rank 652.
- Frozen author manifest SHA-256: `4edef8fe79ffe05582edec1331e8aeff3df8a7e6382d5db824dc016cd8b7d7f8`.
- Frozen author archive: 13,788 bytes; SHA-256 `77707979f7580e313f138dd84b34a750f7eb325fecba599deed376ecb211c86a`.
- All 11 payload files match their manifest. The archive has precisely those files and the manifest under `author/`.
- All original author files and private inputs were preserved. No remote operations or helper-agent delegation were performed by this audit.

## Independent source inspection

The precise source statement on printed p. 857 of OWR 15/2023 was read from a fresh download and visually inspected. It has exactly the arbitrary-loopless-matroid, full ambient real-space, rationally-spanned-subspace and nonempty-partition scope used in the packet. The pinned target record was also read; its August literature assessment predates the September prior manuscript.

The whole 12-page Ferudun manuscript was independently re-extracted from the preserved PDF and read, including the full proof in Sections 2-3, its two-matroid consequence, nonmatroid-fan example, and scope/verification disclosures. This audit did not rely on the landing-page claim or prior audit reports as mathematical evidence. Direct repeat retrieval of EulerSolve returned HTTP 403, so the pre-existing PDF was used and its SHA-256 was rechecked against the recorded public metadata. A fresh indexed public landing-page result independently confirmed the manuscript title, author, 30 September release, version, DOI and unrefereed/AI-assisted status. This is a limitation on repeat retrieval, not a mathematical gap. The DOI archive bytes were not independently obtained or compared.

Fresh downloads of Bernstein, DEPRY, the OWR report and Antolini-Dewar-Tanigawa match the author packet's four PDF hashes and byte counts exactly. Bernstein's Theorem 3.5, Lemmas 3.3-3.4 and their proofs were read in the original source; the theorem page was also rendered and visually inspected. DEPRY Theorem 1.3.2 and its complete combinatorial proof in Section 3 were read, as were the relevant statements and scope distinctions in Sections 1.3-1.5. Antolini-Dewar-Tanigawa Theorem 2.7 and Section 6 were checked for the cited roles. Source URLs, versions, hashes, retrieval and inspection details are in `SOURCE_AUDIT.json`; no source text or source PDF is redistributed in the portable audit.

## Main theorem: independently checked proof

Let E be finite and nonempty, M loopless, r its rank function, and F the full Bergman support in R^E, retaining its lineality. Write its finitely many maximal cones as C_a and their real linear spans as L_a. Each cone is a convex polyhedral cone and has nonempty relative interior in its span. Thus a cone sum has dimension equal to that of the sum of its spans, and finite unions have maximum constituent dimension. Consequently

    D := dim(F+F) = max_(a,b) dim(L_a+L_b),
    dim(F+U) = max_a dim(L_a+U).

These are dimensions of polyhedral supports, not the dimension of their overall linear hulls. No claim that the union itself is a vector space is being made.

For any real subspace U, Grassmann's formula applied to L_a+U and L_b+U gives

    dim(L_a+U)+dim(L_b+U)
      = dim(L_a+L_b+U)+dim((L_a+U) intersect (L_b+U))
      >= dim(L_a+L_b)+dim U.

Take the maximum over a,b. This proves the universal lower bound D <= 2dim(F+U)-dim U, including irrational U. It neither assumes a maximizing cone pair works for every U nor interchanges a minimum and maximum.

Let p(S) be the minimum partition cost sum_B(2r(B)-1) on S, with p(empty)=0. DEPRY Theorem 1.3.2 proves that p is the rank function of a matroid on E. Its proof establishes nonnegativity, the singleton bound, monotonicity and submodularity by partition uncrossing. No realization is present in its statement or proof. Choose a basis I of this derived matroid. Then |I|=p(E), and every nonempty J subset I satisfies |J|=p(J)<=2r(J)-1.

Bernstein Theorem 3.5, with both matroids equal to M, implies that the coordinate projection of F+F to I has dimension |I|. His theorem is explicitly for loopless matroids of finite rank; linear-space realizability is only used later when applying it to Hadamard products. The opposite fan-sign convention simultaneously negates both summands and leaves dimensions unchanged. Projection cannot increase dimension, hence D>=p(E).

For a partition P of E into k nonempty blocks, take U_P spanned by their indicator vectors. Its dimension is k and it is rational. A maximal flat-chain span projects on block B into the span of the indicators of its intersections with B, including B itself. Every intersection is a flat of the restriction: for X=flat intersect B, closure_M(X) is contained in that flat, so closure_(M|B)(X)=X. After repetitions and the empty set are removed, those intersections form a strict nonempty-flat chain of length at most r(B). Their projected span therefore has dimension at most r(B). Since the coordinates of different blocks give a direct-sum ambient decomposition,

    dim(F+U_P) <= sum_B r(B),
    2dim(F+U_P)-dim U_P <= sum_B(2r(B)-1).

An optimal partition exists because E is finite. At such a partition,

    p(E) <= D <= 2dim(F+U_P)-dim U_P <= p(E).

Thus all quantities agree. The bound for arbitrary real U and this explicit rational minimizer establish the minimum over either real or rational subspaces, without invoking compactness or a density argument. This is the exact theorem requested.

## Adversarial checks of dependencies and scope

1. Bernstein's forest mechanism was checked, rather than treating the theorem's title as a scope guarantee. The combined flat-indicator matrix is transformed into a bipartite incidence matrix by taking successive flat differences. Changing signs on one vertex class identifies its real rank with graphic rank. A forest on an independent coordinate set supplies the required projected dimension.
2. Ferudun's reorganization of Bernstein's greedy construction was checked step by step. Matroid union supplies two covering bases. Each greedy removal assigns positions from the top; if neither one-sided removal is possible, the strict nonempty-subset inequality forces a common element. For each new edge, a putative earlier edge at its designated new endpoint would contradict the earlier nonclosure condition. Thus every step adds an unused endpoint and cannot create a cycle. Closure-lifting flags from the restriction to the full matroid preserves the endpoints of the selected edges. The audit code separately implements and tests this construction on all eligible subsets of every ordered pair of four-element loopless matroids.
3. Neither connectedness nor simplicity is required. Parallel classes, coloops and disconnected matroids are included. The special ten-element example is separately verified to be connected, to contain Fano as a restriction, and to have value 8 below min(10,2*5-1)=9.
4. Each full maximal cone has rank(M) dimensions, including the all-ones direction. Disconnected matroids may have larger common lineality; the proof still applies. Quotienting the all-ones direction without adjusting the formula would change its constants and is not done.
5. Empty E can be included with zero ambient space, F={0}, the empty partition and value zero. For nonempty E, looplessness implies positive rank and nonnegative nonempty-block costs. Matroids with loops are outside the target; their finite-coordinate Bergman support does not support the same unmodified statement.
6. The amoeba interpretation requires a complex linear space meeting the coordinate torus. The combinatorial theorem applies even when no such realization exists. An arbitrary nonlinear variety's coordinate matroid is insufficient for the same amoeba formula. Subtorus-orbit saturation is different from the stabilizer of the original variety.
7. Convexity and the finite cone-family condition suffice for the Grassmann lower bound, but equality with self-sum dimension is special. The nonmatroid K4 coordinate-plane example in the prior note correctly has strict inequality; it does not answer the neighboring general algorithm question.
8. The prior note's ancillary general-variety discussion is not a premise of the selected theorem. No unresolved claim from that discussion is imported into the author packet's proof.

## A nonblocking source-notation issue

Bernstein's Definition 2.6, on printed p. 6, displays the induced-matroid inequality with all subsets, without explicitly excluding the empty subset. For the function 2r-1 the value at the empty set is -1, so taking that display literally would rule out every nonempty independent set and contradict the immediately following examples. The intended condition is the standard one on nonempty subsets. This was confirmed visually, and the same nonempty formulation is explicit in Antolini-Dewar-Tanigawa Theorem 2.7 and Ferudun's Lemma 3.6. The author packet already states the condition correctly. Moreover, the independently checked forest construction proves exactly the nonempty-subset implication needed here, so the lower bound is not dependent on accepting an inconsistent literal display. This external notational omission requires no change to the frozen packet and does not alter the PASS decision.

## The nonoptimal-partition pitfall

The displayed per-partition equality in DEPRY Section 1.4 is too strong. For U_(2,4), take blocks {1,2} and {3,4}. The block-indicator space has dimension 2. Each maximal fan span has basis (1_E,e_i), and adding the block-indicator space gives dimension 3. The objective is therefore 4, whereas the block cost is 6. The actual minimum is 3, attained by the one-block partition. The optimal partition is not this two-block partition. This calculation was verified independently by exact elimination.

Only the upper bound for arbitrary partitions is used in the checked deduction. Equality at optimal partitions is a conclusion of the sandwich, not an assumed source identity. No correction to the target theorem or the packet is required on this account.

## Reproducibility and limitations

The supplied `verify_manifest.py` and `verify_dimensions.py` were run. The latter reproduces `check_results.json` byte-for-byte. Its stated counts are correct: 59 instances, all 27 labeled loopless four-element matroids, 3,717 full-partition evaluations, 130 rational-subspace samples and 590 incidence-versus-Gaussian-rank comparisons. The 59 are instances rather than a claim of 59 pairwise nonisomorphic or distinct matroids. The test implementation's local rank axioms, exhaustive basis-family generation, exact matrix elimination, graph-rank calculation, free extension and connectivity check were reviewed.

The separate `independent_verify.py` imports no author implementation or third-party code. It uses basis exchange to generate matroids, closure extensions to generate flags, exact RREF to identify repeated subspaces, and integer row elimination for dimension calculations. It does not use the author's bipartite-rank routine. Its expanded results are in `independent_results.json`; the concise verified counts are in `AUDIT_RESULT.json`.

Finite tests are regression checks, not evidence exhausting arbitrary matroids or arbitrary subspaces. The proof above supplies those quantifiers. No claim of human peer review, verified live UnsolvedMath status, independently matched DOI-archive bytes or exhaustive literature priority is made. This audit verifies the frozen mathematical packet and source assertions relevant to it; live repository duplicate checks and full dataset byte verifications were not repeated here.

## Corrections and publication guidance

Required corrections: none. Preserve the prior author's attribution, September date, explicit unrefereed/AI-assisted caveat, unavailable live-catalogue caveat, and absence of a new-priority claim. Retain `already_solved` as a workflow disposition based on a mathematically checked prior argument; do not turn it into a claim of refereed acceptance.

Portable files contain only this original audit, independently written tests, regression outputs, hashes, byte counts and public source metadata. Downloaded PDFs, extracted source text, rendered source pages, dataset records, raw retrieval content and private coordination files are excluded. The frozen author manifest and archive hash are bound in `AUDIT_MANIFEST.json`.
