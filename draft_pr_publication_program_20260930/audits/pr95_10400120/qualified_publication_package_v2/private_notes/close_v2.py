from pathlib import Path
import datetime,difflib,hashlib,json,os
from capture_v2 import sha,dump
P=Path(__file__).resolve().parent.parent;N=P/"private_notes";F=P/"publicfiles";V1=P.parent/"qualified_publication_package_v1"
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
for label in ("assembled_run","clean_archive_run"):
 d=json.loads((N/label/"results.json").read_text())
 if d["status"]!="PASS_EXACT_SPECIALIZATION" or d["note_sha256"]!=sha(F/"pr95_note.tex"):raise RuntimeError("run binding")
 if len([r for r in d["runs"] if not r["negative"] and r["exit_code"]==0])!=6:raise RuntimeError("positive count")
 if len([r for r in d["runs"] if r["negative"] and r["exit_code"]==1])!=6:raise RuntimeError("negative count")
controls=json.loads((N/"PAYLOAD_GUARD_CONTROLS.json").read_text())
if controls["hostile_cases"]!=14 or controls["positive_guard_cases"]!=2:raise RuntimeError("guard closure")
for e in json.loads((F/"PAYLOAD_MANIFEST.json").read_text())["files"]:
 if sha(F/e["file"])!=e["sha256"]:raise RuntimeError("public byte change")
diff="\n".join(difflib.unified_diff((V1/"publicfiles/verification/run_all.py").read_text().splitlines(),(F/"verification/run_all.py").read_text().splitlines(),fromfile="v1/verification/run_all.py",tofile="v2/verification/run_all.py",lineterm=""))+"\n"
(N/"RUNNER_R1.patch").write_text(diff)
dump(N/"REPAIR_SCOPE.json",{"UTC":utc,"required_item":"R1","mechanism":"Check every lexical relative component beneath ROOT with is_symlink before reading final file. Reject both final-file and ancestor-directory links through RuntimeError.",
 "v1_runner_sha256":sha(V1/"publicfiles/verification/run_all.py"),"v2_runner_sha256":sha(F/"verification/run_all.py"),"patch_sha256":sha(N/"RUNNER_R1.patch"),
 "unchanged_bytes":{"manuscript":sha(F/"pr95_note.tex"),"PDF":sha(F/"pr95_note.pdf"),"deposit_metadata":sha(P/"zenodo-deposit.json")},
 "mathematical_checkers_unchanged":all(sha(F/"verification"/s)==sha(V1/"publicfiles/verification"/s) for s in ("verify.py","independent_checks.py","root_lattice_check.py")),
 "guards_tested_both_modes":["missing","changed","leaf_symlink","ancestor_symlink","unsafe","duplicate","ast_assertion"],
 "v1_receipts":"Frozen historical records preserved in V1; not relabeled as V2.","publication_clearance":False})
processes=[]
for q in sorted(P.rglob("process.json")):
 d=json.loads(q.read_text())
 if "exit_code" not in d or "pid" not in d:raise RuntimeError("unfinished recorded child "+str(q))
 processes.append({"file":q.relative_to(P).as_posix(),"pid":d["pid"],"exit_code":d["exit_code"],"sha256":sha(q)})
unique=sorted({e["pid"] for e in processes});alive=[]
for pid in unique:
 try:os.kill(pid,0);alive.append(pid)
 except ProcessLookupError:pass
 except PermissionError:alive.append(pid)
