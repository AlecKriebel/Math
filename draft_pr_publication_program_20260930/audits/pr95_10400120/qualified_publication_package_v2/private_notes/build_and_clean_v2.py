from pathlib import Path
import datetime,hashlib,json,shutil,sys,zipfile
from capture_v2 import capture,sha,dump
P=Path(__file__).resolve().parent.parent;N=P/"private_notes";F=P/"publicfiles"
run=N/"assembled_run";d=json.loads((run/"results.json").read_text())
if d["status"]!="PASS_EXACT_SPECIALIZATION" or d["note_sha256"]!=sha(F/"pr95_note.tex"):raise RuntimeError("assembly binding")
shutil.copyfile(run/"results.json",F/"verification/recorded_results.json")
pub=F/"verification/recorded_processes";pub.mkdir()
for sub in sorted(run.iterdir()):
 if not sub.is_dir():continue
 target=pub/sub.name;target.mkdir()
 for file in sub.iterdir():
  if file.is_file() and (file.name in ("process.json","stdout.bin","stderr.bin","verification.json") or file.name.startswith("input_")):
   shutil.copyfile(file,target/file.name)
base=json.loads((F/"PAYLOAD_MANIFEST.json").read_text())["files"]
members=[e["file"] for e in base]+["verification/recorded_results.json"]+[f.relative_to(F).as_posix() for f in sorted(pub.rglob("*")) if f.is_file()]
entries=[{"file":s,"bytes":(F/s).stat().st_size,"sha256":sha(F/s)} for s in sorted(members)]
dump(F/"PAYLOAD_MANIFEST.json",{"schema":"pr95-support-payload/v1","files":entries,
 "hash_scope":"Every V2 support archive member except this manifest. Establish trusted external ZIP digest.",
 "recorded_run_manifest":"Fresh V2 assembly bound 10 current input members; expanded manifest additionally binds current recorded evidence. V1 evidence remains preserved in frozen sibling, not promoted to V2 runs."})
members.append("PAYLOAD_MANIFEST.json")
with zipfile.ZipFile(F/"pr95_support.zip","w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name in sorted(members):
  info=zipfile.ZipInfo(name,date_time=(2026,10,5,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
  z.writestr(info,(F/name).read_bytes())
extract=N/"clean_extracted";extract.mkdir()
with zipfile.ZipFile(F/"pr95_support.zip") as z:
 names=z.namelist()
 if len(names)!=len(set(names)) or set(names)!=set(members):raise RuntimeError("ZIP member coverage")
 for info in z.infolist():
  q=Path(info.filename)
  if q.is_absolute() or ".." in q.parts or ((info.external_attr>>16)&0o170000)==0o120000:raise RuntimeError("unsafe ZIP member")
  if z.read(info.filename)!=(F/info.filename).read_bytes():raise RuntimeError("ZIP bytes differ")
 z.extractall(extract)
for name in members:
 if sha(extract/name)!=sha(F/name):raise RuntimeError("extracted digest mismatch")
dump(N/"ARCHIVE_INTEGRITY.json",{"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"archive_sha256":sha(F/"pr95_support.zip"),"members":len(members),"payload_members":len(entries),"all_member_bytes_match_public":True,"all_extracted_bytes_match_public":True,"safe_paths_no_duplicate_or_symlink_members":True,"exact_members":sorted(members)})
names=["pr95_note.pdf","pr95_note.tex","pr95_support.zip","PR95_PRIORITY_QUALIFICATION.md","README.md","LICENSE.txt"]
(F/"SHA256SUMS.txt").write_text("\n".join(sha(F/name)+"  "+name for name in names)+"\n")
r=capture("clean_archive",[sys.executable,"-E","-B",str(extract/"verification/run_all.py"),"--output-dir",str(N/"clean_archive_run")],extract,[F/"pr95_support.zip",extract/"PAYLOAD_MANIFEST.json",extract/"verification/run_all.py"])
print(json.dumps({"archive_members":len(members),"zip_sha256":sha(F/"pr95_support.zip"),"clean_exit":r["exit_code"]}))
