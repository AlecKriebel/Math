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
        q=p/z['path'];b=q.read_bytes();assert len(b)==z['bytes'] and hashlib.sha256(b).hexdigest()==z['sha256'] and stat.S_IMODE(q.stat().st_mode)==0o444
        add(q)
    assert stat.S_IMODE((p/name).stat().st_mode)==0o444;add(p/name)
def main():
    assert __debug__
    assert subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
    assert subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R)==b''
    before=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
    assert json.loads((P/'inventory.json').read_bytes())['completed_count']==31
    foreign=[]
    for n in subprocess.check_output(['git','diff','--name-only','-z'],cwd=R).decode().split('\0'):
        if n and not n.startswith(P.name+'/'):
            b=(R/n).read_bytes();foreign.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'full_mode':stat.S_IMODE((R/n).stat().st_mode)})
    aa=[P/'audits/pr42_2233',P/'audits/pr43_30004386',P/'audits/pr44_2912'];a42,a43,a44=aa
    for a in aa:
        for q in a.iterdir():
            if q.is_file():add(q)
        for q in a.glob('root_*'):
            if q.is_dir() and ('capture' in q.name or 'dated_' in q.name):tree(q)
    for q,n in [(a42/'acceptance_preparation_family','PREPARATION_MANIFEST.json'),(a42/'acceptance_preparation_family_v2','PREPARATION_MANIFEST.json'),(a42/'acceptance_source_adversary_family','OWN_CLOSED_MANIFEST.json'),(a42/'acceptance_v2_source_adversary_family','OWN_CLOSED_MANIFEST.json'),(a43/'whole_current_source_first_family','SELF_MANIFEST.json'),(a44/'duality_algebra_family','AUTHORSHIP_MANIFEST.json'),(a44/'literal_realization_family','SELF_ONLY_CLOSURE.json'),(a44/'current_preparation_family','PREPARATION_MANIFEST.json'),(a44/'root_original_actual_reproduction','MANIFEST.json')]:closure(q,n)
    utc=dt.datetime.now(dt.timezone.utc).isoformat()
    texts=['PR42 source V1 sealer97064 failed before output publication; exact failure retained. Adjacent V2 source51+self and new independent adversary35+self are clean. ROOT23869 independently verified all1093 outside references, four dated Git bodies and complete exact closures/delta/actual captures. Original2/5,new0/audit0,EP653UNSOLVED; audit100%, final acceptance still pending.',
           'PR43 new whole-current30+self and ROOT1322 independent closure inspection pass; original0/5,new0/audit0,credited prior publication already_solved. Full prior source theorem verified with stated corrections; no project novelty/new paper/DOI/tracker. Audit100%, final-source approval and actual predecessor42/merge pending. Failed ROOT capture/source attempts remain retained.',
           'PR44 both materially distinct independent math families54+self and13+self pass with explicit unresolved geometric gap. ROOT9267 unchanged507/507/29933 outputs byte exact; ROOT11267 full149266659B/raw15458SQL checks pass, prior-keyABSENT. ROOT16186 exact18hunk reconstruction/family topology and own36+self reproduction closure pass. First ROOT evidencebinding used incompatible repository-relative paths; retained verbatim, operative binding uses required audit-relative refs. Closed current source48+self awaits NEWdifferent adversary. Original2/5,new0/audit0,UNSOLVED; scoped scientific audit100%, discovery0%, current+whole+acceptance pending.']
    for a,t in zip(aa,texts):
        with (a/'ROOT_RESEARCH_LOG.md').open('a')as f:f.write('\n'+utc+' — '+t+'\n')
        add(a/'ROOT_RESEARCH_LOG.md')
    with (P/'RESEARCH_LOG.md').open('a')as f:
        f.write('\n'+utc+' — Checkpoint31/180 accepted, completion17.22222222222222%. PR42 repaired source and fresh adversary clean; PR43 full credited-source/current whole audits complete; PR44 qualified partial math and original reproduction complete. All actual failures retained. ACTIVE acceptance43 and sourceadversary44 excluded. Restricted/foreign PDF,text,pixel bodies and raw/SQL caches excluded. Full0444 dated mode observations require restoration in a fresh clone: Git only stores executable flags, not full modes or empty directories. No new paper/DOI/tracker for these partial outcomes.\n')
    add(P/'RESEARCH_LOG.md');add(Path(__file__))
    rows=[]
    for n in sorted(names):
        b=(R/n).read_bytes();rows.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'observed_full_mode':stat.S_IMODE((R/n).stat().st_mode)})
    out=P/'checkpoints/CHECKPOINT_20261003_0135.json'
    with out.open('x')as f:json.dump({'schema':'ROOT_exact_owned_checkpoint/v1','utc':utc,'actual_pid':os.getpid(),'main_before':before,'completed_count':31,'total':180,'completion_estimate_percent':31/180*100,'owned_files':rows,'foreign_dirty_preimages_preserved':foreign,'foreign_primary_bodies_included':False,'active_families_included':False},f,indent=2);f.write('\n')
    add(out)
    subprocess.run(['git','add','-f','--',*sorted(names)],cwd=R,check=True)
    staged={n for n in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0')if n}
    assert staged.issubset(names)
    for n in staged:assert subprocess.check_output(['git','show',':'+n],cwd=R)==(R/n).read_bytes()
    for z in foreign:
        p=R/z['path'];b=p.read_bytes();assert len(b)==z['bytes'] and hashlib.sha256(b).hexdigest()==z['sha256'] and stat.S_IMODE(p.stat().st_mode)==z['full_mode']
    print(json.dumps({'status':'PASS_EXACT_OWNED_CHECKPOINT_STAGED','main_before':before,'owned_members':len(names),'staged_members':len(staged),'foreign_staged_members':0,'owned_bytes':sum(z['bytes']for z in rows),'completed_count':31,'total':180,'completion_estimate_percent':31/180*100}))
if __name__=='__main__':main()
