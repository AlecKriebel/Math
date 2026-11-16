"""Read-only custody and exact arithmetic; no scientific checker is imported."""
from pathlib import Path
import base64
import hashlib
import json
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
P = ROOT.parents[3]
PAPER = P / "papers/23203732"
checks = 0


def require(value, label):
    global checks
    checks += 1
    if not value:
        raise RuntimeError(label)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def typed(value):
    if isinstance(value, dict):
        return ("object", tuple((k, typed(v)) for k, v in value.items()))
    if isinstance(value, list):
        return ("array", tuple(typed(v) for v in value))
    return (type(value).__name__, value)


def namespace(relative, manifest_name, terminals, count, directories):
    base = P / relative
    manifest = json.loads((base / manifest_name).read_bytes())
    records = manifest["files"]
    names = [r["path"] for r in records]
    require(len(names) == len(set(names)), relative + " unique payloads")
    require(not set(names).intersection(terminals), relative + " exact terminals")
    actual_files, actual_dirs = [], []
    for path in base.rglob("*"):
        mode = path.lstat().st_mode
        name = str(path.relative_to(base))
        require(not stat.S_ISLNK(mode), name + " no symlink")
        if stat.S_ISDIR(mode):
            actual_dirs.append(name)
        else:
            require(stat.S_ISREG(mode), name + " regular")
            actual_files.append(name)
    require(len(actual_files) == count, relative + " whole file count")
    require(len(actual_dirs) == directories, relative + " whole directory count")
    require(sorted(actual_files) == sorted(names + terminals), relative + " exact file membership")
    require(len(manifest["directories"]) == len(set(manifest["directories"])), relative + " unique dirs")
    require(sorted(actual_dirs) == sorted(manifest["directories"]), relative + " exact directory membership")
    for record in records:
        path = base / record["path"]
        require(path.is_relative_to(base) and ".." not in Path(record["path"]).parts, "safe relative path")
        require(path.stat().st_size == record["bytes"], str(path) + " bytes")
        require(digest(path) == record["SHA256"], str(path) + " SHA256")
    return {"files": count, "directories": directories, "manifest_SHA256": digest(base / manifest_name)}


