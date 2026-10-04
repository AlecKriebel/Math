# Independent adversarial audit: Problem 2305066 / Function Theory 5.66

Audit date: 2026-10-04 UTC. Scope: frozen public package with SHA-256 manifest `adc5a1fd1921cd735eb6b02266e76e7748b79cffc73d2c49be6560b42877498a`.

## Verdict

**PASS at the explicitly stated published-theorem dependency level.** The exact question has a published negative answer. Recommend **already_solved**, **1/5 substantive attempt turns**, attribution **Kenneth Stephenson (1988)**. No new discovery or formal proof certification is established. No mathematical correction to the frozen proof is required. The original public package was not modified; no remote writes were made.

This audit was performed independently of the author. It included the complete frozen proof and controls, the original problem and update, the complete readable Stephenson article rather than its abstract, the relevant Bishop construction, a direct analytic check of the shift lemma, and exact replay. The remaining qualifications are provenance/representation limits, not an unresolved mathematical step.

## 1. Exact target and historical classification

I independently opened [Hayman and Lingham, arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2), checked the full Problem 5.66 and Update 5.66, and visually inspected a fresh rendering of printed p. 109 (PDF page 110). The question fixes an arbitrary infinite Blaschke product and asks for one positive neighborhood radius on which every fiber is infinite. The update explicitly gives a negative answer via dense finite fibers and a typical disk-automorphism shift. The denominator visibly contains the conjugate parameter. The update's unpublished attribution is stale relative to the 1988 publication; it is not evidence that the mathematical question remained open in 2018.

The recovered catalogue statement agrees with this primary source. Its prior open assessment is contradicted by the original update, so the status correction does not depend on guessing an intended variant of the problem. Adjacent Problem 5.65 is visibly different.

## 2. Published construction dependency checked

