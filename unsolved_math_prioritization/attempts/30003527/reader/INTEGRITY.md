# Offline reader-integrity checks

Run from any directory with Python 3.9 or later:

    python /path/to/reader/verify_reader.py
    python -O /path/to/reader/verify_reader.py
    python -OO /path/to/reader/verify_reader.py

All three commands perform the same checks. The implementation uses explicit failures and return codes; optimization does not disable verification. It requires only the Python standard library and does not contact the network or change the reader.

To pin the manifest to an independently obtained SHA-256 value, add:

    --expected-manifest-sha256 THE_INDEPENDENTLY_OBTAINED_HASH

Without that option, the verifier checks consistency with the manifest present in the directory. The manifest is not a digital signature. If both a payload and its manifest are replaced, internal agreement alone cannot authenticate provenance. The expected manifest hash must come from a trusted separate record, such as the independently reviewed repository commit or acceptance receipt.

## What is checked

- Exact file inventory, SHA-256 and byte count for every listed file, including the verifier itself
- Absence of unexpected regular files, source-PDF file types, symlinks, and nonregular filesystem entries; canonical paths confined to the reader
- UTF-8 decoding; unique JSON keys in parsed metadata
- Selected target identifiers and disposition fields: UNSOLVED, five new shared passes, exhausted continuation, unknown lifetime count, and no novelty/global-openness claim
- Pinned corrected theorem, final two acceptances, and correction-patch identities
- Absence of the superseded original as a current public proof
- Complete provenance inventory, including the one editorially transformed acceptance report
- Sixteen complete proof artifacts and eleven independent audit artifacts
- Existence and containment of local Markdown links
- Public source-identity records explicitly exclude source bodies

MANIFEST.json records every other public file but excludes itself to avoid a self-hash cycle. Its own digest is printed by the verifier and can be pinned externally. Empty directories are not material to the inventory. External websites and Markdown anchors are not checked.

## What is not checked

**Byte integrity is not a mathematical proof.** The script does not decide the truth of any theorem, verify all classical dependencies, authenticate source claims, establish novelty, or resolve the unrestricted question. Mathematical support consists of the complete authored arguments and the independent AI acceptance reports, within their stated scopes and source dependencies.

The program is an integrity utility, not a security sandbox or a proof that every possible false statement or disclosure is absent. Use a trusted verifier, or inspect and verify it independently before execution. Passing an expected hash to a program that has itself been replaced does not make that program trustworthy. The filesystem is assumed stable during a check; concurrent hostile changes are outside the assurance. Publication privacy and semantic scope were reviewed separately. Internal-only vocabulary checks belong to separate private QA and are not shipped in this reader.

Source inspection history is inherited from those reports. Source hashes identify particular inspected copies; no source body or extracted text is redistributed here.
