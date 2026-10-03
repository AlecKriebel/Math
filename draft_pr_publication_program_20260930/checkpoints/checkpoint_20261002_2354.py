"""Publish only completed PR41 and closed first-party PR42/43 audit evidence."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import stat
import subprocess

R=Path('/Users/alec/Documents/Math'); P=R/'draft_pr_publication_program_20260930'; A=P/'audits'
OWN=set(); CLOSURES=[]; FOREIGN=[]


def sha(raw): return hashlib.sha256(raw).hexdigest()
def load(p): return json.loads(p.read_bytes())
def git(*args): return subprocess.check_output(['git',*args],cwd=R)


def add(p,row=None):
    assert p.is_file() and not p.is_symlink() and all(not d.is_symlink() for d in p.parents)
    raw=p.read_bytes(); assert len(raw) <= 104857600
    if row is not None:
        assert type(row.get('bytes',row.get('size'))) is int
        assert len(raw)==row.get('bytes',row.get('size')) and sha(raw)==row['sha256']
    OWN.add(p.relative_to(R).as_posix())


def tree(p):
    for f in p.rglob('*'):
        assert not f.is_symlink()
        if f.is_file(): add(f)


def manifest(p,pin,field='files'):
    assert sha(p.read_bytes())==pin
    m=load(p)
    for row in m[field]: add(p.parent/row['path'],row)
    add(p); CLOSURES.append({'path':p.relative_to(R).as_posix(),'sha256':pin,'owned_members':len(m[field])})


def main():
    assert git('branch','--show-current').strip()==b'main'
    assert git('rev-parse','HEAD').strip()==b'85f830ba77016e6d7ef86a3ca1c93547b6f50f72'
    assert not git('diff','--cached','--name-only').strip()
    X=A/'pr41_9700035'; Y=A/'pr42_2233'; Z=A/'pr43_30004386'
    post=load(X/'ROOT_ACTUAL_POST_INSPECTION.json')
    assert post['status']=='PASS' and post['actual_post_pid']==42797 and post['completed_primary_prs']==31
    manifest(R/'unsolved_math_prioritization/attempts/9700035/MANIFEST.json','47a127d2de60ea688d58b880148ec55193cd022cbd45a7f8022681ffa63a09b5')
    manifest(X/'acceptance_preparation_family_v2/PREPARATION_MANIFEST.json','5f73ee3594751d176ed206ac521558045b0783cfa8b932af1bdde633deacd9aa')
    manifest(X/'acceptance_v2_adversary_family/FIRST_PARTY_MANIFEST.json','ebec51d9c41f63b8fadb159e93a85e51709b84dbbdbde4f2fb31b713e0018a32')
    manifest(X/'final_evidence_reconciliation/FINAL_MANIFEST.json','3a68c2625e567cf78dcbe37e22e0ebb2dbc3be359e533a0e786317d85492c6fa')
    for f in X.iterdir():
        if f.is_file(): add(f)
        elif f.name.startswith('root_') and f.name.endswith('_actual_capture'): tree(f)
    tree(X/'integration_log_preimages')
    manifest(Y/'current_preparation_family_v2/PREPARATION_MANIFEST.json','c77fbc8effa07391977ed49a161001625f81bdcf1f0e647537fdae441d0b2071')
    manifest(Y/'current_source_adversary_family/OWN_CLOSED_MANIFEST.json','6c1d15b46aeba383cb8fea883755efa27bbe9f6b9e8d46f6243d783f3997c518')
    manifest(Y/'current_v2_source_adversary_family/OWN_CLOSED_MANIFEST.json','0a0cf95dfde2893127a1fa298f6f07ad453286ec2c9598170602b45c410c1d8e')
    add(Y/'ROOT_RESEARCH_LOG.md')
    # Original PR43 and genuine ROOT evidence contain no downloaded paper body.
    for f in Z.iterdir():
        if f.is_file(): add(f)
        elif (f.name.startswith('root_') and f.name.endswith('_actual_capture')) or f.name in ['source_snapshot','original_git_commands','root_original_actual_reproduction']: tree(f)
        elif f.name.startswith('root_pr41_') and f.name.endswith('_capture'): tree(f)
    cc=Z/'compactness_source_family/OWNERSHIP_MANIFEST.json'
    assert sha(cc.read_bytes())=='9abc7c0dba6d4167201eec93608772be0bb26f31faf03e21805650e7d8ebc2b9'
    cm=load(cc)
    for row in cm['first_party_files']: add(cc.parent/row['path'],row)
    for row in cm['foreign_individually_excluded']: FOREIGN.append({'path':(cc.parent/row['path']).relative_to(R).as_posix(),**{k:row[k] for k in ['bytes','sha256']}})
    add(cc); CLOSURES.append({'path':cc.relative_to(R).as_posix(),'sha256':sha(cc.read_bytes()),'owned_members':18,'foreign_members':8})
    pp=Z/'probability_source_family/SELF_MANIFEST.json'
    assert sha(pp.read_bytes())=='de68537cda5407bf5b0c1a4dcd28de7ae51c96932d4b3af84aca389d82607e7c'
    pm=load(pp); selected=0
    for row in pm['files']:
        if row['classification']=='first_party_audit_artifact': add(pp.parent/row['path'],row); selected+=1
        else: FOREIGN.append({'path':(pp.parent/row['path']).relative_to(R).as_posix(),**{k:row[k] for k in ['bytes','sha256']}})
    assert selected==43; add(pp); CLOSURES.append({'path':pp.relative_to(R).as_posix(),'sha256':sha(pp.read_bytes()),'owned_members':43,'foreign_members':23})
    for name in ['root_checkpoint_2310_corrected_push_actual_capture','root_lossless_log_recovery_actual_capture']: tree(A/'pr39_9500008'/name)
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    note='\n'+now+' — PR41 complete100% as accepted qualified UNSOLVED partial; exact original-head MERGED85f830ba/tree1c2a1355, genuine reconciliation35045, finalization39874, mirror40915, post42797 and independent ROOTpost45426 PASS. Current547/dependencies469/accepted558+self0444 remain bound. Full31 prior states/history prefix preserved; native32targets39originalturns31primary/one preserved duplicate. Original2/5,new0/audit0, discovery0%; no paper/newDOI/tracker. Program31/180=17.2222%. PR42 two independent math families and genuine ROOT18306/18306/1263/raw149266659/all15458SQL PASS; original source guard repaired and NEW different source review0a0cf95d clean, pending genuine current freeze/whole gate. PR43 exact published JKP target independently verified by two new source families, repaired probability derivation and compactness/all-N attainability; genuine unchanged current527/historical527/oldindependent664 and whole raw/SQL PASS. Original0/5/new0/audit0; already_solved prior credited, current provenance repairs/source preparation pending. PR18/20 holds retained. Historical dated source inspections are retained observations, not assertions mutable main files remain at their old hashes after legitimate acceptance. No external human contact.\n'
    with (P/'RESEARCH_LOG.md').open('a') as f: f.write(note)
    with (X/'ROOT_RESEARCH_LOG.md').open('a') as f: f.write(note)
    for p in [P/'RESEARCH_LOG.md',P/'inventory.json',X/'ROOT_RESEARCH_LOG.md',R/'unsolved_math_prioritization/state.json',R/'unsolved_math_prioritization/history.jsonl',Path(__file__).resolve()]: add(p)
    records=[{'path':n,'bytes':len((R/n).read_bytes()),'sha256':sha((R/n).read_bytes()),'observed_worktree_mode':stat.S_IMODE((R/n).stat().st_mode)} for n in sorted(OWN)]
    out=P/'checkpoints/CHECKPOINT_20261002_2354.json'
    with out.open('x') as f:
        json.dump({'utc':now,'head_before':git('rev-parse','HEAD').decode().strip(),'completed':31,'total':180,'completion_percent':31/180*100,'closed_manifests':CLOSURES,'exact_owned_files':records,'individual_foreign_exclusions':FOREIGN,'excluded':'Active PR43 current preparation; all downloaded primary PDFs/text/renders/headers; both unrelated tracked referee logs; unchanged local105073924-byte PR41 original adversary raw log remains represented by its published byte-exact gzip/recovery qualification. Intentional empty controls are recorded by closed manifests; Git cannot represent empty directories or complete worktree permission bits.'},f,indent=2); f.write('\n')
    add(out)
    names=sorted(OWN)
    for i in range(0,len(names),100): git('add','-f','--',*names[i:i+100])
    staged=set(filter(None,git('diff','--cached','--name-only','-z').decode().split('\0')))
    assert staged <= OWN and not any(n.startswith('paper_ii_') for n in staged)
    for entry in filter(None,git('ls-files','--stage','-z').split(b'\0')):
        meta,n=entry.split(b'\t'); name=n.decode()
        if name not in staged: continue
        mode,oid,stage=meta.split(); assert stage==b'0' and mode in [b'100644',b'100755']
        raw=(R/name).read_bytes(); assert len(raw)<=104857600
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oid.decode()
    print(json.dumps({'status':'EXACT_OWNED_CHECKPOINT_STAGED','members':len(staged),'bytes':sum(len((R/n).read_bytes()) for n in staged),'completed':31,'completion_percent':31/180*100}))


if __name__=='__main__': main()
