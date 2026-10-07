# Acceptance report

Date: 2026-10-07 UTC. Problem 10000051 / AMR-099-0051. **Accepted corrected partial work only; unsolved, 5/5.**

The complete original candidate, full independent audit, actual correction patch and corrected mathematical text were reviewed. The required changes are adopted: independent fair measure in Proposition 7.2; a threshold Boolean control whose high-density probability tends to one while fair probability tends to zero; and explicit optimization guards in both assertion-based author scripts. Original and audit freezes remain byte-for-byte unchanged.

## Accepted scope

Finite Hex duality; exact direction-symmetric cases; the checked seven-square 65/128 versus 63/128 example; unit horizontal and vertical vertex extremal length; correctly oriented influence and finite-size change-of-measure bounds; the explicit high-density consequence of Peled's square-packing theorem; and the stated finite-chain countable results with their exact additional hypotheses.

Peled's Theorem 2.13 and square-specific Section 3 parameter are external mathematical dependencies, not independently reproved here. The [primary manuscript](https://arxiv.org/abs/2001.10855) is credited. Neither a uniform fair-color horizontal lower bound, the fair-color small-mesh half limit, nor an unconditional countable-tiling resolution is accepted. The corrected threshold control is not a square-tiling counterexample. Five mathematical approaches are recorded; source checking, audit, repairs and packaging add no proof-search turns.

## Bound inputs and verification

- Original manifest SHA-256: `d7e9b428572aa3864071d8e9bba50732afa6606586a4f1aa5250ada59ea24736`.
- Audit manifest SHA-256: `4c4bb2148bd8dabaabccc741351b24c08cd48f372bc8dc14ced7c7b3d8f7cff8`.
- Corrected candidate SHA-256: `01b2e76ed4e7b3b2e41b4d1467d2a56207839904ab541c356271e891da140254`.
- Corrected-slice manifest SHA-256: `57cda6d9529eb69521cab8e4e71aae5cfb5908d4ceb7dfd3c02f793b500c9cd8`.

Publication verification includes externally pinned complete-file inventories; exact patch application with zero fuzz; fresh ordinary execution of author and corrected scripts in temporary copies; normal/-O/-OO independent-check agreement; direct corrected -O/-OO rejection; and unchanged frozen result bytes. The wrapper runs under normal, -O and -OO and under PYTHONOPTIMIZE=1/2 while starting assertion-based scripts in ordinary isolated Python. Thirteen mutation controls per interpreter mode reject altered original/audit/corrected files, missing/extra files, symlinks (including the root), unexpected empty directories, duplicate JSON keys, a changed manifest, a locally rehashed mutation, an incorrect external pin and a changed verifier rejected by its independent external bootstrap hash. The complete resulting root-manifest hash is supplied externally in the draft PR rather than placed self-referentially here.

This is mathematical and reproducibility acceptance of limited partials. Exact finite checks do not replace the written general proofs. Bounded source searches are not a completeness or priority guarantee. Local replay is distinct from GitHub CI; no CI success is claimed without actual check results. No merge, release, DOI issuance or external outreach is part of this acceptance.
