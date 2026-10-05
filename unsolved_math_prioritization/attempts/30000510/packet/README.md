# Baby Teichmuller space prior-result verification

Rank 657, ID 30000510, OWR-1275-010.

The current repository queue was queued 0/5 and no prior user/repository attempt was found. A third-party preprint, released 1 October 2026, already answers the components and ordinary singular-cohomology questions. Its proof was inspected and reconstructed in PROOF.md. This packet is a verification of prior mathematics, not a new discovery.

For every n>=3 there are n-1 components. With any abelian coefficient group A, the singular cohomology is A^(n-1) in degree zero, and additionally A in degree n-3 for even n; it is zero in all remaining positive degrees. The normalized pair slice is convex, except for a deleted interior point in the even middle component. A locally trivial bundle with contractible fiber links the slice to the actual quotient, including its non-Hausdorff case.

Read PROOF.md for every quantifier, quotient convention, proof step and limitation. SOURCE_VERIFICATION.json binds the original report, prior preprint and standard-topology source to their inspected bytes. RESEARCH_LOG.md records the early prior-result stopping decision; it does not claim five artificial proof attempts.

Reproduce finite controls using Python 3 with no external dependencies:

    python3 verify.py

The command prints deterministic JSON identical to CONTROL_RESULTS.json. These exact finite controls are auxiliary checks, never universal proof. The code was written for this packet; no downloaded program is executed. Source PDFs, source archives, full source text, datasets and private coordination are not included.

AUTHOR_FREEZE.json in the enclosing directory binds every packet file. Publication requires a fresh independent audit against that exact manifest. No remote write, publication, new DOI or claim of peer review was performed.
