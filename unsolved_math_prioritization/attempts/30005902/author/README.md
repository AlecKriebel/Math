# Hopf cohomology brackets: unrestricted-field counterexample

Target: 30005902 / OWR-14298370-002; catalog rank 802.

**Author result, independent audit pending:** the literal unrestricted-field vanishing statement is false. A 27-dimensional Hopf algebra over F₃ has [f_x,f_y]=−f_z≠0 in Ext_H¹(F₃,F₃). It is non-quasitriangular and has S²=id. The proof checks cocycles, the exact Hopf-to-Hochschild embedding, and nonboundaries explicitly.

**Scope boundary:** this does not settle the finite-dimensional characteristic-zero variant or a separately imposed restriction excluding cohomological degree one. No new-theorem priority, editorial acceptance, or human peer-review claim is made.

Read `PROOF.md` for the argument and `SOURCE_AUDIT.md` for provenance, source scope, and prior-work limitations. One substantive proof approach was used, then proof search stopped; four of the five permitted approaches were unused.

Verification, requiring only Python's standard library:

    python3 verify_counterexample.py
    python3 verify_packet.py

For an authenticated freeze check, supply the separately recorded manifest digest as `--manifest-sha256 DIGEST`; add `--negative-controls` to test eight altered packets. Without a supplied digest the packet verifier checks internal consistency only.

The mathematical replay makes 26,584 exact assertions, including four negative controls. The packet integrity replay checks the frozen manifest and reproduces the result bytes. Exact computation supports the written proof and is not represented as a formal proof-assistant proof.

The packet contains authored mathematics, code, result files, and public verification metadata only. It contains no downloaded papers, source extracts, images, full dataset records, raw corpora, or private coordination material. Nothing was written to the remote repository during this investigation.
