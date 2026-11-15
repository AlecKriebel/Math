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
def main(preseal):
    m=load(R/"SOURCE_READY_MANIFEST.json");require(set(m["excluded_terminal_files"])==EXCLUDED,"Manifest terminal boundary")
    names=[]
    for row in m["files"]:bound(row);names.append(row["path"])
    require(len(names)==len(set(names)) and set(names)=={p.relative_to(R).as_posix() for p in R.rglob("*") if p.is_file()}-EXCLUDED,"Complete source namespace")
    for item in load(R/"INPUT_MANIFEST.json")["files"]:
        external=Path(item["path"]);require(external.is_file()and external.stat().st_size==item["bytes"]and sha(external)==item["SHA256"],"Whole original policy/helper/queue input binding")
    q=load(R/"QUEUE_BINDING.json");qp=Path(q["queue_path"]);require(qp.stat().st_size==q["whole_queue_bytes"] and sha(qp)==q["whole_queue_SHA256"],"Preserved203reconciliation changed")
    ready=load(R/"SOURCE_READY.json");a=load(R/"ACQUIRED_NATIVE.json");record=load(R/"record.response.body")
    require(record["id"]==q["identity_only"]["record_id"]==ready["record_id"]==a["record_id"],"Native/queue/readiness record")
    require(record["metadata"]["title"]==q["identity_only"]["title"]==ready["title"] and record["doi"]==q["identity_only"]["doi"]==ready["DOI"],"Title/DOI identity")
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
    require([x["original_api_file_object"] for x in a["all_assets_in_original_order"]]==record["files"],"Every original native asset object retained in native order")
    for asset in a["all_assets_in_original_order"]:
        original=asset["original_api_file_object"];matches=[x for key,x in pairs if x.get("key",key)==original["key"]]
        require(len(matches)==1 and matches[0]==asset["whole_original_native_files_entry"],"Whole original file-entry association retained")
    require(a["version_original"]==record["metadata"].get("version") and a["version_field_present"]==("version" in record["metadata"]),"Absent/null/empty/string native version distinction")
    distinct=load(R/"NATIVE_DISTINCT_WORK_CHECK.json");require(distinct["same_concept_prior_SOURCE_READY_packets"]==[] and len(distinct["opaque_queue_identity_matches"])==1,"No duplicate distinct-work source packet")
    transports=load(R/"ALL_TRANSPORT_RECEIPTS.json")
    require([x["HTTP_status"] for x in transports]==ready["HTTP_status_sequence"],"Whole original transport order")
    for i,t in enumerate(transports):
        require(t["method"]=="GET" and urlsplit(t["request_URL"]).scheme=="https" and urlsplit(t["request_URL"]).hostname=="zenodo.org","Ordinary native request")
        require(isinstance(t["actual_request_headers_in_sent_order"],list) and isinstance(t["response_headers_in_received_order"],list),"Original ordered headers")
        p=inside(t["body_path"]);require(p.stat().st_size==t["bytes"] and sha(p)==t["SHA256"],"Complete successful/non200 body")
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
    custody=load(R/"MANUSCRIPT_CUSTODY.json");pdf=custody["selected_actual_PDF"];p=bound(pdf,True);require(p.read_bytes().startswith(b"%PDF-"),"Actual PDF format")
    tex=custody["controlling_TeX"];p=Path(tex["extracted_path"]);require(p.stat().st_size==tex["bytes"] and sha(p)==tex["SHA256"] and len(p.read_bytes().splitlines())==tex["opaque_byte_splitlines_count"],"Exact controlling TeX identity")
    require(len(custody["all_TeX_candidates"])==1 and custody["controlling_TeX_selection_basis"],"Metadata-only source selection")
    images=custody["fresh_page_rasters"];require(len(images)==pdf["pages"]==ready["selected_actual_PDF"]["pages"],"Actual page/raster metadata")
    for image in images:
        p=bound(image,True);b=p.read_bytes();require(b[:8]==b"\x89PNG\r\n\x1a\n" and struct.unpack(">II",b[16:24])==(image["width"],image["height"]),"Fresh PNG format/dimensions")
        require(image["visually_read"] is False,"Source-only raster exposure")
    require(load(R/"RENDER_RECEIPT.json")["exit_code"]==0 and load(R/"NATIVE_IDENTITY_MATCH.json")["current_native_identifier_and_queued_status_match"] is True and load(R/"NATIVE_IDENTITY_MATCH.json")["actual_native_PDF_checksum_and_size_verified"] is True,"Actual metadata-only render/native identity checks")
    require(ready["printed_date"] is None and ready["printed_version"] is None and ready["printed_title_date_version_inspected"] is False,"Unread printed fields remain literal null")
    require(ready["target_PDF_text_extracted"] is False and ready["mathematical_PDF_TeX_or_pixels_read"] is False and ready["source_programmes_executed"]==[],"No scientific reading or supplied-code execution")
    require(ready["scientific_verdict"] is None and ready["publication_authority"] is False,"Source-only authority")
    require(all(not arc[k] for k in ["unsafe_names","duplicate_or_case_colliding_names","nonregular_payloads","unsupported_nested_magic"]),"Archive fail-closed boundaries")
    if not preseal:
        seal=load(R/"SOURCE_READY_SEAL.json")
        for f,k in [("SOURCE_READY.json","SOURCE_READY_SHA256"),("SOURCE_READY_MANIFEST.json","MANIFEST_SHA256"),("SOURCE_READY_CLOSURE.json","CLOSURE_SHA256")]:require(sha(R/f)==seal[k],"Final source seal")
        require(seal["owned_payload_count"]==len(names),"Final source extent")
    print(json.dumps({"status":"SOURCE_CUSTODY_PASS","record_id":ready["record_id"],"mode":"preseal" if preseal else "sealed","checks":N,"owned_payloads":len(names),"whole_regular_payload_occurrences":count,"nested_archives":arc["nested_archive_count"],"PDF_pages":pdf["pages"],"TeX_lines":tex["opaque_byte_splitlines_count"],"actual_HTTP_requests":len(transports),"scientific_reading_or_execution":False,"network_requests":0,"writes":0},sort_keys=True))
if __name__=="__main__":
    require(sys.argv[1:] in [[],["--preseal"]],"Usage: verify_custody.py [--preseal]")
    main(sys.argv[1:]==["--preseal"])
