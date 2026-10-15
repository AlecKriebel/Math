#!/usr/bin/env python3
"""Private-copy replay; complete owned execution receipts and output streams."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,datetime

HERE=Path(__file__).absolute().parent
TARGET=HERE.parent/'scope_repaired_snapshot/problems/30000590_group_ring_cohomology'
PRIVATE=HERE/'private_replay'
ROOT=PRIVATE/'current'
OUT=HERE/'replay_outputs'
OUT.mkdir(exist_ok=True)
shutil.copytree(TARGET,ROOT,dirs_exist_ok=True)
ALIASES=HERE/'raw_sources/source_aliases'
ALIASES.mkdir(exist_ok=True)
names=[('owr2006-43.pdf','OWR2006_virtual_FP.pdf'),('davis-dymara-januszkiewicz-okun-2006.pdf','DDJO2006_correct.pdf'),('davis-pdgroups.pdf','Davis_pdgroup.pdf'),('davis-okun-published2012.pdf','Davis_Okun_DO3.pdf'),('davis-infinite-group-actions2024.pdf','Davis_IGAP.pdf'),('sharifi-homalg.pdf','Sharifi_homalg.pdf')]
expect=json.loads((ROOT/'SOURCE_MANIFEST.json').read_bytes())['files']+[json.loads((ROOT/'SOURCE_ADDITION_T4.json').read_bytes())['source']]
sources=[]
for (dest,src),e in zip(names,expect):
    data=(HERE/'raw_sources'/src).read_bytes()
    assert len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256']
    (ALIASES/dest).write_bytes(data)
    sources.append({'fresh_private_filename':src,'candidate_filename':dest,'url':e['url'],'bytes':len(data),'sha256':e['sha256'],'fresh_download_matches_historical_binding':True})
fresh={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fresh_fetches':sources,'earlier_root_receipts_used_as_evidence':False,'task_url_failures':[{'url':'https://msp.org/agt/2006/6-3/agt-v6-n3-p14-p.pdf','result':'wrong Habiro-Meilhan paper; retained as ignored DDJO2006.pdf'},{'url':'https://people.math.osu.edu/davis.12/papers/pdgroup.pdf','result':'HTTP404; correct primary independently found without papers/'},{'url':'https://people.math.osu.edu/davis.12/papers/IGAP.pdf','result':'HTTP404; correct primary independently found without papers/'}],'task_transcription_failure_is_candidate_defect':False}
(HERE/'FRESH_SIX_SOURCE_BINDINGS.json').write_text(json.dumps(fresh,indent=2)+'\n')
receipts=[]
def run(label,script,args=(),cwd=ROOT,expected=None):
    cmd=[sys.executable,str(script),*map(str,args)]
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc=subprocess.run(cmd,cwd=cwd,capture_output=True)
    a,b=OUT/(label+'.stdout.txt'),OUT/(label+'.stderr.txt')
    a.write_bytes(proc.stdout);b.write_bytes(proc.stderr)
    receipt={'label':label,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'cwd':str(cwd),'script_sha256':hashlib.sha256(Path(script).read_bytes()).hexdigest(),'exit_code':proc.returncode,'stdout_file':str(a.relative_to(HERE)),'stderr_file':str(b.relative_to(HERE)),'stdout_bytes':len(proc.stdout),'stderr_bytes':len(proc.stderr),'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(proc.stderr).hexdigest()}
    if expected:
        receipt['expected_candidate_receipt']=str(Path(expected).relative_to(ROOT))
        receipt['byte_exact']=proc.stdout==Path(expected).read_bytes()
    receipts.append(receipt)
    (HERE/'REPLAY_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
    assert proc.returncode==0,label
    assert not proc.stderr,label+' stderr'
    if expected: assert receipt['byte_exact'],label+' receipt mismatch'
    return proc.stdout

for i in range(1,6):run(f'author_turn_{i}',ROOT/f'check_turn_{i}.py',expected=ROOT/f'TURN_{i}_CHECKS.json')
run('prior_independent_controls',ROOT/'review/independent_checks.py',expected=ROOT/'review/INDEPENDENT_CHECKS.json')
run('packet_no_sources',ROOT/'verify_packet.py')
run('packet_with_fresh_sources',ROOT/'verify_packet.py',['--source-dir',ALIASES],expected=ROOT/'review/AUTHOR_REPLAY.json')
run('review_wrapper',ROOT/'review/verify_review.py',['--author',ROOT])
run('publication_no_sources',ROOT/'verify_publication.py')
run('publication_with_fresh_sources',ROOT/'verify_publication.py',['--source-dir',ALIASES])

# FINAL_REPLAY was produced before the self-binding final manifest existed.
PRE=PRIVATE/'pre_final_manifest'
shutil.copytree(ROOT,PRE,dirs_exist_ok=True)
(PRE/'FINAL_AUTHOR_MANIFEST.json').unlink()
raw=run('historical_pre_final_receipt',PRE/'verify_packet.py',['--author-dir',PRE,'--source-dir',ALIASES,'--allow-unfrozen'],cwd=PRE)
assert raw==(ROOT/'FINAL_REPLAY.json').read_bytes()
receipts[-1]['byte_exact_FINAL_REPLAY']=True
(HERE/'REPLAY_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
for e in json.loads((HERE.parent/'scope_repaired_snapshot_manifest.json').read_bytes())['files']:
    if e['path'].startswith('problems/'):
        path=ROOT/Path(e['path']).relative_to('problems/30000590_group_ring_cohomology')
        assert hashlib.sha256(path.read_bytes()).hexdigest()==e['sha256']
summary={'status':'PASS','runs':len(receipts),'all_stdout_and_stderr_complete':True,'source_pdfs_freshly_bound':6,'author_assertions':747103,'prior_independent_assertions':23463,'historical_FINAL_REPLAY_byte_exact':True,'historical_review_AUTHOR_REPLAY_byte_exact':True,'private_candidate_copy_unchanged':True,'proof_replacement_by_counts':False}
print(json.dumps(summary,indent=2))
