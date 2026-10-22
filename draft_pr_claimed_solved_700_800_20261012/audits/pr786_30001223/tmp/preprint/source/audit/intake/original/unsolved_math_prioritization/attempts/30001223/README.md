# Simple tops of Young modules: audited counterexamples

Problem 30001223 / OWR-3400-007, rank 824. Queue status: **claimed_solved, 1/5 author turns**. Two independent mathematical audits accepted the precise counterexample below without corrections. This is an authored mathematical claim, not a novelty or human-peer-review claim.

## Exact result

For every odd prime p, over an algebraically closed field of characteristic p, take q=1, r=2p-1 and lambda=(2p-2,1). The source's Young module F I(lambda) is simple, while the polynomial injective I_n(lambda) is not projective for any integer n >= 2. The smallest example has p=3, r=5, lambda=(4,1), and a four-dimensional simple Young module.

This disproves the unrestricted positive-characteristic bridge in Miyachi's Conjecture 7. Its index-set proposal is a **stronger** statement, not an established equivalent classification; the same example refutes that bridge too. The separate De Visscher-Donkin classification of projective-injective polynomial modules is not refuted. Nothing here settles a restriction to characteristic zero with a nontrivial root of unity.

## Required reading together

1. [Authored proof](author/proof.md)
2. [First independent audit and mandatory convention supplement](first_audit/mathematical_audit.md)
3. [Second adversarial review](second_review/SECOND_REVIEW.md)

The convention supplement directly identifies the stable-rank multiplication kernel with I_N(lambda), then its multilinear Schur weight with the augmentation module. It removes any sign, conjugation or label ambiguity. The rank-two calculation identifies the genuine polynomial injective hull, and the all-rank argument invokes both injective and tilting truncation with their label hypotheses. It does not assume arbitrary preservation of projectivity under truncation.

## Reproduce

Python 3.10+ with its standard library suffices. Obtain the independently recorded SHA-256 of PUBLICATION_MANIFEST.json and run:

    python -I -B verify_publication.py --expected-manifest SHA256
    python -I -B -O verify_publication.py --expected-manifest SHA256

Use an absolute script path to run from any working directory. The verifier checks the complete regular-file inventory, every byte count/hash, the three external ZIP pins and exact archive/member equality before executing anything else. It then runs the three gates, all 34 author and 28 first-audit controls under both drivers, and all 24 second-review controls under both drivers. The fresh formal coefficient graph tests cover 24 odd primes through 97. They are finite support for the proof, not proof of either universal quantifier.

Use --integrity-only to skip computation. Extra files/directories, bytecode caches, missing entries, links, FIFOs, schema changes and corrupt bytes are rejected. The external manifest/archive pins are required authenticity anchors; an internally consistent coordinated rewrite is not authenticated. No malicious-runtime or concurrent-filesystem-replacement guarantee is made.

## Preservation and sources

All three frozen ZIPs and all extracted members are preserved byte-for-byte. The author's pending-review wording and proposed status remain historical statements; the later acceptance verdicts are in the two reviews. The original first-execution chronology is author-reported, not reconstructed by replay. The wrapper records the newly clarified 1/5 author-turn count without rewriting a frozen receipt.

[Corpus verification](CORPUS_VERIFICATION.json) records fresh full-file hashes and complete-target reconstruction against the supplied frozen snapshot. Public citations, source titles, PDF hashes/sizes and page locators are in [source metadata](author/sources.json). No source PDFs, copied extracts, dataset contents, private sources, private personal information or private coordination files are included.

The only existing-file edit changes this queue row's Status, Turns and qualified Findings link. All other queue bytes are preserved. No merge, release, DOI creation or outside outreach accompanies this draft.
