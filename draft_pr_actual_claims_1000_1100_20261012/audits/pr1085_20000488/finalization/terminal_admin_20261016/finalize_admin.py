"""Bounded terminal accounting only; no service or mathematical mutation."""
from pathlib import Path
import datetime, difflib, hashlib, io, json, shutil, subprocess, sys, zipfile

F = Path(__file__).resolve().parent
A = F.parents[1]
K = A / 'preprint_v1_0'
STAMP = datetime.datetime.now(datetime.timezone.utc).isoformat()
ALLOWED = ['README.md', 'verify_package.py', 'PAYLOAD_MEMBERS.txt',
           'SUPPORT_MANIFEST.json', 'pr1085_support_v1_0.zip', 'UPLOAD_BINDINGS.json']

def sha(body): return hashlib.sha256(body).hexdigest()
def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + '\n')
def pin(path, base):
    data=path.read_bytes()
    return {'path':str(path.relative_to(base)), 'bytes':len(data), 'sha256':sha(data)}
def need(ok, message):
    if not ok: raise ValueError(message)

def initialize():
    need(not (F/'BASELINE_INPUT_PINS.json').exists(), 'baseline already captured')
    rows=[pin(p,A) for p in sorted(A.rglob('*')) if p.is_file() and F not in p.parents]
    need(not any(p.is_symlink() for p in A.rglob('*') if F not in p.parents), 'unexpected symlink')
    dump(F/'BASELINE_INPUT_PINS.json', {'utc':STAMP, 'scope':'All immediate pre-terminal regular audit files, hash-only; terminal effort excluded.', 'files':rows})
    for name in ALLOWED:
        dest=F/'before'/'preprint_v1_0'/name
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(K/name,dest)
    dump(F/'AUTHORIZED_EXISTING_CHANGES.json', {'utc':STAMP, 'files':['preprint_v1_0/'+x for x in ALLOWED], 'scope':'Only terminal prose/accounting/verifier plus necessary allowlist/manifest/ZIP/binding. Before bytes captured before mutation. All math/PDF/metadata/history unchanged.'})
    (F/'RESEARCH_LOG.md').write_text('# PR1085 terminal administration\n\n'+STAMP+' — Froze all '+str(len(rows))+' immediate inputs, and exact before bytes of six permitted existing edits. Assigned administrative execution 10%; whole reviews already complete, root terminal adoption and services remain outside scope.\n')

