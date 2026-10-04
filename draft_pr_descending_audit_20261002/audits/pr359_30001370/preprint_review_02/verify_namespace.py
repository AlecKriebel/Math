"""Read-only inventory/provenance verifier. No mathematical programs or writes."""
import argparse, hashlib, json, pathlib

N = pathlib.Path(__file__).resolve().parent
GENERATED = {"PUBLIC_MANIFEST.json","PRIVATE_MANIFEST.json","CLOSURE.json"}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pairs(items):
    result = {}
    for key,value in items:
        assert key not in result, ("duplicate JSON key",key)
        result[key] = value
    return result

def load(path):
    return json.loads(path.read_text(),object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def safe(name):
    p = pathlib.PurePosixPath(name)
    assert name not in ("", ".") and not p.is_absolute()
    assert ".." not in p.parts and str(p) == name
    return name

def check(record,relative=False):
    path = N/safe(record["path"]) if relative else pathlib.Path(record["path"])
    assert not path.is_symlink() and path.is_file(), str(path)
    data = path.read_bytes()
    assert len(data) == record["bytes"] and sha(data) == record["sha256"], str(path)
    return data

def tree():
    files,dirs = set(),set()
    for path in N.rglob("*"):
        assert not path.is_symlink(), str(path)
        name = str(path.relative_to(N))
        safe(name)
        if path.is_file():
            files.add(name)
        elif path.is_dir():
            dirs.add(name)
        else:
            raise AssertionError(("nonregular entry",name))
    return files,dirs

def core(public_only):
    plan = load(N/"CLOSURE_PLAN.json")
    whitelist = plan["public_whitelist_before_generated_closure"]
    assert len(whitelist) == len(set(whitelist))
    assert all("/" not in safe(name) for name in whitelist)
    gate = load(N/"PRIMARY_GATE.json")
    for row in gate["files"]:
        if not public_only or not row["path"].startswith("private/"):
            check(row,relative=True)
    assert sha((N/"PRIMARY_GATE.json").read_bytes()) == plan["primary_gate_sha256"]
    current = load(N/"CURRENT_BINDINGS.json")
    replays = load(N/"REPLAY_BINDINGS.json")
    assert current["status"] == "PASS"
    assert current["full_package_outputs_compared_to_current_expected"] is True
    assert replays["full_package_outputs_compared_to_current_expected"] is True
    assert load(N/"FILE_SCHEMA_INVENTORY.json")["zip_members"] == 74
    if public_only:
        return whitelist,0
    for row in current["canonical_four"].values():
        check(row)
    for row in load(N/"SOURCE_INVENTORY.json")["sources"]:
        check(row)
    runs = replays["runs"]
    assert len(runs) == 11
    for name,row in runs.items():
        native = json.loads(check(row["native_receipt"]))
        out = check(row["stdout"])
        err = check(row["stderr"])
        assert native["argv"] == row["argv"] and native["cwd"] == row["cwd"]
        assert native["exit_code"] == row["exit_code"] == 0 and err == b""
        assert native["started_utc"] == row["started_utc"] and native["finished_utc"] == row["finished_utc"]
        assert sha(out) == native["stdout_sha256"] and sha(err) == native["stderr_sha256"]
        for version in row["observed_input_versions"]:
            check(version)
        if "expected_complete_stdout" in row:
            assert check(row["expected_complete_stdout"]) == out
    check(replays["runtime_version_native_receipt"])
    check(replays["runtime_version_full_stdout"])
    check(replays["parent_independent_control_replay_receipt"])
    # Verify every complete standardized native receipt, including non-replay reads.
    for receipt in (N/"private/receipts").glob("*.json"):
        native = load(receipt)
        if "stdout_file" not in native:
            continue
        for key in ("stdout","stderr"):
            data = (receipt.parent/safe(native[key+"_file"])).read_bytes()
            assert sha(data) == native[key+"_sha256"], str(receipt)
        for row in native["inputs"]:
            path = pathlib.Path(row["path"])
            if not path.is_file() or sha(path.read_bytes()) != row["sha256"]:
                path = N/"private/code_versions"/row["sha256"]/path.name
            check({**row,"path":str(path)})
    return whitelist,len(runs)

def verify(public_only=False,draft=False):
    whitelist,runs = core(public_only)
    if draft:
        assert not (N/"CLOSURE.json").exists(), "namespace already closed"
        files,dirs = tree()
        assert {p for p in files if not p.startswith("private/")} == set(whitelist)
        assert all(p == "private" or p.startswith("private/") for p in dirs)
        return {"status":"PASS_DRAFT_READ_ONLY_INVENTORY","closed":False,
                "public_files":len(whitelist),"private_files":sum(p.startswith("private/") for p in files),
                "replay_bindings_checked":runs,"read_only":True}
    closure = load(N/"CLOSURE.json")
    assert closure["closed"] is True and closure["status"] == "FINAL_CLOSED"
    for key,name in [("public_manifest","PUBLIC_MANIFEST.json"),("private_manifest","PRIVATE_MANIFEST.json")]:
        check({"path":name,**closure[key]},relative=True)
    public = load(N/"PUBLIC_MANIFEST.json")
    private = load(N/"PRIVATE_MANIFEST.json")
    assert public["sealed_utc"] == private["sealed_utc"] == closure["sealed_utc"]
    assert len(public["files"]) == closure["public_files"] == len(whitelist)
    assert {safe(row["path"]) for row in public["files"]} == set(whitelist)
    for row in public["files"]:
        check(row,relative=True)
    # Public mirrors may omit the private directory. Root-level public bytes must be exact.
    root_files = {p.name for p in N.iterdir() if p.is_file()}
    assert root_files == set(whitelist)|GENERATED
    assert all(not p.is_symlink() for p in N.iterdir())
    private_count = 0
    if not public_only:
        names = [safe(row["path"]) for row in private["files"]]
        assert len(names) == len(set(names)) == closure["private_files"]
        assert all(p.startswith("private/") for p in names)
        for row in private["files"]:
            check(row,relative=True)
        files,dirs = tree()
        assert files == set(whitelist)|set(names)|GENERATED
        assert dirs == set(private["directories"])
        check(closure["root_approval_receipt"],relative=True)
        private_count = len(names)
    return {"status":"PASS_CLOSED_READ_ONLY_INVENTORY","closed":True,
            "mode":"public_only_private_external_unchecked" if public_only else "full_private_and_live_external_bindings",
            "closure_sha256":sha((N/"CLOSURE.json").read_bytes()),
            "public_files":len(whitelist),"private_files_checked":private_count,
            "replay_bindings_checked":runs,"read_only":True}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-only",action="store_true")
    parser.add_argument("--draft",action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.public_only,args.draft),indent=2)+"\n",end="")
