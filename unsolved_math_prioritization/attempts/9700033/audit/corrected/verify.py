#!/usr/bin/env python3
"""Strict byte binding and finite diagnostics; not a continuum proof verifier."""
import hashlib
import itertools
import json
import pathlib
import sys
from fractions import Fraction


def require(condition, message):
    if not condition:
        raise ValueError(message)


def mass(a, b, low, high):
    return (b-a)*(1/low-1/high)


def diagnostics():
    result = {"scaling_rectangles": 0, "intensity_tail_sums": 0,
              "last_exit_controls": 0, "negative_math_controls": 0}
    values = [Fraction(1,3), Fraction(1,2), Fraction(1), Fraction(2), Fraction(3)]
    for width, low, height, scale in itertools.product(values, repeat=4):
        a = Fraction(-7, 3)
        b, high = a+width, low+height
        require(mass(a,b,low,high) == mass(scale*a,scale*b,scale*low,scale*high),
                "marked intensity is not scaling invariant")
        result["scaling_rectangles"] += 1
    for r in values:
        for k in range(1, 21):
            total = sum((1/(r*2**i)-1/(r*2**(i+1)) for i in range(k)), Fraction())
            require(total == 1/r-1/(r*2**k), "intensity telescoping failed")
            result["intensity_tail_sums"] += 1
    for n in range(9):
        for middle in itertools.product("AMB", repeat=n):
            word = ("A",)+middle+("B",)
            first_b = word.index("B")
            last_a = max(i for i in range(first_b) if word[i] == "A")
            require(all(x == "M" for x in word[last_a+1:first_b]),
                    "last-exit/first-entry subpath control failed")
            result["last_exit_controls"] += 1
    # Wrong exponent and the first-exit shortcut must actually fail these controls.
    wrong_mass = lambda a,b,low,high: (b-a)*(1/low**2-1/high**2)/2
    require(wrong_mass(Fraction(0),Fraction(1),Fraction(1),Fraction(2)) !=
            wrong_mass(Fraction(0),Fraction(2),Fraction(2),Fraction(4)),
            "wrong-exponent control did not distinguish scaling")
    result["negative_math_controls"] += 1
    word = "AMAMB"
    require("A" in word[1:word.index("B")], "first-exit shortcut control failed")
    result["negative_math_controls"] += 1
    require(2*Fraction(3)/Fraction(2) != 1, "component-count control failed")
    result["negative_math_controls"] += 1
    require(result == {"scaling_rectangles":625,"intensity_tail_sums":100,
                       "last_exit_controls":9841,"negative_math_controls":3},
            "diagnostic coverage mismatch")
    return result


def main():
    root = pathlib.Path(__file__).absolute().parent
    require(not root.is_symlink(), "symlink package root")
    cert_path = root/"CERTIFICATE.json"
    require(not cert_path.is_symlink(), "symlink certificate")
    certificate = json.loads(cert_path.read_text())
    require(certificate["problem_id"] == 9700033, "wrong problem ID")
    require(certificate["result"] == "UNSOLVED_SCOPED_PARTIAL", "wrong disposition")
    entries = certificate["files"]
    require(set(entries) == {"README.md", "RESULT.md", "SOURCE_MANIFEST.json", "verify.py"},
            "wrong expected file set")
    actual = set()
    for p in root.rglob("*"):
        require(not p.is_symlink(), "symlink: "+str(p))
        require(p.is_file(), "unexpected directory or special node: "+str(p))
        actual.add(p.relative_to(root).as_posix())
    require(actual == set(entries)|{"CERTIFICATE.json"}, "unlisted or missing files")
    for name, expected in entries.items():
        raw = (root/name).read_bytes()
        require(len(raw) == expected["bytes"], "size mismatch: "+name)
        require(hashlib.sha256(raw).hexdigest() == expected["sha256"], "hash mismatch: "+name)
    sources = json.loads((root/"SOURCE_MANIFEST.json").read_text())
    require(sources["canonical_pair"]["sha256"] ==
            "21b8f492c3e9bbdc7d788b8dde10d0d0d9ea6b46a947b1bf4f9447507155d8f0",
            "wrong canonical exact-ID binding")
    require(sources["canonical_pair"]["matches_catalog_review_hash"] is True,
            "catalog match missing")
    result = diagnostics()
    print(json.dumps({"status":"PASS", "problem_id":9700033,
                      "files_bound":len(entries), "diagnostics":result,
                      "proof_scope":"finite diagnostics only; not a continuum proof"},
                     sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        print("FAIL: "+str(exc), file=sys.stderr)
        sys.exit(1)
