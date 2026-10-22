# PR788 definition/topology validation packet

Read REPORT.md for the mathematical conclusion and exact scope. INITIAL_POSITION.md preserves the source-only pre-author position. Source PDFs/text/images and test copies are excluded.

The caller must independently SHA256-pin VERIFY.py before execution, and supply a trusted MANIFEST.json SHA256. Run `python3 -B VERIFY.py --manifest-sha256 PIN --input-root /absolute/path/to/intake`. An optimized run with `-O -B` is supported. No writes or network access occur in verification.

MANIFEST.json inventories every other packet file. INPUT_BINDINGS.json binds source record, root identity, original proof and inspected historical reports. DIAGNOSTIC_RESULTS.json is replayed by the checker. CONTROL_RESULTS.json records actual preseal runs of the same checker/diagnostic code, including rejection controls; its stage manifest differs from the final manifest solely because control results are added after those runs. The final sealed packet is independently replayed after sealing, with receipt outside the packet to avoid circular hashes.
