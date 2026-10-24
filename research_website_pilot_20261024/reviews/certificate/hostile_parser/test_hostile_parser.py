#!/usr/bin/env python3
"""Adversarial tests of an unchanged local copy of the deposited checker.

Run: python3 -I -S -B test_hostile_parser.py
No network, git, or writes outside this review directory. Tests use the complete
genuine certificate, never substitute a reduced graph or mock the checker.
"""
from pathlib import Path
import copy
from datetime import datetime, timezone
import gzip
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2] / "sources" / "published-release"
CHECKER_HASH = "f329371d046d69e94130a2326320f050d740d281ba1387bccbf050d800468ed1"
CERT_HASH = "6573c55f2998f4576a050a0757ca74f1cae9cadfa96ec61c69b181c530f79c4f"
started = datetime.now(timezone.utc).isoformat()
started_monotonic = time.monotonic()
checker = (HERE / "verify_currents.py").read_bytes()
raw = (HERE / "square_flow_certificate.json.gz").read_bytes()
assert hashlib.sha256(checker).hexdigest() == CHECKER_HASH
assert hashlib.sha256(raw).hexdigest() == CERT_HASH
assert checker == (SOURCE / "verify_currents.py").read_bytes()
assert raw == (SOURCE / "square_flow_certificate.json.gz").read_bytes()
plain = gzip.decompress(raw)
genuine = json.loads(plain)
spec = importlib.util.spec_from_file_location("deposited_checker", HERE / "verify_currents.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
records = []


def run_case(name, entry, expected, call, note=""):
    began = time.monotonic()
    try:
        value = call()
        actual = "ACCEPT"
        detail = value.get("status", repr(value)) if isinstance(value, dict) else repr(value)
    except Exception as exc:
        actual = "REJECT"
        detail = type(exc).__name__ + ": " + str(exc)
    records.append({"name": name, "entry": entry, "expected": expected,
                    "actual": actual, "test_pass": actual == expected,
                    "detail": detail, "note": note,
                    "seconds": round(time.monotonic() - began, 4)})


def changed(name, mutate, expected="REJECT", note=""):
    data = copy.deepcopy(genuine)
    mutate(data)
    run_case(name, "check(data)", expected, lambda: module.check(data), note)


run_case("baseline exact main", "main()", "ACCEPT", module.main)
run_case("baseline direct check", "check(data)", "ACCEPT", lambda: module.check(genuine))

# Every key used by the mathematical check is required. KeyError/TypeError count
# as rejection, but are recorded separately from deliberate RuntimeError guards.
for key in genuine:
    changed("missing key " + key, lambda d, k=key: d.pop(k),
            "ACCEPT" if key == "construction" else "REJECT",
            "Construction text is unused metadata." if key == "construction" else "")
for invalid in (None, [], 0, True, "certificate"):
    run_case("top level " + repr(invalid), "check(data)", "REJECT",
             lambda d=invalid: module.check(d))

for key, valid in (("q", 2), ("radius", 10), ("denominator", module.D),
                   ("vertices", 3070), ("total_energy_numerator", module.ENERGY),
                   ("total_energy_denominator", module.D**2)):
    for label, value in (("bool", True), ("float", float(valid)),
                         ("string", str(valid)), ("zero", 0),
                         ("negative", -valid), ("plus one", valid + 1),
                         ("null", None), ("nan", float("nan")),
                         ("infinity", float("inf"))):
        accepted = key == "vertices" and label == "float"
        changed(key + " " + label, lambda d, k=key, v=value: d.__setitem__(k, v),
                "ACCEPT" if accepted else "REJECT",
                "3070.0 compares equal to 3070; the graph size is independently fixed." if accepted else "")

changed("one current plus one", lambda d: d["flows"][0].__setitem__(0, d["flows"][0][0] + 1))
changed("last current plus one", lambda d: d["flows"][-1].__setitem__(-1, d["flows"][-1][-1] + 1))
changed("boolean current", lambda d: d["flows"][0].__setitem__(0, True))
changed("float current equal numerical value", lambda d: d["flows"][0].__setitem__(0, float(d["flows"][0][0])))
changed("float zero current", lambda d: d["flows"][0].__setitem__(d["flows"][0].index(0), 0.0))
changed("null current", lambda d: d["flows"][0].__setitem__(0, None))
changed("string current", lambda d: d["flows"][0].__setitem__(0, str(d["flows"][0][0])))
changed("current omitted", lambda d: d["flows"][0].pop())
changed("current added", lambda d: d["flows"][0].append(0))
changed("one row omitted", lambda d: d["flows"].pop())
changed("one row added", lambda d: d["flows"].append(d["flows"][0].copy()))
changed("source rows exchanged", lambda d: d["flows"].__setitem__(slice(0, 2), d["flows"][:2][::-1]))
changed("source row duplicated", lambda d: d["flows"].__setitem__(1, d["flows"][0].copy()))
changed("all flow signs reversed", lambda d: d.__setitem__("flows", [[-v for v in r] for r in d["flows"]]))
changed("all zero flows", lambda d: d.__setitem__("flows", [[0] * len(r) for r in d["flows"]]))
changed("flows null", lambda d: d.__setitem__("flows", None))
changed("row null", lambda d: d["flows"].__setitem__(0, None))
changed("flows object", lambda d: d.__setitem__("flows", {str(i): r for i, r in enumerate(d["flows"])}))

def corrupt_with_energies(d):
    d["flows"][0][0] += 1
    d["energy_numerators"][0] = sum(x*x for x in d["flows"][0])
    d["total_energy_numerator"] = sum(d["energy_numerators"])

changed("current changed with energies recomputed", corrupt_with_energies)

def circulation_with_energies(d):
    index = {tuple(e): k for k, e in enumerate(d["edge_order"])}
    # 0,1,2 form a triangle in the genuine square graph. Add one integer
    # circulation, preserving divergence exactly, then recompute both energies.
    d["flows"][0][index[0, 1]] += 1
    d["flows"][0][index[1, 2]] += 1
    d["flows"][0][index[0, 2]] -= 1
    d["energy_numerators"][0] = sum(x*x for x in d["flows"][0])
    d["total_energy_numerator"] = sum(d["energy_numerators"])

changed("valid divergence changed circulation and energies", circulation_with_energies,
        note="Feasible alternate flow is rejected by pinned total energy; direct check is certificate-specific.")

changed("edge deleted", lambda d: d["edge_order"].pop())
changed("edge added", lambda d: d["edge_order"].append([0, 3069]))
changed("edge order exchanged", lambda d: d["edge_order"].__setitem__(slice(0, 2), d["edge_order"][:2][::-1]))
changed("edge orientation reversed", lambda d: d["edge_order"][0].reverse())
changed("duplicate edge", lambda d: d["edge_order"].__setitem__(1, d["edge_order"][0].copy()))
changed("edge loop", lambda d: d["edge_order"].__setitem__(0, [0, 0]))
changed("edge outside graph", lambda d: d["edge_order"][0].__setitem__(1, 3070))
changed("edge endpoint float", lambda d: d["edge_order"][0].__setitem__(0, 0.0))
changed("edge endpoint bool", lambda d: d["edge_order"][0].__setitem__(1, True))
changed("edge extra endpoint", lambda d: d["edge_order"][0].append(2))
changed("edge_order null", lambda d: d.__setitem__("edge_order", None))

def coordinated_edge_swap(d):
    d["edge_order"][0], d["edge_order"][1] = d["edge_order"][1], d["edge_order"][0]
    for row in d["flows"]:
        row[0], row[1] = row[1], row[0]

changed("coordinated edge and current reorder", coordinated_edge_swap)
changed("root neighbor removed", lambda d: d["root_neighbors"].pop())
changed("root neighbor added", lambda d: d["root_neighbors"].append(3070))
changed("root neighbor order exchanged", lambda d: d["root_neighbors"].__setitem__(slice(0, 2), d["root_neighbors"][:2][::-1]))
changed("root neighbor duplicated", lambda d: d["root_neighbors"].__setitem__(1, 1))
changed("root neighbor bool", lambda d: d["root_neighbors"].__setitem__(0, True))
changed("root neighbor float", lambda d: d["root_neighbors"].__setitem__(0, 1.0))
changed("root neighbor zero", lambda d: d["root_neighbors"].__setitem__(0, 0))
changed("energy one changed", lambda d: d["energy_numerators"].__setitem__(0, d["energy_numerators"][0] + 1))
changed("energy float", lambda d: d["energy_numerators"].__setitem__(0, float(d["energy_numerators"][0])))
changed("energy boolean", lambda d: d["energy_numerators"].__setitem__(0, True))
changed("energy removed", lambda d: d["energy_numerators"].pop())
changed("energy added", lambda d: d["energy_numerators"].append(0))
changed("energies null", lambda d: d.__setitem__("energy_numerators", None))
changed("unknown mathematical-looking metadata", lambda d: d.update({"claimed_bound": -100, "source": 0}),
        "ACCEPT", "Unrecognized metadata is ignored and never returned as a verified fact.")

# Actual JSON parser semantics, including duplicate keys, NaN, and syntax errors.
json_text = plain.decode("utf-8")
assert json_text.startswith("{") and json_text.endswith("}")
json_cases = [
    ("duplicate q wrong then genuine", '{"q":3,' + json_text[1:], "ACCEPT"),
    ("duplicate q genuine then wrong", json_text[:-1] + ',"q":3}', "REJECT"),
    ("duplicate flows empty then genuine", '{"flows":[],' + json_text[1:], "ACCEPT"),
    ("duplicate flows genuine then empty", json_text[:-1] + ',"flows":[]}', "REJECT"),
    ("duplicate energy wrong then genuine", '{"total_energy_numerator":0,' + json_text[1:], "ACCEPT"),
    ("duplicate energy genuine then wrong", json_text[:-1] + ',"total_energy_numerator":0}', "REJECT"),
    ("duplicate equal q", '{"q":2,' + json_text[1:], "ACCEPT"),
    ("vertices exponent numeral", json_text.replace('"vertices":3070', '"vertices":3.07e3'), "ACCEPT"),
    ("unused metadata NaN", json_text[:-1] + ',"ignored":NaN}', "ACCEPT"),
    ("trailing nonwhitespace", json_text + "x", "REJECT"),
    ("missing closing brace", json_text[:-1], "REJECT"),
    ("trailing comma", json_text[:-1] + ",}", "REJECT"),
]
for name, text, expectation in json_cases:
    if name == "vertices exponent numeral":
        assert text != json_text, "expected compact field token must be present"
    run_case(name, "json.loads + check(data)", expectation,
             lambda s=text: module.check(json.loads(s)),
             "Standard json.loads resolves duplicate keys to their last value; validation applies to that resolved object."
             if name.startswith("duplicate") else "")

# The public entry point is tested by subprocess with the unchanged checker and
# altered sibling certificates. All edits occur in a temporary child here.
main_variants = [
    ("same JSON recompressed", gzip.compress(plain, mtime=0)),
    ("truncated gzip", raw[:-1]),
    ("gzip appended junk", raw + b"junk"),
    ("gzip appended empty member", raw + gzip.compress(b"", mtime=0)),
    ("non gzip bytes", b"not a certificate"),
    ("empty file", b""),
]
for name, text, _ in json_cases:
    main_variants.append((name, gzip.compress(text.encode(), mtime=0)))
damaged = bytearray(raw)
damaged[len(damaged)//2] ^= 1
main_variants.append(("gzip bit changed", bytes(damaged)))
with tempfile.TemporaryDirectory(prefix="main-tests-", dir=HERE) as temp:
    temp = Path(temp)
    (temp / "verify_currents.py").write_bytes(checker)
    def check_main(contents, optimize=False):
        (temp / "square_flow_certificate.json.gz").write_bytes(contents)
        cmd = [sys.executable, "-I", "-S", "-B"]
        if optimize:
            cmd.append("-O")
        cmd.append(str(temp / "verify_currents.py"))
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode:
            message = result.stderr.splitlines()[-1] if result.stderr else "empty stderr"
            raise RuntimeError(f"subprocess exit {result.returncode}: {message}")
        return json.loads(result.stdout)
    run_case("baseline subprocess", "unchanged main subprocess", "ACCEPT", lambda: check_main(raw))
    run_case("baseline optimized subprocess", "unchanged main subprocess -O", "ACCEPT", lambda: check_main(raw, True))
    for name, contents in main_variants:
        assert contents != raw
        run_case(name, "unchanged main subprocess", "REJECT", lambda c=contents: check_main(c),
                 "Must fail exact compressed-certificate SHA256 before JSON parsing.")
    run_case("mutated optimized subprocess", "unchanged main subprocess -O", "REJECT",
             lambda: check_main(main_variants[0][1], True))

# The helper has a narrower contract. check() supplies its trusted graph, source,
# and default D; these tests make misuse explicit without conflating entry points.
n, _, _, edges = module.finite_graph(10)
for name, source in (("wrong source", 2), ("source zero", 0), ("source out of range", n),
                     ("source bool", True), ("source float", 1.0), ("source negative", -1)):
    run_case(name, "inspect_flow helper", "REJECT",
             lambda s=source: module.inspect_flow(genuine["flows"][0], edges, n, s))
run_case("float denominator equal D", "inspect_flow helper", "ACCEPT",
         lambda: module.inspect_flow(genuine["flows"][0], edges, n, 1, float(module.D)),
         "Helper does not validate denominator type. check() always supplies default integer D.")
run_case("zero flow zero denominator", "inspect_flow helper", "ACCEPT",
         lambda: module.inspect_flow([0] * len(edges), edges, n, 1, 0),
         "Helper permits zero denominator; the certificate check rejects it before helper use.")
run_case("zero flow boolean denominator", "inspect_flow helper", "ACCEPT",
         lambda: module.inspect_flow([0] * len(edges), edges, n, 1, False),
         "Helper permits False denominator; the certificate check rejects it before helper use.")

# Confirm source and copied originals still match the initial immutable inputs.
assert checker == (HERE / "verify_currents.py").read_bytes() == (SOURCE / "verify_currents.py").read_bytes()
assert raw == (HERE / "square_flow_certificate.json.gz").read_bytes() == (SOURCE / "square_flow_certificate.json.gz").read_bytes()
summary = {"started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
           "elapsed_seconds": round(time.monotonic() - started_monotonic, 3),
           "python": sys.version, "checker_sha256": CHECKER_HASH,
           "certificate_sha256": CERT_HASH, "completion_percent": 100,
           "test_count": len(records), "test_pass_count": sum(r["test_pass"] for r in records),
           "test_fail_count": sum(not r["test_pass"] for r in records),
           "observed_accept_count": sum(r["actual"] == "ACCEPT" for r in records),
           "observed_reject_count": sum(r["actual"] == "REJECT" for r in records),
           "status": "PASS" if all(r["test_pass"] for r in records) else "HOLD",
           "scope": "Pinned checker plus direct JSON/check and helper misuse tests; finite input validation only.",
           "records": records}
(HERE / "test_results.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
print(json.dumps({k: v for k, v in summary.items() if k != "records"}, indent=2))
if summary["test_fail_count"]:
    for record in records:
        if not record["test_pass"]:
            print(json.dumps(record))
    raise SystemExit(1)
