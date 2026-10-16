# Software guard component repair — PR411 / 6800014

**PASS for the repaired software component; no mathematical change.** The offline current19-file author candidate retains the exact source19 inventory and author status `claimed_solved`, turns2/5. Only the three current executable guards, current publication metadata, and three dated editorial/reproducibility addenda changed. Zero new author proof-search turns.

| Current script | Original static predicates | Actual mandatory evaluations in each mode |
|---|---:|---:|
| `verify.py` | 19 | 24 |
| `check_hessian.py` | 2 | 2 |
| `audit/independent_checks.py` | 18 | 28 |

Every original `assert P` is replaced by `if not (P): raise AssertionError(constant diagnostic)`. `guard_relation.py` proves the exact complete AST relation, preserving each predicate and its short circuit. No original assert message existed. `run_checked.py` wraps each predicate with a recorder returning the original object unchanged; the original `not` performs truth conversion once. This avoids line-trace overcounting of multiline guards. Every static guard is reached, and the54 actual evaluations and stdout hashes agree in normal/-O execution. The independent software adversary separately reversed the AST guards and checked stateful truth conversion and counts.

The full theorem and proof bytes, current `SOURCE_AUDIT.md`, six frozen author files, `FROZEN_AUTHOR_HASHES.json`, requirements, and historical `audit/INDEPENDENT_AUDIT.md` are unchanged. The main proof SHA256 remains `3009eff237f0c11059a2bed1241e04ac2dc5779f1c285c7138d4dc1ca1405472`; the audit remains `6dcef6481f4e5e62c4ea9ecd971498c5b562bb73671e63ec55ac8da9138b1516`. The two absent standalone historical byte objects remain **UNATTESTED**. Original historical `-O` output is **not certified validation**, since its assertions are erased.

Producer post-fix38 controlled executions all met authentic expected success/failure diagnostics. These include normal/-O entrypoints from a foreign cwd, a clean positive-whitelist archive extracted into a path with spaces, false actual algebra predicates, false current theorem interval, false publication claim, frozen/current/original metadata corruption, frozen proof corruption, checker corruption, missing/extra files, an unlistedFIFO, whitelist tampering, lazy Boolean traps, and an algebra predicate changed with candidate publication/whitelist/seal hashes consistently recomputed. Rehashing still fails the independently reconstructed AST relation. Captured outputs and all mutated fixtures remain private; `TEST_RESULTS.json` is a bounded native result summary, not a substituted successful receipt.

The new independent adversary found one actual blocker in the first component: an unlistedFIFO was ignored by file-only inventory. The fix rejects symlinks and every entry that is neither a regular file nor a directory; producer and adversary both retested it in both modes. Independent checks also reject sockets, file/directory symlinks, and unsafe paths. Original false-PASS evidence and the adversary's interrupted cache-affected control run are preserved privately. The repaired component has zero blockers. This review does not replace the later sequential whole-package preprint adversaries.

The positive verification whitelist binds every current prose/metadata/code/result byte and all nineteen original inputs. The current publication manifest deliberately excludes itself; the independent whitelist includes it. The whitelist and final seal deliberately exclude self-hashes; the actual whitelist SHA256 is in the seal, and the seal's actual SHA256 must be authenticated in independent parent custody. No fabricated circular self-hash or attestation is used. An attacker able to replace all code, data and custody objects is outside this unkeyed integrity boundary. Hash binding authenticates the reviewed prose bytes; analytic truth comes from the separately inspected proof.

No source PDFs, third-party source, corpora, private runtime/venv/cache, raw fixture, or raw execution logs are in the positive delivery set. No source snapshot, git/index/branch, live PR, remote, author counter, or external communication was changed.
