from pathlib import Path
import hashlib,io,json,subprocess,sys,zipfile
p=Path("draft_pr_actual_claims_1000_1100_20261012/audits/pr1064_30001073/preprint_v1_0").resolve()
def require(c,m):
 if not c:raise ValueError(m)
allow=json.loads((p/"SUPPORT_ALLOWLIST.json").read_text())["members"]
buf=io.BytesIO()
with zipfile.ZipFile(p/"support.zip") as existing:
 require(existing.testzip() is None,"CRC")
 require([i.filename for i in existing.infolist()]==allow,"names/order")
 for info in existing.infolist():
  require(info.date_time==(2026,10,14,0,0,0) and info.create_system==3 and info.external_attr==0o100644<<16 and info.internal_attr==0 and info.compress_type==zipfile.ZIP_DEFLATED and not info.flag_bits&1,"headers")
  b=existing.read(info);require(b==(p/info.filename).read_bytes(),"payload")
  if info.filename!="paper.pdf":b.decode("utf8")
with zipfile.ZipFile(buf,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as rebuilt:
 for name in allow:
  info=zipfile.ZipInfo(name,date_time=(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.internal_attr=0;info.compress_type=zipfile.ZIP_DEFLATED
  rebuilt.writestr(info,(p/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
require(buf.getvalue()==(p/"support.zip").read_bytes(),"closed rebuild")
rows=[]
for optimized in [False,True]:
 argv=[sys.executable,"-I","-B"]+(["-O"] if optimized else [])+[str(p/"verify_package.py"),"--require-deposit-binding"]
 r=subprocess.run(argv,cwd=p,capture_output=True,text=True)
 require(r.returncode==0,"current verifier failed "+r.stderr)
 rows.append({"argv":argv,"returncode":r.returncode,"stdout":r.stdout,"stderr":r.stderr})
tool=p.parents[3]/"zenodo_deposit_tool/zenodo.py"
require(tool.is_file(),"uploader absent")
argv=[sys.executable,"-I","-B",str(tool),"check",str(p/"publication/zenodo-deposit.json")]
r=subprocess.run(argv,cwd=p,capture_output=True,text=True)
require(r.returncode==0,"local native check "+r.stderr)
rows.append({"argv":argv,"returncode":r.returncode,"stdout":r.stdout,"stderr":r.stderr})
print(json.dumps({"pass":True,"candidate_unchanged":True,"independent_CLOSED_zip_equal":True,"all_members":len(allow),"archive_bytes":len(buf.getvalue()),"archive_sha256":hashlib.sha256(buf.getvalue()).hexdigest(),"actual_commands":rows},indent=2))
