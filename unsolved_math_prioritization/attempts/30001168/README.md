# Weighted Yamabe heat-trace comparison: a dimension-three counterexample

Problem 30001168 / OWR-3389-021, rank 821. Status: **claimed_solved**, 1/5 substantive approaches.

The universal comparison over all dimensions n >= 3 is false. The authored construction gives a smooth, strictly positive, volume-normalized weight on the standard round S³. A finite capped cylinder of length 10000 has scaled heat trace strictly greater than 13/20 at a specified positive time, while the round scaled trace is strictly less than 129/200 at every positive time. Their threshold gap is 1/200.

Two independent AI analytic reviews accept this exact result without mathematical corrections. The second review adds a four-region all-time round bound independent of the two preceding interval-grid implementations. This is a full negative answer to the universal assertion through dimension three; the comparison restricted to n >= 4 and the separate monotonicity problem 30001169 remain unresolved by this work. There is no historical-priority, human-peer-review, or formal proof-assistant verification claim.

## Read the mathematics

- [Authored proof](author/PROOF.md)
- [Independent adversarial audit](audit/AUDIT.md)
- [Second analytic review and four-region proof](second_review/SECOND_REVIEW.md)
- [Current acceptance and scope](ACCEPTANCE.json)
- [Source verification metadata](audit/SOURCE_VERIFICATION.json)
- [Checkpoint log](RESEARCH_LOG.md)

The three archives in `archives/` and their extracted files are unchanged frozen snapshots. Pending-audit or unpublished wording inside earlier snapshots describes the time of that snapshot; this wrapper and the subsequent reviews supply the current acceptance. No historical field has been overwritten.

## Reproduce

Use Python 3 with its standard library only, from any working directory:

    python -I -B /path/to/verify_publication.py
    python -I -B -O /path/to/verify_publication.py
    python -I -B /path/to/package_controls.py

The publication gate checks an exact regular-file inventory, a pinned manifest, all bytes and hashes, the three immutable archive identities, ZIP member safety, exact archive/extraction agreement, ordinary and relocated arithmetic replays, and the independent audit's 34 expected-outcome controls. The second-review verifier also rejects two mathematical negative controls. `package_controls.py` separately tests the outer gate in normal and optimized Python. All mutations occur in temporary copies.

Trust the wrapper verifier through its Git commit or a separately verified hash. A checksum authenticates bytes relative to that anchor; an arithmetic checker does not prove smooth compactification, conformal covariance, Poisson summation, or min-max. Those analytic obligations are addressed in the proof and both reviews.

Only authored mathematics, code, reviews, results, and public verification metadata are included. No copied source documents, extracted source text, dataset contents, or private material are included in this attempt directory. The sole shared-file change is the target queue row's Status, Turns and Findings cells. This draft submission does not merge or release the result.
