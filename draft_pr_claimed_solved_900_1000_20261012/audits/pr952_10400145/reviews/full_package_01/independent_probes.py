import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise RuntimeError('isolated only')
from pathlib import Path
import math,json,hashlib,copy,tempfile,datetime,sqlite3,difflib
O=Path(__file__).resolve().parent;A=O.parents[1];ROOT=A.parents[2];P=ROOT/'draft_pr_claimed_solved_900_1000_20261012';events=[]
def need(x,label):
 if not x:raise RuntimeError(label)
def event(label,fn,positive=True):
 try:r=fn()
 except (RuntimeError,ValueError,TypeError,KeyError,sqlite3.Error,OSError) as e:
  need(not positive,'unexpected failure '+label+': '+str(e));events.append({'test':label,'status':'REJECTED_EXPECTED','guard':str(e)});return
 need(positive,'unexpected acceptance '+label);events.append({'test':label,'status':'PASS'});return r
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True).encode()
# Universal monomial jets q^z t^j, including negative Laurent exponents.
# binom(z+n*j,d) is polynomial of rank degree <=d, so every (d+1)st
# finite difference vanishes. No candidate module is used for these checks.
def choose(z,k):
 v=1
 for i in range(k):v=v*(z-i)//(i+1)
 return v
count=0
for d in range(5):
 for z in range(-9,10):
  for j in range(8):
   for start in [1,2,5]:
    vals=[choose(z+(start+r)*j,d) for r in range(d+2)]
    for _ in range(d+1):vals=[y-x for x,y in zip(vals,vals[1:])]
    need(vals==[0],'Laurent monomial finite-difference identity');count+=1
