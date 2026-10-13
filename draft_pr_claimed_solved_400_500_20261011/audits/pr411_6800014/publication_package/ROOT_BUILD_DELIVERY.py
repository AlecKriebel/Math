#!/usr/bin/env python3
"""Build the positive PR411 delivery packet; no native writes or mathematical certification."""
import hashlib
import json
import os
from pathlib import Path
import stat
import zipfile
from datetime import datetime, timezone

HERE = Path(__file__).absolute().parent
CASE = HERE.parent
PACKET = CASE / "prepared_packet"
PREFIX = "unsolved_math_prioritization/attempts/6800014/"

PUBLICATION = """# Local Ricci-pinching maxima on an almost-abelian group

Alec Kriebel — independent researcher; ORCID https://orcid.org/0009-0001-9320-500X.
Research note, 13 October 2026 (UTC).

The [six-page preprint](preprint/local_ricci_pinching_maxima.pdf) gives an explicit negative answer to the literal fixed-group assertion in [Morgan–Pansu Question 14, section 11](https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf#page=12). For the known five-dimensional family A_u = J ⊕ uE₁₂, every parameter 0 < u < 1/2 has a standard metric that is a non-strict local maximum of F = Scal²/||Ric||² with value 1/3 among all nearby left-invariant metrics on the fixed simply connected group. Its Ricci endomorphism fails Ric = cI + D with D a derivation of that group's Lie algebra. An explicit metric on the same group has F = 9/17, so this local maximum is not global. The proof covers the full metric Gram matrix and unrestricted cross-block, with a uniform cubic remainder along the flat family; the Hessian alone is insufficient. Neither endpoint is included.

The metric is nevertheless a geometric Ricci soliton, isometric to R² × H₃. A solvsoliton presentation on another transitive group does not meet the derivation assertion for the original fixed group.

Lauret's [23 July 2018 talk](https://www.ime.usp.br/~mtg/slides/j_lauret.pdf) already announces the relevant negative existence result. The family and value 1/3 are prior Lauret–Will work. The actually inspected arXiv versions [I v1](https://arxiv.org/abs/1808.01380v1) and [I v2](https://arxiv.org/abs/1808.01380v2) leave positive small-parameter local maximality unknown. The chronology does not establish withdrawal or falsity of the earlier announcement. Final journal full texts were inaccessible and are not attested. This is an attributed explicit proof note; it claims no novelty, first assertion, first proof, or current community-open status. Its bibliography and bounded priority qualifications are in the paper and verification materials.

AI tools were used extensively in solving, symbolic computation, source review, drafting, and adversarial verification. The preprint is unrefereed and has received no external human peer review. Machine-agent reviews are not human refereeing.

## Files and reproduction

- [Standalone TeX](preprint/local_ricci_pinching_maxima.tex) and [source ZIP](preprint/local_ricci_pinching_maxima_source.zip): source, build instructions, and a byte manifest. Compiler versions can change PDF serialization; the distributed PDF has its own exact hash.
- [Verification ZIP](preprint/local_ricci_pinching_maxima_verification.zip): 100 members, comprising the intact 73-file version-2 core, 25 selected complete review/check artifacts, a README and support manifest. The selections outside the core do not represent the entire sealed review corpus or redistribute third-party primary-source PDFs. Historical and private case-relative references are identified in the support README.
- [Version-2 instructions](verification_v2/README.md): 54 mandatory evaluations of 39 preserved predicates in normal and optimized Python, exact input custody, and corruption controls. Run `python -B verification_v2/run_all.py` and `python -B -O verification_v2/run_all.py` in an environment containing the recorded SymPy version. The ZIP also includes exact standard-library rational curvature and boundary checks.
- [Proposed preprint metadata](preprint/ZENODO_METADATA.json) and [delivery manifest](DELIVERY_MANIFEST.json): exact bytes, source origins and Git modes. Actual production DOI and tracker receipts are recorded separately after publication; the proposed metadata is not a publication receipt.

The original mathematical proofs and historical audit are preserved. Current prose addenda correct status/version interpretations and prior-source credit. The three current checkers preserve their original mathematical predicates in mandatory branches. Original historical optimized assertion outputs remain uncertified, and two absent historical byte objects remain unattested. Historical component conclusions are distinct from later complete-package reviews.

The selected source row is `claimed_solved` with author turns `2/5`; editorial, verification and publication work adds zero substantive author proof-search turns. The result is the explicit negative answer stated above, with the priority qualifications already disclosed. This delivery packet covers only problem 6800014.
"""


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def read(path):
    path = Path(path).absolute()
    need(path.is_relative_to(CASE), "outside case")
    for ancestor in [path, *path.parents]:
        need(not ancestor.is_symlink(), "symlink ancestor")
    need(stat.S_ISREG(path.lstat().st_mode), "nonregular file")
    return path.read_bytes()


def inventory(root):
    need(root.is_dir() and not root.is_symlink(), "bad directory")
    found = {}
    for parent, dirs, files in os.walk(root, followlinks=False):
        for name in dirs:
            p = Path(parent) / name
            need(stat.S_ISDIR(p.lstat().st_mode) and not p.is_symlink(), "special directory")
        for name in files:
            p = Path(parent) / name
            found[p.relative_to(root).as_posix()] = read(p)
    return found


