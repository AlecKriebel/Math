# Independent audit packet

Verdict: ACCEPT_COMPLETE_COUNTEREXAMPLE for problem 30003703 / OWR-15987-013.

The audit accepts D_n(5) != A_n(5) for n >= 4 and D_n(6) != A_n(6) for n >= 3, in precisely the rational SL2 component-function setting of the primary conjecture. It makes no novelty claim.

Read AUDIT.md for the complete reasoning and limitations. BINDING.json fixes the exact authored release reviewed. SOURCES.json contains source metadata and inspection limits. NEGATIVE_CONTROLS.json describes the 12 mathematical adversarial controls. independent_controls.py uses its own exact-arithmetic implementation; independent_results.json retains its full result. It never imports the authored verifier.

Requires Python 3.8 or newer, standard library only. Given sibling release/ and independent_audit/ folders:

    python3 -B release/validate_release.py
    python3 -B independent_audit/independent_controls.py --release release
    python3 -B independent_audit/validate_audit.py --release release

AUDIT_MANIFEST.json covers every other file in this folder. Its own SHA-256 is supplied in the audit handoff. The release manifest must have SHA-256 9770e7f73a5ffc81f52d92c38f3bebcc9714b470b854f9281e9749b4584591be. The audit leaves that release untouched.

No public-source PDFs, extracts, page images, raw records, or private coordination files are included. The scripts need no network and write no files when run with -B as shown. CORRUPTION_TESTS.json records separate temporary-copy tests of rejection behavior.
