from pathlib import Path
import json,hashlib,shutil,subprocess,datetime
D=Path(__file__).resolve().parent;P=D.parents[2]
family='likelihood_threshold_adversary_01';src=D/family;mf=src/'SAFE_AUTHORED_MANIFEST.json';m=json.loads(mf.read_text())['safe_authored_files']
for row in m:
 q=src/row['path'];raw=q.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
dst=D/'root_fresh_replays'/family;dst.mkdir(parents=True,exist_ok=True)
shutil.copyfile(src/'exact_controls.py',dst/'exact_controls.py')
py='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python'
r=subprocess.run([py,str(dst/'exact_controls.py')],capture_output=True,text=True,timeout=180);assert r.returncode==0,r.stderr
(dst/'stdout.txt').write_text(r.stdout);(dst/'stderr.txt').write_text(r.stderr)
assert (dst/'exact_controls_results.json').read_bytes()==(src/'exact_controls_results.json').read_bytes()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
old=json.loads((D/'ROOT_FRESH_FAMILY_REPLAY_ACCEPTANCE.json').read_text())
old['reviewer_families'].append(dict(family=family,manifest_sha256=hashlib.sha256(mf.read_bytes()).hexdigest(),safe_manifest_files=len(m),all_safe_bytes_verified=True,independent_controls_replayed=188,exact_byte_match=True,report_sha256=hashlib.sha256((src/'REPORT.md').read_bytes()).hexdigest()))
old.update(utc=now,status='PASS_THREE_INDEPENDENT_MATHEMATICAL_SOURCE_FAMILIES',all_reports_and_full_derivations_read_by_root=True,original_assertions_replayed=1996,fresh_assertions_replayed=3537)
(D/'ROOT_COMPLETE_MATHEMATICAL_ACCEPTANCE.json').write_text(json.dumps(old,indent=2)+'\n')
text='''# Root mathematical and source acceptance\n\n'''+now+''' — case35%. Three independent approach families complete and sealed: elimination/dominance, likelihood/PD/probability, and source-first quantifier reconstruction. All full reports and derivations read by root, every safe manifest payload rehashed, all fresh controls replayed from isolated root copies. Counts:188+1808 submitted exact controls;16+3333+188 fresh exact controls. These finite controls supplement universal written arguments.\n\nBoth stated colorings satisfy exact I3nonzero, I4zero and WMLT2. Singleton MLT4 is independently confirmed by the full prior theorem proof and a new specialized open3-sample failure/generic4-sample success proof. No mathematical repair is required. The inherited independent checker hardcodes its proof hash; its historical output is a provenance label, and intake/root byte hashing separately binds all20 actual original files. Do not treat that constant as dynamic verification.\n\nThe strongest source-independent conclusion is a counterexample to printed Proposition3(B)'s numerical WMLT=n implication, and to the full literal numerical scenarios under the unrestricted written model class. It satisfies the PD-intersection antecedentB; bareAorB remains unrefuted. No new assumption restricting the printed proposition to four-cycles may be invented. No exact tied-modelMLT or unknown-mean sample count is transferred. The current draft is mathematically valid within its express scope.\n\nPriority remains uncleared. Root has found exact old singleton coverage by Gross/Sullivant2015 plus Blekherman/Sinn2017 and a September2026 same-author coloredC4 counterexample. Two new independent priority families are reading those originals and testing exact target overlap. An unqualified novel resolution of the original bare conjecture is unsupported. A status/credit correction is a potential reasonable repair, not yet promoted. No manuscript, upload, DOI, tracker action, merge, closure, PRcomment or branch mutation is cleared at this checkpoint. Goal remains active/incomplete;42/19/19/0 counts and held293,292,280,239 unchanged.\n'''
(D/'ROOT_MATHEMATICAL_SYNTHESIS.md').write_text(text)
state=json.loads((D/'CURRENT_AUDIT_STATE.json').read_text());state.update(utc=now,completion_percent=35,stage='mathematics_and_precise_source_scope_pass_priority_audit_in_progress',mathematical_verdict='PASS under exact zero-mean RCON hypotheses; no mathematical repair',source_verdict='PASS scoped printed numerical implication; bare SOS/intersection alternative unrefuted',priority_verdict='Pending two fresh primary-source families; exact earlier covering results located')
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
s=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text());s.update(utc=now,case_completion_percent=35,current_stage=state['stage'],mathematical_verdict=state['mathematical_verdict'],source_verdict=state['source_verdict'],priority_verdict=state['priority_verdict']);(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(s,indent=2)+'\n')
for q in [D/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with q.open('a') as f:f.write('\n## '+now+': PR212 mathematical/source acceptance —35%\n\nAll three new mathematical/source families sealed and root-validated.1996 original +3537 fresh exact controls reproduce; full written arguments and source pages checked. No mathematical defect. Exact scoped numerical counterexample only; bareAorB unresolved. Two priority families independently testing old singleton combination and new September2026 same-author colored-cycle theorem before any promotion. No paper/provider/PR/queue/DB/tracker action; counts42/19/19/0; goal active/incomplete. Disk recovery losslessly compressed60 completed-ownPR214 private transportJSONs, saving19012731bytes; actualscience/receipts untouched, exactrestorepaths/hashes inDISK_RECOVERY_RECEIPT.json.\n')
src=(D/'publish_initial_checkpoint.py').read_text().replace('INITIAL_CHECKPOINT_PUBLICATION_RECEIPT.json','MATHEMATICAL_CHECKPOINT_PUBLICATION_RECEIPT.json')
a=src.index("review=D/'source_scope_adversary_01'");b=src.index("selection=P/'next_selection_after_pr214_20261015'",a)
src=src[:a]+'''for name in ['source_scope_adversary_01','elimination_dominance_adversary_01','likelihood_threshold_adversary_01']:
    review=D/name
    manifest=json.loads((review/'SAFE_AUTHORED_MANIFEST.json').read_text())
    manifest=manifest if isinstance(manifest,list) else manifest['safe_authored_files']
    for row in manifest:
        q=review/row['path'];raw=q.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        paths.append(q)
    paths.append(review/'SAFE_AUTHORED_MANIFEST.json')
paths += [q for q in (D/'root_fresh_replays').rglob('*') if q.is_file()]
'''+src[b:]
src=src.replace('Checkpoint PR212 at15%: frozen claimed-solved intake, direct source reconstruction and reproducible controls','Checkpoint PR212 at35%: three independent mathematical-source families verified; priority audit in progress').replace('case_completion_percent=15','case_completion_percent=35')
(D/'publish_mathematical_checkpoint.py').write_text(src)
print(json.dumps({'utc':now,'status':old['status'],'original_exact':1996,'fresh_exact':3537,'case_percent':35},indent=2))