if alive:raise RuntimeError("recorded PIDs still alive "+str(alive))
dump(N/"PROCESS_CLOSURE.json",{"UTC":utc,"recorder_pid":os.getpid(),"completed_receipts":len(processes),"unique_child_pids":len(unique),"all_recorded_child_pids_terminated":True,"checked_pids":unique,"processes":processes})
dump(N/"PDF_PRESERVATION_QA.json",{"UTC":utc,"pages":5,"PDF_sha256":sha(F/"pr95_note.pdf"),"manuscript_sha256":sha(F/"pr95_note.tex"),"identical_to_visually_verified_V1":True,"new_PDF_authoring_or_rendering_performed":False,"basis":"V1 visual QA and sealed round1 independently read every page; exact byte identity retained. No editor tab/PDF modification."})
public=[{"file":q.relative_to(P).as_posix(),"bytes":q.stat().st_size,"sha256":sha(q)} for q in sorted(F.rglob("*")) if q.is_file()]
dump(N/"FROZEN_CANDIDATE_MANIFEST.json",{"schema":"pr95-frozen-qualified-candidate/v2","UTC":utc,"package_revision":"V2","deposit_version":"1.0","frozen_public_candidate":True,"public_files":public,"deposit_manifest":{"file":"zenodo-deposit.json","sha256":sha(P/"zenodo-deposit.json"),"bytes":(P/"zenodo-deposit.json").stat().st_size},
 "source_head":"6534ad01e519c719628a18984b108e73cf2e8ead","problem":"10400120 / AMR-103-0120","original_author_effort":"2/5","new_central_proof_search_turns":0,
 "repair_scope_sha256":sha(N/"REPAIR_SCOPE.json"),"clean_archive_results_sha256":sha(N/"clean_archive_run/results.json"),"payload_guard_controls_sha256":sha(N/"PAYLOAD_GUARD_CONTROLS.json"),
 "role":"Prepared corrected candidate for new round2 adversarial review; not an adversarial review or publication clearance.",
 "priority_clearance":False,"worldwide_novelty_established":False,"human_peer_review":False,"publication_clearance":False})
with (N/"RESEARCH_LOG.md").open("a") as f:
 f.write("\n"+utc+" - V2 frozen after final-source/full clean ZIP suites,14 hostile guard rejects+2 clean guards, exact110-member safe ZIP/member/digest verification, actual top-level Zenodo LOCAL check exit0 and693 unchanged V1 manifest entries. Source/docs/provenance repair only; note/PDF/math/metadata unchanged. All recorded child PIDs terminated. Preparation estimate100%, math100% under accepted imported foundations; priorityunresolved; publicationclearancefalse. Initial setup mkdir failed because helper authoring already created its folder; source version preserved, no public payload copied before failure. Initial unsafe fixture replaced a required member and thus rejected at coverage rather than path-safety check; expected-reason harness failed and all partial records/source/fixtures preserved. Final fixture appends unsafe path, exercising intended guard in both modes. Neither failure was relabeled as a successful intended test.\n")
