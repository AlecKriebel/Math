#!/usr/bin/python3
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sqlite3,subprocess,urllib.request
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
ORIG=ROOT.parent/'original_preparation_family'
cfg=json.loads((ROOT/'source_input.json').read_text());checks=0

def need(v,msg):
 global checks
 checks+=1
 if not v:raise AssertionError(msg)

def body_row(p):
 p=Path(p);h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return {'path':str(p),'bytes':p.stat().st_size,'sha256':h.hexdigest(),'mode':format(p.stat().st_mode&0o7777,'04o')}

def load(p):return json.loads(Path(p).read_text())
refs=[]
for p in [ORIG/'original'/'CANDIDATE.md',ORIG/'original'/'source_record.json',ORIG/'original'/'status.json',ORIG/'original'/'turns.jsonl',ORIG/'ORIGINAL_AUTHENTICATION.json',ORIG/'SCIENCE_INDEX.json',ORIG/'SOURCE_ACCOUNTING.json',ORIG/'SELF_MANIFEST.json']:
 refs.append(body_row(p))
need(refs[-1]['sha256']==cfg['actual_closed_original_manifest_sha256'],'Genuine closed original packet pin')
auth=load(ORIG/'ORIGINAL_AUTHENTICATION.json')
need(auth['original_head']==cfg['original_head'],'Original original-head identity')
need(auth['actual_merge_base_oid']==cfg['actual_merge_base'],'Actual merge-base distinct from reported base')
need(auth['github_base_oid']==cfg['reported_base'] and not auth['github_base_equals_actual_merge_base'],'Reported base qualification')
sci=load(ORIG/'SCIENCE_INDEX.json')
need(sci['original_science_count']==16 and sci['complete_original_diff_count']==17,'Full original science/diff counts')
for r in sci['original_science']:
 p=Path(r['archive_path']);rr=body_row(p)
 need(rr['sha256']==r['sha256'] and rr['bytes']==r['bytes'],'Selected authenticated original whole body')
 b=p.read_bytes();need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob_sha1'],'Original Git blob identity recomputed')
 need(rr['mode']=='0444','Original file remains closed')
 if rr['path'] not in {x['path'] for x in refs}:refs.append(rr)
account=load(ORIG/'SOURCE_ACCOUNTING.json')
corpus=[Path(account['raw_corpus_references'][n]['path']) for n in ['problems.json','research_results.json']]
db=Path(account['SQL_database_reference']['path'])
before=[body_row(p) for p in corpus+[db]]
for r,e in zip(before,[account['raw_corpus_references']['problems.json'],account['raw_corpus_references']['research_results.json'],account['SQL_database_reference']]):
 need(r==e,'Whole raw source reference agrees with dated source accounting')
problems=load(corpus[0]);results=load(corpus[1]);record=load(ORIG/'original'/'source_record.json')
selected=[p for p in problems if p['id']==cfg['problem_id']]
need(len(selected)==1 and selected[0]['problem_number']==cfg['source_code'],'Unique raw numeric/source code match')
need(selected[0]==record['problem'],'Literal original problem equals raw selected problem')
need(str(cfg['problem_id']) not in results,'Raw report key ABSENT, not null')
c=sqlite3.connect('file:'+str(db)+'?mode=ro',uri=True)
row=c.execute('SELECT key,payload,report,report IS NULL,typeof(report) FROM records WHERE key=?',(str(cfg['problem_id']),)).fetchone()
need(row is not None and row[0]==str(cfg['problem_id']),'SQL exact selected row')
need(json.loads(row[1])==record['problem'],'SQL selected problem typed equality')
need(row[2]=='{}' and row[3]==0 and row[4]=='text','SQL non-NULL TEXT empty-object fallback')
need(record['upstream_report'] is None and 'upstream_report' in record,'Archived wrapper null is a separate placeholder')
need(not (ORIG/'original'/'prior_report.json').exists(),'No archived separate report material')
turns=[json.loads(t) for t in (ORIG/'original'/'turns.jsonl').read_text().splitlines() if t.strip()]
status=load(ORIG/'original'/'status.json')
need(len(turns)==1 and turns[0]['turn']==1,'One literal original JSONL turn')
need(sci['original_turns_used']==1 and sci['original_turn_limit']==5 and sci['original_proposal_status']=='claimed_solved','Original proposal 1/5, not new-control counts')
need([body_row(p) for p in corpus+[db]]==before,'Raw source whole bodies and modes unchanged during read-only checks')
refs.extend(before)
# Record genuine ROOT original-source closure/readback captures without inferring
# any ROOT reading of this new mathematical review.
A45=ROOT.parent.parent/'pr45_9900007'
for name in ['root_pr55_original_source_closure_actual_capture','root_pr55_original_source_closed_readback_actual_capture']:
 folder=A45/name
 cap=load(folder/'CAPTURE.json');need(cap['exit_code']==0,'Genuine ROOT original-source command exited zero')
 for n in ['CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin']:refs.append(body_row(folder/n))
