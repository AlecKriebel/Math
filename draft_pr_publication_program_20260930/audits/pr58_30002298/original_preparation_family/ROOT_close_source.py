import datetime,json,os,sys
from packet_common import HERE,prepared_check,sha,mode,topology
assert sys.argv[1:]==["--root-only-close-after-reading"]
assert not (HERE/"SELF_MANIFEST.json").exists()
idx,ready,controls=prepared_check(False)
files,dirs=topology();rows=[]
for rel in files:
    path=HERE/rel;body=path.read_bytes()
    rows.append({"path":rel,"bytes":len(body),"sha256":sha(body),"mode":mode(path)})
rows.append({"path":"SELF_MANIFEST.json","bytes":None,"sha256":"LITERAL_SELF_REFERENCE_NOT_A_DIGEST","mode":"0444"})
record={"schema":"pr58-original-closed-source-manifest/v1","actual_ROOT_closer_pid":os.getpid(),"actual_UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"files":sorted(rows,key=lambda x:x["path"]),"directories":dirs,"scope":"Original SOURCE custody only; no mathematical or priority acceptance","root_approval":False,"native_acceptance":False}
body=(json.dumps(record,indent=2)+"\n").encode()
fd=os.open(str(HERE/"SELF_MANIFEST.json"),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
with os.fdopen(fd,"wb") as stream:
    stream.write(body);stream.flush();os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno())
prepared_check(True)
print(json.dumps({"status":"PASS_ORIGINAL_SOURCE_ROOT_CLOSURE_ONLY","actual_closer_pid":os.getpid(),"manifest_sha256":sha(body),"prepared_files":len(files),**controls,"root_approval":False,"native_acceptance":False}))
