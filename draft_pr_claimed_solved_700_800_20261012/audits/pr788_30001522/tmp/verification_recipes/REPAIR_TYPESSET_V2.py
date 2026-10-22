from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp");P=T/"preprint";S=P/"source";M=T/"root-receipts";B=T/"repair_typeset_v2"
if not(M/"ROOT_CIRCLE_ACTION_PRECISION_REPAIR.json").exists():raise RuntimeError("Editorial repair must be applied first")
if B.exists():raise RuntimeError("Typeset workspace exists; inspect existing result before re-execution")
B.mkdir()
command=["/opt/homebrew/bin/tectonic","--keep-logs","--outdir",str(B),str(S/"paper.tex")]
r=subprocess.run(command,cwd="/",capture_output=True,text=True,timeout=300)
receipt={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"command":command,"exit_code":r.returncode,"stdout":r.stdout,"stderr":r.stderr,"reason":"Prepublication precision/date clarification following first completed fresh review; no new mathematical claim.","PDF_creation_marker_repeated":False}
(M/"REPAIR_DRAFT_COMPILATION.json").write_text(json.dumps(receipt,indent=2)+"\n")
if r.returncode or r.stderr:raise RuntimeError("Actual TeX compilation requires inspection")
pdf=(B/"paper.pdf").read_bytes();info=subprocess.run(["pdfinfo",str(B/"paper.pdf")],capture_output=True,text=True,check=True).stdout
pages=int(next(x.split(":",1)[1]for x in info.splitlines()if x.startswith("Pages:")))
if pages!=4:raise RuntimeError("Inspect changed pagination before adopting revised PDF")
(P/"output/pdf/paper.pdf").write_bytes(pdf)
render=subprocess.run(["pdftoppm","-scale-to","1250","-png",str(P/"output/pdf/paper.pdf"),str(P/"tmp/pdfs/page")],cwd="/",capture_output=True,text=True,timeout=120)
if render.returncode or render.stderr:raise RuntimeError(render.stderr)
receipt.update(PDF_pages=pages,paper_tex={"bytes":(S/"paper.tex").stat().st_size,"sha256":hashlib.sha256((S/"paper.tex").read_bytes()).hexdigest()},paper_pdf={"bytes":len(pdf),"sha256":hashlib.sha256(pdf).hexdigest()},root_visual_inspection_pending=True)
(M/"REPAIR_DRAFT_COMPILATION.json").write_text(json.dumps(receipt,indent=2)+"\n")
(S/"audit/root-receipts/FINAL_DRAFT_COMPILATION.json").write_text(json.dumps(receipt,indent=2)+"\n")
(M/"REPAIR_PDF_INFO.txt").write_text(info)
print(json.dumps({"result":"COMPILED_AND_RENDERED","pages":pages,"stderr_empty":not r.stderr,"tex":receipt["paper_tex"],"pdf":receipt["paper_pdf"],"visual_review_pending":True}))
