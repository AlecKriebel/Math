#!/usr/bin/env python3
"""Read-only independent original-stage identity/provenance audit; writes own outputs only."""
import collections, hashlib, json, pathlib, re, sqlite3, subprocess
from datetime import datetime, timezone

ROOT = pathlib.Path('/Users/alec/Documents/Math')
HERE = pathlib.Path(__file__).resolve().parent
AUDIT = HERE.parent
SNAP = AUDIT / 'source_snapshot'
HEAD = 'a92af24e2e6015893787e0c55cd4618f7098917e'
BASE = '01358d66fc67d1c462bddf31c0d4ee5b120e6737'
MAIN = '8d7564ed861f86bf1e38c43877c0634a07f474b8'
PREFIX = 'unsolved_math_prioritization/attempts/6800007/'

def sha(data): return hashlib.sha256(data).hexdigest()
def read(path): return json.loads(path.read_bytes())
def save(name, value): (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def git(*args): return subprocess.check_output(['git', *args], cwd=ROOT)
def blob(ref,path): return git('show',ref+':'+path)
def queue_row(data): return [s for s in data.decode().splitlines() if '| 6800007 / AMR-067-0007 |' in s]
def leaves(value):
    if isinstance(value,dict): return sum(leaves(v) for v in value.values())
    if isinstance(value,list): return sum(leaves(v) for v in value)
    return 1

result={'utc':datetime.now(timezone.utc).isoformat(), 'head':HEAD, 'actual_base':BASE,
        'metadata_base':read(AUDIT/'snapshot_manifest.json')['base'], 'files':[]}
manifest=read(AUDIT/'snapshot_manifest.json')
isolated=HERE/'isolated_original'; isolated.mkdir(exist_ok=True)
for member in manifest['files']:
    data=(SNAP/member['path']).read_bytes()
    headbytes=blob(HEAD,PREFIX+member['path'])
    oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    item={'path':member['path'],'size':len(data),'sha256':sha(data),'git_blob':oid,
          'matches_manifest':len(data)==member['size'] and sha(data)==member['sha256'] and oid==member['git_blob'],
          'matches_exact_head':data==headbytes}
    if member['path'].endswith('.json'):
        obj=json.loads(data); item.update(json_type=type(obj).__name__,json_scalar_leaves=leaves(obj),
            json_keys=list(obj) if isinstance(obj,dict) else None)
    elif member['path'].endswith('.jsonl'):
        obj=[json.loads(line) for line in data.decode().splitlines()]; item.update(records=len(obj),json_scalar_leaves=leaves(obj))
    else: item['lines']=len(data.splitlines())
    target=isolated/member['path']; target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    result['files'].append(item)
assert len(result['files'])==15 and all(f['matches_manifest'] and f['matches_exact_head'] for f in result['files'])
diff=git('diff','--binary',BASE,HEAD)
given=(AUDIT/'pr_input/diff.patch').read_bytes()
paths=git('diff','--name-only',BASE,HEAD).decode().splitlines()
result['diff']={'bytes':len(diff),'sha256':sha(diff),'matches_saved_patch':diff==given,'paths':paths,
                'exactly_16':len(paths)==16,'queue_changed': 'unsolved_math_prioritization/QUEUE.md' in paths}
assert paths==manifest['changed_paths'] and diff==given
result['queue']={ref:queue_row(blob(ref,'unsolved_math_prioritization/QUEUE.md')) for ref in [BASE,HEAD,MAIN]}
result['queue']['current']=queue_row((ROOT/'unsolved_math_prioritization/QUEUE.md').read_bytes())
q=(ROOT/'unsolved_math_prioritization/queue.py').read_bytes()
result['queue']['legacy_generator']={'sha256':sha(q),'header_columns':8,'current_row_columns':len(result['queue']['current'][0].split('|')[1:-1]),
    'generator_called':False,'reason':'Legacy rank() overwrites QUEUE with eight columns, dropping protected current fields.'}
result['pr_body_scope']={'only_folder_claim':'only this problem\'s attempt folder changes' in read(AUDIT/'pr_input.json')['body'],
    'contradicted_by_queue':True,'historical_no_merge_language':'No merge or release is requested' in read(AUDIT/'pr_input.json')['body'],
    'not_current_authorization':True}
result['old_receipt']={name:read(SNAP/name) for name in ['verification.json','review/review_summary.json']}
ind=read(SNAP/'review/independent_results.json')
result['independent_results_inventory']={'keys':list(ind),'checks_count':len(ind.get('checks',[])),
    'unique_check_labels':len(set(ind.get('checks',[]))), 'pass':ind.get('pass'),
    'full_decoded_scalar_leaves':leaves(ind),'noncheck_fields':{k:v for k,v in ind.items() if k!='checks'}}
save('EXACT_INPUT_AUDIT.json',result)

problems=read(HERE/'tmp/problems.json'); reports=read(HERE/'tmp/research_results.json')
matches_id=[p for p in problems if str(p.get('id'))=='6800007']
matches_code=[p for p in problems if p.get('problem_number')=='AMR-067-0007']
assert len(matches_id)==len(matches_code)==1 and matches_id==matches_code
p=matches_id[0]; r=reports['AMR-067-0007']
stored=read(SNAP/'source_record.json')
assert p==stored['problem'] and r==stored['prior_upstream_report']
review_hash=sha(json.dumps([p,r],sort_keys=True).encode())
statement_hash=sha(p['statement'].encode())
source={'utc':datetime.now(timezone.utc).isoformat(),'revision':read(SNAP/'source_manifest.json')['dataset_revision'],
    'raw_files':{n:{'size':(HERE/'tmp'/n).stat().st_size,'sha256':sha((HERE/'tmp'/n).read_bytes())} for n in ['problems.json','research_results.json']},
    'unique_id_count':len(matches_id),'unique_code_count':len(matches_code),'problem':p,'prior_report':r,
    'source_record_problem_equal':True,'source_record_full_report_equal':True,'review_hash':review_hash,'statement_hash':statement_hash,
    'hash_meaning':'review_hash = SHA256 of Python default json.dumps([raw_problem, raw_report], sort_keys=True). It binds source content/context; not proof, readiness or mathematical validity.',
    'related_flag_targets':[{'id':v['id'],'problem_number':v['problem_number'],'title':v['title'],'statement':v['statement'],'classification':v.get('research_classification'),'prior_report':reports.get(v['problem_number'])} for v in problems if 'flag manifold' in (v.get('title','')+' '+v.get('statement','')).lower() and v.get('id')!=6800007]}
dbpath=ROOT/'unsolved_math_prioritization/cache/catalog.sqlite'
db=sqlite3.connect(dbpath.as_uri()+'?mode=ro',uri=True)
rows=db.execute('select key,payload,report,typeof(payload),typeof(report) from records where key=?',('6800007',)).fetchall()
assert len(rows)==1
key,payload,report,tp,tr=rows[0]; sqlp=json.loads(payload);sqlr=json.loads(report)
source['sqlite']={'opened_read_only':True,'key':key,'payload_sql_type':tp,'report_sql_type':tr,'report_is_sql_null':report is None,
    'report_decoded_type':type(sqlr).__name__,'payload_equals_raw':sqlp==p,'report_equals_raw':sqlr==r,
    'revision_rows':db.execute('select revision from metadata').fetchall(),
    'review_hash':sha(json.dumps([sqlp,sqlr],sort_keys=True).encode())}
source['sqlite']['unique_code_count']=sum(json.loads(row[0]).get('problem_number')=='AMR-067-0007' for row in db.execute('select payload from records'))
db.close()
for ref in [MAIN,HEAD]:
    historical={}
    for file in ['state.json','history.jsonl','catalog.json']:
        try:
            data=blob(ref,'unsolved_math_prioritization/'+file)
            obj=[json.loads(l) for l in data.decode().splitlines()] if file.endswith('jsonl') else json.loads(data)
            relevant=[v for v in obj if str(v.get('id'))=='6800007'] if isinstance(obj,list) else obj.get('6800007')
            historical[file]={'file_sha256':sha(data),'matching_target':relevant}
        except subprocess.CalledProcessError: historical[file]={'unavailable':True}
    source.setdefault('dated_histories',{})[ref]=historical
current={}
for name in ['state.json','history.jsonl','assessment_history.jsonl','catalog.json']:
    path=ROOT/'unsolved_math_prioritization'/name
    data=path.read_bytes();obj=[json.loads(l) for l in data.decode().splitlines()] if name.endswith('jsonl') else json.loads(data)
    matching=[v for v in obj if str(v.get('id'))=='6800007'] if isinstance(obj,list) else obj.get('6800007')
    current[name]={'sha256':sha(data),'target':matching}
source['current_local_records']=current
ghdata=(HERE/'tmp/GITHUB_ALL_STATE_CURRENT.json').read_bytes();pages=json.loads(ghdata); pulls=[p for page in pages for p in page]
patterns=[r'6800007',r'AMR[- ]?067[- ]?0007',r'totally real',r'flag immersions',r'flag manifold']
ghmatches=[{'number':v['number'],'state':v['state'],'draft':v.get('draft'),'title':v['title'],'url':v['html_url'],'head':v['head']['sha'],'base':v['base']['sha'],'body':v.get('body'),'created_at':v['created_at'],'updated_at':v['updated_at'],'merged_at':v['merged_at']} for v in pulls if any(re.search(s,(v['title']+' '+(v.get('body') or '')),re.I) for s in patterns)]
source['current_gh_inventory']={'utc_analysis':datetime.now(timezone.utc).isoformat(),'query':'GET repos/AlecKriebel/Math/pulls?state=all&per_page=100, gh --paginate --slurp',
    'pages':len(pages),'pulls':len(pulls),'states':dict(collections.Counter(v['state'] for v in pulls)), 'sha256':sha(ghdata),'bytes':len(ghdata),'patterns':patterns,'matches':ghmatches,
    'limits':'Current all-state title/body inventory is not proof of historical absence at readiness time or absence of differently named work; issues, remote branches and outside repositories not queried. Query, model and effort metadata cannot certify mathematics.'}
source['identity_controls']={'json_null_distinct_from_sql_NULL':json.dumps(None)=='null' and None!='null',
    'report_hash_changes_if_null':sha(json.dumps([p,None],sort_keys=True).encode())!=review_hash,
    'report_hash_changes_if_empty_object':sha(json.dumps([p,{}],sort_keys=True).encode())!=review_hash,
    'compact_serialization_changes_hash':sha(json.dumps([p,r],sort_keys=True,separators=(',',':')).encode())!=review_hash,
    'id_change_changes_hash':sha(json.dumps([{**p,'id':6800006},r],sort_keys=True).encode())!=review_hash,
    'code_change_changes_hash':sha(json.dumps([{**p,'problem_number':'AMR-067-0006'},r],sort_keys=True).encode())!=review_hash}
save('SOURCE_IDENTITY_AUDIT.json',source)
print(json.dumps({'files':len(result['files']),'exact_blobs':True,'diff_paths':len(paths),'review_hash':review_hash,'unique_id':True,'unique_code':True,'gh_matches':[v['number'] for v in ghmatches],'prior_report':r},indent=2))
