#!/usr/bin/env python3
"""Data-only identity/archive/reference checks, no scientific code execution."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

K = Path(__file__).resolve().parent
S = K.parent.parent / "sources"
E = S / "archives/02-gram_locus_support.zip.extracted"
PINS = {
 "seigal.pdf": "09f688310260a3a07db1c6a0aff53163209e377c201f6044c461eb601cc70163",
 "hss-v2.pdf": "68a6e634e0197851b5b1d6d487918597bc0da4f7964cdb84183e8793d95cde34",
 "bravyi-v1.pdf": "a23c86f24764a9ce930e7de3bcb23f0a6fc4b34081244b0b749352046668cd30",
 "dsl-published.pdf": "707814c6d7ae700bce1c61d5519cd32441cafbe8b60af63c4b21c04acc4f6589",
 "sinn-v1.pdf": "1b85888e22d27942bcb4d03ca22ccdf93c251988cacc8bb6e034f91e1c07c8ba",
 "ferudun.pdf": "a99172938f203f5a494c2191a73072299857ce8d3adfa6867831ca737c471cbb",
 "owr.pdf": "13b45b3e2c9f585fab343c1d10d3e0fc9e1b4cf47880b5bcf1808fcb23280de3",
}
def identity(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

result = {"primary": {}}
for name, expected in PINS.items():
    actual = identity((K / "primary" / name).read_bytes())
    assert actual["sha256"] == expected, name
    result["primary"][name] = actual
archive = S / "zenodo-files/gram_locus_support.zip"
data = archive.read_bytes()
assert identity(data)["sha256"] == "4df495ac35094dfbacaf4453bde1a71ecae80de23aa50111b3eb7664c2f453e2"
manifest = json.loads((E / "MANIFEST.json").read_text())
assert manifest["format"] == "PR170-Gram-locus-support-v2"
assert manifest["self_reference_exclusion"] == "MANIFEST.json"
entries = []
with zipfile.ZipFile(archive) as z:
    infos = z.infolist()
    names = [item.filename for item in infos]
    assert len(names) == len(set(names)), "Duplicate ZIP member"
    assert set(names) == set(manifest["files"]) | {"MANIFEST.json"}
    assert set(names) == {p.relative_to(E).as_posix() for p in E.rglob("*") if p.is_file()}
    for item in infos:
        name = item.filename
        path = PurePosixPath(name)
        assert not path.is_absolute() and ".." not in path.parts and not item.is_dir(), name
        mode = item.external_attr >> 16
        assert stat.S_ISREG(mode), (name, mode)
        body = z.read(item)
        assert body == (E / name).read_bytes(), name
        actual = identity(body)
        if name != "MANIFEST.json":
            assert actual == manifest["files"][name], name
        entries.append(dict(path=name, mode_octal=oct(stat.S_IMODE(mode)), **actual))
result["archive"] = dict(identity(data), files=len(entries), entries=entries,
                          embedded_pdf_count=sum(e["path"].lower().endswith(".pdf") for e in entries))
index = json.loads((E / "SUPPORT_INDEX.json").read_text())
included = [name for family in index["families"] for name in family["included_paths"]]
assert len(included) == len(set(included))
assert all((E / name).is_file() for name in included)
firsts = json.loads((E / "priority_reviews/root/FIRST_SEAL_IDENTITIES.json").read_text())
for row in firsts["first_records"]:
    if row["included_archive_path"] is not None:
        assert identity((E / row["included_archive_path"]).read_bytes()) == {key: row[key] for key in ["bytes", "sha256"]}
result["support_index_included_paths_resolve"] = len(included)
result["excluded_private_evidence_not_authenticated_as_available"] = True
proof = (K / "primary/pr170-original-proof.md").read_bytes()
head = (K / "primary/pr170-head-proof.md").read_bytes()
assert proof == head
blob = hashlib.sha1(b"blob " + str(len(proof)).encode() + b"\0" + proof).hexdigest()
assert blob == "0288098b58b95678c1c350c8766db7602966d1a9"
pr = json.loads((K / "primary/pr170.json").read_text())
repo = json.loads((K / "primary/github-repo.json").read_text())
commits = json.loads((K / "primary/pr170-commits.json").read_text())
result["chronology"] = {"PR_created": pr["created_at"], "PR_current_updated": pr["updated_at"],
 "PR_head": pr["head"]["sha"], "repository_private": repo["private"], "repository_visibility": repo["visibility"],
 "original_commit": commits[0]["sha"], "original_author": commits[0]["commit"]["author"]["date"],
 "original_committer": commits[0]["commit"]["committer"]["date"],
 "proof": dict(identity(proof), git_blob_oid=blob), "historical_visibility_certified": False}
normal = (K / "runtime/verification.normal.json").read_bytes()
assert normal == (K / "runtime/verification.optimized.json").read_bytes()
assert normal == (E / "verification.normal.json").read_bytes() == (E / "verification.optimized.json").read_bytes()
result["baseline_bytes_exact_to_each_other_and_deposit"] = identity(normal)
result["status"] = "ALL_DATA_IDENTITY_CHECKS_PASS"
(K / "DATA_CHECKS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "primary_PDFs": len(PINS),
                  "ZIP_members": len(entries), "included_support_references": len(included), "original_blob_oid": blob}))
