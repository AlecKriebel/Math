#!/usr/bin/env python3
"""Read-only PR37 audit; executions and downloaded/source copies stay ignored.

Run with /usr/bin/python3 from any cwd. --fetch independently retrieves cited
sources; default replays frozen originals, corruption controls, corpus joins,
native queue.score, and Git provenance. No CLI queue command is generated.
"""
import argparse, collections, datetime, hashlib, importlib.util, json, os
from pathlib import Path
import re, shutil, sqlite3, subprocess, sys, urllib.request

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SNAP = HERE.parent / 'source_snapshot'
TMP = HERE / 'ignoredtmp'
HEAD = '84bb43d21b36e4d97229806e2518fbc135bee786'
BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
PYTHON = '/usr/bin/python3'
sys.dont_write_bytecode = True
LEDGER = []

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def record(path):
    b = path.read_bytes()
    return {'path': str(path.relative_to(REPO)), 'bytes': len(b), 'sha256': sha(b)}
def read(path):
    d = record(path); d['read_at_utc'] = utc(); LEDGER.append({'kind':'full_file_read', **d})
    return json.loads(path.read_text())
def write(name, obj): (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
def command(argv, cwd=None):
    start = utc()
    r = subprocess.run(argv, cwd=cwd or REPO, capture_output=True, timeout=180)
    item={'kind':'execution', 'argv':argv, 'cwd':str(cwd or REPO), 'start_utc':start,
          'end_utc':utc(), 'returncode':r.returncode, 'stdout_sha256':sha(r.stdout),
          'stderr_sha256':sha(r.stderr), 'stdout_bytes':len(r.stdout), 'stderr_bytes':len(r.stderr)}
    LEDGER.append(item)
    return r
def git(*args):
    r = command(['git', *args])
    if r.returncode: raise RuntimeError(r.stderr.decode())
    return r.stdout
def tree(ref):
    rows=[]
    for row in git('ls-tree','-r','-z',ref,'--','unsolved_math_prioritization/attempts/3009').split(b'\0'):
        if row:
            left,p=row.decode().split('\t'); mode,kind,blob=left.split()
            rows.append({'mode':mode,'kind':kind,'blob':blob,'path':p})
    return rows

def fetch_sources():
    requests = [
      ('k3.pdf','https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf'),
      ('kp_v3.pdf','https://arxiv.org/pdf/math/0303258v3'),
      ('boronski_v1.pdf','https://arxiv.org/pdf/1510.06663v1'),
      ('pardon.pdf','https://arxiv.org/pdf/1112.2324'),
      ('kp_metadata.html','https://arxiv.org/abs/math/0303258'),
      ('boronski_metadata.html','https://arxiv.org/abs/1510.06663'),
      ('brown_doi.html','https://doi.org/10.2307/2041926'),
      ('dress_doi.html','https://doi.org/10.1016/0040-9383(69)90010-X'),
      ('requested_problem.html','https://www.unsolvedmath.com/problems/3009'),
    ]
    rows=[]; out=TMP/'sources'; out.mkdir(parents=True,exist_ok=True)
    for name,url in requests:
        row={'url':url,'started_utc':utc()}
        try:
            with urllib.request.urlopen(url,timeout=45) as response:
                data=response.read(); row.update(final_url=response.url,status=response.status,
                    content_type=response.headers.get('Content-Type'),bytes=len(data),sha256=sha(data))
            (out/name).write_bytes(data)
            if name.endswith('.pdf'):
                r=command(['pdftotext','-layout',str(out/name),str(out/(name+'.txt'))])
                row['text_extraction_returncode']=r.returncode
        except Exception as e: row['retrieval_failure']=repr(e)
        row['ended_utc']=utc(); rows.append(row)
    write('SOURCE_RETRIEVALS.json',rows)

def corpus():
    qroot=REPO/'unsolved_math_prioritization'
    manifest=read(qroot/'manifest.json')
    problems=read(qroot/'cache/problems.json')
    reports=read(qroot/'cache/research_results.json')
    p=[x for x in problems if str(x['id'])=='3009']
    assert len(p)==1
    p=p[0]; frozen=read(SNAP/'source_record.json')
    code=p['problem_number']; joins=[x['id'] for x in problems if x['problem_number']==code]
    present=code in reports
    # This importer default is explicitly distinguished from a report entry.
    importer_report=reports[code] if present and len(joins)==1 else {}
    spec=importlib.util.spec_from_file_location('native_queue',qroot/'queue.py')
    queue=importlib.util.module_from_spec(spec); spec.loader.exec_module(queue)
    policy=read(qroot/'policy.json'); native=queue.score(p,importer_report,policy)
    source_review_hash=queue.digest(json.dumps([p,importer_report],sort_keys=True))
    catalog=read(qroot/'catalog.json'); assessments=read(qroot/'assessments.json'); state=read(qroot/'state.json')
    related=read(qroot/'review_v2/related_target_groups.json')
    normalized=lambda x: re.sub(r'\s+',' ',x.get('statement','')).strip()
    duplicates=[{'id':x['id'],'problem_number':x['problem_number']} for x in problems
                if normalized(x)==normalized(p)]
    dbfile=qroot/'cache/catalog.sqlite'
    db=sqlite3.connect('file:'+str(dbfile)+'?mode=ro',uri=True)
    sql={'file':record(dbfile),'metadata_rows':db.execute('SELECT * FROM metadata').fetchall(),
         'count':db.execute('SELECT count(*) FROM records').fetchone()[0],
         'schema':db.execute("SELECT name,sql FROM sqlite_master WHERE type='table'").fetchall()}
    rows=db.execute('SELECT key,payload,report FROM records WHERE key=?',('3009',)).fetchall()
    sql['target_rows']=[{'key':key,'payload_sha256':sha(payload.encode()),'report_sha256':sha(rep.encode()),
       'payload_semantic_equal_raw':json.loads(payload)==p,'report_json':json.loads(rep),
       'payload_byte_equal_native_json_dumps':payload==json.dumps(p)} for key,payload,rep in rows]
    db.close()
    raw_checks={name:{**record(qroot/'cache'/name),
        'manifest_match':record(qroot/'cache'/name)['sha256']==v['sha256'] and record(qroot/'cache'/name)['bytes']==v['bytes']}
        for name,v in manifest['files'].items()}
    data={'at_utc':utc(),'manifest':manifest,'raw_checks':raw_checks,'problem_count':len(problems),
      'report_key_count':len(reports),'unique_numeric_id_count':len(set(str(x['id']) for x in problems)),
      'id_matches':1,'problem_number_matches':joins,'exact_join_key':code,'separate_report_key_present':present,
      'report_absence_qualification':'{} is the native importer fallback, not a separate raw research-results entry.',
      'frozen_semantic_equal_raw':frozen==p,
      'frozen_whole_file':record(SNAP/'source_record.json'),
      'frozen_byte_equal_default_indent2_serialization':(SNAP/'source_record.json').read_bytes()==(json.dumps(p,indent=2)+'\n').encode(),
      'native_queue_score':native,'native_review_hash':source_review_hash,
      'catalog_entry':[x for x in catalog if str(x['id'])=='3009'],
      'assessment_entry':assessments.get('3009'),'state_entry_present':'3009' in state,
      'state_entry':state.get('3009'),'related_groups_matching_literal_id_or_code':[],
      'full_related_groups_sha256':sha(json.dumps(related,sort_keys=True).encode()),
      'normalized_statement_duplicates':duplicates,'sql':sql}
    data['semantic_related_raw_candidates']=[{'id':x['id'],'problem_number':x['problem_number'],
       'title':x.get('title'),'statement_sha256':sha((x.get('statement') or '').encode())}
       for x in problems if re.search(r'doubly.small|hilbert.{0,2}smith|recurrent homeomorphism',
                                      (x.get('title') or '')+' '+(x.get('statement') or ''),re.I)]
    # Record exact matching substructures without claiming string search establishes semantic independence.
    groups=related if isinstance(related,list) else related.get('groups',related)
    iterable=groups.items() if isinstance(groups,dict) else enumerate(groups)
    for key,value in iterable:
        if re.search(r'(?<!\d)3009(?!\d)|KP-5\.2',json.dumps(value)):
            data['related_groups_matching_literal_id_or_code'].append({'key':key,'value':value})
    write('CORPUS_PROVENANCE.json',data)

def git_provenance():
    sm=read(HERE.parent/'snapshot_manifest.json'); tree_rows=tree(HEAD)
    rows=[]
    for row in tree_rows:
        blob=git('cat-file','blob',row['blob']); rel=row['path'].split('/attempts/3009/',1)[1]
        file=SNAP/rel; b=file.read_bytes()
        advertised=[x for x in sm['files'] if x['path']==rel][0]
        rows.append({**row,'snapshot_equal_git_blob':b==blob,'sha256':sha(blob),
             'bytes':len(blob),'advertised_mode_matches':row['mode']==advertised['mode'],
             'advertised_blob_matches':row['blob']==advertised['git_blob'],
             'advertised_sha_matches':sha(blob)==advertised['sha256']})
    diff=git('diff',BASE,HEAD,'--'); frozen=(HERE.parent/'pr_input/diff.patch').read_bytes()
    paths=git('diff','--name-only',BASE,HEAD).decode().splitlines()
    qpath='unsolved_math_prioritization/QUEUE.md'
    qdiff=git('diff',BASE,HEAD,'--',qpath).decode()
    head_queue=git('show',HEAD+':'+qpath).decode(); base_queue=git('show',BASE+':'+qpath).decode()
    inventory=read(REPO/'draft_pr_publication_program_20260930/inventory.json')
    olditem=[x for x in inventory['items'] if x.get('number',x.get('pr'))==37]
    data={'at_utc':utc(),'current_branch':git('branch','--show-current').decode().strip(),
      'current_main_head':git('rev-parse','HEAD').decode().strip(),'head':HEAD,'base':BASE,
      'merge_base':git('merge-base',BASE,HEAD).decode().strip(),
      'changed_path_count':len(paths),'paths_equal_snapshot':paths==sm['changed_paths'],
      'changed_paths':paths,'attempt_artifact_count':len(rows),'file_mode_blob_checks':rows,
      'full_diff_bytes':len(diff),'full_diff_sha256':sha(diff),'frozen_diff_byte_equal':diff==frozen,
      'head_state_path_present':bool(git('ls-tree',HEAD,'--','unsolved_math_prioritization/state.json')),
      'QUEUE_diff':qdiff,'head_QUEUE_3009':[x for x in head_queue.splitlines() if '3009 /' in x or '| 3009 |' in x],
      'base_QUEUE_3009':[x for x in base_queue.splitlines() if '3009 /' in x or '| 3009 |' in x],
      'current_QUEUE_3009':[x for x in (REPO/qpath).read_text().splitlines() if '3009 /' in x or '| 3009 |' in x],
      'original_turns':read(SNAP/'turns.json'),'inventory_item_historical':olditem}
    data['head_base_state']={}
    for ref in [BASE,HEAD]:
        b=git('show',ref+':unsolved_math_prioritization/state.json'); j=json.loads(b)
        data['head_base_state'][ref]={'blob_sha256':sha(b),'target_key_present':'3009' in j,
                                    'target_entry':j.get('3009'),'total_state_entries':len(j)}
    data['separate_one_turns_json_exists']=any(q.name=='one-turns.json' for q in SNAP.rglob('*'))
    # Read current public metadata; never issue a mutation or outreach.
    r=command(['gh','api','repos/AlecKriebel/Math/pulls/37'])
    (TMP/'current_pr_metadata.json').write_bytes(r.stdout)
    if not r.returncode:
        j=json.loads(r.stdout); data['current_metadata']={k:j.get(k) for k in ['number','state','draft','title','body','updated_at','merged_at','merge_commit_sha']}
        data['current_metadata']['head']={k:j['head'].get(k) for k in ['ref','sha']}
        data['current_metadata']['base']={k:j['base'].get(k) for k in ['ref','sha']}
        data['current_metadata']['source_receipt']=record(TMP/'current_pr_metadata.json')
    else: data['current_metadata_failure']=r.stderr.decode()
    write('GIT_ACCOUNTING_PROVENANCE.json',data)

def replays():
    root=TMP/'replays'; root.mkdir(parents=True,exist_ok=True)
    scripts=[('check_controls.py','check_results.json',31),
             ('independent_review/independent_checks.py','independent_review/independent_results.json',8462)]
    cases=[('original',None,None),
      ('code_embedding_corruption','check_controls.py',('2*x[0],2*x[1]','3*x[0],2*x[1]')),
      ('input_metric_vectors_corruption','independent_review/independent_checks.py',('i*i+j*j<=4','i*i+j*j<=8')),
      ('source_proof_fixedcount_corruption','PARTIAL.md',('has exactly two fixed points.','has exactly three fixed points.')),
      ('source_record_bound_corruption','source_record.json',('uniformly bounded in diameter','not bounded in diameter')),
      ('accounting_turn_limit_corruption','turns.json',('"substantive_turns_used": 1','"substantive_turns_used": 6')),
      ('accounting_outcome_corruption','turns.json',('"outcome": "unsolved"','"outcome": "verified_solved"'))]
    receipts=[]
    for name,path,replacement in cases:
        dest=root/name
        if dest.exists(): shutil.rmtree(dest)
        shutil.copytree(SNAP,dest)
        if path:
            t=(dest/path).read_text(); assert replacement[0] in t
            (dest/path).write_text(t.replace(*replacement))
        case={'name':name,'mutation_path':path,'replacement':replacement,'executions':[]}
        for script,receipt,expected in scripts:
            original=(SNAP/receipt).read_bytes()
            (dest/receipt).unlink()
            r=command([PYTHON,str(dest/script)],dest)
            (dest/(Path(script).name+'.stdout')).write_bytes(r.stdout)
            (dest/(Path(script).name+'.stderr')).write_bytes(r.stderr)
            result={'script':script,'expected_passed':expected,'returncode':r.returncode,
                    'stderr_tail':r.stderr.decode()[-1200:],'receipt_written':(dest/receipt).exists()}
            if (dest/receipt).exists():
                generated=(dest/receipt).read_bytes(); j=json.loads(generated); old=json.loads(original)
                result.update(complete_receipt_byte_equal=generated==original,
                   complete_receipt_json_equal=j==old,generated_sha256=sha(generated),
                   original_sha256=sha(original),passed=j['passed'],failed=j['failed'],
                   check_count=len(j['checks']),every_check_pass=all(v=='PASS' for v in j['checks'].values()))
                expected_stdout=(json.dumps(j if script=='check_controls.py' else
                                   {k:v for k,v in j.items() if k!='checks'},indent=2)+'\n').encode()
                result['stdout_byte_equal_actual_interface_serialization']=r.stdout==expected_stdout
                result['stdout_interface']='full receipt' if script=='check_controls.py' else 'metadata only, excluding checks'
            case['executions'].append(result)
        # Input corruption is compared semantically, separately from checker diagnostic status.
        if name.startswith('accounting'):
            t=json.loads((dest/'turns.json').read_text()); case['semantic_accounting_valid']=t['substantive_turns_used']==len(t['responses']) and t['substantive_turns_used']<=t['turn_limit'] and t['outcome']=='unsolved'
        if name=='source_proof_fixedcount_corruption':case['primary_theorem_statement_valid']=False
        if name=='source_record_bound_corruption':case['literal_source_matches_raw_corpus']=False
        receipts.append(case)
    write('REPLAY_AND_CORRUPTION_CONTROLS.json',{'at_utc':utc(),'python':PYTHON,'cases':receipts,
       'interpretation':'Actual source/accounting corruptions reproduce all diagnostics because neither original checker reads prose/source_record/turns. Native execution failure detects code/vector corruption, but PASS counts alone are not a provenance, theorem, or accounting certificate.'})

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--fetch',action='store_true')
    parser.add_argument('--manifest',action='store_true'); parser.add_argument('--verify-manifest',action='store_true')
    args=parser.parse_args()
    if args.manifest or args.verify_manifest:
        paths=sorted(p for p in HERE.rglob('*') if p.is_file() and
                    'ignoredtmp' not in p.relative_to(HERE).parts and '__pycache__' not in p.relative_to(HERE).parts
                    and p!=HERE/'FIRST_PARTY_MANIFEST.json')
        assert not any(p.is_symlink() for p in paths), 'Authored symlink is not an admitted regular file'
        rows=[{'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in paths]
        if args.verify_manifest:
            expected=json.loads((HERE/'FIRST_PARTY_MANIFEST.json').read_text())
            assert rows==expected['files'], 'Authored file set or hash mismatch'
            print(json.dumps({'verified':True,'files':len(rows),'exclusions':['FIRST_PARTY_MANIFEST.json','ignoredtmp/**','__pycache__/**']}))
        else:write('FIRST_PARTY_MANIFEST.json',{'at_utc':utc(),'self_excluding':True,
                 'foreign_material':'ignoredtmp/** only; no foreign file is admitted to authored files.',
                 'exclusions':['FIRST_PARTY_MANIFEST.json','ignoredtmp/**','__pycache__/**'],'files':rows})
        return
    TMP.mkdir(parents=True,exist_ok=True)
    if args.fetch:fetch_sources()
    corpus(); git_provenance(); replays()
    write('READ_EXECUTION_LEDGER.json',{'created_at_utc':utc(),'rows':LEDGER,
       'external_review_exposure':'Original metadata embedded a review verdict; independent source and import seals precede original review prose. No root/sibling report contents are inputs.'})

if __name__=='__main__':main()
