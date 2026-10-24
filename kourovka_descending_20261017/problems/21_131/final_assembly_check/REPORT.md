# Independent final assembly delta audit

**QUALIFIED PASS — no required correction found.** Completed 2026-10-24T19:20:30.400947+00:00. Best-guess completion of this assigned assembly audit: **100%**; this is a workflow estimate, not a probability of mathematical truth.

This is the final release assembly guard after the two completed full package reviews. It verifies the delta, packaged execution and metadata consistency. It is not a new universal-proof review, originality certification, human peer review, or formal proof-assistant certificate. The previously disclosed original-1986 source-custody limitation and bounded priority assessment remain unchanged.

## Fixed artifact identity

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Final `publication/source-and-verification.zip` | 180781 | `566026ccf23b2ff0b24fcff41d80bf9c5fb7ef22729b68f1a06f254383626c4e` |
| Unchanged `publication/paper.pdf` | 92698 | `5788ee036f6b3c3932bb6c0c18e5ec581678bf5951a18d76d853545370fd0c9c` |
| Unchanged `preprint/main.tex` | 23341 | `36d6afdfa88437c9f1d35afa17e537b98edce4cfa698564475be554b69daaa2b` |
| Unchanged `zenodo-deposit.json` | 5189 | `474e667125730538c4959de79b1f0c5e223316356713db52b5def8b45fc71410` |

The complete per-file hashes and machine-readable results are in `assembly_receipt.json`. The archive and metadata were hashed again at the end without change. Standalone paper/source and archived copies are byte-identical.

## Exact delta from the reviewed 27-file package

The baseline is `receipts/package_before_final_review_report.json`, whose archive hash is `e1fc9b2568e324aa5d2d45d29ceeca79c390f5424c7d790e108d0be6a277ec19`. I independently confirmed all 27 baseline file hashes against the second review's retained extraction before comparing the final archive.

- **25 baseline files are byte-identical**, including paper, TeX, all original verification code/output, license and all prior source manifests/audits.
- **README.md** changes only by one paragraph explaining the separate 468-case stress script and requiring ordinary, non-optimized Python. `README_delta.diff` records the complete text delta. The standalone and archived final README agree.
- **MANIFEST.json** updates the README entry and adds the three new entries. Its final SHA-256 is `b6e181f79bfdc0f1bf8d1056840f6bfe155e64191839384f53fa30d148021d2b`.
- **Three additions**: `audits/final_package02.md`, `verification/review2_stress.py`, and `verification/review2_stress.json`. Each is byte-identical to the already-authored second review report, independent stress program, or its JSON output. Their hashes are, respectively, `cec2d267d06b7ffcf5983f22cd4b78150a9245a38cc645c4d6bcca03ed05fe81`, `263825d122064df3b1d2689b57f258883e3688d194e971624f810e55c881d6d2`, and `26402110373290c49b2737168d027ff169b39d32b9d9bedd0ecb81724f527465`.
- No removals or other baseline-file changes occur. The paper, mathematical source, original verifiers and deposit metadata remain unchanged.

All 30 ZIP entries are unique safe regular files under the single package prefix, without absolute/parent-traversal paths, backslashes, drive-style names, symlinks or encryption. CRC validation passes. All 29 manifest entries cover exactly the other 29 archive files; every size and SHA-256 matches. The manifest deliberately excludes itself, as stated.

## Fresh execution and added-script inspection

I extracted this exact final archive into `final_assembly_check/fresh_unpack/` and ran the documented entry points with ordinary Python, with `PYTHONOPTIMIZE` removed. Both return 0 and produce byte-identical packaged JSON:

- `python3 verification/run_all.py`: 11,778 section checks; 63 named matrix checks; 348,516 fresh tree comparisons; 3,516 fresh algebra assertions; the remaining construction-family and wreath/augmentation outputs also match the full expected JSON. Output SHA-256: `55c7234689788a5991d9b144575bce9658ec00d97011555079baef6d5d9e69a8`.
- `python3 verification/review2_stress.py`: 78 named comparisons over each of field orders 2, 3, 4, 5, 7 and 11, totaling **468**, with both negative controls true in every case. Output SHA-256: `26402110373290c49b2737168d027ff169b39d32b9d9bedd0ecb81724f527465`.
- Canonical `-O` and `PYTHONOPTIMIZE=1` invocations both refuse execution with exit 1 and the documented assertion-safety message.

I read the entire added stress program. It imports only the standard library and no packaged evaluator, uses a fixed pseudorandom seed, and asserts concrete 12-by-12 matrix equalities with UT4 coefficient matrices. Its inverses use the valid terminating geometric series for strictly upper triangular 4-by-4 matrices. The 468 count is 24 times three named comparisons plus six distinct-index elementary commutator cases per field. Separate actual assertions check two-sided inverse correctness, coefficient noncommutativity and failure of the auxiliary diagonal-map homomorphism; the recorded booleans follow these assertions. The README correctly requires non-optimized Python for this assertion-based supplement.

For order four, XOR addition/negation and reduction modulo `t^2+t+1` implement F4 using two-bit coefficients. To check the actual packaged helpers, I extracted their definitions from its syntax tree, evaluated them at q=4, and exhaustively checked all 64 element triples for addition/multiplication associativity, commutativity and distributivity, plus identities, additive inverses and nonzero multiplicative inverses. The multiplication table is `[[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]]`. These are finite checks only; no new universal mathematical conclusion is inferred.

## Metadata and scope

The unchanged deposit file's two file paths exist and identify the exact audited PDF/archive. Its title, Alec Kriebel author/ORCID, 24 October 2026 date and version 1.0.0 match the paper and README. Its `cc-by-4.0` license matches the README and package LICENSE, which explicitly applies to the paper, original prose and code. Third-party article bodies remain absent. The README continues to distinguish finite checks from infinite proofs, the canonical embedding from the homogeneous section statement, and AI review from independent human peer review. The added historical report preserves the 27-file hash it actually reviewed and is clearly separate from this 30-file assembly audit.

No reviewed candidate, Git state or publication record was modified. No external individual was contacted, and no child agent was created. All audit-generated files are confined to `final_assembly_check/`.
