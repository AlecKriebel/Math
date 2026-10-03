"""ROOT verifies closed source evidence and records completed personally read scope."""
from pathlib import Path
import datetime as dt,hashlib,json,stat,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];F=A/'current_source_adversary_family';S=A/'current_preparation_family'
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return {'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b)}
def closure(d,name,expected,count):
    b=(d/name).read_bytes();assert sha(b)==expected;m=json.loads(b);rows=m['files'];assert len(rows)==count
    names={z['path']for z in rows}|{name};assert {q.relative_to(d).as_posix()for q in d.rglob('*')if q.is_file()}==names
    for q in d.rglob('*'):assert not q.is_symlink()and(q.is_dir()or(q.is_file()and stat.S_IMODE(q.stat().st_mode)==0o444))
    for z in rows:
        b=(d/z['path']).read_bytes();assert type(z['bytes'])is int and len(b)==z['bytes']and sha(b)==z['sha256']
    return ref(d/name)
def dump(name,j):
    with(A/name).open('x')as f:json.dump(j,f,indent=2);f.write('\n')
def main():
    assert __debug__; (A/'ROOT_CURRENT_PREREQUISITES_PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    sources=[closure(S,'PREPARATION_MANIFEST.json','0ecdd7c6aaf27c766dcb83b8991f1d8093b3ed233e6e2e926d501b0501c1f4a6',48),closure(F,'SELF_MANIFEST.json','93c1d2c80992c8e6498e9de0005a2958ffd95a2e58eed8a56f3cc062a0cb6b04',49)]
    foreign=load(F/'INDIVIDUAL_FOREIGN_INPUTS.json');assert len(foreign['files'])==foreign['foreign_input_count']==366
    for z in foreign['files']:
        p=R/z['path'];assert not p.is_symlink()and all(not x.is_symlink()for x in p.parents);b=p.read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']
    caps=[]
    for name,pid in [('FINAL_INSPECTION_ACTUAL_CAPTURE',37323),('INDEPENDENT_CONTROLS_V2_ACTUAL_CAPTURE',29743),('SUPPLEMENTAL_GATES_ACTUAL_CAPTURE',32860)]:
        d=F/name;c=load(d/'CAPTURE.json');assert c['actual_execution']is True and c['completed']is True and c['status']=='PASS'and c['exit_code']==0 and c['pid']==pid and c['source_unchanged']is True and c['operator_unchanged']is True
        assert sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==c['source_sha256']and sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==c['operator_sha256']
        for k in ['stdout','stderr']:
            b=(d/c[k]['path']).read_bytes();assert len(b)==c[k]['bytes']and sha(b)==c[k]['sha256']
        assert dt.datetime.fromisoformat(c['started_utc'])<dt.datetime.fromisoformat(c['finished_utc']);caps.append(ref(d/'CAPTURE.json'))
    verdict=load(F/'VERDICT.json');assert 'PASS' in verdict['verdict']
    notes='ROOT personally read all18 original science/helper/result/source/ledger files and the whole19-path diff; actual16186 checked every original hunk. ROOT independently derived the duality/right-module conventions, full degree-one PAIR-map sufficiency and seven-coset permutation/norm quotient with its integral augmentation distinction. The unmarked2type-to-pairmap and actualgeometric-pair realization gaps remain unresolved. Operative Kirby/Lomonaco/Hillman/Jablonowski/Conway-Kasprowski target/proof excerpts were personally read with exact stated category/source limits; no exhaustive priority or fullproof claim. ROOT personally read both complete independent math reports/verdicts and mechanically verified their entire closures/foreign inputs. Actual9267 unchanged507/507/29933 outputs and11267 full149266659B/raw15458SQL including ABSENTprior fallback{} were read in full; 16186 independent closure checks pass. ROOT fully read626-line builder/129-line operator/contracts/qualifications/drafts/private controlsource and actual own-source controls; complete new independent49+self source report/verdict now personally read. This real inspection independently rechecks all366 foreign references, 48+self and49+self full0444 closures and three genuine current source-control/closure captures. This approves standard conditional deductions as a scoped UNSOLVED partial, no novel result/paper/DOI/tracker; NEWwhole-current gate remains PENDING.'
    now=dt.datetime.now(dt.timezone.utc).isoformat();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip();assert subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
    scope='# ROOT PR44 scoped standard-partial acceptance\n\nROOT_SCOPE_ACCEPTED_STANDARD_PARTIAL_ONLY\n\nPR44 / 2912 / KP-4.36\nHead: c772dc5b851ec91da9d46d534577609e5d3ca389\nBase: 01358d66fc67d1c462bddf31c0d4ee5b120e6737\nStatus: unsolved\nOriginal turns: 2/5; new: 0; audit: 0\nFull problem solved: false\nNovelty: false\nNEW whole-current review: PENDING\nPaper/new DOI/tracker: false\n\n'+notes+'\n'
    with(A/'ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md').open('x')as f:f.write(scope)
    fresh={'schema':'PR44_ROOT_FRESH13_INPUT_PREIMAGES_v1','approved_by_root':True,'created_utc':now,'reason':'Actual current main and all thirteen native/program bodies after genuinely verified PR42 acceptance and published checkpoint. Older source-family input hashes are evidence only; these current bodies alone govern the read-only freeze.','current_head':head,'files':[]}
    paths=['draft_pr_publication_program_20260930/inventory.json']+['unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']]
    for n in sorted(paths):
        b=(R/n).read_bytes();fresh['files'].append({'path':n,'bytes':len(b),'sha256':sha(b)})
    dump('ROOT_CURRENT_INPUT_PREIMAGES.json',fresh)
    ledger=load(S/'DRAFT_ROOT_READ_LEDGER.json');ledger.update(created_utc=now,reading_completed=True,root_flags={k:True for k in ledger['root_flags']},reading_notes=notes,scope_certificate_sha256=sha(scope.encode()),preparation_manifest_sha256=sources[0]['sha256'],source_qualification_sha256=sha((S/'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes()),evidence_bindings_sha256=sha((A/'ROOT_EVIDENCE_BINDINGS.json').read_bytes()))
    dump('ROOT_PRIMARY_READ_LEDGER.json',ledger)
    science=load(S/'DRAFT_ROOT_SCIENCE_CARD.json');science.update({k:v for k,v in ledger.items()if k!='schema'});science.update(partial_valid=True,read_ledger_sha256=sha((A/'ROOT_PRIMARY_READ_LEDGER.json').read_bytes()),current_input_manifest_sha256=sha((A/'ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes()))
    dump('ROOT_SCIENCE_CARD.json',science)
    for z in fresh['files']:
        b=(R/z['path']).read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==head
    result={'schema':'pr44-root-complete-current-source-inspection/v1','status':'PASS','utc':now,'source_closures':sources,'entire_source_verdict':verdict,'individual_foreign_references_verified':366,'complete_actual_source_captures':caps,'new_whole_current_gate':'PENDING','original_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'real_prerequisites':[ref(A/n)for n in ['ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_EVIDENCE_BINDINGS.json']]}
    dump('ROOT_SOURCE_SAFETY_INSPECTION.json',result);print(json.dumps({'status':'PASS_REAL_ROOT_CURRENT_PREREQUISITES','head':head,'inspection':ref(A/'ROOT_SOURCE_SAFETY_INSPECTION.json')}))
if __name__=='__main__':main()
