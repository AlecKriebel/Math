# Settled quadratic polynomial research packet

Outcome: the intended odd-characteristic settledness conjecture is unresolved, after five distinct approach families. The packet contains rigorous partial statements, an exact special family, a characteristic-two scope correction, a published obstruction to the original one-step Markov mechanism, and reproducible exact checks. No general solution or novelty claim is made.

Read PROOF.md first. EXACT_RESULTS.json records exact rational stable-mass profiles and polynomial certificates. LIMITATIONS.md states what was not established. SOURCE_VERIFICATION.json records primary-source versions, public URLs, byte counts, hashes and inspection scope. RESEARCH_LOG.md and turns.jsonl record the five approach families and their gaps.

## Reproduction

Use Python 3.12 and SymPy 1.14.0 (other recent versions may work). Run:

    python verify.py > replay.json
    cmp EXACT_RESULTS.json replay.json
    python test_controls.py

The script uses SymPy to propose factorizations, then checks each factor by a separately implemented Rabin irreducibility test and checks exact multiplication. Polynomial coefficient lists are in ascending order. All computations are over prime fields; Theorem 2 itself is proved for odd prime powers. Stable branches are pruned only after the proven finite-orbit certificate succeeds. Their exact rational mass remains in the accounting.

These finite checks are not a proof of asymptotic settledness. The special-family and characteristic-two conclusions rest on the written all-depth proofs. The Markov support exclusion rests on the cited published theorem, not on absence in a finite search.

This directory contains authored material and public verification metadata only. No source PDF, extracted source text, corpus contents, private coordination files, authentication information or remote-write receipt is included. It is an author packet awaiting fresh independent audit; it is not a publication or review approval.
