# Independent acceptance audit: KP-3.41 / ID 2839

## Decision

Accept the exact frozen author package as **stalled partial, five approaches out of five**. It supplies correct elementary deductions and a properly bounded literature/gap analysis. It does not prove or refute the high-surgery conjecture, establish novelty, or certify the full proofs of the papers it invokes. The LOSS-dependent obstruction is conditional on the stated Li–Wan–Zhou preprint input.

No mathematical correction patch is required for the four stated deductions. The original archive and external manifest are preserved byte-for-byte. This audit adds an exact-byte acceptance verifier, stronger adversarial replay, and explicit scope qualifications. In particular, the wording about Golla's criterion must be read as a test of **nonvanishing of the specified contact invariant**. It is not an if-and-only-if criterion for tightness, even for that specified contact structure. The deductions in the report do not use that invalid converse.

Accepted original ZIP: 11,598 bytes; SHA-256 c19623ac22f119bf828875af3cb961e04c2d5679ddd7aa8dcdfdd135416e446a.

Accepted original external manifest: 1,322 bytes; SHA-256 be3be60e6fe3d89f6642a36f479160e783a5a0d062e450e47e2a3b8072ec8213.

The original STATUS.json field saying the independent audit is pending is historical frozen data. ACCEPTANCE.json records the present independent decision without rewriting that original.

## 1. Input identity and inherited-work gate

All bytes of the three supplied complete corpora were read and rehashed. Their sizes and digests agree with all three declared pins. The catalog's unique string ID "2839" and the problems corpus's unique integer ID 2839 agree on KP-3.41. Catalog rank 913 and the five-turn limit agree. The complete problem record was inspected, not just its statement or a summary. It contains ordinary descriptive background and an explicitly marked literature triage; the associated report value is empty.

The statement digest is 749b71051566bb470bb377e46477858e1f6506f8468ecea0fa5ba9fc46ea3e1f. Recomputing Python's default json.dumps([complete_record, reports.get(problem_number,{})], sort_keys=True), encoded as UTF-8, gives pair digest 4a4a4a2b98291ca38bfa7104b2da6bd6c979a4362baea22ebc1cb4bfbb3c156d. Both equal the catalog and author pins. INPUT_CHECKS.json contains only verification metadata, not the underlying records.

This confirms the inherited literature-triage-only gate. It cannot establish absence of unrelated prior work throughout the literature or repository. The author's bounded repository-search history is retained as historical metadata and is not silently promoted to a complete search.

## 2. Exact target and sign convention

K3 Section 3.5 requires the contact orientation to agree with the prescribed manifold orientation and uses the coorientable convention. Problem 3.41 asks for a knot-dependent integer threshold for an entire tail of surgery slopes. In the smooth Dehn-surgery convention, the finite slopes are rational, measured using the meridian and Seifert longitude. An integer threshold does not restrict the quantified slopes to integers. The author report correctly makes the orientation, rational-slope quantifier, and dependence on the fixed knot explicit.

A theorem for all negative surgeries, a knot-or-mirror disjunction, fillability obstructions, or a theorem on only integral slopes cannot by itself meet that target. The meridional/infinite slope is harmless because it yields the standard oriented sphere.

Source: [K3 author preliminary version](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), Section 3.5, pp.160–162. The local PDF was rehashed and the target pages were visually inspected. No source pages are included in this package.

## 3. Standard Legendrian surgery and stabilization

Golla's Theorem 1.1 concerns xi_n^-(L), positive integer contact coefficient n, and a Legendrian representative in standard tight S^3. Its three conditions are the sharp self-linking equality, the lower bound on the **smooth** coefficient n+tb, and tau=nu. They characterize nonvanishing of its contact invariant. Increasing n changes only the coefficient condition. Proposition 6.18 retains the sharp representative hypothesis for its rational-slope conclusions, with epsilon=1 or epsilon=0 as stated by the author. None of these hypotheses can be removed by relabeling an integer threshold.

