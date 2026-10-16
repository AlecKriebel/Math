"""Build the exact PR781 preprint deposit from a closed, pinned source tree."""
from pathlib import Path, PurePosixPath
import argparse, datetime, hashlib, io, json, os, stat, sys, tempfile, zipfile
sys.dont_write_bytecode = True

def need(condition, message):
    if not condition:
        raise ValueError(message)

def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON key: " + key)
        result[key] = value
    return result

def reject_constant(value):
    raise ValueError("Nonfinite JSON: " + value)

def parse(raw):
    return json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)

def identity(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()

def safe_name(name):
    need(isinstance(name, str) and name and not PurePosixPath(name).is_absolute()
         and "\\" not in name and all(p not in ("", ".", "..") for p in name.split("/"))
         and str(PurePosixPath(name)) == name, "Unsafe relative path: " + str(name))
    return name

def regular(path):
    need(stat.S_ISREG(path.lstat().st_mode), "Nonregular input: " + str(path))
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as stream:
        need(stat.S_ISREG(os.fstat(stream.fileno()).st_mode),
             "Nonregular opened input: " + str(path))
        return stream.read()

def inventory(root):
    need(not root.is_symlink() and root.is_dir(), "Source must be a directory")
    files, directories = {}, set()
    for path in root.rglob("*"):
        need(not path.is_symlink(), "Source symlink: " + str(path))
        name = safe_name(path.relative_to(root).as_posix())
        if path.is_dir():
            directories.add(name)
        else:
            files[name] = regular(path)
    expected = {p.as_posix() for name in files for p in Path(name).parents if p.as_posix() != "."}
    need(directories == expected, "Unexpected empty source directory")
    return files

def closed_source(root, pin):
    need(isinstance(pin, str) and len(pin) == 64 and all(c in "0123456789abcdef" for c in pin),
         "An external SHA256 manifest pin is required")
    files = inventory(root)
    need(identity(files["MANIFEST.json"])["sha256"] == pin, "External source manifest pin mismatch")
    manifest = parse(files["MANIFEST.json"])
    need(manifest["schema"] == "pr781-closed-source/v1", "Wrong manifest schema")
    expected = {}
    for row in manifest["files"]:
        name = safe_name(row["path"])
        need(name != "MANIFEST.json" and name not in expected, "Repeated/self inventory name")
        need(set(row) == {"path", "bytes", "sha256"}, "Malformed source entry")
        expected[name] = {"bytes": row["bytes"], "sha256": row["sha256"]}
    need(set(files) == set(expected) | {"MANIFEST.json"}, "Closed source inventory differs")
    for name, value in expected.items():
        need(identity(files[name]) == value, "Source bytes differ: " + name)
    return files

def archive(files):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for name, raw in sorted(files.items()):
            item = zipfile.ZipInfo(safe_name(name), date_time=(2026, 10, 16, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            bundle.writestr(item, raw, compresslevel=9)
    return output.getvalue()

def validate_outputs(output, names, source, pdf):
    # Inspect lexical ancestors before resolution can hide a symlink.
    output = output.absolute()
    targets = [output / safe_name(name) for name in names]
    directories = {output}
    for target in targets:
        directories.update(target.parents)
    for directory in sorted(directories, key=lambda p: len(p.parts)):
        need(not directory.is_symlink(), "Output ancestor symlink")
        need(not directory.exists() or directory.is_dir(), "Output parent is not a directory")
    canonical, closed = output.resolve(), source.resolve()
    need(canonical != closed and closed not in canonical.parents, "Output lies inside closed source")
    protected = set()
    for path in list(source.rglob("*")) + [pdf]:
        if path.is_file():
            value = path.stat()
            protected.add((value.st_dev, value.st_ino))
    for target in targets:
        need(not target.is_symlink(), "Output destination symlink")
        resolved = target.resolve()
        need(canonical in resolved.parents and resolved != closed and closed not in resolved.parents,
             "Output target escapes or aliases closed source")
        if target.exists():
            value = target.stat()
            need(stat.S_ISREG(value.st_mode) and value.st_nlink == 1, "Nonregular/multiply linked output")
            need((value.st_dev, value.st_ino) not in protected, "Output aliases a protected input")
    return canonical

def atomic_write(path, raw):
    fd, temporary = tempfile.mkstemp(prefix=".pr781-build-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    finally:
        if os.path.lexists(temporary):
            os.unlink(temporary)

def build(source, pin, pdf_path, output):
    payload = closed_source(source, pin)
    pdf = regular(pdf_path)
    need(pdf.startswith(b"%PDF-"), "Missing PDF signature")
    bindings = parse(payload["PREPRINT_BINDINGS.json"])
    need(identity(pdf) == bindings["paper.pdf"], "PDF differs from exact reviewed binding")
    need(identity(payload["paper.tex"]) == bindings["paper.tex"], "TeX binding differs")
    metadata = parse(payload["zenodo-metadata.json"])["metadata"]
    need(metadata["title"] == "An effective criterion for prescribed block-code extensions"
         and metadata["version"] == "1.0" and metadata["publication_type"] == "preprint",
         "Wrong release metadata")
    source_zip = archive(payload)
    deposit = {"metadata": metadata, "files": [
        {"path": "output/pdf/paper.pdf", "name": "paper.pdf"},
        {"path": "source-and-verification.zip", "name": "source-and-verification.zip"}]}
    flat = {"metadata": metadata, "files": [
        {"path": "paper.pdf"}, {"path": "source-and-verification.zip"}]}
    outputs = {"paper.tex": payload["paper.tex"], "output/pdf/paper.pdf": pdf,
               "source-and-verification.zip": source_zip,
               "zenodo-deposit.json": json_bytes(deposit),
               "zenodo-metadata.json": payload["zenodo-metadata.json"],
               "zenodo-upload-kit.zip": archive({
                   "paper.pdf": pdf, "source-and-verification.zip": source_zip,
                   "zenodo-deposit.json": json_bytes(flat),
                   "zenodo-metadata.json": payload["zenodo-metadata.json"],
                   "README.md": b"Upload only paper.pdf and source-and-verification.zip with the exact enclosed metadata. This outer ZIP is a convenience kit. See the source README for credited dependencies, verification and review limits.\n"})}
    names = list(outputs) + ["RELEASE_INVENTORY.json"]
    out = validate_outputs(output, names, source, pdf_path)
    result = {"schema": "pr781-release-inventory/v1", "source_manifest_sha256": pin,
              "source_files_including_manifest": len(payload),
              "files": [{"path": name, **identity(raw)} for name, raw in outputs.items()]}
    out.mkdir(parents=True, exist_ok=True)
    for name in names:
        (out / name).parent.mkdir(parents=True, exist_ok=True)
    for name, raw in outputs.items():
        atomic_write(out / name, raw)
    atomic_write(out / "RELEASE_INVENTORY.json", json_bytes(result))
    need(inventory(source) == payload, "Closed source changed during rebuild")
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).absolute().parent)
    parser.add_argument("--expected-manifest-sha256", required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.source.absolute(), args.expected_manifest_sha256,
                   args.pdf.absolute(), args.output_dir.absolute())
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
