# 5000007: reviewed proof with an explicit wording correction

## Outcome

The parity-aware typeA0 conjecture in Fuchs has a complete proof in [PROOF_V2.md](PROOF_V2.md), with a [scope-matched independent AI review](independent_review/FINAL_REVIEW.md). This is not human peer review, and novelty is not certified.

The bare imported condition beta−alpha=2pi/5 is false as an unqualified formulation: the two direct face diagonals satisfy it and have graph-distance-two endpoints. The proof records exactly this exception and preserves Fuchs's even/odd classification and non-A0 diagonal calibration. Do not say the unqualified extracted sentence was proved true.

The external16-face certificate's geometry is independently verified, including length and shortness. Its actual transported source-type calculation gives beta−alpha=144degrees, henceA1, while the public72-degree subtraction uses the other boundary ray and an interior angle. See [the precise audit](EXTERNAL_CERTIFICATE_AUDIT.md) and the final review.

## Reproduce

From this directory, with Python's standard library:

```sh
python check_certificate.py
python check_half_turn.py
python independent_review/reviewer_exact_check.py
python -m unittest discover -s . -p 'test_*.py' -v
```

All certification decisions use exact arithmetic; numerical angles and lengths are displayed only for readability. No downloaded external software was executed.

## Provenance and limits

This is recovery of a previously started interrupted attempt, not a fresh zero-turn attempt. The lost historical count is unknown and nonzero. [The manifest](recovery_manifest.json), [research log](RESEARCH_LOG.md), original frozen candidate, and both review versions preserve that history. The draft-branch QUEUE display row records claimed_solved with the explicit source-scope correction and unknown/5 (interrupted) historical count. No state.json history was rewritten. [Draft PR #190](https://github.com/AlecKriebel/Math/pull/190) remains open for review; it is not a merge or release.

Source locations and source hash receipts are recorded in the proof and manifest. Downloaded source PDFs/text are retained locally under an ignored sources directory and are not republished in this package. The pinned dataset cache hashes were verified before the exact statement and prior desk report were extracted.
