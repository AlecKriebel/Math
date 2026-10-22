# Offline finite verification

Use installed Python3 with a trusted standard library. Obtain the package-manifest SHA256, archive SHA256 and verifier SHA256 from the separately published deposit metadata/repository freeze. Authenticate verify_package.py BEFORE execution. A hash sidecar shipped with the same mutable bytes is informational and not independent authority.

The verifier requires Python -I -S -B and exact closed package identity. With absolute paths, run:

    python3 -I -S -B /trusted/verify_package.py --archive /download/habiro-rank-interpolation-verification-v1.0.zip --archive-sha256 EXTERNAL_ZIP_SHA256 --manifest-sha256 EXTERNAL_MANIFEST_SHA256 --run-checkers --work-dir /owned/empty-work

Alternatively use --root /owned/extracted-package and omit --archive/--archive-sha256. Keep work outside the closed package. Repeat with outer -O and -OO; a changed-ambient run uses PYTHONOPTIMIZE=2 plus hostile PYTHONPATH/user-site and a different working directory. Because -I ignores ambient optimization, the env2 outer optimization is0, with explicit inner normal/O/OO launches. Exact receipt schemas and original bytes remain unchanged.

Supported stages: independent exact math; original author_v3/bootstrap.py packet; original audit_algebra/audit_controls.py; original audit_source_bridge/independent_algebra.py. Each is run at inner optimization0,1,2, for12 launches. Per-stage raw stdout must match across those modes. A separate explicit exception guard remains active in all modes. The verifier authenticates every payload, all33 original Git blobs and mode100644, and the independent math SHA256ff44cdce74d36b40995843f7bc450e31fcac532163f3a411da51f3244ea82601. ZIP metadata is checked completely before member decompression; nested archive inventories are required if any ZIP is included.

Successful status PASS_CLOSED_FINITE_PACKAGE with its replays is a finite-package observation only. Read all scope fields: Linux legacy/bwrap/EROFS, source reading, topology reproof and whole-filesystem readonly remain NOT_RUN/NOT_TESTED; priority/human/formal/full-paper certification remain false. The actual original full Linux replays are NOT_REPRODUCED here. See AUDIT_LIMITS.md.

Engineering fixtures can be replayed after authenticating both test and driver:
    python3 -I -S -B /package/engineering/test_profile.py --originals /package/original/unsolved_math_prioritization/attempts/10400145 --verifier-sha256 EXTERNAL_DRIVER_SHA --work-dir /owned/empty-work
The test expects its adjacent engineering/verify_package.py and engineering/independent_math.py, which are preserved exact copies. Its92 controls were run under outer normal/O/OO with actual optimization-specific verifier compilation; included cold fixtures and direct semantic mutants do not confer mathematical acceptance. Pure observation predicates are tested separately and receive no service authority.

The three-page PDF is byte-identical inside paper/ and in the separate deposit upload. Compile paper/main.tex with a current TeX environment; PDF bytes can differ across compiler/date/font environments even when the mathematics/layout agrees. The provided PDF is the rendered and inspected publication artifact. No raw source corpus, third-party PDF or credentials are required for the finite profile; rechecking cited topology requires obtaining the primary sources separately.
