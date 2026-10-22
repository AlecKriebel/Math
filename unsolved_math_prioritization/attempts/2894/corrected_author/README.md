# Verification packet: KP-4.18 / 2894

Read REPORT.md for the outcome, PROOF.md for the theorem-chain deduction and exact remaining gap, status.json for machine-readable disposition, and sources.json for public source identities.

This authored-only packet excludes source PDFs, source extracts, dataset contents, and private coordination. Public dataset hashes and source identities are verification metadata only.

Run:

python verify_packet.py . /path/to/FOUR_MANIFOLD_SIMPLE_2894_CORRECTED_EXTERNAL_MANIFEST.json /path/to/FOUR_MANIFOLD_SIMPLE_2894_CORRECTED_SAFE.zip

The same check is supported under python -O. Omitting the final ZIP argument performs only packet-file and metadata checks, and reports zip_verified false; it does not check the archive. The external manifest binds the verifier and every other packet file, as well as the ZIP. Treat it as a separately retained integrity reference; this is not a cryptographic signature or formal proof assistant. The checker does not fetch sources or validate the cited mathematical theorems.

This corrected derivative preserves the author freeze separately. Its literature implication and artifact were independently audited; the cited algebraic L-theory theorems were not independently re-proved. The canonical combined status is unsolved, with one of five approaches used. No publication has been performed by this audit.
