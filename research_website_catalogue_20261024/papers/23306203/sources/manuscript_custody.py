#!/usr/bin/env python3
"""Source-only PDF/page-image/TeX identity, with no text extraction or visual reading."""
from pathlib import Path
import datetime,hashlib,json,struct,subprocess,re
R=Path(__file__).resolve().parent
def require(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pagecount(path):
    result=subprocess.run(["pdfinfo",str(path)],capture_output=True,check=True,text=True)
    match=re.search(r"^Pages:\s+(\d+)\s*$",result.stdout,re.M)
    require(match is not None,"PDF page count missing from native parser metadata")
    return int(match.group(1))
def main():
    a=json.loads((R/"ACQUIRED_NATIVE.json").read_text());arc=json.loads((R/"ARCHIVE_CUSTODY.json").read_text())
    pdfs=[z for z in a["all_assets_in_original_order"] if Path(z["path"]).suffix.lower()==".pdf"]
    require(len(pdfs)==1,"Ambiguous actual standalone reader")
    selected=dict(pdfs[0]);pdf=Path(selected["path"]);count=pagecount(pdf)
    selected.update({"pages":count,"text_extracted":False,"pages_visually_or_scientifically_read":False,"actual_standalone_API_asset":True})
    texs=[dict(z) for z in arc["regular_payload_occurrences"] if z["original_member_name"].lower().endswith(".tex")]
    native_tex=[z for z in a["all_assets_in_original_order"] if Path(z["path"]).suffix.lower()==".tex"]
    require(len(texs)==1,"Controlling TeX requires further metadata-only selection")
    controlling=dict(texs[0]);t=Path(controlling["extracted_path"]);controlling["opaque_byte_splitlines_count"]=len(t.read_bytes().splitlines());controlling["preamble_or_mathematical_body_read"]=False
    embedded=[]
    for z in arc["regular_payload_occurrences"]:
        p=Path(z["extracted_path"])
        if p.read_bytes()[:5]==b"%PDF-":
            pcount=pagecount(p)
            embedded.append(dict(z)|{"pages":pcount,"identical_to_standalone_published_PDF":z["SHA256"]==selected["SHA256"],"body_or_pixels_scientifically_read":False})
    if native_tex:
        require(len(native_tex)==1 and native_tex[0]["SHA256"]==controlling["SHA256"] and Path(native_tex[0]["path"]).stem==pdf.stem,"Standalone source/archived source/PDF filename binding mismatch")
        basis="sole archived TeX, byte-identical to actual native standalone TeX with same basename as actual native PDF; no source body read"
    else:
        adjacent=any(Path(z["extracted_path"]).parent==t.parent and z["identical_to_standalone_published_PDF"] for z in embedded)
        basis=("sole archived TeX, adjacent archived PDF byte-identical to actual native standalone reader; no preamble or source body read" if adjacent else "sole archived TeX with same basename as sole actual native PDF; co-deposited source identity only, no source body or build correspondence certified" if t.stem==pdf.stem else "sole archived TeX occurrence in original source container with byte-identical embedded native PDF elsewhere in the same archive; structural association only, no source body or build correspondence certified" if any(z["identical_to_standalone_published_PDF"]for z in embedded) else "sole archived TeX occurrence co-deposited with sole actual native standalone PDF; source identity only, no body or build correspondence certified")
    out=R/"rasters";out.mkdir();argv=["pdftoppm","-r","145","-png",str(pdf),str(out/"page")]
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(argv,capture_output=True)
    receipt={"started_UTC":start,"completed_UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"argv":argv,"exit_code":p.returncode,"stdout":p.stdout.decode(errors="replace"),"stderr":p.stderr.decode(errors="replace"),"images_opened_or_emitted_or_visually_read":False}
    (R/"RENDER_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n");require(p.returncode==0,"Fresh raster generation failure")
    rasters=[]
    for path in sorted(out.glob("page-*.png")):
        b=path.read_bytes();require(b[:8]==b"\x89PNG\r\n\x1a\n","PNG signature")
        width,height=struct.unpack(">II",b[16:24]);rasters.append({"path":str(path),"bytes":len(b),"SHA256":sha(b),"width":width,"height":height,"visually_read":False})
    require(len(rasters)==count,"Fresh page-raster count mismatch")
    originals=[json.loads((R/name).read_text())["structuredContent"]for name in ["NATIVE_SHEET_IDENTITY_SUBRANGES.json","NATIVE_SHEET_MANUSCRIPT_SUBRANGES.json"]];cells={}
    for s in [s for native in originals for s in native["sheets"]]:
        if s["properties"]["sheetId"]!=1052646184:continue
        for group in s["data"]:
            sr=group.get("startRow",0);sc=group.get("startColumn",0)
            for i,row in enumerate(group.get("rowData",[])):
                for j,cell in enumerate(row.get("values",[])):cells[(sr+i+1,sc+j)]=cell
    queue=json.loads((R/"QUEUE_BINDING.json").read_text())["identity_only"];row=queue["sheet_row"]
    def value(col):
        c=cells.get((row,col),{});return c.get("formattedValue")
    require(value(1)==a["title"] and value(11)=="https://doi.org/"+a["doi"] and value(12)=="https://zenodo.org/records/"+str(a["record_id"]),"Current native sheet exact identity mismatch")
    require(value(13)==a["publication_date"] and value(22)==str(a["record_id"]) and value(23)=="Z-"+str(a["conceptrecid"]),"Current sheet date/work identity mismatch")
    sheet_version_unsupplied=value(14)=="Not supplied"
    require(sheet_version_unsupplied or value(14)==a["version_original"],"Known current sheet/native edition mismatch")
    require(value(27)=="Queued — eligible Zenodo paper","Current native status is not queued")
    require(value(21)==pdf.name and value(25)==pdf.name+": "+selected["SHA256"],"Current sheet actual manuscript checksum mismatch")
    identity={"sheet_tab":"Full List","sheetId":1052646184,"row":row,"literal_native_cells":[{"column_zero_based":c,"present_in_returned_data":(row,c)in cells,"whole_original_cell":cells.get((row,c))} for c in [0,1,11,12,13,14,15,16,21,22,23,25,27,28]],"native_sheet_version_string_original":value(14),"native_API_version_field_present":a["version_field_present"],"native_API_version_original":a["version_original"],"sheet_version_unsupplied":sheet_version_unsupplied,"queue_and_fresh_native_record_match":True,"actual_native_PDF_SHA256_matches_current_sheet":True,"scientific_assessment_columns_read":False}
    (R/"NATIVE_IDENTITY_MATCH.json").write_text(json.dumps(identity,indent=2,ensure_ascii=False)+"\n")
    result={"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"record_id":a["record_id"],"selected_actual_PDF":selected,"actual_standalone_readers":[selected],"controlling_TeX":controlling,"controlling_TeX_selection_basis":basis,"all_TeX_candidates":texs,"actual_standalone_TeX_assets":native_tex,"embedded_PDFs":embedded,"fresh_page_rasters":rasters,"PDF_pages":count,"source_byte_line_count":controlling["opaque_byte_splitlines_count"],"printed_title_date_version_inspected":False,"printed_date":None,"printed_version":None,"PDF_text_extracted":False,"mathematical_PDF_TeX_or_pixels_read":False}
    (R/"MANUSCRIPT_CUSTODY.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    # Type-only JSON views retain all raw originals; description strings are never displayed.
    schemas=[]
    def walk(x,path,role):
        item={"role":role,"JSON_pointer":path,"original_type":type(x).__name__}
        if x is None or x=={} or x==[]:item["original_empty_or_null_value"]=x
        schemas.append(item)
        if isinstance(x,dict):
            for key,value in x.items():walk(value,path+"/"+str(key).replace("~","~0").replace("/","~1"),role)
        elif isinstance(x,list):
            for i,value in enumerate(x):walk(value,path+"/"+str(i),role)
    for obj in a["whole_native_API_objects"]:walk(json.loads(Path(obj["path"]).read_bytes()),"",obj["role"])
    (R/"NATIVE_SCHEMA_TYPES.json").write_text(json.dumps(schemas,indent=2,ensure_ascii=False)+"\n")
    (R/"SOURCE_LOG.md").open("a").write("\n"+result["UTC"]+" — 80%: All original regular occurrences CRC/size/SHA checked; actual nested-container counts retained in archive custody. Sole controlling archived TeX selected by file identity/adjacent exact native PDF or exact standalone TeX; source text remains unread. Actual PDF page counts and fresh per-page raster hashes recorded without opening images. Current bounded native identity/SHA checks pass; printed fields remain null/unread.\n")
    print(json.dumps({"record_id":a["record_id"],"PDF_pages":count,"TeX_bytes":controlling["bytes"],"TeX_lines":controlling["opaque_byte_splitlines_count"],"controlling_TeX_path":controlling["extracted_path"],"controlling_TeX_SHA256":controlling["SHA256"],"fresh_unread_rasters":len(rasters),"printed_fields":None},indent=2))
if __name__=="__main__":main()
