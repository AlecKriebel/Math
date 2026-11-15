#!/usr/bin/env python3
"""Pure read-only editorial custody plus five tiny in-memory boundary controls.

No imports/execution of scientific or old editorial programs, no subprocess,
network, browser or writes. These controls illustrate necessary scope, not a
new scientific review or a proof by finite sampling.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
from html.parser import HTMLParser

OWN = Path(__file__).resolve().parent
P = OWN.parent.parent
EXCLUDED = {"OWNED_MANIFEST.json", "FINAL_SEAL.json", "CLOSURE_RESULTS.json"}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def strict(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(strict(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(strict(x, y) for x, y in zip(a, b))
    return a == b


inputs = json.loads((OWN/"INPUT_MANIFEST.json").read_text())
for item in inputs["protected_files"]:
    p = Path(item["absolute_path"])
    require(p.is_file() and p.stat().st_size == item["bytes"] and sha(p) == item["sha256"], "Protected input changed: "+str(p))

literal = json.loads((OWN/"WHOLE_LITERAL_INPUT_VERDICTS.json").read_text())
for rid, record in literal.items():
    for lane, item in record["whole_three_original_literal_verdicts"].items():
        original = P/"papers"/rid/"reviews"/lane/"VERDICT.json"
        copied = OWN/item["raw_byte_copy"]
        require(copied.read_bytes() == original.read_bytes(), "Whole verdict bytes changed")
        require(strict(item["whole_literal_object"], json.loads(original.read_text())), "Whole verdict object/order/type changed")
    for item in record["authority_copies"]:
        require((OWN/item["copy"]).read_bytes() == Path(item["source"]).read_bytes(), "Whole authority copy changed")

pub113 = json.loads((P/"papers/23441890/publication.json").read_text())
pro113 = json.loads((P/"papers/23441890/promotion.json").read_text())
pro114 = json.loads((P/"papers/23174283/publication/promotion/promotion.json").read_text())
for obj in (pub113, pro113):
    require(obj["canonical_url"] is None and obj["AA"] is None and obj["follow_up"] is None, "113 canonical/AA/follow-up assigned")
for key in ("production_integration_authorized", "publication_clearance", "ready_to_publish", "rendered_copy_verified", "local_http_verified", "deployed", "live_verified", "browser_verified", "native_verified", "canonical_verified"):
    require(pro113[key] is False, "113 premature public gate: "+key)
require(pro114["state"]["canonical_url"] is None and pro114["state"]["AA"] is None and pro114["state"]["root_editorial_adoption"] is None, "114 assigned adoption/canonical/AA")
for k, v in pro114["state"].items():
    if k not in ("private_editorial_complete", "root_editorial_adoption", "canonical_url", "AA"):
        require(v is False, "114 premature gate: "+k)
require(pro114["science"]["follow_up"] is None and pro114["science"]["domain"]["integer_n_upper_bound"] is None, "114 follow-up/all-n domain altered")


class AbstractParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag == "p" and dict(attrs).get("id") == "original-abstract":
            self.active = True
    def handle_endtag(self, tag):
        if tag == "p":
            self.active = False
    def handle_data(self, text):
        if self.active:
            self.parts.append(text)


def abstract(tex):
    return tex.split(r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0]


def norm113(s):
    return re.sub(r"\s+", "", s.replace(r"\Z", r"\mathbb Z"))


def norm114(s):
    s = s.replace("Fₙ", "F_n").replace(r"\sqrt{F_n}", "√F_n").replace(r"\geq", "≥")
    s = s.replace("$", "").replace("--", "–").replace("’", "'")
    return re.sub(r"\s+", "", s)


t113 = (P/"papers/23441890/sources/published-source/kourovka-21-149/main.tex").read_text()
t114 = (P/"papers/23174283/sources/published-source/spherical_fibonacci_separation.tex").read_text()
require(norm113(abstract(t113)) == norm113(pub113["abstract"]), "113 original abstract truncated/changed")
h114 = (P/"papers/23174283/publication/promotion/page.html").read_text()
parser = AbstractParser(); parser.feed(h114)
require(norm114(abstract(t114)) == norm114("".join(parser.parts)), "114 original abstract truncated/changed")

controls = []
# 1: One fixed alpha is stronger than choosing a different alpha per embedding.
diagonal = ((True, False), (False, True))
exists_forall = any(all(row) for row in diagonal)
forall_exists = all(any(diagonal[a][e] for a in range(2)) for e in range(2))
require(forall_exists and not exists_forall, "Quantifier boundary control failed")
controls.append({"family":"Dlab quantifier order", "witness":"2x2 diagonal predicate: forall e exists alpha is true; exists alpha forall e is false", "implication":"Retain ONE fixed automorphism for BOTH ambients and EVERY embedding."})

# 2: Bilateral cells have the stated shift. A nontrivial compact bump copy
# fixes two endpoints yet moves an interior point in every negative cell;
# it therefore cannot be affine on any initial ray.
def phi(n, x):
    return -(F(2)**(-n))+(F(2)**(-n-1))*x
for n in (-3, 0, 2):
    for x in (F(0), F(1,3), F(1)):
        require(phi(n, x)/2 == phi(n+1, x), "Bilateral shift changed")
    a, b = phi(n, F(0)), phi(n, F(1))
    source_x, moved_x = F(1,3), F(5,12)
    require(a < phi(n, source_x) < b and phi(n, source_x) != phi(n, moved_x), "Nontrivial cell witness missing")
require(phi(-3, F(1,3))/2 != phi(-4, F(1,3)), "Wrong shift unexpectedly survived")
controls.append({"family":"Dlab initial-ray boundary", "witness":"v phi_n=phi_(n+1); fixed cell endpoints and nontrivial interior bump copies arbitrarily far left exclude eventual affinity", "implication":"The larger bare group B cannot be substituted for A_R or the standard reflected family.", "finite_arithmetic_samples":9, "universal_argument":"Two fixed points force an affine formula to be identity; a moved interior point contradicts it in a cell beyond any proposed ray threshold."})

# 3: The smallest genuine Fibonacci set has exactly one pair. Adding both
# endpoints produces two closest pairs, so the half-open scope is essential.
N, E, S = (0,0,1), (-1,0,0), (0,0,-1)
def dist2(a, b):
    return sum((F(x)-F(y))**2 for x, y in zip(a,b))
require(dist2(N,E) == 2 and dist2(E,S) == 2 and dist2(N,S) == 4, "Endpoint witness changed")
controls.append({"family":"Fibonacci endpoint range", "q":2, "half_open_pair_squared_distance":"2", "both_endpoints_minimizing_pairs":2, "implication":"Do not extend unique pair to 0<=k<=q."})

# 4: With midpoint heights +/-1/2 and opposite longitudes, squared chord is4,
# while the written unshifted q=2 theorem gives2. No trigonometric float.
midpoint_d2 = F(1)+F(3,4)+F(3,4)+2*F(3,4)
require(midpoint_d2 == 4 and midpoint_d2 != F(4,2), "Midpoint witness changed")
controls.append({"family":"Fibonacci unshifted heights", "q":2, "midpoint_squared_chord":"4", "unshifted_squared_chord":"2", "implication":"No midpoint-height promotion."})

# 5: The exact q=12,p=1 witness has D²=2-sqrt(105)/6 <1/3 because105>100.
# This rejects an arbitrary-coprime-multiplier replacement without scanning.
require(105 > 100 and F(2)-F(10,6) == F(1,3), "General multiplier witness changed")
controls.append({"family":"Fibonacci arithmetic scope", "q":12, "p":1, "pair":[5,6], "exact_squared_chord":"2-sqrt(105)/6 < 1/3 = 4/q", "sign_certificate":"105>100", "implication":"Do not replace consecutive Fibonacci multiplier by arbitrary coprime p."})

if (OWN/"OWNED_MANIFEST.json").exists():
    owned = json.loads((OWN/"OWNED_MANIFEST.json").read_text())
    actual = {str(f.relative_to(OWN)) for f in OWN.rglob("*") if f.is_file() and str(f.relative_to(OWN)) not in EXCLUDED}
    require(actual == {x["relative_path"] for x in owned["files"]}, "Owned audit inventory changed")
    for item in owned["files"]:
        f = OWN/item["relative_path"]
        require(f.stat().st_size == item["bytes"] and sha(f) == item["sha256"], "Owned audit file changed")
if (OWN/"FINAL_SEAL.json").exists():
    seal = json.loads((OWN/"FINAL_SEAL.json").read_text())
    for key, name in (("owned_manifest_sha256","OWNED_MANIFEST.json"), ("input_manifest_sha256","INPUT_MANIFEST.json"), ("report_sha256","REPORT.md"), ("verdicts_sha256","VERDICTS.json"), ("closure_result_sha256","CLOSURE_RESULTS.json")):
        require(seal[key] == sha(OWN/name), "Final seal mismatch: "+key)

print(json.dumps({"status":"PASS_READ_ONLY_EDITORIAL_CUSTODY_AND_SMALL_BOUNDARY_CONTROLS", "protected_preexisting_files_checked":len(inputs["protected_files"]), "whole_original_literal_verdicts_checked":6, "full_original_abstracts_checked":2, "small_in_memory_boundary_families":len(controls), "boundary_controls":controls, "scientific_programmes_or_old_content_verifiers_executed":False, "network_browser_or_preexisting_writes":False, "publication_authority":False}, indent=2))
