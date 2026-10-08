# Reproducibility hardening of the independent audit checks

This addendum changes execution safeguards only. The accepted mathematical proof, corrected five-approach report and both audit texts are unchanged. The original scripts, result JSON and prior manifests are preserved separately; the hardened scripts are new variants accompanied by exact source patches.

## Result

Both hardened checkers pass under normal Python, `-O` and `-OO`, with real and effective UID 1000. Their complete arithmetic JSON outputs are byte-for-byte identical to the preserved original outputs. All 45 semantic-mutation runs fail active invariant guards in those same three modes.

The test input files were mode `0444`; their directory and the child working directory were mode `0555`. The nonroot process attempted an actual input-directory write and received `PermissionError`. Every positive checker invocation also enabled its own nonroot/read-only guard. Source hashes and directory contents were unchanged after the tests, and the working directory remained empty.

The receipt records six positive mode checks, 45 semantic-mutation rejections, six successful explicit external outputs, 18 output-path or overwrite rejections, and 18 controls reproducing the historical scripts' behavior. Child credentials were checked directly as UID/EUID 1000. These were not root runs against merely symbolic read-only permissions.

## Historical limitations preserved transparently

The original normalization checker used 15 Python assertions and wrote its result next to the script. Its normal-mode numerical run was valid, but the assertions disappeared under `-O` and `-OO`. The historical controls reproduce a concrete false pass: removing one of the two stabilizer crossing terms changes the computed evaluation from 16 to 32, yet the optimized original still emits a PASS payload. The same mutation is caught in normal mode. On actual read-only inputs, the original also fails when it attempts its implicit result-file write.

The original follow-up checker used 14 assertions, also wrote beside the script, and explicitly refused optimized modes. It did not silently claim optimized validation: its `-O` and `-OO` controls fail immediately with its documented enabled-assertions requirement. Its normal-mode arithmetic output remains valid, but read-only execution fails at its implicit write. A normal-mode Gram mutation is caught by its assertion.

Thus the earlier numerical receipts support their stated normal-mode arithmetic checks. They do not establish optimized or read-only reproducibility. This addendum supplies that missing execution property without changing or withdrawing any accepted mathematical argument.

## Hardened behavior

- All 29 assertions are replaced by explicit `require` calls raising `RuntimeError`; abstract-syntax inspection confirms that neither hardened checker contains an assertion statement.
- The optimized-mode refusal is removed from the new follow-up variant because its invariant guards now remain active in every tested mode.
- Output goes to stdout by default. There is no implicit write beside either script or in its working directory.
- An optional `--output` must name a new absolute destination outside the input directory. Relative paths, input-directory destinations and existing files are rejected. Exclusive file creation prevents overwriting between the existence check and the write.
- `--require-readonly` verifies nonroot identity, nonwritable script and input directory, and an actual failed write probe.
- `--mutant` is a testing control that deliberately corrupts a mathematical computation. Each provided mutation must fail a substantive invariant before any PASS result is emitted.

The normalized checker tests seven corruptions: doubled product evaluation, an omitted stabilizer crossing, a missing Heegaard constraint, a wrong Euler coefficient, a wrong stabilization genus shift, a wrong component rescaling exponent and a nonzero seam correction. The follow-up checker tests eight: a missing free closed-component color, ignored boundary-color conflicts, a dropped newly closed component, a wrong Euler weight, a wrong Gram exponent, a falsely commutative dihedral multiplication, a wrong Fourier sign and a uniform scalar substituted for componentwise normalization.

## Reproduction

Run `python3 validate_hardened.py` from an environment whose real and effective UID are 1000, with this directory and its preserved `historical` subdirectory available. The harness constructs separate nonwritable input and working directories, runs both programs in all three Python modes, applies the semantic controls, tests output safeguards and reproduces the historical limitations. It saves detailed logs and `HARDENING_RECEIPT.json` outside the nonwritable input copy.

The hardened checkers themselves can run under other ordinary nonroot user IDs. The UID-1000 requirement belongs to this particular reproducibility harness and receipt. Neither checker reads source documents, accesses the network or changes the mathematical artifacts.

The exact patches are `patches/check_normalization.py.patch` and `patches/check_followup.py.patch`. Their historical inputs and hardened outputs are hash-pinned in `HARDENING_MANIFEST.json`. The receipt records byte-identical reproduction of both complete original arithmetic outputs, rather than merely matching a PASS label or selected counts.
