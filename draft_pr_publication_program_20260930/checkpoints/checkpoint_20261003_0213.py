"""Publish an exact whitelist of completed first-party audit findings only."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, subprocess
P=Path(__file__).resolve().parents[1];R=P.parent
names=set()
def add(p):
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    assert p.stat().st_size<=100*1024*1024,str(p)
    names.add(p.relative_to(R).as_posix())
def tree(p):
    assert p.is_dir() and not p.is_symlink()
    for q in p.rglob('*'):
        assert not q.is_symlink()
        if q.is_file():add(q)
def closure(p,name):
    j=json.loads((p/name).read_bytes())
    for z in j['authored_members'] if name=='SELF_ONLY_CLOSURE.json' else j['files']:
        if z['path']==name:continue
        q=p/z['path'];b=q.read_bytes();assert len(b)==z['bytes'] and hashlib.sha256(b).hexdigest()==z['sha256'] and stat.S_IMODE(q.stat().st_mode)==0o444
        if z.get('publication_allowed',True) is True:add(q)
    assert stat.S_IMODE((p/name).stat().st_mode)==0o444;add(p/name)
def main():
    assert __debug__
    assert subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
    assert subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R)==b''
    before=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
    assert json.loads((P/'inventory.json').read_bytes())['completed_count']==32
    foreign=[]
    for n in subprocess.check_output(['git','diff','--name-only','-z'],cwd=R).decode().split('\0'):
        if n and not n.startswith(P.name+'/'):
            b=(R/n).read_bytes();foreign.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'full_mode':stat.S_IMODE((R/n).stat().st_mode)})
    aa=[P/'audits/pr42_2233',P/'audits/pr43_30004386',P/'audits/pr44_2912'];a42,a43,a44=aa; a45=P/'audits/pr45_9900007'
    for a in aa:
        for q in a.iterdir():
            if q.is_file():add(q)
        for q in a.glob('root_*'):
            if q.is_dir() and ('capture' in q.name or 'dated_' in q.name):tree(q)
    for q,n in [(a42/'acceptance_preparation_family','PREPARATION_MANIFEST.json'),(a42/'acceptance_preparation_family_v2','PREPARATION_MANIFEST.json'),(a42/'acceptance_source_adversary_family','OWN_CLOSED_MANIFEST.json'),(a42/'acceptance_v2_source_adversary_family','OWN_CLOSED_MANIFEST.json'),(a43/'whole_current_source_first_family','SELF_MANIFEST.json'),(a44/'duality_algebra_family','AUTHORSHIP_MANIFEST.json'),(a44/'literal_realization_family','SELF_ONLY_CLOSURE.json'),(a44/'current_preparation_family','PREPARATION_MANIFEST.json'),(a44/'root_original_actual_reproduction','MANIFEST.json')]:closure(q,n)
    for q,n in [(a43/'acceptance_preparation_family','PREPARATION_MANIFEST.json'),(a43/'acceptance_preparation_family_v2','PREPARATION_MANIFEST.json'),(a43/'acceptance_source_adversary_family','SELF_MANIFEST.json'),(a44/'current_source_adversary_family','SELF_MANIFEST.json'),(a45,'ORIGINAL_PREPARATION_MANIFEST.json'),(a45/'probability_metric_family','OWN_CLOSURE.json'),(a45/'literal_priority_family','FINAL_CLOSURE_MANIFEST.json')]:closure(q,n)
    add(a45/'probability_metric_family/OWN_CLOSURE.sha256')
    for q in a45.glob('*actual_capture'):
        if q.is_dir():tree(q)
    for n in ['final_acceptance_v2','superseded_preflight_after_concurrent_PR387','superseded_preflight_after_concurrent_PR386','rejected_original_merge_after_concurrent_PR386','rejected_original_merge_after_concurrent_PR386_v3','root_checked_ready_and_original_merge_v4','root_actual_original_merge_v4_inspection','integration_log_preimages']:tree(a42/n)
    closure(R/'unsolved_math_prioritization/attempts/2233','MANIFEST.json')
    for n in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl',P.name+'/inventory.json']:add(R/n)
    utc=dt.datetime.now(dt.timezone.utc).isoformat()
    texts=['PR42 actual original-head merge311284853ce13a5fa8fac934a87e1e379a976fc2 published at02:08:35Z. Final closed395+self accepted packet and genuine ROOT58523 independent complete post verify all393 merge bodies, exact parents/tree, whole named queue patch, all32 prior native states/history prefix, one present event, entire inventory and all13 allowed preimages. 32/180=17.7778%; UNSOLVED original2/5,new0/audit0/no newpaperDOItracker. Two superseded preflights, improper original-merge continuation after failedHEAD check, actual full-preservation rollback and all failed wrappers retained honestly. Final V4 checked readiness/main gating performed correct original merge; its own verification then stopped on wrong ROOT queue-path spelling. Corrected distinct readonly inspector52842 verified actual intended queue conflict and exact17 originals before overlay; no science/source guard weakened. Workflow100%, full discovery0%.',
    'PR43 mathematical/current/whole gates complete, prior published theorem already_solved, original0/5/new0/audit0. New original-source adversary119+self found overlay snapshot filename and mirror scope-token defects. Adjacent source45+self narrowly fixes exactlytwo production tokens; original failed source+verdict retained, new DIFFERENT V2 sourceadversary pending. ROOT complete actualPR42 predecessor now exists, future43 approval and acceptance still pending. Full-target project discovery0%.',
    'PR44 scoped UNSOLVED original2/5,new0/audit0/no novelpaper. Both independent mathematical families and actual ROOT507/507/29933 original reproduction pass with both precise geometric realization gaps. Closed current48+self and new independent source49+self clean after ROOT audit-relative evidencebinding correction; old erroneousbinding retained. ROOT has personally read full builder/operator/contracts/own controlsource and new complete report+verdict. Current ROOT external approval/freeze, NEWwhole adversary and acceptance remain pending. Scientific scoped audit100%, target discovery0%.']
    for a,t in zip(aa,texts):
        with (a/'ROOT_RESEARCH_LOG.md').open('a')as f:f.write('\n'+utc+' — '+t+'\n')
        add(a/'ROOT_RESEARCH_LOG.md')
    with (P/'RESEARCH_LOG.md').open('a')as f:
        f.write('\n'+utc+' — Checkpoint32/180 accepted, completion17.77777777777778%. PR42 real merge and ROOT independent actual post complete; all superseded/failure/rollback evidence retained. PR43 exacttwo-token acceptance repairs await new V2 adversary; PR44 closed source review clean/current freeze pending. PR45 original18/diff export and two independent partial mathematical/source audits complete; NEW full Asmussen1992 primary access boundedcomparison included, original access history unchanged. ROOT45 original reproduction remains pending. ACTIVE PR43 newV2 adversary and PR45 current SOURCEpreparation excluded. Restricted/foreign PDF,text,pixel bodies and raw/SQL caches excluded. Full0444 dated mode observations require restoration in a fresh clone: Git only stores executable flags, not full modes or empty directories. No new paper/DOI/tracker for these partial outcomes.\n')
    add(P/'RESEARCH_LOG.md');add(Path(__file__))
    rows=[]
    for n in sorted(names):
        b=(R/n).read_bytes();rows.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'observed_full_mode':stat.S_IMODE((R/n).stat().st_mode)})
    out=P/'checkpoints/CHECKPOINT_20261003_0213.json'
    with out.open('x')as f:json.dump({'schema':'ROOT_exact_owned_checkpoint/v1','utc':utc,'actual_pid':os.getpid(),'main_before':before,'completed_count':32,'total':180,'completion_estimate_percent':32/180*100,'owned_files':rows,'foreign_dirty_preimages_preserved':foreign,'foreign_primary_bodies_included':False,'active_families_included':False},f,indent=2);f.write('\n')
    add(out)
    subprocess.run(['git','add','-f','--',*sorted(names)],cwd=R,check=True)
    staged={n for n in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0')if n}
    assert staged.issubset(names)
    for n in staged:assert subprocess.check_output(['git','show',':'+n],cwd=R)==(R/n).read_bytes()
    for z in foreign:
        p=R/z['path'];b=p.read_bytes();assert len(b)==z['bytes'] and hashlib.sha256(b).hexdigest()==z['sha256'] and stat.S_IMODE(p.stat().st_mode)==z['full_mode']
    print(json.dumps({'status':'PASS_EXACT_OWNED_CHECKPOINT_STAGED','main_before':before,'owned_members':len(names),'staged_members':len(staged),'foreign_staged_members':0,'owned_bytes':sum(z['bytes']for z in rows),'completed_count':32,'total':180,'completion_estimate_percent':32/180*100}))
if __name__=='__main__':main()