source_results=[]
for key,pages in [('book_url',[219,220,221,222,299,301,302,345,361,362,363,364,365]),('sano_url',[1,2,3,14,15,16]),('ogusu_sano_url',[1,3,4,5,6,7,9,10,11]),('owr_url',[919,920,921])]:
 with urllib.request.urlopen(cfg[key],timeout=45) as response:
  b=response.read();final_url=response.url
 h=hashlib.sha256(b).hexdigest()
 if key=='book_url':need(h==cfg['book_expected_sha256'],'Exact previously personally read primary GKZ edition')
 proc=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout','-','-'],input=b,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 need(proc.returncode==0 and not proc.stderr,'Primary PDF extracts without errors')
 text=proc.stdout.decode();normalized=' '.join(text.split())
 if key=='book_url':
  flags={k:v in normalized for k,v in {'ch7_upper_convention':'upper boundary','ch7_definition':'Definition 1.4.','ch7_normal_label':'Theorem 1.7.','ch10_initial_label':'Theorem 1.4.','ch11_smooth_identification':'Theorem 1.3.','ch11_vertices':'Theorem 3.2.','ch11_fan':'Theorem 3.4.','ch11_explicit_vertex_cone':'Proposition 3.7.'}.items()}
 elif key=='sano_url':
  flags={k:v in normalized for k,v in {'source_model':'Theorem 1.4.','smooth_scope':'smooth polarized','degree_scope':'greater than or equal to two','massive_boundary':'massive','old_analytic_mechanism':'energy'}.items()}
 elif key=='ogusu_sano_url':
  flags={k:v in normalized for k,v in {'source_partial_result':'Theorem 1.2.','surface_product_identity':'Proposition 3.5.','massive_definition':'massive','old_reverse_direction_gap':'converse','weight_projection':'trivially'}.items()}
 else:
  flags={'literal_problem':'Can we (re)-prove' in normalized,'theorem_reference':'Sano' in normalized,'combinatorial_request':'combinatorial way' in normalized}
 need(all(flags.values()),'Primary key definitions and exact question are present')
 source_results.append({'url':cfg[key],'final_url':final_url,'bytes':len(b),'sha256':h,'physical_page_count':len(text.split('\f'))-1,'selected_printed_page_reading_references':pages,'text_presence_checks':flags,'primary_body_or_text_saved':False,'qualification':'These are source presence checks. The written audit contains the personal mathematical reading; this script does not certify the primary theorems.'})
result={'status':'PASS_PRIMARY_ACQUISITION_AND_LITERAL_SCOPE_CONTROLS','utc':datetime.now(timezone.utc).isoformat(),'require_evaluations':checks,'prior_report':{'raw_key':'ABSENT','SQL_report_literal':'{}','SQL_type':'text','SQL_is_NULL':False,'archived_wrapper_upstream_report':None,'generic_response_count':'not supplied; no count invented'},'original':{'head':cfg['original_head'],'actual_merge_base':cfg['actual_merge_base'],'reported_base':cfg['reported_base'],'claimed_solved_turns':'1/5','JSONL_entries':1},'primary_sources':source_results,'external_reference_count':len(refs),'external_reference_qualification':'Whole in-place SHA256/body size/full mode; no primary or giant corpus copies. Original file authentication is the existing Git API tree/blob record, not a signed commit certificate.','acceptance_authority':False,'mathematical_proof_certified_by_source_presence_checks':False}
(ROOT/'EXTERNAL_REFERENCES.json').write_text(json.dumps(refs,indent=2)+'\n')
(ROOT/'PRIMARY_AND_SCOPE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='primary_sources'},sort_keys=True))
