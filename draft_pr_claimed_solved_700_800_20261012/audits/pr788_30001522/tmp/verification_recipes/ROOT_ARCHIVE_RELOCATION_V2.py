from pathlib import Path
import datetime,hashlib,json,os,stat,subprocess,sys,tempfile,zipfile
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp");P=T/"preprint";W=T/"root_archive_relocation_v2";W.mkdir(exist_ok=True)
inv=json.loads((P/"PACKAGE_INVENTORY.json").read_text());pin=inv["source_manifest_sha256"]
with tempfile.TemporaryDirectory(dir=W,prefix="owned-relocation-")as td:
 d=Path(td);s=d/"source with spaces";s.mkdir()
 with zipfile.ZipFile(P/"source-and-verification.zip")as z:
  names=z.namelist();assert len(names)==len(set(names))==inv["source_files_including_manifest"]
  for x in z.infolist():
   path=Path(x.filename);assert not path.is_absolute()and".."not in path.parts and stat.S_ISREG(x.external_attr>>16)
  z.extractall(s)
 r=subprocess.run(["/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3","-I","-B","-O",str(s/"verify_source.py"),"--expected-manifest-sha256",pin,"--pdf",str(P/"output/pdf/paper.pdf"),"--replay"],cwd="/",env=dict(os.environ,TMPDIR=str(d)),capture_output=True,text=True,timeout=300)
 if r.returncode or r.stderr:raise RuntimeError(r.stdout+r.stderr)
 got=json.loads(r.stdout);assert got["result"]=="PASS"and got["external_evidence_files_rehashed"]==0 and len(got["finite_replay_processes"])==10
 with zipfile.ZipFile(P/"zenodo-upload-kit.zip")as z:
  assert len(z.namelist())==len(set(z.namelist()))==5
  assert z.read("paper.pdf")==(P/"output/pdf/paper.pdf").read_bytes()
  assert z.read("source-and-verification.zip")==(P/"source-and-verification.zip").read_bytes()
  assert z.read("zenodo-metadata.json")==(P/"zenodo-metadata.json").read_bytes()
  flat=json.loads(z.read("zenodo-deposit.json"));assert flat["metadata"]==json.loads((P/"zenodo-metadata.json").read_text())["metadata"]
  assert flat["files"]==[{"path":"paper.pdf"},{"path":"source-and-verification.zip"}]
receipt={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","source_manifest_sha256":pin,"source_archive_files":len(names),"relocated_with_spaces":True,"optimized_bundled_Python_replay":got,"outer_convenience_kit_files":5,"exact_inner_PDF_sourceZIP_metadata":True,"historical_76_body_custody_replayed":False}
(T/"root-receipts/ROOT_ARCHIVE_RELOCATION_V2.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"result":"PASS","source_files":len(names),"relocated_finite_replays":10,"outer_kit_exact":True}))
