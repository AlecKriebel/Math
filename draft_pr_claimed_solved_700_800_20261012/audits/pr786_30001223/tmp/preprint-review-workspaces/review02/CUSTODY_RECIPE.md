# Review02 custody and reproduction

Use caller-held final review MANIFEST.json and custody_check.py SHA256 pins from the parent handoff. MANIFEST.json is the sole self-hash exception. The final pin is recorded outside the packet in the owned scratch; a pin obtained only from an untrusted copy is not independent authentication.

With PACKET the review02 folder, INPUT the authoritative frozen preprint-review-inputs/review02, T the supplied PR786 RAM root and SCRATCH the owned preprint-review-scratch02:

    python3 -B PACKET/custody_check.py --packet PACKET --input-root INPUT --expected-manifest-sha MANIFEST_SHA --expected-checker-sha CHECKER_SHA --primary-root T --visual-root SCRATCH
    python3 -B -O PACKET/custody_check.py --packet PACKET --input-root INPUT --expected-manifest-sha MANIFEST_SHA --expected-checker-sha CHECKER_SHA --primary-root T --visual-root SCRATCH

Input paths are explicit so preserved copies can be rehomed. The checker independently closes all9 inputs, sourceZIP213 members, full selected record/prior and41 original Git blobs, paper TeX/PDF,6 release outputs, upload-kit metadata, current source pins and review receipts. Optional primary-root/visual-root verify the actual4 supplied source PDFs and5 viewed renders. Core custody does not pretend to reproduce absent third-party bodies or visual judgment. The initial whole-paper position is hard-pinned.

Copied-input custody controls:

    python3 -B PACKET/test_custody.py --packet PACKET --input-root INPUT --scratch SCRATCH

Copied source/builder/verifier controls:

    python3 -B PACKET/software_guards.py --source SCRATCH/bundle --pdf INPUT/output/pdf/paper.pdf --scratch SCRATCH

The supplied SCRATCH/bundle was extracted only after verifying frozen input/source manifest pins. A fresh extraction must reject repeated/unsafe/nonregular ZIP names and independently verify that exact source manifest. Guard programs write only temporary owned copies in scratch, remove them, and leave original inputs unchanged. No tests mutate the closed paper/package or old priority packet. POSIX nonregular controls have5-second timeouts. They do not certify hostile concurrent-filesystem race resistance.

Exact program and build command arrays are stored in REPLAY_312_NORMAL/OPTIMIZED, REPLAY_SYSTEM_CORE, CUSTODY_SYSTEM_OPTIMIZED and BUILD_312_NORMAL/OPTIMIZED receipts. NumPy is used only via the specified bundled Python3.12.14 runtime. Full bundled replay includes24 children; standard-library-only core replay includes20. The six regenerated output hashes match the frozen release inventory byte-for-byte.

CUSTODY_TEST_RESULTS records an earlier testing manifest before adding that receipt. The final manifest includes the receipt; final positive normal/O replay is stored outside the sealed packet to avoid circular hashes. No optimization-sensitive asserts protect the checker.

REPORT and MATH_RECONSTRUCTION provide human review, not a proof-assistant certificate. Initial prior exposure/reused-session limits and priority uncertainty are explicit. Third-party full bodies/images remain outside this authored flat review packet. RAM is the actual staging location; root manages canonical/durable preservation and publication.
