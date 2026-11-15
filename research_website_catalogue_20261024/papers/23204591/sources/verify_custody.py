#!/usr/bin/env python3
"""Pure offline source custody; standard library only, no project/supplied-code imports."""
from pathlib import Path,PurePosixPath
from urllib.parse import urlsplit,urljoin
import hashlib,io,json,stat,struct,sys,tarfile,zipfile,zlib,unicodedata
R=Path(__file__).resolve().parent
EXCLUDED={"SOURCE_READY_MANIFEST.json","SOURCE_READY_CLOSURE.json","SOURCE_READY_SEAL.json"}
N=0
def require(x,m):
    global N
    N+=1
    if not x:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inside(p):
    p=Path(p);require(p.resolve().is_relative_to(R) and not p.is_symlink(),"Path outside/symlink source root");return p
def bound(row,absolute=False):
    p=Path(row["path"]) if absolute else R/row["path"]
    if not absolute:
        s=PurePosixPath(row["path"]);require(not s.is_absolute() and ".." not in s.parts and str(s)==row["path"],"Unsafe manifest name")
    inside(p);require(p.is_file() and p.stat().st_size==row["bytes"] and sha(p)==row["SHA256"],"Source payload changed: "+str(p));return p
def typed(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return list(a)==list(b) and all(typed(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(typed(x,y)for x,y in zip(a,b))
    return a==b
def main(preseal):
    m=load(R/"SOURCE_READY_MANIFEST.json");require(set(m["excluded_terminal_files"])==EXCLUDED,"Manifest terminal boundary")
    names=[]
    for row in m["files"]:bound(row);names.append(row["path"])
    require(len(names)==len(set(names)) and set(names)=={p.relative_to(R).as_posix() for p in R.rglob("*") if p.is_file()}-EXCLUDED,"Complete source namespace")
    actual_files=[];actual_dirs=[]
    for p in R.rglob("*"):
        mode=p.lstat().st_mode;require(not stat.S_ISLNK(mode),"No source symlink")
        if stat.S_ISDIR(mode):actual_dirs.append(p.relative_to(R).as_posix())
        else:require(stat.S_ISREG(mode),"No source special member");actual_files.append(p.relative_to(R).as_posix())
    require(sorted(actual_dirs)==m["directories"],"Strict complete source directory namespace")
    expected_controls=["SOURCE_READY_MANIFEST.json"] if preseal else sorted(EXCLUDED)
    require(sorted(actual_files)==sorted(names+expected_controls),"Exact entire source files; root terminal exclusions only")
    if preseal:require(not (R/"SOURCE_READY_CLOSURE.json").exists() and not (R/"SOURCE_READY_SEAL.json").exists(),"Preseal cannot ignore existing final controls")
    for item in load(R/"INPUT_MANIFEST.json")["files"]:
        external=Path(item["path"]);require(external.is_file()and external.stat().st_size==item["bytes"]and sha(external)==item["SHA256"],"Whole original policy/helper/queue input binding")
    q=load(R/"QUEUE_BINDING.json");require(q["root_supplied_current_eligibility_confirmed"] is True and q["native_eligibility_literal"]=="Queued — eligible Zenodo paper","Root supplied current eligibility")
    ready=load(R/"SOURCE_READY.json");a=load(R/"ACQUIRED_NATIVE.json");record=load(R/"record.response.body")
    require(record["id"]==q["identity_only"]["record_id"]==ready["record_id"]==a["record_id"],"Native/queue/readiness record")
    require(record["metadata"]["title"]==a["title"]==ready["title"] and record["doi"]==record["metadata"]["doi"]==a["doi"]==ready["DOI"],"Whole native title/DOI identity")
    for field in ["publication_date","created","updated"]:
        v=record["metadata"][field] if field=="publication_date" else record[field]
        require(v==ready[field],"Native date identity")
    require(ready["version"]==record["metadata"].get("version") and ready["version_field_present"]==("version" in record["metadata"]),"Literal native version")
    require(a["latest_record_id"]==record["id"] and ready["all_enumerated_version_ids"]==a["all_version_ids"] and a["version_pagination_exhaustive"] is True,"Actual latest/allversions")
    for obj in a["whole_native_API_objects"]:bound(obj,True)
    objects={x["role"]:load(Path(x["path"])) for x in a["whole_native_API_objects"]}
    latest=objects["latest"]
    require(record.get("status")==latest.get("status")=="published" and record.get("state")==latest.get("state")=="done","Actually published record and current latest")
    require(latest["id"]==record["id"] and latest["doi"]==record["doi"] and latest["conceptrecid"]==record["conceptrecid"],"Latest published identity")
    version_pages=[(role,value) for role,value in objects.items() if role.startswith("versions-page")]
    version_hits=[v for role,page in version_pages for v in page["hits"]["hits"]]
    require(len(version_hits)==len({str(v["id"]) for v in version_hits}) and [v["id"] for v in version_hits]==a["all_version_ids"],"Whole original version enumeration in actual page/hit order")
    for index,(role,page) in enumerate(version_pages):
        total=page["hits"]["total"];count=total if type(total)is int else total.get("value") if isinstance(total,dict) else None
        require(type(count)is int and count==len(version_hits),"Every original API total agrees with exhausted version enumeration")
        nextlink=page.get("links",{}).get("next")
        require(bool(nextlink)==(index+1<len(version_pages)),"Exhaustive actual versions pagination")
        if nextlink:
            receipt=load(R/"ALL_TRANSPORT_RECEIPTS.json")
            following=[x for x in receipt if x["logical_role"]==version_pages[index+1][0] and x["redirect_hop"]==0]
            require(len(following)==1 and following[0]["request_URL"]==nextlink,"Only actual next-version link followed")
    require(any(v["id"]==record["id"] for v in version_hits),"Actual record occurs in complete versions")
    files=objects["files"];entries=files["entries"]
    pairs=list(entries.items()) if isinstance(entries,dict) else [(None,x) for x in entries]
    require(typed([x["original_api_file_object"] for x in a["all_assets_in_original_order"]],record["files"]),"Every original native asset object retained in native order")
    for asset in a["all_assets_in_original_order"]:
        original=asset["original_api_file_object"];matches=[x for key,x in pairs if x.get("key",key)==original["key"]]
        require(len(matches)==1 and typed(matches[0],asset["whole_original_native_files_entry"]),"Whole original file-entry association retained")
    require(a["version_original"]==record["metadata"].get("version") and a["version_field_present"]==("version" in record["metadata"]),"Absent/null/empty/string native version distinction")
    snapshot=load(R/"ROOT_SNAPSHOT_CUSTODY.json")
    for original,copied in zip(snapshot["originals"],snapshot["copies"]):
        p=Path(original["path"]);require(p.stat().st_size==original["bytes"] and sha(p)==original["SHA256"],"Original root supplied snapshot")
        cp=bound(copied,True);require(cp.read_bytes()==p.read_bytes() and typed(load(cp),load(p)),"Whole original typed snapshot wrapper retained")
    cells=load(R/"NATIVE_SHEET_IDENTITY_SUBRANGES.json");metadata=load(R/"NATIVE_SHEET_METADATA.json")
    require(cells["isError"] is False and metadata["isError"] is False,"Both actual native API snapshots succeeded")
    require(cells["structuredContent"]["spreadsheetId"]==metadata["structuredContent"]["spreadsheetId"]=="1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20","Authoritative native Sheet identity")
    row=q["identity_only"]["sheet_row"];matched={}
    for sh in cells["structuredContent"]["sheets"]:
        for block in sh.get("data",[]):
            for i,rd in enumerate(block.get("rowData",[])):
                if block.get("startRow",0)+i+1!=row:continue
                require(sh["properties"]["sheetId"]==1052646184,"Exact Full List tab")
                for j,cell in enumerate(rd.get("values",[])):
                    col=block.get("startColumn",0)+j
                    if col in [22,27]:matched[col]=cell
    require(set(matched)=={22,27} and matched[22]["effectiveValue"]["numberValue"]==record["id"] and matched[27]["effectiveValue"]["stringValue"]=="Queued — eligible Zenodo paper","Only assigned exact W/AB identifiers and eligibility confirmed")
    identity=load(R/"NATIVE_IDENTITY_MATCH.json")
    require(typed(identity["literal_native_cells"],[{"column_zero_based":c,"whole_original_cell":matched[c]} for c in [22,27]]),"Whole assigned native cell objects")
    require(ready["current_native_sheet_and_fresh_published_record_identity_match"] is True and identity["fresh_native_Sheet_read"] is False and identity["root_supplied_fresh_native_snapshot_read"] is True,"Honest root supplied snapshot/direct connector distinction")
    concepts=load(R/"PAIR_NATIVE_IDENTITY.json")
    require(concepts["two_actual_native_concepts_distinct"] is True and concepts["whole_inventory_or_prior_corpus_distinct_work_reconciliation_claimed"] is False,"Bounded pair concept distinction only")
    require(len({str(x["conceptrecid_original"]) for x in concepts["records"]})==2,"Actual pair concept values distinct")
    for x in concepts["records"]:
        p=Path(x["whole_record"]["path"]);require(p.stat().st_size==x["whole_record"]["bytes"] and sha(p)==x["whole_record"]["SHA256"],"Whole pair native record body")
        require(load(p)["id"]==x["record_id"] and typed(load(p)["conceptrecid"],x["conceptrecid_original"]),"Native pair identity literals")
    transports=load(R/"ALL_TRANSPORT_RECEIPTS.json")
    require([x["HTTP_status"] for x in transports]==ready["HTTP_status_sequence"],"Whole original transport order")
    for i,t in enumerate(transports):
        require(t["method"]=="GET" and urlsplit(t["request_URL"]).scheme=="https" and urlsplit(t["request_URL"]).hostname=="zenodo.org","Ordinary native request")
        require(isinstance(t["actual_request_headers_in_sent_order"],list) and isinstance(t["response_headers_in_received_order"],list),"Original ordered headers")
        p=inside(t["body_path"]);require(p.stat().st_size==t["bytes"] and sha(p)==t["SHA256"],"Complete successful/non200 body")
        require(t["whole_native_response_body_complete"] is True and t["error_type"] is None and t["all_received_body_bytes_preserved_before_followup"] is True,"Actual complete native response/failure semantics")
        request=inside(t["actual_sent_request_bytes_path"]);require(request.stat().st_size==t["actual_sent_request_bytes"] and sha(request)==t["actual_sent_request_SHA256"],"Whole actual request bytes")
        u=urlsplit(t["request_URL"]);target=u.path+("?"+u.query if u.query else "")
        expected=("GET "+target+" HTTP/1.1\r\n"+"".join(k+": "+v+"\r\n" for k,v in t["actual_request_headers_in_sent_order"])+"\r\n").encode("latin1")
        require(request.read_bytes()==expected,"Actual whole sent request/header order, no hidden authorization/proxy")
        if t["redirect_hop"]:
            previous=transports[i-1];locations=[v for k,v in previous["response_headers_in_received_order"] if k.lower()=="location"]
            require(len(locations)==1 and urljoin(previous["request_URL"],locations[0])==t["request_URL"],"Only actual native redirect followed")
    for asset in a["all_assets_in_original_order"]:
        p=bound(asset,True);b=p.read_bytes();original=asset["original_api_file_object"];algorithm,expected=original["checksum"].split(":",1)
        require(len(b)==original["size"] and hashlib.new(algorithm,b).hexdigest()==expected,"Native checksum/size")
        require(inside(asset["transport_body_path"]).read_bytes()==b,"Fresh native transport/asset bytes")
        e=asset["whole_original_native_files_entry"];require(e["checksum"]==original["checksum"] and e["size"]==original["size"],"Original record/files-entry association")
    arc=load(R/"ARCHIVE_CUSTODY.json");require(all(c["kind"]=="zip" for c in arc["containers"]),"Actual container family is ZIP");require(arc["nested_archive_count"]==sum(c["container_depth"]>0 for c in arc["containers"]),"Actual nested container count")
    count=0;expanded=0;occurrences=[]
    for container in arc["containers"]:
        p=inside(container["input_path"]);require(sha(p)==container["input_SHA256"],"Actual original container")
        with zipfile.ZipFile(p) as z:
            infos=z.infolist();require(len(infos)==len(container["members"]),"Whole native member count")
            directory=[{"ordinal_zero_based":i,"filename":v.filename,"original_filename":v.orig_filename,"is_directory":v.is_dir(),"bytes":v.file_size,"compressed_bytes":v.compress_size,"CRC32":"%08x"%v.CRC,"flags":v.flag_bits,"compression":v.compress_type,"native_date_time":list(v.date_time),"external_attr":v.external_attr,"internal_attr":v.internal_attr,"create_system":v.create_system,"create_version":v.create_version,"extract_version":v.extract_version,"header_offset":v.header_offset,"extra_hex":v.extra.hex(),"comment_hex":v.comment.hex()}for i,v in enumerate(infos)]
            require(directory==container["whole_original_central_directory"]and z.comment.hex()==container["original_archive_comment_hex"],"Whole original central directory/comment")
            seen=set()
            for info,item in zip(infos,container["members"]):
                require(info.filename==info.orig_filename==item["original_member_name"],"Original member names")
                name=PurePosixPath(info.filename);require(not name.is_absolute() and ".." not in name.parts and "\\" not in info.filename,"Safe member path")
                folded=unicodedata.normalize("NFC",info.filename.rstrip("/")).casefold();require(folded not in seen,"Duplicate/case collision");seen.add(folded)
                mode=stat.S_IFMT(info.external_attr>>16);require(mode in ([0,stat.S_IFDIR] if info.is_dir() else [0,stat.S_IFREG]),"No links/nonregular members")
                require(not(info.flag_bits&1),"No encrypted member")
                if info.is_dir():continue
                body=z.read(info);require(len(body)==info.file_size==item["bytes"] and "%08x"%(zlib.crc32(body)&0xffffffff)==item["CRC32"]=="%08x"%info.CRC,"Native CRC/size")
                require(hashlib.sha256(body).hexdigest()==item["SHA256"] and inside(item["extracted_path"]).read_bytes()==body,"Whole extracted occurrence byte identity")
                nested_zip=zipfile.is_zipfile(io.BytesIO(body))
                linked=[c for c in arc["containers"] if c["parent_occurrence"]=={"container_id":container["container_id"],"ordinal_zero_based":item["ordinal_zero_based"]}]
                require(item["safe_regular_body"] is True,"Occurrence classification")
                if nested_zip:
                    require(item["nested_archive_kind"]=="zip" and len(linked)==1,"Every nested ZIP has one actual child container")
                    child=linked[0];require(child["input_path"]==item["extracted_path"] and child["input_SHA256"]==item["SHA256"] and child["container_depth"]==container["container_depth"]+1,"Nested container whole-byte/depth binding")
                else:
                    require(item["nested_archive_kind"] is None and linked==[] and not body.startswith((b"\x1f\x8b",b"BZh",b"\xfd7zXZ\x00",b"7z\xbc\xaf\x27\x1c",b"Rar!",b"!<arch>")) and not tarfile.is_tarfile(io.BytesIO(body)),"No omitted nested container")
                count+=1;expanded+=len(body);occurrences.append((container["container_id"],item["ordinal_zero_based"]))
    require(count==arc["whole_regular_payload_occurrences"]==ready["whole_regular_payload_occurrences"] and expanded==arc["expanded_bytes_all_depths"],"Complete occurrence/size coverage")
    require(set(occurrences)=={(x["container_id"],x["ordinal_zero_based"]) for x in arc["regular_payload_occurrences"]},"No omitted/duplicated regular occurrence")
    custody=load(R/"MANUSCRIPT_CUSTODY.json")
    native_readers=[x for x in a["all_assets_in_original_order"] if Path(x["path"]).suffix.lower()==".pdf"]
    require(len(native_readers)==len(custody["actual_standalone_readers"]),"ALL actual native PDF assets covered, not merely mutually matching lists")
    for asset,reader in zip(native_readers,custody["actual_standalone_readers"]):
        require(all(k in reader and typed(v,reader[k])for k,v in asset.items()),"Every whole native PDF asset retained in native order")
        require(type(reader["pages"])is int and reader["pages"]>0,"Actual reader page-count metadata type")
    native_tex=[x for x in a["all_assets_in_original_order"] if Path(x["path"]).suffix.lower()==".tex"]
    require(typed(native_tex,custody["actual_standalone_TeX_assets"]) and typed(native_tex,ready["actual_standalone_TeX_assets"]),"ALL actual native standalone TeX assets covered")
    expected_embedded=[x for x in arc["regular_payload_occurrences"] if Path(x["original_member_name"]).suffix.lower()==".pdf" or Path(x["extracted_path"]).read_bytes().startswith(b"%PDF-")]
    require(len(expected_embedded)==len(custody["embedded_PDFs"]),"Every archive PDF occurrence has retained metadata")
    for original,enriched in zip(expected_embedded,custody["embedded_PDFs"]):require(all(k in enriched and typed(v,enriched[k]) for k,v in original.items()),"Whole embedded PDF occurrence retained")
    pdf=custody["selected_actual_PDF"];p=bound(pdf,True);require(p.read_bytes().startswith(b"%PDF-"),"Actual PDF format")
    require(any(typed(pdf,x)for x in custody["actual_standalone_readers"]),"Selected primary is one whole actual native reader")
    require(typed(custody["selected_actual_PDF"],ready["selected_actual_PDF"]) and typed(custody["controlling_TeX"],ready["controlling_TeX"]),"Primary reader/source objects exactly retained inREADY")
    tex=custody["controlling_TeX"];p=Path(tex["extracted_path"]);require(p.stat().st_size==tex["bytes"] and sha(p)==tex["SHA256"] and len(p.read_bytes().splitlines())==tex["opaque_byte_splitlines_count"],"Exact controlling TeX identity")
    require(custody["controlling_TeX_selection_basis"] and ready["source_mapping_is_structural_only_no_typeset_or_scientific_equivalence_certified"] is True,"Metadata-only source selection")
    actual_tex=[x for x in arc["regular_payload_occurrences"] if x["original_member_name"].lower().endswith(".tex")]
    require(typed(actual_tex,custody["all_TeX_candidates"]),"All actual archived TeX candidates preserved in native occurrence order")
    require(len(ready["all_TeX_candidates"])==len(actual_tex),"Every source candidate retained directly inREADY")
    for original,enriched in zip(actual_tex,ready["all_TeX_candidates"]):
        require(all(k in enriched and typed(v,enriched[k]) for k,v in original.items()),"Whole original TeX occurrence object retained")
        require(enriched["opaque_byte_splitlines_count"]==len(Path(original["extracted_path"]).read_bytes().splitlines()) and enriched["preamble_or_mathematical_body_read"] is False,"Opaque line counts only for every source")
    require(typed(ready["controlling_TeX_sources_in_original_archive_order"],ready["all_TeX_candidates"]),"Direct whole-record source list order")
    expected_additional=[x for x in ready["all_TeX_candidates"] if x["SHA256"]!=custody["controlling_TeX"]["SHA256"] or x["extracted_path"]!=custody["controlling_TeX"]["extracted_path"]]
    require(typed(expected_additional,ready["additional_controlling_TeX_sources"]),"Exact additional-source list minus selected source, no dropped extra source")
    associations=ready["native_reader_source_structural_associations"]
    require(len(associations)==len(custody["actual_standalone_readers"]),"Every actual native reader/source link retained")
    for association in associations:
        rr=[x for x in custody["actual_standalone_readers"] if x["original_api_file_object"]["key"]==association["native_PDF_key"]]
        require(len(rr)==1 and rr[0]["SHA256"]==association["native_PDF_SHA256"],"Structural reader identity")
        tt=[x for x in actual_tex if x["original_member_name"]==association["archived_TeX_member"] and x["SHA256"]==association["archived_TeX_SHA256"]]
        require(len(tt)==1,"Structural TeX identity, no typeset/scientific equivalence claim")
    require(len(ready["actual_standalone_readers"])==len(custody["actual_standalone_readers"]),"All native PDF readers directly inREADY")
    for original,enriched in zip(custody["actual_standalone_readers"],ready["actual_standalone_readers"]):
        require(all(k in enriched and typed(v,enriched[k]) for k,v in original.items()),"Whole original native reader object retained")
        require(enriched["scientific_role_or_typeset_equivalence_assessed"] is False and len(enriched["structural_source_associations"])==1,"Every reader has its structural-only source link")
    images=custody["fresh_page_rasters"]
    require(len(images)==sum(x["pages"]for x in custody["actual_standalone_readers"])==ready["all_native_reader_total_pages"],"All actual reader page/raster metadata")
    require(pdf["pages"]==ready["selected_actual_PDF"]["pages"],"Primary reader page metadata")
    for reader in custody["actual_standalone_readers"]:
        bound(reader,True);require(sum(i["native_reader_key"]==reader["original_api_file_object"]["key"] and i["native_reader_SHA256"]==reader["SHA256"] for i in images)==reader["pages"],"Every native reader has complete fresh unread raster coverage")
    for image in images:
        p=bound(image,True);b=p.read_bytes();require(b[:8]==b"\x89PNG\r\n\x1a\n" and struct.unpack(">II",b[16:24])==(image["width"],image["height"]),"Fresh PNG format/dimensions")
        require(image["visually_read"] is False,"Source-only raster exposure")
    require(load(R/"RENDER_RECEIPT.json")["exit_code"]==0 and load(R/"NATIVE_IDENTITY_MATCH.json")["current_native_identifier_and_queued_status_match"] is True and load(R/"NATIVE_IDENTITY_MATCH.json")["actual_native_PDF_checksum_and_size_verified"] is True,"Actual metadata-only render/native identity checks")
    require(ready["printed_date"] is None and ready["printed_version"] is None and ready["printed_title_date_version_inspected"] is False,"Unread printed fields remain literal null")
    require(ready["target_PDF_text_extracted"] is False and ready["mathematical_PDF_TeX_or_pixels_read"] is False and ready["source_programmes_executed"]==[],"No scientific reading or supplied-code execution")
    for obj,key,target in [(record,"conceptrecid","native_conceptrecid_whole_field"),(record["metadata"],"version","native_version_whole_field"),(record["metadata"],"license","native_license_metadata_whole_field"),(record["metadata"],"resource_type","native_resource_type_whole_field")]:
        require(typed({"present":key in obj,"original_value":obj.get(key)},ready[target]),"Exact native whole field presence/value/type: "+target)
    key_input=next(x for x in load(R/"INPUT_MANIFEST.json")["files"] if x["role"]=="base_READY_key_order_only")
    key_schema=load(Path(key_input["path"]));basekeys=key_schema["SOURCE_READY_key_order"]
    suffix=["source_custody_schema_additions","additional_controlling_TeX_sources","controlling_TeX_sources_in_original_archive_order","native_reader_source_structural_associations","whole_record_source_reading_requirement_for_future_science","all_native_reader_total_pages","source_mapping_is_structural_only_no_typeset_or_scientific_equivalence_certified"]
    require(list(ready)==basekeys+suffix and ready["schema"]==key_schema["schema"],"Exact established READY base key-order prefix and declared additive suffix")
    require(type(ready["version_field_present"])is bool and ready["version_field_present"]==("version" in record["metadata"]) and typed(ready["version"],record["metadata"].get("version")),"Native ABSENT/null/empty/string version literal; no defaults")
    expected_distinct={"record_swh":{"present":"swh" in record,"original_value":record.get("swh")},"latest_swh":{"present":"swh" in latest,"original_value":latest.get("swh")},"versions_swh_fields":[{"present":"swh" in x,"original_value":x.get("swh")}for x in version_hits],"versions_total_original_fields":a["all_versions_total_original_fields"],"files_entries_original_type":type(files["entries"]).__name__,"files_order":{"present":"order" in files,"original_value":files.get("order")},"files_default_preview":{"present":"default_preview" in files,"original_value":files.get("default_preview")},"original_header_order_and_duplicates_preserved":True}
    require(typed(expected_distinct,ready["native_schema_distinctions"]),"Literal native absent/null/type/key/list distinctions")
    require(typed(ready["whole_native_API_objects"],a["whole_native_API_objects"]) and typed(ready["all_native_assets_in_original_order"],a["all_assets_in_original_order"]),"Whole original API/asset objects retained with exact types and key/list order")
    shapes=[]
    def walk(x,path,role):
        item={"role":role,"JSON_pointer":path,"original_type":type(x).__name__}
        if x is None or x=={} or x==[]:item["original_empty_or_null_value"]=x
        shapes.append(item)
        if isinstance(x,dict):
            for k,v in x.items():walk(v,path+"/"+str(k).replace("~","~0").replace("/","~1"),role)
        elif isinstance(x,list):
            for i,v in enumerate(x):walk(v,path+"/"+str(i),role)
    for obj in a["whole_native_API_objects"]:walk(load(Path(obj["path"])),"",obj["role"])
    require(typed(shapes,load(R/"NATIVE_SCHEMA_TYPES.json")),"Whole native schema type/empty/null map")
    literal=load(R/"NATIVE_ORIGINAL_OBJECTS.json")
    require(len(literal)==len(a["whole_native_API_objects"]),"Whole literal native object count")
    for original,copied in zip(a["whole_native_API_objects"],literal):
        require(copied["role"]==original["role"] and typed(copied["original_body_binding"],original) and typed(copied["whole_original_object"],load(Path(original["path"]))),"Whole original native objects/order/types/nulls preserved")
    require(ready["scientific_verdict"] is None and ready["publication_authority"] is False,"Source-only authority")
    require(all(not arc[k] for k in ["unsafe_names","duplicate_or_case_colliding_names","nonregular_payloads","unsupported_nested_magic"]),"Archive fail-closed boundaries")
    if not preseal:
        seal=load(R/"SOURCE_READY_SEAL.json")
        for f,k in [("SOURCE_READY.json","SOURCE_READY_SHA256"),("SOURCE_READY_MANIFEST.json","MANIFEST_SHA256"),("SOURCE_READY_CLOSURE.json","CLOSURE_SHA256")]:require(sha(R/f)==seal[k],"Final source seal")
        require(seal["owned_payload_count"]==len(names),"Final source extent")
    print(json.dumps({"status":"SOURCE_CUSTODY_PASS","record_id":ready["record_id"],"mode":"preseal" if preseal else "sealed","checks":N,"owned_payloads":len(names),"whole_regular_payload_occurrences":count,"nested_archives":arc["nested_archive_count"],"PDF_pages":pdf["pages"],"all_native_reader_pages":ready["all_native_reader_total_pages"],"native_readers":len(custody["actual_standalone_readers"]),"TeX_sources":len(actual_tex),"TeX_lines":tex["opaque_byte_splitlines_count"],"actual_HTTP_requests":len(transports),"scientific_reading_or_execution":False,"network_requests":0,"writes":0},sort_keys=True))
if __name__=="__main__":
    require(sys.argv[1:] in [[],["--preseal"]],"Usage: verify_custody.py [--preseal]")
    main(sys.argv[1:]==["--preseal"])
