"""Bounded, import-safe adapter for the two adopted native contracts. No science runs."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).absolute().parent
PROJECT = HERE.parent.parent
IDS = ("23439582", "23440389")
ROOT_AUTH = {
    "23439582": "9bf2f7bc49c6eb4d9d5a58d126b564050d1ddc92f3c767c7150d448ff95788fe",
    "23440389": "1c13db0ce39d199de6bd5851c8f73859fed0c1e5360bcab07bdbb9bbb53c5c99",
}
OLD_SENTENCE = "The proof is analytic and uses the credited classical inputs."
NEW_SENTENCE = "The proof combines algebraic and topological arguments using the credited classical inputs."
EXPECTED = {
    "23439582": {"version": "1.0.0", "pages": 4, "members": 20,
        "pdf": "f11b2f3aa0e1aeec4c5971264e734c0458bd512cbb09e5e5ca11a60f0a037644",
        "zip": "1aeab807b46af3836bcce647c6bd24be945c2f1b82fb710684d087538db51933"},
    "23440389": {"version": "1.0", "pages": 3, "members": 61,
        "pdf": "2b98b7f4129114bf98434ae285a67736976cb4aa3d49b56298c2ee7fec5c6f6f",
        "zip": "65cf534be55648b0d501a3af2834b8397f8f18e8680804ba96f7d405876c3cbb"},
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def literal(value):
    """Retain JSON types AND dict/list order; bool is not interchangeable with int."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def same(left, right):
    return literal(left) == literal(right)


class Frozen:
    def __init__(self, root=HERE):
        self.root = Path(root)
        self.rows = json.loads((self.root / "FROZEN_INPUTS.json").read_text())["files"]
        self.by_path = {r["original_path"]: r for r in self.rows}
        require(len(self.by_path) == len(self.rows) == 607, "exact 607 original input bindings")

    def read(self, path):
        row = self.by_path[str(path)]
        data = (self.root / row["snapshot_path"]).read_bytes()
        require(len(data) == row["bytes"] and digest(data) == row["SHA256"], "frozen bytes: " + str(path))
        return data

    def obj(self, path):
        return json.loads(self.read(path))

    def verify_all(self, originals=True):
        for row in self.rows:
            self.read(row["original_path"])
            if originals:
                data = Path(row["original_path"]).read_bytes()
                require(len(data) == row["bytes"] and digest(data) == row["SHA256"], "original input drift: " + row["original_path"])
        return len(self.rows)


def verify_whole_wrappers(value, frozen):
    """Authenticate heterogeneous bound JSON objects without imposing a common schema."""
    count = 0
    if isinstance(value, dict):
        if "whole_literal_object" in value and "path" in value:
            raw = frozen.read(value["path"])
            require(len(raw) == value["bytes"] and digest(raw) == value["SHA256"], "whole wrapper byte binding")
            require(same(json.loads(raw), value["whole_literal_object"]), "whole wrapper types/order/nulls")
            count += 1
        for child in value.values():
            count += verify_whole_wrappers(child, frozen)
    elif isinstance(value, list):
        for child in value:
            count += verify_whole_wrappers(child, frozen)
    return count


def approved_main(record_id, original):
    require(original.count("<main>") == 1 and original.endswith("</main>"), "single original main tree")
    require("<main id=" not in original, "original main has no id")
    text = original.replace("<main>", '<main id="main">', 1)
    if record_id == "23439582":
        require(text.count(OLD_SENTENCE) == 1 and NEW_SENTENCE not in text, "exactly one approved stylistic replacement")
        text = text.replace(OLD_SENTENCE, NEW_SENTENCE, 1)
    return text


def load_records(frozen=None):
    frozen = frozen or Frozen()
    records = []
    for rid in IDS:
        base = PROJECT / "papers" / rid
        editorial = base / "reviews/editorial"
        pub = frozen.obj(base / "publication.json")
        promotion = frozen.obj(base / "promotion.json")
        adapter = frozen.obj(editorial / "SCHEMA_ADAPTER.json")
        sb = pub["source_binding"]
        protocol_path = sb.get("source_protocol_binding_file", sb.get("source_protocol_binding_path"))
        protocol = frozen.obj(protocol_path)
        ready_path = sb.get("current_source_ready_path", sb.get("source_ready_path"))
        ready = frozen.obj(ready_path)
        verdict_key = "whole_original_two_scientific_custom_verdicts" if rid == "23439582" else "whole_original_custom_scientific_verdicts"
        main = (HERE / "inputs" / (rid + "-original-main.html")).read_text()
        candidate = frozen.read(editorial / "candidate/index.html").decode()
        require(re.findall(r"<main>.*?</main>", candidate, re.S) == [main], "main snapshot exactly matches adopted candidate")
        r = {"id": rid, "pub": pub, "promotion": promotion, "adapter": adapter,
             "protocol": protocol, "ready": ready, "ready_path": ready_path,
             "verdicts": promotion[verdict_key], "main_original": main,
             "main": approved_main(rid, main), "bib": frozen.read(editorial / "citation.bib")}
        validate_record(r, frozen)
        records.append(r)
    return records


