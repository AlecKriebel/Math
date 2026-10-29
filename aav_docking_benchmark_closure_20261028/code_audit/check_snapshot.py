"""Read-only, dependency-free checks of the frozen AAV benchmark snapshot.

Run from this effort folder: python3 code_audit/check_snapshot.py
Writes only code_audit/checks.json; does not import or execute upstream code.
"""
import ast
import hashlib
import json
from collections import Counter
from pathlib import Path

EFFORT = Path(__file__).resolve().parents[1]
ROOT = EFFORT / "snapshot"
TREE = json.loads((ROOT / "TREE.json").read_text())


def blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


inventory = []
for item in TREE["tree"]:
    if item["type"] != "blob":
        continue
    path = ROOT / item["path"]
    inventory.append({
        "path": item["path"], "expected_bytes": item["size"],
        "exists": path.exists(),
        "actual_bytes": path.stat().st_size if path.exists() else None,
        "blob_sha_matches": blob_sha(path.read_bytes()) == item["sha"] if path.exists() else None,
    })

source = (ROOT / "pilot/pilot-script.py").read_text()
syntax = ast.parse(source)
functions = {node.name: node for node in syntax.body if isinstance(node, ast.FunctionDef)}
prepare_text = ast.get_source_segment(source, functions["prepare"])
dock_text = ast.get_source_segment(source, functions["dock"])
raw_required = ["data/raw/7MTZ.cif", "data/raw/7MT0.cif", "data/raw/GAL.cif"]
raw_status = {p: (ROOT / p).exists() for p in raw_required}
blank_structure_status = {
    name: {"upstream_size": next(x["size"] for x in TREE["tree"] if x["path"] == name),
           "local_is_whitespace_only": not (ROOT / name).read_text().strip(),
           "upstream_blob_is_exact_CRLF": next(x["sha"] for x in TREE["tree"] if x["path"] == name) == blob_sha(b"\r\n")}
    for name in ["data/7MTZ.cif", "data/7MT0.cif"]
}

pdbs = {}
for name in ["AAV9-trimmed-gal.pdb", "trimmed-aav9.pdb"]:
    atomlines = [line for line in (ROOT / "pdb-files" / name).read_text().splitlines()
                 if line.startswith(("ATOM  ", "HETATM"))]
    protein = [x for x in atomlines if x.startswith("ATOM  ")]
    hetero = [x for x in atomlines if x.startswith("HETATM")]
    residue_sets = {}
    for line in protein:
        residue_sets.setdefault(line[21], set()).add((line[22:27], line[17:20]))
    pdbs[name] = {
        "protein_atom_count": len(protein),
        "protein_atoms_by_chain": dict(Counter(line[21] for line in protein)),
        "protein_residues_by_chain": {k: len(v) for k, v in residue_sets.items()},
        "hetero_atom_count": len(hetero),
        "hetero_atoms_by_residue": dict(Counter(line[17:20].strip() for line in hetero)),
    }

# A boundary counterexample to the current apo-contact denominator construction.
# Lines 325–332 use the receptor's surviving atom keys to subset the holo universe.
# Removing one native-contact atom can turn 1/2 recovery into a reported 1/1.
true_native_contacts = {("C1", "retained_atom"), ("C1", "missing_apo_atom")}
predicted_contacts = {("C1", "retained_atom")}
surviving_apo_atom_keys = {"retained_atom"}
restricted_native = {x for x in true_native_contacts if x[1] in surviving_apo_atom_keys}
counterexample = {
    "scope": "Synthetic boundary case; not evidence that the missing AAV apo input has this defect",
    "full_holo_reference_recall": len(true_native_contacts & predicted_contacts) / len(true_native_contacts),
    "current_key_restricted_recall": len(restricted_native & predicted_contacts) / len(restricted_native),
    "implication": "Missing native-contact atoms must trigger exclusion/explicit treatment, or denominator changes across receptor states",
}

out = {
    "commit": TREE["sha"],
    "syntax_parses": True,
    "inventory": inventory,
    "required_raw_paths_exist": raw_status,
    "blank_AAV_reference_files": blank_structure_status,
    "prepare_writes_receptor_pdb": "output_structure.write_pdb" in prepare_text,
    "prepare_writes_receptor_pdbqt": "receptor.pdbqt" in prepare_text,
    "dock_requires_receptor_pdbqt": "_receptor.pdbqt" in dock_text,
    "committed_docking_result_files": [x["path"] for x in TREE["tree"] if x["type"] == "blob" and
                                      (x["path"].startswith("results/") or x["path"].endswith(".pdbqt"))],
    "pdb_inventory": pdbs,
    "apo_contact_denominator_boundary": counterexample,
    "limits": ["Upstream docking was not run", "Structure files were not density-validated",
               "No assumption that prepared PDBQT or uncommitted results do not exist elsewhere"],
}
output = EFFORT / "code_audit/checks.json"
output.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({k: v for k, v in out.items() if k != "inventory"}, indent=2))
