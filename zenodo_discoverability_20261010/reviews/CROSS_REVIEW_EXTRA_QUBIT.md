# Independent adversarial content review: additional qubit manuscript 21699069

**PASS — no blocking content issue.** Reviewed at 2026-10-10 14:21 PDT; 100% of assigned metadata-content cross-review complete. No proposal or remote record was modified by this reviewer.

The original public record is `papers/21699069/native_public_record.json`; the proposal is `patches/21699069.json`; the draft translation is `papers/21699069/native_target_metadata.json`. The deposited source is the line-numbered 251541-byte PDF `kriebel-2026-minimum-bell-setting-complexity-review-v1.1.0.pdf`. Independently calculated MD5 equals the public deposited MD5 `a5a7a0d08c99e864159de09a7866f6ab`. The matching extraction's title/author lines, abstract, Main Theorem, model/convexification definitions, contribution and proof roadmaps, Theorem 9.3/Corollary 9.4, operational limitations, AI/provenance and code-verification statements, and relevant references were checked. This is a manuscript-fidelity review, not independent verification of every mathematical proof.

## Content and boundary checks

The Main Theorem fixes bipartite local dimension at most two, arbitrary finite input-dependent output alphabets and shared-randomness convexification. It gives equality of the convexified two-input-per-party POVM and PVM behavior sets. A rational 3×2 Bell functional has a specific exact POVM lower bound above a global analytic PVM upper bound, making 3×2 the minimum input architecture up to party exchange.

The distinction among inputs, outputs and local dimensions is explicit. Definition 2.1 includes zero projectors and local stochastic postprocessing without enlarging local dimension. §10 excludes equality of raw nonconvex strategy images, same-state identification, operator-level POVM simulability, an exact global optimum claim, and a private-randomness entropy claim. The metadata description already preserves the consequential convexification and simulation qualifications, and the proposal leaves that description byte-for-byte unchanged.

The proposed sixteen subject tags are supported by the exact text. Bell nonlocality/inequalities, quantum correlations, qubits, POVM/PVM and nonprojective measurements are the central subject. Shared randomness, convex behavior sets and dimension-constrained correlations describe the actual observation space. Measurement-setting complexity names the result. The Lorentz cone/incidence model is used in the main proof. The explicit 3×2 construction combines CHSH locking with a three-state discrimination task (§1 proof roadmap and §3), supporting `state discrimination`. `Quantum foundations` is an accurate broader subject tag; it adds no theorem claim.

## Identity and related-resource checks

The current record is already classified as publication/preprint and contains one scholarly manuscript PDF. No software reclassification is proposed. The filename's “review” means a line-numbered review layout; neither the proposal nor the preserved description presents it as expert peer-reviewed work.

The primary record `21699161` has the same title, author, main theorem and mathematical manuscript. The tracked website `docs/papers/minimum-bell-setting-complexity/index.html` independently maps `21699161` to the primary publication DOI and `21699069` to the line-numbered review presentation; it supplies `review.pdf` separately. Therefore `isVariantFormOf` is a well-supported relationship between presentations. It is appropriately weaker than an identity-of-bytes assertion: the primary and review PDFs differ in line-numbering/layout, and the recorded extraction comparison finds a tiny matrix reading-order difference. No claim of exact PDF byte identity is introduced.

The source-release URL is already literal in the current description and is also listed in the tracked site as the immutable v1.1.0 source/verifier release. The paper website's canonical URL and title match this manuscript. The added scholarly DOI `10.1103/PhysRevA.82.062115` is exactly reference [4], Vértesi and Bene's *Two-qubit Bell inequality for which positive operator-valued measurements are relevant*, explicitly credited in the deposited abstract and introduction. The relationship is `cites`, preserving the paper's attribution to the earlier 3×2 existence result.

## Creator, provenance and protected fields

The correctly ordered native author name, given name, family name and existing researcher role are preserved in the native target. The only substantive author change is adding the human user's supplied ORCID `0009-0001-9320-500X`. No coauthor or affiliation is invented. English is added because the original record has no language entry and the deposited text is English.

The complete AI-assistance, human-responsibility and absent-independent-expert-review paragraphs remain unchanged. DOI, concept identity, version, publication date, rights, access, custom code-repository field and file identities are not part of the proposed content patch. Independent QA also verifies unchanged publication classification and exact native description preservation.

`CROSS_REVIEW_EXTRA_QUBIT_QA.json` binds the proposal and native target by SHA-256 and records all exact checks. The proposal is ready for the root's separate same-record native compatibility/publish/readback workflow. This review performed no Zenodo mutation and no external communication.
