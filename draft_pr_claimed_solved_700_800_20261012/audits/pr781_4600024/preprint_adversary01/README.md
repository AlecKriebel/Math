# PR781 preprint adversary01

This closed authored packet reviews the old exact six artifacts bound by INPUTS.json. It reports one repairable FIFO blocking-read issue; no mathematical issue was identified. Read REPORT.md and MATH_DERIVATION.md.

Use the externally reported MANIFEST.json SHA256; a digest supplied by an untrusted packet is not independent authentication. The checker is explicit-exception and performs no writes. Example:

    python3 -I -B verify_custody.py --expected-manifest-sha256 PIN --input-root REVIEWED_PACKAGE
    python3 -I -B -O verify_custody.py --expected-manifest-sha256 PIN --input-root REVIEWED_PACKAGE
    python3 -I -B test_custody.py --expected-manifest-sha256 PIN --input-root REVIEWED_PACKAGE --scratch OWNED_SCRATCH

REVIEWED_PACKAGE can be the preserved review01_input revision. It must contain the old exact source directory, six artifacts and RELEASE_INVENTORY.json. Repaired inputs intentionally fail these historical bindings.

The read-guard reproduction copies only into caller-owned scratch and checks the old original verifier:

    python3 -I -B reproduce_read_guards.py --input-root REVIEWED_PACKAGE --scratch OWNED_SCRATCH

It intentionally records the defective manifest/PDF FIFO timeout; this is diagnostic evidence of an issue, not a passing verifier control. No candidate mutation occurs. The independent_profiles.py finite ternary controls need only standard-library Python and are not a proof of the general theorem.

The manifest inventories every flat file except itself. No primary-source full bodies, rendered pages, nested scratch directories, remote credentials or publication mutations are part of this packet.
