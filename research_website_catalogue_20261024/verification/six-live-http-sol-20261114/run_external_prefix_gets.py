#!/usr/bin/env python3
"""One bounded prefix GET per six DOI/native PDF/ZIP links; no full assets."""
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

OWN=Path(__file__).resolve().parent
if (OWN/"EXTERNAL_PREFIX_RESULTS.json").exists():
    raise SystemExit("Existing result retained; no replay")
gate=json.loads((OWN/"DEPLOY_GATE.json").read_text())
if gate.get("live_GETs_authorized") is not True:
    raise SystemExit("Deployment authorization missing")
items=json.loads((OWN/"EXTERNAL_LINK_EXPECTATIONS.json").read_text())["requests"]


def fetch(pair):
    i,item=pair;hops=[]
    class Track(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,req,fp,code,msg,headers,newurl):
            hops.append({"URL":req.full_url,"HTTP_status":code,"reason":msg,
                         "response_headers_in_received_order":list(headers.raw_items()),
                         "next_URL":newurl})
            return super().redirect_request(req,fp,code,msg,headers,newurl)
    record={"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),**item,
            "method":"GET","explicit_request_headers":[["Range","bytes=0-1023"]],
            "cache_busting":False,"redirects":hops,"full_external_asset_downloaded":False}
    response=None
    try:
        opener=urllib.request.build_opener(Track())
        req=urllib.request.Request(item["URL"],headers={"Range":"bytes=0-1023"},method="GET")
        try:response=opener.open(req,timeout=30)
        except urllib.error.HTTPError as error:response=error
        prefix=response.read(1024)
        record.update({"final_URL":response.geturl(),"HTTP_status":response.code,
                       "reason":response.reason,"MIME_original":response.headers.get("Content-Type"),
                       "response_headers_in_received_order":list(response.headers.raw_items()),
                       "response_headers_raw_latin1":response.headers.as_bytes().decode("latin1"),
                       "body_prefix_bytes_read":len(prefix),"body_prefix_sha256":hashlib.sha256(prefix).hexdigest(),
                       "prefix_file":"external-prefixes/"+str(i).zfill(2)+".bin",
                       "reachability_status":"REACHABLE_PREFIX_ONLY" if response.code in [200,206] else "HTTP_FAILURE_RECORDED"})
        (OWN/record["prefix_file"]).write_bytes(prefix)
        record["expected_PDF_or_ZIP_magic_seen"]=(prefix.startswith(b"%PDF-") if item["kind"]=="native_PDF" else prefix.startswith(b"PK") if item["kind"]=="native_ZIP" else None)
    except Exception as error:
        record.update({"reachability_status":"TRANSPORT_FAILURE_RECORDED","exception":type(error).__name__+": "+str(error)})
    finally:
        if response is not None:response.close()
    return record


(OWN/"external-prefixes").mkdir(exist_ok=True)
with ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(fetch,enumerate(items,1)))
summary={"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "scope":"Only six article DOI and twelve actually linked native PDF/ZIP URLs; no other background links checked.",
         "requests":results,"requests_attempted":len(results),
         "reachable_prefix_responses":sum(x["reachability_status"]=="REACHABLE_PREFIX_ONLY" for x in results),
         "failures_recorded":sum(x["reachability_status"]!="REACHABLE_PREFIX_ONLY" for x in results),
         "whole_external_asset_integrity_claimed":False,"all_external_links_healthy_claimed":False,
         "published_own_host_full_bytes_check_independent_of_external_access":True}
(OWN/"EXTERNAL_PREFIX_RESULTS.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps({k:v for k,v in summary.items() if k!="requests"},indent=2))
for x in results:
    if x["reachability_status"]!="REACHABLE_PREFIX_ONLY":
        print(json.dumps({"URL":x["URL"],"HTTP_status":x.get("HTTP_status"),"exception":x.get("exception")}))
