#!/usr/bin/env python3
"""Read-only package integrity/metadata audit; writes only adjacent receipts.

Run with the bundled Python runtime (pypdf required). Does not execute any
package code, extract the archive, mutate the package, or contact a network.
"""
import ast
import datetime
import hashlib
import json
import os
import pathlib
import re
import stat
import unicodedata
import zipfile

from pypdf import PdfReader

OUT = pathlib.Path(__file__).resolve().parent
PROJECT = OUT.parents[2]
PACKET = PROJECT / "reviews/package_v3"
SOURCE = PACKET / "source-and-verification"
BUILDER = PROJECT / "checks/build_publication_package.py"
EXPECTED_PAYLOAD = {
    "main.tex", "references.bib", "README.md", "REPRODUCE.md", "LICENSE.txt",
    "DEPENDENCY_LEDGER.md", "PRIORITY_AUDIT.md", "PRIORITY_SEARCH_LOG.json",
    "PINNED_SOURCE.json", "SUPPLEMENT_PAIR_IDENTITY.md",
    "SUPPLEMENT_TRANSFER_LEMMA.md", "SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md",
    "SUPPLEMENT_LOCAL_THEORY.md", "exact_kernel_certificate.py",
    "rational_selection_certificate.py", "verify_pair_identity.py",
    "FORMAL_SCOPE_AUDIT.md", "FORMAL_BUILD_LIMITATIONS.json",
    "PRIMARY_REFERENCE_PROVENANCE.md", "ARCHIVE_MAP.json",
    "PRELIMINARY_PRIORITY_AUDIT.md", "PRELIMINARY_PRIORITY_SEARCH_LOG.json",
    "SUPPLEMENT_OCCUPATION_AUDIT.md", "FORMAL_SOURCE_INVENTORY.json",
    "FORMAL_STATIC_SCAN.json", "ORIGINAL_CONTINUATION_ATTRIBUTION.json",
}
EXPECTED_SOURCE = EXPECTED_PAYLOAD | {"SHA256SUMS.json"}
EXPECTED_PACKET = {f"source-and-verification/{n}" for n in EXPECTED_SOURCE} | {
    "upload-kit/paper.pdf", "upload-kit/source-and-verification.zip",
    "upload-kit/README.md", "zenodo-deposit.json", "REVIEW_INVENTORY.json",
}
EXPECTED_AUTHOR = "Alec Kriebel"
EXPECTED_ORCID = "0009-0001-9320-500X"
EXPECTED_TITLE = "Signed impulse estimates and global smooth solutions for finite multispecies relativistic Vlasov-Maxwell"
EXPECTED_PDF_SHA256 = "20581b8b253c470d9fd775f88931002fc99729b7d7db21da5e6274482c5b990a"
EXPECTED_ZIP_SHA256 = "b14fa882d987ef6b168b9b821c86b1685f4e6abcd7540837e9f3afa9c0cff527"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def normalized(value):
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("--", "-")
    value = re.sub("[\u2010-\u2015]", "-", value)
    return " ".join(value.split())

