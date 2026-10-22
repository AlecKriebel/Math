# Coding efficiency: audited scoped partial results

Problem **30005026 / OWR-9790359-007**, rank **788**. **UNSOLVED, 5/5 approaches used.** The original finite-valued stationary target on Z^d remains unresolved. The independent AI-assisted audit accepts the scoped partials with two nonblocking source errata; it is not peer review or a novelty determination.

## Mathematical scope

The original question asks, for every epsilon > 0, for some finite-alphabet IID source with entropy within epsilon of the target's entropy per site and an exponentially decaying coding radius. Its alphabet, law, code, and tail constants may depend on epsilon. No common alphabet bound or uniform tail constants are assumed.

The authored results include a marginal-support obstruction, a finite-entropy countable IID example, a composition bound, a periodic-phase obstruction, and fixed-alphabet uniform-tail compactness. The countable IID example refutes **only the catalog's broadened wording**, never the original finite-output problem. The prescribed-source-family compactness obstruction also does not refute the existential question.

The positive mixing finite-state Markov subclass is credited to Harvey–Holroyd–Peres–Romik, Theorem 2. The equal-entropy exclusion is credited to Gabor's 2025 preprint, Theorem 1.2. Neither external theorem is independently reproved here. Finite arithmetic controls supplement the written arguments, rather than prove the infinite-process statements.

## Preserved evidence and source corrections

- `author/`: all 11 files of the unchanged author freeze, including historical audit-pending language.
- `audit/`: all 18 files of the independent audit, verdict PASS_SCOPED_WITH_NONBLOCKING_SOURCE_ERRATA.
- `SOURCE_CORRECTIONS.md`: the mandatory source addendum, identical to `audit/CORRECTIONS.md`.
- `frozen_archives/`: canonical base64 encodings of both original ZIP byte streams. Decode with Python's base64 module to recover the exact ZIPs; the verifier compares every member against the preserved directories.
- `PUBLICATION_PROVENANCE.json` and `PUBLICATION_INPUT_REPLAY.json`: fresh repository binding and metadata-only replay of complete cached source inputs.

C1: the catalog's parenthetical **2023 is a valid report publication year**; the workshop itself took place in February 2022. C2: HHPR Section 5 occupies printed **pp.28–31**, not pp.30–32. These corrections do not alter any proposition. The frozen author inspection history is not rewritten; the independent additional inspection is separately recorded in `audit/SOURCE_AUDIT.json`. The current audit supersedes historical pending-audit status without changing either freeze.

Primary sources: [original report](https://ems.press/content/serial-article-files/46944), [report publication metadata](https://ems.press/journals/owr/issues/2056), [Meyerovitch–Spinka v1, Question 8.3](https://arxiv.org/abs/2201.06542v1), [HHPR](https://www.math.ucdavis.edu/~romik/data/uploads/papers/expoplms.pdf), [Gabor v1 preprint](https://arxiv.org/abs/2509.06018v1).

## Portable verification

Python 3, standard library only. No network or external input is needed for the packet replay:

    python3 -B /path/to/packet/verify_publication.py --expected-manifest <SHA-256>
    python3 -B /path/to/packet/test_publication_integrity.py

The verifier rejects optimized Python, validates exact recursive inventory, manifest pins, both original ZIP streams and every member, then replays **141,484 author assertions**, **141,484 independently reconstructed assertions**, and **46,913 additional independent assertions**. It verifies exact saved replay bytes where the frozen programs produce those files. The last count includes all 6,672 ternary maps on four finite binary-block supports and three rejected invalid mathematical relaxations.

Supply `--queue-before` and `--queue-after` together to check the complete queue hashes and exact patch. Optional `audit/verify_inputs.py` rehashes three complete corpora and five PDFs if those privately obtained external inputs are supplied. No source PDFs, extracts, images, or raw corpora are distributed.

## Repository change

Only this queue row's Status and Turns change, from queued / 0/5 to unsolved / 5/5. Findings and every other queue byte, including the existing stale header, are preserved. The packet does not update historical catalog, assessment, state, or unrelated rows. The draft is a publication checkpoint for scoped partial results, with no sixth proof-search approach, general solution, merge, release, DOI, or external outreach.
