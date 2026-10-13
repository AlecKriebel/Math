from pathlib import Path
import datetime,hashlib,json,os,signal
P=Path(__file__).resolve().parent.parent;N=P/"private_notes";F=P/"publicfiles"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
clean=json.loads((N/"clean_archive_run/results.json").read_text())
if clean["status"]!="PASS_EXACT_SPECIALIZATION":raise RuntimeError("clean archive did not pass")
if clean["note_sha256"]!=sha(F/"pr95_note.tex"):raise RuntimeError("clean archive note mismatch")
zip_payload=json.loads((F/"PAYLOAD_MANIFEST.json").read_text())
for e in zip_payload["files"]:
 q=F/e["file"]
 if sha(q)!=e["sha256"] or q.stat().st_size!=e["bytes"]:raise RuntimeError("payload change")
processes=[]
for q in sorted(P.rglob("process.json")):
 d=json.loads(q.read_text())
 if "pid" not in d or "exit_code" not in d:raise RuntimeError("unfinished process receipt "+str(q))
 # Recorded copied receipts may repeat the same PID; each has explicit completion.
 processes.append({"file":q.relative_to(P).as_posix(),"pid":d["pid"],"exit_code":d["exit_code"],"sha256":sha(q)})
unique={d["pid"] for d in processes}
alive=[]
for pid in sorted(unique):
 try:os.kill(pid,0);alive.append(pid)
 except ProcessLookupError:pass
 except PermissionError:alive.append(pid)
if alive:raise RuntimeError("recorded process PID still alive: "+str(alive))
dump(N/"PROCESS_CLOSURE.json",{"UTC":utc,"completed_receipts":len(processes),"unique_child_pids":len(unique),"checked_pids_no_longer_alive":sorted(unique),"processes":processes})
dump(N/"BUILTIN_COMPILATION.json",{"source":str(F/"pr95_note.tex"),"final_note_sha256":sha(F/"pr95_note.tex"),
 "observed_final_response":{"path":str(F/"pr95_note.tex"),"kind":"success","message":"The current source compiled successfully with the desktop editor's compiler."},
 "provenance":"Actual built-in compile tool response after the line-length repair, retained from tool transcript; this is not a subprocess receipt.","editor_tab_opened":False,
 "export":{"tool":"tectonic","exit_code":0,"final_export_warnings":False},"marker":{"operation_kind":"create","expected_output_count":1,"output_format":"pdf","successful_calls":1}})
public=[{"file":q.relative_to(P).as_posix(),"bytes":q.stat().st_size,"sha256":sha(q)} for q in sorted(F.rglob("*")) if q.is_file()]
metadata=P/"zenodo-deposit.json"
dump(N/"FROZEN_CANDIDATE_MANIFEST.json",{"schema":"pr95-frozen-qualified-candidate/v1","UTC":utc,"frozen_public_candidate":True,
 "note_pages":5,"public_files":public,"deposit_manifest":{"file":"zenodo-deposit.json","bytes":metadata.stat().st_size,"sha256":sha(metadata)},
 "final_clean_archive_results":{"file":"private_notes/clean_archive_run/results.json","sha256":sha(N/"clean_archive_run/results.json")},
 "packet_role":"Reviewable prepared candidate for fresh ROOT whole-package adversarial rounds; no publication clearance.",
 "source_head":"6534ad01e519c719628a18984b108e73cf2e8ead","source_problem":"10400120 / AMR-103-0120",
 "original_author_effort":"2/5","new_central_proof_search_turns":0,"priority_clearance":False,"worldwide_novelty_established":False,"human_peer_review":False,"publication_clearance":False})
with (N/"RESEARCH_LOG.md").open("a") as f:
 f.write("\n"+utc+" - Clean ZIP extraction: full 109-member payload guard passed; 6 positive exits0/6 arithmetic false exits1. Optimized hostile payload mutation rejected before output creation (exit1, exact hash-mismatch message). Actual top-level Zenodo kit local check exit0 with exact seven-file metadata/file digest output. All recorded child PIDs checked terminated. Candidate public bytes frozen for ROOT review. Preparation completion estimate100%; narrow mathematics100% under cited foundations; priority unresolved; no publication clearance or worldwide firstness. One initial JS author-script construction error occurred before file/script execution; a later store(undefined) tool error occurred after successful capture launch, whose eventual exit0 is recorded. No failed scientific run relabeled success.\n")
