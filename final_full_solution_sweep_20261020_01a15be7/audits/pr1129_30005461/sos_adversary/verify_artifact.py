"""Read-only, offline verifier. Requires the manifest digest from outside this tree."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys

sys.dont_write_bytecode = True
HEAD = "26fed29c1130e539ba018a37200f133870f0e036"
BASE = "f6caddda8f8be2cdb3e91494325d8f7f365bc3fc"
PUBLIC = {".gitignore", "CHECKS.json", "CONTROL_TESTS.json", "RESEARCH_LOG.md", "REVIEW.md", "SOURCE_BINDINGS.json", "VERIFYING.md", "independent_checks.py", "verify_artifact.py"}
PR_NAMES = {"ACCEPTANCE.json", "CREDITED_MIXED_EXPONENT_PROOF.md", "MANIFEST.json", "MATHEMATICAL_AUDIT.md", "PROOF.md", "README.md", "REAL_DELTA_APPENDIX.md", "SOURCE_METADATA.json", "SOURCE_REVIEW.md", "STATUS.json"}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pairs(items):
    out = {}
    for key, value in items:
        need(key not in out, "duplicate JSON key: " + key)
        out[key] = value
    return out


def nonfinite(value):
    raise ValueError("nonfinite JSON value: " + value)


def parse(data):
    return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=nonfinite)


def relative(value):
    need(type(value) is str and value and "\\" not in value and "\0" not in value, "invalid relative path")
    path = PurePosixPath(value)
    need(not path.is_absolute() and path.as_posix() == value and all(part not in (".", "..", "") for part in path.parts), "noncanonical relative path")
    return value


def entries(value, allowed=None):
    need(type(value) is list, "inventory must be a list")
    out = {}
    folded = set()
    for entry in value:
        need(type(entry) is dict and set(entry) == {"path", "bytes", "sha256"}, "invalid inventory entry")
        name = relative(entry["path"])
        need(name not in out and name.casefold() not in folded, "duplicate inventory path")
        need(type(entry["bytes"]) is int and entry["bytes"] >= 0, "invalid byte count")
        need(type(entry["sha256"]) is str and re.fullmatch("[0-9a-f]{64}", entry["sha256"]) is not None, "invalid SHA256")
        if allowed is not None:
            need(name in allowed, "unexpected inventory path")
        out[name] = entry
        folded.add(name.casefold())
    return out


def read_bound(root, entry):
    path = root / relative(entry["path"])
    need(not path.is_symlink() and path.is_file(), "bound input is not a regular file")
    data = path.read_bytes()
    need(len(data) == entry["bytes"] and digest(data) == entry["sha256"], "byte identity mismatch: " + entry["path"])
    return data


def verify(root, anchor):
    need(re.fullmatch("[0-9a-f]{64}", anchor) is not None, "external anchor must be a lower-case SHA256")
    need(not root.is_symlink() and root.is_dir(), "root must be a nonsymlink directory")
    root = root.resolve(strict=True)
    need(Path(__file__).resolve(strict=True) == root / "verify_artifact.py", "execute the verifier in the selected fresh copy")
    actual_files = set()
    actual_dirs = set()
    for path in root.rglob("*"):
        need(not path.is_symlink(), "symlink rejected: " + str(path.relative_to(root)))
        mode = path.stat().st_mode
        name = path.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            actual_dirs.add(name)
        else:
            need(stat.S_ISREG(mode), "special filesystem object rejected")
            actual_files.add(name)
    raw_manifest = (root / "MANIFEST.json").read_bytes()
    need(digest(raw_manifest) == anchor, "external manifest anchor mismatch")
    manifest = parse(raw_manifest)
    need(type(manifest) is dict and set(manifest) == {"schema", "head", "base", "public_files", "private_manifest"}, "invalid top-level manifest")
    need(manifest["schema"] == "pr1129-sos-audit-seal-v1" and manifest["head"] == HEAD and manifest["base"] == BASE, "manifest scope mismatch")
    public = entries(manifest["public_files"], PUBLIC)
    need(set(public) == PUBLIC, "public inventory incomplete")
    input_entry = entries([manifest["private_manifest"]])
    need(set(input_entry) == {"private/INPUT_MANIFEST.json"}, "private manifest path mismatch")
    input_manifest = parse(read_bound(root, manifest["private_manifest"]))
    need(type(input_manifest) is dict and set(input_manifest) == {"schema", "files"} and input_manifest["schema"] == "pr1129-private-inputs-v1", "invalid private manifest")
    private = entries(input_manifest["files"])
    need(all(name.startswith("private/") and name != "private/INPUT_MANIFEST.json" for name in private), "private inventory escaped its tree")
    expected_files = set(public) | set(private) | {"MANIFEST.json", "private/INPUT_MANIFEST.json"}
    need(actual_files == expected_files, "closed file inventory mismatch")
    expected_dirs = {parent.as_posix() for name in expected_files for parent in PurePosixPath(name).parents if parent.as_posix() != "."}
    need(actual_dirs == expected_dirs, "closed directory inventory mismatch")
    for entry in list(public.values()) + list(private.values()):
        read_bound(root, entry)

    scope = parse((root / "private/PR_SCOPE.json").read_bytes())
    need(scope["head"] == HEAD and scope["base"] == BASE, "captured PR scope mismatch")
    need(type(scope["changed_files"]) is list and len(scope["changed_files"]) == 10, "captured PR inventory count mismatch")
    captured = {}
    for entry in scope["changed_files"]:
        name = PurePosixPath(entry["repository_path"]).name
        need(name in PR_NAMES and name not in captured, "PR filename mismatch")
        need(entry["repository_path"] == "unsolved_math_prioritization/attempts/30005461/" + name, "PR repository path mismatch")
        need(entry["capture_path"] == "private/pr_head/" + name, "PR capture path mismatch")
        data = (root / entry["capture_path"]).read_bytes()
        need(entry["bytes"] == len(data) and entry["sha256"] == digest(data), "captured PR digest mismatch")
        blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
        need(blob == entry["git_blob"], "captured Git blob mismatch")
        captured[name] = data
    need(set(captured) == PR_NAMES, "PR member inventory incomplete")
    prior_manifest = parse(captured["MANIFEST.json"])
    need(prior_manifest["member_count"] == 10 and set(prior_manifest["members"]) == PR_NAMES and len(prior_manifest["members"]) == 10, "PR-authored inventory mismatch")
    seen = set()
    for entry in prior_manifest["entries"]:
        name = entry["file"]
        need(name in PR_NAMES - {"MANIFEST.json"} and name not in seen, "PR-authored digest inventory mismatch")
        need(entry["bytes"] == len(captured[name]) and entry["sha256"] == digest(captured[name]), "PR-authored digest mismatch")
        seen.add(name)
    need(seen == PR_NAMES - {"MANIFEST.json"}, "PR-authored digest inventory incomplete")
    for name in ["STATUS.json", "ACCEPTANCE.json"]:
        status = parse(captured[name])
        need(status["full_resolution"] is True and status["limit"] == 3 and status["essential_preprint_dependency"] is False, "PR declared principal scope changed")
        need(status["novelty_claim"] is False and status["mathematical_verdict_depends_on_omitted_code"] is False, "PR declared limits changed")
    acceptance = parse(captured["ACCEPTANCE.json"])
    for field in ["proof", "audit", "credited_clause_proof", "optional_appendix"]:
        entry = acceptance[field]
        need(entry["bytes"] == len(captured[entry["name"]]) and entry["sha256"] == digest(captured[entry["name"]]), "PR acceptance binding mismatch")

    sources = parse((root / "SOURCE_BINDINGS.json").read_bytes())
    need(sources["head"] == HEAD and sources["base"] == BASE and sources["source_scripts_executed"] is False, "source-binding scope mismatch")
    source_paths = set()
    for entry in sources["source_files"]:
        name = relative(entry["path"])
        need(name in private and name.startswith("private/sources/") and name not in source_paths, "source binding path mismatch")
        need(entry["bytes"] == private[name]["bytes"] and entry["sha256"] == private[name]["sha256"], "source-binding identity mismatch")
        need(entry["url"].startswith("https://"), "unexpected source URL")
        source_paths.add(name)
    need(source_paths == {"private/sources/" + name for name in ["original_owr.pdf", "bkr_publisher.pdf", "bkr_v1.pdf", "scheiderer_arxiv_v1.pdf", "stubborn_v1.pdf", "stacks_01XS.html", "bkr_publisher.html"]}, "required primary source absent")

    # Load only the newly authored independent checker after its exact bytes are validated.
    spec = importlib.util.spec_from_file_location("sealed_pr1129_independent_checks", root / "independent_checks.py")
    need(spec is not None and spec.loader is not None, "cannot load bound independent checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.run_checks()
    need(result == parse((root / "CHECKS.json").read_bytes()), "recomputed exact checks differ from recorded checks")
    return {"verdict": "PASS", "head": HEAD, "public_files": len(public), "private_files": len(private), "exact_checks": result["total_exact_checks"], "mathematical_adverse_controls": result["mathematical_adverse_control_count"], "manifest_sha256": anchor, "read_only_offline": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--expect-manifest-sha256", required=True)
    args = parser.parse_args()
    try:
        result = verify(Path(args.root).absolute(), args.expect_manifest_sha256)
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
