#!/usr/bin/env python3
"""Fresh complete gate integrity/context/replay harness; writes only owned scratch.

All copied programs retain exact bytes. The fake project tree has a read-only
Git-dir link solely for immutable Git reads; no command mutates Git or canonical
data. Finite diagnostics do not prove the universal PDE theorem.
"""
from pathlib import Path
import datetime, hashlib, json, shutil, sqlite3, subprocess, sys, urllib.request

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
ROOT=HERE.parents[3]
CURRENT=AUDIT/'reviewed_candidate'
HEAD='5ac4a57e08dd72a6f16768f2288b9c0349999431'
BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
PREFIX='unsolved_math_prioritization/attempts/30004186/'
EXPECTED_MANIFEST='aa37f2c4370054b547a45ce812c02f744dba8277a1ae656a8ca5961132278344'
CTX='759ed8f6518e7a61a2356296cdc080f951f41bc93ca448182f1ce2143cda5a7b'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def dump(path,j):path.write_text(json.dumps(j,indent=2)+'\n')
def jsonfile(path):return json.loads(path.read_bytes())

def main():
    assert git('branch','--show-current').decode().strip()=='main'
    scratch=HERE/'tmp'/('replay_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
    scratch.mkdir(parents=True)
    bindings=[]
    for name,origin,m,n in [('current',CURRENT,CURRENT/'MANIFEST.json',30),('support',AUDIT,CURRENT/'CURRENT_PROOF_DEPENDENCIES.json',66)]:
        j=jsonfile(m);assert len(j['files'])==n
        if name=='current':assert sha(m.read_bytes())==EXPECTED_MANIFEST
        for row in j['files']:
            data=(origin/row['path']).read_bytes()
            assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
            bindings.append({'scope':name,**row,'verified':True})
    assert {str(x.relative_to(CURRENT)) for x in CURRENT.rglob('*') if x.is_file()}=={'MANIFEST.json'}|{x['path'] for x in jsonfile(CURRENT/'MANIFEST.json')['files']}
    protected=[CURRENT/'MANIFEST.json']+[CURRENT/r['path'] for r in jsonfile(CURRENT/'MANIFEST.json')['files']]+[AUDIT/r['path'] for r in jsonfile(CURRENT/'CURRENT_PROOF_DEPENDENCIES.json')['files']]
    before={str(p):sha(p.read_bytes()) for p in protected}
    archives={'CANDIDATE.md':'ORIGINAL_CANDIDATE.md','README.md':'ORIGINAL_README.md','SOURCE_AUDIT.md':'ORIGINAL_SOURCE_AUDIT.md','provenance.json':'ORIGINAL_provenance.json','readiness.json':'ORIGINAL_readiness.json'}
    originals=[]
    exact=scratch/'original';exact.mkdir()
    paths=git('ls-tree','-r','--name-only',HEAD,'--',PREFIX).decode().splitlines();assert len(paths)==16
    for path in paths:
        rel=path[len(PREFIX):];data=git('show',HEAD+':'+path)
        assert data==(CURRENT/archives.get(rel,rel)).read_bytes(),rel
        q=exact/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
        originals.append({'path':path,'bytes':len(data),'sha256':sha(data),'git_blob':git('rev-parse',HEAD+':'+path).decode().strip()})
    assert (CURRENT/'ORIGINAL_pr_body.md').read_text()==jsonfile(AUDIT/'pr_input/pr.json')['body']
    assert (CURRENT/'CANDIDATE.md').read_text().split('## 1.',1)[1]==(CURRENT/'ORIGINAL_CANDIDATE.md').read_text().split('## 1.',1)[1]
    assert (CURRENT/'SOURCE_AUDIT.md').read_bytes().startswith((CURRENT/'ORIGINAL_SOURCE_AUDIT.md').read_bytes())
    diff=git('diff',BASE,HEAD,'--');assert diff==(AUDIT/'pr_input/diff.patch').read_bytes()
    (scratch/'original_diff.patch').write_bytes(diff)
    changed=git('diff','--name-only',BASE,HEAD).decode().splitlines();assert len(changed)==17
    dump(HERE/'INPUT_INTEGRITY.json',{'utc':now(),'current_bound_members':30,'current_physical_files_including_self_excluding_manifest':31,'support_files':66,'bindings':bindings,'originals':originals,'six_archives_exact':True,'candidate_sections_1_onward_unchanged':True,'diff_sha256':sha(diff),'changed_paths':changed,'before_hashes':before})

    fake=scratch/'Math';fake.mkdir()
    (fake/'.git').write_text('gitdir: '+str(ROOT/'.git')+'\n')
    fa=fake/'draft_pr_publication_program_20260930/audits/pr29_30004186';fa.mkdir(parents=True)
    shutil.copytree(exact,fa/'source_snapshot')
    shutil.copyfile(AUDIT/'snapshot_manifest.json',fa/'snapshot_manifest.json')
    shutil.copytree(AUDIT/'pr_input',fa/'pr_input')
    for fam in ['existence_family','instability_family','primary_scope_family']:
        dest=fa/fam;dest.mkdir()
        for row in jsonfile(CURRENT/'CURRENT_PROOF_DEPENDENCIES.json')['files']:
            if row['path'].startswith(fam+'/'):
                rel=row['path'][len(fam)+1:];q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(AUDIT/row['path'],q)
        assert sha((dest/'MANIFEST.json').read_bytes())==sha((AUDIT/fam/'MANIFEST.json').read_bytes())
    uq=fake/'unsolved_math_prioritization';uq.mkdir()
    for name in ['cache','manifest.json']:(uq/name).symlink_to(ROOT/'unsolved_math_prioritization'/name,target_is_directory=(name=='cache'))
    runs=[]
    jobs=[(exact/'check_identities.py',CURRENT/'check_results.json',20,[]),
          (exact/'independent_review/independent_checks.py',CURRENT/'independent_review/independent_results.json',135,[]),
          (exact/'independent_review/submitted_check_identities.py',CURRENT/'independent_review/submitted_results.json',20,[]),
          (fa/'existence_family/existence_controls.py',AUDIT/'existence_family/CONTROL_RESULTS.json',55,[]),
          (fa/'instability_family/adversarial_checks.py',AUDIT/'instability_family/adversarial_results.json',66,[]),
          (fa/'primary_scope_family/independent_source_controls.py',AUDIT/'primary_scope_family/INDEPENDENT_CONTROLS_RESULTS.json',16,['--no-write'])]
    for i,(script,receipt,count,flags) in enumerate(jobs):
        initial=sha(script.read_bytes());run=subprocess.run(['/usr/bin/python3',str(script),*flags],cwd=fake,capture_output=True,timeout=60)
        (scratch/('run_%s.stdout.json'%i)).write_bytes(run.stdout);(scratch/('run_%s.stderr.txt'%i)).write_bytes(run.stderr)
        assert run.returncode==0,(script,run.stderr)
        assert sha(script.read_bytes())==initial
        # Existence controls intentionally omit evidence from stdout, but write
        # the complete receipt beside the isolated copied script.
        got=jsonfile(script.with_name('CONTROL_RESULTS.json')) if i==3 else json.loads(run.stdout)
        wanted=jsonfile(receipt)
        changes=[k for k in set(got)|set(wanted) if got.get(k)!=wanted.get(k)]
        assert set(changes)<=({'utc'} if i>=3 else set()),(script,changes)
        assert got.get('assertions',got.get('passed',got.get('check_count')))==count
        if i<3:assert run.stdout==receipt.read_bytes()
        runs.append({'script':str(script.relative_to(scratch)),'sha256':initial,'returncode':0,'count':count,'actual_changed_fields':changes,'all_other_fields_exact':True,'stdout_sha256':sha(run.stdout),'stderr_sha256':sha(run.stderr)})
    # Run actual retained read-only reproducer before any receipt-regenerating
    # validation harness touches its copied closed inputs.
    read_only=fa/'primary_scope_family/reproduce.py'
    repro=subprocess.run(['/usr/bin/python3',str(read_only)],cwd=fake,capture_output=True,timeout=60)
    (scratch/'read_only_reproducer.stdout.json').write_bytes(repro.stdout);(scratch/'read_only_reproducer.stderr.txt').write_bytes(repro.stderr)
    assert repro.returncode==0,repro.stderr
    reproduced=json.loads(repro.stdout)
    assert reproduced['fresh_controls']==16 and reproduced['rejected_mutants']==12
    # Independently reproduce read-only Git/full-diff and isolated legacy harnesses.
    for name in ['validate_original.py','replay_legacy.py']:
        script=fa/'existence_family'/name
        r=subprocess.run(['/usr/bin/python3',str(script)],cwd=fake,capture_output=True,timeout=60)
        (scratch/(name+'.stdout.json')).write_bytes(r.stdout);(scratch/(name+'.stderr.txt')).write_bytes(r.stderr)
        assert r.returncode==0,r.stderr
    assert before=={str(p):sha(p.read_bytes()) for p in protected}
    dump(HERE/'REPLAY_RECEIPT.json',{'utc':now(),'status':'PASS','isolated_tree':str(scratch.relative_to(HERE)),'runs':runs,'primary_readonly_reproducer':reproduced,'actual_validation_harnesses_passed':True,'closed_input_before_after_equal':True,'excluded_fields_only_if_actual_changed':'utc on timestamped family controls; original outputs byte exact','scope':'Unchanged copied programs and diagnostic receipts only; universal PDE proof is written reconstruction.'})

    cache=ROOT/'unsolved_math_prioritization/cache';manifest=jsonfile(ROOT/'unsolved_math_prioritization/manifest.json')
    url='https://huggingface.co/api/datasets/ulamai/UnsolvedMath/tree/37e53eabe540fb458758e198be61634bd02ee008'
    raw=urllib.request.urlopen(url).read();(scratch/'fresh_upstream_tree.json').write_bytes(raw);tree={x['path']:x for x in json.loads(raw)}
    rawfiles={}
    for name in ['problems.json','research_results.json']:
        data=(cache/name).read_bytes();expected=manifest['files'][name]
        assert sha(data)==expected['sha256']==tree[name]['lfs']['oid'];assert len(data)==expected['bytes']==tree[name]['size']
        rawfiles[name]={'bytes':len(data),'sha256':sha(data)}
    problems=jsonfile(cache/'problems.json');reports=jsonfile(cache/'research_results.json')
    hits=[x for x in problems if x['id']==30004186];assert len(hits)==1 and sum(x['problem_number']=='OWR-17128-002' for x in problems)==1
    source=hits[0];assert source==jsonfile(CURRENT/'source_record.json');assert 'OWR-17128-002' not in reports
    actual=sha(json.dumps([source,{}],sort_keys=True).encode());assert actual==CTX
    null=sha(json.dumps([source,None],sort_keys=True).encode());assert null!=CTX
    db=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro',uri=True)
    row=db.execute('SELECT payload,typeof(report),report FROM records WHERE key=?',('30004186',)).fetchone();db.close()
    assert json.loads(row[0])==source and row[1:] == ('text','{}')
    state=jsonfile(ROOT/'unsolved_math_prioritization/state.json');assert '30004186' not in state
    queue=(ROOT/'unsolved_math_prioritization/QUEUE.md').read_text();rows=[x for x in queue.splitlines() if '30004186 / OWR-17128-002' in x];assert len(rows)==1 and '| queued | 0/5 |' in rows[0]
    history={}
    for name in ['history.jsonl','assessment_history.jsonl']:
        f=ROOT/'unsolved_math_prioritization'/name
        history[name]=[x for x in f.read_text().splitlines() if '30004186' in x] if f.exists() else []
        assert not history[name]
    basepaths=git('ls-tree','-r','--name-only',BASE,'--',PREFIX).decode();assert not basepaths
    ledger=jsonfile(CURRENT/'turns.json');assert ledger['used']==1 and ledger['limit']==5 and len(ledger['turns'])==1 and ledger['original_target_outcome']=='partial'
    dump(HERE/'SOURCE_CONTEXT_RECEIPT.json',{'utc':now(),'upstream_tree_url':url,'fresh_tree_sha256':sha(raw),'raw_files':rawfiles,'unique_id_code':True,'source_equal_curated_record':True,'prior_key_present':False,'prior_fallback':{},'SQL_report_type':row[1],'SQL_report_value':row[2],'context_sha256':actual,'null_mutant_context_sha256':null,'base_attempt_absent':True,'current_target_state_absent':True,'current_queue_row':rows[0],'current_histories':history,'original_turns':ledger,'new_substantive_attempts':0,'limits':'Bounded exact objects/current state, not global absence, historical model/query telemetry, novelty, or future acceptance.'})
    print(json.dumps({'status':'PASS','current_bound_members':30,'physical_current_files':31,'bound_support':66,'original16_diff17':True,'six_archives':True,'runs':[x['count'] for x in runs],'context':actual,'closed_inputs_unchanged':True},indent=2))

if __name__=='__main__':main()