def mutate():
    base=json.loads((F/'BASELINE_INPUT_PINS.json').read_text())
    frozen={r['path']:r for r in base['files']}
    selected=[]; exclusions=[]
    old_snapshots={'preprint_v1_0/'+n for n in ALLOWED if not n.endswith('.zip')}
    root_names={'ROOT_WHOLE_PACKAGE_REVIEW_01.json','ROOT_WHOLE_PACKAGE_REVIEW_02.json','ROOT_PREPRINT_REVIEW_01.json'}
    excluded_names={'.gitignore','COMMANDS.json','COMMAND_RECEIPTS.json','REAL_COMPILE_NORMAL.json','REAL_COMPILE_OPTIMIZED.json','initialize.py','seal_review.py','reproduce_package.py','reproduce_and_attack.py'}
    for row in base['files']:
        src=row['path']; path=Path(src)
        include=src in old_snapshots or src in root_names or (path.parts[:2] in [('reviews','package_01'),('reviews','package_02')] and 'private' not in path.parts and path.name not in excluded_names)
        if include:
            origin=(F/'before'/src) if src in old_snapshots else A/src
            data=origin.read_bytes(); need(len(data)==row['bytes'] and sha(data)==row['sha256'], 'source before copy '+src)
            target='evidence/terminal/'+src
            dest=K/target; dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
            item={'source_relative_audit':src,'copy':target,'bytes':len(data),'sha256':sha(data)}
            if src in old_snapshots: item['source_snapshot_relative_audit']=str(origin.relative_to(A))
            selected.append(item)
        else:
            if 'private' in path.parts: reason='Third-party source extract; not distributed.'
            elif path.name in {'COMMANDS.json','COMMAND_RECEIPTS.json','REAL_COMPILE_NORMAL.json','REAL_COMPILE_OPTIMIZED.json'}: reason='Raw command/compiler streams remain local; authored reports and bounded identity receipts selected.'
            elif src == 'preprint_v1_0/pr1085_support_v1_0.zip': reason='The exact previous authored support archive is retained in local before custody; no nested old archive is distributed.'
            elif src == 'preprint_v1_0/paper.pdf': reason='The unchanged authored paper already remains the primary current PDF payload; no duplicate terminal copy is added.'
            elif src.startswith('preprint_v1_0/'): reason='Already preserved prepared-stage payload, exact historical evidence or local preparation derivative; not duplicated as terminal evidence.'
            elif path.suffix in {'.pdf','.png','.gz','.zip','.log'}: reason='Primary third-party body, derivative pixel/log, operational capture or old archive; not added to terminal evidence.'
            elif path.name in excluded_names: reason='Operational environment/sealing/reproduction utility or ignore rule; not a portable proof input.'
            else: reason='Already preserved prepared-stage material, private source/custody, duplicate historical copy or root-local operational record; no extra distribution needed.'
            exclusions.append({**row,'reason':reason})
    shutil.copyfile(F/'BASELINE_INPUT_PINS.json',K/'TERMINAL_INPUT_PINS.json')
    dump(K/'TERMINAL_COPY_MAP.json',{'scope':'Exact selected authored review/root records and before-edit snapshots; original preparation copy map is unchanged. Locators and source_snapshot refer to local audit custody, not a promise every source is distributed.','files':selected})
    dump(K/'TERMINAL_EXCLUSIONS.json',{'scope':'Every immediate frozen terminal input not selected; exact per-source partition. Original preparation exclusions are unchanged.','files':exclusions})
    terminal={'schema':1,'utc':STAMP,'pr':1085,'problem_id':20000488,'audited_head':'5e23f0c801d23976830657d2eef2b32bdc7da05a',
      'status':'TERMINAL_ADMIN_CHECKED_PENDING_ROOT_INTEGRITY_ADOPTION','whole_reviews_completed':2,'minimum_whole_reviews':2,
      'latest_actionable_P0_P1_P2_P3':0,'root_terminal_integrity_adoption_required':True,
      'publication_ready':False,'all_actionable_issues_resolved':False,'published':False,
      'services_hold':'preceding PR1032 priority cursor','historical_STATUS_preserved':True,
      'priority':'UNKNOWN_EXACT_REMAINING_GEOMETRIC_FORMULATIONS','novelty':'UNKNOWN','worldwide_open_status':'UNKNOWN','independent_discovery':'UNKNOWN',
      'human_peer_review':False,'formal_proof_certificate':False,
      'paper_pdf_sha256':'464de043ac6b723f3bd5c03dddb6efd1c0bfeb05b5209bb532006580b7aedc2d',
      'paper_tex_sha256':'c18a6ed12250dcee413e85f9a6297c525015396f151cdab8d89a6eb76938046d',
      'review_evidence':[{'review':n,'verdict':'evidence/terminal/reviews/package_0'+str(n)+'/VERDICT.json','output_pins':'evidence/terminal/reviews/package_0'+str(n)+'/OUTPUT_PINS.json','seal':'evidence/terminal/reviews/package_0'+str(n)+('/FINAL_SEAL.json' if n==1 else '/SEAL.json'),'root_adoption':'evidence/terminal/ROOT_WHOLE_PACKAGE_REVIEW_0'+str(n)+'.json'} for n in [1,2]],
      'meaning':'Two fresh complete reviews both found zero actionable concerns and were adopted by root. This bounded administrative record is not a new mathematical review, publication clearance, human refereeing or firstness certificate. The external root terminal integrity seal determines release readiness.'}
    dump(K/'TERMINAL_ACCOUNTING.json',terminal)
    readme=(F/'before/preprint_v1_0/README.md').read_text()
    old='STATUS.json records readiness and all-issues-clearance false, zero **new** whole-package reviews, and a minimum of two fresh whole-package reviews plus root adoption. Publication services are held behind PR #1032\'s priority cursor. Dated historical records are not current readiness assertions.'
    new='The unchanged dated preparation STATUS.json records the pre-review stage. TERMINAL_ACCOUNTING.json now records two completed **new** complete whole-package reviews (minimum two), both with zero actionable P0–P3 findings and both adopted by root. Current readiness and all-issues-clearance remain false pending the external root terminal integrity adoption. Publication services remain held behind PR #1032\'s priority cursor. Historical preparation and review records retain exact original bytes and their captured-stage meaning.'
    need(old in readme,'expected exact old paragraph');readme=readme.replace(old,new)
    readme+='\n## Terminal administrative evidence\n\nTERMINAL_INPUT_PINS.json hash-freezes all immediate pre-terminal inputs. TERMINAL_COPY_MAP.json and TERMINAL_EXCLUSIONS.json form their exact source-by-source partition. Selected authored whole01/02 reports, independent derivations/checkers, bounded source-interface/custody receipts and root adoptions are exact copies in evidence/terminal/. Five small before-edit snapshots retain their old bytes; the previous support ZIP stays only in local custody. Raw compiler/command streams, third-party bodies, source extracts, pixels, runtimes and old archives are not added. Earlier locators and receipts are historical; no omitted program or original no-executable submission is represented as newly replayed. The original preparation copy/exclusion maps, status, reports, pins and seals are unchanged.\n\nThe operative verifier checks both the preserved preparation stage and the separate terminal accounting. It requires two reviews, latest zero findings, exact root review adoption/output-manifest identities and the complete terminal copy/exclusion partition. It rejects premature readiness, service-hold bypass, false priority/novelty/refereeing promotion and missing or changed review evidence. The terminal administration changes neither the proof nor the paper PDF, mathematical checker, writer guards or exact bibliographic metadata. The unchanged paper has already been actually compiled in both modes and all seven pages actually viewed by both whole reviewers. No new compilation or image-generation claim is made by this administrative step.\n'
    (K/'README.md').write_text(readme)
    verifier=(F/'before/preprint_v1_0/verify_package.py').read_text()
    anchor='    require(regular(ROOT / "paper.pdf").read_bytes().startswith(b"%PDF-"), "paper PDF signature")\n'
    block='''    # Original STATUS is an immutable preparation snapshot; terminal accounting
    # is separate and cannot itself confer root release readiness.
    terminal = read_json(ROOT / "TERMINAL_ACCOUNTING.json")
    require(type(terminal.get("schema")) is int and terminal["schema"] == 1, "terminal schema")
    require(terminal.get("pr") == 1085 and type(terminal["pr"]) is int and
            terminal.get("problem_id") == 20000488 and
            terminal.get("audited_head") == status["audited_head"], "terminal identity")
    require(terminal.get("status") == "TERMINAL_ADMIN_CHECKED_PENDING_ROOT_INTEGRITY_ADOPTION", "terminal stage")
    for key in ["whole_reviews_completed", "minimum_whole_reviews"]:
        require(type(terminal.get(key)) is int and terminal[key] == 2, "terminal two reviews: " + key)
    require(type(terminal.get("latest_actionable_P0_P1_P2_P3")) is int and
            terminal["latest_actionable_P0_P1_P2_P3"] == 0, "latest review zero findings")
    require(terminal.get("root_terminal_integrity_adoption_required") is True and
            terminal.get("historical_STATUS_preserved") is True, "root adoption and historical stage")
    for key in ["publication_ready", "all_actionable_issues_resolved", "published",
                "human_peer_review", "formal_proof_certificate"]:
        require(terminal.get(key) is False, "terminal forbidden promotion: " + key)
    require(terminal.get("services_hold") == status["services_hold"], "terminal ordered hold")
    for key in ["priority", "novelty", "worldwide_open_status", "independent_discovery"]:
        require(terminal.get(key) == status[key], "terminal historical scope: " + key)
    for name, key in [("paper.pdf", "paper_pdf_sha256"), ("paper.tex", "paper_tex_sha256")]:
        require(sha(regular(ROOT / name).read_bytes()) == terminal.get(key), "unchanged paper identity")
    terminal_inputs = read_json(ROOT / "TERMINAL_INPUT_PINS.json")["files"]
    terminal_frozen = {r["path"]: r for r in terminal_inputs}
    require(len(terminal_frozen) == len(terminal_inputs), "unique terminal input paths")
    terminal_copies = read_json(ROOT / "TERMINAL_COPY_MAP.json")["files"]
    terminal_exclusions = read_json(ROOT / "TERMINAL_EXCLUSIONS.json")["files"]
    selected_paths = [r["source_relative_audit"] for r in terminal_copies]
    excluded_paths = [r["path"] for r in terminal_exclusions]
    require(len(set(selected_paths)) == len(selected_paths) and
            len(set(excluded_paths)) == len(excluded_paths) and
            set(selected_paths).isdisjoint(excluded_paths) and
            set(selected_paths + excluded_paths) == set(terminal_frozen), "terminal complete custody partition")
    require(len({r["copy"] for r in terminal_copies}) == len(terminal_copies), "unique terminal destinations")
    for row in terminal_copies:
        old = terminal_frozen[row["source_relative_audit"]]
        require(row["copy"] == "evidence/terminal/" + row["source_relative_audit"] and
                row["copy"] in names and row["bytes"] == old["bytes"] and
                row["sha256"] == old["sha256"], "terminal source/copy identity")
        data = regular(ROOT / row["copy"]).read_bytes()
        require(len(data) == row["bytes"] and sha(data) == row["sha256"], "terminal exact copied bytes")
    for row in terminal_exclusions:
        old = terminal_frozen[row["path"]]
        require(row["bytes"] == old["bytes"] and row["sha256"] == old["sha256"] and
                isinstance(row.get("reason"), str) and bool(row["reason"]), "terminal individual exclusion")
    expected_evidence = [{"review": n,
        "verdict": "evidence/terminal/reviews/package_0" + str(n) + "/VERDICT.json",
        "output_pins": "evidence/terminal/reviews/package_0" + str(n) + "/OUTPUT_PINS.json",
        "seal": "evidence/terminal/reviews/package_0" + str(n) + ("/FINAL_SEAL.json" if n == 1 else "/SEAL.json"),
        "root_adoption": "evidence/terminal/ROOT_WHOLE_PACKAGE_REVIEW_0" + str(n) + ".json"}
        for n in [1, 2]]
    require(terminal.get("review_evidence") == expected_evidence, "exact two review interfaces")
    for evidence in expected_evidence:
        verdict = read_json(ROOT / evidence["verdict"])
        adoption = read_json(ROOT / evidence["root_adoption"])
        seal = read_json(ROOT / evidence["seal"])
        output_hash = sha(regular(ROOT / evidence["output_pins"]).read_bytes())
        require(seal.get("output_pins_sha256") == adoption.get("output_pins_sha256") == output_hash,
                "exact reviewed output-manifest/root adoption binding")
        require(adoption.get("whole_reviews_completed") == evidence["review"] and
                type(adoption["whole_reviews_completed"]) is int and
                adoption.get("minimum_whole_reviews") == 2 and
                type(adoption.get("actionable_P0_P1_P2_P3")) is int and
                adoption["actionable_P0_P1_P2_P3"] == 0 and
                adoption.get("publication_ready") is False and adoption.get("published") is False and
                adoption.get("services_held_after_pr") == 1032, "root review adoption semantics")
        expected_status = ("ADOPT_COMPLETE_WHOLE01_ZERO_ACTIONABLE_PENDING_REQUIRED_NEW_WHOLE02"
                           if evidence["review"] == 1 else
                           "ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN")
        require(adoption.get("status") == expected_status, "captured root review stage")
        require(verdict.get("audited_head") == status["audited_head"] and
                verdict.get("pr") == 1085 and verdict.get("problem_id") == 20000488,
                "review verdict identity")
        if evidence["review"] == 1:
            require(verdict.get("verdict") == "ZERO_ACTIONABLE_P0_P1_P2_P3" and
                    verdict.get("findings") == [] and all(type(verdict.get(k)) is int and verdict[k] == 0
                    for k in ["P0", "P1", "P2", "P3"]), "whole01 zero finding semantics")
        else:
            require(verdict.get("status") == "PASS_ZERO_ACTIONABLE_P0_P1_P2_P3" and
                    verdict.get("actionable_findings") == [] and
                    verdict.get("root_adoption_required") is True and
                    verdict.get("publication_ready_set_by_this_review") is False and
                    all(type(verdict.get("severity_counts", {}).get(k)) is int and
                    verdict["severity_counts"][k] == 0 for k in ["P0", "P1", "P2", "P3"]),
                    "whole02 zero finding semantics")
'''
    need(anchor in verifier,'exact verifier insertion anchor')
    verifier=verifier.replace(anchor,block+anchor)
    verifier=verifier.replace('"publication_ready": False, "new_whole_reviews": 0,','"publication_ready": False, "new_whole_reviews": 2,\n            "terminal_exact_copies": len(terminal_copies), "terminal_individual_exclusions": len(terminal_exclusions),')
    verifier=verifier.replace('Universal proofs are in paper.tex; new whole reviews and root adoption are pending.','Universal proofs are in paper.tex; two complete whole reviews are recorded, external root terminal integrity adoption remains required, and services are held after PR1032.')
    (K/'verify_package.py').write_text(verifier)
    old_names=(F/'before/preprint_v1_0/PAYLOAD_MEMBERS.txt').read_text().splitlines()
    new_names=sorted(set(old_names+[r['copy'] for r in selected]+['TERMINAL_INPUT_PINS.json','TERMINAL_COPY_MAP.json','TERMINAL_EXCLUSIONS.json','TERMINAL_ACCOUNTING.json']))
    (K/'PAYLOAD_MEMBERS.txt').write_text('\n'.join(new_names)+'\n')
    manifest=json.loads((F/'before/preprint_v1_0/SUPPORT_MANIFEST.json').read_text())
    manifest['files']=[pin(K/name,K) for name in new_names]
    dump(K/'SUPPORT_MANIFEST.json',manifest)
    result=subprocess.run([sys.executable,'-B',str(K/'build_archive.py'),'--output',str(F/'rebuilt.zip')],capture_output=True,text=True)
    need(result.returncode==0,result.stdout+result.stderr)
    (K/'pr1085_support_v1_0.zip').write_bytes((F/'rebuilt.zip').read_bytes());(F/'rebuilt.zip').unlink()
    binding=json.loads((F/'before/preprint_v1_0/UPLOAD_BINDINGS.json').read_text())
    row=binding['files'][1];data=(K/row['filename']).read_bytes();row['bytes']=len(data);row['sha256']=sha(data)
    dump(K/'UPLOAD_BINDINGS.json',binding)
    dump(F/'BUILD_SUMMARY.json',{'utc':STAMP,'baseline_inputs':len(base['files']),'selected_terminal_copies':len(selected),'individual_terminal_exclusions':len(exclusions),'archive_members':len(new_names)+1,'archive_bytes':len(data),'archive_sha256':sha(data),'builder_stdout':result.stdout})
    with (F/'RESEARCH_LOG.md').open('a') as log: log.write('\n'+STAMP+' — Added separate two-review terminal accounting, exact selected review copies and per-source exclusions; preserved historical status/reports/seals and all mathematics/metadata. Administrative execution 50%; current clean controls and root adoption remain.\n')

if __name__=='__main__':
    if sys.argv[1:]==['initialize']: initialize()
    elif sys.argv[1:]==['mutate']: mutate()
    else: raise ValueError('use initialize or mutate')
