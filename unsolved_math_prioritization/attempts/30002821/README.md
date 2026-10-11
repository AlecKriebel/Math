# Ford-circle maximality: an audit of an existing proof

Target: 30002821 / OWR-13498-011, Optimality of Greedy Circle Packings.

The accepted result is Alper Ferudun's existing version 1.1 proof, dated September 30, 2026: the complete greedy line-tangent packing maximizes total area in the gap between the x-axis and two tangent unit disks. The maximum is pi*(zeta(3)/zeta(4)-1), approximately 0.347543510672718666238146745405400598. No missing step or theorem-changing repair was identified for this exact target.

This is an AI-assisted, unrefereed proof-audit edition. Acceptance records an independent internal AI audit of Alper Ferudun's existing version 1.1 proof; it is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete authored mathematical reconstruction, every written formula and example, and all acceptance qualifications are retained. Executable code, raw computational datasets, copied source PDFs or text, source renderings, raw search responses, and private coordination material are not distributed. Historical finite checks support the written proof and cannot be reproduced from this edition alone.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey, or mathematical execution.

## Exact mathematical scope

The unit boundary disks have centers (-1,1) and (1,1). Packed disks have positive radius, touch the x-axis, and have pairwise disjoint interiors in the bounded gap. Boundary contacts are allowed; the two boundary disks are excluded from the objective. The complete greedy family has radius 1/q^2 and base point 2p/q-1 for every coprime pair 0<p<q. Every recursively generated gap must eventually be filled.

For any two externally tangent positive-radius boundary disks on a common line, the same greedy family maximizes the sum of r^alpha for every alpha>1. The auxiliary weight w(s)=1/(exp(1/s)-1), where s=sqrt(r), and nonnegative scale superpositions are also covered, with extended values allowed for the latter. The greedy radius-power sum diverges at alpha<=1. Arbitrary nondecreasing weights, uniqueness of global optimizers, disks not required to touch the line, and nontangent boundary disks are outside acceptance.

## Reading order

1. PROOF.md contains the entire authored mathematical audit once, including the exact theorem, public citations, source inspection, Sections 1-7, the all-degree positivity argument, both independent inductions, all limiting steps and the nondecreasing-weight counterexample.
2. AUDIT.md is a review summary and roadmap of the discharged obligations, not a substitute for the full reconstruction.
3. ACCEPTANCE.md and ACCEPTANCE.json identify the accepted existing theorem and explicit exclusions.
4. SOURCES.json and VERIFICATION.json preserve public source identities, historical inspection scope and bounded supporting-check metadata.
5. MANIFEST.json lists exactly eight files and hashes the other seven members. Its own digest is pinned independently by the publication description.

## Attribution

Alper Ferudun, *The Ford-Circle Packing Has Maximum Area: An Answer to a Question of Propp and Kenyon*, version 1.1, September 30, 2026: https://doi.org/10.5281/zenodo.23049959.

The original question is Problem 7 by Jim Propp and Richard Kenyon in Günter Rote's collected open problems, *Discrete Differential Geometry*, Oberwolfach Report 13/2015, printed page 722: https://doi.org/10.4171/OWR/2015/13.

The manuscript describes itself as unrefereed and AI-assisted. Acceptance here rests on the written mathematical reconstruction, not the source author's verification narrative or a claim of external review.
