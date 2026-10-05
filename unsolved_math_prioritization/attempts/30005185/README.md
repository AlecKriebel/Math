# Reduced Khovanov rank modulo four: unresolved partial investigation

Problem **30005185 / OWR-11101915-009**, queue rank 744. **Unsolved; 5/5 approaches used.**

The independent AI audit passes this as a correct unresolved investigation, with no mandatory corrections. It is not human peer review, a full solution, a knot counterexample, or a novelty claim.

## Verified result and remaining gap

Over Q or an odd-characteristic field, the slice-knot rank residue reduces exactly to the parity of the number of even X-exponents in the lifted Lee normal form. That geometric parity statement remains unproved. A maximum exponent of two does not determine the parity of the number of even exponents. Formal split-tower complexes are algebraic negative controls, not realized knot counterexamples.

The integral universal-coefficient parity obstruction is separate. The lifted-Lee argument does not extend here to characteristic two. Six explicit small integral cube controls are torsion-free; these checks are neither a census replay nor a procedure for deciding ribbonness.

- [Authored proof and precise gap](khovanov_30005185/PROOFS.md)
- [Five bounded approaches](khovanov_30005185/APPROACHES.md)
- [Independent audit and limitations](khovanov_30005185_independent_audit/AUDIT_REPORT.md)
- [Current publication status](release_status.json)

## Reproduce

Python 3.10 or later; standard library only. From any working directory:

    python -B /path/to/30005185/verify_release.py

The wrapper checks the full publication allowlist, frozen sizes and hashes, both archive member sets and bytes, scope flags, author replay, and independent replay against its frozen receipt. It is safe to invoke the wrapper with Python -O: child checks explicitly run without optimization. Do not invoke the original assertion-based scripts with -O.

Both original freezes are unchanged. The author's pre-audit status and all no-remote-write statements describe their historical snapshots. The later independent audit and this wrapper provide the publication context. Public scholarly-source titles, URLs, hashes, byte counts and retrieval/inspection history are included; source PDFs, extracted text, raw census data and private coordination files are excluded.

The queue change is limited to this row's Status and Turns cells. Findings, Chat, DOI, all other rows and the pre-existing stale header are preserved byte for byte.