report=f"""# PR95 qualified research-note package preparation

Prepared candidate frozen {utc}. Preparation estimate100% for this assigned package; this is not a publication clearance or a worldwide novelty claim.

## Result and exact qualifications

Full ordinary SU(5), WZW k=5, shifted r=10, all126 integrable labels; L(5,1) and L(5,2) have pi1=Z/5 and positive unequal S3-normalized squares3475+1550sqrt5 and4025+1800sqrt5. The note contains the analytic five-survivor A4 lattice proof, exact table, positive embedding, S00 normalization, orientation/inverse conventions and elementary topology. It imports established RT/modular-category and Hansen-Takata formula inputs. The preprint math/0209403v2 is the actual formula source; final journal text has not been compared.

The target is Conjecture7.5 printed p474 in Ohtsuki's volume4 (nominal2002, actually published1June2004), attributed to Guadagnini-Pilo CMP192(1998)47-65. Kuriya's exact-title 2003 preprint is expressly credited; its complete text is unavailable and we cannot establish that it does not already contain or circumscribe this result. Priority remains unresolved, with no firstness, exhaustive novelty clearance, global-open-status or novel historical-resolution assertion. The later SU(N) WZNW spin-independence/background-phase qualification is preserved; no blanket spin dismissal. AI use is extensive; note unrefereed, no conventional human peer review.

## Candidate paths and freeze

- publicfiles/pr95_note.pdf: five pages, sha256 {sha(F/'pr95_note.pdf')}.
- publicfiles/pr95_note.tex: sha256 {sha(F/'pr95_note.tex')}.
- publicfiles/pr95_support.zip: 110 clean members, sha256 {sha(F/'pr95_support.zip')}.
- zenodo-deposit.json: actual top-level kit shape, seven upload files, sha256 {sha(metadata)}.
- private_notes/FROZEN_CANDIDATE_MANIFEST.json: full public-member and deposit metadata inventory.
- private_notes/INPUTS.json and publicfiles/verification/SOURCE_PROVENANCE.json: read inputs and exact source adaptations.
- private_notes/assembled_final_run and private_notes/clean_archive_run: actual full child execution evidence.
- private_notes/outer_processes: actual clean-extraction/tamper/local-Zenodo-check parent processes.
- private_notes/PDF_VISUAL_QA.json and render_final/: actual final page images and review record.

The author certificate now binds the current qualified note bytes via a script-relative path. Historical COUNTEREXAMPLE.md is not redistributed. Repaired author and historical checker retain exact mathematics; explicit validation survives -O. The fresh stdlib root-lattice source changes only its explanatory derivation filename. Original/source audit files remain immutable and unmodified.

## Actual execution and QA

Both final-source assembly and clean ZIP extraction ran three routes ordinarily and with -O: six positive exits0, six actual false arithmetic coefficient targets rejected with exit1 and no success stdout/author JSON. Positive ordinary/-O stdout is byte-identical in each route. Fresh process receipts include actual argv, child PIDs, UTC start/end, sanitized Python environment/version, input snapshots/hashes, full stdout/stderr and exits. Tested CPython3.12.14, NumPy2.3.5; lattice code stdlib only. The retained exact_assertions=2005 schema is explained as a count of finite explicit checks, not quality or independent theorem count.

Optimized payload mutation test exited1 on the declared verify.py hash mismatch before creating output. Top-level /Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py check exited0 and confirmed exact metadata plus seven upload file sizes/SHA256s. No stage/upload/publish was performed.

The PDF skill marker ran successfully exactly once, immediately before initial TeX authoring. Built-in compiler succeeded initially and after one wording/layout repair. Tectonic exported the final five-page PDF without warnings. All final pages were rendered at85dpi and visually read; zero remaining visual defects. No UI tab was opened. Initial overlong preprint token was fixed by shortening wording; first-source run evidence remains preserved.

All controlled processes terminated; process-closure record has {len(unique)} unique child PIDs. A construction-time JS syntax error preceded any draft-script execution; another helper store(undefined) error occurred after a completed tool-launch step. Both were process bookkeeping errors, not scientific executions. No failed scientific result is hidden or relabeled.

## Remaining work and constraints

No unresolved mathematical gap was found in the already accepted narrow gate under its imported foundations. Direct historical priority gap remains the unavailable Kuriya full text; other bounded read/version gaps are disclosed. Fresh whole-package adversarial review, ROOT adjudication, external services/Zenodo publication, tracker update, PR/Git integration and any later disposition are ROOT responsibilities and remain undone here. This preparation grants none of those clearances.

No external individual contact, central proof search, Git/index/branch/PR/service/tracker/editor state change, or edit outside qualified_publication_package_v1 was made. Original effort2/5; zero new central proof-search turns. No copyrighted third-party source PDFs/extracted text/rendered source pages, source-retrieval headers, private historical audit receipts or credentials enter the public package.
"""
(N/"REPORT.md").write_text(report,encoding="utf-8")
manifest={"schema":"pr95-preparation-packet/v1","UTC":utc,"operator_pid":os.getpid(),"frozen_candidate_manifest_sha256":sha(N/"FROZEN_CANDIDATE_MANIFEST.json"),"files":[{"file":q.relative_to(P).as_posix(),"bytes":q.stat().st_size,"sha256":sha(q)} for q in sorted(P.rglob("*")) if q.is_file() and q.name not in ("PREPARATION_MANIFEST.json","CLOSURE.json")]}
dump(P/"PREPARATION_MANIFEST.json",manifest)
dump(P/"CLOSURE.json",{"UTC":utc,"preparation_manifest_sha256":sha(P/"PREPARATION_MANIFEST.json"),"frozen_candidate_manifest_sha256":sha(N/"FROZEN_CANDIDATE_MANIFEST.json"),"report_sha256":sha(N/"REPORT.md"),"public_candidate_frozen":True,"publication_clearance":False,"preparation_estimate_percent":100})
print(json.dumps({"closure":str(P/"CLOSURE.json"),"preparation_manifest_sha256":sha(P/"PREPARATION_MANIFEST.json"),"frozen_manifest_sha256":sha(N/"FROZEN_CANDIDATE_MANIFEST.json"),"report_sha256":sha(N/"REPORT.md")},indent=2))
