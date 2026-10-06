from pathlib import Path
import collections, datetime, hashlib, json, re, sqlite3, subprocess

ROOT=Path('/Users/alec/Documents/Math')
OUT=Path(__file__).resolve().parent
SOURCE=OUT.parent/'source_snapshot'
Q=ROOT/'unsolved_math_prioritization'
HEAD='762f5808268a85a5cb5373d3f7d60ad160b828f5'
BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
ID='10400115'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def command(args):
 r=subprocess.run(args,cwd=ROOT,capture_output=True,check=False)
 return {'args':args,'exit':r.returncode,'stdout':r.stdout.decode(errors='replace'),'stderr':r.stderr.decode(errors='replace')}
def git(*args):
 r=command(['git',*args]);assert r['exit']==0,r;return r['stdout']
def norm(x):return ''.join(re.findall(r'[a-z0-9]+',x.casefold()))

raw=read(Q/'cache/problems.json'); reports=read(Q/'cache/research_results.json'); manifest=read(Q/'manifest.json')
con=sqlite3.connect('file:'+str(Q/'cache/catalog.sqlite')+'?mode=ro',uri=True)
sql={k:{'problem':json.loads(p),'report':json.loads(r)} for k,p,r in con.execute('SELECT key,payload,report FROM records')}
raw_by_id={str(x['id']):x for x in raw};counts=collections.Counter(x['problem_number'] for x in raw)
selected=raw_by_id[ID];prior=reports[selected['problem_number']]
corpus={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'revision':manifest['revision'],'raw_records':len(raw),'sqlite_records':len(sql),'sqlite_revision':con.execute('SELECT revision FROM metadata').fetchall(),
 'source_files':[{ 'name':n,'sha256':sha((Q/'cache'/n).read_bytes()),'bytes':(Q/'cache'/n).stat().st_size,'matches_manifest':{'sha256':sha((Q/'cache'/n).read_bytes()),'bytes':(Q/'cache'/n).stat().st_size}==v} for n,v in manifest['files'].items()],
 'literal_id_matches':[x['id'] for x in raw if str(x['id'])==ID],
 'literal_code_matches':[x['id'] for x in raw if x['problem_number']==selected['problem_number']],
 'literal_statement_matches':[x['id'] for x in raw if x.get('statement')==selected['statement']],
 'normalized_statement_matches':[x['id'] for x in raw if norm(x.get('statement',''))==norm(selected['statement'])],
 'broad_algebraic_braid_matches':[{k:x.get(k) for k in ('id','problem_number','title','statement')} for x in raw if re.search(r'braid|\bBn\b',x.get('statement',''),re.I) and re.search(r'algebraic|\u00afQ|Q.?bar|rational|faithful',x.get('statement',''),re.I)],
 'selected':selected,'selected_prior':prior,'sqlite_selected_matches_raw':sql[ID]['problem']==selected,'sqlite_prior_matches_raw':sql[ID]['report']==prior,
 'snapshot_source_record_matches_sqlite':read(SOURCE/'source_record.json')==sql[ID]['problem'],'snapshot_prior_matches_sqlite':read(SOURCE/'prior_report.json')==sql[ID]['report'],
 'statement_sha256':sha(selected['statement'].encode()),'review_sha256':sha(json.dumps([selected,prior],sort_keys=True).encode()),
 'distinct_neighbor':{'raw_problem':raw_by_id['10400109'],'prior':reports[raw_by_id['10400109']['problem_number']],'sqlite_matches_raw':sql['10400109']['problem']==raw_by_id['10400109']},
 'related_group_matches':[g for g in read(Q/'review_v2/related_target_groups.json')['groups'] if ID in g.get('ids',[]) or '10400109' in g.get('ids',[])],
 'source_type':'Raw prior is OPEN-TRIAGE with no target proof; specialized arbitrary-degree algebraic target differs from generic Temperley-Lieb family.'}
(OUT/'corpus_provenance.json').write_text(json.dumps(corpus,indent=2)+'\n')

snap=read(OUT.parent/'snapshot_manifest.json');files=[]
for f in sorted(SOURCE.rglob('*')):
 if not f.is_file():continue
 relative=str(f.relative_to(SOURCE));b=f.read_bytes();original=git('show',HEAD+':unsolved_math_prioritization/attempts/'+ID+'/'+relative).encode()
 receipt=next(x for x in snap['files'] if x['path']==relative)
 files.append({'path':relative,'bytes':len(b),'sha256':sha(b),'git_blob_sha1':hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest(),'matches_git_head':b==original,'matches_freeze_manifest':sha(b)==receipt['sha256'] and len(b)==receipt['bytes']})