def main():
    need(not PACKET.exists(), "delivery packet already exists; preserve prior packet")
    final_seal = read(HERE / "SUPPORT_ASSEMBLY_FINAL_SEAL.json")
    assembly = json.loads(read(HERE / "SUPPORT_ASSEMBLY_RESULTS.json"))
    need(assembly["result"] == "PASS", "assembly did not pass")
    core = inventory(CASE / "verification_v2")
    author = inventory(CASE / "global_candidate_v2/author_packet")
    need(len(core) == 73 and len(author) == 19, "unexpected accepted component counts")
    support = inventory(HERE / "support")
    source = inventory(HERE / "source_bundle")
    need(len(support) == 100 and len(source) == 3, "unexpected support/source counts")
    for name, data in core.items():
        need(support["verification_v2/" + name] == data, "core copy differs")
    manifest = json.loads(support["SUPPORT_MANIFEST.json"])
    # The producer schema supplies exact member pins; compare all names and bytes independently below.
    need(isinstance(manifest, dict), "invalid support manifest")
    archive_checks = []
    for name, expected in (("local_ricci_pinching_maxima_source.zip", source),
                           ("local_ricci_pinching_maxima_verification.zip", support)):
        p = HERE / "assets" / name
        raw = read(p)
        with zipfile.ZipFile(p) as archive:
            entries = archive.infolist()
            names = [x.filename for x in entries]
            need(names == sorted(expected) and len(names) == len(set(names)), "archive member inventory differs")
            need(not archive.comment, "archive comment")
            for entry in entries:
                need(not entry.is_dir() and entry.create_system == 3
                     and stat.S_ISREG(entry.external_attr >> 16)
                     and stat.S_IMODE(entry.external_attr >> 16) == 0o644
                     and not entry.flag_bits & 1 and not entry.extra and not entry.comment
                     and entry.date_time == (1980, 1, 1, 0, 0, 0), "unexpected ZIP member metadata")
                need(archive.read(entry) == expected[entry.filename], "archive member bytes differ")
        archive_checks.append({"name": name, "members": len(expected), "sha256": digest(raw)})
    contents = {name: (data, "global_candidate_v2/author_packet/" + name) for name, data in author.items()}
    contents.update({"verification_v2/" + name: (data, "verification_v2/" + name) for name, data in core.items()})
    for name in ("local_ricci_pinching_maxima.pdf", "local_ricci_pinching_maxima_source.zip",
                 "local_ricci_pinching_maxima_verification.zip"):
        contents["preprint/" + name] = (read(HERE / "assets" / name), "publication_package/assets/" + name)
    tex = read(HERE / "paper/local_ricci_pinching_maxima.tex")
    pdf = read(HERE / "paper/local_ricci_pinching_maxima.pdf")
    need(digest(tex) == "8bcaec828c6c40fb990ce92ed1cf36f7fbdb643546168fb5f4d884c75db41c72"
         and digest(pdf) == "13d6fcdb924ea1461a6c44d4bb4e6aec1f278598218f8a34f26252d52ca0d37b"
         and contents["preprint/local_ricci_pinching_maxima.pdf"][0] == pdf
         and source["local_ricci_pinching_maxima.tex"] == tex, "reviewed paper bytes differ")
    contents["preprint/local_ricci_pinching_maxima.tex"] = (tex, "publication_package/paper/local_ricci_pinching_maxima.tex")
    metadata = read(CASE / "publication_preparation/PROPOSED_ZENODO_METADATA.json")
    need(len(json.loads(metadata)) == 12, "proposed metadata field count differs")
    contents["preprint/ZENODO_METADATA.json"] = (metadata, "publication_preparation/PROPOSED_ZENODO_METADATA.json")
    contents["PUBLICATION.md"] = (PUBLICATION.encode(), "publication_package/ROOT_BUILD_DELIVERY.py:PUBLICATION")
    need(len(contents) == 98, "unexpected delivery payload count")
    # 19 + 73 + 5 preprint files + PUBLICATION = 98; manifest is the 99th file.
    delivery = {"schema": "pr411-positive-delivery-v1", "time_utc": datetime.now(timezone.utc).isoformat(),
                "source_head": "ac8b960bdda61c154cc30d7e3aba70389a9b139e",
                "scope": "Only problem 6800014; local packaging evidence, not complete-package acceptance",
                "support_assembly_seal_sha256": digest(final_seal), "archive_readback": archive_checks,
                "author_turns": "2/5", "new_author_proof_search_turns": 0,
                "files": [{"path": name, "remote_path": PREFIX + name, "origin": origin,
                           "size": len(data), "sha256": digest(data), "blob_sha": blob(data), "mode": "100644"}
                          for name, (data, origin) in sorted(contents.items())],
                "self_exclusion": "DELIVERY_MANIFEST.json is bound by the external packet seal and exact updater map"}
    contents["DELIVERY_MANIFEST.json"] = (encoded(delivery), "publication_package/ROOT_BUILD_DELIVERY.py:generated_manifest")
    PACKET.mkdir()
    for name, (data, _) in sorted(contents.items()):
        target = PACKET / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(data)
        target.chmod(0o644)
    actual = inventory(PACKET)
    need(actual == {name: data for name, (data, _) in contents.items()}, "delivery readback differs")
    seal = {"schema": "pr411-delivery-external-seal-v1", "time_utc": datetime.now(timezone.utc).isoformat(),
            "result": "PASS_LOCAL_BYTE_ASSEMBLY", "whole_package_acceptance": "SEPARATE",
            "builder_sha256": digest(read(Path(__file__))), "support_assembly_seal_sha256": digest(final_seal),
            "files": [{"path": name, "size": len(data), "sha256": digest(data), "blob_sha": blob(data), "mode": "100644"}
                      for name, data in sorted(actual.items())]}
    with (HERE / "ROOT_DELIVERY_SEAL.json").open("xb") as stream:
        stream.write(encoded(seal))
    print(json.dumps({"payload_files": len(actual), "seal_sha256": digest(encoded(seal)), "archive_readback": archive_checks}))


if __name__ == "__main__":
    main()
