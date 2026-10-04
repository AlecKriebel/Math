"""Prepared PR329 merge/publication guards; importing does not create clearance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess, zipfile

A=Path(__file__).resolve().parent; P=A.parents[1]; R=P.parent
O=R/'problems/20000450_pentagonal_torsion/preprint'
QUEUE='unsolved_math_prioritization/QUEUE.md'
PREFIX='unsolved_math_prioritization/attempts/20000450/'
ORIGINAL_HEAD='96395a4f506af6a6045e3cd59afcba2db6b7e2e7'
BRANCH='math/20000450-pentagonal-torsion-reviewed'
FORMAL=('pentagonal-torsion-note.tex','pentagonal-torsion-note.pdf',
        'pentagonal-torsion-verification.zip','zenodo-deposit.json')
RELEASE='problems/20000450_pentagonal_torsion/PREPRINT_RELEASE.md'
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def pin(p):
    assert p.is_file() and not p.is_symlink(),p
    b=p.read_bytes()
    return dict(bytes=len(b),sha256=sha(b),mode=f'{stat.S_IMODE(p.stat().st_mode):04o}')
def inventory(d,excluded_roots=()):
    files={};dirs={'.':f'{stat.S_IMODE(d.stat().st_mode):04o}'}
    for p in sorted(d.rglob('*')):
        rel=str(p.relative_to(d))
        if any(rel==n or rel.startswith(n+'/') for n in excluded_roots):continue
        assert not p.is_symlink(),p
        n=rel
        if p.is_file():files[n]=pin(p)
        else:
            assert p.is_dir(),p
            dirs[n]=f'{stat.S_IMODE(p.stat().st_mode):04o}'
    return dict(payloads=files,directory_modes=dirs)
def window():
    assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']

class Capture:
    def __init__(self,purpose):
        self.directory=A/'root_integration_private'/(purpose+'_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
        self.directory.mkdir(parents=True,exist_ok=False);self.entries=[]
    def run(self,label,argv,input=None,ok=(0,),cwd=R):
        argv=[str(x) for x in argv];assert not (self.directory/(label+'.json')).exists()
        start=utc();prep=dict(utc=start,argv=argv,cwd=str(cwd),
            program_pins={x:pin(Path(x)) for x in argv if x.endswith('.py') and Path(x).is_file()})
        (self.directory/(label+'.preexecution.json')).write_text(json.dumps(prep,indent=2)+'\n')
        run=subprocess.run(argv,cwd=cwd,input=input,capture_output=True,
            env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1',PYTHONDONTWRITEBYTECODE='1'))
        streams={}
        for name,b in [('stdout',run.stdout),('stderr',run.stderr)]:
            p=self.directory/(label+'.'+name);p.write_bytes(b);streams[name]=dict(path=str(p),**pin(p))
        rec=dict(**prep,ended_utc=utc(),exit_code=run.returncode,streams=streams)
        self.entries.append(rec);(self.directory/(label+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
        assert run.returncode in ok,(label,run.returncode,run.stderr.decode(errors='replace'))
        return run
    def git(self,*args,input=None,ok=(0,)):
        return self.run('git_'+str(len(self.entries)),['git',*args],input=input,ok=ok).stdout

def current_clearance():
    # This file may be written only after the root actually reads, challenges,
    # reproduces and closes a clean new whole-preprint review of the repair.
    c=load(A/'PUBLISHING_CLEARANCE.json')
    assert c['status']=='READY_AFTER_GLOBAL_REPAIR_AND_NEW_FULL_PREPRINT_REVIEW'
    assert c['original_head']==ORIGINAL_HEAD and c['original_status']=='claimed_solved'
    assert c['final_clean_review']>=2 and c['unresolved_findings']==0
    assert c['historical_review01_finding_retained'] and c['first_priority_certified'] is False
    assert set(c['formal_submission_files'])==set(FORMAL)
    assert {n:pin(O/n) for n in FORMAL}==c['formal_submission_files']
    for n,e in c['immutable_root_artifact_pins'].items():assert pin(A/n)==e,n
    final=load(A/c['final_review_closure'])
    assert final['status']=='PASS_ROOT_EXTERNALLY_CLOSED_CLEAN_FULL_PREPRINT_REVIEW'
    assert final['unresolved_findings']==0 and final['early_stages_externally_verified']
    assert final['complete_independent_outputs_compared'] and final['held_namespace_unchanged']
    assert final['qualified_candidate']==c['qualified_candidate']
    q=load(A/'preprint'/('qualification_'+c['qualified_candidate'])/'QUALIFICATION.json')
    assert q['status']=='NATIVELY_QUALIFIED_FOR_FRESH_ADVERSARIAL_REVIEW'
    assert q['input_count']==8 and q['source_pdf_pair_bound'] and q['all_archive_members_bytes_and_modes_equal']
    mapping=dict(zip(FORMAL,['manuscript.tex','manuscript.pdf','verification.zip','zenodo-deposit.json']))
    for n,qn in mapping.items():
        assert pin(O/n)=={k:q['inputs'][qn][k] for k in ['bytes','sha256','mode']}
    closed=load(A/'ROOT_FINAL_CLOSED_EVIDENCE.json')
    assert closed['status']=='ALL_CURRENT_SCIENTIFIC_AND_REVIEW_NAMESPACES_EXTERNALLY_BOUND'
    for n,e in closed['namespaces'].items():
        # Only the preexisting third-party interpreter is outside the geometry
        # scientific namespace. No mathematical or review artifact is excluded.
        exclusions=e['excluded_roots']
        assert exclusions==(['.runtime'] if n=='geometry' else []),n
        assert inventory(A/n,exclusions)==e['inventory'],n
    for n,e in closed['external_files'].items():assert pin(Path(n))==e,n
    original=load(A/'snapshot_manifest.json')
    assert original['head']==ORIGINAL_HEAD and len(original['files'])==22
    for e in original['files']:
        p=A/'snapshot'/e['path'];b=p.read_bytes()
        assert len(b)==e['bytes'] and sha(b)==e['sha256']
    return c

def queue_binding(cap,base,tree):
    old=cap.git('show',base+':'+QUEUE).splitlines(keepends=True)
    new=cap.git('show',tree+':'+QUEUE).splitlines(keepends=True)
    assert len(old)==len(new)
    changed=[i for i,(a,b) in enumerate(zip(old,new)) if a!=b];assert len(changed)==1,changed
    i=changed[0];a=old[i].split(b'|');b=new[i].split(b'|');assert len(a)==len(b)
    assert a[2].strip().split(b' / ')[0]==b'20000450'
    assert [a[j].strip() for j in (8,9)]==[b'queued',b'0/5']
    assert [b[j].strip() for j in (8,9)]==[b'claimed_solved',b'1/5']
    assert [j for j,(x,y) in enumerate(zip(a,b)) if x!=y]==[8,9,11]
    r=load(A/'queue_repair_receipt.json')
    assert old[i].decode()==r['old_row'] and new[i].decode()==r['new_row']
    return dict(queue_physical_line=i+1,queue_only_pipe_cells=[8,9,11],
        all_other_queue_bytes_equal=True,base_row=old[i].decode(),accepted_row=new[i].decode())

def tree_binding(cap,base,tree):
    c=current_clearance();m=load(A/'repaired_snapshot_manifest.json')
    original=load(A/'snapshot_manifest.json');assert original['head']==ORIGINAL_HEAD and len(original['files'])==22
    expected={e['path'] for e in original['files']}|{RELEASE}
    assert len(expected)==23 and {e['path'] for e in m['files']}==expected
    assert set(cap.git('diff','--name-only',base,tree).decode().splitlines())==expected
    for e in m['files']:
        body=cap.git('show',tree+':'+e['path']);assert len(body)==e['bytes'] and sha(body)==e['sha256']
        assert cap.git('ls-tree',tree,'--',e['path']).split(b'\t',1)[0].split()==[b'100644',b'blob',e['git_blob_sha'].encode()]
    for e in original['files']:
        if e['path']==QUEUE:continue
        body=cap.git('show',tree+':'+e['path']);assert len(body)==e['bytes'] and sha(body)==e['sha256']
    for n,e in c['formal_submission_files'].items():
        p=str((O/n).relative_to(R));body=cap.git('show',tree+':'+p)
        assert len(body)==e['bytes'] and sha(body)==e['sha256']
        assert cap.git('show',base+':'+p)==body
    return dict(all_expected_changed_paths_exact=23,original_attempt_files_unchanged=21,
        four_preexisting_formal_submission_files_exact=True,**queue_binding(cap,base,tree))

def fresh_package_integrity(cap):
    c=current_clearance();B=A/'preprint'/('verification_'+c['qualified_candidate'])
    X=cap.directory/'fresh_package';X.mkdir()
    with zipfile.ZipFile(O/'pentagonal-torsion-verification.zip') as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==54
        for i in z.infolist():
            p=Path(i.filename);assert not p.is_absolute() and '..' not in p.parts
            q=X/p
            if i.is_dir():assert i.external_attr>>16==stat.S_IFDIR|0o755;q.mkdir(parents=True,exist_ok=True);q.chmod(0o755)
            else:
                assert i.external_attr>>16==stat.S_IFREG|0o644
                q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(z.read(i));q.chmod(0o644)
    before=inventory(X);assert before==inventory(B)
    interpreter='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
    run=cap.run('fresh_arithmetic_integrity',[interpreter,'-B',X/'verify.py','--suite','arithmetic'])
    result=json.loads(run.stdout)
    assert not run.stderr and result['status']=='PASS' and result['positive_programs']==2
    assert result['negative_mutants']==4 and result['all_bodies_modes_inventory_unchanged']
    prior=load(A/'preprint'/('qualification_'+c['qualified_candidate'])/'QUALIFICATION.json')
    old=prior['actual_native_replays']['preprint_archive_arithmetic_bundled_'+c['qualified_candidate']]['complete_result']
    assert len(result['results'])==len(old['results'])==6
    for key in ['suite','payload_files','positive_programs','negative_mutants','manifest_sha256','scope']:
        assert result[key]==old[key],key
    for x,y in zip(result['results'],old['results']):
        for key in ['program','actual_exit','stdout_bytes','stdout_sha256','stderr_bytes','complete_mathematical_output_equal','mutant']:
            assert x[key]==y[key],key
    assert inventory(X)==before;current_clearance()
    return dict(fresh_archive_bytes_modes_equal=True,fresh_arithmetic_outputs_exact=True,
        full_symbolic_outputs_bound_by_current_qualification_and_clean_review=True)
