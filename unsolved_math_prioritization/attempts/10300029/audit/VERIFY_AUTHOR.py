"""Read-only, standard-library verification of one pinned data-only author ZIP.

Usage: python -I -S VERIFY_AUTHOR.py AUTHOR.zip [FREEZE_RECEIPT.json]
This verifies bytes and inventory, not mathematical truth. It never extracts,
imports, evaluates, or executes archive contents. No assertion is security-relevant.
"""
import hashlib
import io
import json
import pathlib
import stat
import sys
import zipfile

ARCHIVE_BYTES = 10214
ARCHIVE_SHA256 = "0a6048d92a27bfa34391e530f3bbbcf34b30688831b2df2e2017173ce936c5a1"
RECEIPT_BYTES = 991
RECEIPT_SHA256 = "6f912e9cc0ddb90d6b6d5aaf6ca793a713e38b779da19a0522f551be1bb7c2b3"
MEMBERS = {
    "MANIFEST.json": (1002, "c195830bb5f3739dc146c65ecbbf48933f5bfe1d4ff5d74b31fe5c66de14496c"),
    "README.md": (1094, "659ef8d08167614b9400797a08ea4ac198f182dfe9dfbdbbde505f8ddb13dce4"),
    "RESULT.md": (12679, "525093b7a53a40d4f1af5059392cd634841b9192c4f35cf01a2275ca49a5cf41"),
    "SOURCE_METADATA.json": (7203, "b036f6022ef289819988cfe49fda4dbc383d1d22c8bfec81bdcc32f8dbd49f3e"),
    "STATUS.json": (814, "5931d4cec967eee3b7f3a12d5c9c9a5757748e2d610c9eaf2253e5904d1fa2a5"),
}


class Invalid(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Invalid(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, "Duplicate JSON key")
        out[key] = value
    return out


def reject_constant(value):
    raise Invalid("Non-finite JSON constant")


def strict_json(data):
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def read_regular(path, expected_bytes):
    p = pathlib.Path(path)
    require(stat.S_ISREG(p.lstat().st_mode), "Input is not a regular file")
    require(p.stat().st_size == expected_bytes, "Wrong input byte count")
    with p.open("rb") as handle:
        data = handle.read(expected_bytes + 1)
    require(len(data) == expected_bytes, "Input changed or has wrong byte count")
    return data


def inspect_payload(data):
    """Structural layer; production entry point also pins the outer ZIP hash."""
    require(len(data) <= 100000, "Oversized structural test input")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        require(archive.comment == b"", "Archive comment is forbidden")
        infos = archive.infolist()
        names = [entry.filename for entry in infos]
        require(len(names) == len(set(names)), "Duplicate member")
        require(set(names) == set(MEMBERS), "Exact member inventory mismatch")
        payload = {}
        for entry in infos:
            name = entry.filename
            require(name == entry.orig_filename, "Ambiguous member name")
            require(not entry.is_dir(), "Directory member is forbidden")
            require(entry.create_system == 3, "Unexpected origin system")
            require(entry.external_attr >> 16 == stat.S_IFREG | 0o444,
                    "Member is not a read-only nonexecutable regular file")
            require(entry.flag_bits == 0, "Unexpected ZIP flags")
            require(entry.extra == b"" and entry.comment == b"",
                    "Member extra data or comment is forbidden")
            require(entry.compress_type == zipfile.ZIP_DEFLATED,
                    "Unexpected compression")
            length, digest = MEMBERS[name]
            require(entry.file_size == length, "Wrong member size: " + name)
            value = archive.read(entry)
            require(len(value) == length and sha(value) == digest,
                    "Wrong member bytes: " + name)
            value.decode("utf-8")
            payload[name] = value
        parsed = {name: strict_json(value) for name, value in payload.items()
                  if name.endswith(".json")}
        manifest = parsed["MANIFEST.json"]
        expected = [{"path": name, "bytes": size, "sha256": digest}
                    for name, (size, digest) in MEMBERS.items()
                    if name != "MANIFEST.json"]
        require(manifest["payload_members"] == expected,
                "Manifest does not describe the complete non-self payload")
        require(manifest["format"] == "closed-nonexecutable-mathematical-payload-v1",
                "Unexpected manifest type")
        status = parsed["STATUS.json"]
        require(status["problem_id"] == 10300029 and
                status["overall_disposition"] == "unsolved" and
                status["mathematical_executable_included"] is False,
                "Incorrect disposition or execution scope")
        return [{"path": name, "bytes": size, "sha256": digest}
                for name, (size, digest) in MEMBERS.items()]


def verify(archive_path, receipt_path=None):
    data = read_regular(archive_path, ARCHIVE_BYTES)
    require(sha(data) == ARCHIVE_SHA256, "Wrong archive SHA-256")
    inventory = inspect_payload(data)
    receipt_verified = False
    if receipt_path is not None:
        raw = read_regular(receipt_path, RECEIPT_BYTES)
        require(sha(raw) == RECEIPT_SHA256, "Wrong receipt SHA-256")
        receipt = strict_json(raw)
        require(receipt["bytes"] == ARCHIVE_BYTES and
                receipt["sha256"] == ARCHIVE_SHA256 and
                receipt["members"] == inventory, "Receipt disagreement")
        receipt_verified = True
    return {"verdict": "PASS", "archive_bytes": ARCHIVE_BYTES,
            "archive_sha256": ARCHIVE_SHA256, "members": inventory,
            "receipt_verified": receipt_verified,
            "scope": "Exact data-only author archive identity and inventory; no mathematical execution"}


def main():
    require(len(sys.argv) in (2, 3), "Expected AUTHOR.zip and optional FREEZE_RECEIPT.json")
    result = verify(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(json.dumps({"verdict": "FAIL", "error": str(error)}, sort_keys=True))
        sys.exit(1)
