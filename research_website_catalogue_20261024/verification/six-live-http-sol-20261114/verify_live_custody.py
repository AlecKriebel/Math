#!/usr/bin/env python3
"""Pure offline custody/result closure; no network, subprocess or writes."""
from pathlib import Path
import hashlib
import json
import re
import urllib.parse

OWN=Path(__file__).resolve().parent
EXCLUDED={"OWNED_MANIFEST.json","FINAL_SEAL.json","CLOSURE_RESULTS.json"}


def data(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def check(p,row):
    require(p.is_file() and not p.is_symlink() and p.stat().st_size==row["bytes"] and sha(p)==row["sha256"],"Byte mismatch: "+str(p))


gate=data(OWN/"DEPLOY_GATE.json")
require(gate["deploy_complete"] is True and gate["live_GETs_authorized"] is True,"Missing explicit deployment signal")
require(sha(OWN/"HOSTING_DEPLOY_RECEIPT.json")==gate["hosting_receipt_source_sha256"],"Hosting receipt mismatch")
hosting=data(OWN/"HOSTING_DEPLOY_RECEIPT.json")
require(hosting["returncode"]==0 and hosting["parsed_native_cli_JSON"]["status"]=="success","Hosting native success missing")
expected=data(OWN/"EXPECTED_HTTP.json")
require(expected["approved_public_install_sha256"]==sha(OWN/"APPROVED_PUBLIC_INSTALL.json"),"Approved install copy mismatch")
install=data(OWN/"APPROVED_PUBLIC_INSTALL.json")
require(len(install["installed_public_files"])==26 and len(expected["requests_in_expected_order"])==30,"Wrong approved request set")
local=data(OWN/"local-custody/EXPECTED_LOCAL.json")
public=Path(local["public_root"])
for row in local["unchanged_old_public_files"]:check(public/row["path"],row)
for row in local["unchanged_core_files"]:check(Path(row["path"]),row)
for row in local["approved_installed26"]:check(public/row["path"],row)
names={x["path"] for x in local["unchanged_old_public_files"]+local["approved_installed26"]}
require({str(f.relative_to(public)) for f in public.rglob("*") if f.is_file()}==names and len(names)==556,"Public namespace changed")
require(len(local["unchanged_old_public_files"])==530 and len(local["unchanged_core_files"])==18,"Old/core counts changed")
require(sha(OWN/"local-custody/FINAL_SEAL.json")=="2534c1b9965404c0d8cab0cf79f529fd6d36ccf9fc82679a943b7a6aa685b11e","Local custody seal changed")

live=data(OWN/"LIVE_HTTP_RESULTS.json")
require(live["started_UTC"]>=gate["UTC_explicit_signal_received"],"Live request preceded explicit signal")
require(live["status"]=="PASS_FULL_30_ORDINARY_LIVE_GETS" and len(live["requests"])==30,"Live full-GET check failed")
for i,(row,r) in enumerate(zip(expected["requests_in_expected_order"],live["requests"]),1):
    check(Path(row["approved_local_path"]),row)
    require(data(OWN/"receipts"/(str(i).zfill(2)+".json"))==r,"Individual receipt differs from aggregate")
    require(r["requested_URL"]==r["final_URL"]==row["URL"] and r["HTTP_status"]==200,"Redirect/status mismatch")
    require(r["response_body_bytes"]==row["bytes"] and r["response_body_sha256"]==row["sha256"],"Whole body size/hash mismatch")
    require(r["complete_response_body_consumed"] is True and r["whole_body_compared_byte_for_byte_to_approved"] is True,"Incomplete byte verification")
    require(r["MIME_essence"] in row["MIME_essences_allowed"] and all(r["checks"].values()) and not r["failures"],"Response validation failure")
    require(not urllib.parse.urlsplit(r["requested_URL"]).query and r["cache_busting_or_cache_override"] is False,"Cache-busting/override present")
    if row["require_max_age_zero"]:
        require(any(re.search(r"(?:^|[,\s])max-age\s*=\s*0(?:[,\s]|$)",x,re.I) for x in r["Cache_Control_original_values"]),"Required max-age0 missing")
    if "response_body_file" in r:
        f=OWN/r["response_body_file"]
        require(f.stat().st_size==row["bytes"] and sha(f)==row["sha256"],"Stored small response mismatch")
for article in expected["articles"]:
    require(sha(Path(article["native_record_path"]))==article["native_record_sha256"],"Original raw native record changed")
    record=data(Path(article["native_record_path"]))
    require(article["citation_publication_date"]==record["metadata"]["publication_date"].replace("-","/"),"Citation/native date mismatch")
require(len(live["six_article_metadata_and_readers"])==6 and all(x["status"]=="PASS" and all(x["checks"].values()) for x in live["six_article_metadata_and_readers"]),"Article metadata/reader failure")
index=live["index_and_sitemap"]
require(index["research_index_unique_article_links"]==78 and index["sitemap_URLs"]==index["sitemap_unique_URLs"]==79 and index["all_six_exact_canonicals_in_index"] is True and index["all_six_exact_canonicals_in_sitemap"] is True,"Index/sitemap mismatch")

external=data(OWN/"EXTERNAL_PREFIX_RESULTS.json")
require(len(external["requests"])==18 and external["reachable_prefix_responses"]==18 and external["failures_recorded"]==0,"External prefix checks failed or changed")
for r in external["requests"]:
    f=OWN/r["prefix_file"]
    require(f.stat().st_size==r["body_prefix_bytes_read"]<=1024 and sha(f)==r["body_prefix_sha256"],"External prefix custody mismatch")
    require(r["HTTP_status"] in [200,206],"External HTTP failure")
    if r["kind"]=="native_DOI":
        require(r["HTTP_status"]==200 and r["final_URL"]=="https://zenodo.org/records/"+r["record_id"],"DOI target mismatch")
    else:require(r["HTTP_status"]==206 and r["expected_PDF_or_ZIP_magic_seen"] is True,"Native ranged asset prefix mismatch")
require(external["whole_external_asset_integrity_claimed"] is False and external["all_external_links_healthy_claimed"] is False,"Overstated external health")

if (OWN/"OWNED_MANIFEST.json").exists():
    manifest=data(OWN/"OWNED_MANIFEST.json")
    actual={str(f.relative_to(OWN)) for f in OWN.rglob("*") if f.is_file() and str(f.relative_to(OWN)) not in EXCLUDED}
    require(actual=={x["relative_path"] for x in manifest["files"]},"Owned inventory mismatch")
    for row in manifest["files"]:check(OWN/row["relative_path"],row)
if (OWN/"FINAL_SEAL.json").exists():
    seal=data(OWN/"FINAL_SEAL.json")
    for key,name in [("owned_manifest_sha256","OWNED_MANIFEST.json"),("expected_HTTP_sha256","EXPECTED_HTTP.json"),("live_HTTP_results_sha256","LIVE_HTTP_RESULTS.json"),("external_prefix_results_sha256","EXTERNAL_PREFIX_RESULTS.json"),("report_sha256","REPORT.md"),("verdict_sha256","VERDICT.json"),("closure_result_sha256","CLOSURE_RESULTS.json")]:
        require(seal[key]==sha(OWN/name),"Final seal mismatch: "+key)
print(json.dumps({"status":"PASS_PURE_OFFLINE_LIVE_HTTP_CUSTODY_CLOSURE","ordinary_full_own_host_GETs_passed":30,"approved_installed_files_exact":26,"old_public_files_unchanged":530,"core_files_unchanged":18,"public_namespace_files":556,"article_canonicals_citation_dates_readers":6,"index_articles":78,"sitemap_unique_URLs":79,"research_HTML_max_age_zero":7,"bounded_external_checks":18,"external_DOI_destinations_200":6,"native_asset_prefixes_206_with_magic":12,"whole_external_integrity_or_all_background_health_claimed":False,"network_or_subprocess_or_writes":False,"browser_or_native_AA_authority":False},indent=2))
