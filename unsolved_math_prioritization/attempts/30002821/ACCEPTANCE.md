# Acceptance of the existing Ford-circle maximality proof

Verdict: ACCEPT_EXISTING_PROOF_FOR_EXACT_TARGET.

Target: 30002821 / OWR-13498-011. Attribution: Alper Ferudun, version 1.1, September 30, 2026, https://doi.org/10.5281/zenodo.23049959.

This is an AI-assisted, unrefereed proof-audit edition. Acceptance records an independent internal AI audit of Alper Ferudun's existing version 1.1 proof; it is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete authored mathematical reconstruction, every written formula and example, and all acceptance qualifications are retained. Executable code, raw computational datasets, copied source PDFs or text, source renderings, raw search responses, and private coordination material are not distributed. Historical finite checks support the written proof and cannot be reproduced from this edition alone.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey, or mathematical execution.

## Accepted theorem

Among all countable positive-radius packings in the bounded gap between the x-axis and the tangent unit disks centered at (-1,1) and (1,1), with every packed disk touching the x-axis and interiors pairwise disjoint, the complete greedy family attains maximum total area

pi*(zeta(3)/zeta(4)-1).

The maximizer consists of the disks of radius 1/q^2 at base point 2p/q-1 for coprime integers 0<p<q. Boundary contacts are permitted; the two fixed boundary disks are not counted. Completeness requires eventual insertion in every recursive gap.

For two tangent positive-radius boundary disks on the same line, the same comparison holds for the sum of r^alpha whenever alpha>1. In square-root radius s, it holds for w(s)=1/(exp(1/s)-1) and weights W(s)=integral w(s/t) dmu(t) for positive Borel measures on (0,infinity), allowing infinite values. Monotone convergence handles the nonnegative sums; sigma-finiteness is not required for this step.

## Proof and review scope

The full 25,188-byte original authored audit is retained in PROOF.md, with an editorial introduction and a historically phrased nondistribution notice for its supplementary checker. Sections 1-6, every mathematical formula, the nondecreasing-weight counterexample and all proof arguments are unchanged. Section 7 retains every acceptance qualification. AUDIT.md supplies a separate review roadmap.

No missing step was identified. The compactness, countability, chain endpoints including k=2, all-degree positivity and nonnegative limiting arguments are explanations of valid implicit steps in the accepted source strategy. They do not constitute a repair of a false theorem. The manuscript's nonnegative-sum integration statement is justified by monotone convergence, without changing its theorem.

Historical exact and symbolic checks reported 242,391 successes and are supplementary only. Their byte identity and aggregate coverage are recorded in VERIFICATION.json. No mathematical checks were rerun while preparing this edition.

## Explicit exclusions

- A newly discovered theorem or proof, or certified novelty or priority.
- Uniqueness of the global maximizing packing.
- Nontangent boundary disks or packed disks not required to touch the line.
- Every nondecreasing weight; the full report includes a counterexample.
- A finite power-sum value for alpha<=1, where the greedy sum diverges.
- External human peer review, journal acceptance, or formal proof-assistant certification.
- Reliance on the source author's verification narrative, software or priority claims.

The accepted theorem resolves the exact mathematical target as a prior result in a publicly available unrefereed preprint. This classification does not imply acceptance of unrelated claims or a literature-wide priority certification.
