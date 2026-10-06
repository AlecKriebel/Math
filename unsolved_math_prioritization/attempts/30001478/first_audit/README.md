# Independent audit of the projective-line quotient

Verdict: complete counterexample to both literal assertions in problem 30001478, independently checked. Read `mathematical_audit.md` and the characteristic-scope clarification in `scope_addendum.md`.

The `author/` directory preserves the nine extracted author-freeze files byte-for-byte. No author file was edited. All other files are independent audit work or public verification metadata.

Run with Python 3.9+, standard library only:

    python3 verify_audit.py
    python3 -O verify_audit.py
    python3 test_audit.py

The main verifier checks the exact recursive inventory, regular-file types, and every manifest hash before launching the unchanged author verifier, its 47-control test suite, and the independently written symbolic and finite-field checker. It never imports author code. Unexpected directories, source files, bytecode, symlinks, and nonregular entries are rejected.

The finite computations do not replace the universal proof. No novelty or publication-priority claim is made, and the result remains an unrefereed mathematical note. No PDFs, third-party text extracts, dataset contents, or private coordination material are included.
