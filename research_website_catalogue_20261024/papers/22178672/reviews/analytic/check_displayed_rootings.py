"""Check only the two rootings printed on article page 30; seek no replacements.

Independent standard-library calculation from the literal arc lists, with
reticulation roles inferred from indegree and compared with the printed roles.
"""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import datetime

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PDF = ROOT / "sources/K3P_Level2_Identifiability_Article_v1.0.0.pdf"
SOURCE = ROOT / "sources/published-source/K3P_Level2_Article_Source_v1.0.0/k3p_level2_article_source/sections/13_sharpness.tex"

NETWORKS = {
    "W": {
        "arcs": [("r","S"),("r","L0"),("S","U"),("S","V"),
                 ("U","X"),("V","Z"),("Z","X"),("U","V"),
                 ("Z","L1"),("X","L2")],
        "printed_reticulations": ["V","X"],
    },
    "Wprime": {
        "arcs": [("r","S"),("r","L0"),("S","U"),("S","X0"),
                 ("V","X0"),("U","X1"),("V","X1"),("U","V"),
                 ("X0","L1"),("X1","L2")],
        "printed_reticulations": ["X0","X1"],
    },
}

results = {}
for name, spec in NETWORKS.items():
    children, parents = defaultdict(list), defaultdict(list)
    for a,b in spec["arcs"]:
        children[a].append(b)
        parents[b].append(a)
    nodes = set(children) | set(parents)
    retics = {v for v in nodes if len(parents[v]) == 2}
    if retics != set(spec["printed_reticulations"]):
        raise RuntimeError("Printed reticulation list differs from literal indegrees")
    bad = [v for v in sorted(nodes) if children[v]
           and all(child in retics for child in children[v])]
    results[name] = {
        **spec,
        "inferred_reticulations": sorted(retics),
        "tree_child": not bad,
        "violations": [{"vertex":v,"children":children[v],
                        "child_indegrees":{c:len(parents[c]) for c in children[v]}}
                       for v in bad],
    }

if results["W"]["violations"][0]["vertex"] != "U":
    raise RuntimeError("Unexpected W result")
if results["Wprime"]["violations"][0]["vertex"] != "V":
    raise RuntimeError("Unexpected Wprime result")

payload = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "scope": "Only the displayed rootings; no search for alternative rootings",
    "definition_page":5,"arc_lists_page":30,"erroneous_witness_statement_page":31,
    "article_sha256": hashlib.sha256(PDF.read_bytes()).hexdigest(),
    "sharpness_source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "results": results,
    "finding": "Both displayed rooted presentations are not tree-child",
    "does_not_show": "Neither failure of weak tree-childness of their semi-directed graphs nor falsity of the main theorem is inferred",
}
(OUT/"displayed_rooting_defect.json").write_text(json.dumps(payload,indent=2)+"\n")
print(json.dumps(payload,indent=2))