I independently retrieved and read [Stephenson's complete article text](https://www.academia.edu/60898917/Construction_of_an_Inner_Function_in_the_Little_Bloch_Space), including Sections 1–5 and references. The header identifies *Transactions of the American Mathematical Society* 308(2) (1988), 713–720; [DOI](https://doi.org/10.1090/S0002-9947-1988-0951624-3).

Construction check: the nested finite sets exclude zero and have dense union. Each finite generation has finitely many sheets. Zero survives on every sheet, while a designated point first removed at stage n survives only on finitely many earlier sheets. The tree-like gluing retains simple connectivity; its nonconstant bounded projection rules out parabolic uniformization. Section 3 chooses each generation length after estimating escape through the outer circle on an auxiliary covering. Shrinking neighborhoods of finitely many punctures have arbitrarily small hitting probability; sufficiently many generations capture arbitrarily much of the outer-circle escape probability. Exhaustion then gives innerness. Section 4 explicitly identifies infinitely many zeros and performs the Blaschke-shift reduction. These are the three properties used in the packaged theorem, not an inference from little-Bloch membership alone.

The source is OCR-bearing web text; its mathematical typography is imperfect, including some probability constants. The argument needs errors tending to zero, not their particular indexing. I did not obtain or visually inspect Stephenson's publisher PDF. The asserted input theorem is a faithful synthesis of the construction and Section 4, not a falsely quoted numbered theorem.

For independent published corroboration, I read [Bishop (1993)](https://www.math.stonybrook.edu/~bishop/papers/Indestructible.pdf), pp. 96 and 98–102, and visually inspected freshly rendered pp. 101–102. The preliminary construction on pp. 101–102 is explicitly an infinite Blaschke product and explicitly has finite fibers on the sets E_n, whose union is dense by the density condition on p. 100. Its harmonic-majorant estimate supplies a direct Blaschke variant of Stephenson's construction. The later modification begins only after that conclusion and produces an indestructible product. The frozen package correctly avoids assigning the preliminary finite-fiber property to the paper's final indestructible example.

The targeted title/author/problem searches located no invalidating correction. This is not an exhaustive literature certificate. All retrieved source bytes and rendered pages remain private and are excluded from the audit publication allowlist.

## 3. Independent analytic audit of the a.e. shift proof

The lemma needs planar almost-everywhere, not the stronger capacity-zero exceptional-set theorem. The proof correctly uses the nonnegative disk Green kernel to average over the shift parameter before passing to the boundary.

For s=|u|, the angular mean of the numerator logarithm is log max(rho,s); the denominator logarithm has mean zero. Integrating the two intervals [0,s] and [s,1] against 2 pi rho d rho gives (pi/2)(1-s^2) with the stated sign. The s=0 endpoint gives pi/2 directly. I also checked this radial identity symbolically, independently of the author's finite rational code.

For each parameter alpha, the shifted function is nonconstant and inner. Circular means of its logarithm are finite for every positive radius, even when the circle meets zeros: isolated logarithmic singularities are integrable. Subharmonicity gives monotonicity. Tonelli applies because the negative logarithm is nonnegative on the disk. The integrated circular mean tends to zero by dominated convergence applied to |f|^2, which is bounded by one and tends to one almost everywhere. Fatou can be applied along any sequence of radii increasing to one; monotonicity supplies the same limit for the full radial approach. Consequently the limiting negative mean vanishes for almost every parameter.

Canonical factorization then detects the singular factor correctly. For a zero at the origin its contribution is m log r. For nonzero zeros a_j the Blaschke contribution is the sum of log max(r,|a_j|), with multiplicity. For r bounded below, the absolute terms are dominated by -log|a_j|; this is summable because all but finitely many |a_j| exceed 1/2 and -log|a_j| <= 2(1-|a_j|) there. The Blaschke mean therefore tends to zero. The singular-inner factor has constant circular mean equal to minus its positive measure's total mass. Zero limiting mean forces that mass to vanish.

There is no impermissible dominated-convergence argument for log|f| itself. That distinction matters: a nonconstant zero-free singular inner function has boundary modulus one almost everywhere while its logarithmic circular mean remains strictly negative. The package avoids this trap.

## 4. Infinite product and fiber quantifiers

The automorphism and inverse formulas are correct for nonreal parameters. The denominator cannot vanish inside the disk. Exact fiber equality follows by applying the inverse automorphism, so finite fibers transport without any continuity or multiplicity assumption beyond analyticity. The image of a dense set is dense because this automorphism is a homeomorphism.

A good shift need not be zero and need not lie in the designated dense set. Indeed, a good shift cannot turn the constructed function into a finite Blaschke product: the shifted fiber over -alpha is precisely the original infinite zero fiber. Every nonconstant finite Blaschke product is rational and has only finitely many preimages of a fixed disk value. Constants are excluded by nonconstancy. Therefore every good shift used here is an infinite Blaschke product.

The same fixed shifted product is used for all radii. For every delta>0, its dense finite-fiber set meets the nonempty punctured disk 0<|w|<min(delta,1). This is exactly the negation of the proposed universal neighborhood statement. Choosing one such value for each 1/n gives a nonzero sequence tending to zero. No selected value equals zero, since an infinite Blaschke product's zero fiber is infinite.

An infinite Blaschke product has infinitely many distinct zeros: multiplicity at any interior zero of a nonzero analytic function is finite. Likewise, a finite fiber has finite total multiplicity. The proof does not confuse distinct preimages, multiplicity, or an infinite number of artificial repeated product factors. A finite fiber is allowed to be empty, as in the original question.

## 5. Rouché finite-level lemma

For each fixed positive integer N, select N distinct zeros. Finitely many small pairwise disjoint closed disks around them can be chosen inside the unit disk, with zero-free boundaries. The minimum boundary modulus is positive. For every |w| below this minimum, Rouché's theorem gives at least one zero of B-w in each disk. Disjointness gives N distinct preimages, even if an individual original zero has multiplicity greater than one.

This proves only a radius depending on N. Neither compactness of finitely many boundary circles nor pointwise divergence of fiber counts supplies one radius valid for all N. The author's scalar shrinking-radius negative control is a logical illustration; it does not pretend to construct the analytic counterexample. The fixed-B quantifier order is sound throughout.

## 6. Replays, freeze, and provenance

`independent_checks.py` replayed the author's exact controls and obtained JSON equality with `CHECKS.json`: 69 grid points and 4,761 checks in each identity family, with all three negative controls passing. It also replayed `verify_manifest.py` and checked every one of the nine manifested files against the supplied frozen hash before and after execution. Additional independent symbolic controls checked the inverse, disk defect, difference identity, Green integral, and its center endpoint. These checks support implementation correctness only, not the infinite construction or limiting analysis.

The three available original source artifacts were independently rehashed and match the recorded byte counts and SHA-256 values. The Stephenson 24,026-byte artifact is a JSON-serialized web-tool textual response, not a publisher PDF, raw webpage file, or cryptographic authentication of the underlying original journal bytes. A separate fresh web retrieval was retained privately with its own hash; its response identifiers differ.

I independently rehashed the recovered 69,291,427-byte problems corpus and reproduced SHA-256 `37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252`. Its selected record exactly matches the private selected record. It does not match the repository's pinned 68,931,837-byte problems snapshot, as already disclosed in the frozen package. This limits snapshot provenance; the exact mathematical target is independently established above.

The full claimed 80,334,822-byte research-results corpus was unavailable to this auditor. Its matching hash remains an author-recorded observation, not an independently replayed one. A smaller same-named file was rejected as a substitute. This qualification should accompany the audit; copied metadata is not a fresh hash check.

I inspected the preserved main-reference, queue, state, attempts-list, PR-search, and related-target-group artifacts. They agree with the author's point-in-time claims relevant to this ID. I did not repeat current remote duplicate searches and make no concurrency guarantee. Source retrieval failures, corpus mismatch, and the difference between finite controls and analytic proof are disclosed rather than treated as successes.

## 7. Release recommendation

The source-backed mathematical result passes. Preserve the original attribution and dependency caveats; retain `already_solved` and the one-turn attempt accounting. This independent audit is quality assurance, not a new substantive proof-search attempt. Keep the frozen package intact and attach these findings separately. See `CORRECTIONS.md` for nonblocking precision suggestions and `AUDIT_CHECKS.json` for replay results.