def validate_record(r, frozen):
    rid, p, pr, s, rd, ex = r["id"], r["pub"], r["promotion"], r["pub"]["source_binding"], r["ready"], EXPECTED[r["id"]]
    base = PROJECT / "papers" / rid
    require(same(p, frozen.obj(base / "publication.json")), "whole publication object/types/order/nulls unchanged")
    require(same(pr, frozen.obj(base / "promotion.json")), "whole promotion object/types/order/nulls/historical flags unchanged")
    require(same(r["adapter"], frozen.obj(base / "reviews/editorial/SCHEMA_ADAPTER.json")), "whole original editorial adapter unchanged")
    require(same(rd, frozen.obj(r["ready_path"])), "whole literal original READY, not a normalized replica")
    protocol_path = s.get("source_protocol_binding_file", s.get("source_protocol_binding_path"))
    require(same(r["protocol"], frozen.obj(protocol_path)), "whole native transport/source protocol unchanged")
    authority = PROJECT / "verification" / ("root-editorial-" + rid + "-20261115.json")
    require(digest(frozen.read(authority)) == ROOT_AUTH[rid], "root editorial adoption exact authority")
    require(p["publication_date"] == "2026-10-17" and p["version"] == ex["version"] and p["pdf_pages"] == ex["pages"], "original date/version/page contract")
    require(p["canonical_url"] is None and p["AA"] is None and p["native_sheet_aa_url"] is None, "historical canonical/AA null")
    require(p["follow_up"] is None and pr["follow_up"] is None, "no invented followup")
    for key in ("deployed", "live_verified", "native_verified", "public_page_published", "production_integration_authorized", "ready_to_publish", "canonical_verified"):
        require(pr[key] is False, "historical publication flag stays false: " + key)
    require(same(s["whole_original_source_ready"], rd) and same(pr["whole_original_source_ready"], rd), "whole source READY literal equality")
    require(digest(frozen.read(r["ready_path"])) == s["source_ready_sha256"], "exact source READY bytes")
    require(len(r["verdicts"]) == 2, "exactly two whole original science verdicts")
    vk = "whole_original_two_scientific_custom_verdicts" if rid == "23439582" else "whole_original_custom_scientific_verdicts"
    require(same(r["verdicts"], p["review_metadata"][vk]), "publication/promotion whole verdict consistency")
    for w in r["verdicts"]:
        require(type(w["whole_literal_object"]) is dict and len(w["whole_literal_object"]) > 5, "custom verdict preserved, not generic PASS")
        require(same(w["whole_literal_object"], frozen.obj(w["path"])), "original complete custom verdict")
    verify_whole_wrappers(r["protocol"], frozen)
    require(p["license"] == "CC BY 4.0" and p["license_url"] == "https://creativecommons.org/licenses/by/4.0/", "actual CC BY 4.0 license")
    if rid == "23439582":
        require(p["code_license"] == "CC BY 4.0", "121 real authored code license")
        require(rd["completion_percent"] == s["historical_ready_completion_percent"] == 95, "121 READY95 preserved")
        require(s["final_source_seal_completion_percent"] == 100 and s["native_ZIP_fresh_GET_claimed"] is False, "121 final100, cached ZIP, no fresh GET")
        require(rd["new_resumption_HTTP_status_sequence"] == [200, 301, 200, 200, 200, 200] and rd["prior_failed_HTTP_status_sequence"] == [403, 403, 403], "121 six new + three old 403 transports")
        require(len(r["protocol"]["six_actual_new_transport_objects"]) == 6 and len(r["protocol"]["three_actual_old_403_transport_objects"]) == 3, "121 complete transport objects")
        require(rd["all_supporting_payloads_inventoried"] == 20 and len(rd["all_embedded_PDFs"]) == 1, "121 all20 payloads and embedded PDF")
        embedded = rd["all_embedded_PDFs"][0]
        require(embedded["byte_identical_to_published_PDF"] is True and embedded["SHA256"] == ex["pdf"], "121 unchanged embedded PDF")
        cache = r["protocol"]["cache_association"]
        require("whole_literal_object" in cache, "whole actual cache association")
    else:
        require(p["code_license"] is None and p["authored_package_license"] == "CC BY 4.0", "122 separate code instrument null; broad CC grant includes code")
        require(rd["actual_statuses_in_dispatch_order"] == [200, 301, 200, 200, 200, 200, 200] and rd["actual_ordinary_HTTP_requests"] == 7, "122 seven normal requests")
        require(len(r["protocol"]["transport_objects"]) == 7, "122 seven whole transport objects")
    assets = rd["all_native_assets_in_original_order"]
    require(len(assets) == 2, "exactly two original assets")
    require([a["original_api_file_object"]["key"] for a in assets] == [p["supplement_filename"], p["pdf_filename"]], "literal native ZIP then PDF order")
    for a, kind in zip(assets, ("zip", "pdf")):
        require(a["SHA256"] == ex[kind], "native asset SHA: " + kind)
        raw = frozen.read(a["path"])
        require(len(raw) == a["bytes"] and digest(raw) == ex[kind], "native asset bytes: " + kind)
        require(hashlib.md5(raw).hexdigest() == a["MD5"], "native asset MD5: " + kind)
    require(r["bib"].decode() == p["prepared_bibtex"], "prepared BibTeX unchanged")
    require(r["main"] == approved_main(rid, r["main_original"]), "only declared HTML/prose changes")
    return True


