# Erdős 156: audited interval-Sidon partials

Queue row 1856, corpus ID 1963. **UNSOLVED.** This publication contains authored mathematical deductions, finite checks and an independently verified construction certificate, plus public source metadata. It contains no third-party source documents or dataset contents. No logarithm removal, novel result, exhaustive contemporary literature verdict, or eight-mark threshold optimality is claimed.

## Accepted mathematical scope

- Exact ordinary-Sidon saturation includes midpoint and repeated-summand blockers.
- The parity-sensitive necessary bound is 2N ≤ k³+k−2eo.
- Difference-budget completion has the stated seed-coverage conditions and optional exception set; modular saturation alone is insufficient.
- Interpolation works with a suitable seed family and O(n^(2/3)) gaps; no such family is constructed.
- The eight-mark N=144 certificate proves existence only, not g(144)=8 or optimality of 144. Witness equations are authored mathematical certificate data, generated and independently verified here, not copied third-party source text. The underlying example is attributed in FIVE_APPROACHES.md.

FIVE_APPROACHES.md and INDEPENDENT_AUDIT.md are the accepted, byte-preserved mathematical documents. The author's exhaustive implementation covers N≤16. The separately written independent implementation covers N≤15. The reviewer also read and reran the author's N≤16 implementation; this is not independent implementation coverage through N=16.

SOURCE_GATE.md and PUBLIC_SOURCE_METADATA.json record bounded inspection/search evidence. The official page returned HTTP 403; the indexed OPEN classification was four months old. The finite preprint's computational archive was not independently replayed. These limitations remain in force.

## Reproduce

Python 3 standard library only. From this directory:

    python verify_package.py
    python -O verify_package.py
    python test_controls.py
    python -O test_controls.py

The verifier checks the exact recursive file inventory, prohibits symlinks, nested manifests, unsafe paths, duplicate keys, unlisted files and empty directories, verifies AST equivalence, and executes both mathematical programs in temporary copies in ordinary and optimized modes. Every byte of stdout and all three final JSON output files must match the frozen replay evidence. Subprocesses run outside the packet directory to check working-directory independence. The root manifest excludes only itself; its external hash belongs in the acceptance receipt. Manifest self-consistency is not an authenticity claim; compare the externally frozen package manifest hash.

Direct mathematical runs are also available:

    python checks.py
    python -O checks.py
    python independent_audit.py
    python -O independent_audit.py

They deterministically regenerate results. The independent verifier requires both the certificate and author results before doing its checks. It never silently skips a missing certificate. test_controls.py executes actual certificate, equation, finite-value, and midpoint-algorithm corruptions in both modes, plus missing-input, recursive-inventory, and enumeration-domain AST negative controls. It creates mutations only in temporary copies.

## Optimization-safe conversion and historical hashes

The original programs and their original three JSON outputs are preserved under original/. These are historical audit inputs, not the recommended optimized-mode entry points: their Python assert statements would disappear under -O.

For the root programs, every Assert(test, msg) AST node is mechanically replaced by If(Not(test), [Raise(AssertionError(msg))], []), omitting the exception argument when no message was supplied. This retains normal assertion evaluation and lazy message evaluation, but does not disappear with optimization. All other original AST nodes are identical. The independent program additionally receives a fixed, explicitly checked prefix that requires certificate_N144.json and checks_results.json to exist. verify_equivalence reconstructs precisely that transformation and prefix, compares complete ASTs without positional attributes, and rejects any remaining Assert nodes. AST equivalence is not a replacement for the mathematical audit or execution replay.

The historical independent-audit hashes in INDEPENDENT_AUDIT.md refer to original/ versions. Converted verifier hashes and its self-reported output differ by design; the root independent_audit_results.json and replay/independent_audit.py.stdout bind the converted verifier. Author results and certificate remain byte-identical to the originals. No published original claim is silently widened by the packaging conversion.
