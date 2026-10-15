"""Portable integrity, consistency, and exact-control verification; standard library only."""
from pathlib import Path, PurePosixPath
from fractions import Fraction
from itertools import product
import hashlib
import json
import os
import re
import stat
import subprocess
import sys

TITLE = "A fixed moment separator without a rational normalized sum-of-squares certificate"
FILES = {
    "README.md", "CLAIM_SCOPE.md", "PRIORITY_NOTE.md", "data.json",
    "SOURCE_VERSIONS.json", "verification/check_exact.py",
    "verification/expected_result.json", "verify_package.py",
    "record_metadata.json", "paper.tex",
}
F_COEFFICIENTS = {
    "4,0,0":"1", "1,3,0":"1", "0,4,0":"1", "2,1,1":"-3",
    "1,2,1":"-4", "2,0,2":"2", "1,0,3":"1", "0,1,3":"1", "0,0,4":"1",
}
CLAIM = {
    "fixed_polynomial":"p", "minimum_on_unit_ball":"1", "mass":"1", "L_m_p":"0", "L_m_q":"0",
    "nonnegative_representing_measure_exists":False, "moment_matrix_PSD":False,
    "rational_certificate_convention":"rational polynomial square factors",
    "p_in_1_plus_Q_R_g":True, "p_in_1_plus_Q_Q_g":False, "p_in_Q_Q_g":True,
    "q_in_1_plus_Q_Q_g":True, "all_finite_multiplier_degrees_excluded_for_p_minus_1":True,
    "rational_rescaling_c_gt_1_removes_normalized_obstruction":True,
    "companion_strict_margin_regime_resolved":False, "worldwide_firstness_certified":False,
    "current_openness_certified":False,
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)

def sha(body):
    return hashlib.sha256(body).hexdigest()

def safe_relative(value):
    require(isinstance(value, str) and value != "", "Manifest path is not a nonempty string")
    p = PurePosixPath(value)
    require(not p.is_absolute() and "\\" not in value and str(p) == value,
            "Noncanonical or absolute manifest path: " + value)
    require(all(part not in ("", ".", "..") for part in p.parts), "Unsafe manifest path: " + value)
    return p

def census(root):
    files, directories = set(), set()
    for folder, ds, fs in os.walk(str(root), followlinks=False):
        for name in ds + fs:
            p = Path(folder) / name
            mode = p.lstat().st_mode
            rel = p.relative_to(root).as_posix()
            require(not stat.S_ISLNK(mode), "Symlink in package: " + rel)
            if stat.S_ISDIR(mode):
                directories.add(rel)
            elif stat.S_ISREG(mode):
                files.add(rel)
            else:
                raise ValueError("Nonregular entry in package: " + rel)
    require(files == FILES | {"manifest.json"}, "Package file inventory differs from the required complete archive")
    require(directories == {"verification"}, "Package directory inventory differs from the required complete archive")
    return files

