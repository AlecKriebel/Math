# Independent computational and integrity review

PR 908; problem 30006191 / OWR-14299085-005; frozen `bounded_region_v2`; head `a35667b1bb0bafed69916709997a4684223ecc93`. This review examines the one eligible bounded-region candidate and preserves its historical 1/5 claim. It does not audit a legacy packet or promote the full five-part program.

The finite mathematical controls pass, with no counterexample found to the sampled algebra. Publication tooling needs repair: the historical assertion-based checkers can emit PASS with genuine failures under optimized Python, and the old wrapper has incomplete inventory and outer-manifest validation. No mathematical proof edit is indicated by this family. The 26 original files were verified before and after and remain unchanged.

## Claim and evidentiary limits

The target is an existential continuum result in three dimensions: fixed ball B(0,4), unregularized density convention L(L−sigma), sigma in {0,1}, fixed smooth normalized f, packed N/N+1 Slaters, and times pi/(2N+1−sigma). The claimed annihilation-vector and operator-norm differences tend to two. This is a norm statement along changing states, compatible with continuity on each fixed vector. It is not a fixed-density prediction, statement for all potentials, or claim in dimensions one and two.

CONTROL_PLAN.md was written after reading the mathematical claim and before reading or importing any historical checker. The independent code constructs creation matrices from occupation parity and Slaters from determinants; it imports no author/audit code. Historical programs were subsequently executed only in disposable copies.

The strongest computational evidence is finite exact algebra plus numerical diagnostics. It cannot establish infinite-dimensional domains, Sobolev bounds, uniform estimates for all N, or the continuum limit. Those remain written-proof obligations for the independent analytic families. No discretized continuum Hamiltonian, empirical physical prediction, or rigorous floating interval enclosure is claimed here.

## Independent mathematical controls

`independent_math_checks.py` passes 2,668 exact predicates and 558 floating diagnostics. Exact means integer/rational/SymPy symbolic calculations, with explicit guards; the floating absolute tolerance is 2e-11 and maximum equality residual is 3.295848094936011e-14. Counts are calls of predicates/diagnostics, not claims of statistical independence or exhaustive proof.

The exact controls include CAR and parity signs in one through four modes; diagonal density versus off-diagonal normal ordering; vacuum and one-particle sectors; rationally rotated occupied and leakage projections; first/second moments for n=0 through four; determinant versus creator Slater orientation; a noncommuting two-mode cutoff Duhamel sign; sector-potential differences for n=0 through twelve; both phase conventions for N=1 through 32; finite packing ceilings N=1 through 2,000; and dimension exponents d=1 through eight. q=0, q=I, and empty/full occupied spaces are included. The Slater identity is checked using independently built many-body matrices and one-body traces.

A same-sector correlated six-mode state is an exact countercontrol: (|111000>+|000111>)/sqrt(2), with q projecting onto the last three modes, has mean 3/2 and variance 9/4. Thus Var(M)≤mean cannot be used for arbitrary interacting states. The candidate applies this bound to freely evolved Slaters, which is the appropriate state class.

Floating controls use complex random orthonormal frames, generic Hermitian free generators, varied ranks of q, n=1 and m−1 in four/five/six modes, and generic as well as special phase times. Full Fock evolution agrees with the creation matrix element `exp(i t (2N+1−sigma)) <f,exp(i t h)f>`, and the annihilation witness is its conjugate minus one. Generic times expose phase and bra errors that a phase of minus one could conceal. The controls reject wrong phase 72 times, wrong bra 108 times, false late orthogonality 108 times, mean-as-second-moment 54 times, and mean-as-M-norm 108 times. The late free occupied overlap is intentionally allowed to become nonzero; initial orthogonality suffices for the CAR matrix element.

An independent finite local interaction also checks the two-evolved-vector bound and vector Duhamel identity, with 48-node numerical quadrature. These are diagnostics and are not rigorous enclosures. The finite commutator model separately checks the leakage upper bound for positive, zero, and negative times.

## Uniformity and continuum gap

The written mechanism uses one fixed cutoff chi with fixed bounded derivative norms. Its commutator is bounded from H1 to L2 by a constant determined by those norms. Packing gives total initial H1 energy at most a fixed constant times n^(5/3), including the fixed f contribution. Consequently lambda≤C s² n^(5/3); the Slater second moment gives ||M Phi||≤C(|s|n^(5/6)+s²n^(5/3)). Integrating 2n times this expression yields n^(11/6)t² and (2/3)n^(8/3)t³. This algebra is checked exactly.

For both conventions and N≥1, t_N≤pi/(2N), and n=N or N+1≤2N, so the constants can stay uniform. The three-dimensional powers are −1/6 and −1/3. The general exponents −1/2+1/d and −1+2/d are negative precisely for d>2; they vanish at d=2 and grow at d=1. Endpoint failure of this estimate does not prove the theorem false there. Smooth fixed f also makes its free overlap tend to one; the finite tests do not replace that strong-continuity argument.

The remaining analytic gap for this computational family is independent validation of the continuum functional analysis and its all-N estimates. No difficulty is hidden by assuming an interacting state stays Slater, omitting a creation-bra evolution, or discarding density diagonal pairs: these are all separate controls. Final mathematical acceptance must include the analytic/source families.

## Unchanged frozen replay