def command_arg(text, command):
    match = re.search(re.escape(command) + r"\s*\{", text)
    if not match:
        raise ValueError(f"Missing {command}")
    start = match.end()
    depth = 1
    for index in range(start, len(text)):
        if text[index] == "{" and (index == 0 or text[index - 1] != "\\"):
            depth += 1
        if text[index] == "}" and (index == 0 or text[index - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return text[start:index]
    raise ValueError(f"Unbalanced {command}")

def compare_sets(actual, expected):
    return {"pass": actual == expected, "missing": sorted(expected - actual),
            "extra": sorted(actual - expected)}

start = datetime.datetime.now(datetime.timezone.utc).isoformat()
checks = {}
issues = []
notes = []
advisories = []
initial = {}
fs_anomalies = []
empty_dirs = []
for root, dirs, files in os.walk(PACKET, followlinks=False):
    root = pathlib.Path(root)
    if root != PACKET and not dirs and not files:
        empty_dirs.append(str(root.relative_to(PACKET)))
    for name in dirs + files:
        path = root / name
        mode = path.lstat().st_mode
        relative = str(path.relative_to(PACKET))
        if stat.S_ISLNK(mode) or not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            fs_anomalies.append({"path": relative, "mode": oct(mode)})
        if stat.S_ISREG(mode):
            data = path.read_bytes()
            initial[relative] = {"bytes": len(data), "sha256": sha(data)}

checks["packet_exact_file_whitelist"] = compare_sets(set(initial), EXPECTED_PACKET)
checks["filesystem_regular_files_only"] = {
    "pass": not fs_anomalies and not empty_dirs,
    "anomalies": fs_anomalies, "unexpected_empty_directories": empty_dirs,
}
builder_ast = ast.parse(BUILDER.read_text())
builder_files = next(ast.literal_eval(node.value) for node in builder_ast.body
    if isinstance(node, ast.Assign)
    and any(isinstance(target, ast.Name) and target.id == "files" for target in node.targets))
checks["builder_allowlist_matches_independent_whitelist"] = compare_sets(set(builder_files), EXPECTED_PAYLOAD - {"ARCHIVE_MAP.json"})
checks["source_directory_exact_whitelist"] = compare_sets(
    {str(p.relative_to(SOURCE)) for p in SOURCE.rglob("*") if p.is_file()}, EXPECTED_SOURCE)
json_duplicate_keys = []
def json_pairs_no_duplicates(pairs):
    seen = set()
    for key, value in pairs:
        if key in seen:
            json_duplicate_keys.append(key)
        seen.add(key)
    return dict(pairs)
json_duplicate_files = []
for relative in sorted(initial):
    if relative.endswith(".json"):
        previous_count = len(json_duplicate_keys)
        json.loads((PACKET / relative).read_text(), object_pairs_hook=json_pairs_no_duplicates)
        if len(json_duplicate_keys) != previous_count:
            json_duplicate_files.append({"file": relative, "duplicate_keys": json_duplicate_keys[previous_count:]})
checks["json_no_duplicate_keys"] = {"pass": not json_duplicate_files, "anomalies": json_duplicate_files,
    "checked": sum(relative.endswith(".json") for relative in initial)}

manifest = json.loads((SOURCE / "SHA256SUMS.json").read_text())
checks["source_manifest_exact_coverage"] = compare_sets(set(manifest), EXPECTED_PAYLOAD)
manifest_mismatches = []
for name, digest in manifest.items():
    actual = initial.get("source-and-verification/" + name, {}).get("sha256")
    if digest != actual or not re.fullmatch("[0-9a-f]{64}", digest):
        manifest_mismatches.append({"path": name, "declared": digest, "actual": actual})
checks["source_manifest_sha256"] = {"pass": not manifest_mismatches, "checked": len(manifest), "mismatches": manifest_mismatches}

inventory = json.loads((PACKET / "REVIEW_INVENTORY.json").read_text())
checks["inventory_exact_coverage"] = compare_sets(set(inventory["files"]), EXPECTED_PACKET - {"REVIEW_INVENTORY.json"})
inventory_mismatches = [
    {"path": name, "declared": expected, "actual": initial.get(name)}
    for name, expected in inventory["files"].items() if expected != initial.get(name)
]
checks["inventory_hashes_and_sizes"] = {"pass": not inventory_mismatches, "checked": len(inventory["files"]), "mismatches": inventory_mismatches}
checks["requested_candidate_pdf_and_zip_hashes"] = {
    "pass": initial["upload-kit/paper.pdf"]["sha256"] == EXPECTED_PDF_SHA256
    and initial["upload-kit/source-and-verification.zip"]["sha256"] == EXPECTED_ZIP_SHA256,
    "expected_pdf_sha256": EXPECTED_PDF_SHA256, "expected_zip_sha256": EXPECTED_ZIP_SHA256}

archive_map = json.loads((SOURCE / "ARCHIVE_MAP.json").read_text())
checks["archive_map_exact_mapped_payload"] = compare_sets(set(archive_map["original_project_paths"]), EXPECTED_PAYLOAD - {"ARCHIVE_MAP.json"})
checks["archive_map_agrees_with_builder_source_paths"] = {
    "pass": archive_map["original_project_paths"] == builder_files,
    "mapped_payload_files": len(archive_map["original_project_paths"])}
map_bad_paths = []
for archive_name, original_name in archive_map["original_project_paths"].items():
    original_path = pathlib.PurePosixPath(original_name)
    if (pathlib.PurePosixPath(archive_name).name != archive_name
            or original_path.is_absolute() or ".." in original_path.parts
            or not (SOURCE / archive_name).is_file()):
        map_bad_paths.append({"archive_file": archive_name, "original_path": original_name})
checks["archive_map_supplied_paths_safe_and_present"] = {"pass": not map_bad_paths, "anomalies": map_bad_paths}
checks["archive_map_omissions_explicit"] = {
    "pass": set(archive_map["omitted_inputs"]) == {"sources/upstream_pinned/", "checks/formal_scope/lean/", "sources/priority_primary/ PDFs"}
    and "excluded" in archive_map["omitted_inputs"]["sources/priority_primary/ PDFs"]
    and "failed build" in archive_map["omitted_inputs"]["checks/formal_scope/lean/"],
    "omitted_inputs": archive_map["omitted_inputs"]}
map_source_comparisons = []
for archive_name, original_name in archive_map["original_project_paths"].items():
    original_path = PROJECT / original_name
    original = original_path.read_bytes()
    expected_copy = original
    if archive_name.endswith(".md"):
        expected_text = original.decode()
        substitutions = {"PAIR_IDENTITY.md": "SUPPLEMENT_PAIR_IDENTITY.md",
            "LOCAL_THEORY.md": "SUPPLEMENT_LOCAL_THEORY.md",
            "UNIFORM_LEMMA_CHAIN.md": "SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md"}
        for old, new in substitutions.items():
            if archive_name != new:
                expected_text = expected_text.replace("`" + old + "`", "`" + new + "`")
        if archive_name == "SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md":
            expected_text = expected_text.replace("`AUDIT.md`", "`SUPPLEMENT_OCCUPATION_AUDIT.md`")
        if archive_name == "FORMAL_SCOPE_AUDIT.md":
            expected_text = "> Archive provenance note: original project paths below identify historical evidence. The provided formal inventory, scan and failed-build receipt use FORMAL_ filenames. The project-local reproduction script and Lean checkout are intentionally excluded; obtain the pinned upstream sources and follow their documented build instructions. No formal build succeeded. See ARCHIVE_MAP.json.\n\n" + expected_text
            for old, new in [("checks/formal_scope/source_inventory.json", "FORMAL_SOURCE_INVENTORY.json"),
                    ("static_scan.json", "FORMAL_STATIC_SCAN.json"),
                    ("build_receipt.json", "FORMAL_BUILD_LIMITATIONS.json")]:
                expected_text = expected_text.replace("`" + old + "`", "`" + new + "`")
        expected_copy = expected_text.encode()
    map_source_comparisons.append({"archive_file": archive_name, "original_path": original_name,
        "original_sha256_now": sha(original), "archive_sha256": sha((SOURCE / archive_name).read_bytes()),
        "expected_copy_sha256": sha(expected_copy), "documented_transform_matches": (SOURCE / archive_name).read_bytes() == expected_copy})
checks["archive_map_current_source_correspondence"] = {
    "pass": all(item["documented_transform_matches"] for item in map_source_comparisons),
    "comparisons": map_source_comparisons,
    "method": "Independent implementation of the documented Markdown basename replacements and formal provenance preface; builder not executed."}

zip_entries = []
zip_unsafe = []
zip_mismatches = []
with zipfile.ZipFile(PACKET / "upload-kit/source-and-verification.zip") as archive:
    infos = archive.infolist()
    names = [item.filename for item in infos]
    checks["zip_exact_whitelist"] = compare_sets(set(names), {"source-and-verification/" + n for n in EXPECTED_SOURCE})
    checks["zip_no_duplicate_entries"] = {"pass": len(names) == len(set(names)), "entries": len(names)}
    checks["zip_crc"] = {"pass": archive.testzip() is None}
    for item in infos:
        mode = item.external_attr >> 16
        path = pathlib.PurePosixPath(item.filename)
        if (not stat.S_ISREG(mode) or item.is_dir() or item.flag_bits & 1
                or path.is_absolute() or ".." in path.parts
                or "\\" in item.filename or "\x00" in item.filename
                or len(path.parts) != 2 or path.parts[0] != "source-and-verification"):
            zip_unsafe.append({"name": item.filename, "mode": oct(mode), "flags": item.flag_bits})
        data = archive.read(item)
        entry = {"name": item.filename, "bytes": len(data), "sha256": sha(data),
                 "mode": oct(mode), "encrypted": bool(item.flag_bits & 1)}
        zip_entries.append(entry)
        expected = initial.get(item.filename)
        if expected != {"bytes": len(data), "sha256": sha(data)}:
            zip_mismatches.append({"path": item.filename, "source": expected, "archive": entry})
checks["zip_safe_regular_unencrypted_entries"] = {"pass": not zip_unsafe, "anomalies": zip_unsafe}
checks["zip_bytes_equal_source"] = {"pass": not zip_mismatches, "checked": len(zip_entries), "mismatches": zip_mismatches}

pdf = PdfReader(PACKET / "upload-kit/paper.pdf")
checks["pdf_not_encrypted"] = {"pass": not pdf.is_encrypted}
checks["pdf_expected_page_count"] = {"pass": len(pdf.pages) == 11, "expected": 11, "actual": len(pdf.pages)}
pdf_texts = [page.extract_text() or "" for page in pdf.pages]
pdf_metadata = {str(k): str(v) for k, v in pdf.metadata.items()}
pdf_uris = []
pdf_active_actions = []
for index, page in enumerate(pdf.pages):
    for annot_ref in page.get("/Annots", []):
        annot = annot_ref.get_object()
        action = annot.get("/A")
        if action:
            action = action.get_object()
            if action.get("/URI"):
                pdf_uris.append(str(action["/URI"]))
            if action.get("/S") in {"/JavaScript", "/Launch"}:
                pdf_active_actions.append({"page": index + 1, "kind": str(action.get("/S"))})
pdf_root = pdf.trailer["/Root"]
unexpected_annotations = [{"page": index + 1, "subtype": str(annotation.get_object().get("/Subtype"))}
    for index, page in enumerate(pdf.pages) for annotation in page.get("/Annots", [])
    if annotation.get_object().get("/Subtype") != "/Link"]
checks["pdf_no_forms_or_nonlink_annotations"] = {
    "pass": not pdf_root.get("/AcroForm") and not unexpected_annotations,
    "has_form_tree": bool(pdf_root.get("/AcroForm")), "unexpected_annotations": unexpected_annotations}
names_dict = pdf_root.get("/Names")
if names_dict:
    names_dict = names_dict.get_object()
pdf_embedded = bool(names_dict and names_dict.get("/EmbeddedFiles")) or bool(pdf_root.get("/AF"))
pdf_script_tree = bool(names_dict and names_dict.get("/JavaScript"))
open_action = pdf_root.get("/OpenAction")
if open_action:
    open_action = open_action.get_object()
    if hasattr(open_action, "get") and open_action.get("/S") in {"/JavaScript", "/Launch"}:
        pdf_active_actions.append({"location": "catalog OpenAction", "kind": str(open_action.get("/S"))})
for location, value in [("catalog", pdf_root)] + [(f"page {i+1}", page) for i, page in enumerate(pdf.pages)]:
    additional = value.get("/AA")
    if additional:
        pdf_active_actions.append({"location": location, "kind": "additional actions present"})
checks["pdf_no_embedded_files_or_active_scripts"] = {
    "pass": not pdf_embedded and not pdf_script_tree and not pdf_active_actions,
    "embedded_files_or_associated_files": pdf_embedded, "javascript_name_tree": pdf_script_tree,
    "javascript_or_launch_annotations": pdf_active_actions,
}

tex = (SOURCE / "main.tex").read_text()
deposit = json.loads((PACKET / "zenodo-deposit.json").read_text())
metadata = deposit["metadata"]
readme = (SOURCE / "README.md").read_text()
kit_readme = (PACKET / "upload-kit/README.md").read_text()
license_text = (SOURCE / "LICENSE.txt").read_text()
tex_title = command_arg(tex, "\\title")
tex_author = command_arg(tex, "\\author")
tex_date = command_arg(tex, "\\date")
readme_title = re.search(r"^\*\*(.+)\*\*$", readme, re.M).group(1).rstrip(".")
title_values = {"tex_title": tex_title, "pdf_title": pdf_metadata.get("/Title", ""),
                "zenodo_title": metadata.get("title", ""), "readme_title": readme_title}
checks["title_consistency"] = {"pass": all(normalized(value) == EXPECTED_TITLE for value in title_values.values()),
    "normalization": "NFKC, TeX double hyphen and Unicode dash to ASCII hyphen, whitespace collapse", "values": title_values}
first_page = normalized(pdf_texts[0])
checks["pdf_title_page_contains_title"] = {"pass": EXPECTED_TITLE in first_page}
creators = metadata.get("creators", [])
checks["author_and_orcid_consistency"] = {"pass":
    tex_author.startswith(EXPECTED_AUTHOR) and EXPECTED_ORCID in tex_author
    and f"https://orcid.org/{EXPECTED_ORCID}" in tex_author
    and pdf_metadata.get("/Author") == EXPECTED_AUTHOR
    and EXPECTED_AUTHOR in first_page and EXPECTED_ORCID in first_page
    and f"https://orcid.org/{EXPECTED_ORCID}" in pdf_uris
    and creators == [{"name": "Kriebel, Alec", "orcid": EXPECTED_ORCID}]
    and f"{EXPECTED_AUTHOR} — ORCID https://orcid.org/{EXPECTED_ORCID}. No affiliation or coauthor is claimed." in readme
    and "\\and" not in tex_author
    and EXPECTED_AUTHOR in license_text and EXPECTED_ORCID in license_text,
    "tex_author": tex_author, "pdf_author": pdf_metadata.get("/Author"), "zenodo_creators": creators,
    "pdf_orcid_uri_present": f"https://orcid.org/{EXPECTED_ORCID}" in pdf_uris,
    "orcid_pdf_info_field": "Not supplied; visible text and hyperlink checked instead"}
checks["publication_date_consistency"] = {"pass": tex_date == "October 6, 2026"
    and tex_date in first_page and metadata.get("publication_date") == "2026-10-06",
    "tex_visible_date": tex_date, "zenodo_publication_date": metadata.get("publication_date"),
    "pdf_creation_date": pdf_metadata.get("/CreationDate"),
    "interpretation": "PDF creation timestamp 2026-10-07 UTC is a build timestamp, not the publication date."}
checks["readmes_identical"] = {"pass": readme == kit_readme}
checks["license_consistency"] = {"pass": metadata.get("license") == "cc-by-4.0"
    and metadata.get("access_right") == "open" and "CC BY 4.0" in readme
    and "https://creativecommons.org/licenses/by/4.0/" in license_text}
checks["review_publication_state_and_disclosures"] = {"pass":
    inventory.get("publication_state") == "review package, not staged or published"
    and inventory.get("version") == "v3" and inventory.get("packet_directory") == str(PACKET)
    and not metadata.get("doi") and not metadata.get("prereserve_doi")
    and "zenodo.org/record" not in readme and "zenodo.org/record" not in tex
    and "AI tools were used extensively" in readme and "AI tools were used extensively" in metadata["description"]
    and "has not undergone conventional human peer review" in metadata["description"]
    and "has not undergone conventional human peer review" in normalized(" ".join(pdf_texts))
    and "not Lean formalized" in readme,
    "inventory_publication_state": inventory.get("publication_state"),
    "deposit_has_own_doi_or_reserved_doi": bool(metadata.get("doi") or metadata.get("prereserve_doi")),
    "interpretation": "V3 intentionally removes v1 internal proof candidate/pending labels and presents final theorem language. Editorial readiness does not assert an existing deposit. The review inventory explicitly records not staged or published; no own DOI or Zenodo record is claimed in the upload metadata."}
notes.append("V3 final theorem language and removed internal pending labels are editorial changes explicitly confirmed by the parent task. The packet remains not staged or published as recorded by REVIEW_INVENTORY; this audit supplies no readiness/publication certification.")

expected_upload_paths = {"publication/upload-kit/paper.pdf", "publication/upload-kit/source-and-verification.zip", "publication/upload-kit/README.md"}
manifest_uploads = {item["path"] for item in deposit["files"]}
checks["deposit_upload_whitelist"] = compare_sets(manifest_uploads, expected_upload_paths)
upload_bindings = []
for upload in sorted(manifest_uploads):
    source_binding = PROJECT / upload
    candidate_binding = PACKET / "upload-kit" / pathlib.Path(upload).name
    project_hash = sha(source_binding.read_bytes()) if source_binding.is_file() else None
    candidate_hash = sha(candidate_binding.read_bytes()) if candidate_binding.is_file() else None
    upload_bindings.append({"manifest_path": upload, "project_resolves": source_binding.is_file(),
        "packet_resolves_directly": (PACKET / upload).is_file(),
        "project_sha256": project_hash, "reviewed_candidate_sha256": candidate_hash,
        "same_bytes_now": project_hash == candidate_hash and candidate_hash is not None})
checks["deposit_project_paths_currently_match_reviewed_candidate"] = {
    "pass": all(binding["same_bytes_now"] for binding in upload_bindings), "bindings": upload_bindings}
notes.append("Zenodo file paths are project-root-relative publication/upload-kit paths, not packet-relative paths. The current-project hash comparisons below determine which bytes those mutable paths select. The immutable v3 review bytes must be explicitly bound before any staging of v3.")
advisories.append({"id": "A1", "severity": "advisory", "topic": "upload path binding",
    "finding": notes[-1], "blocking_current_package": False,
    "blocking_current_project_staging_of_v3": not all(binding["same_bytes_now"] for binding in upload_bindings)})
bib = (SOURCE / "references.bib").read_text()
bibitem_keys = set(re.findall(r"\\bibitem\{([^}]+)\}", tex))
cited_keys = {key.strip() for citation in re.findall(r"\\cite\{([^}]+)\}", tex) for key in citation.split(",")}
checks["embedded_bibliography_covers_citations"] = {
    "pass": cited_keys <= bibitem_keys, "cited_keys": sorted(cited_keys),
    "embedded_keys": sorted(bibitem_keys), "missing_citation_keys": sorted(cited_keys - bibitem_keys)}
auxiliary_identifiers = ["10.1137/1.9781611971477", "10.1007/s00220-014-2108-8", "10.1007/BF01218078",
    "math/0301175", "2609.29013", "10.1007/BF00250732", "Global classical solutions of the three-dimensional relativistic Vlasov--Maxwell system"]
checks["auxiliary_bibliography_covers_embedded_works"] = {
    "pass": all(identifier in bib for identifier in auxiliary_identifiers),
    "identifiers_checked": auxiliary_identifiers,
    "interpretation": "The v1 Bouchut-Golse-Pallard auxiliary BibTeX omission is fixed; the newly cited Mattingly-Pankavich-Ben-Artzi preprint is also present. This is citation catalog consistency, not bibliographic truth/priority validation."}
attribution = json.loads((SOURCE / "ORIGINAL_CONTINUATION_ATTRIBUTION.json").read_text())
attribution_doi = "10.1007/BF00250732"
checks["original_continuation_attribution_scope_and_catalog_consistency"] = {
    "pass": attribution.get("doi") == attribution_doi
    and attribution.get("primary_url") == "https://link.springer.com/article/" + attribution_doi
    and attribution.get("authors") == ["Robert T. Glassey", "Walter A. Strauss"]
    and attribution.get("year") == 1986 and attribution.get("volume") == 92
    and normalized(attribution.get("pages", "")) == "59-90"
    and attribution.get("title") == "Singularity formation in a collisionless plasma could occur only at high velocities"
    and "Primary publisher bibliographic record and abstract" in attribution.get("scope_actually_inspected", "")
    and "original full theorem/proof not revalidated here" in attribution.get("scope_actually_inspected", "")
    and "without adding a new analytic dependency" in attribution.get("scope_actually_inspected", "")
    and attribution_doi in tex and attribution_doi in bib
    and "\\bibitem{GlasseyStrauss1986}" in tex
    and "precise formulation of" in tex and "Luk--Strain" in tex,
    "attribution_record": attribution,
    "interpretation": "Local metadata/abstract-only inspection is recorded explicitly. The exact relied-on continuation formulation remains attributed to already inspected Luk-Strain and Bouchut-Golse-Pallard sources. No new mathematics, original-proof revalidation, priority or publisher verification is performed by this read-only audit."}
if "math/0301175" not in bib and "Bouchut" not in bib:
    advisories.append({"id": "A2", "severity": "advisory", "topic": "auxiliary bibliography completeness",
        "finding": "Bouchut, Golse and Pallard (2003), arXiv:math/0301175, is cited and fully present in the embedded main.tex/PDF bibliography and PRIMARY_REFERENCE_PROVENANCE.md but absent from references.bib. REPRODUCE.md expressly states that references.bib is not used by the standalone build, so the candidate remains reproducible.",
        "recommendation": "If references.bib is intended as a complete reusable citation catalog, add this work in a future version and refresh all manifests/archive hashes.",
        "blocking_current_package": False})

secret_patterns = {
    "private_key_pem": r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    "github_token": r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b",
    "aws_access_key": r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "slack_token": r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b",
    "openai_key": r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b",
    "google_api_key": r"\bAIza[A-Za-z0-9_-]{30,}\b",
    "basic_auth_url": r"https?://[^\s/:@]+:[^\s/@]+@",
    "credential_assignment": r"(?i)[\"']?(?:access_token|refresh_token|api_key|password|client_secret)[\"']?\s*[:=]\s*[\"'][^\"'\s]{8,}[\"']",
}
secret_hits = []
text_inputs = {}
for relative in initial:
    if relative.endswith((".md", ".txt", ".tex", ".bib", ".py", ".json")):
        text_inputs[relative] = (PACKET / relative).read_text()
text_inputs["upload-kit/paper.pdf [extracted text and metadata]"] = "\n".join(pdf_texts) + json.dumps(pdf_metadata)
for relative, content in text_inputs.items():
    for kind, pattern in secret_patterns.items():
        for match in re.finditer(pattern, content):
            secret_hits.append({"path": relative, "kind": kind,
                "line": content.count("\n", 0, match.start()) + 1,
                "matched_content": "REDACTED"})
checks["credential_pattern_scan"] = {"pass": not secret_hits, "scanned_text_inputs": len(text_inputs),
    "patterns": list(secret_patterns), "hits": secret_hits,
    "limitation": "Pattern scan plus exact whitelist inspection; absence of every possible secret encoding is not provable."}
reference_receipt_path = OUT / "reference_check/reference_receipt.json"
reference_receipt = json.loads(reference_receipt_path.read_text())
checks["independent_reference_receipt_matches_audited_packet"] = {
    "pass": reference_receipt["candidate_packet_hashes"] == initial
    and all(reference_receipt["checks"].values()) and not reference_receipt["blockers"]
    and not reference_receipt["unclassified_references"] and reference_receipt["candidate_unchanged"],
    "receipt_path": str(reference_receipt_path), "receipt_sha256": sha(reference_receipt_path.read_bytes()),
    "reference_checks_passed": reference_receipt["passed_checks"],
    "reference_check_count": reference_receipt["check_count"],
    "classified_reference_occurrences": len(reference_receipt["reference_occurrences"]),
    "classification_counts": reference_receipt["reference_classification_counts"]}
for finding in reference_receipt["findings"]:
    advisories.append(dict(finding, blocking_current_package=False))
current_project_check_names = {
    "builder_allowlist_matches_independent_whitelist", "archive_map_agrees_with_builder_source_paths",
    "archive_map_current_source_correspondence", "deposit_project_paths_currently_match_reviewed_candidate"}
current_project_observations = {name: checks.pop(name) for name in sorted(current_project_check_names)}
project_drift = not all(result["pass"] for result in current_project_observations.values())
notes.append("The earlier independent reference receipt records exact agreement with the builder/source snapshot then inspected. Current project files are mutable external observations rather than frozen-packet inputs. Later drift does not alter package_v3, but can block selecting v3 through current project upload paths.")
for name, result in checks.items():
    if not result["pass"]:
        issues.append({"check": name, "severity": "blocking within audit scope", "details": result})
notes.append("The archive contains locally authored manuscript, notes, code and provenance/hash ledgers only. Provenance facts and third-party citation metadata remain; no third-party manuscript/PDF/source clone, data corpus, dependency tree, cache, failed build tree, or binary is archived.")
notes.append("SHA256SUMS intentionally excludes itself. REVIEW_INVENTORY intentionally excludes itself. Their exact coverage and all declared hashes are verified; this receipt hashes both manifests.")

final = {relative: {"bytes": (PACKET / relative).stat().st_size,
    "sha256": sha((PACKET / relative).read_bytes())} for relative in initial}
checks["audited_packet_unchanged_during_audit"] = {"pass": final == initial}
if not checks["audited_packet_unchanged_during_audit"]["pass"]:
    issues.append({"check": "audited_packet_unchanged_during_audit", "severity": "blocking within audit scope"})

report = {
    "audit_scope": "Packaging, manifests, archive hygiene and author/title/date/license/candidate metadata only; not mathematics, priority or publication approval.",
    "status": "FAIL" if issues else "PASS_WITH_PROJECT_DRIFT" if project_drift else "PASS",
    "frozen_package_status": "PASS" if not issues else "FAIL",
    "current_project_upload_binding_status": "PASS" if current_project_observations["deposit_project_paths_currently_match_reviewed_candidate"]["pass"] else "FAIL_FOR_STAGING_V3_VIA_CURRENT_PATHS",
    "started_utc": start, "completed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "completion_estimate_percent": 100,
    "packet": str(PACKET), "audit_script_sha256": sha(pathlib.Path(__file__).read_bytes()),
    "builder_reference": {"path": str(BUILDER), "sha256": sha(BUILDER.read_bytes()),
                          "read_only_ast_allowlist_extraction": True},
    "initial_project_snapshot": {
        "receipt_path": str(OUT / "INITIAL_PROJECT_SNAPSHOT.json"),
        "receipt_sha256": sha((OUT / "INITIAL_PROJECT_SNAPSHOT.json").read_bytes()),
        "retained_builder_snapshot_sha256": sha((OUT / "checked_inputs/build_publication_package.py").read_bytes())},
    "checks": checks, "issues": issues, "advisories": advisories, "notes": notes,
    "current_project_observations": current_project_observations,
    "independent_reference_audit": {
        "verdict": reference_receipt["verdict"],
        "receipt_sha256": sha(reference_receipt_path.read_bytes()),
        "check_count": reference_receipt["check_count"],
        "passed_checks": reference_receipt["passed_checks"],
        "script_sha256": sha((OUT / "reference_check/audit_references.py").read_bytes()),
        "classified_reference_occurrences": len(reference_receipt["reference_occurrences"]),
        "classification_counts": reference_receipt["reference_classification_counts"],
        "scope": reference_receipt["scope"],
        "initial_builder_sha256": reference_receipt["builder_read_only_sha256"],
        "exact_remaining_gap": "Historical optional reproduction/receipt/digest navigation details recorded in nonblocking advisories; supplied current artifact references resolve."},
    "all_packet_file_hashes_and_sizes": initial, "zip_entries": zip_entries,
    "pdf": {"pages": len(pdf.pages), "info_metadata": pdf_metadata,
            "first_page_metadata_text": "\n".join(pdf_texts[0].splitlines()[:7])},
    "mutations": "Only adjacent audit artifacts; no package/source mutation, git command, network request or publication action.",
}
(OUT / "audit_receipt.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"status": report["status"], "checks": len(checks), "issues": issues,
    "advisories": len(advisories),
    "current_project_observation_count": len(current_project_observations),
    "current_project_upload_binding_status": report["current_project_upload_binding_status"],
    "packet_files": len(initial), "zip_files": len(zip_entries), "pdf_pages": len(pdf.pages),
    "pdf_sha256": initial["upload-kit/paper.pdf"]["sha256"],
    "zip_sha256": initial["upload-kit/source-and-verification.zip"]["sha256"]}, indent=2))
