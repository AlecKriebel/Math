"""Independent, read-only audit of the exact preprint kit.

Writes only the caller-specified review receipt. No network or git operations.
All checks survive Python -O. It does not verify the geometric theorem.
"""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile


def require(value, message):
    if not value:
        raise ValueError(message)


def info(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def safe(name):
    require(isinstance(name, str) and name and "\\" not in name and
            not PurePosixPath(name).is_absolute() and
            all(p not in ("", ".", "..") for p in name.split("/")) and
            str(PurePosixPath(name)) == name, "Unsafe inventory path")
    return name


def manifest_check(files, manifest_name="MANIFEST.json"):
    require(manifest_name in files, "Missing manifest")
    rows = json.loads(files[manifest_name])["files"]
    listed = {}
    for row in rows:
        name = safe(row["path"])
        require(name not in listed and name != manifest_name, "Duplicate/self manifest entry")
        listed[name] = {key: row[key] for key in ("bytes", "sha256")}
    require(set(files) == set(listed) | {manifest_name}, "Manifest inventory differs")
    for name, expected in listed.items():
        require(info(files[name]) == expected, "Manifest content differs: " + name)
    return {"manifest": manifest_name, "listed_files": len(rows),
            "closed_inventory_and_hashes": True, **info(files[manifest_name])}


def zip_inventory(raw, label, receipts):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        require(z.testzip() is None, "CRC error: " + label)
        items = z.infolist()
        names = [safe(i.filename) for i in items]
        require(len(names) == len(set(names)), "Duplicate ZIP entry: " + label)
        for item in items:
            require(not item.is_dir() and not item.flag_bits & 1 and
                    stat.S_IFMT(item.external_attr >> 16) in (0, stat.S_IFREG),
                    "Nonregular/encrypted ZIP entry: " + label)
        files = {i.filename: z.read(i) for i in items}
    receipts.append({"archive": label, "entries": len(files), "crc_ok": True,
                     "paths_unique_safe_regular_unencrypted": True})
    return files


def recursive_leaves(files, label, archives):
    result = {}
    for name, raw in files.items():
        if name.endswith(".zip"):
            nested = zip_inventory(raw, label + "/" + name, archives)
            result.update(recursive_leaves(nested, label + "/" + name, archives))
        else:
            result[label + "/" + name] = raw
    return result


def subtree(files, prefix):
    return {n[len(prefix):]: b for n, b in files.items() if n.startswith(prefix)}


def main():
    review = Path(__file__).resolve().parents[1]
    governing = review.parent / "preprint"
    receipt = {"checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "optimized_auditor": sys.flags.optimize > 0, "archives": []}
    pins = {
        "paper.tex": "fe385adc3db169e6eeacce965c337aaf5f7a185491944ca096c0709bbcb785b6",
        "output/pdf/paper.pdf": "f3e5619c7e1560c45f7793b0f7e4dabfbbf66d08f568f3478b5bb8f35779ea17",
        "source-and-verification.zip": "22bcb3d40fd734a6ee6e416319f329739395dcc66417da5f27e82d32a85694cf",
        "zenodo-deposit.json": "4158f1d7b94528ca7e203859b5cdb41d54038300ca1f468b411570d95cb2f264",
        "zenodo-metadata.json": "4e21becd2c6534e3cf8053428b16690e40df52f77e1f3d3017e29e0b9f5d1cae",
        "zenodo-upload-kit.zip": "ebe24c6dc38bf339433477070ed4cc7f264f5a525490e04eb0ab8d9d3b45d97c",
    }
    actual = {n: (governing / n).read_bytes() for n in pins}
    for name, pin in pins.items():
        require(info(actual[name])["sha256"] == pin, "Exact input pin changed")
    inventory = json.loads((governing / "PACKAGE_INVENTORY.json").read_bytes())
    require({v["path"] for v in inventory["files"]} == set(pins), "Top output set differs")
    for row in inventory["files"]:
        require(info(actual[row["path"]]) == {k: row[k] for k in ("bytes", "sha256")},
                "Top inventory differs")
    receipt["pins"] = [{"path": n, **info(b)} for n, b in actual.items()]
    support = zip_inventory(actual["source-and-verification.zip"], "support", receipt["archives"])
    outer = zip_inventory(actual["zenodo-upload-kit.zip"], "outer", receipt["archives"])
    require(len(support) == inventory["support_files"] == 78, "Wrong support count")
    require(set(outer) == {"paper.pdf", "source-and-verification.zip", "zenodo-deposit.json",
                           "zenodo-metadata.json", "README.md"}, "Outer kit set differs")
    require(outer["paper.pdf"] == actual["output/pdf/paper.pdf"] and
            outer["source-and-verification.zip"] == actual["source-and-verification.zip"] and
            support["paper.tex"] == actual["paper.tex"], "Nested published bytes differ")
    receipt["manifests"] = [manifest_check(support)]
    historical = subtree(support, "historical_candidate/")
    receipt["manifests"].append(manifest_check(historical, "PUBLICATION_MANIFEST.json"))
    for prefix in ["tangent_seshadri_30004324_v2/", "tangent_seshadri_30004324_v2_delta_acceptance/"]:
        receipt["manifests"].append({"location": prefix, **manifest_check(subtree(historical, prefix))})
    for name in ["TANGENT_SESHADRI_30004324_AUTHOR_SAFE_FREEZE.zip",
                 "TANGENT_SESHADRI_30004324_V2_SAFE_FREEZE.zip"]:
        files = zip_inventory(historical[name], name, receipt["archives"])
        receipt["manifests"].append({"location": name, **manifest_check(files)})
    layouts = json.loads(historical["AUDIT_LAYOUTS.json"])["packages"]
    for layout in layouts:
        files = {safe(row["original_path"]): historical[safe(row["stored_path"])]
                 for row in layout["files"]}
        require(len(files) == len(layout["files"]), "Duplicate audit layout entry")
        for row in layout["files"]:
            require(info(files[row["original_path"]]) == {k: row[k] for k in ("bytes", "sha256")},
                    "Audit layout content differs")
        require(info(files["MANIFEST.json"])["sha256"] == layout["manifest_sha256"],
                "Reconstructed audit manifest pin differs")
        receipt["manifests"].append({"location": "reconstructed:" + layout["package"],
                                     **manifest_check(files)})
    original = review.parent / "original/unsolved_math_prioritization/attempts/30004324"
    frozen = {q.relative_to(original).as_posix(): q.read_bytes()
              for q in original.rglob("*") if q.is_file()}
    require(frozen == historical and len(frozen) == 49, "Original frozen inventory/bytes differ")
    receipt["frozen_originals"] = {"count": len(frozen), "byte_identical": True}
    leaves = recursive_leaves(support, "support", receipt["archives"])
    suspicious = [n for n, b in leaves.items() if b.startswith(b"%PDF") or
                  re.search(r"(?i)(private_sources|source_download|\.pdf$|\.docx$|\.png$|\.pem$)", n)]
    require(not suspicious, "Private or third-party body candidate found in support")
    secret_markers = [n for n, b in leaves.items() if re.search(
        rb"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{30,}|\bAKIA[0-9A-Z]{16}\b", b)]
    require(not secret_markers, "Credential candidate found in support")
    receipt["support_body_screen"] = {"recursive_nonzip_leaves": len(leaves),
        "pdf_private_source_or_common_credential_candidates": 0,
        "scope": "Mechanical candidate screen plus authored-source manual assessment; not arbitrary secret detection"}
    objects = [json.loads(actual["zenodo-metadata.json"])["metadata"],
        json.loads(actual["zenodo-deposit.json"])["metadata"],
        json.loads(support["zenodo-metadata.json"])["metadata"],
        json.loads(outer["zenodo-metadata.json"])["metadata"],
        json.loads(outer["zenodo-deposit.json"])["metadata"]]
    require(all(o == objects[0] for o in objects), "Metadata objects differ")
    require(json.loads(actual["zenodo-deposit.json"])["files"] == [
        {"path": "output/pdf/paper.pdf", "name": "paper.pdf"},
        {"path": "source-and-verification.zip", "name": "source-and-verification.zip"}],
        "Top deposit files differ")
    require(json.loads(outer["zenodo-deposit.json"])["files"] == [
        {"path": "paper.pdf"}, {"path": "source-and-verification.zip"}], "Flat deposit files differ")
    orcid = objects[0]["creators"][0]["orcid"]
    digits = orcid.replace("-", ""); total = 0
    for digit in digits[:-1]:
        total = (total + int(digit)) * 2
    check = (12 - total % 11) % 11
    require(digits[-1] == ("X" if check == 10 else str(check)), "ORCID checksum differs")
    receipt["metadata"] = {"five_objects_equal": True, "file_lists_correct": True,
        "orcid_checksum_valid": True, "title": objects[0]["title"], "version": objects[0]["version"],
        "publication_date": objects[0]["publication_date"], "license": objects[0]["license"]}
    env = os.environ.copy(); env["PYTHONDONTWRITEBYTECODE"] = "1"
    temp_root = review / "tmp" / "mutations"; temp_root.mkdir(parents=True, exist_ok=True)
    mutations = ["changed_same_size", "extra_nested_manifest", "missing_payload", "duplicate_manifest_path",
                 "self_manifest_entry", "traversal_manifest_path", "symlink"]
    receipt["outer_integrity_mutations"] = []
    for opt in (False, True):
        for mutation in mutations:
            with tempfile.TemporaryDirectory(dir=temp_root) as td:
                root = Path(td)
                for n, b in support.items():
                    p = root / n; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b)
                if mutation == "changed_same_size":
                    b = (root / "README.md").read_bytes(); (root / "README.md").write_bytes(bytes([b[0] ^ 1]) + b[1:])
                elif mutation == "extra_nested_manifest":
                    (root / "extra").mkdir(); (root / "extra/MANIFEST.json").write_text("{}\n")
                elif mutation == "missing_payload":
                    (root / "README.md").unlink()
                elif mutation == "symlink":
                    (root / "linked").symlink_to(root / "README.md")
                else:
                    m = json.loads((root / "MANIFEST.json").read_text())
                    if mutation == "duplicate_manifest_path":
                        m["files"].append(m["files"][0])
                    elif mutation == "self_manifest_entry":
                        m["files"].append({"path": "MANIFEST.json", **info((root / "MANIFEST.json").read_bytes())})
                    elif mutation == "traversal_manifest_path":
                        m["files"][0]["path"] = "../README.md"
                    (root / "MANIFEST.json").write_text(json.dumps(m))
                cmd = [sys.executable] + (["-O"] if opt else []) + [str(root / "verify_bundle.py"), "--integrity-only"]
                run = subprocess.run(cmd, env=env, capture_output=True, text=True)
                require(run.returncode != 0, "Integrity mutation accepted")
                receipt["outer_integrity_mutations"].append({"mutation": mutation, "outer_optimized": opt,
                                                            "rejected": True, "exit": run.returncode})
    receipt["result"] = "PASS"
    output = review / "evidence" / ("package_audit_optimized.json" if sys.flags.optimize else "package_audit_normal.json")
    output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"result": receipt["result"], "manifests": len(receipt["manifests"]),
                      "original_files": len(frozen), "recursive_leaf_files": len(leaves),
                      "rejected_outer_mutations": len(receipt["outer_integrity_mutations"]),
                      "receipt": str(output)}, indent=2))


if __name__ == "__main__":
    main()
