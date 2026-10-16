#!/usr/bin/env python3
"""Build a closed deterministic ZIP from the strictly verified allowlist."""
import argparse, io, zipfile
from kit_common import ROOT, ARCHIVE, FIXED_TIME, safe_output, regular, emit, sha
from verify_package import verify

def archive_bytes():
    verify(check_archive=False, check_deposit=False)
    from kit_common import members
    names = sorted(members() + ["SUPPORT_MANIFEST.json"])
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9, strict_timestamps=True) as z:
        for name in names:
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, regular(ROOT / name).read_bytes(), compresslevel=9)
    return stream.getvalue()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    args = p.parse_args()
    out = safe_output(args.output)
    data = archive_bytes()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    emit({"passed": True, "archive_bytes": len(data), "archive_sha256": sha(data)})
if __name__ == "__main__":
    main()
