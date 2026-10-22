#!/usr/bin/env python3
"""New portable adapters of preserved reviewer controls, with explicit guards.

Original files are unchanged. Adapters remove only nonportable historical custody
in the priority checker and verify the distributed kit separately. They do not
claim full historical input replay or prove the universal surface result.
"""
import argparse
import ast
import contextlib
import io
import json
import shutil
import tempfile
from pathlib import Path
import importlib.util
import sys
sys.dont_write_bytecode = True

_spec = importlib.util.spec_from_file_location("pr1080_kit_verify", Path(__file__).resolve().with_name("verify.py"))
verify = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(verify)

PROGRAMS = {
    "word": ("originals/reviews/positive_words_01/check_word_mechanism.py", "8589beb7e81baeb7c1366fb0a7cc1715362ab82e279fcf0bf2778ee7b18daf45"),
    "surface": ("originals/reviews/surface_orbits_01/sanity_checks.py", "5b94032916d8c987e602144dbead751c9766987288387bb7d6a560fcf0240582"),
    "priority": ("originals/reviews/priority_01/check_prior_corollary.py", "4ec25270464e20ca1d377fddced825039ea620dce218b066d35b0b8486f1081e"),
}


class ExplicitGuards(ast.NodeTransformer):
    def visit_Assert(self, node):
        error = ast.Raise(exc=ast.Call(func=ast.Name(id="RuntimeError", ctx=ast.Load()),
                                      args=[ast.Constant(value="portable reviewer guard at original line " + str(node.lineno))], keywords=[]), cause=None)
        replacement = ast.If(test=ast.UnaryOp(op=ast.Not(), operand=node.test), body=[error], orelse=[])
        return ast.copy_location(replacement, node)


def adapt(kind, source, fault):
    tree = ast.parse(source)
    if kind == "priority":
        funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"]
        verify.require(len(funcs) == 1, "priority main anchor changed")
        main = funcs[0]
        cuts = [i for i, n in enumerate(main.body) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "b" for t in n.targets)]
        verify.require(len(cuts) == 1, "priority custody anchor changed")
        main.body = main.body[:cuts[0]] + [ast.Return(value=ast.Call(func=ast.Name(id="locals", ctx=ast.Load()), args=[], keywords=[]))]
    # Explicit, falsifiable faults in the actual adapted mathematical mechanisms.
    if fault == "word_conjugation" and kind == "word":
        funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "correct_rhs"]
        verify.require(len(funcs) == 1, "word fault anchor changed")
        funcs[0].body = ast.parse("return reduced(tuple(x for block in blocks for x in block))").body
    elif fault == "parity" and kind == "surface":
        funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "pair"]
        verify.require(len(funcs) == 1, "parity fault anchor changed")
        funcs[0].body = ast.parse("return 1").body
    elif fault == "erasing" and kind == "priority":
        main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
        matches = [n for n in main.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "expansions" for t in n.targets)]
        verify.require(len(matches) == 1, "expansion fault anchor changed")
        matches[0].value = ast.parse("{'A': 'A', 'B': 'B', 'C': ''}", mode="eval").body
    tree = ExplicitGuards().visit(tree)
    ast.fix_missing_locations(tree)
    verify.require(not any(isinstance(n, ast.Assert) for n in ast.walk(tree)), "assert left in adapter")
    return tree


def run(fault=None):
    integrity = verify.verify()
    results = {}
    with tempfile.TemporaryDirectory(prefix="pr1080-controls-") as temp:
        scratch = Path(temp)
        for kind, (relative, expected_hash) in PROGRAMS.items():
            original = verify.ROOT / relative
            if expected_hash:
                verify.require(verify.digest(original) == expected_hash, "adapter source hash changed")
            work = scratch / kind
            work.mkdir()
            copied = work / original.name
            shutil.copyfile(original, copied)
            if kind == "surface":
                target = work / "inputs/git"
                target.mkdir(parents=True)
                for p in (verify.ROOT / "originals/submitted").iterdir():
                    shutil.copyfile(p, target / p.name)
            namespace = {"__name__": "portable_reviewer_adapter", "__file__": str(copied)}
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                exec(compile(adapt(kind, original.read_text(), fault), str(copied), "exec"), namespace)
                if kind in ("word", "priority"):
                    local = namespace["main"]()
            if kind == "word":
                r = json.loads((work / "WORD_CONTROL_RESULTS.json").read_text())
                expected = json.loads((original.parent / "WORD_CONTROL_RESULTS.json").read_text())
                verify.require(r == expected, "word control output differs")
                results[kind] = {"insertion_cases": r["insertion_cases"], "result_matches_preserved": True}
            elif kind == "surface":
                r = json.loads((work / "SANITY_RESULTS.json").read_text())
                expected = json.loads((original.parent / "SANITY_RESULTS.json").read_text())
                r.pop("timestamp"); expected.pop("timestamp")
                verify.require(r == expected, "surface control output differs excluding timestamp")
                results[kind] = {"insertion_cases": r["insertion_cases"], "mod2_self_pairing_cases": r["mod2_self_pairing_cases"], "result_matches_preserved_except_timestamp": True}
            else:
                verify.require(local["normal_checks"] == 351 and local["invariant_checks"] == 20412
                               and local["expansion_checks"] == 9841 and local["missing_normality_checks"] == 20,
                               "priority exact counts differ")
                verify.require(local["target_words"] == ["BCA", "BABA"], "priority target fiber differs")
                results[kind] = {"normal_cone_checks": 351, "two_sided_order_checks": 20412,
                                 "nonerasing_atomic_expansion_checks": 9841, "missing_normality_checks": 20,
                                 "target_words": local["target_words"], "historical_52_input_replay": False,
                                 "portable_integrity_replaces_historical_custody": True}
    return {"status": "PASS", "finite_checks_only": True, "guards_survive_python_O": True,
            "kit_integrity": integrity, "controls": results,
            "limitations": "Finite fault controls are not universal proofs; original six-file edition has no executable; omitted historical input replay is not claimed."}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fault", choices=["word_conjugation", "parity", "erasing"])
    a = p.parse_args()
    print(json.dumps(run(a.fault), indent=2))


if __name__ == "__main__":
    main()
