# Independent source, model and dependency-scope audit: PR 872

**Decision: PASS_TARGET_AND_DEPENDENCY_SCOPE. No source-scope blocker found.** This is not a mathematical acceptance of all proof calculations or a priority verdict. The affirmative outcome is conditional on those separate lanes. The explicit publication limits below must be retained.

## Frozen claim and independence

The target is problem 30006628 / OWR-14299911-031 at PR head `e3d77731b45b5f463df46e769faa01d65fe193ec`. The 19,961-byte `PROOF.md` has SHA256 `3bed7a81c5562d793bc4991fe62e1c06703818a9046495a7fe96d0b38e1ac100`.

I first retrieved the primary OWR and random-quotient PDFs, reconstructed their exact model, and saved `INDEPENDENT_TARGET_MEMO.md`. Only afterwards did I read the PR proof/README. I have not read either earlier mathematical-audit verdict. Later I read the original archive's source-pin metadata to reconcile independently retrieved bytes and corpus identity; its literature-search summary was not used as evidence for this decision. A parent reader subsequently independently supplied the same normal/cyclic thinning clarification.

## Exact target and model

The [published OWR report](https://ems.press/content/serial-article-files/53603), Problem 16, printed pp. 535–536 (PDF pages 49–50), asks for property (T) above density one third for at least three factors. The [EMS landing](https://ems.press/journals/owr/articles/14299911) dates publication to 21 July 2026, distinct from the February workshop.

[Random Quotients of Free Products v2](https://arxiv.org/abs/2502.08630v2), Definition 1.1, provides the precise model: fixed nontrivial finitely generated factors, specified finite generating sets and fixed positive integer ball radius; syllables are distinct nonidentity ball elements. Uniform relator draws are independent and with replacement from rooted, cyclically reduced normal-form words of exact syllable length. The PR uses this model and integer-part relator counts. No quotient by rotations, inverse classes, or alternative word representatives is made.

The actual fixed-parameter claim is every density in `(1/3,1)`, as length tends through all integers. It includes `d=1/2`; neither critical density `d=1/3` nor growing radius/alphabet/factor count is asserted. Torsion and infinite, non-finitely-presented factors are allowed. Nothing requires an algorithm for arbitrary factor word problems: the syllables are actual group elements in finite theoretical balls, and free-product normal-form uniqueness identifies the sampled words.

The proposed broader fixed finite inverse-closed generating-alphabet extension uses the same combinatorial model. Ball alphabets satisfy these hypotheses. Its additional generality does not narrow the original problem.

## Boundary cases and model traps

1. **At least three is essential for the stated all-length target.** Current v2 Definition 1.1 permits two factors; its Question 1.9 consequently has wider literal scope than OWR Problem 16. Take the two factors to be infinite cyclic. Every odd-length cyclically reduced relator universe is empty, so the quotient is the unchanged rank-two free group and maps onto the integers. It cannot have property (T). This is consistent with v2 Remark 1.3. The PR does not claim this false extension. A paper may describe the result as the at-least-three-factor case of Question 1.9, never as the complete literal unrestricted question. With three nonempty factor alphabets, cyclic factor strings exist at every length at least two; equivalently the factor-transition graph is primitive.

2. **All three length residues must be proved.** A result only along multiples of three would not imply the stated limit. The PR explicitly uses `(L,L,L)`, `(L,L,L+1)` and `(L,L+1,L+1)` block lengths. Its own mean-link and concentration calculations, not a blanket Gromov-model analogy, must establish their gaps. Those calculations are outside this lane's final verdict.

3. **With replacement is the exact source rule.** The notation `R` as a subset is accompanied by an explicit replacement instruction. Duplicate draws do not impose additional group relations but may supply repeated 2-cells/link edges. The supporting [Kotowski–Kotowski v2](https://arxiv.org/abs/1106.2242v2), p. 4, itself explicitly permits repeated IID relators and fixes integer-part rounding. No no-collision assertion has been used. In particular, one must not assert duplicate-free sampling at all densities merely because the relative duplicate count is small. This audit does not silently replace the random law by a without-replacement law.

4. **Free-group reduction is not a distribution theorem.** Property (T) passes to quotients, but a choice of free representatives for arbitrary ball elements need not produce uniformly sampled balls in free factors. The proposed proof avoids relying on that suggested shortcut. It constructs a triangular presentation directly over blocks of the actual alphabet and maps it to a finite-index subgroup of the desired quotient. Its deterministic map/index proof must be independently checked, as in the mathematical lanes.

## OWR's abbreviated normal-form definition: explicit robustness deduction

The OWR talk's §2.3 on printed p. 523 writes a normal-form word universe without expressly repeating the wrap-around reduction condition. The formal paper's Definition 1.1 in both [v1](https://arxiv.org/abs/2502.08630v1) and v2 uses cyclic reduction; v2 expands the definition into adjacent and last/first factor restrictions. The PR exactly follows that formal model. These two displayed universes should not be called equal.

Even the literal linear-normal-word reading of the workshop summary follows from the cyclic theorem by the following conditional deduction. Let `A` be the symmetric complete multipartite alphabet matrix, `lambda` its Perron eigenvalue, and `r` its positive unit Perron vector. These objects are determined by the fixed alphabet. For `n>=3`, primitivity yields

    T_l = 1^T A^(l-1) 1 ~ lambda^(l-1) (sum_a r_a)^2,
    Z_l = trace(A^l) ~ lambda^l.

Here `T_l` counts all linearly reduced words and `Z_l` counts the cyclic ones. Consequently `Z_l/T_l` tends to `lambda/(sum_a r_a)^2 > 0`. Among `floor(T_l^d)` independent uniform normal-form draws, the cyclic draws have a binomial count with mean asymptotic to a positive constant times `lambda^(d*l)`.

Fix any `dprime` strictly between `1/3` and `d`. With probability tending to one, there are at least `floor(Z_l^dprime)` cyclic draws, by the scalar binomial lower-tail bound. Conditional on the retained count, the retained words are still independent and uniform on the cyclic universe; that count is independent of their identities. Use the first prescribed number of cyclic draws. Their quotient has property (T) with probability tending to one if the PR's cyclic theorem is correct. The quotient using every originally drawn relator is a further quotient, hence also has property (T). This proves robustness to the abbreviated normal-word reading without asserting identical distributions and without a new central proof search.

## Exact dependencies and their hypotheses

**Triangular spectral criterion.** In Kotowski–Kotowski v2, §2.3 defines the degree-weighted normalized Laplacian for a multigraph, counting parallel edges. Definition 2.12 introduces its triangular presentation link and excludes loops by cyclic reduction. Theorem 2.13 assumes connectedness and normalized gap strictly above `1/2`; it does not require independent edges or a random-graph model. Its edge convention `{u,v^-1}` is transformed to the PR convention `{u^-1,v}` by global inversion of vertex labels. The graph spectra agree. The PR's formal inverse-pair alphabet and reduced block triangles are the relevant objects; original factor torsion is not a license to identify formal inverse vertices. Repeated triangular relators can be represented as repeated presentation 2-cells, consistently with the source's repeated-IID-relator convention and multigraph formulation.

**Quotient and finite-index transfer.** Remarks 2.10 and 2.11 in the same v2 state these permanence properties, with the latter referring to the standard property-(T) monograph theorem. This lane checked the exact statements, not a reproof of the book theorem. The triangular group is finitely generated for every fixed length even when original factors are not finitely presented.

**Matrix concentration.** [Tropp v7](https://arxiv.org/abs/1004.4389v7), Corollary 5.2, spans PDF pp. 20–21; Remark 5.3 supplies the simplified lower tail. The required matrices are a finite independent family of self-adjoint positive semidefinite summands, almost surely bounded by a deterministic operator-norm constant. They need not commute or be identically distributed. The PR applies the theorem on a deterministic common-kernel complement, which preserves these hypotheses; the ambient dimension can be replaced by an upper bound. Independence across sampled relators is sufficient; independence of a sample's three link edges is neither given nor required. Verification of the particular norm/mean-degree/gap estimates remains with the proof audits.

## Current versions, provenance and limits

Fresh retrievals match the original source pins for OWR, RQFP v2, KK v2 and Tropp v7; `RETRIEVAL_RECEIPTS.json` gives exact bytes/hashes. The current arXiv records report RQFP v2 on 28 September 2026 (PDF internally dated 29 September), KK v2 on 12 May 2012 and Tropp v7 on 15 June 2011. RQFP v2 retains Question 1.9 and is labelled to appear in Transactions AMS; this is a source-metadata observation, not a contemporary exhaustive openness/novelty certificate. RQFP v1's question was numbered 1.8 and its high-density theorem wording differs; no proof-body identity across revisions is assumed. Tropp's current arXiv metadata calls v7 its version of record. KK's exact v2 statement was read; an independently retrieved final journal body was not required or claimed to be identical.

The exact inherited problem record and report-pair hash reproduced as `f49c17584ada1a931294e4222414fc5b57ee1d60afca82d6818029457badf17f` from the complete 3,767-byte canonical pair, with a unique ID match and empty associated report object. The actual OWR question agrees. A fresh direct attempt at the target website returned HTTP 429, so live target content remains unverified. No raw corpus record, source PDF, extraction, webpage or page image is distributed in this public audit allowlist.

No full-paper priority search, novelty certification, formal verification, or external human peer review is claimed. This lane made no Git/queue/PR changes and no external communication. `MODEL_SCOPE_CHECKS.json` records 17 explicit gates and their exact limits. The main result can proceed to the other mathematical and priority gates without a source-scope repair, provided the at-least-three restriction, fixed-parameter limit and model conventions above remain explicit.
