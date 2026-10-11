import json,os,sys
from packet_common import HERE,prepared_check,sha,mode,topology
assert len(sys.argv)==3 and sys.argv[1]=="--root-only-read-after-close" and len(sys.argv[2])==64
body=(HERE/"SELF_MANIFEST.json").read_bytes();assert sha(body)==sys.argv[2]
m=json.loads(body);assert m["schema"]=="pr58-original-closed-source-manifest/v1" and m["root_approval"] is False and m["native_acceptance"] is False
idx,ready,controls=prepared_check(True);files,dirs=topology()
assert dirs==m["directories"] and {x["path"] for x in m["files"]}==set(files) and len(m["files"])==len(files)
for row in m["files"]:
    if row["path"]=="SELF_MANIFEST.json":
        assert row=={"path":"SELF_MANIFEST.json","bytes":None,"sha256":"LITERAL_SELF_REFERENCE_NOT_A_DIGEST","mode":"0444"} and mode(HERE/"SELF_MANIFEST.json")=="0444"
    else:
        p=HERE/row["path"];b=p.read_bytes();assert len(b)==row["bytes"] and sha(b)==row["sha256"] and mode(p)==row["mode"]=="0444"
print(json.dumps({"status":"PASS_SEPARATE_ORIGINAL_SOURCE_READBACK_ONLY","actual_reader_pid":os.getpid(),"actual_closer_pid":m["actual_ROOT_closer_pid"],"manifest_sha256":sys.argv[2],"closed_files":len(files),**controls,"root_approval":False,"native_Git_writes":False}))
