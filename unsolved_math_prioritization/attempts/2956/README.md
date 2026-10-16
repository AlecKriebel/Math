# KP-4.80 / 2956: audited exotic mapping-class torsion partial results

Status: **unsolved, 5/5 mathematical approaches**. The authored mathematical report is accepted unchanged as partial progress. Neither existence question is settled. The executable verifier requires the separately preserved optimization-safe correction.

## Results and boundaries

For the standard symmetric leaf-neck construction on a connected sum of n identical oriented simply connected summands, the neck subgroup has rank 0 or n−1 over F₂ when n is odd, and rank 0, 1 or n−1 when n is even. For three K3 summands this reduces the proposed Klein four-group to one unproved neck-nontriviality statement. It does not prove that statement.

The η⁴=0 calculation kills only the specified nonequivariant framed Bauer–Furuta detector for three or more K3 summands. It does not trivialize the mapping class or an equivariant refinement. Additional capping, root-reflection and periodic-action restrictions remain conditional on the explicitly cited imported theorems. The original Ruberman proof was not inspected; its involution statement is imported through Konno's explicit formulation. No novelty claim is made.

- [Unchanged original report](original/frozen_v1/REPORT.md)
- [Independent mathematical and executable audit](audit/public/AUDIT_REPORT.md)
- [Acceptance and verification limits](ACCEPTANCE.md)
- [Actual ten-assert correction patch](audit/public/VERIFY_EXACT_OPTIMIZATION_FIX.patch)
- [Corrected verifier](corrected_v1/verify_exact.py)

## Preservation

The original freeze, receipt and archive remain separate under `original/`. The independent audit, its receipt and archive remain under `audit/`. Only the two corrected verifier artifacts are under `corrected_v1/`. The two existing ZIP archives are byte-for-byte preserved and their members are checked against the published source-free files. No scholarly source bodies, extracted source text, dataset contents, private files or private coordination material are included.

Original ZIP: 21,964 bytes; SHA-256 `cd72bc9863fb1cf4d99a22471ff712c7a59a3b2ed15d3323583204182865a570`.

Independent audit ZIP: 29,127 bytes; SHA-256 `ab0d2fb046f4cce7677a5f7589633f0cd31c618e53b8ca519391a109a01a3a07`.

## Reproduction and external trust

Python 3.10 or newer and a genuine real/effective UID 1000 are required. No network or source documents are used. First compare `BOOTSTRAP.py` against the external SHA-256 printed in this publication's draft PR description or a previously trusted acceptance receipt. Do not derive trust by computing a fresh hash from an untrusted packet. Review the bootstrap before executing it. The external bootstrap pins the verifier and manifest; the manifest pins the complete payload, and the verifier separately pins all accepted historical inputs.

After externally authenticating the bootstrap, run from any working directory, replacing PACKET with this directory's absolute path:

    python -I -S -B PACKET/BOOTSTRAP.py PACKET > normal.json
    python -I -S -B -O PACKET/BOOTSTRAP.py PACKET > optimized.json
    python -I -S -B -OO PACKET/BOOTSTRAP.py PACKET > optimized_twice.json

For trust-boundary, relocated read-only and hostile-working-directory controls, replace EXTERNAL_BOOTSTRAP_SHA256 with the trusted external value, and repeat in normal, -O and -OO modes:

    python -I -S -B PACKET/mutation_tests.py --root PACKET --bootstrap-sha256 EXTERNAL_BOOTSTRAP_SHA256 > controls.json

Each bootstrap invocation runs the original and corrected baselines, five source mutations against each, one genuinely recomputed independent RREF/permutation baseline, and eight independent semantic mutations. The independent mutants use the pinned expected-data cache; the independent baseline never does. The full baseline output bytes must match the frozen JSON. Every run retains full stdout and full stderr text in its JSON receipt; only the random temporary-directory name in stderr is replaced with `<temporary>`, explicitly marked in the receipt. The control harness includes those full receipts for its ordinary and relocated runs.

All executed specimens are 0444 files in 0555 directories; real UID/EUID 1000 file-append and directory-create probes must fail with PermissionError. Semantic rejection requires an actual AssertionError, empty stdout and exit code 1. Inability to write output is never counted as mathematical rejection. These are ordinary permission restrictions, not immutable mounts.

A PASS means that the precise scoped acceptance conditions and expected controls ran. It does not mean that the defective original optimized verifier is safe: across -O and -OO, its ten deliberately incorrect runs must falsely report success, reproducing the known defect. The corrected verifier rejects all fifteen source-mutant runs across three modes. Independent arithmetic rejects all twenty-four data mutants. Fresh source retrieval and fresh corpus matching are **NOT_RUN**. The archived eleven-PDF and two-dataset pin checks remain historical evidence only.

The expected-rank-only mutant changes a check rather than the emitted data, so its optimized false-PASS output is identical to the unmutated JSON. False-PASS classification is based on the missed semantic rejection. Every candidate execution additionally matches the preserved audit's exact per-case stdout hash, byte count and exit code; semantic failures retain the same final error message. An initial publication-wrapper condition incorrectly required every false-PASS output to differ from baseline; that preparation condition was corrected before publication, with no historical artifact or mathematical change.