changed=git('diff','--name-only',BASE,HEAD).splitlines();merge_base=git('merge-base',BASE,HEAD).strip()
queue_head=git('show',HEAD+':unsolved_math_prioritization/QUEUE.md');queue_base=git('show',BASE+':unsolved_math_prioritization/QUEUE.md')
queue_diff=git('diff',BASE,HEAD,'--','unsolved_math_prioritization/QUEUE.md')
(OUT/'selected_queue_diff.txt').write_text(queue_diff)
for name,content in [('head',queue_head),('base',queue_base)]:
 (OUT/('selected_queue_'+name+'.txt')).write_text('\n'.join(x for x in content.splitlines() if ID in x)+'\n')
git_receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':HEAD,'base':BASE,'actual_merge_base':merge_base,'snapshot_files':files,'snapshot_file_count':len(files),'changed_paths':changed,'changed_path_count':len(changed),'head_queue_row':[x for x in queue_head.splitlines() if ID in x],'base_queue_row':[x for x in queue_base.splitlines() if ID in x],'diff_lines_changed':[x for x in queue_diff.splitlines() if x.startswith(('+','-')) and not x.startswith(('+++','---'))], 'read_only_current_main':git('rev-parse','HEAD').strip(),'current_branch':git('branch','--show-current').strip(),'head_commit':git('show','--no-patch','--format=fuller',HEAD),'head_target_history':git('log','--format=%H %cI %s',HEAD,'--','unsolved_math_prioritization/attempts/'+ID),'base_attempt_paths':git('ls-tree','-r','--name-only',BASE,'--','unsolved_math_prioritization/attempts/'+ID)}
(OUT/'git_scope_receipt.json').write_text(json.dumps(git_receipt,indent=2)+'\n')

canonical={}
for fn in ['state.json','catalog.json','assessments.json','history.jsonl','assessment_history.jsonl']:
 path=Q/fn
 if fn.endswith('.jsonl'):selected_rows=[json.loads(s) for s in path.read_text().splitlines() if s.strip() and str(json.loads(s).get('id'))==ID]
 else:
  content=read(path);selected_rows=content.get(ID) if isinstance(content,dict) else [x for x in content if str(x.get('id'))==ID]
 canonical[fn]={'sha256':sha(path.read_bytes()),'selected_rows':selected_rows}
canonical['QUEUE.md']={'sha256':sha((Q/'QUEUE.md').read_bytes()),'selected_rows':[x for x in (Q/'QUEUE.md').read_text().splitlines() if ID in x]}
canonical['caveat']='Canonical mirror is parent work after accepting partial; static assessment can remain historical, queue generation needs status/assessment synchronization and impact-score reapplication. No canonical file mutated by this audit.'
(OUT/'canonical_mirror_diagnostic.json').write_text(json.dumps(canonical,indent=2)+'\n')

# Read-only GitHub all-state exact target search, using all returned pages, not cached inventories.
pulls=command(['gh','api','--paginate','--slurp','repos/AlecKriebel/Math/pulls?state=all&per_page=100']); pr26=command(['gh','api','repos/AlecKriebel/Math/pulls/26'])
github={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_state_query':pulls,'pr26_query':pr26}
if pulls['exit']==0:
 pages=json.loads(pulls['stdout']);all_prs=[p for page in pages for p in page]
 github['all_state_total']=len(all_prs);github['exact_target_matches']=[{k:p.get(k) for k in ('number','state','title','body','html_url','head','base','draft','merged_at')} for p in all_prs if re.search(r'10400115|AMR-103-0115',str(p.get('title'))+' '+str(p.get('body'))+' '+str(p.get('head',{}).get('ref')))]
if pr26['exit']==0:
 current=json.loads(pr26['stdout']);github['head_still_matches']=current['head']['sha']==HEAD;github['pr26_selected']={k:current.get(k) for k in ('number','state','title','body','draft','merged','merged_at','html_url')}
(OUT/'github_readonly_receipt.json').write_text(json.dumps(github,indent=2)+'\n')
print(json.dumps({'raw_count':len(raw),'literal_id':corpus['literal_id_matches'],'code':corpus['literal_code_matches'],'statement':corpus['literal_statement_matches'],'normalized':corpus['normalized_statement_matches'],'source_hashes_match':all(x['matches_manifest'] for x in corpus['source_files']),'sqlite_snapshot_match':corpus['snapshot_source_record_matches_sqlite'] and corpus['snapshot_prior_matches_sqlite'],'review_hash':corpus['review_sha256'],'snapshot_file_count':len(files),'all_files_match_head':all(x['matches_git_head'] for x in files),'changed_path_count':len(changed),'queue_head_row':git_receipt['head_queue_row'],'all_state_total':github.get('all_state_total'),'all_state_exact_prs':[p['number'] for p in github.get('exact_target_matches',[])],'head_still_matches':github.get('head_still_matches')},indent=2))
