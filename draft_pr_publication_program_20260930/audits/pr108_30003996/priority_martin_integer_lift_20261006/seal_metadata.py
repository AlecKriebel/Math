"""Seal bounded audit metadata; no external mutation."""
import datetime, hashlib, json, pathlib, sys
D=pathlib.Path(__file__).resolve().parent
A=D.parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    p=pathlib.Path(p)
    b=p.read_bytes()
    return {"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"pdf_magic":b.startswith(b"%PDF-") if p.suffix in [".pdf",".bin"] else None}
records=[json.loads(s) for s in (D/"private/COMMANDS_RAW.jsonl").read_text().splitlines()]
downloads={}
for r in records:
    a=r.get("argv",[])
    if a and a[0]=="curl" and "-o" in a:
        name=pathlib.Path(a[a.index("-o")+1]).name
        downloads[name]={"retrieved_utc":r["utc"],"curl_pid":r["pid"],"curl_exit":r["exit"],"url":a[-1],"raw_argv_receipt":"private/COMMANDS_RAW.jsonl"}
sources=[
 ("owr",A/"primary_sources_20261006/owr.pdf","Kaibel, Combinatorial Optimization contribution in OWR2018, printed3014–3015","https://ems.press/content/serial-article-files/46772","Complete contribution PDF46–47 text before freeze; rendered pages inspected after freeze","source provided locally"),
 ("candidate",A/"repaired_diagnostics_v1/PROOF.md","Exact current repaired candidate; original head provided3526d46bf143b08e5055ffa7728c6278e9f958ea",None,"Complete proof before independent freeze","provided local candidate"),
 ("martin1991",D/"private/martin1991.pdf","ORL10(3),119–128, April1991; DOI10.1016/0167-6377(91)90028-N",None,"Publisher metadata and abstract; NO original full proof","HTML instead of PDF; pdftotext PID7199 exit1"),
 ("martin1991plain",D/"private/martin1991_pdf_plain.bin","Same original, ordinary publisher endpoint",None,"No full proof","HTTP403 HTML; ordinary endpoint attempt"),
 ("martin1991pdfft",D/"private/martin1991_pdfft.bin","Same original, ordinary publisher endpoint",None,"No full proof","HTTP403 HTML; ordinary endpoint attempt"),
 ("kaibel2017",D/"private/kaibel2017.pdf","Constructing Extended Formulations; Simons Berkeley2017 slides",None,"Relevant slide18–20 dualization/extension complexity and slide26 tree example plus targeted text searches; not entire deck proof review","primary institutional PDF"),
 ("goemans_myung1993",D/"private/goemans_myung1993.pdf","Networks23(1993),19–28; receivedJuly1991, acceptedJune1992",None,"Entire10printed pages19–28, including proofs/formulations and bibliography","primary author institutional PDF"),
 ("owa2017",D/"private/owa2017.pdf","Authors final draft9October2016; EJOR260(3),886–903,1August2017; DOI10.1016/j.ejor.2016.10.016",None,"Introduction/definition; complete complexity proofpp4–5; complete formulation section3.1pp6–9 including fixed-root subsection; not entire computational paper","primary UPC author final draft, CCBYNCND4.0 cover"),
 ("friesen2019",D/"private/friesen2019.pdf","Dissertation submitted17June2019, defended24September2019",None,"Title/intro; Proposition2 equationsp8 and forest variantp9; complete Proposition13 proofpp68–69 and contextpp68–72; targeted full text searches; rendered PDF18 printed8 inspected; not entire thesis","primary national-library dissertation PDF"),
 ("ccz2010",D/"private/ccz2010.pdf","November2009, revisedFebruary2010",None,"Complete §6.1pp25–26; §4.3pp14–15; targeted full text searches; not entire48-page survey","primary author institutional PDF"),
 ("neurips2022",D/"private/neurips2022.pdf","NeurIPS2022 official proceedings main paper",None,"Main§4.1–4.2pp6–7 and§5.1; targeted text searches; not all learning/experimental proofs","primary proceedings PDF"),
 ("neurips2022_supp",D/"private/neurips2022_supp.pdf","NeurIPS2022 official supplemental paper",None,"Complete Proposition4 proof printedp20; related model context searches; not all supplementary proofs","primary proceedings supplement"),
 ("cutbasis2007",D/"private/cutbasis2007.pdf","Report108 UniversityKaiserslautern, authorpreprint23March2007; date seen in indexed text",None,"PDF not retrieved; bibliographic version lead only. No assertion of full original preprint read","CiteSeer public attempt HTML; third-party discovery copy not relied on as proof"),
 ("cutbasis2010",D/"private/cutbasis2010.pdf","DAM158(4),277–290,28February2010; DOI10.1016/j.dam.2009.07.015",None,"Local PDF not retrieved; primary publisher indexed actual Theorem3.2 full proof,§4.1–4.2/§4.4 read via web16/18. Not entire paper","Publisher PDF attempt HTML; actual relevant proofs/models available via primary web results")
]
manifest=[]
scopes=[]
for ident,p,version,url,scope,status in sources:
    item={"id":ident,**pin(p),"version":version,"read_scope":scope,"access_status":status}
    if p.name in downloads:
        item.update(downloads[p.name])
    elif url:
        item["url"]=url
    manifest.append(item)
    scopes.append({"source":ident,"path":str(p),"scope":scope,"sha256":item["sha256"],"declaration_utc":now,"timing":"before freeze" if ident in ["owr","candidate"] else "after freeze"})
extra=[
 (pathlib.Path("/Users/alec/Documents/Math/AGENTS.md"),"Complete applicable instruction file before freeze"),
 (pathlib.Path("/Users/alec/Documents/Math/unsolved_math_prioritization/AGENTS.md"),"Complete applicable instruction file before freeze"),
 (pathlib.Path("/Users/alec/.codex/plugins/cache/openai-primary-runtime/pdf/26.904.11930/skills/pdf/SKILL.md"),"Complete PDF skill before source extraction"),
 (A/"original_source_authentication_20261006/original_attempt/RESEARCH_LOG.md","Complete old author log AFTER independent freeze; no concrete literal prior theorem"),
 (A/"original_source_authentication_20261006/original_attempt/README.md","Complete old author README AFTER independent freeze"),
 (A/"CURRENT_EFFECTIVE_ARTIFACTS.json","Artifact pins/metadata only, after freeze"),
 (A/"INTAKE_CHECKPOINT_SELECTION_20261006.json","Artifact path inventory/selection metadata only, after freeze"),
 (A/"ROOT_MATHEMATICAL_GATE_20261006.json","File pin only during sealing; root gate100 supplied by parent, not independently re-audited")
]
for p,scope in extra:
    scopes.append({**pin(p),"scope":scope,"declaration_utc":now})
raw=[]
for p in sorted((D/"private").rglob("*")):
    if p.is_file():
        raw.append({**pin(p),"path":str(p.relative_to(D)),"redistribution":"private ignored; do not publish raw third-party content"})
missing=[
 {"id":"martin1986","title":"A sharp polynomial size LP formulation of the minimum spanning tree problem","date":"1986 Chicago working paper, bibliography evidence in Goemans–Myung1993","scope":"original not retrieved; bibliographic lead only"},
 {"id":"martin1988","title":"Using separation algorithms to generate mixed integer model reformulations","date":"1988 Chicago working paper, bibliography evidence in Goemans–Myung1993","scope":"original not retrieved; do not assign1991 publication theorem content"},
 {"id":"maculan1986","title":"A new linear programming formulation for the shortest s-directed spanning tree problem","date":"1986 JCISS11,53–56; bibliographic lead","scope":"original not retrieved; no theorem-level use"},
 {"id":"wong1980","title":"Integer programming formulations of the traveling salesman problem","date":"1980; Kaibel adjacentProblem2 citation lineage","scope":"original not retrieved; no direct hardness transfer"}
]
(D/"SOURCE_MANIFEST.json").write_text(json.dumps({"sealed_utc":now,"sources":manifest,"unretrieved_originals":missing,"raw_material_manifest":raw,"disk_bytes":sum(q.stat().st_size for q in D.rglob("*") if q.is_file()),"limit_bytes":350*1024*1024},indent=2)+"\n")
(D/"READ_SCOPE.json").write_text(json.dumps({"sealed_utc":now,"scope_type":"Specific complete sections versus full documents explicitly distinguished","independence":"Other family reports not consulted; author logs only after independent freeze","items":scopes},indent=2)+"\n")
diagnostics={
 "sealed_utc":now,"normal_and_optimized_python":"actual PIDs12107/12109 exit0 at2026-10-06T05:07:32; full exact rational witness saved",
 "validation":json.loads((D/"LIFT_VALIDATION.json").read_text()),
 "extraction_failure":{"pid":7199,"utc":"2026-10-06T05:01:17.325590+00:00","argv":["pdftotext","-layout",str(D/"private/martin1991.pdf"),"output text path; see exact receipt"],"exit":1,"diagnosis":"downloaded publisher response was HTML, not PDF"},
 "failed_downloads":[{"file":p.name,"bytes":p.stat().st_size,"pdf_magic":p.read_bytes().startswith(b"%PDF-")} for p in (D/"private").iterdir() if p.suffix in [".pdf",".bin"] and not p.read_bytes().startswith(b"%PDF-")],
 "no_fresh_hardness_route":True,"added_proof_turns":0
}
(D/"DIAGNOSTICS.json").write_text(json.dumps(diagnostics,indent=2)+"\n")
tool_receipts={
 "sealed_utc":now,"API_PID":"OS process IDs are not exposed for web/view_image/apply_patch APIs; do not fabricate them",
 "web":"18 calls: exact saved result bytes/SHAs in source manifest and private/webN.json; per-call queries/UTC semantics in SEARCH_RECEIPTS.json",
 "view_images":["private/owr-46.png","private/owr-47.png","private/friesen-018.png"],
 "authoring":"Filesystem writes through recorded Python subprocesses; any apply_patch API authoring itself has no exposed OS PID",
 "failed_apply_patch":{"utc_interval":["2026-10-06T05:12:00Z","2026-10-06T05:14:05Z"],"result":"verification failed, expected line not found","file":"LIFT_MODEL.md","changes":0},
 "provenance_limit":"Bootstrap2 read-only inventory calls have no exposed PID; disclosed in BOOTSTRAP_SCOPE.json. Exact original queries for web1–3 not retained."
}
(D/"TOOL_RECEIPTS.json").write_text(json.dumps(tool_receipts,indent=2)+"\n")
log=(D/"RESEARCH_LOG.md").read_text()
log += "\nThe following event times come from CLI/API receipts; checkpoint estimates were consolidated at seal time, not falsely presented as contemporaneous file writes. They measure bounded family audit work, not mathematical discovery or exhaustive history.\n\n"
for utc,pct,event in [
 ("2026-10-06T05:01:17.325590+00:00",25,"Original Martin PDF extraction failed on HTML; block reported promptly. Primary DOI/date authenticated; no unread-proof inference."),
 ("2026-10-06T05:02:55.528539+00:00",45,"Primary CCZ, Friesen, OWA and Goemans texts obtained; exact shared-tree versus projected/fixed-root distinctions investigated."),
 ("2026-10-06T05:06:18.555897+00:00",65,"Official supplemental actual Proposition4 proof retrieved; single-root projection checked. Source contribution and outward equations rendered and inspected."),
 ("2026-10-06T05:07:32+00:00",80,"Existing candidate finite rational lift diagnostic passed in normal and optimized Python; B2 same-proof restriction and shift verified. No central proof route added."),
 ("2026-10-06T05:10:45.148Z",90,"Actual primary cut-basis theorem proof and ILPs read; adjacent prior hardness preserved with unresolved linear-objective transfer gap."),
 (now,100,"Bounded family sealed: GO for attributed2018 resolution from this family, conditional on root; NO-GO absolute-first/history-checked claims. No concrete covering antecedent authenticated. Original2/5 retained; added proof turns0.")
]:
    log += f"- {utc}: {pct}% bounded audit complete. {event}\n"
log += "\nNo external contacts or outreach preparation. No Git/index/remote/editor/service/publication actions. All audit writes remain in this dedicated folder.\n"
(D/"RESEARCH_LOG.md").write_text(log)
v=json.loads((D/"VERDICT.json").read_text()); v["sealed_utc"]=now; (D/"VERDICT.json").write_text(json.dumps(v,indent=2)+"\n")
print(json.dumps({"sealed_utc":now,"source_count":len(manifest),"raw_count":len(raw),"scope_count":len(scopes),"disk_bytes":sum(q.stat().st_size for q in D.rglob("*") if q.is_file())}))