def native_audit(records):
    return {"scope": "Private publication adapter; original native/review objects preserved, no new scientific assessment.",
        "prior_role": "Stage author previously performed record122 adversarial review; informed integration, not an independent code audit.",
        "records": [{"record_id": r["id"], "whole_original_source_ready": r["ready"],
            "whole_original_native_API_objects": r["pub"]["source_binding"]["whole_original_native_API_objects"],
            "whole_native_transport_protocol": r["protocol"],
            "whole_original_two_scientific_custom_verdicts": r["verdicts"],
            "historical_publication_flags_unchanged": r["promotion"],
            "authored_package_license": "CC BY 4.0",
            "separate_code_instrument": r["pub"]["code_license"]} for r in records]}


def output_paths(records):
    out = {"research/index.html", "research/sitemap.xml"}
    for r in records:
        p = r["pub"]; prefix = "research/" + p["slug"] + "/"
        out.update((prefix + "index.html", prefix + "assets/" + p["pdf_filename"], prefix + "assets/" + p["supplement_filename"], prefix + "assets/citation.bib"))
    require(len(out) == 10, "exact ten-path overlay")
    return out


def verify_live_baseline():
    baseline = json.loads((HERE / "FRESH_BASELINE.json").read_text())
    root = Path(baseline["public_root"])
    actual = sorted(str(x.relative_to(root)) for x in root.rglob("*") if x.is_file())
    require(actual == sorted(x["path"] for x in baseline["public_files"]), "fresh585 public namespace fence")
    for row in baseline["public_files"]:
        data = (root / row["path"]).read_bytes()
        require(len(data) == row["bytes"] and digest(data) == row["SHA256"], "old public bytes unchanged: " + row["path"])
    supplement = json.loads((HERE / "ROOT_AUTHORIZED_CORE_SUPPLEMENT.json").read_text())
    require(supplement["authorized_current_SHA256"] == "405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0", "only exact root-authorized helper update")
    require(supplement["original_baseline_binding"]["SHA256"] == "91d5c5d285502e5a82f3eb090cf3399458c96416a873a674439ef5a1b435af5b", "original helper fence retained")
    for row in baseline["installed_core_files"] + baseline["site_configurations"]:
        data = Path(row["path"]).read_bytes()
        if row["path"] == supplement["exact_original_path"]:
            require(same(row, supplement["original_baseline_binding"]), "supplement cannot rebind another baseline entry")
            require(len(data) == supplement["authorized_current_bytes"] and digest(data) == supplement["authorized_current_SHA256"], "exact authorized current checkpoint helper")
        else:
            require(len(data) == row["bytes"] and digest(data) == row["SHA256"], "installed core/config fence: " + row["path"])
    require(digest(Path(baseline["site_index_path"]).read_bytes()) == baseline["site_index_SHA256"], "website Git index unchanged")
    prior = json.loads((HERE / "PROTECTED_PRIOR_PACKETS.json").read_text())
    for packet in prior["packets"]:
        for row in packet["files"]:
            data = Path(row["path"]).read_bytes()
            require(len(data) == row["bytes"] and digest(data) == row["SHA256"], "old sealed two/five packet unchanged")
    return {"public_files": len(actual), "index_entries": baseline["index_entries"], "sitemap_locations": baseline["sitemap_locations"], "core_files": len(baseline["installed_core_files"]), "core_original_unchanged": len(baseline["installed_core_files"]) - 1, "root_authorized_checkpoint_helper_supplement": supplement["authorized_current_SHA256"], "prior_owned_payloads": [p["complete_owned_payloads_verified"] for p in prior["packets"]]}
