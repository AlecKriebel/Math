# Independent code and artifact audit

2026-10-28. Upstream commit: `e9d39e3ef1c58647c2bf9dea7dfc90f823198791`.

The committed repository does not yet supply a reproducible answer to its scientific question. It supplies a carefully qualified proposed protocol, one AAV9 oracle-site docking script, two trimmed structures, and pocket-prediction outputs. No committed docking poses, run manifests, pose metrics, summary results, specificity measurements, or confirmatory cohort were found. This conclusion concerns the public snapshot; it does not assert that additional work does not exist elsewhere.

## Established blockers

1. **The required atomic AAV reference inputs are absent.** `pilot/pilot-script.py:71–72` reads `data/raw/7MTZ.cif` and `data/raw/7MT0.cif`; line 158 reads `data/raw/GAL.cif`. The committed tree instead has `data/<name>.cif`. More seriously, both committed AAV CIF files are exactly the same two bytes, CRLF, independently established by matching their Git blob hash to `b'\r\n'`. Renaming these files cannot repair the missing coordinates. Fetch and verify the actual reference structures, validation information, source versions, and checksums.

2. **Receptor preparation does not reach docking input.** `prepare()` writes `holo_receptor.pdb` and `apo_receptor.pdb` at line 138, and a ligand PDBQT at line 216. `dock()` requires receptor PDBQT files at lines 272–281 and writes a blocked status when they are absent. No receptor PDB-to-PDBQT stage or reproducible external command is present. The receptor protonation/repair/conversion process must be supplied and audited for atom loss and chain/residue mapping.

3. **The advertised invocation does not match the tree.** The script docstring says `python src/pilot.py ...` at line 2; the actual file is `pilot/pilot-script.py`. The computed project root still works for the actual location, but instructions should specify the actual path and full stages. Tests and a one-command replay are absent.

4. **The committed outputs do not measure docking accuracy.** The tree contains fpocket and P2Rank outputs, but no `results/` files or PDBQT pose files. Accordingly there is no public evidence here of Top-1/Top-5 pose recovery, best returned RMSD, score discrimination, apo–holo change, or specificity. Pocket-prediction scores alone cannot establish those quantities.

## Interpretation limits in the present implementation

- `prepare()` uses the deposited ligand to choose receptor chains (lines 87–96), define the box center (81–82), and place the independent ligand conformer at that center (202–204). This is explicitly an oracle-site local diagnostic, as correctly stated at lines 1 and 244. A successful run would establish conditional pose recovery for that case; it cannot establish blind site discovery or biological binding specificity.
- The two trimmed PDBs have materially different content: `AAV9-trimmed-gal.pdb` has three chains R/S/U, each with 518 residues and 4,131 protein atoms, plus three 12-heavy-atom GAL residues; `trimmed-aav9.pdb` has H/W/Y, each with 177 residues and 1,362 atoms, with no ligand. A direct comparison of P2Rank centers against GAL coordinates requires a documented coordinate transform, residue mapping, and assembly provenance. The cropped receptor also needs scrutiny for artificial boundaries. No such mapping or structural validation is committed.
- fpocket/P2Rank invocation, exact software versions, and preparation provenance for the committed output files are missing. P2Rank's first three predictions involve rotated chain pairings with almost identical scores; distinct biological site classes must be established and symmetry copies merged before Top-k evaluation.
- The pilot implements three Vina seeds for a single galactose ligand and two receptor states. These are repeated measurements on one case, not independent biological samples. Galactose has no inter-sugar linkage, so it cannot test carbohydrate linkage torsion handling.

## Metric correctness and boundary cases

The RMSD expression at lines 350–353 is an appropriate atom-name-matched displacement in a fixed receptor frame for a complete, consistently named GAL reference. It correctly refuses an atom-set mismatch, and it does not independently align away the ligand's positional error. This observation is a code inspection, not a completed end-to-end validation.

Before expanding the benchmark, add native-coordinate and deliberately translated/rotated pose controls, atom-order/name permutation tests, apo alignment controls, and documented symmetry-equivalent receptor-site handling. General glycans additionally need graph/stereochemistry-valid equivalences, incomplete-density/core handling, and linkage/ring checks. These functions are not implemented here.

One concrete boundary defect is testable without the absent coordinates: lines 325–332 define the native holo contact universe using only the current receptor's atom keys. If an apo structure lacks one of two native-contact atoms and recovers the other, this reports recall 1/1 instead of 1/2 against the full holo reference. `code_audit/check_snapshot.py` records that counterexample. This is not evidence that the missing AAV apo input has that defect. Resolve it through explicit complete-site eligibility checks or a declared missing-atom policy and fixed reference identities. Apo-only atom keys also produce a lookup failure at line 331.

Additional untested boundaries include insertion codes and alternate atom conformations, which `atomdict()` ignores at lines 40–50; hydrogen-containing references, because reference coordinates filter hydrogens at 24–28 but reference names do not at 223; missing/empty pose sets, which fail at lines 389 and 395; and partial/stale run manifests. Guard these explicitly if they fall within cohort eligibility.

The protocol correctly warns that best returned RMSD diagnoses only the score-filtered returned pool. The code retains no pre-ranking candidate pool, so it cannot prove that a near-native pose was never sampled internally.

## Checkable evidence and closure sequence

Run `python3 code_audit/check_snapshot.py` from this effort folder. It checks source syntax without importing upstream code, verifies blob hashes against `snapshot/TREE.json`, inventories required paths and PDB contents, and constructs the contact-denominator counterexample. Results are in `code_audit/checks.json`. All 23 retrieved source blobs match their upstream Git hashes after the root agent's byte-restoration step; `.gitignore` is deliberately not part of the retrieved source set. No docking, package installation, density analysis, or biological validation was performed in this audit.

The first engineering milestone should be a clean-environment replay that downloads verified inputs, prepares complete receptor neighborhoods and ligand chemistry, executes both receptor states, and passes independent metric controls. Archive all inputs and outputs. Only then freeze and execute a leakage-controlled cohort study and the separate experimental-specificity endpoint.

Checkpoint: code/artifact closure assessment 100% complete within its stated read-only scope; the scientific benchmark remains unexecuted in the inspected public snapshot. Exact biological conclusion remains open.
