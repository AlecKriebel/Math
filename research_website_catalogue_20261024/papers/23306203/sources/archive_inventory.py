#!/usr/bin/env python3
"""Fresh namespace/CRC/nested-occurrence custody. Never interprets source mathematics."""
from pathlib import Path,PurePosixPath
import bz2,datetime,gzip,hashlib,io,json,lzma,stat,tarfile,unicodedata,zipfile
R=Path(__file__).resolve().parent
LIMIT=64*1024*1024
TOTAL_LIMIT=128*1024*1024
containers=[];payloads=[];expanded=0
def require(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def safe(name,isdir):
    require(isinstance(name,str) and name and "\x00" not in name and "\\" not in name,"Unsafe original archive name")
    base=name[:-1] if isdir and name.endswith("/") else name
    p=PurePosixPath(base)
    require(base and not p.is_absolute() and ".." not in p.parts and "." not in p.parts and str(p)==base and ":" not in p.parts[0],"Noncanonical/traversing archive name")
    return base
def kind(b,name):
    if zipfile.is_zipfile(io.BytesIO(b)):return "zip"
    if b.startswith(b"7z\xbc\xaf\x27\x1c") or b.startswith(b"Rar!") or b.startswith(b"!<arch>"):return "unsupported"
    if b.startswith((b"PK\x03\x04",b"PK\x05\x06",b"PK\x07\x08")):return "unsupported"
    if b.startswith(b"\x1f\x8b"):return "gzip"
    if b.startswith(b"BZh"):return "bz2"
    if b.startswith(b"\xfd7zXZ\x00"):return "xz"
    if len(b)>262 and b[257:262]==b"ustar":return "tar"
    if str(name).lower().endswith((".tar",".tgz",".tar.gz",".tar.bz2",".tar.xz")):
        try:
            with tarfile.open(fileobj=io.BytesIO(b),mode="r:*"):return "tar"
        except tarfile.TarError:raise RuntimeError("Named archive is not safely recognized: "+name)
    return None
def scan(data,input_path,output,depth,parent_occurrence=None):
    global expanded
    require(depth<=12,"Nested depth cap");k=kind(data,str(input_path));require(k and k!="unsupported","Unsupported nested/container magic")
    if k in ["gzip","bz2","xz"]:
        try:
            with tarfile.open(fileobj=io.BytesIO(data),mode="r:*"):k="tar"
        except tarfile.TarError:pass
    cid="container-%03d"%(len(containers)+1)
    c={"container_id":cid,"container_depth":depth,"input_path":str(input_path),"input_bytes":len(data),"input_SHA256":sha(data),"kind":k,"parent_occurrence":parent_occurrence,"extraction_root":str(output),"members":[]}
    containers.append(c);output.mkdir(parents=True,exist_ok=False)
    names={};file_names=set();directory_names=set()
    def namespace(name,isdir):
        clean=safe(name,isdir);norm=unicodedata.normalize("NFC",clean).casefold()
        require(norm not in names,"Duplicate/case-colliding namespace: "+name);names[norm]=name
        parts=norm.split("/")
        for i in range(1,len(parts)):require("/".join(parts[:i]) not in file_names,"File/directory prefix collision")
        if not isdir:
            require(norm not in directory_names and not any(x.startswith(norm+"/") for x in names if x!=norm),"File/directory namespace collision")
            file_names.add(norm)
        else:directory_names.add(norm)
        return clean
    def store(name,body,metadata,ordinal):
        global expanded
        expanded+=len(body);require(len(body)<=LIMIT and expanded<=TOTAL_LIMIT,"Expanded-size cap")
        target=output/safe(name,False);target.parent.mkdir(parents=True,exist_ok=True);require(not target.exists(),"Extraction overwrite");target.write_bytes(body)
        nested=kind(body,name)
        occurrence={"container_id":cid,"container_depth":depth,"ordinal_zero_based":ordinal,"original_member_name":name,"extracted_path":str(target),"bytes":len(body),"SHA256":sha(body),"safe_regular_body":True,"nested_archive_kind":nested}|metadata
        payloads.append(occurrence);c["members"].append(occurrence)
        require(nested!="unsupported","Unsupported nested archive body, retained and blocked")
        if nested:scan(body,target,R/"nested"/("%s-member%04d"%(cid,ordinal)),depth+1,{"container_id":cid,"ordinal_zero_based":ordinal})
    if k=="zip":
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            infos=z.infolist()
            c["original_archive_comment_hex"]=z.comment.hex()
            c["whole_original_central_directory"]=[{"ordinal_zero_based":i,"filename":t.filename,"original_filename":t.orig_filename,"is_directory":t.is_dir(),"bytes":t.file_size,"compressed_bytes":t.compress_size,"CRC32":"%08x"%t.CRC,"flags":t.flag_bits,"compression":t.compress_type,"native_date_time":list(t.date_time),"external_attr":t.external_attr,"internal_attr":t.internal_attr,"create_system":t.create_system,"create_version":t.create_version,"extract_version":t.extract_version,"header_offset":t.header_offset,"extra_hex":t.extra.hex(),"comment_hex":t.comment.hex()}for i,t in enumerate(infos)]
            for i,t in enumerate(infos):
                require(t.orig_filename==t.filename,"NUL-truncated ZIP filename")
                isdir=t.is_dir();namespace(t.filename,isdir)
                mode=stat.S_IFMT(t.external_attr>>16)
                require(not (t.flag_bits&1),"Encrypted member")
                require(mode in ([0,stat.S_IFDIR] if isdir else [0,stat.S_IFREG]),"Nonregular or symlink ZIP member")
                meta={"CRC32":"%08x"%t.CRC,"compressed_bytes":t.compress_size,"compression_method":t.compress_type,"native_external_attr":t.external_attr,"native_create_system":t.create_system,"native_flags":t.flag_bits,"native_date_time":list(t.date_time)}
                if isdir:c["members"].append({"ordinal_zero_based":i,"original_member_name":t.filename,"directory":True}|meta);continue
                require(t.file_size<=LIMIT,"Declared expanded member exceeds cap")
                with z.open(t) as f:body=f.read(LIMIT+1)
                require(len(body)==t.file_size,"ZIP native size/CRC read discrepancy")
                store(t.filename,body,meta,i)
    elif k=="tar":
        with tarfile.open(fileobj=io.BytesIO(data),mode="r:*") as z:
            for i,t in enumerate(z.getmembers()):
                isdir=t.isdir();namespace(t.name,isdir)
                meta={"native_type_hex":t.type.hex(),"native_mode":t.mode,"native_uid":t.uid,"native_gid":t.gid,"native_mtime":t.mtime,"native_linkname":t.linkname,"native_pax_headers":t.pax_headers}
                require(isdir or (t.isfile() and not t.issym() and not t.islnk()),"Nonregular TAR member")
                if isdir:c["members"].append({"ordinal_zero_based":i,"original_member_name":t.name,"directory":True}|meta);continue
                require(t.size<=LIMIT,"TAR size cap");f=z.extractfile(t);require(f is not None,"Missing TAR regular payload");body=f.read(LIMIT+1);require(len(body)==t.size,"TAR size mismatch");store(t.name,body,meta,i)
    else:
        opener={"gzip":gzip.GzipFile,"bz2":bz2.BZ2File,"xz":lzma.LZMAFile}[k]
        with opener(io.BytesIO(data),"rb") as f:body=f.read(LIMIT+1)
        require(len(body)<=LIMIT,"Single compressed payload cap");namespace("expanded-payload.bin",False);store("expanded-payload.bin",body,{"original_compressed_member_name_not_invented":True},0)
    return cid
def main():
    a=json.loads((R/"ACQUIRED_NATIVE.json").read_text());top=[]
    for asset in a["all_assets_in_original_order"]:
        p=Path(asset["path"]);b=p.read_bytes();k=kind(b,p.name)
        require(k!="unsupported","Unsupported original archive magic")
        if k:top.append({"asset_path":str(p),"container_id":scan(b,p,R/"published-source"/("asset-%03d"%(asset["ordinal_zero_based"]+1)),0)})
    require(top,"No complete original archive")
    result={"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"record_id":a["record_id"],"top_level_archives":top,"containers":containers,"regular_payload_occurrences":payloads,"top_level_archive_count":len(top),"recursive_archive_container_count":len(containers),"nested_archive_count":sum(c["container_depth"]>0 for c in containers),"whole_regular_payload_occurrences":len(payloads),"expanded_bytes_all_depths":expanded,"unsafe_names":[],"duplicate_or_case_colliding_names":[],"nonregular_payloads":[],"unsupported_nested_magic":[],"CRC_and_native_size_verified_by_full_reads":True,"source_mathematical_bodies_scientifically_read":False,"source_programmes_executed":[]}
    (R/"ARCHIVE_CUSTODY.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({k:result[k] for k in ["record_id","top_level_archive_count","recursive_archive_container_count","nested_archive_count","whole_regular_payload_occurrences","expanded_bytes_all_depths"]}))
if __name__=="__main__":main()
