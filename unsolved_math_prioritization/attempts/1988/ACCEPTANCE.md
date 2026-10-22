# Acceptance report

Verdict: ACCEPT AFTER TWO EXACT DOMAIN/SCOPE CORRECTIONS. The candidate is not accepted literally as written.

## Review status and edition binding

These AI-assisted authored documents and their independent internal AI audit are unrefereed. “Accepted” refers only to the corrected partial results in this edition. No external human peer review, journal acceptance, formal proof-assistant certification, novelty or exhaustive worldwide-status determination is claimed.

This edition applies both required corrections. Its PROOF.md is exactly the corrected proof identified below, with no further mathematical or editorial proof changes. The complete substantive audit and correction explanation are preserved; finite checks described below are historical and their code, certificates and detailed outputs are omitted.

## Accepted mathematical content

- For a 3-permutable set and fixed C>=0, only finitely many positive integers n have every integer of [n,2n-C] in the set.
- The equivalent divergence of deficits of full intervals whose starting points tend to infinity.
- The finite-prefix bound P>=k+2 for k distinct shifted C3 scales and the two fixed anchors.
- The stated two-color and bounded-additive-dyadic-run exclusions.
- The affine-coordinate conclusion after distinguishing infinite from finite intersections and using positive coordinates.
- For each prescribed nondecreasing unbounded f:N->N, one 3-permutable set with upper natural density at least 2/3 and infinitely many full intervals whose positive deficits are at most f of their starting points.
- Equivalence by translation of the zero-based and positive-integer two-set existence questions, correcting the issue in Kasel's Remark 3.

The finite C3 lemma is properly attributed to Kasel. Proposition 7 is properly attributed as an adaptation of Geneson's construction. Neither is presented as a newly discovered underlying mechanism.

## Required corrections

1. Theorem 1 must say “positive integers n.” Negative integers otherwise give infinitely many empty intervals.
2. The affine extension must distinguish infinite and finite intersections and work in positive inverse coordinates.

CORRECTIONS.patch is the complete two-hunk patch, preserved byte for byte: 2,030 bytes; SHA256 fa7fbcfaca2a8e832172cf750bf589194c141334213d56c2305b473fcfc61ac7. Its exact replacements and expected output were separately verified during the audit and edition preparation. No changes to the core mathematical argument are required.

Original proof: 16,461 bytes; SHA256 8c4d56bb0e21785f4aeb21239518783dcf139afd10839c6514fea6472e0ad0b7.

Corrected proof produced by that exact patch: 16,759 bytes; SHA256 670b73ed1e4c3a0fd52235a67f6ee9a67140bb8949e923798bb52c73f5e074bd.

The original candidate was not modified. The corrected byte identity was independently regenerated from the replacement specification and the complete unified patch was checked against those replacements in normal, -O, and -OO modes.

## Original target and limits

The general two-set partition target remains unresolved by this packet. There is no valid partition construction and no theorem excluding all two-colorings. No novelty certification, exhaustive priority search, or independent certification of current global openness is provided. An upper-density lower bound for one part is not evidence that its complement is admissibly orderable.

Acceptance of the infinite arguments is based on the mathematical audit, including mirror propagation, all four C3 cases, endpoint checks, fixed-anchor quantifiers, and cross-stage exclusion. The finite certificate replay and other exact computations are supporting checks only.

## Verification boundaries

The candidate's 21 public members and external seal matched the supplied pins before and after the audit. Fresh retrievals of all three primary PDFs matched the recorded source byte counts and SHA256 hashes. The candidate generator reproduced all ten certificate files and its generation manifest byte for byte in a temporary copy. Candidate and independent check outputs match across normal and optimized Python modes.

The original audit inventory included authored audit/correction files, original audit scripts, and public verification results. This edition distributes only authored proof, audit, acceptance and correction material with public verification/source metadata. Copied third-party source PDFs, extraction text, renderings, code, finite certificates, detailed test outputs, dataset contents and private material are excluded. Edition preparation performed no new scholarly-source retrieval or inspection.

## Exact distributed review identities

PROOF.md: 16,759 bytes; SHA256 670b73ed1e4c3a0fd52235a67f6ee9a67140bb8949e923798bb52c73f5e074bd.

AUDIT.md: 16,757 bytes; SHA256 f1e95d9fe696d0ccf57bfa0f287be057e92a1cbd4658995ed392fce043812b2f.

CORRECTIONS.md: 3,107 bytes; SHA256 6291feb2fbb6b2386b56ef1891d9f23290f3627b66c390c419713029223123ae.

CORRECTIONS.patch: 2,030 bytes; SHA256 fa7fbcfaca2a8e832172cf750bf589194c141334213d56c2305b473fcfc61ac7.
