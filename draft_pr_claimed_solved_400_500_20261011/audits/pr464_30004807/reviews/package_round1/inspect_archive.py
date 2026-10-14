#!/usr/bin/env python3
"""Read-only frozen-candidate integrity inspection and private extraction."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import stat
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
PACKAGE = AUDIT / "package"
FORBIDDEN = {"private_sources", "private_cases", "mutation_fixtures", ".secrets", ".zenodo-state", "__pycache__", ".venv"}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, "Duplicate JSON key")
        result[key] = value
    return result

def decode(data):
    return json.loads(data, object_pairs_hook=pairs)

def safe(name):
    require(type(name) is str and name, "Empty entry")
    p = PurePosixPath(name)
    require(not p.is_absolute() and ".." not in p.parts and p.as_posix() == name, "Unsafe entry")
    require(not set(p.parts) & FORBIDDEN, "Private entry")
    require(p.suffix not in {".pyc", ".pdf", ".png", ".jpeg", ".jpg", ".env"}, "Unexpected binary/private source")
    return p

def main():
    frozen_path = AUDIT / "PACKAGE_REVIEW_INPUT_2.json"
    frozen_data = frozen_path.read_bytes()
    frozen = decode(frozen_data)
    frozen_records = []
    for path, binding in frozen["files"].items():
        target = PACKAGE / path
        require(target.is_file() and not target.is_symlink(), "Frozen input missing or symlink")
        data = target.read_bytes()
        require(len(data) == binding["bytes"] and sha(data) == binding["sha256"], "Frozen input differs: " + path)
        frozen_records.append({"path": path, "bytes": len(data), "sha256": sha(data)})
    bindings = decode((PACKAGE / "SHA256SUMS.json").read_bytes())["files"]
    require(len(bindings) == 180, "Wrong positive archive payload count")
    out = HERE / "private_sources" / "extracted"
    require(not out.exists(), "Extraction already exists")
    entries = []
    scan_patterns = {"private_key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "github_credential": r"(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})", "google_credential": r"AIza[A-Za-z0-9_-]{30,}", "actual_access_token": r'"access_token"\s*:\s*"[^"\s]{20,}"'}
    hit_counts = {name: 0 for name in scan_patterns}
    with zipfile.ZipFile(PACKAGE / "regular_zas_bianchi_verification_v1.zip") as archive:
        require(archive.testzip() is None, "CRC failure")
        infos = archive.infolist()
        require(len(infos) == 181 and len({i.filename for i in infos}) == 181, "Wrong or duplicate archive inventory")
        require({i.filename for i in infos} == set(bindings) | {"SHA256SUMS.json"}, "Archive entry set differs")
        require(archive.read("SHA256SUMS.json") == (PACKAGE / "SHA256SUMS.json").read_bytes(), "Internal manifest differs")
        for info in infos:
            p = safe(info.filename)
            require(not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16), "Directory or symlink entry")
            require(not info.flag_bits & 1, "Encrypted entry")
            data = archive.read(info)
            require(len(data) == info.file_size, "ZIP byte count differs")
            disk = PACKAGE.joinpath(*p.parts)
            require(disk.is_file() and not disk.is_symlink() and disk.read_bytes() == data, "On-disk package differs")
            if info.filename != "SHA256SUMS.json":
                binding = bindings[info.filename]
                require(type(binding["bytes"]) is int and len(data) == binding["bytes"] and sha(data) == binding["sha256"], "Archive digest differs")
            text = data.decode("utf-8")
            require("\x00" not in text, "Binary data in authored text")
            if p.suffix == ".json":
                decode(data)
            for name, pattern in scan_patterns.items():
                hit_counts[name] += len(re.findall(pattern, text))
            entries.append({"path": info.filename, "bytes": len(data), "sha256": sha(data), "crc32": f"{info.CRC:08x}"})
            target = out.joinpath(*p.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    require(not any(hit_counts.values()), "Credential pattern detected; inspect privately")
    selection = decode((out / "REVIEW_EVIDENCE_SELECTION.json").read_bytes())
    origins_verified = []
    for entry in selection["entries"]:
        relative = PurePosixPath(entry["origin"])
        require(not relative.is_absolute() and ".." not in relative.parts and not set(relative.parts) & FORBIDDEN, "Unsafe evidence origin")
        origin = Path("/Users/alec/Documents/Math").joinpath(*relative.parts)
        data = (out / entry["path"]).read_bytes()
        require(len(data) == entry["bytes"] and sha(data) == entry["sha256"] and origin.read_bytes() == data, "Selected evidence origin differs")
        origins_verified.append(entry["path"])
    metadata = decode((PACKAGE / "metadata.json").read_bytes())
    deposit = decode((PACKAGE / "deposit.json").read_bytes())
    require(deposit["metadata"] == metadata, "Deposit metadata differs")
    require(deposit["files"] == [{"path": "manuscript.pdf", "name": "regular_zas_bianchi_defect.pdf"}, {"path": "regular_zas_bianchi_verification_v1.zip"}], "Wrong upload inventory")
    result = {"status": "PASS", "input_manifest_sha256": sha(frozen_data), "frozen_files": frozen_records, "archive_entries": 181, "payload_hashes_verified": 180, "crc_all_passed": True, "exact_entry_set": True, "all_entries_text_and_json_duplicate_keys_checked": True, "evidence_origins_verified": len(origins_verified), "evidence_origin_paths": origins_verified, "credential_pattern_hit_counts": hit_counts, "metadata_deposit_exact_equality": True, "private_extraction_only": True, "entries": entries}
    (HERE / "ARCHIVE_INSPECTION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key not in {"entries", "evidence_origin_paths", "frozen_files"}}, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
