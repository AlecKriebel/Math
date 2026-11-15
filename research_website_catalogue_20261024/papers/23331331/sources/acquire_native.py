#!/usr/bin/env python3
"""New source-only metadata/assets acquisition, using only fresh ordinary GETs."""
from pathlib import Path
import datetime,hashlib,json
from ordinary_get import fetch
R=Path(__file__).resolve().parent
def require(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    q=json.loads((R/"QUEUE_BINDING.json").read_text())["identity_only"]
    record=json.loads((R/"record.response.body").read_bytes());m=record["metadata"]
    require(record["id"]==q["record_id"] and m["title"]==q["title"] and record["doi"]==q["doi"],"Native record identity mismatch")
    require(m["resource_type"]["type"]=="publication","Not an actual published paper record")
    objects=[{"role":"record","path":str(R/"record.response.body"),"bytes":(R/"record.response.body").stat().st_size,"SHA256":sha((R/"record.response.body").read_bytes())}]
    b,receipt,redirects=fetch(record["links"]["latest"],"latest")
    latest=json.loads(b);require(latest["id"]==record["id"],"Queue record is not the current native latest; preserve and reconcile alias")
    objects.append({"role":"latest","path":receipt["body_path"],"bytes":len(b),"SHA256":sha(b)})
    versions=[];original_totals=[];next_url=record["links"]["versions"];pages=0
    while next_url:
        pages+=1;require(pages<=100,"Unexpected versions pagination")
        b,vr,_=fetch(next_url,"versions-page%03d"%pages);v=json.loads(b)
        hits=v["hits"];require(isinstance(hits,dict) and isinstance(hits["hits"],list),"Unsupported native version shape retained")
        versions.extend(hits["hits"]);original_totals.append(hits.get("total"))
        objects.append({"role":"versions-page%03d"%pages,"path":vr["body_path"],"bytes":len(b),"SHA256":sha(b)})
        next_url=v.get("links",{}).get("next")
    require(len({str(v["id"]) for v in versions})==len(versions),"Duplicate version ids")
    total=original_totals[0]
    count=total if type(total)is int else total.get("value") if isinstance(total,dict) else None
    require(type(count)is int and count==len(versions),"Native version enumeration incomplete or unknown total type")
    require(any(v["id"]==record["id"] for v in versions),"Actual record absent from versions")
    b,fr,_=fetch(record["links"]["files"],"files");files=json.loads(b);entries=files["entries"]
    require(isinstance(entries,(list,dict)),"Unsupported files entries original shape retained")
    if isinstance(entries,dict):
        entry_pairs=[(key,value) for key,value in entries.items()]
    else:entry_pairs=[(None,value) for value in entries]
    objects.append({"role":"files","path":fr["body_path"],"bytes":len(b),"SHA256":sha(b)})
    native_assets=record["files"];require(isinstance(native_assets,list) and native_assets,"No native published assets")
    assets=[];(R/"assets").mkdir()
    for i,a in enumerate(native_assets):
        key=a["key"];require(isinstance(key,str) and Path(key).name==key and key not in [".",".."],"Unsafe native asset key")
        matching=[e for k,e in entry_pairs if (e.get("key",k)==key)]
        require(len(matching)==1,"Native record/files endpoint association ambiguous")
        e=matching[0]
        b,ar,_=fetch(a["links"]["self"],"asset-%03d"%(i+1),"*/*")
        algorithm,expected=a["checksum"].split(":",1)
        require(len(b)==a["size"] and hashlib.new(algorithm,b).hexdigest()==expected,"Actual native asset checksum/size mismatch")
        require(e["size"]==a["size"] and e["checksum"]==a["checksum"],"Record/files whole original checksum discrepancy")
        target=R/"assets"/key;target.write_bytes(b)
        assets.append({"ordinal_zero_based":i,"original_api_file_object":a,"whole_original_native_files_entry":e,"path":str(target),"transport_body_path":ar["body_path"],"bytes":len(b),"SHA256":sha(b),"native_checksum_verified":True,"fresh_ordinary_native_GET":True,"cached_bytes_reused":False})
    out={"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"record_id":record["id"],"conceptrecid":record["conceptrecid"],"title":m["title"],"doi":record["doi"],"version_field_present":"version" in m,"version_original":m.get("version"),"publication_date":m["publication_date"],"created":record["created"],"updated":record["updated"],"license_original":m.get("license"),"resource_type_original":m.get("resource_type"),"latest_record_id":latest["id"],"all_versions_total_original_fields":original_totals,"all_version_ids":[v["id"] for v in versions],"version_pagination_exhaustive":True,"whole_native_API_objects":objects,"all_assets_in_original_order":assets,"files_entries_original_type":type(entries).__name__,"files_order_present":"order" in files,"files_order_original":files.get("order"),"files_default_preview_present":"default_preview" in files,"files_default_preview_original":files.get("default_preview"),"whole_objects_not_reserialized_in_place":True,"metadata_description_mathematical_content_scientifically_read":False}
    (R/"ACQUIRED_NATIVE.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
    (R/"SOURCE_LOG.md").open("a").write("\n"+out["UTC"]+" — 45%: Fresh native record/latest/allversions/files and every original asset authenticated by native size/checksum; all native order/object/null/header shapes and redirect bodies retained. No scientific text/code/results read. Safe recursive archive/PDF metadata/fresh unread rasters pending.\n")
    print(json.dumps({"record_id":record["id"],"latest":latest["id"],"versions":out["all_version_ids"],"assets":[{"key":a["original_api_file_object"]["key"],"bytes":a["bytes"],"SHA256":a["SHA256"]} for a in assets],"HTTP_statuses":[a["HTTP_status"] for a in json.loads((R/"ALL_TRANSPORT_RECEIPTS.json").read_text())]},indent=2))
if __name__=="__main__":main()
