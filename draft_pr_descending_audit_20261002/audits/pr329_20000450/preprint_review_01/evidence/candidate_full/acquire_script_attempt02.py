#!/usr/bin/env python3
"""Copy exact released eight inputs and qualification, then safely extract ZIP."""
import hashlib
import json
import pathlib
import shutil
import zipfile

root = pathlib.Path(__file__).resolve().parents[1]
source = root.parent / "preprint" / "qualification_v02"
dest = root / "evidence" / "candidate_full"
(dest / "inputs").mkdir(parents=True, exist_ok=True)
names = ("snapshot_manifest.json", "ROOT_CURRENT_MATHEMATICAL_GATE.json",
         "ROOT_PRIORITY_CLOSURE.json", "manuscript.tex", "manuscript.pdf",
         "verification.zip", "zenodo-deposit.json", "source_pdf_binding.json")
rows = []
for name in names + ("QUALIFICATION.json",):
    src = source / (name if name == "QUALIFICATION.json" else "inputs/" + name)
    dst = dest / (name if name == "QUALIFICATION.json" else "inputs/" + name)
    data = src.read_bytes()
    if dst.exists():
        assert dst.read_bytes() == data, f"Existing evidence differs: {dst}"
    else:
        shutil.copyfile(src, dst)
    assert data == src.read_bytes() == dst.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    if name == "QUALIFICATION.json":
        assert sha == "5d97927660309fefdfd62bf34b2403c6d9310f6d607121976a6ab461052fc0fa"
    if name == "verification.zip":
        assert sha == "6b650fcbe41a6ddca2f6b626b1c16182d8e7f7d9650320585b1c96d16e67dcf0"
    row = {"name": name, "source": str(src), "copy": str(dst), "bytes": len(data), "sha256": sha}
    rows.append(row)
    print(json.dumps(row, sort_keys=True))
(dest / "exact_full_input_pins.json").write_text(json.dumps(rows, indent=2) + "\n")
archive = dest / "archive"
archive.mkdir(exist_ok=True)
with zipfile.ZipFile(dest / "inputs" / "verification.zip") as z:
    payloads = []
    for item in z.infolist():
        path = pathlib.PurePosixPath(item.filename)
        assert not path.is_absolute() and ".." not in path.parts
        assert not ((item.external_attr >> 16) & 0o170000) == 0o120000
        if item.is_dir():
            (archive / path).mkdir(parents=True, exist_ok=True)
            continue
        data = z.read(item)
        target = archive / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert target.read_bytes() == data, f"Existing extracted evidence differs: {target}"
        else:
            target.write_bytes(data)
        mode = (item.external_attr >> 16) & 0o777
        if mode:
            target.chmod(mode)
        row = {"path": item.filename, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "zip_mode": oct(mode)}
        payloads.append(row)
        print(json.dumps(row, sort_keys=True))
    assert len(payloads) == 50
(dest / "archive_inventory.json").write_text(json.dumps(payloads, indent=2) + "\n")

current = (root / "FIRST_CANDIDATE_ASSESSMENT.md").read_bytes()
old = current.replace(b"No clipped text, unreadable", b"No clipped text,+unreadable")
sha = hashlib.sha256(old).hexdigest()
assert sha == "42bccc5a26c15bb8c7dfeb41c2ecdc896af9e04c9b6a11e92c23662e06690a5b"
reconstruction = dest / "first_assessment_42bccc_COMPUTED_RECONSTRUCTION.md"
reconstruction.write_bytes(old)
print(json.dumps({"computed_reconstruction": str(reconstruction), "sha256": sha,
                  "warning": "After-the-fact exact byte reconstruction at this native execution time; not historical retrieval evidence."}))
