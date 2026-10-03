# Random-graph coloring growth rates

Problem 30002320 / OWR-12481-005 has a consequential transcription issue: the original question asks for the expected nth root of the number of colorings. Moving the root outside the expectation changes the problem.

- [Result, complete elementary proofs, and remaining gap](RESULT.md)
- [Five proof-attempt routes](RESEARCH_LOG.md)
- [Source provenance and literature scope](SOURCE_AUDIT.md)
- [Machine-readable disposition](STATUS.json)
- [Exact supplementary checks](checks/check.py) and [results](checks/results.json)

The outside-root expression converges to k(1−1/k)^(d/2). The source conjecture remains unresolved in this packet. We prove the standard low-density formula and an explicit high-density zero region, explain the known all-k condensation theorem, and isolate the failures of naive temperature, logarithmic, and ensemble arguments.

Recommended classification: partial, five substantive approaches used, no novelty or complete-resolution claim. This packet contains no new paper or DOI. An independent audit is required before publication; the author packet alone does not authorize it.

The checks are finite exact controls, not a proof of the asymptotic conjecture. Reproduce with Python 3, standard library only:

    python checks/check.py

The command prints JSON and does not write files or use the network.
