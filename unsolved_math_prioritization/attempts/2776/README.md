# KP-2.28 / 2776: type-preserving RAAG embedding partial results

**Unsolved after five substantive routes (5/5). No universal solution or novelty claim.**

This source-free draft preserves the seven-file original edition and sixteen-file independent audit byte for byte. The `corrected/` slice applies the required verifier correction and the optional scope clarification as separate, pinned files. Read `ACCEPTANCE.md`, then `corrected/RESEARCH_REPORT.md` and `audit/AUDIT_REPORT.md`.

## Scope

The authored results include an all-word Schottky construction for free groups, a graph/support criterion and a local C5 support-model obstruction, a cycle-cover diagonal obstruction, a P4 loxodromic element killed by all free-target detectors, and persistence of reducibility under the stated unbranched covers and restrictions of the same representation. These do not establish the general type-preserving embedding conjecture and do not rule out every embedding.

Runnels' connected-support convention counts extra boundary-twist annuli as separate components. The support implication used is filling of the whole ambient surface. Finite-index loxodromicity remains relative to the original ambient RAAG; no new RAAG presentation or different representation of the subgroup is covered.

## Important verifier correction

The original verifier has 15 Python asserts. All are stripped by optimization: five corrupt specimens falsely pass under each of `-O` and `-OO` (10 false passes). Its unmodified CLI also fails in all three genuinely read-only runs because it always writes a neighboring results file. The preserved original README describes that historical behavior; it is not the supported reproduction instruction for this publication.

The corrected verifier has no asserts, uses always-active conditions, and writes the complete JSON to stdout by default. Its output is byte-identical to the original frozen results in normal, `-O`, and `-OO` runs. It rejects all 15 mutation/mode combinations. A separate checker reproduces its own exact frozen output. Finite computation corroborates written proofs; it does not certify all unbounded claims.

## Trust and reproduction

Use Python 3 on a POSIX system as actual UID/EUID 1000. Obtain the `BOOTSTRAP.py` SHA-256 from a separately trusted review/PR record and authenticate the bootstrap bytes **before execution**. A hash stored only inside the downloaded packet is not an external trust anchor. Run the authenticated bootstrap with `python3 -I -S -B /trusted/path/BOOTSTRAP.py /path/to/packet`; repeat with `-O` and `-OO` before the script path. It authenticates the manifest and wrapper before the wrapper runs any payload.

The wrapper enforces an exact recursive allowlist, rejects symlinks and special files, strictly parses JSON (including duplicate keys, nonfinite/overflow values and type distinctions), checks immutable original/audit/corrected pins, applies both patches with exact context in memory, and replays corrected/independent checks and the full execution audit in genuinely read-only temporary specimens. Every run probes actual write denial and checks evidence remains unchanged.

The execution-audit comparison is exact after explicitly validating and normalizing only the Python runtime string, temporary pathname in the original CLI's PermissionError, and hash of the external-output acknowledgment containing that temporary path. Both mathematical output files remain exact frozen byte comparisons. The external-output audit independently checks file bytes. All other receipt fields, keys, types, list order and values must agree.

`mutation_tests.py --root /path/to/packet --bootstrap-sha256 EXTERNAL_PIN` exercises integrity/schema corruption, attempted self-consistent repinning, relocation, and hostile import environments. Invoke the harness itself with `-I -S -B` and normal/`-O`/`-OO` modes after authenticating its manifest-bound bytes.

## Sources and exclusions

Public citations and source hash/retrieval/inspection metadata are retained. Original and audit references to inspection, retrieval and nonpublication are historical records. This fresh source-free replay reports source-PDF hash/re-extraction work as `NOT_RUN`; six PDF identities and five extraction matches remain historical audit evidence. The Runnels thesis proof was not inspected and Oh–Park was screened, not proof-audited. No source PDFs, images, extracts, datasets, private material, or coordination files are included.