For a positive and b negative stabilizations, tb'=tb-a-b and rot'=rot+a-b. Therefore tb'-rot'=tb-rot-2a, and a positive deficit from the required equality becomes delta+2a. This is an identity for all nonnegative integers a,b, not an empirical extrapolation from the finite checker. The transverse self-linking convention is sl=tb-rot. Reversing orientation exchanges the sign of rot, so the two initial orientations must be considered separately. The report does so. No restriction on every possible Legendrian representative follows from an obstruction for stabilizations of one representative.

Source: [Golla, published PDF](https://msp.org/gt/2015/19-1/gt-v19-n1-p04-p.pdf), Theorem 1.1, Remark 1.3, Proposition 6.18, pp.172 and 221–222; those statements and the rational extension were inspected.

The separate Conway theorem actually rules out every positive contact surgery on every standard-contact Legendrian figure-eight representative. It is stronger than a vanishing-invariant conclusion. It still does not rule out positive tight structures on the smooth surgered manifold obtained by other methods. This distinction is explicit in both the source and author report.

Source: [Conway, author PDF](https://www.jiconway.com/Papers/Figure-Eight_Surgeries.pdf), Theorem 1.1 and Remark 1.2. The Conway–Etnyre–Tosun PDF recorded in SOURCE_CHECKS.json is only a corroborating pointer, not an additional theorem dependency.

## 4. Mirror/orientation proof

Let a positive tight structure be supplied on S^3_{-r}(mirror K), identified with -S^3_r(K). Pulling back by the corresponding orientation-reversing map makes its defining three-form negative on the fixed target orientation. Diffeomorphisms preserve existence or nonexistence of an overtwisted disk, so the pulled-back structure remains tight. They do not change the preceding sign conclusion.

For a nonzero smooth real function f, direct differentiation gives

    (f beta) wedge d(f beta)
      = f beta wedge (df wedge beta + f d beta)
      = f^2 beta wedge d beta.

The term containing beta twice vanishes. Since f^2 is everywhere positive, neither reversing coorientation nor any such rescaling turns the resulting negative contact structure into a positive one. This is a complete elementary sign argument. It does not exclude constructing an unrelated positive structure. The cited universal negative-surgery theorem therefore leaves precisely the positive-orientation gap identified by the author.

## 5. Conditional nonzero-LOSS barrier

The relevant Li–Wan–Zhou admissibility conditions are tb!=1 and tb-rot=2g(K)-1, in a contact structure on S^3. Theorem 1.6(2) transfers nonzero LOSS to nonzero contact invariant after Legendrian surgery. Theorem 3.3 supplies invariance under negative stabilization. These are the precise inputs; non-looseness alone would not suffice.

Fix a forbidden positive integral smooth slope s and suppose an admissible nonzero-LOSS representative has t=tb>=s+1. The integer k=t-s-1 is nonnegative. After k negative stabilizations, both tb and rot drop by k, preserving their difference. The final tb is s+1>=2, and every intermediate tb is at least this value. Thus the exceptional value 1 is never reached. LOSS remains nonzero; Legendrian surgery has smooth slope tb-1=s and nonzero contact invariant, hence is positive and tight. This contradicts the forbidden-slope premise. Consequently such representatives have tb<=s.

This proof covers k=0 and s=1 as well as larger values. It does not presume the original ambient structure is tight. It proves a conditional barrier for admissible nonzero-LOSS representatives, not a bound for all non-loose knots or all Legendrian knots. Applying s=2m-1 yields tb<=2m-1 exactly as claimed.

Source: [Li–Wan–Zhou arXiv:2510.05294v1](https://arxiv.org/abs/2510.05294), Definition 1.4, Theorems 1.6(2), 1.7 and 3.3. The public record checked on 2026-10-06 lists v1, submitted 2025-10-06, with no journal reference displayed. The source theorem's full proof is not independently certified here. The universal negative-surgery input and this conditional deduction must not be described as resolving the positive problem.

## 6. The sharp integer calibration and quantifier gap

Use the positive torus knot K_m=T(2,2m+1), with integer m>=1; m=0 is not included. Its genus is m. The established L-space-knot case gives positive tight structures for every rational slope at least 2m. The exceptional oriented manifold at smooth slope 2m-1 admits no positive tight structure. Any integer N<2m satisfies N<=2m-1, so its rational tail includes that forbidden slope. Thus the minimum **integer** threshold is 2m. This does not assert that 2m is the infimum of successful real thresholds or that intervening rational slopes are all bad.

Since 2m is unbounded as m varies, no one finite threshold can serve all knots. Negating the original statement instead requires one fixed knot with bad rational slopes unbounded above. The family with varying knot does not supply it.

The nonexistence citation is honest: [Lisca–Stipsicz arXiv:0709.0737v1](https://arxiv.org/abs/0709.0737), PDF pp.2–3, explicitly defines the positive torus-knot family and cites its earlier reference [24], Corollary 1.2, for nonexistence. That earlier proof was not independently re-audited. The inspected paper's Theorem 1.1 provides the complementary Seifert classification. Its arXiv record lists the Duke Mathematical Journal publication; the local bytes are the 2007 author version, not asserted to be identical to the 2009 journal PDF.

## 7. Remaining approaches and source limits

The Roberts discussion is a logical audit of the explicitly attributed K3 formulation. Even a disjunction for every slope does not choose the needed knot branch, and the fibered-hyperbolic restriction remains. The reviewer did not independently inspect both full Roberts papers; DOI landing-page retrieval failed in this review. No stronger Roberts interpretation is used.

Ding–Li–Wu's stated families and positivity restrictions on the pretzel parameters match the author's summary. Their results concern rational eventual Stein fillability of those families and do not constitute an all-knot result. The current public arXiv page lists v3, dated 2025-02-25, as an accepted version and gives Asian Journal of Mathematics 28 (2024), no.5, 617–652. The date discrepancy between issue year and revision date is not itself an inconsistency. Source: [arXiv:2111.02151](https://arxiv.org/abs/2111.02151), Theorems 1.13–1.16, Question 1.17, Conjecture 1.18.

All seven supplied PDF files were fully rehashed against the author metadata. This is byte verification of locally supplied inputs. Successful public PDF opens and current arXiv metadata checks are separate observations; parsed web views do not establish a fresh full-byte match. Every inspected proof statement remains an external mathematical input. Search failures, bounded negative searches, and publication labels are not proofs of correctness or absence of later work.

## 8. Executable audit and acceptance boundary

The author's six files exactly match the original external manifest, archive membership, sizes and SHA-256 digests. The independent replay reruns the final frozen author checker under normal Python, -O and -OO, including relocated extraction and the author's advertised controls. Additional tests cover each member, missing/extra entries, symlinks, duplicate keys, traversal attempts, type errors, false outcome flags, and altered corpus identity metadata. See REPLAY_RESULTS.json for the complete retained results.

The author checker intentionally has a narrower scope than this audit: it hashes package members against the supplied manifest, checks selected status/identity fields, and runs finite arithmetic examples. It does not rehash the actual corpora or PDFs, prove geometric existence/nonexistence, prove the universal identities by induction or algebra, authenticate the manifest itself, or check its archive metadata. Adversarial rehashing of altered report prose or source-hash metadata is accepted by that checker. Those passes are recorded as trust-boundary diagnostics, never as accepted mathematical revisions.

verify_acceptance.py pins both original inputs and verifies every byte before executing the extracted author checker. It additionally verifies the audit package against an externally pinned manifest. Optional arguments independently replay the three complete corpus files and all seven source PDF pins; omitted inputs are reported as not rechecked. The separate final receipt reports tests on the exact frozen audit package, including optimized modes, relocation, and tampering. Supplying an attacker-selected manifest hash is not authentication; the receipt's digest is the trust anchor. Before executing package code, use a trusted hashing tool to verify the outer ZIP against the receipt. A modified verifier cannot be trusted to authenticate itself. Tamper tests invoke the known-good verifier against candidate roots.

All finite arithmetic tests remain regression diagnostics. Analytical arguments above, read against the inspected source hypotheses, supply the mathematical review. No assertion relies on Python assertions surviving optimization.

## Disposition

Accepted scope: exact-gapped partial analysis, elementary stabilization/sign/threshold deductions, and a conditional LOSS barrier. The arbitrary-knot positive rational tail remains unresolved. No sixth approach, publication, source redistribution, or general theorem certification is part of this audit.
