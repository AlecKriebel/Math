# Scoped acceptance report

## Decision

Accept the full mathematical proof as a scoped partial result for problem 30006109 and accept the stated distinction between the hard-capacity model and the later dropout model. The original open-ended problem remains unresolved by this packet.

## Accepted theorem

The instance consists of a finite explicitly represented tree, explicitly listed commodities, recoverable tree paths, and nonnegative rational weights and capacities with finite binary encodings. Congestion counts listed commodity incidences per edge, including duplicate commodity paths and zero-weight constrained commodities.

Under these assumptions:

1. The feasible sets form a k-extendible system for positive congestion k. The supplied complete exchange and telescoping proof establishes that decreasing-profit greedy returns a hard-feasible set of value at least OPT/k.
2. Congestion zero has optimum zero. Congestion at most two permits exact polynomial-time optimization. The full proof preserves parallel choices and edge upper capacity one, clips vertex capacities, and supplies an explicit ordinary general-graph matching gadget. Its slot construction avoids pseudopolynomial expansion from huge binary capacities.
3. Rational capacity flooring and path-size clipping preserve the feasible set exactly.
4. For the authored two-edge example, the hard-capacity optimum is 3 and the later dropout optimum is 4. The dropout model therefore does not automatically provide a hard-feasible approximation guarantee.

The proof is preserved in full. No mathematical region was rewritten or shortened during preparation. Two audit-only editorial changes clarify publication boundaries and are recorded verbatim in VERIFICATION_METADATA.json.

## Attribution and source boundaries

The greedy result is an application of the general k-extendible framework associated with Mestre. The proof is given directly, so access to only the publisher's two-page preview does not replace a missing proof step. The exact algorithm imports the established polynomial-time theorem for ordinary weighted matching; the packet does not re-prove the blossom algorithm. Gabow's generalized-matching conventions are not silently substituted for the unit-edge-capacitated degree-upper-bound formulation.

The OWR problem statement does not explicitly specify signs or finite encodings. The packet's nonnegative rational hypotheses are added assumptions, not quotations or assertions about unstated source conventions.

The source record pins the inspected arXiv v3 of the later FZA manuscript. Targeted inspection establishes its model and theorem scope; no full audit of its approximation proofs or claim of journal acceptance is made. A separate transfer between models is not proved impossible.

## Verification evidence

The supplied audit manifest, proof, and audit identities were checked before preparation. Every artifact listed by the upstream audit manifest was hashed individually. Its executable checker was reviewed for its local role and was excluded from the public allowlist. Four locally retained source PDFs match their recorded SHA-256 hashes and byte counts.

The authored finite checker was rerun locally in normal, Python -O, and Python -OO modes. All three completed with PASS and produced byte-identical output matching the audited aggregate record: 234,946 greedy instances; 9,050 exchange systems and 55,975 exchange triples; 4,600 degree-bound systems and 35,132 subset comparisons; and 260 matching-gadget optimum checks. Rational capacity flooring and the four-choice witness also passed. Raw enumerated instance collections and executable programs are not distributed.

These are bounded consistency checks. They do not independently prove the general theorem or certify every step of the imported matching algorithm. Source hashes establish file identity only. Preparation checks source bytes and the accepted record; it does not claim a fresh complete reading of every cited source or a lifetime retrieval count.

## Certification limits

This is AI-assisted mathematical work and AI-assisted review. It is not external human expert peer review, journal acceptance, or a formally machine-checked proof. No novelty, best-possible ratio, new hardness threshold, or full resolution is asserted.

Only the exact files in PUBLICATION_MANIFEST.json constitute this public-safe packet. Its preparation makes no publication, source modification, queue modification, or third-party outreach claim.
