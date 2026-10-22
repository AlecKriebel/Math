from pathlib import Path
import datetime,hashlib,json,subprocess
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");P=T/"preprint";S=P/"source";M=T/"root-receipts";B=T/"repair_typeset_v3";V=T/"package_versions/v2_review02"
assert not(M/"ROUND02_REPAIRS_V3_COMPILATION.json").exists()and not B.exists()
peer=json.loads((M/"WHOLE02_ROOT_REPLAY.json").read_text());assert peer["result"]=="PASS"and peer["review_actionable_issues"]==2
assert(S/"MANIFEST.json").read_bytes()==(V/"source/MANIFEST.json").read_bytes()
tex=(S/"main.tex").read_text();assert tex.count("pp.~1360--1362.")==1;newtex=tex.replace("pp.~1360--1362.","pp.~1360--1363.");assert newtex.count(r"\cite[pp.~1361--1362]{OWR}")==1;(S/"main.tex").write_text(newtex)
p=S/"README.md";text=p.read_text();needle="## Contents and review provenance";assert text.count(needle)==1
section="""## Explicit optional algebra-packet control command

The sealed algebra packet README's "same arguments" shorthand is superseded here for test_packet.py: omit --replay, which is accepted only by its verify_packet.py. Before running the optional control harness, copy the entire sealed audit/math_quotient_algebra directory (all 15 files) to a new owned ordinary directory outside the closed source. The harness makes temporary directories under packet.parent and temporarily hardlinks its copied REPORT; do not pass the frozen source directory as its test root.

Point --intake-root to the absolute extracted source's audit/intake directory and --primary-root to the absolute directory containing the four external files recorded in the copied PRIMARY_SOURCES.json. Those third-party bodies are not redistributed in this archive. For example, with a complete owned copy and a matching retrieved primary bank:

FENCEsh
python3 -I -B /absolute/owned/algebra-packet-copy/test_packet.py \\
  --packet /absolute/owned/algebra-packet-copy \\
  --intake-root /absolute/extracted-source/audit/intake \\
  --primary-root /absolute/retrieved-primary-bank \\
  --expected-manifest-sha256 7cd556c6a87d2117f803112268e4b8eb86316c76dac40c9fee82ffe0ccf6eea0 \\
  --expected-checker-sha256 31246b25e6040d2d676f0fd5d1b6c4c65cedc0a67440da313a3ff0a584689333
FENCE

The unchanged corrected invocation passes 2 positive and 16 negative controls. This is an optional custody-control suite, separate from the advertised read-only core --replay. Preserve all sealed family/original files and their external pins; this clarification does not alter them.

"""
section=section.replace("FENCE",chr(96)*3);p.write_text(text.replace(needle,section+needle))
B.mkdir();cmd=["/opt/homebrew/bin/tectonic","-X","compile","--keep-logs","--outdir",str(B),str(S/"main.tex")]
r=subprocess.run(cmd,cwd="/",capture_output=True,text=True,timeout=300)
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"REPAIRS_COMPILED_PENDING_VISUAL_AND_REBIND"if r.returncode==0 else"COMPILE_FAILED","command":cmd,"exit_code":r.returncode,"stdout":r.stdout,"stderr":r.stderr,"source_edits":["main.tex bibliography1360–1363 only","README explicit superseding owned-copy algebra control command without --replay"],"mathematical_claim_changes":False,"all_original_58_and_all4_math_priority_packets_preserved":True,"exact_old_v2_preserved":str(V),"PDF_authoring_marker_repeated":False,"publication_version_still":"1.0 first unpublished release"}
(M/"ROUND02_REPAIRS_V3_COMPILATION.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n");assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr)
info=subprocess.run(["pdfinfo",str(B/"main.pdf")],capture_output=True,text=True,check=True).stdout;pages=int(next(l.split(":",1)[1]for l in info.splitlines()if l.startswith("Pages:")));assert pages==4
(P/"output/pdf/paper.pdf").write_bytes((B/"main.pdf").read_bytes());render=P/"render_v3";render.mkdir()
r=subprocess.run(["pdftoppm","-scale-to","1500","-png",str(P/"output/pdf/paper.pdf"),str(render/"page")],capture_output=True,text=True,timeout=120);assert r.returncode==0 and not r.stderr,r.stderr
out.update(PDF_pages=4,PDF_sha256=hashlib.sha256((P/"output/pdf/paper.pdf").read_bytes()).hexdigest(),paper_tex_sha256=hashlib.sha256((S/"main.tex").read_bytes()).hexdigest(),root_all4visual_pending=True)
(M/"ROUND02_REPAIRS_V3_COMPILATION.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"result":out["result"],"pages":4,"PDF_sha256":out["PDF_sha256"],"visual_and_binding_pending":True}))
