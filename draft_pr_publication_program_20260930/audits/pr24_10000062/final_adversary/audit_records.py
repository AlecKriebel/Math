#!/usr/bin/env python3
"""Read-only record/integrity audit and isolated historical/family replays."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,subprocess,shutil,sqlite3,re

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
REPO=AUDIT.parents[2]
HEAD='6b702110d1bd4b9220e2033fa5eed030911ce8c6'
BASE='01358d66fc67d1c462bddf31c0d4ee5b120e6737'
TARGET='unsolved_math_prioritization/attempts/10000062/'

def digest(b):return sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def write(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')

def main():
    assert git('branch','--show-current').decode().strip()=='main'
    snap=json.loads((AUDIT/'snapshot_manifest.json').read_text())
    frozen=[]
    for row in snap['files']:
        path=row['path']; b=(AUDIT/'source_snapshot'/path).read_bytes(); original=git('show',HEAD+':'+TARGET+path)
        ok=len(b)==row['bytes'] and digest(b)==row['sha256'] and b==original
        assert ok,path
        frozen.append({'path':path,'bytes':len(b),'sha256':digest(b),'exact_head_match':True})
    current_manifest=AUDIT/'reviewed_candidate/MANIFEST.json'
    assert digest(current_manifest.read_bytes())=='725be2b346d5d38d711f9a0a3d8bd35f32424be349a55b5e6593da20a07433d7'
    current=[]
    for row in json.loads(current_manifest.read_text())['files']:
        b=(AUDIT/'reviewed_candidate'/row['path']).read_bytes()
        assert len(b)==row['bytes'] and digest(b)==row['sha256'],row['path']
        current.append({'path':row['path'],'bytes':len(b),'sha256':digest(b),'match':True})
    original=(AUDIT/'source_snapshot/CANDIDATE.md').read_bytes()
    updated=(AUDIT/'reviewed_candidate/CANDIDATE.md').read_bytes()
    assert original[original.index(b'## 1.'):]==updated[updated.index(b'## 1.'):]
    for name in ['CANDIDATE.md','README.md','readiness.json','status.json']:
        assert (AUDIT/'reviewed_candidate'/('ORIGINAL_'+name)).read_bytes()==(AUDIT/'source_snapshot'/name).read_bytes()
    families=[]
    for family in ['metric_ball_family','symmetry_family','primary_scope_family']:
        m=AUDIT/family/'MANIFEST.json'; rows=json.loads(m.read_text())['files']; checked=[]
        for row in rows:
            b=(m.parent/row['path']).read_bytes()
            assert len(b)==row['bytes'] and digest(b)==row['sha256'],(family,row['path'])
            checked.append({'path':row['path'],'bytes':len(b),'sha256':digest(b)})
        families.append({'family':family,'manifest_sha256':digest(m.read_bytes()),'checked':checked})
    seals=[('metric_ball_family','SEALED_CRITERION.md','seal.json','criterion_sha256'),
           ('symmetry_family','INDEPENDENT_RECONSTRUCTION.md','SEAL.json','reconstruction_sha256'),
           ('primary_scope_family','SEALED_CRITERION.md','criterion_seal.json','sha256')]
    for family,file,seal,key in seals:
        assert digest((AUDIT/family/file).read_bytes())==json.loads((AUDIT/family/seal).read_text())[key]
    assert digest((HERE/'EARLY_CRITERIA_AND_RECONSTRUCTION.md').read_bytes())==json.loads((HERE/'EARLY_SEAL.json').read_text())['sha256']['EARLY_CRITERIA_AND_RECONSTRUCTION.md']
    pr=json.loads(subprocess.check_output(['gh','pr','view','24','--repo','AlecKriebel/Math','--json','headRefOid,baseRefOid,state,isDraft,title,body,url'],cwd=REPO))
    assert pr['headRefOid']==HEAD
    assert pr['body']==(AUDIT/'current_pr_body.md').read_text()
    paths=git('diff','--name-only',BASE+'...'+HEAD).decode().splitlines()
    assert paths==snap['changed_paths']
    queue_diff=git('diff',BASE,HEAD,'--','unsolved_math_prioritization/QUEUE.md').decode()
    queue_lines=[x for x in queue_diff.splitlines() if x.startswith(('+','-')) and not x.startswith(('+++','---'))]
    assert len(queue_lines)==2 and all('10000062 / AMR-099-0062' in x for x in queue_lines)
    current_queue=[x for x in (REPO/'unsolved_math_prioritization/QUEUE.md').read_text().splitlines() if '10000062 / AMR-099-0062' in x]
    write('INTEGRITY_AND_HEAD_RECEIPT.json',{'utc':datetime.now(timezone.utc).isoformat(),'head':HEAD,'actual_merge_base':BASE,
        'snapshot_manifest_sha256':digest((AUDIT/'snapshot_manifest.json').read_bytes()),'frozen':frozen,
        'current_manifest_sha256':digest(current_manifest.read_bytes()),'current':current,'science_sections_unchanged':True,
        'original_archives_exact':True,'family_manifest_checks':families,'all_seals_valid':True,
        'live_pr':pr,'live_pr_body_current_exact':True,'diff_paths':paths,'selected_queue_diff':queue_lines,'current_main_queue_row':current_queue,
        'post_integration_mirror':'Parent-owned future action, not asserted historically performed.'})

    cache=REPO/'unsolved_math_prioritization/cache'; manifest=json.loads((REPO/'unsolved_math_prioritization/manifest.json').read_text())
    corpus=[]
    for name in ['problems.json','research_results.json']:
        b=(cache/name).read_bytes(); recorded=manifest['files'][name]
        assert len(b)==recorded['bytes'] and digest(b)==recorded['sha256']
        corpus.append({'name':name,'bytes':len(b),'sha256':digest(b)})
    problems=json.loads((cache/'problems.json').read_text()); reports=json.loads((cache/'research_results.json').read_text())
    record=json.loads((AUDIT/'reviewed_candidate/input_record.json').read_text())
    target=[p for p in problems if p['id']==10000062]; codes=[p for p in problems if p['problem_number']=='AMR-099-0062']
    assert len(target)==len(codes)==1
    assert all(record['problem'][key]==value for key,value in target[0].items())
    assert reports['AMR-099-0062']==record['prior_report']
    normalize=lambda s:re.sub(r'\s+',' ',s.strip()).casefold()
    equivalent=[p['id'] for p in problems if normalize(p['statement'])==normalize(target[0]['statement'])]
    assert equivalent==[10000062]
    con=sqlite3.connect('file:'+str((cache/'catalog.sqlite').resolve())+'?mode=ro',uri=True)
    assert con.execute('SELECT revision FROM metadata').fetchone()[0]==record['source_revision']
    payload,report=con.execute('SELECT payload,report FROM records WHERE key=?',('10000062',)).fetchone()
    assert json.loads(payload)==target[0] and json.loads(report)==record['prior_report']
    related=REPO/'unsolved_math_prioritization/review_v2/related_target_groups.json'
    mentions='10000062' in related.read_text() or 'AMR-099-0062' in related.read_text()
    ledger=[json.loads(x) for x in (AUDIT/'reviewed_candidate/turns.jsonl').read_text().splitlines() if x]
    status=json.loads((AUDIT/'reviewed_candidate/status.json').read_text())
    assert len(ledger)==1 and ledger[0]['turn']==status['turns_used']==1 and status['turn_limit']==5
    assert status['full_source_solved'] is False and status['new_discovery_claim'] is False
    write('CORPUS_AND_BUDGET_RECEIPT.json',{'utc':datetime.now(timezone.utc).isoformat(),'revision':record['source_revision'],
        'corpus':corpus,'problem_count':len(problems),'report_count':len(reports),'literal_id_matches':len(target),
        'literal_code_matches':len(codes),'complete_target_payload_match':True,'complete_prior_report_match':True,
        'sqlite_revision_payload_report_match':True,'normalized_statement_matches':equivalent,'related_group_mentions':mentions,
        'related_group_sha256':digest(related.read_bytes()),'ledger':ledger,'budget':{'turns_used':1,'turn_limit':5,'validation_new_attempts':0},
        'archival_model_limit':'Labels are preserved attribution, not independently recoverable model execution attestations.',
        'canonical_history_limit':'Original QUEUE edit was handwritten; future accepted-state mirror may record present acceptance only, without inventing prior transitions.'})

    scripts=[('source_snapshot/verify.py',['verification.json']),('source_snapshot/review/submitted_verify.py',['verification.json']),
        ('source_snapshot/review/independent_checks.py',['independent_results.json']),
        ('metric_ball_family/full_cell_checks.py',['full_cell_results.json','canonical_cell_certificate.json']),
        ('symmetry_family/exact_checks.py',['EXACT_RESULTS.json']),('primary_scope_family/new_controls.py',['new_control_results.json'])]
    replay=[]
    for index,(path,outputs) in enumerate(scripts):
        src=AUDIT/path; run=HERE/'tmp/runs'/str(index);run.mkdir(parents=True,exist_ok=True)
        dst=run/src.name;shutil.copy2(src,dst)
        proc=subprocess.run(['/usr/bin/python3',str(dst)],cwd=run,capture_output=True,text=True,timeout=300)
        (run/'stdout.txt').write_text(proc.stdout);(run/'stderr.txt').write_text(proc.stderr)
        assert proc.returncode==0,(path,proc.stdout,proc.stderr)
        result=[]
        for output in outputs:
            generated=(run/output).read_bytes();saved=(src.parent/output).read_bytes()
            identical=generated==saved
            old=json.loads(saved);new=json.loads(generated)
            if 'at_utc' in new:old.pop('at_utc',None);new.pop('at_utc',None)
            assert old==new,(path,output)
            result.append({'file':output,'generated_sha256':digest(generated),'saved_sha256':digest(saved),
                           'byte_identical':identical,'mathematical_fields_identical':True,'only_ignored_field':'at_utc' if not identical else None})
        replay.append({'script':path,'script_sha256':digest(src.read_bytes()),'exit_code':proc.returncode,'outputs':result,
                       'stdout':proc.stdout,'stderr':proc.stderr})
        print('reproduced',path,flush=True)
    write('REPRODUCTION_RECEIPT.json',{'utc':datetime.now(timezone.utc).isoformat(),'runtime':'/usr/bin/python3 standard library',
                                     'isolated_ignored_runs':True,'replays':replay,'status':'PASS'})

if __name__=='__main__':main()
