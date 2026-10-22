# New rational Hilbert-modular Lyapunov exponents: credited prior result

Problem 30002533 / OWR-12870-003, rank 723. Prepared 2026-10-05.

**Recommended disposition: already_solved, one substantive literature-verification approach.** The existential question in the 2014 report is answered by the published Gothic-curve literature. This packet gives a complete deduction from explicitly cited theorems, including the component issue that a direct use of the Gothic volume formula would miss. It is not a new construction or a proof of the cited deep theorems.

There are actual primitive Gothic Teichmüller components whose normalized, nonuniformizing Prym exponent is rational and outside `{1, 1/2, 1/3, 1/5, 1/7}`. A sequence of such component exponents converges to `3/13`. In particular, eventually they lie in `(14/65,16/65)`, which misses the old set.

We do not identify the exponent of a named individual component, claim that `3/13` occurs on a curve, or classify all exponents. The volume ratio for a possibly disconnected Gothic locus is an average; it cannot by itself certify a component exponent. The fixed-Hilbert-surface finiteness question is outside the resolved scope.

Read `PROOF.md`, then `SOURCE_SCOPE.md`. `APPROACH_LOG.md` records the early stop and rejected shortcuts. `STATUS.json` is machine-readable. `verify.py` checks exact arithmetic, negative controls, and the frozen manifest; it does not formally verify the literature or geometry.

Replay: `python3 -B verify.py`. To independently check separately obtained PDFs against the public source hashes: `python3 -B verify.py --sources-dir PATH`. Without those files, source checking is explicitly `NOT_RUN_MISSING_SOURCES` and is not a source-verification pass.

This freeze is an author submission awaiting a fresh independent audit and the parent review gate. No repository writes, publication, or queue edit were made. Only authored mathematics/code/status/logs and public verification metadata are in this directory. Source PDFs, source extracts, page images, raw dataset records, and private coordination material are excluded.
