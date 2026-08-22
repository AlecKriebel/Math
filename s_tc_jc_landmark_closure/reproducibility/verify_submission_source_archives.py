#!/usr/bin/env python3
"""Rebuild every submission PDF from the instructions inside its source ZIP.

This is intentionally an extracted-archive test.  It does not import either
package builder, and it executes the documented archive-local shell commands
verbatim before comparing the resulting PDFs byte for byte with the delivered
files.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile


PROJECT = Path(__file__).resolve().parents[1]
SOURCE_DATE_EPOCH = "1786924800"


PACKAGES = (
    {
        "name": "biorxiv",
        "zip": PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_source.zip",
        "root": Path("."),
        "anchor": "From the root of the extracted bioRxiv source ZIP",
        "outputs": {
            "paper/main.pdf": PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC.pdf",
            "supplement/supplement.pdf": PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf",
        },
    },
    {
        "name": "systematic_biology",
        "zip": PROJECT / "journal_submission/systematic_biology/SB_LaTeX_Source.zip",
        "root": Path("SB_LaTeX_Source"),
        "anchor": "From this extracted source directory",
        "outputs": {
            "paper/main.pdf": PROJECT / "journal_submission/systematic_biology/SB_Main_Manuscript.pdf",
            "supplement/supplement.pdf": PROJECT / "journal_submission/systematic_biology/SB_Supplementary_Material.pdf",
        },
    },
    {
        "name": "journal_of_mathematical_biology",
        "zip": PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_LaTeX_Source.zip",
        "root": Path("JMB_LaTeX_Source"),
        "anchor": "From this extracted source directory",
        "outputs": {
            "paper/main.pdf": PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_Main_Manuscript.pdf",
            "supplement/supplement.pdf": PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_Supplementary_Information.pdf",
        },
    },
)

COVER_LETTERS = (
    (
        PROJECT / "journal_submission/systematic_biology/SB_Cover_Letter.tex",
        PROJECT / "journal_submission/systematic_biology/SB_Cover_Letter.pdf",
    ),
    (
        PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_Cover_Letter.tex",
        PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_Cover_Letter.pdf",
    ),
)

VERIFIER_CAPSULES = (
    PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_verifier_entrypoints.zip",
    PROJECT / "journal_submission/systematic_biology/SB_Exact_Verifier_Entry_Points.zip",
    PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_Exact_Verifier_Entry_Points.zip",
)

# This list is deliberately repeated here rather than imported from the
# capsule builder.  The replay verifier must reject a self-consistent capsule
# that silently omits one of the promised entry points.
VERIFIER_CAPSULE_MEMBER_SET = frozenset({
    "README_FIRST.md",
    "SHA256SUMS",
    "CERTIFICATE_BUNDLE_ENVELOPE.json",
    "THEOREM_CERTIFICATE_CROSSWALK.md",
    "RUNTIME_AND_HARDWARE.md",
    "verify_downloaded_archive.py",
})

PACKAGE_MANIFESTS = {
    PROJECT / "biorxiv_submission": frozenset({
        "Strong_Tree_Childness_Sharp_Level2_JC.pdf",
        "Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf",
        "Strong_Tree_Childness_Sharp_Level2_JC_source.zip",
        "Strong_Tree_Childness_Sharp_Level2_JC_verifier_entrypoints.zip",
        "BIORXIV_METADATA.md", "BIORXIV_UPLOAD_MAP.md",
        "FINAL_HUMAN_CHECKLIST.md",
    }),
    PROJECT / "journal_submission/systematic_biology": frozenset({
        "SB_Main_Manuscript.pdf", "SB_Supplementary_Material.pdf",
        "SB_LaTeX_Source.zip", "SB_Cover_Letter.tex",
        "SB_Cover_Letter.pdf", "SB_Exact_Verifier_Entry_Points.zip",
        "SB_SUBMISSION_METADATA.md", "SYSTEMATIC_BIOLOGY_UPLOAD_MAP.md",
        "FINAL_HUMAN_CHECKLIST.md",
    }),
    PROJECT / "journal_submission/journal_of_mathematical_biology": frozenset({
        "JMB_Main_Manuscript.pdf", "JMB_Supplementary_Information.pdf",
        "JMB_LaTeX_Source.zip", "JMB_Cover_Letter.tex",
        "JMB_Cover_Letter.pdf", "JMB_Exact_Verifier_Entry_Points.zip",
        "JMB_SUBMISSION_METADATA.md", "JMB_UPLOAD_MAP.md",
        "FINAL_HUMAN_CHECKLIST.md",
    }),
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_outer_manifest(directory: Path, expected_names: frozenset[str]) -> None:
    manifest_path = directory / "SHA256SUMS"
    require(manifest_path.is_file(), f"package manifest missing: {directory}")
    records: dict[str, str] = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", line)
        require(match is not None,
                f"malformed package checksum: {directory}:{line}")
        value, name = match.groups()
        require(name not in records,
                f"duplicate package checksum: {directory}:{name}")
        records[name] = value
    require(set(records) == expected_names,
            f"package manifest file set differs: {directory}")
    for name, value in records.items():
        target = directory / name
        require(target.is_file(), f"manifested package file missing: {target}")
        require(digest(target) == value, f"package checksum differs: {target}")


def mutation_test_outer_manifest() -> None:
    """A manifest that drops the verifier capsule must fail closed."""
    with tempfile.TemporaryDirectory(prefix="stc-jc-manifest-mutation-") as name:
        directory = Path(name)
        article = directory / "article.pdf"
        capsule = directory / "verifier.zip"
        article.write_bytes(b"article")
        capsule.write_bytes(b"capsule")
        manifest = directory / "SHA256SUMS"
        manifest.write_text(
            f"{digest(article)}  {article.name}\n"
            f"{digest(capsule)}  {capsule.name}\n",
            encoding="utf-8",
        )
        expected = frozenset({article.name, capsule.name})
        verify_outer_manifest(directory, expected)
        manifest.write_text(
            f"{digest(article)}  {article.name}\n", encoding="utf-8"
        )
        try:
            verify_outer_manifest(directory, expected)
        except AssertionError:
            return
        raise AssertionError("capsule-omitting package manifest mutation escaped")


def safe_extract(archive_path: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        require(names, f"empty source archive: {archive_path}")
        for name in names:
            candidate = Path(name)
            require(not candidate.is_absolute() and ".." not in candidate.parts,
                    f"unsafe ZIP member: {archive_path}: {name}")
            data = archive.read(name)
            if Path(name).suffix.lower() in {".md", ".tex", ".bib", ".sty", ".cls"}:
                text = data.decode("utf-8")
                for leaked in ("/Users/", "/private/tmp/", "file://"):
                    require(leaked not in text,
                            f"local path leaked into {archive_path.name}:{name}")
        archive.extractall(destination)


def documented_commands(build_text: str, anchor: str) -> str:
    require(anchor in build_text, f"archive-local build anchor missing: {anchor}")
    suffix = build_text.split(anchor, 1)[1]
    match = re.search(r"```bash\s*\n(.*?)```", suffix, flags=re.DOTALL)
    require(match is not None, f"archive-local bash block missing after: {anchor}")
    commands = match.group(1).strip()
    require(commands == (
        "export SOURCE_DATE_EPOCH=1786924800\n"
        "cd paper\n"
        "tectonic main.tex\n"
        "cd ../supplement\n"
        "tectonic supplement.tex"
    ), f"unexpected archive-local commands after {anchor}: {commands!r}")
    return commands


def verify_package(spec: dict[str, object]) -> dict[str, str]:
    archive_path = spec["zip"]
    assert isinstance(archive_path, Path)
    require(archive_path.is_file(), f"source archive missing: {archive_path}")
    env = os.environ.copy()
    env.pop("SOURCE_DATE_EPOCH", None)
    with tempfile.TemporaryDirectory(prefix=f"stc-jc-source-replay-{spec['name']}-") as name:
        extracted = Path(name)
        safe_extract(archive_path, extracted)
        root = extracted / spec["root"]
        assert isinstance(root, Path)
        build = root / "BUILD.md"
        require(build.is_file(), f"archive BUILD.md missing: {archive_path}")
        commands = documented_commands(build.read_text(encoding="utf-8"), spec["anchor"])
        subprocess.run(
            ["/bin/bash", "-euo", "pipefail", "-c", commands],
            cwd=root,
            env=env,
            check=True,
        )
        hashes: dict[str, str] = {}
        outputs = spec["outputs"]
        assert isinstance(outputs, dict)
        for relative, expected in outputs.items():
            rebuilt = root / relative
            assert isinstance(expected, Path)
            require(rebuilt.is_file(), f"documented command did not build: {relative}")
            rebuilt_hash = digest(rebuilt)
            expected_hash = digest(expected)
            require(rebuilt_hash == expected_hash,
                    f"extracted-source replay differs: {spec['name']}:{relative}")
            hashes[relative] = rebuilt_hash
        return hashes


def verify_cover_letter(source: Path, expected: Path) -> str:
    require(source.is_file() and expected.is_file(),
            f"cover-letter source/PDF missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    for leaked in ("/Users/", "/private/tmp/", "file://"):
        require(leaked not in source_text, f"local path leaked into {source}")
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = SOURCE_DATE_EPOCH
    with tempfile.TemporaryDirectory(prefix="stc-jc-cover-replay-") as name:
        root = Path(name)
        copied = root / source.name
        shutil.copyfile(source, copied)
        subprocess.run(["tectonic", copied.name], cwd=root, env=env, check=True)
        rebuilt = copied.with_suffix(".pdf")
        require(digest(rebuilt) == digest(expected),
                f"cover-letter replay differs: {source.name}")
    return digest(expected)


def verify_verifier_capsule(path: Path) -> str:
    require(path.is_file(), f"verifier-entrypoint capsule missing: {path}")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        require(names and len(names) == len(set(names)),
                f"empty or duplicate verifier capsule members: {path}")
        require(set(names) == VERIFIER_CAPSULE_MEMBER_SET,
                f"verifier capsule mandatory member set differs: {path}")
        readme = archive.read("README_FIRST.md").decode("utf-8")
        for needle in (
            "navigation capsule only",
            "not the proof archive",
            "stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz",
            "bash verify.sh quick",
            "bash verify.sh full",
            "bash verify.sh regenerate-all",
            "No included script uploads files",
        ):
            require(needle in readme, f"verifier capsule README missing: {needle}")
        expected: dict[str, str] = {}
        for line in archive.read("SHA256SUMS").decode("utf-8").splitlines():
            match = re.fullmatch(r"([0-9a-f]{64})  ([^/].*)", line)
            require(match is not None, f"malformed capsule checksum: {line}")
            value, name = match.groups()
            require(name not in expected, f"duplicate capsule checksum: {name}")
            expected[name] = value
        require(set(expected) == set(names) - {"SHA256SUMS"},
                f"capsule checksum coverage differs: {path}")
        for name, value in expected.items():
            require(hashlib.sha256(archive.read(name)).hexdigest() == value,
                    f"capsule member checksum differs: {path}:{name}")
    return digest(path)


def mutation_test_verifier_capsule_member() -> None:
    """A re-sealed capsule missing one mandatory entry point must fail."""
    source = VERIFIER_CAPSULES[0]
    require(source.is_file(), f"verifier capsule missing before mutation: {source}")
    with zipfile.ZipFile(source) as archive:
        payloads = {
            name: archive.read(name)
            for name in archive.namelist()
            if name != "SHA256SUMS"
        }
    removed = "verify_downloaded_archive.py"
    require(removed in payloads, f"mutation target missing: {removed}")
    del payloads[removed]
    internal_sums = "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n"
        for name, data in payloads.items()
    ).encode("utf-8")
    with tempfile.TemporaryDirectory(prefix="stc-jc-capsule-mutation-") as name:
        mutated = Path(name) / "mutated_capsule.zip"
        with zipfile.ZipFile(mutated, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for member, data in payloads.items():
                archive.writestr(member, data)
            archive.writestr("SHA256SUMS", internal_sums)
        try:
            verify_verifier_capsule(mutated)
        except AssertionError:
            return
    raise AssertionError("mandatory-member capsule mutation escaped")


def main() -> None:
    if shutil.which("tectonic") is None and not Path("/opt/homebrew/bin/tectonic").is_file():
        raise RuntimeError("Tectonic is required for extracted-source replay")
    # Make the archive's literal `tectonic` command portable on the standard
    # local setup even when Homebrew is not already in PATH.
    if shutil.which("tectonic") is None:
        os.environ["PATH"] = f"/opt/homebrew/bin:{os.environ.get('PATH', '')}"
    mutation_test_outer_manifest()
    for directory, expected_names in PACKAGE_MANIFESTS.items():
        verify_outer_manifest(directory, expected_names)
    mutation_test_verifier_capsule_member()
    records = {str(spec["name"]): verify_package(spec) for spec in PACKAGES}
    covers = {
        source.name: verify_cover_letter(source, expected)
        for source, expected in COVER_LETTERS
    }
    capsules = {path.name: verify_verifier_capsule(path) for path in VERIFIER_CAPSULES}
    require(len(set(capsules.values())) == 1,
            "submission-support verifier capsules are not byte-identical")
    print("VERIFIED: source ZIPs reproduce six article/supplement PDFs; "
          "standalone TeX reproduces two cover-letter PDFs")
    for package, outputs in records.items():
        for relative, value in sorted(outputs.items()):
            print(f"{package}:{relative} {value}")
    for name, value in sorted(covers.items()):
        print(f"cover:{name} {value}")
    for name, value in sorted(capsules.items()):
        print(f"verifier_capsule:{name} {value}")


if __name__ == "__main__":
    main()
