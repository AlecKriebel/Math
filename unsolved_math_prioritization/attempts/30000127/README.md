# Leroux entropy: corrected conditional partial results

The full target 30000127 / OWR-757-005 remains unresolved after 5/5 approaches. No sixth route, general three-state Oleinik bound or novelty claim is introduced. Read current/REPORT.md, the complete current/INDEPENDENT_AUDIT.md and current/CORRECTION.patch. All 17 accepted input files are preserved byte-for-byte.

The scalar face theorem assumes a bounded D-valued weak Cauchy solution with prescribed bounded initial data, interior generalized convex Lax entropy inequalities, and global membership in one specified face for both solution and data. It gives uniqueness and both Riemann invariant upper bounds with sharp common coefficient 1/2. The constant invariant on a face has zero slope. The source-kernel correction uses finite-scale W_epsilon, the uniform ||K_prime||_1/ell error, normalized profiles and strong local L1 passage; integral kernel normalization is not exact discrete normalization.

The trace-topology issue is specific to the inspected arXiv v2. It is neither a PDE/hydrodynamic counterexample nor an audit of an uninspected journal proof. The conditional invariant rectangle, positive-gap deterministic weighted estimate, physical-viscosity obstruction, natural-order non-attractiveness and positive-probability finite-ring event retain all stated hypotheses and limitations. No uniform hydrodynamic probability or unconditional system uniqueness/convergence is proved.

## Public reproduction and trust

Authenticate BOOTSTRAP.py against the independent SHA-256 in the reviewed PR description before executing it. Save the authenticated copy outside the packet. Make every packet file 0444 and each directory 0555. Run as actual UID=EUID=1000:

- python -I -S -B /trusted/BOOTSTRAP.py --controls /path/to/packet
- python -I -S -B -O /trusted/BOOTSTRAP.py --controls /path/to/packet
- python -I -S -B -OO /trusted/BOOTSTRAP.py --controls /path/to/packet

Omit --controls for positive and semantic replay only. The external bootstrap binds the complete recursive inventory, acceptance, all historical/pre-seal receipts, code and mode-specific fixed raw references. Every raw stdout/stderr byte and recursive JSON type is compared without normalization. Exact names and counts distinguish positive checks from intended mutation rejections, integrity negatives, schema negatives and comparator controls. Actual read-only create/append EACCES probes and before/after hashes run under UID/EUID 1000. Permissions are an accidental-write barrier, not kernel immutability or protection from intentional owner chmod.

The tested runtime is CPython 3.12.14 with SymPy 1.14.0 and mpmath 1.3.0. NO_SITE_RUNNER.py retains -I -S -B, explicitly adds sysconfig's installed purelib directory, checks dependency versions and origins, then executes the unchanged checker. It does not run site initialization or .pth hooks. The interpreter, standard library and packages in that installed directory are trusted, not authenticated by this packet. It catches expected ValueError validation exceptions at the adapter boundary and prints their type and complete message as deterministic stderr; this is the actual raw subprocess stderr compared, not a normalized traceback. Unexpected exceptions fail independently. Existing dependency installation is required; no installation is performed by the packet. Hostile working-directory and PYTHONPATH imports are tested, including shadow SymPy/mpmath and sitecustomize.

Each checker emits exactly eight named check families, not a count of all internal symbolic operations. There are two positive checker suites and eight intended mathematical mutation rejections per mode, six positives and 24 rejections across normal/-O/-OO. Historical accepted audit evidence separately records six positives and 24 rejections. Finite checks do not prove analytic or stochastic statements.

current/ACCEPTANCE.json, current/AUDIT_EVIDENCE.json, current/VERIFICATION.json, current/MANIFEST.json and current/ORIGINAL_MANIFEST.json are historical accepted evidence. current/run_audit.py is retained unchanged; its original harness is NOT_RUN here. Public source titles, URLs, hashes, sizes and inspection history are historical. Source bodies and private material are absent. Historical/original report replay, historical patch application, fresh source search, source-body replay, dataset replay and formal proof-assistant verification are NOT_RUN.

PREPARATION_RECEIPT.json and PREPARATION_CONTROLS_* are pre-seal evidence, not final trust anchors. The final manifest binds these delivered receipts. Final external receipts stay outside the inventory to avoid circular hashing. No QUEUE changes are included.
