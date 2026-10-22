# Torus-surgery surface unknotting: audited partial results

Problem 2910 / KP-4.34, rank 918. **Unsolved, 3/5 approaches.** The accepted work is a scoped, stalled partial audit. Neither the smooth nor locally flat general problem is solved or refuted. No novelty or human peer-review claim is made.

Start with [the accepted proof](clarified/PROOF.md), [research report](clarified/REPORT.md), [full independent audit](audit/AUDIT.md), and [exact acceptance](audit/ACCEPTANCE.json).

## Results and limits

- Canonical surgery multiplicity must be ±1 for a standard ambient sphere; this necessary homology condition is not sufficient.
- The spun Hopf-link example ends at smooth standard S4, while either first surgery has H1 = Z. It exposes a final-versus-stagewise inference error, not a counterexample to the target conjecture.
- The spun-knot route is credited prior work. General surfaces still lack the required construction, stagewise standardness, and tracked-pair endpoint argument.
- The accepted pair-neutral gluing lemma states the boundary extension, smooth collar, and additional surface-boundary hypotheses explicitly.

## Exact artifacts

`original/` and `audit/AUTHOR_SAFE_FREEZE.zip` preserve the original ten-file packet byte-for-byte. Its historical awaiting-audit wording remains unchanged. `clarified/` and `audit/CLARIFIED_SAFE.zip` are the exact independently accepted derivative. [The actual patch](audit/CLARIFICATION.patch) changes only PROOF.md, sources.json, and status.json: explicit gluing and smooth spinning details, a version-specific source URL, and audit state. Mathematical conclusions are unchanged.

`audit/` is the exact 17-member extraction of `AUDIT_SAFE.zip`; `AUDIT_EXTERNAL_MANIFEST.json` and the two historical receipts preserve its trust anchors and review history. Historical statements that publication had not occurred describe that earlier audit, not this later draft PR.

All three full corpus pins and four PDF pins were rehashed during publication preparation, with the complete record/report pair checked. The separate corpus and PDF inputs are not distributed. Relevant primary-source inspection and fresh retrieval history are documented by the independent audit; the publication wrapper does not fetch or rehash those absent source inputs.

## Replay and trust boundary

Use Python 3 with only the standard library. First obtain a trusted SHA-256 for `PUBLICATION_MANIFEST.json` and `verify_publication.py` from the publication receipt or authenticated commit. Verify the wrapper itself before executing it. Then, from any directory:

    python3 -I -S -B /path/to/verify_publication.py --expected-manifest TRUSTED_SHA256
    python3 -I -S -B -O /path/to/verify_publication.py --expected-manifest TRUSTED_SHA256

The wrapper rejects unsafe paths, links, special files, duplicate keys, wrong inventories, changed bytes, and unsupported scope claims. It checks the immutable original, derivative, audit, patch, and acceptance pins, then runs frozen code only from an authenticated temporary snapshot. Descendant interpreters inherit isolated, no-site, and no-bytecode execution through a shim. The audit reproduces the actual patch, original and clarified checkers, 2,401 independent matrices plus 2,401 sign-reversed controls, and 48 package rejection checks. Historical outer-audit testing adds 16 rejection checks. Publication-specific adversarial testing is separately recorded.

These scripts verify exact bytes, arithmetic, and constrained metadata. They do not certify embeddings, diffeomorphisms, surface isotopy, literature completeness, or novelty. Replacing the wrapper and trust anchor together defeats this trust model.

Only authored mathematical text, code, audit/acceptance artifacts, and public verification metadata are included. Third-party PDFs, extracted source text, screenshots, source corpora, and private coordination material are excluded. The K3 source is linked, not reposted. This is a draft review artifact, with no release, DOI, or merge.
