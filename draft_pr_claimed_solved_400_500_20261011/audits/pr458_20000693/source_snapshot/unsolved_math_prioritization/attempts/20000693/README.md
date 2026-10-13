# AIM 5.3 / 20000693: scoped Dirichlet-product moment heuristic

**Heuristic. Credited synthesis. General moment asymptotic unproved. Author turns: 1/5.**

This is the current entrypoint. An independent AI-assisted audit accepts the leading-term heuristic for finitely many fixed, unshifted Dirichlet characters of arbitrary fixed moduli and fixed nonnegative real weights. It handles repeated primitive constituents, principal and nonreal characters, zero weights, deleted Euler factors, and the Barnes-G constant. This responds to the displayed Dirichlet-product example in [AIM Problem 5.3](http://aimpl.org/zetamoments/5/), attributed to C. Turnage-Butterbaugh.

Read [the final clarifications](REVIEW_ADDENDUM.md), [the frozen heuristic](author/HEURISTIC.md), [the independent review](review/REVIEW.md), and [the source/prior-work gate](author/SOURCE_GATE.md). The clarification layer implements all three nonblocking recommendations without changing the accepted formula or using another substantive research turn.

The principal models belong to Keating--Snaith, Heap, and Sahay. No new mathematical priority or human peer review is claimed. Only the defined arithmetic constant's local analysis, convergence and positivity are proved here. The critical-line moment asymptotic, distinct-constituent independence, unitary zero model and weighted prime/zero splitting remain conjectural. The review discusses the intermediate GRH premise in the cited derivation; GRH alone does not prove the model assumptions.

The queue's `claimed_solved` label means completion of this exact, openly scoped heuristic request only. It does not mean that the general high-moment theorem has been solved. Excluded are negative powers, shifted or unbalanced moments, growing-modulus/weight uniformity, all lower-order terms, and a universal result for higher-degree imprimitive L-functions.

## Evidence and reproduction

The frozen author replay reports 966 checks. A separately constructed reviewer suite reports 380 cases. Both outputs were freshly reproduced byte for byte for publication. Their case-count conventions differ and must not be combined into a uniform proof certificate. These are local algebra, phase-integral and finite random-matrix checks; they do not numerically certify or prove actual high moments.

Run `python3 verify_publication.py` to check the public packet's hashes. Run `python3 verify_publication.py --replay` to execute both suites in temporary directories and compare their output bytes to the frozen reports. Replay requires Python, SymPy 1.13.1 and mpmath 1.3.0, the versions recorded in those reports. The frozen files are not overwritten.

All 11 author files and 11 review research files, plus the review addendum, are preserved byte for byte. The review's source-text extraction is deliberately excluded, as are external PDFs/HTML, imported records/corpus, and operational authorization records. The original review manifest records the excluded text's hash as historical provenance; the public verifier checks the explicitly published subset. Raw source links and checksums remain available in the research manifests. Source checks are historical audit evidence, not a claim that external files are bundled here. The Keating--Snaith PDF was absent from the audit cache, as the review discloses.

Historical pending-review and local-only labels inside frozen files record their state when written. This additive entrypoint and [PUBLICATION_STATE.json](PUBLICATION_STATE.json) give the current research disposition. The independently reviewed mathematical content has not been edited.

This draft contains only this target's public research packet and its own queue Status, Turns and scope-qualified Findings cells. No merge, release, DOI, or external outreach is part of this publication. Alec Kriebel; AI-assisted research synthesis, verification and review.
