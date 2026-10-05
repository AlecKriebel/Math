# Negative-p Aleksandrov concentration: scoped partial results

Problem 30004953 / OWR-8415364-011, rank 785. **UNSOLVED, 5/5 substantive approaches used.** The original all-dimensional, all-p <= -1 optimal-concentration problem remains unresolved.

The completed independent AI audit passes the expressly scoped mathematics with no required mathematical repair. This is not human peer review, editorial acceptance, a formal certificate, or a novelty determination. Read [the frozen proofs](author/PROOFS.md), [the full deductive audit](audit/INDEPENDENT_PROOF_AUDIT.md), [clarifications](audit/CORRECTIONS.md), and [the source update](audit/SOURCE_UPDATE.md).

## Accepted scope and boundary cases

- In the plane at p = -1, every even nonzero finite measure whose antipodal-pair mass ratios are **strictly below pi/(pi+2)** has an origin-symmetric solution.
- The orthogonal four-atom measure at equality has **no solution even among nonsymmetric bodies**. For a concentration guarantee written with <= c, pi/(pi+2) is only a **nonattained supremum**, not an admissible endpoint.
- In dimension n >= 2 at p = -1, an even nonzero finite measure **spanning the ambient space** has a solution if every line-mass ratio is strictly below 1/(1+d_n), where d_n = 2 Gamma(n/2)/(sqrt(pi) Gamma((n-1)/2)). This is sufficient; sharpness for n >= 3 remains unproved.
- The compactified variational argument, rank k > -p exclusion, exact p < -1 two-pair examples, and a solution that is not a global maximizing critical point survive the audit. These examples do not establish a universal p < -1 concentration guarantee.
- The general p < -1 optimal guarantee and higher-dimensional p = -1 sharpness remain unresolved in this work. The primary evenness hypothesis is restored; no solution of the unrestricted shortened catalog wording is claimed.

## Literature update and attribution limits

Shaodan Yang and Yinyin Hu, *The Planar Lp Aleksandrov Problem*, Journal of Mathematical Research with Applications **46(3) (2026), 397-411**, DOI **10.3770/j.issn:2095-2651.2026.03.009**. The [official issue](http://jmre.ijournals.cn/en/ch/index.aspx?year_id=2026&quarter_id=3) and [official abstract](http://jmre.ijournals.cn/en/ch/reader/view_abstract.aspx?file_no=20260309&flag=1) have now authenticated the bibliographic identity and abstract. The full-text link returned slider-guard HTML and was not bypassed. The full paper remains uninspected; exact theorem hypotheses, concentration estimates, and overlap remain unverified.

The separate Feng-Hu-Li-Lv paper, [DOI 10.1007/s00208-026-03420-w](https://link.springer.com/article/10.1007/s00208-026-03420-w), has an inspected publisher abstract but unavailable and uninspected full text. Its abstract already announces p = -1 nonexistence and p < -1 nonuniqueness examples. **Overlap, novelty and priority remain unverified.** An abstract alone does not settle these questions.

Both input freezes are preserved byte for byte. Their earlier audit-pending, source-search and no-remote-write labels are historical checkpoints. This later wrapper records the completed scoped audit and bibliographic update without rewriting those records.

## Replay

Python 3 and mpmath 1.3.0 are required. From this directory:

    python3 test_publication_integrity.py
    python3 -O test_publication_integrity.py

These commands check recursive inventories, hashes, archive/extracted equality, immutable input bindings, source/status guardrails, normal and optimized author and independent controls, and the audit's author-replay/tamper tests. They do not rewrite saved results. The 100 reviewer-built high-precision controls are finite regression evidence; they are not interval proofs or formal certificates for the continuous theorems. The deductive proofs and adversarial mathematical audit carry that burden.

Only authored proofs, code, results, audit prose, immutable safe archives and public verification metadata are included. No source PDFs, excerpts, images, raw corpora or private coordination files are redistributed. The queue patch changes only this record's Status and Turns, preserving its other columns and all other bytes, including the pre-existing stale embedded header.
