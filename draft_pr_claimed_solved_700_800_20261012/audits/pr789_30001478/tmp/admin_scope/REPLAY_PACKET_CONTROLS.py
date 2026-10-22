#!/usr/bin/env python3
"""Read-only final packet replay; all tampering happens in owned scratch copies.

The unchanged externally pinned checker runs against each copy. No Git, sheet,
publication, credential, source package or original packet mutation occurs.
"""
import argparse, copy, hashlib, json, os, shutil, stat, subprocess, sys, tempfile
from pathlib import Path
OWN = Path(__file__).resolve().parent

def need(v, message):
    if not v: raise RuntimeError(message)

def sha(raw): return hashlib.sha256(raw).hexdigest()

def repin(folder):
    p = folder / "MANIFEST.json"
    m = json.loads(p.read_text())
    for row in m["files"]:
        raw = (folder / row["path"]).read_bytes()
        row.update(bytes=len(raw), sha256=sha(raw))
    p.write_text(json.dumps(m, indent=2) + "\n")
    return sha(p.read_bytes())

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--packet", type=Path, default=OWN / "packet")
    p.add_argument("--expected-manifest-sha256", required=True)
    p.add_argument("--package", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    packet = a.packet.resolve()
    need(packet.is_relative_to(OWN) and a.out.resolve().is_relative_to(OWN), "Owned administrative paths required")
    need(sha((packet / "MANIFEST.json").read_bytes()) == a.expected_manifest_sha256, "Original external manifest pin differs")
    checker = packet / "CHECKS.py"
    original = {p.name: (sha(p.read_bytes()), len(p.read_bytes()), p.lstat().st_nlink,
                         stat.S_ISREG(p.lstat().st_mode), p.is_symlink()) for p in packet.iterdir()}
    scratch = OWN / "scratch/packet_replay"
    scratch.mkdir(parents=True, exist_ok=True)
    runroot = Path(tempfile.mkdtemp(prefix="sealed-packet-", dir=scratch))
    cases = []
    def test(name, change=None, expected=False, optimized=False, source=False, semantic_repin=False, wrong_pin=False):
        folder = runroot / name
        shutil.copytree(packet, folder, copy_function=shutil.copyfile)
        if change: change(folder)
        pin = repin(folder) if semantic_repin else a.expected_manifest_sha256
        if wrong_pin: pin = "0" * 64
        command = [sys.executable, "-I", "-B"]
        if optimized: command.append("-O")
        # Execute the copied checker itself, so the relocation positive is a
        # relocated runnable packet rather than only relocated receipt data.
        command += [str(folder / "CHECKS.py"), "--packet", str(folder), "--expected-manifest-sha256", pin]
        if source:
            need(a.package is not None, "Explicit external source package required for replay")
            command += ["--package", str(a.package.resolve())]
        r = subprocess.run(command, capture_output=True, text=True, timeout=180, cwd="/")
        try: report = json.loads(r.stdout)
        except ValueError: report = {"result": "INVALID_CHECKER_RESPONSE"}
        accepted = r.returncode == 0 and not r.stderr and report.get("result") == "PASS"
        cases.append({"case": name, "expected_acceptance": expected, "accepted": accepted,
                      "control_pass": accepted == expected,
                      "checker_reason": report.get("reason"), "external_source_replayed": source,
                      "semantic_consistency_control_with_new_fixture_manifest": semantic_repin})
    def alter_json(folder, name, edit):
        path = folder / name
        v = json.loads(path.read_text()); edit(v)
        path.write_text(json.dumps(v, indent=2) + "\n")
    test("ordinary_exact_packet", expected=True)
    test("optimized_exact_packet", expected=True, optimized=True)
    if a.package: test("relocated_packet_and_external_source_replay", expected=True, source=True)
    test("wrong_external_manifest_pin", wrong_pin=True)
    test("changed_manifest_bytes", lambda f: (f / "MANIFEST.json").write_bytes((f / "MANIFEST.json").read_bytes() + b"\n"))
    test("changed_authored_leaf", lambda f: (f / "BINDINGS.json").write_bytes((f / "BINDINGS.json").read_bytes() + b"\n"))
    test("missing_authored_leaf", lambda f: (f / "VERDICT.json").unlink())
    test("unexpected_regular_file", lambda f: (f / "EXTRA").write_text("owned fixture"))
    test("unexpected_empty_directory", lambda f: (f / "EMPTY").mkdir())
    test("unexpected_FIFO", lambda f: os.mkfifo(f / "FIFO"))
    def symlink_leaf(folder):
        path = folder / "BINDINGS.json"; raw = path.read_bytes(); path.unlink()
        target = runroot / "symlink-target.json"; target.write_bytes(raw); path.symlink_to(target)
    test("authored_leaf_symlink", symlink_leaf)
    def hardlink_leaf(folder):
        path = folder / "BINDINGS.json"
        os.link(path, runroot / "hardlink-counterpart.json")
    test("authored_leaf_hardlink", hardlink_leaf)
    def symlink_root(folder):
        actual = folder.with_name(folder.name + "-actual")
        folder.rename(actual); folder.symlink_to(actual, target_is_directory=True)
    test("packet_root_symlink", symlink_root)
    test("three_review_readiness_even_with_resealed_fixture", lambda f: alter_json(f, "READINESS_AT_PUBLICATION.json", lambda v: v.update(actual_whole_preprint_rounds=3)), semantic_repin=True)
    test("public_payload_hash_drift_even_with_resealed_fixture", lambda f: alter_json(f, "PUBLIC_VERIFICATION.json", lambda v: v["public_files"][0].update(sha256="0" * 64)), semantic_repin=True)
    test("tracker_extra_cell_even_with_resealed_fixture", lambda f: alter_json(f, "TRACKER_VERIFICATION.json", lambda v: v["cells"].append(copy.deepcopy(v["cells"][0]))), semantic_repin=True)
    test("merge_parent_drift_even_with_resealed_fixture", lambda f: alter_json(f, "MERGE_SCOPE.json", lambda v: v["actual_merge"]["parents"].__setitem__(0, "0" * 40)), semantic_repin=True)
    test("missing_integration_second_parent_even_with_resealed_fixture", lambda f: alter_json(f, "MERGE_SCOPE.json", lambda v: v["integration"]["parents"].pop()), semantic_repin=True)
    test("other_path_not_preserved_even_with_resealed_fixture", lambda f: alter_json(f, "MERGE_SCOPE.json", lambda v: v["actual_merge"].update(every_other_path_preserved_from_premerge_main=False)), semantic_repin=True)
    need(sha((packet / "MANIFEST.json").read_bytes()) == a.expected_manifest_sha256, "Original packet was unexpectedly changed")
    after = {p.name: (sha(p.read_bytes()), len(p.read_bytes()), p.lstat().st_nlink,
                      stat.S_ISREG(p.lstat().st_mode), p.is_symlink()) for p in packet.iterdir()}
    need(after == original, "Original packet leaf bytes or link types were unexpectedly changed")
    result = {"result": "PASS_PACKET_REPLAY_AND_TAMPER_CONTROLS" if all(c["control_pass"] for c in cases) else "FAIL",
              "checker_sha256": sha(checker.read_bytes()), "externally_pinned_manifest_sha256": a.expected_manifest_sha256,
              "cases": cases, "controls": len(cases), "all_original_packet_files_untouched": True,
              "credentials_read": False, "network_or_remote_mutations": False,
              "tamper_fixtures_outside_authored_packet": True}
    a.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["result"] == "FAIL": raise SystemExit(1)

if __name__ == "__main__": main()