def main():
    pins = {
        "sources/SOURCE_READY_SEAL.json": "cf9ffb0b5f509af974aa3e7a368c2672e000f2665aecf772a0df57f658145287",
        "reviews/scope/FINAL_SEAL.json": "c9ae1ef347f619ab7a45fa8374999c5e80129dd4900f1488a4e058df97fe8553",
        "reviews/adversarial/FINAL_SEAL.json": "ac56647773baa8e66de655af3ce092457719d16d12012020c1f0f07d45520182",
        "reviews/root/INITIAL_RECONSTRUCTION_20261115.md": "6a53b5000bae0984d99834b724b20bfd6120d6e6fef8e66f19ea275afa24cb20",
    }
    for name, sha in pins.items():
        require(digest(PAPER / name) == sha, name + " fixed seal")
    correction = "verification/23203732-adversarial-custody-correction-sol-20261115"
    require(digest(P / correction / "FINAL_SEAL.json") == "fe806f3f32f50f344a66dfca9ae8ca4aa935fc0a2acec77e17af9da8890cc53e", "separate correction seal")
    extents = {
        "source": namespace("papers/23203732/sources", "SOURCE_READY_MANIFEST.json", ["SOURCE_READY_CLOSURE.json", "SOURCE_READY_MANIFEST.json", "SOURCE_READY_SEAL.json"], 101, 18),
        "scope": namespace("papers/23203732/reviews/scope", "OWNED_MANIFEST.json", ["CLOSURE.json", "FINAL_SEAL.json", "OWNED_MANIFEST.json"], 233, 29),
        "adversarial": namespace("papers/23203732/reviews/adversarial", "MANIFEST.json", ["MANIFEST.json", "FINAL_SEAL.json"], 159, 20),
        "separate_correction": namespace(correction, "MANIFEST.json", ["MANIFEST.json", "FINAL_SEAL.json"], 14, 0),
    }
    source = PAPER / "sources/published-source/asset-002"
    archive = PAPER / "sources/assets/cost-betti-source-and-verification.zip"
    members, expanded = 0, 0
    with zipfile.ZipFile(archive) as handle:
        require(handle.testzip() is None, "ZIP complete CRC")
        for entry in handle.infolist():
            if entry.is_dir():
                continue
            member = Path(entry.filename)
            require(not member.is_absolute() and ".." not in member.parts, "safe ZIP member")
            require(handle.read(entry) == (source / member).read_bytes(), entry.filename + " whole ZIP bytes")
            members += 1
            expanded += entry.file_size
    require((members, expanded) == (35, 313796), "whole ZIP extent")
    require((source / "paper.pdf").read_bytes() == (PAPER / "sources/assets/paper.pdf").read_bytes(), "embedded PDF whole identical")
    primary = PAPER / "reviews/adversarial/primary"
    upstream = json.loads((source / "upstream/UPSTREAM_MANIFEST.json").read_bytes())
    require(upstream["commit"] == "adc7f1241b42e322a6451854ab7e4b4c146bf78a", "exact upstream pin")
    bodies = []
    for entry in upstream["files"]:
        name = Path(entry["path"]).name
        if "/build/" in entry["path"]:
            path = primary / ("extra-v3/openai-surgery-figure.hop0.body" if name == "surgery-figure.tex" else name)
        elif name == "INPUTS.md":
            path = primary / name
        elif name == "unequal-costs-rank-100-amalgam.pdf":
            path = primary / "openai-pinned.pdf"
        else:
            continue
        require(path.stat().st_size == entry["bytes"] and digest(path) == entry["sha256"], name + " native upstream binding")
        bodies.append({"name": name, "bytes": path.stat().st_size, "SHA256": digest(path)})
    require(len(bodies) == 13, "12 fully read source bodies plus PDF binding")
    api = json.loads((primary / "extra/openai-contents.hop0.body").read_bytes())
    decoded = base64.b64decode(api["content"])
    require(decoded == (primary / "openai-pinned.pdf").read_bytes(), "whole official API PDF content")
    require(hashlib.sha1(b"blob " + str(len(decoded)).encode() + b"\0" + decoded).hexdigest() == api["sha"], "official native Git blob SHA1")
    expected = source / "verification/check_fox_results.json"
    for mode in ["NORMAL", "OPTIMIZED"]:
        observed = PAPER / ("reviews/adversarial/NATIVE_" + mode + ".stdout.json")
        require(observed.read_bytes() == expected.read_bytes(), mode + " whole expected stream")
        require(typed(json.loads(observed.read_bytes())) == typed(json.loads(expected.read_bytes())), mode + " whole typed ordered JSON")
        require((PAPER / ("reviews/adversarial/NATIVE_" + mode + ".stderr.txt")).read_bytes() == b"", mode + " empty stderr")
    replay = json.loads((PAPER / "reviews/adversarial/NATIVE_REPLAY_RECEIPT.json").read_bytes())
    require(all(run["exit_code"] == 0 for run in replay["runs"]), "actual designated owner exits")
    require(replay["O_assertions_disabled_not_verification"] is True, "optimized output is not assertion verification")
    require(2 * 3**97 * 96**4 < 2**183 and 2**61 > 200, "independent exact alpha certificate")
    require(digest(P / "scripts/checkpoint_subtree.py") == "405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0", "sole separately authorized checkpoint helper")
    print(json.dumps({"status": "PASS_READ_ONLY_CUSTODY_AND_EXACT_ARITHMETIC", "checks": checks, "extents": extents, "ZIP_regular_members": members, "ZIP_expanded_bytes": expanded, "upstream_bound_bodies": bodies, "native_scientific_routes_executed_by_root": 0, "optimized_native_output_is_assertion_verification": False, "subprocess_network_imports_or_writes": False}, indent=2))


if __name__ == "__main__":
    main()
