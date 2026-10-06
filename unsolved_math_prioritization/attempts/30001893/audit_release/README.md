# Independent audit of 30001893

Verdict: PASS_PARTIAL_ONLY. Five of five substantive approaches are accepted as partial work. The full source problem remains unsolved by this package. No novelty or current global-openness claim is made.

Read AUDIT.md for the full mathematical adjudication, source limitations, and the independent polynomial dependency certificate. BINDING.json binds the untouched author ZIP and all eight release files. RESULTS.json records replays and the verdict; NEGATIVE_CONTROLS.json separates mathematical checks from scope and binding guards. INDEPENDENT_RESULTS.json contains the exact independent output.

Replay the independent controls with Python 3, using only its standard library:

    python3 -B independent_controls.py --author-release PATH_TO_FROZEN_RELEASE --author-zip PATH_TO_AUTHOR_SAFE_FREEZE.zip
    python3 -O -B independent_controls.py --author-release PATH_TO_FROZEN_RELEASE --author-zip PATH_TO_AUTHOR_SAFE_FREEZE.zip

The default paths work when audit_release, release, and AUTHOR_SAFE_FREEZE.zip are siblings in the original local task directory. No author code is imported or executed by this independent script. The separate recorded author replays used its documented commands.

Do not interpret test success as a proof of the full 4n-5 conjecture. The safe audit contains no scholarly PDFs, source extracts, images, raw records, or private coordination, and does not perform remote writes.