report=f"""# PR95 V2 qualified package preparation

Preparation completed and corrected candidate frozen {utc}. Preparation100% only; no adversarial-review or publication clearance.

## R1 repair and scope

The only substantive repair is in verification/run_all.py: each lexical component of every declared relative payload path beneath ROOT is checked for symlink status before reading contents. A linked final file or ancestor directory raises RuntimeError. The source diff is private_notes/RUNNER_R1.patch; exact source scope/hashes in REPAIR_SCOPE.json. README and verification instructions specify this behavior; source provenance identifies the runner change.

V1 and sealed round1 remain unchanged. All693 V1 preparation-manifest entries, the pinned review reportSHA256be4f8abab1cda0ea36fd60b0174bb409570942fe62ee780e9624f8187ac139e2 and closed-manifestSHA25630b71243599df77235d73d7c8b118c342f31bb94654ee6648f1e8bf39e98a4c0 rechecked. Only active public authored inputs/PDF were copied, not693 V1 private files or primary sources. V1 receipts stay historical in the frozen sibling.

The mathematical programs, manuscript and five-pagePDF retain exact V1 bytes. Canonical Zenodo deposit metadata is byte-identical, including version1.0; no release exists. No PDF authoring/rendering/compiler/UI step was repeated. V1 and round1 page-by-page QA remains applicable by byte identity.

## Actual validation

Final V2 assembly and fresh clean extraction each pass all6positive children and reject6actual false arithmetic coefficients with exit1. Positive ordinary/-O streams are byte-identical for each route. Every run is fresh, with actual argv/PIDs/UTC/environment/version/input snapshots/hashes/exits/full streams. Current recorded public results are V2 assembly receipts; final expanded archive carries109 guarded members plus manifest,110 members total.

Missing, changed, leaf-symlink, ancestor-symlink, unsafe path, duplicate entry and removable-AST-assertion cases reject explicitly in both ordinary and optimized modes:14 hostile processes. Each uses the actual full runner CLI and rejects before output directory creation with no success stdout. Both clean guard probes pass. The ancestor symlink points to identical recorded-process contents; normal and -O both raise the specific 'symlinked payload path component: verification/recorded_processes/...' error, not an unrelated import failure.

The trustedZIP digest, exact safe memberlist, no duplicates/no symlink ZIP entries, every archived/public byte and every extracted/public digest were checked. Actual repository top-level Zenodo LOCAL check exits0 and matches exact7-upload file identity/metadata; no service action was performed. Process closure records{len(unique)} unique completed child PIDs, all checked terminated.

Two harness/setup failures are retained: initial setup mkdir FileExistsError before public copies, and an initial unsafe fixture that replaced a required name, triggering earlier coverage rejection and thus failing the expected-reason harness. Initial source/partial actual guard receipts/fixtures remain preserved. The final unsafe fixture appends an unsafe entry and exercises the intended path check. No failed intended test is relabeled PASS; no failed scientific result is hidden.

## Frozen paths and hashes

- publicfiles/pr95_note.pdf: {sha(F/'pr95_note.pdf')} (unchanged5pages).
- publicfiles/pr95_note.tex: {sha(F/'pr95_note.tex')} (unchanged).
- publicfiles/verification/run_all.py: {sha(F/'verification/run_all.py')}.
- publicfiles/pr95_support.zip: {sha(F/'pr95_support.zip')}.
- zenodo-deposit.json: {sha(P/'zenodo-deposit.json')} (unchanged).
- private_notes/FROZEN_CANDIDATE_MANIFEST.json binds all public bytes and exact metadata.
- private_notes/INPUTS.json, REPAIR_SCOPE.json, RUNNER_R1.patch, PRESERVATION_CHECK.json and ARCHIVE_INTEGRITY.json bind read/repair/preservation/archive scope.
- private_notes/assembled_run/, clean_archive_run/ and processes/ retain fresh completed process evidence.
- private_notes/PAYLOAD_GUARD_CONTROLS.json indexes all final boundary controls.

## Qualifications and remaining work

Verified claim remains ordinary full SU(5), WZWk5/shiftedr10,126 full labels; L(5,1),L(5,2),pi1Z5; positive unequal S3-normalized squares3475+1550sqrt5 and4025+1800sqrt5, under established imported RT/modular-category/HT foundations. Manuscript/README/priority supplement/metadata retain directly relevant Kuriya full-text gap, unresolved historical priority, no firstness/exhaustive novelty/currentglobalopen/new historical-resolution claims, extensive AI/unrefereed/no conventional human peer review. Originaleffort2/5;zero new central proof-search turns.

Exact remaining package work is a NEW round2 whole-package adversarial review and ROOT adjudication. Historical priority remains unresolved. Publication/Zenodo services/Git integration/PR/tracker are ROOT responsibilities and remain undone here. No outside individual communication, Git/index/branch/PR/UI/editor/credentials/cache/service/tracker mutation or write outside this V2 folder occurred.
"""
(N/"REPORT.md").write_text(report,encoding="utf-8")
files=[];links=[]
for q in sorted(P.rglob("*")):
 if q.is_symlink():
  links.append({"file":q.relative_to(P).as_posix(),"target":str(q.readlink()),"intentional_negative_control":True})
 elif q.is_file() and q.name not in ("PREPARATION_MANIFEST.json","CLOSURE.json"):
  files.append({"file":q.relative_to(P).as_posix(),"bytes":q.stat().st_size,"sha256":sha(q)})
dump(P/"PREPARATION_MANIFEST.json",{"schema":"pr95-v2-preparation-packet/v1","UTC":utc,"operator_pid":os.getpid(),"files":files,"intentional_control_symlinks":links,"frozen_candidate_manifest_sha256":sha(N/"FROZEN_CANDIDATE_MANIFEST.json")})
dump(P/"CLOSURE.json",{"UTC":utc,"preparation_manifest_sha256":sha(P/"PREPARATION_MANIFEST.json"),"frozen_candidate_manifest_sha256":sha(N/"FROZEN_CANDIDATE_MANIFEST.json"),"report_sha256":sha(N/"REPORT.md"),"public_candidate_frozen":True,"publication_clearance":False,"preparation_estimate_percent":100})
print(json.dumps({"preparation_manifest_sha256":sha(P/"PREPARATION_MANIFEST.json"),"frozen_manifest_sha256":sha(N/"FROZEN_CANDIDATE_MANIFEST.json"),"report_sha256":sha(N/"REPORT.md"),"files":len(files),"symlinks":len(links),"zip_sha256":sha(F/"pr95_support.zip")},indent=2))