def consistency(root, expected):
    data = load_json(root / "data.json")
    metadata = load_json(root / "record_metadata.json")
    sources = load_json(root / "SOURCE_VERSIONS.json")
    require(data["schema_version"] == 1 and data["title"] == TITLE and data["version"] == "1.0",
            "Unexpected data schema, title, or version")
    require(data["variables"] == ["x", "y", "z"], "Unexpected variable order")
    polynomials = {
        "f": F_COEFFICIENTS,
        "g": {"0,0,0":"1", "2,0,0":"-1", "0,2,0":"-1", "0,0,2":"-1"},
        "p": dict(F_COEFFICIENTS, **{"0,0,0":"1"}),
        "q": {"0,0,0":"1", "4,0,0":"1"},
    }
    require(data["polynomials"] == polynomials, "Polynomial coefficient data changed")
    indices = [a for a in product(range(5), repeat=3) if sum(a) <= 4]
    entries = [{"exponents":list(a), "value":str(int(a==(0,0,0))-int(a==(4,0,0)))} for a in indices]
    require(data["moments"] == {"maximum_total_degree":4, "index_order":"lexicographic ascending triples", "entries":entries},
            "The complete rational moment data changed")
    require(data["claim"] == CLAIM, "Claim boundaries changed")
    require(data["auxiliary"] == {
        "norm_polynomial_low_to_high":["1","-1","0","0","1"],
        "beta_polynomial_low_to_high":["-1","-4","0","1"],
        "beta_real_interval":["-2","-1"],
        "real_SOS_identity":"4f=U^2-beta V^2; U and V are exactly displayed in paper.tex."},
        "Auxiliary exact polynomial data changed")
    require(data["verification"]["exact_assertions"] == 2059 and data["verification"]["floating_diagnostics"] == 0,
            "Unexpected finite-check scope")
    moments = {tuple(e["exponents"]):Fraction(e["value"]) for e in entries}
    def L(poly):
        return sum(Fraction(c) * moments[tuple(int(v) for v in k.split(","))] for k, c in poly.items())
    require(L(polynomials["p"]) == 0 and L(polynomials["q"]) == 0, "Moment annihilation failed")
    require(expected["norm_terms"] == F_COEFFICIENTS and expected["moment_nonzero"] == {"0,0,0":"1","4,0,0":"-1"},
            "Expected output disagrees with exact data")
    require(expected["status"] == "PASS" and expected["exact_assertions"] == 2059
            and expected["moment_entries"] == 35 and expected["floating_diagnostics"] == 0,
            "Expected finite result changed")
    require(metadata["title"] == TITLE and metadata["publication_date"] == "2026-10-06"
            and metadata["version"] == "1.0", "Publication title, date, or version differs")
    require(metadata["upload_type"] == "publication" and metadata["publication_type"] == "preprint"
            and metadata["access_right"] == "open" and metadata["license"] == "cc-by-4.0",
            "Publication type, access, or license differs")
    require(metadata["creators"] == [{"name":"Kriebel, Alec","affiliation":"Independent researcher","orcid":"0009-0001-9320-500X"}],
            "Author metadata differs")
    require(all(text in metadata["description"] for text in (
        "minimum one", "not positive semidefinite", "c&gt;1", "rational polynomial-square",
        "unrefereed preprint", "AI tools were used extensively", "without independent human peer review",
        "formal proof-assistant certification", "No worldwide-firstness")),
        "Publication description lacks required scope/disclosure statements")
    manuscript = (root / "paper.tex").read_text(encoding="utf-8")
    title_match = re.search(r"\\title\{(.*?)\}", manuscript, re.DOTALL)
    require(title_match is not None, "Missing manuscript title")
    title = re.sub(r"\\\\|\s+", " ", title_match.group(1)).strip()
    title = " ".join(title.split())
    require(title == TITLE, "Manuscript and metadata titles differ")
    require("0009-0001-9320-500X" in manuscript, "Manuscript ORCID differs")
    require("unrefereed preprint" in manuscript and "AI tools were used extensively" in manuscript,
            "Manuscript disclosure is missing")
    require(sources["schema_version"] == 1 and sources["audit_date"] == "2026-10-06",
            "Source-version schema or audit date differs")
    require(sources["original_submission"] == {
        "head":"deb9d7491a0bf887f7615717a5b484caf212cfd6", "QUEUE_status":"claimed_solved",
        "author_allocation":"1/5", "new_author_proof_search_turns":0}, "Original submission provenance differs")
    checker = sources["checker"]
    checker_body = (root / "verification/check_exact.py").read_bytes()
    require(checker["original_bytes"] == 5810 and checker["original_sha256"] == "ec303611beb60b666e636a0028eecd84b2937ca5eb2271003dec89012179da19",
            "Original checker provenance differs")
    require(checker["portable_name"] == "verification/check_exact.py" and checker["portable_bytes"] == len(checker_body)
            and checker["portable_sha256"] == sha(checker_body), "Portable checker provenance differs")
    restored = checker_body.replace(
        b'"""Exact finite controls; the all-degree and Galois proofs are in paper.tex."""',
        b'"""Exact finite controls; the all-degree and Galois arguments are in PROOF.md."""', 1)
    require(len(restored) == 5810 and sha(restored) == checker["original_sha256"],
            "Checker executable content differs beyond its recorded docstring adaptation")
    expected_body = (root / "verification/expected_result.json").read_bytes()
    require(len(expected_body) == 504 and sha(expected_body) == "434a1cd7a7174de9dad34eee2b607d171e4cab0f3d631ec04bdb0fb27f4a5752",
            "Complete expected output identity differs")
    require(checker["expected_result_bytes"] == len(expected_body) and checker["expected_result_sha256"] == sha(expected_body),
            "Expected output provenance differs")
    related = [{"identifier":s["identifier"], "relation":"references",
                "scheme":"url" if s["identifier"].startswith("https:") else "doi"}
               for s in sources["primary_sources"]]
    require(metadata["related_identifiers"] == related, "Metadata related sources differ from source-version inventory")
    require(sources["worldwide_firstness_certified"] is False and sources["current_openness_certified"] is False
            and sources["source_redistribution"] is False and sources["formal_proof_assistant_certification"] is False
            and sources["independent_human_peer_review"] is False, "Source-version limits changed")

def main():
    script = Path(__file__).absolute()
    require(not script.is_symlink(), "The verifier itself is a symlink")
    root = script.parent
    census(root)
    manifest = load_json(root / "manifest.json")
    require(isinstance(manifest, dict) and isinstance(manifest.get("files"), list), "Invalid file manifest")
    entries = manifest["files"]
    seen = set()
    for entry in entries:
        require(isinstance(entry, dict) and set(entry) == {"path", "bytes", "sha256"}, "Invalid manifest entry")
        relative = safe_relative(entry["path"])
        name = relative.as_posix()
        require(name not in seen and name in FILES, "Duplicate or unexpected manifest entry: " + name)
        seen.add(name)
        require(type(entry["bytes"]) is int and entry["bytes"] >= 0, "Invalid manifest byte count")
        require(isinstance(entry["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) is not None,
                "Invalid SHA-256 digest")
        body = (root / name).read_bytes()
        require(len(body) == entry["bytes"] and sha(body) == entry["sha256"], "File identity mismatch: " + name)
    require(seen == FILES, "Manifest does not cover exactly the complete package except itself")
    expected_body = (root / "verification/expected_result.json").read_bytes()
    expected = load_json(root / "verification/expected_result.json")
    consistency(root, expected)
    command = [sys.executable, "-I", "-B", str(root / "verification/check_exact.py")]
    completed = subprocess.run(command, cwd=str(root), stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, check=False)
    if completed.returncode != 0 or completed.stderr or completed.stdout != expected_body:
        sys.stderr.buffer.write(completed.stderr)
        raise RuntimeError("Exact checker failed, produced errors, or differed from its complete expected output")
    print(json.dumps({
        "status":"PASS", "hashed_files":len(entries), "manifest_excludes_itself":True,
        "data_and_metadata_consistent":True, "exact_assertions":expected["exact_assertions"],
        "floating_diagnostics":0,
        "scope":"Portable file integrity and finite exact controls; the written analytic proof and bounded priority comparison require reading the manuscript and notes."},
        indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
