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
    assert json.loads((P/'inventory.json').read_bytes())['completed_count']==33
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
    closure(a43/'acceptance_v2_source_adversary_family','SELF_MANIFEST.json')
    closure(a44/'reviewed_candidate','MANIFEST.json')
    closure(a45/'current_preparation_family','PREPARATION_MANIFEST.json')
    closure(R/'unsolved_math_prioritization/attempts/30004386','MANIFEST.json')
    for n in ['final_acceptance_v2','root_checked_ready_and_original_merge_v2','root_actual_original_merge_v2_inspection','root_actual_original_merge_v3_inspection','root_actual_v2_acceptance_dated_Git','root_actual_v3_acceptance_dated_Git','integration_log_preimages']:tree(a43/n)
    for n in ['tmp/root_pr44_current_outer_20261003T021713.681669Z','tmp/root_pr44_current_build_20261003T021713.736020Z']:tree(a44/n)
    utc=dt.datetime.now(dt.timezone.utc).isoformat()
    texts=['PR42 accepted original3112848 and ROOT58523 complete post remain verified unchanged. UNSOLVED2/5/no newturns. Superseded/shared-main race, exact rollback and failed ROOT wrapper records retained. Workflow100%, target discovery0%.',
    'PR43 real original-head mergec60255489a342fae02c0acf3d1026255b47be3d1 published02:27:31Z. New different source118+self412b6812 PASS exacttwo-token repaired45+self11f39. ROOT70405 actualsource author verifies all1067 foreign identities, exactdelta/closures/realactualcapture schemas and authentic completed42 predecessor. Failed own69764 reader assumed generic capturekeys; preserved, corrected distinct70405 uses actualschema. Actual70783 finalseal, complete355-overlay/357+self canonical packet, exactparents/tree/body/creditedsource dispositions and native34targets41turns33primaries verified by actualROOT77832 completepost. Proper actualmergeauto-merged exit0: own72323 expectedconflict1 stopped after correctmerge, separate72991 inspection used wrong originalsizekey; failures preserved, corrected73398 full16/nativeautomaticqueue passed before overlay. No production/scienceguard weakened. Original0/5,new0/audit0,already_solved credited JKP DOI10.4064/sm210413-16-9, no projectnovelty/newpaperDOItracker. Workflow100%, project discovery0%.',
    'PR44 genuineROOT63648 closedsource/external prerequisite inspection verifies all366 foreign refs/full48+self+49+self closures. Actual64348 builder via reviewed64347 ROOTouter completes430+self currentfreeze; ROOT65947 independently checksallcurrent430/native13/deps/original18/twelveimmutablemathfiles and genuinefinalGit/outerevidence. Whole read-only nativefreeze epoch preserved; newsource-first whole adversary ACTIVE. Scopedstandardconditionalmath UNSOLVED2/5,new0/audit0,no novelpaper; preciseunmarked2type-pairmap and actualgeometricpair gaps unchanged. Currentfreeze workflow75%, full discovery0%.']
    for a,t in zip(aa,texts):
        with (a/'ROOT_RESEARCH_LOG.md').open('a')as f:f.write('\n'+utc+' — '+t+'\n')
        add(a/'ROOT_RESEARCH_LOG.md')
    with (P/'RESEARCH_LOG.md').open('a')as f:
        f.write('\n'+utc+' — Checkpoint33/180 accepted, completion18.333333333333332%. PR43 original-head merge and completeROOT actualpost done, credited prior resolution preserved, no projectpaper. PR44 real430+self currentfreeze independently inspected; new whole adversary ACTIVE excluded. PR45 currentSOURCE47+self closed with truefuture gates; NEWdifferent sourceadversary ACTIVE excluded. Original mathematical/source families and newbounded Asmussenfullsource comparison published with all64foreign/access/OCRbodies individually excluded. ROOT45 originalhelper reproduction remains pending. Allfailed ROOTexecution wrappers retained honestly. Git does not preserve full0444 or emptydirs: restore recordedlocalmodes before reproducing guards. No new DOI/tracker/release.\n')
    add(P/'RESEARCH_LOG.md');add(Path(__file__))
    rows=[]
    for n in sorted(names):
        b=(R/n).read_bytes();rows.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'observed_full_mode':stat.S_IMODE((R/n).stat().st_mode)})
    out=P/'checkpoints/CHECKPOINT_20261003_0230.json'
    with out.open('x')as f:json.dump({'schema':'ROOT_exact_owned_checkpoint/v1','utc':utc,'actual_pid':os.getpid(),'main_before':before,'completed_count':33,'total':180,'completion_estimate_percent':33/180*100,'owned_files':rows,'foreign_dirty_preimages_preserved':foreign,'foreign_primary_bodies_included':False,'active_families_included':False},f,indent=2);f.write('\n')
    add(out)
    subprocess.run(['git','add','-f','--',*sorted(names)],cwd=R,check=True)
    staged={n for n in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0')if n}
    assert staged.issubset(names)
    for n in staged:assert subprocess.check_output(['git','show',':'+n],cwd=R)==(R/n).read_bytes()
    for z in foreign:
        p=R/z['path'];b=p.read_bytes();assert len(b)==z['bytes'] and hashlib.sha256(b).hexdigest()==z['sha256'] and stat.S_IMODE(p.stat().st_mode)==z['full_mode']
    print(json.dumps({'status':'PASS_EXACT_OWNED_CHECKPOINT_STAGED','main_before':before,'owned_members':len(names),'staged_members':len(staged),'foreign_staged_members':0,'owned_bytes':sum(z['bytes']for z in rows),'completed_count':33,'total':180,'completion_estimate_percent':33/180*100}))
if __name__=='__main__':main()
