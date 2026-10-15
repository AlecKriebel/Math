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
    aa=[P/'audits/pr42_2233',P/'audits/pr43_30004386',P/'audits/pr44_2912',P/'audits/pr45_9900007'];a42,a43,a44,a45=aa
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
    closure(a44/'whole_current_source_first_family','SELF_MANIFEST.json')
    tree(a44/'root_complete_dated_four_actual_Git')
    closure(a45/'current_source_adversary_family','OWN_CLOSURE.json')
    closure(a45/'root_original_actual_reproduction','MANIFEST.json')
    closure(a45/'reviewed_candidate','MANIFEST.json')
    execution=json.loads((a45/'reviewed_candidate/CURRENT_EXECUTION_REFERENCE.json').read_bytes())
    tree(a45/execution['audit_relative_outer_capture']);tree(a45/execution['audit_relative_inner_attempt'])
    utc=dt.datetime.now(dt.timezone.utc).isoformat()
    texts=['PR42 actual original-head acceptance and complete58523 post remain verified. Workflow100%, target discovery0%.',
    'PR43 actual original-head acceptance c602554 and complete77832 post remain verified;33of180 accepted. Credited prior resolution, no projectnovelty/newpaperDOItracker. Workflow100%, project discovery0%.',
    'PR44 fresh whole-current source-first96+self ea6416 clean, operative79792 controls75769/51hostiles and final88925 genuine closure fully read. ROOT95178 full96+self and964foreign checks passed after preserved94701 prelaunch mutable-field mistake. The whole foreign964 list excludes native4;95178 had correctly checked own ten immutable Git records but empty direct ROOT arrays. Corrected separate actualROOT1084 directly queried frozen2b9d023 four100644 completebodies/eightrealGitcaptures and updated whole ROOT23535B54c094...; originalV2record retained verbatim. SOURCEacceptanceprep ACTIVE excluded; no finalacceptance. UNSOLVED2/5,new0/audit0,bothrealizationgaps retained. Workflow85%, discovery0%.',
    'PR45 original mathematical families complete; ROOT independently reconciled all-fixedcoupling proof, weakwindow/metric/tightoffset/setwise limits and primarysource scope. Newsource70+self bc8495 clean report personally read; SOURCE47+self and319fixedinputs+64excludedforeign checked. Actual88783 three unchangedhelpers885/885/3044 entirebyteexact; raw88914 failed ownplain-vs-wrapper equality afterwholeSQL, corrected distinct89614 confirms all149266659B and15458SQL plus PRESENT AMR prior dict exactlynestedupstream. Closure96803 overly banned commonempty stderr, corrected97408 preservesoldstage/source and checks entirefirstpartyclosedD with zero foreignbodycopy. GenuineROOT99416 fiveprereqs/9flags then99703outer->99704 actualcurrentbuilder freezes497+self;2177 completecurrent497/416deps/native13/wholeouter/final47Git inspected. Newwhole-current source-first adversary ACTIVE excluded. UNSOLVED1/5,new0/audit0,no novelpaperDOItracker; broadcharacterizationgap. Workflow75%, discovery0%.']
    for a,t in zip(aa,texts):
        with (a/'ROOT_RESEARCH_LOG.md').open('a')as f:f.write('\n'+utc+' — '+t+'\n')
        add(a/'ROOT_RESEARCH_LOG.md')
    with (P/'RESEARCH_LOG.md').open('a')as f:
        f.write('\n'+utc+' — Checkpoint33/180 accepted, completion18.333333333333332%. PR44 whole source/math review and genuine ROOT complete evidence reconciled; SOURCE acceptance preparation ACTIVE excluded. PR45 genuine original reproduction and corrected complete rawSQL/present prior verified; current497+self frozen and ROOTchecked, NEWwhole-current adversary ACTIVE excluded. All ROOT own failed/corrected wrappers preserved; no source guard weakened or original mathematical scope expanded. All foreign primary/cache/SQL/OCR/access bodies excluded; Git native stdout is first-party procedural evidence. Full0444/emptydirs local observations require restoration in fresh checkout. No newpaperDOItracker/release.\n')
    add(P/'RESEARCH_LOG.md');add(Path(__file__))
    rows=[]
    for n in sorted(names):
        b=(R/n).read_bytes();rows.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'observed_full_mode':stat.S_IMODE((R/n).stat().st_mode)})
    out=P/'checkpoints/CHECKPOINT_20261003_0300.json'
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
