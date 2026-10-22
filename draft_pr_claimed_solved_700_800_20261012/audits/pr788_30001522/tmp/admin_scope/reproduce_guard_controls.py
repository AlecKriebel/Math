"""Reproduce 2 positive/21 negative eligibility guard controls without network or writes."""
from pathlib import Path
import ast,copy,hashlib,json,sys,types
W=Path(__file__).resolve().parent
s=(W/'PUBLICATION_DRIVER_REPAIRED_SNAPSHOT.py').read_text()
assert hashlib.sha256(s.encode()).hexdigest()=='6c59308d34c38654550348e4d91aba8f38f960aed300359bca84530aac3bc102'
node=[n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)and n.name=='fresh_eligibility']
assert len(node)==1
module=ast.Module(body=node,type_ignores=[]);ast.fix_missing_locations(module)
r=json.loads((W/'ELIGIBILITY_INDEPENDENT_READ.json').read_text());g=json.loads((W/'FINAL_READINESS_PREPUBLICATION_SNAPSHOT.json').read_text());base=r['rows']['original_parent']['row'];cand=r['rows']['candidate']['row']
GOOD={'pr':r['pr'],'candidate':cand,'main':base,'acceptance':False,'catalog':[{'id':'30001522','statement_hash':g['statement_hash'],'review_hash':g['review_hash']}]}
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def test(case):
 class Remote:
  def __init__(self,head):self.head=head
  def entry(self,path):return {}if case['acceptance']else None
  def read(self,path):
   if path.endswith('QUEUE.md'):return case['main']if self.head=='main'else case['candidate']
   if path.endswith('catalog.json'):return json.dumps(case['catalog'])
   raise RuntimeError('unplanned read')
 fake=types.ModuleType('graphql_scoped_commit');fake.get_pr=lambda n:copy.deepcopy(case['pr']);fake.Remote=Remote;fake.head_oid=lambda:'main';sys.modules['graphql_scoped_commit']=fake
 ns={'sys':sys,'D':W,'U':W/'scratch','need':need,'json':json,'save':lambda p,v:None,'now':lambda:'MOCK_CONTROL'};exec(compile(module,'exact_guard_AST','exec'),ns)
 try:ns['fresh_eligibility'](copy.deepcopy(g));return {'accepted':True}
 except Exception as e:return {'accepted':False,'error':str(e)}
controls=[]
def add(name,change,expected):
 c=copy.deepcopy(GOOD);change(c);a=test(c)
 if a['accepted']!=expected:raise RuntimeError('Control failed: '+name)
 controls.append({'name':name,'expected_accept':expected,**a})
add('exact original-parent queued0/5 baseline accepted',lambda c:None,True)
add('exact reviewed claimed2/5 candidate on main accepted',lambda c:c.update(main=cand),True)
for status in ['queued','unsolved','already_solved','in_progress','published','claimed_Solved']:
 add('candidate status '+status,lambda c,s=status:c.update(candidate=cand.replace('| claimed_solved |','| '+s+' |')),False)
add('changed candidate head',lambda c:c['pr']['head'].update(sha='0'*40),False)
add('closed candidate',lambda c:c['pr'].update(state='closed'),False)
add('already merged',lambda c:c['pr'].update(merged=True),False)
add('native acceptance already present',lambda c:c.update(acceptance=True),False)
add('changed queued budget',lambda c:c.update(main=base.replace('| 0/5 |','| 1/5 |')),False)
add('changed queued note',lambda c:c.update(main=base+' changed'),False)
add('main unsolved instead of exact baseline',lambda c:c.update(main=base.replace('| queued |','| unsolved |')),False)
add('main already_solved instead of exact baseline',lambda c:c.update(main=base.replace('| queued |','| already_solved |')),False)
add('main claimed with different budget',lambda c:c.update(main=cand.replace('| 2/5 |','| 3/5 |')),False)
add('duplicate candidate rows',lambda c:c.update(candidate=cand+'\n'+cand),False)
add('duplicate main rows',lambda c:c.update(main=base+'\n'+base),False)
add('main own source record missing',lambda c:c.update(catalog=[]),False)
add('main own source record duplicated',lambda c:c['catalog'].append(copy.deepcopy(c['catalog'][0])),False)
add('main statement identity changed',lambda c:c['catalog'][0].update(statement_hash='0'*64),False)
add('main review identity changed',lambda c:c['catalog'][0].update(review_hash='0'*64),False)
expected=json.loads((W/'GUARD_CONTROL_RESULTS.json').read_text())['controls']
if controls!=expected:raise RuntimeError('Results differ from sealed guard receipt')
print(json.dumps({'result':'PASS','positive_controls':2,'negative_controls':21,'no_network_or_writes':True}))
