"""Select literal PR52 source/status records without copying or mutating shared data."""
from pathlib import Path
import datetime,hashlib,json,re,sqlite3
F=Path(__file__).resolve().parent;R=Path('/Users/alec/Documents/Math');U=R/'unsolved_math_prioritization'
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return {'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':h.hexdigest(),'mode':format(p.stat().st_mode&0o7777,'04o')}
def save(n,x):(F/n).write_text(json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
manifest=json.loads((U/'manifest.json').read_bytes());assert manifest['revision']=='37e53eabe540fb458758e198be61634bd02ee008'
rawpins={};raw={}
for n in ['problems.json','research_results.json']:
 p=U/'cache'/n;pin=ident(p);assert {k:pin[k] for k in ['bytes','sha256']}==manifest['files'][n];rawpins[n]=pin;raw[n]=json.loads(p.read_bytes())
p=raw['problems.json'];selected=[x for x in p if str(x.get('id'))=='30000644'];assert len(selected)==1;code=selected[0]['problem_number'];samecode=[x for x in p if x.get('problem_number')==code]
reports=raw['research_results.json'];present=code in reports
norm=lambda s:re.sub(r'\s+',' ',s).strip()
exact=[x for x in p if norm(x.get('statement',''))==norm(selected[0]['statement'])]
terms=[x for x in p if ('reduction' in x.get('title','').lower() and 'automorphism' in x.get('title','').lower()) or ('SAut' in x.get('statement','') and ('t^m' in x.get('statement','') or 't^{m}' in x.get('statement','')))]
dbpath=U/'cache/catalog.sqlite';db=sqlite3.connect('file:'+str(dbpath.resolve())+'?mode=ro&immutable=1',uri=True);schema=db.execute('PRAGMA table_info(records)').fetchall();rows=db.execute('SELECT key,payload,report FROM records WHERE key=?',('30000644',)).fetchall();assert len(rows)==1;revision=db.execute('SELECT revision FROM metadata').fetchall();db.close()
q=rows[0];assert json.loads(q[1])==selected[0] and json.loads(q[2])==({} if not present else reports[code])
original=json.loads((F/'original/source_record.json').read_bytes());assert original==selected[0]
cat=json.loads((U/'catalog.json').read_bytes());catalogrows=[x for x in cat if str(x.get('id'))=='30000644'];assert len(catalogrows)==1
related=json.loads((U/'review_v2/related_target_groups.json').read_bytes())
def related_matches(x):
 if isinstance(x,dict):
  if '30000644' in json.dumps(x,sort_keys=True):return [x]
  return []
 if isinstance(x,list):return [r for y in x for r in related_matches(y)]
 return []
# Select matching complete top-level groups; no related-record discovery credit is inferred.
if isinstance(related,dict):rg={k:related_matches(v) for k,v in related.items()};rg={k:v for k,v in rg.items() if v}
else:rg=related_matches(related)
state=json.loads((U/'state.json').read_bytes());queue=(U/'QUEUE.md').read_text();targetlines=[x for x in queue.splitlines() if '30000644 /' in x]
save('SELECTED_LITERAL_SOURCE.json',{'schema':'pr52-selected-literal-source/v1','date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'revision':manifest['revision'],'raw_file_bindings':rawpins,'raw_problem_record':selected[0],'raw_research_results_key':code,'raw_research_results_key_present':present,'raw_research_results_literal_value':reports[code] if present else None,'raw_research_results_value_semantics':'actual JSON null' if present and reports[code] is None else ('present JSON object/value' if present else 'ABSENT key; null here is only the absence-display sentinel'),'raw_matching_problem_code_records':samecode,'raw_exact_normalized_statement_records':exact,'raw_related_term_records':terms,'sql_database_reference_only':ident(dbpath),'sql_immutable_read_schema':schema,'sql_metadata_revision_literal':revision,'sql_selected_key_literal':q[0],'sql_selected_payload_literal':q[1],'sql_selected_report_literal':q[2],'sql_report_decoded_type':type(json.loads(q[2])).__name__,'original_source_record_equal_raw_selected':True,'original_prior_report_bytes':(F/'original/prior_report.json').read_bytes().decode(),'original_prior_report_decoded':json.loads((F/'original/prior_report.json').read_bytes()),'no_large_raw_corpus_copied':True})
save('DATED_NATIVE_SELECTION.json',{'schema':'pr52-dated-native-selection/v1','date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reference_only_no_future_authority':True,'bindings':[ident(U/n) for n in ['manifest.json','catalog.json','state.json','QUEUE.md','README.md','review_v2/related_target_groups.json','queue.py']],'selected_catalog':catalogrows[0],'selected_state_present':'30000644' in state,'selected_state':state.get('30000644'),'selected_queue_lines':targetlines,'selected_related_groups':rg,'native_status_not_replaced':True})
print(json.dumps({'status':'PASS','raw_report_key_present':present,'sql_report_literal':q[2],'original_prior_report_literal':(F/'original/prior_report.json').read_text().strip(),'matching_problem_code_records':len(samecode),'exact_normalized_statement_records':len(exact),'related_term_records':len(terms),'source_record_equal':True,'raw_corpora_fully_hash_authenticated':True},sort_keys=True))
