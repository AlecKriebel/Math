# Canonical-potential exponent converse: verification package

Alec Kriebel, version 1.0, 17 October 2026. Extensively AI-assisted and unrefereed;
no external human peer review or formal proof-assistant certification.

This package independently certifies a negative answer to the canonical-W
exponent converse in Schumann's OWR 20/2021 report, printed p1125. It does not
refute the later varsigma-coordinate conjecture or establish current openness.
The reduced word and entire transformed support already occur in Denis
Mironov's public crystal dataset, Case 267, in commit
0d6e564cf5e69d79c1074d5d1e3e72ac700904d6 (Git date 6 March 2020), cited by
Koshevoy--Mironov's 2022 computational paper. We claim no first discovery of
these data. The note is an attributed coordinate clarification with independent
canonical reconstruction and directly checkable facet certificates.

## Primary, dependency-free verification

From the extracted package root, run Python 3.10 or later:

    python3 verify.py

It uses only the standard library, has no network access, executes no source-
author code, and reconstructs the reduced-word seed and canonical optimized
pullbacks over exact integer Laurent polynomials. certificate.json contains
both separately generated 22-row certificate tables. The program checks 22
unit-coefficient monomials, 968 integer separation products, 22 dimension-11 facets
in dimension 12, the chamber map, and 30 deliberately corrupted controls.
It writes results.json. Neither a historical program run nor a floating-point
LP result is a premise. Optional optimization-mode checks are:

    python3 -O verify.py
    python3 -OO verify.py

These use explicit exceptions, so correctness checks remain enabled.

## Independent symbolic reconstruction

Install the optional pinned dependency in an environment of your choice:

    python3 -m pip install -r requirements-optional.txt
    python3 reconstruct.py
    python3 source_controls.py

These separately traverse the reduced-word braid graph in two orders and
compute exact canonical pullbacks with SymPy 1.14.0. The earlier reviewer inherited candidate-containing context and was not
blinded; its output freeze preceded a local file comparison only. See
INDEPENDENCE_AND_CHRONOLOGY.md. Replay emits a neutral OUTPUT_DIGEST.txt,
without recreating historical chronology. The source-control script reproduces the published
D4 comparison example; normal Python execution is required because the optional
controls also use assertions. No downloaded third-party data are required.

## Fresh source-only reconstruction

A different reviewer received only the reduced word, Dynkin diagram and primary
references, without parent history or candidate results. It froze its complete
support before comparison and never inspected the candidate. The parent later
compared the frozen support with the candidate. Its separate implementation
checks all 12,504 directed chamber/braid edges, alternate optimizing routes and
22 further exact facet witnesses. Its historical receipt is preserved unchanged;
replay checks the frozen output and never regenerates historical chronology.
With the same optional SymPy dependency, run in normal Python mode:

    python3 -B blind_reconstruction/verify_blind.py
    python3 -B blind_reconstruction/verify_supplement.py
    python3 -B blind_reconstruction/verify_source_regression.py

The optional programs use assertions; do not use -O or -OO for those commands.
The primary verify.py retains all its checks under those modes.

## Files, sources and review limits

manuscript/main.tex is the complete PDF source. The reviews/ reports preserve
mathematical independence, tests, positive prior-data findings and source-
inspection limits. They refer to audit-local source downloads and historical
artifacts which are not all part of this portable package. Their scope is not
external peer review. References and complete mathematical formulas appear in
the manuscript. The original unlicensed source dataset, source-author programs,
third-party PDFs and extracts are excluded; use the cited public links instead.

The primary verification result concerns the exact displayed example, not a
classification, a novelty certificate, the general sufficient theorem, or a
proof of any later conjecture. MANIFEST.json binds distributed file bytes.