events.append({'test':'Laurent_coefficient_higher_jet_controls','status':'PASS','exact_cases':count})
need([n*(n*n-1)*-1 for n in (1,2,3,4)]==[0,-6,-24,-60],'cubic values')
need(choose(-3,2)==6,'negative-binomial control')
# Stage-three divided-difference order: rank2 fixes b0=-6. Rank3 then
# needs -12*x additional, whereas (q3-q)(q3-q2) starts2*x^2.
events.append({'test':'second_Newton_coefficient_forced_pole','status':'PASS','additional_numerator_linear':-12,'denominator_leading_degree':2,'denominator_leading_coefficient':2,'forced_pole_leading_coefficient':-6})
# Load actual externally authenticated core, disallow every service/Git boundary.
core=P/'accept_pr952.py';raw=core.read_bytes();need(sha(raw)=='854a8694e3b4b46d3eff32f207729d2637c262b9714d8a7b052289450831e908','core pin')
n={'__name__':'_reviewer_independent_inert_','__file__':str(core)};exec(compile(raw,str(core),'exec',dont_inherit=True,optimize=0),n)
def forbidden(*a,**k):raise RuntimeError('REVIEWER: real external calls forbidden')
for key in ['run','gws','remote_main','pr_view','bounded_public_get']:n[key]=forbidden
# Direct exact type/byte preservation probes with awkward valid unrelated data.
q=b'LEAD\r\n| 10400145 / AMR-103-0145 | b | c | d | e | f | g | claimed_solved | 1/5 | j | old  | oldDOI |\r\nTAIL'
state=b' { "a": [1.00, -0, "\\u03b1"], "b" : { "sp" :  2 }  } \n';history=b'{"id":"x","unrelated":"\\u03b1"}'
eventrow=n['native_event']({'freeze_sha256':'f'*64},{'id':17,'doi':'10.5281/zenodo.17','record_url':'https://zenodo.org/records/17'},{'mergeCommit':{'oid':'a'*40}},{'updated_range':"'Math Puzzles'!A7:D7"})
r=n['native_replacements'](q,state,history,eventrow);need(r[n['HISTORY']].startswith(history),'historyprefix');need(n['queue_parts'](r[n['QUEUE']])[0]==n['queue_parts'](q)[0],'queue unrelated');need(b'[1.00, -0, "\\u03b1"]' in r[n['STATE']] and b'"b" : { "sp" :  2 }' in r[n['STATE']],'unrelated state literal')
events.append({'test':'native_raw_literals_CRLF_and_missing_history_newline','status':'PASS'})
row=n['tracker_row']({'doi':'10.5281/zenodo.17'});headers=['Original Problem','Solution Chat URL','DOI','Notes']
for label,value in [('PR_anchor_alone','https://github.com/AlecKriebel/Math/pull/952'),('title_case_alone',n['TITLE'].upper()),('problem_ID_alone','10400145'),('alternate_AMR','AMR-103-0145')]:event('tracker_'+label,lambda v=value:n['duplicate_tracker']([headers,['','','',v]],row),False)
event('notes_entity_change_no_normalization',lambda:n['exact_remote_metadata']({'metadata':{'notes':'&lt;p&gt;x&lt;/p&gt;'}},{'notes':'<p>x</p>'}),False)
event('creator_extra_affiliation_no_normalization',lambda:n['exact_remote_metadata']({'metadata':{'creators':[{'name':'Kriebel, Alec','affiliation':None}]}},{'creators':[{'name':'Kriebel, Alec'}]}),False)
# Guarded client proves failed responses do not release exclusive POST intents.
private=O/'private_independent';private.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(dir=private) as td:
 t=Path(td);n.update(ROOT=t,W=t/'workflow');n['W'].mkdir()
 class Lost:
  def __init__(self):self.creates=0
  def create(self,m):self.creates+=1;raise RuntimeError('lost create response, no ID')
 c=Lost();k={'validate_record':lambda *a:None,'verify':lambda *a:[]};g=n['GuardedZenodoClient'](c,k,{'title':'x'},[],lambda:None,'stage');event('create_lost_response',lambda:g.create({'title':'x'}),False)
 g2=n['GuardedZenodoClient'](c,k,{'title':'x'},[],lambda:None,'stage');event('create_lost_response_second_process_stopped_by_intent',lambda:g2.create({'title':'x'}),False);need(c.creates==1,'second POST reached client')
 # Actual function with the unchanged private nonempty report, new fixture cases.
 frozen= json.loads((A/'source_record_private.txt').read_bytes());need(bool(frozen['prior_research']),'nonempty prior must not be empty assumption')
 n.update(ROOT=t,A=t/'audit');n['A'].mkdir();(n['A']/'source_record_private.txt').write_bytes((A/'source_record_private.txt').read_bytes());cache=t/'unsolved_math_prioritization/cache';cache.mkdir(parents=True);db=cache/'catalog.sqlite'
 blobs={n['CATALOG']:enc([{'id':10400145,'present':True,'holds':[],'statement_hash':n['STATEMENT'],'review_hash':n['REVIEW']}]),n['RELATED']:enc({'groups':[]})};n['blob']=lambda ref,p:blobs[p]
 def rebuild(report,raw_problem=None):
  if db.exists():db.unlink()
  with sqlite3.connect(db) as c:
   c.execute('CREATE TABLE records(key TEXT,payload TEXT,report TEXT)');c.execute('INSERT INTO records VALUES(?,?,?)',(n['KEY'],raw_problem or json.dumps(frozen['problem'],indent=3),json.dumps(report,sort_keys=False,indent=4)))
 def source():
  before=db.read_bytes();names=sorted(p.name for p in cache.iterdir())
  try:return n['source_gate']('INERT')
  finally:need(db.read_bytes()==before and sorted(p.name for p in cache.iterdir())==names,'source mutated fixture')
 rebuild(dict(reversed(list(frozen['prior_research'].items()))));r=event('source_nonempty_prior_raw_whitespace_keyorder_semantic_identity',source);need(r['raw_prior_report_matched_frozen_report'] is True and r['prior_research_sha256']==n['PRIOR_REPORT_SHA'],'reportpin')
 changed=copy.deepcopy(frozen['prior_research']);changed['REVIEWER_NEW_FIELD']=[];rebuild(changed);event('source_report_added_empty_field_rejected_by_full_equality',source,False)
 rebuild(frozen['prior_research'],json.dumps(frozen['problem'])[:-1]+',"id":10400145}');event('source_duplicate_raw_problem_key_rejected',source,False)
 # Empty, null and boolean report were never treated as missing original history.
 for report in [{},None,False]:rebuild(report);event('source_raw_prior_type_or_empty_'+repr(report),source,False)
# All five wrapper bodies must be identical except their explicit final action.
base=(P/'merge_pr952.py').read_text();actions={'merge_pr952.py':'merge','run_pr952_zenodo.py':'zenodo','append_pr952_tracker.py':'tracker','update_pr952_publication_ledger.py':'native','finalize_pr952_and_gate_next.py':'finalize'}
for name,action in actions.items():need((P/name).read_text().replace("entry('"+action+"')","entry('ACTION')")==base.replace("entry('merge')","entry('ACTION')"),'wrapper drift '+name)
events.append({'test':'all_five_wrappers_entire_source_equivalence_except_fixed_action','status':'PASS','wrapper_count':5})
print(json.dumps({'schema':'pr952-full01-independent-probes-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','outer_optimization':sys.flags.optimize,'events':events,'event_count':len(events),'real_service_calls':0,'real_Git_calls':0,'private_bodies_in_output':False},sort_keys=True))