All twenty executions pass: wrapper integrity/full plus author/audits A/B, each under normal, -O, -OO, and PYTHONOPTIMIZE=2. Available environment: Python 3.14.6, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0, mpmath 1.3.0. Historical audit B records Python 3.12.14. The runner observes parent and child optimization without changing frozen code.

CLI -O and -OO do not propagate to historical wrapper children, which run at optimize=0. Inherited PYTHONOPTIMIZE=2 does propagate, so all children run at optimize=2. AST counts are wrapper zero, author 27, audit A two, audit B 25 assert statements. Optimized PASS outcomes do not validate removed predicates.

No replay output is claimed byte-identical or JSON-identical to historical saved results. The author numerical difference is 4.44e-16, audit A's Duhamel ratio differs by 5.87e-13, and audit B's numerical differences are at most 3.99e-14. Current controls pass their original tolerances. Historical author/audit B saved source-byte PASS fields differ because fresh source-byte checks were not requested. No PDFs were retained or read by this family, and historical PDF/corpus hashes are not treated as freshly verified source bytes.

Audit A's 5,659 check() calls contain 5,000 integer phase/polynomial predicates, two exact symbolic integral/decay predicates, and 657 floating or mixed predicates. This count includes shared parameters and duplicate labels. Audit B's 16,768 and the author's 4,288 sector cases are sampled integer checks; none of these counts turns a finite program into the continuum proof.

## Historical validation failures

Twenty-four optimization fixtures distinguish corruption from mathematics. Unchanged author/A/B programs reject altered proof bytes normally but emit PASS in each optimized mode. Deliberately false mathematical asserts in author/B likewise fail normally and emit PASS optimized. Audit A's deliberately false explicit `check()` fails in all four modes. These fixtures mutate only disposable copies, not the candidate.

Twenty-two bounded historical wrapper fixtures show actual boundaries. The old wrapper rejects missing/extra regular files, PDF/CSV source extras, internal symlinks, an expected README replaced by FIFO, changed nested manifests, unsafe manifest paths, and a semantic proof change even after rehashing author/PACKAGE manifests. Its proof and nested pins therefore supply useful protection.

However it accepts undeclared empty directories, extra FIFOs/sockets, a root symlink alias, outer problem_id=True, revision=999, an added metadata key, and a duplicate outer JSON key. It lacks an independently fixed outer PACKAGE hash and reads that manifest before checking its type. A PACKAGE FIFO blocked until the harness terminated the subprocess after two seconds. None of these tooling findings falsifies the mathematical theorem; they do preclude treating the historical wrapper alone as a safe publication gate.

## Independent portable verifier and negative controls

`verify_frozen_packet.py` is a standard-library utility with fixed external HEAD/PACKAGE/proof pins, three nested pins, exact file and directory allowlists, strict JSON/type/path handling, and explicit guards. It checks lstat before reads, rejects symlinks and special nodes, and uses O_NOFOLLOW/O_NONBLOCK plus fstat identity checks for final-entry races. It does not claim protection against concurrent ancestor-directory renaming. It accepts the direct packet, standalone original_packet, and the current original/full-prefix layouts.

All 104 negative runs (26 fixtures by four modes) reject safely without timeout. All twelve positive layout/mode controls pass. The fixtures cover missing/extra/source files, empty directories, FIFOs/sockets, expected-file and manifest FIFOs, internal/root symlinks, wrong roots, rehashed semantic proof changes, malformed/duplicate/bad-type/path JSON changes, nested changes, and all three substituted external anchors. The new mathematical false guard also rejects in four modes. AST scanning confirms zero assert nodes in all six authored utilities.

The external Git head and outer PACKAGE fingerprint must be authenticated independently; this review uses the pins supplied by the parent audit. SHA-256 fingerprints are not cryptographic signatures, proof certificates, or evidence of authorship. Anyone who replaces both the verifier and its anchor can defeat consistency checks; that is an external trust failure. Nested/source metadata fingerprints describe frozen bytes, not a new source retrieval.

## Reproduction

Use Python with NumPy, SciPy, and SymPy for mathematical controls and old full replay; the packet verifier itself needs only the standard library. From this review folder:

```
python verify_frozen_packet.py --root /absolute/path/to/original_packet --output receipt.json
python independent_math_checks.py --output math_receipt.json
python reproduce_frozen.py --packet /absolute/path/to/original_packet --python /absolute/path/to/python --output replay_receipt.json
python compare_replays.py --packet /absolute/path/to/original_packet --replay-receipts replay_receipt.json --output comparison.json
python negative_controls.py --packet /absolute/path/to/original_packet --python /absolute/path/to/python --output negative_receipt.json
```

The replay and hostile fixtures create ignored disposable tmp work and remove their packet copies; they never mutate original_packet. Relative roots containing parent traversal are intentionally rejected. Reports contain only authored diagnostics, control metadata and fingerprints, without source documents, extracted source text, data corpus, screenshots, or API payloads. No Git mutation, publication, PR comment, spreadsheet edit, or external communication was performed by this family.

The initial replay harness omitted TMPDIR for the unchanged wrapper's nested temporary copy, so that automatically removed transient copy used the platform temporary area. Final receipts were regenerated with TMPDIR explicitly confined to this review's tmp folder. The log records the oversight. Because the two harnesses had already been fingerprinted once, their exact initial versions and initial review-manifest bytes are preserved in historical/; these are provenance records, not entry points to execute. The independent packet verifier remained unchanged.
