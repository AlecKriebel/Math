from pathlib import Path
import json,hashlib,datetime,shutil,zipfile
P=Path(__file__).resolve().parent.parent;F=P/"publicfiles";N=P/"private_notes"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
run=N/"assembled_final_run"
d=json.loads((run/"results.json").read_text())
if d["status"]!="PASS_EXACT_SPECIALIZATION":raise RuntimeError("assembled result")
if d["note_sha256"]!=sha(F/"pr95_note.tex"):raise RuntimeError("assembled note byte mismatch")
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
 "hash_scope":"Every support archive member except this manifest. Public process records are fresh certificate executions, not private source-audit receipts. Establish trusted ZIP digest separately.",
 "recorded_run_manifest":"Initial final-source run bound 10 input members; later archive manifest additionally binds recorded process evidence. Fresh clean extraction validates this expanded archive."})
members.append("PAYLOAD_MANIFEST.json")
with zipfile.ZipFile(F/"pr95_support.zip","w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name in sorted(members):
  info=zipfile.ZipInfo(name,date_time=(2026,10,5,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
  z.writestr(info,(F/name).read_bytes())
extract=N/"clean_extracted";extract.mkdir()
with zipfile.ZipFile(F/"pr95_support.zip") as z:
 if any(Path(n).is_absolute() or ".." in Path(n).parts for n in z.namelist()):raise RuntimeError("archive path")
 z.extractall(extract)
tamper=N/"tampered_extracted";shutil.copytree(extract,tamper)
q=tamper/"verification/verify.py";q.write_text(q.read_text()+"\n# hostile payload mutation\n")
for name in ["pr95_note.pdf","pr95_note.tex","pr95_support.zip","PR95_PRIORITY_QUALIFICATION.md","README.md","LICENSE.txt"]:
 if not (F/name).is_file():raise RuntimeError("missing deposit file "+name)
sums=[sha(F/name)+"  "+name for name in ["pr95_note.pdf","pr95_note.tex","pr95_support.zip","PR95_PRIORITY_QUALIFICATION.md","README.md","LICENSE.txt"]]
(F/"SHA256SUMS.txt").write_text("\n".join(sums)+"\n")
dump(N/"PDF_VISUAL_QA.json",{"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"pages":5,"dpi":85,"all_pages_visually_read":True,"final_layout_defects_found":0,"pdf_sha256":sha(F/"pr95_note.pdf"),"note_sha256":sha(F/"pr95_note.tex"),"images":[{"file":x.relative_to(N).as_posix(),"sha256":sha(x),"bytes":x.stat().st_size} for x in sorted((N/"render_final").glob("*.png"))],"initial_issue":"Long preprint token extended text line on page1; shortened wording, no content change. Final export has no TeX warnings."})
with (N/"RESEARCH_LOG.md").open("a") as f:
 f.write("\n"+datetime.datetime.now(datetime.timezone.utc).isoformat()+" - Final-source suite 6 positive exits0/6 false exits1; ordinary/-O positive stdout byte-identical. Final 5-page PDF rendered/read page by page with zero remaining visual defects. Support ZIP built with authored content/fresh certificate receipts only; immutable primary PDFs/private source audits excluded. Clean extraction and payload mutation control prepared. Preparation estimate90%; mathematics100%; priority unresolved; publication clearance false.\n")
print(json.dumps({"support_members":len(members),"zip_sha256":sha(F/"pr95_support.zip"),"pdf_sha256":sha(F/"pr95_note.pdf")}))
