#!/usr/bin/env python3
"""Bounded ordinary live GETs, only after explicit deployment authorization.

No cache-busting, cache override, browser or preexisting writes. Stream every
PDF/ZIP completely and compare every byte to approved local bytes; retain
full ordered response headers and complete-body hashes. Small bodies saved.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

OWN = Path(__file__).resolve().parent


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(pair):
    ordinal, expected = pair
    started = utc()
    url = expected["URL"]
    if urllib.parse.urlsplit(url).query or not url.startswith("https://aleckriebel.com/"):
        raise RuntimeError("Not an ordinary approved origin URL")
    opener = urllib.request.build_opener(NoRedirect())
    request = urllib.request.Request(url, method="GET")
    response = None
    record = {"ordinal": ordinal, "started_UTC": started, "method":"GET", "requested_URL":url,
              "explicit_request_headers":list(request.header_items()), "cache_busting_or_cache_override":False,
              "expected":expected, "failures":[]}
    try:
        try:
            response = opener.open(request, timeout=35)
        except urllib.error.HTTPError as error:
            response = error
        record.update({"HTTP_status":response.code, "reason":response.reason,
                       "final_URL":response.geturl(), "HTTP_version":getattr(response,"version",None),
                       "response_headers_in_received_order":list(response.headers.raw_items()),
                       "response_headers_raw_latin1":response.headers.as_bytes().decode("latin1"),
                       "MIME_original":response.headers.get("Content-Type"),
                       "Cache_Control_original_values":response.headers.get_all("Cache-Control") or []})
        mime = (record["MIME_original"] or "").split(";",1)[0].strip().lower()
        record["MIME_essence"] = mime
        h = hashlib.sha256(); count = 0; equal = True; full = True; chunks = []
        limit = max(expected["bytes"]+65536, 2000000)
        with Path(expected["approved_local_path"]).open("rb") as approved:
            while True:
                block = response.read(65536)
                if not block:
                    break
                count += len(block)
                h.update(block)
                if approved.read(len(block)) != block:
                    equal = False
                if expected["store_full_response_body"]:
                    chunks.append(block)
                if count > limit:
                    full = False
                    record["failures"].append("Unexpected response exceeded bounded size")
                    break
            if approved.read(1):
                equal = False
        record.update({"response_body_bytes":count,"response_body_sha256":h.hexdigest(),
                       "complete_response_body_consumed":full,
                       "whole_body_compared_byte_for_byte_to_approved":equal and full,
                       "response_body_storage":"full-small-body" if expected["store_full_response_body"] else "complete-stream-hash-and-byte-comparison; no duplicate binary stored"})
        if chunks:
            suffix = Path(expected["path"]).suffix
            body_file = "responses/"+str(ordinal).zfill(2)+suffix
            (OWN/body_file).write_bytes(b"".join(chunks))
            record["response_body_file"] = body_file
        checks = {"status_200":record["HTTP_status"]==200,
                  "no_redirect_and_correct_target":record["final_URL"]==url and record["HTTP_status"]==200,
                  "compatible_MIME":mime in expected["MIME_essences_allowed"],
                  "complete_body":full,
                  "whole_expected_size":count==expected["bytes"],
                  "whole_expected_SHA256":h.hexdigest()==expected["sha256"],
                  "whole_expected_bytes":equal and full}
        if expected["require_max_age_zero"]:
            checks["Cache_Control_max_age_zero"] = any(re.search(r"(?:^|[,\s])max-age\s*=\s*0(?:[,\s]|$)",x,re.I) for x in record["Cache_Control_original_values"])
        record["checks"] = checks
        record["failures"].extend(name for name,ok in checks.items() if not ok)
    except Exception as error:
        record["exception"] = type(error).__name__+": "+str(error)
        record["failures"].append("Transport/read exception")
    finally:
        if response is not None:
            response.close()
    record["completed_UTC"] = utc()
    record["status"] = "PASS" if not record["failures"] else "FAIL"
    (OWN/"receipts"/(str(ordinal).zfill(2)+".json")).write_text(json.dumps(record,indent=2)+"\n")
    return record


class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.meta={}; self.canonicals=[]; self.links=[]; self.frames=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="meta" and "name" in a:self.meta[a["name"]]=a.get("content")
        if tag=="link" and a.get("rel")=="canonical":self.canonicals.append(a.get("href"))
        if tag=="a" and a.get("href"):self.links.append(a["href"])
        if tag=="iframe":self.frames.append(a.get("src"))


parser=argparse.ArgumentParser(); parser.add_argument("--perform-live-GETs",action="store_true");args=parser.parse_args()
if not args.perform_live_GETs:
    raise SystemExit("Explicit --perform-live-GETs argument required; no network performed")
gate=json.loads((OWN/"DEPLOY_GATE.json").read_text())
if gate.get("deploy_complete") is not True or gate.get("live_GETs_authorized") is not True:
    raise SystemExit("Explicit deployment-complete authorization missing; no network performed")
if (OWN/"LIVE_HTTP_RESULTS.json").exists():
    raise SystemExit("Existing live result retained; this runner refuses to overwrite/replay")
expected=json.loads((OWN/"EXPECTED_HTTP.json").read_text())
(OWN/"responses").mkdir(exist_ok=True); (OWN/"receipts").mkdir(exist_ok=True)
started=utc()
with ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(fetch,enumerate(expected["requests_in_expected_order"],1)))
by_url={r["requested_URL"]:r for r in results}
structural=[]
for article in expected["articles"]:
    r=by_url[article["URL"]]
    entry={"URL":article["URL"],"record_id":article["record_id"],"checks":{}}
    if "response_body_file" in r:
        page=Page();page.feed((OWN/r["response_body_file"]).read_text())
        linked={urllib.parse.urljoin(article["URL"],x).split("#",1)[0] for x in page.links}
        frames={urllib.parse.urljoin(article["URL"],x).split("#",1)[0] for x in page.frames if x}
        entry["checks"]={"exact_single_canonical":page.canonicals==[article["canonical"]],
                         "citation_DOI":page.meta.get("citation_doi")==article["citation_DOI"],
                         "citation_original_native_date":page.meta.get("citation_publication_date")==article["citation_publication_date"],
                         "citation_PDF_URL":page.meta.get("citation_pdf_url")==article["citation_pdf_url"],
                         "all_three_exact_assets_linked":set(article["all_three_approved_asset_URLs"])<=linked,
                         "complete_original_PDF_iframe":article["citation_pdf_url"] in frames}
        entry["observed_canonicals"]=page.canonicals; entry["observed_citation_date"]=page.meta.get("citation_publication_date")
    else:entry["checks"]={"HTML_body_available":False}
    entry["status"]="PASS" if all(entry["checks"].values()) else "FAIL";structural.append(entry)
index=by_url["https://aleckriebel.com/research/"]
page=Page();page.feed((OWN/index["response_body_file"]).read_text())
article_links={urllib.parse.urljoin(index["requested_URL"],x) for x in page.links if re.fullmatch(r"/research/[^/]+/",x)}
sitemap=by_url["https://aleckriebel.com/research/sitemap.xml"]
tree=ET.fromstring((OWN/sitemap["response_body_file"]).read_bytes());locs=[e.text for e in tree.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
new_canonicals={x["canonical"] for x in expected["articles"]}
indexes={"research_index_unique_article_links":len(article_links),"expected_index_articles":78,
         "sitemap_URLs":len(locs),"sitemap_unique_URLs":len(set(locs)),"expected_sitemap_URLs":79,
         "all_six_exact_canonicals_in_index":new_canonicals<=article_links,
         "all_six_exact_canonicals_in_sitemap":new_canonicals<=set(locs)}
index_pass=len(article_links)==78 and len(locs)==len(set(locs))==79 and new_canonicals<=article_links and new_canonicals<=set(locs)
overall=all(r["status"]=="PASS" for r in results) and all(r["status"]=="PASS" for r in structural) and index_pass
summary={"started_UTC":started,"completed_UTC":utc(),"status":"PASS_FULL_30_ORDINARY_LIVE_GETS" if overall else "FAIL_LIVE_HTTP_CHECKS",
         "deployment_explicitly_completed_before_any_live_GET":True,"requests":results,
         "six_article_metadata_and_readers":structural,"index_and_sitemap":indexes,
         "full_response_GETs":len(results),"passed_response_GETs":sum(r["status"]=="PASS" for r in results),
         "public_or_native_AA_writes":0,"redirect_or_site_core_Git_mutations":False,"browser_verification_claimed":False}
(OWN/"LIVE_HTTP_RESULTS.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps({k:v for k,v in summary.items() if k not in ["requests","six_article_metadata_and_readers"]},indent=2))
for r in results:
    if r["status"]!="PASS":print(json.dumps({"URL":r["requested_URL"],"failures":r["failures"],"HTTP_status":r.get("HTTP_status"),"exception":r.get("exception")}))
