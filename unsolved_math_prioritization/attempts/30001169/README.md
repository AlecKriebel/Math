# Weighted Yamabe heat-trace monotonicity: audited partial results

Problem 30001169 / OWR-3389-022, rank 822. **Unsolved; five of five approaches used.** The arbitrary-weight, all-time question in dimensions n >= 4 remains open in this attempt.

## Read the mathematics

Read [the authored proof](reviewed/author/proof.md), [the independent audit](reviewed/audit/AUDIT.md), and the mandatory [derivative-remainder clarification](reviewed/audit/DERIVATIVE_REMAINDER.md) together. The clarification derives differentiated asymptotics by finite differences and a spectral second-derivative bound; it does not naively differentiate a big-O term.

Accepted partial results:
- Every fixed smooth positive admissible weight has a strictly decreasing scaled trace near zero. In dimension four, f(t)=1/6-t²/90+O_W(t³) and f′(t)=-t/45+O_W(t²).
- The known all-weight large-time range is recovered.
- In dimension four, normalized weights with 999/1000 <= W <= 1001/1000 decrease for every t >= 1/4. Independent exact rational implementations check 750 intervals and 13,500 exponential enclosures, with every upper bound below -3/500.
- Infinite-cylinder trace density decreases. Compact capped-cylinder transfer is unproved.
- An abstract spectral example obstructs endpoint-only reasoning. It is not a geometric counterexample.

No uniform small-time interval is obtained from pointwise closeness alone. The possible gap before t=1/4 remains. The 42-record numerical scan is reproducible but uncertified: six coarse positive maxima disappear on refinement. None of these scans proves or disproves the target. No result is imported from the neighboring dimension-three question.

## Exact replay

Python's standard library suffices for every exact check. Obtain the independently published SHA-256 of PUBLICATION_MANIFEST.json, then run:

    python -I -B verify_publication.py --expected-manifest SHA256
    python -I -B -O verify_publication.py --expected-manifest SHA256

The verifier checks strict inventory, every byte count and hash, exact archive-member equality, accepted archive identities, the audit envelope and both certificates, and actually reruns all 48 author rejection/relocation tests plus the two independent relocated exact checks. Use --integrity-only to omit expensive computational replay. Run from any working directory using an absolute script path. Missing files, extra files/directories, links, FIFOs and unlisted bytecode are rejected before content reads.

The 26 audit-envelope relocation/rejection tests and publication corruption checks were also actually rerun; results are in PUBLICATION_TEST_RESULTS.json. A hash manifest requires an independently trusted external anchor. These computations supplement analytic arguments; they are not proof-assistant formalizations.

## Optional numerical replay

Only the exploratory scan needs NumPy and SciPy; recorded versions are in requirements-exploration.txt. After providing those packages, run:

    OPENBLAS_NUM_THREADS=1 python -I -B reviewed/author/exploratory.py

This is optional reproducibility research, not a substitute for either exact certificate. The accepted audit records a byte-identical rerun of all 42 records.

## Sources, identity and preservation

The public author derivative and rebound audit ZIPs in archives/ are preserved exactly. The audit embeds the same ten author files. The editorial revision did not change mathematics, code, claims or computed mathematical results. Earlier recorded no-publication and source-access limitations remain historical statements; they do not describe this publication's present repository state.

CORPUS_VERIFICATION.json records fresh full-file hashes and complete-record reconstruction. It publishes no dataset content. Public source titles, URLs, hashes and inspection history are in the reviewed metadata. Current literature completeness and novelty are not certified.

The only existing-file edit is the target queue row: Status queued to unsolved and Turns 0/5 to 5/5. Every other queue byte, including its pre-existing header, is preserved. No release, DOI, merge or outside outreach accompanies this draft.
