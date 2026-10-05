# Independent audit of problem 30002653

Verdict: PASS for the retained, restricted all-components-invariant theorem and lemmas; the unrestricted target remains unsolved after 5/5 approaches. No novelty claim. See AUDIT.md for the mathematical audit and one nonblocking wording clarification.

Reproduce the original author checks without changing their packet:

    python3 ../safe/verify.py

Reproduce the independent standard-library controls:

    python3 independent_controls.py --packet ../safe --output /tmp/prym-independent-results.json

Run from any working directory using absolute paths if needed. The independent checker imports no author code and checks externally pinned author manifest and research hashes. Compare the newly generated result with INDEPENDENT_RESULTS.json. The recorded relocated replay performed exactly that comparison.

The finite checks support the conceptual proof; they are not a formal verification or an exhaustive general-cover enumeration. Odd fixed-branch-degree configurations are labeled algebraic tests, not geometrically realizable covers.

All files here are authored audit content, code, or verification metadata. Public-source PDFs, extracted text, page images, raw records, and private coordination files are excluded. MANIFEST.json lists every other audit file with a byte count and SHA-256. Its own digest is supplied externally. The author packet remains separately frozen and unchanged.
