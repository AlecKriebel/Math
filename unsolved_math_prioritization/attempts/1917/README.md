# Erdős Problem 81: credited prior resolution

**Problem 1917 / EP-81, rank 883. Disposition: already_solved, 0/5 fresh proof approaches.**

Credit belongs to **Obinna Okechukwu**, [*Clique partitions and bounded simplicial defect*, arXiv:2609.20871v1](https://arxiv.org/abs/2609.20871v1), submitted 15 September 2026. This package publishes an independent AI-assisted audit of that prior result. It claims no new solution.

## Accepted mathematical statement and limits

Theorem 1.1 and Corollary 1.2 give an absolute nonnegative constant K_0 such that every finite simple chordal graph G on n vertices satisfies

cp(G) <= floor(n(n+1)/6) + K_0.

Here cp partitions all edges into arbitrary complete subgraphs, with each edge used exactly once. The constant is uniform in n and G, without connectedness, splitness, density, or minimum-degree restrictions. For n>=1 this is at most n^2/6 + (1/6+K_0)n; the empty graph has cp=0. It therefore resolves the EP-81 quadratic-plus-linear target. Eventual exactness and its book-graph equality classification are also accepted. The stronger **all-order exact** conjecture, its small-order equality classification, and auxiliary Section 6 are outside this acceptance.

The status is a mathematical-audit disposition. The inspected source is an arXiv preprint. Journal acceptance, external human-referee approval, official problem-website status, formal proof-assistant verification, and explicit usable universal thresholds were not established. No comprehensive novelty search is claimed.

## Read the work

- [Exact acceptance](independent_audit/ACCEPTANCE.md)
- [Signed fractional argument and fixed-pattern packing](independent_audit/FRACTIONAL_AUDIT.md)
- [Integral construction, rigidity and final theorem](independent_audit/INTEGRAL_AND_RIGIDITY_AUDIT.md)
- [Adversarial audit of the asymptotic-to-exact bridge](independent_audit/ADVERSARIAL_BRIDGE_AUDIT.md)
- [Inspected sources and access limits](independent_audit/SOURCE_INSPECTION.json), [corpus provenance](independent_audit/PROVENANCE.json), and [audit receipt](INDEPENDENT_AUDIT_RECEIPT.json)
- [Original historical assessment](original_author/MAIN_PROOF_ASSESSMENT.md), [scope bridge](original_author/HYPOTHESIS_BRIDGE.md), and [approach log](original_author/APPROACH_LOG.md)
- [Publication metadata](PUBLICATION_METADATA.json), [publication checks](PUBLICATION_TEST_RESULTS.json), [file manifest](PUBLICATION_MANIFEST.json), and [checkpoint log](RESEARCH_LOG.md)

The audit uses established finite LP duality and Yuster's fixed-pattern packing theorem with verified hypotheses; the latter's regularity/matching foundations are not reproved. Galvin's original Theorem 4.1 and its exact list-coloring application were inspected. The needed Dirac simplicial-pair lemma is independently proved despite unavailable full access to the original article. No conjectural hypothesis or correction patch is required for the accepted main chain.

## Reproducibility and preservation

Both frozen ZIPs and external member manifests in `archives/` are unchanged. Their 13 author and 14 audit members are also unpacked byte-for-byte. The original pending-audit status and all no-publication fields are historical freeze-time facts; this wrapper records the later accepted publication disposition.

Run `python verify_publication.py .` from this directory for static archive, inventory, metadata and acceptance-binding checks plus hostile-mutation controls. These static checks do not execute archive code. Run `python original_author/verify.py` and `python independent_audit/checks.py` for bounded mathematical corroboration, and repeat with `-O`. The author program checks exact arithmetic and 680 concrete partitions; the independent program checks all 1,100 labelled graphs through order five, including 895 chordal graphs, and 8,240 arithmetic cases. Mathematical negative controls reject malformed partitions, exact fractional/integral equality, and an invalid nonnegative dual substitution. These finite checks do not prove the asymptotic theorem.

Optional complete-corpus and primary-PDF replays require separately supplied files with the recorded public pins. Publication-stage full-input checks, normal/optimized checks and relocated source-free checks are recorded separately from the historical receipts. Standalone runs honestly report optional inputs NOT_RUN. Source PDFs, extracted text, images and dataset contents are excluded.

Only this target row's Status and qualified Findings are changed in QUEUE.md; Turns stays 0/5. All unrelated bytes, notes and existing chat links are preserved. This is a draft PR only, without merge, auto-merge, release, DOI or outreach. No CI-pass claim is made.
