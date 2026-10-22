# Portable finite verification for PR239 / 30001321

Use Python 3.11 or newer. From this folder, run:

    python3 -E -S -B -P verify.py

The default uses only Python's standard library. It runs eight reviewed checkers and expects **376,020 exact finite assertions**, including 197 controls for hypotheses deliberately outside the theorem.

To add the original symbolic return-series checker, install the optional dependency in your preferred Python environment using requirements-optional.txt, then run:

    python3 -E -S -B -P verify.py --with-sympy

That adds 486 assertions under SymPy 1.14.0, for **376,506** total. The runner installs nothing and makes no network requests. It prints one JSON execution report to standard output and creates no files in this archive.

## What is authenticated and run

Before any checker or optional dependency is executed, verify.py authenticates every listed file against the relative MANIFEST.json by exact length and SHA256. It additionally reconstructs the native Git-blob SHA1 for all 32 preserved submission files. It refuses unlisted members, symlinks, nonregular members, duplicate entries and noncanonical paths. The manifest is an integrity inventory, not a digital signature; an external archive digest or trusted original supplies its authenticity anchor.

The runner copies only each selected checker source into its own temporary directory. This matters because the replica and excluded-boundary checkers write EXACT_RESULTS.json and BOUNDARY_RESULTS.json beside themselves. Those writes remain in temporary directories, which are removed afterward. The frozen archive, submission snapshots and historical receipts are never overwritten.

The selected checkers are:

| Relative source | Assertions |
|---|---:|
| submission/check_turn2.py | 50,324 |
| submission/check_turn3.py | 17,148 |
| submission/independent_review/independent_check.py | 31,888 |
| audits/math_replica_family_01/independent_exact_checks.py | 37,140 |
| audits/math_replica_family_01/excluded_boundary_checks.py | 197 |
| audits/math_martingale_family_01/independent_exact_controls.py | 197,758 |
| audits/math_coalescence_family_01/independent_exact_checks.py | 22,225 |
| audits/reproduction_history_family_01/independent_finite_check.py | 19,340 |
| submission/check_turn1.py, optional SymPy | 486 |

Each actual output must have the reviewed JSON count, status and applicable schema/properties. The runner checks that assertion-family sums equal their totals. It also checks the replica and boundary files written in temporary directories, and the coalescence checker's self-reported source digest. No comparison depends on timestamps, temporary paths or byte-identical newly generated receipts. Failures stop the run.

**Do not execute audits/reproduction_history_family_01/actual_replay_driver.py as a portable runner.** It is an exact historical provenance artifact with original absolute working-directory assumptions. The only portable entry point is verify.py; its explicit checker allowlist excludes that driver.

## Archive and evidential boundaries

- submission/ contains the exact 32-file current PR attempt snapshot, including the original proof/dependency notes and historical review. The preserved original/current PR heads were identical. Its native blob pins were derived from the authenticated source-materialization manifest, 65,348 bytes, SHA256 4ddb9e5c9dc2487b9fb5fd8f993e562517b5efe2b4af2c2ae87c1a5c61feefa4, at HEAD 7f17eef77c52b2d9b2ec3ad0803c016267fa6496.
- audits/ contains only the finite positive payloads and exact original manifest/seal of four fresh review families.
- priority/ contains the nine positively selected priority-review v2 payloads and exact manifest 02/seal 02.
- Original manifests, receipts and status files are retained byte-for-byte as dated history. Some contain original absolute paths. Those paths are documentary text only; verify.py does not follow them. Only the new relative MANIFEST.json supplies runtime file paths.
- No third-party PDFs, downloaded full texts, private research copies, raw API/provider/tracker output, native-operation scripts, credentials or whole-directory exports are included.

Finite assertions corroborate algebra, probability identities, parameter choices, parity, killing and strip sensitivity. They do **not** prove the infinite-time estimates, settle novelty or establish priority. Repeated parameter instances are not independent theorems. The self-contained manuscript supplies the analytic argument.

The frozen turn1/turn2 partial statuses and turn3 pending-review status are historical, as is the later positive review. Manifests do not independently prove the original number of author turns, reviewer identities, absence of pre-freeze assistance or historical PDF access. The new reproduction/history family explicitly read the older review before constructing its distinct checks and was not blinded. These are AI-assisted, unrefereed research artifacts, with no claim of human peer review or certified first discovery.

The package's actual preparation execution receipts are maintained outside this frozen subtree to avoid a self-hashing cycle. A later run creates a fresh JSON report; it should not be mistaken for the historical run.

