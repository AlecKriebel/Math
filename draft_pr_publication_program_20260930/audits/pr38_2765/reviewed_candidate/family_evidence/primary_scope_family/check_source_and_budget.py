from pathlib import Path
import hashlib,json,copy,datetime
out=Path(__file__).resolve().parent
raw=json.loads((out/'raw_source_record.json').read_text());score=json.loads((out/'raw_importer_pin.json').read_text())['pure_queue_score'];original=json.loads((out/'original_pin/source_record.json').read_text());turns=json.loads((out/'original_pin/turns.json').read_text());attempt=json.loads((out/'original_pin/attempt.json').read_text())
def source_check(p):
 assert p['id']==2765 and p['problem_number']=='KP-2.17','numeric identity'
 assert hashlib.sha256(p['statement'].encode()).hexdigest()==score['statement_hash'],'literal statement hash'
 assert p==original,'complete source equality'
def accounting_check(t,a):
 assert a['substantive_attempt_limit']==5,'five-turn limit'
 assert a['substantive_attempts_used']==len(t),'counter ledger agreement'
 assert [x['turn'] for x in t]==list(range(1,len(t)+1)),'distinct contiguous turns'
 assert 0<=len(t)<=5,'bounded response budget'
 assert not a['full_closed_surface_resolution_claimed'] and not a['novel_result_claimed'],'unresolved original scope'
ledger=[]
def run(name,f):
 try:f();status='PASS';failure=None
 except Exception as e:status='REJECT';failure=type(e).__name__+': '+str(e)
 ledger.append({'case':name,'status':status,'failure':failure})
run('complete_literal_source_baseline',lambda:source_check(raw));run('reported_budget_baseline',lambda:accounting_check(turns,attempt))
p=copy.deepcopy(raw);p['statement']=p['statement'].replace('a closed geodesic','a simple closed geodesic');run('source_simple_reference_substitution',lambda:source_check(p))
p=copy.deepcopy(raw);p['id']=2764;run('source_wrong_numeric_identity',lambda:source_check(p))
a=copy.deepcopy(attempt);a['substantive_attempts_used']=0;run('accounting_reset_counter',lambda:accounting_check(turns,a))
t=copy.deepcopy(turns);t[1]['turn']=1;run('accounting_duplicate_turn',lambda:accounting_check(t,attempt))
t=copy.deepcopy(turns)
for k in range(3,7):t.append(dict(t[0],turn=k))
a=copy.deepcopy(attempt);a['substantive_attempts_used']=6;run('accounting_sixth_response',lambda:accounting_check(t,a))
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':ledger,'scope':'These controls prove consistency of the original authored two-turn ledger and reject source/budget corruption. They do not prove the native transcript contains no hidden proof turns. Shared current state/catalog/history omission is separately recorded; audit itself adds zero substantive proof responses.'}
(out/'SOURCE_ACCOUNTING_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
