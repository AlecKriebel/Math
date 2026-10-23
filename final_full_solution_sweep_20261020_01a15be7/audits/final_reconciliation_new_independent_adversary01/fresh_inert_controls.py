"""Fresh inert adversarial controls. No service/production authority is used."""
from pathlib import Path
import json,copy,hashlib,base64,collections
W=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/final_reconciliation_new_independent_adversary01')
p=W/'independent_checks.py';b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=='63f9f0d1cd4d8e8d87b3c087ce8db2535ef526db3f359e2df7f4c13ce550aa8a'
I={'__file__':str(p),'__name__':'_inert_independent_checks'};exec(compile(b,str(p),'exec'),I)
R=I['R'];J=I['J'];n=I['frozen_join']();need=I['need'];typed=I['typed'];C=I['C'];H=I['H']
s=I['strict']((R/'audits/prior_source_eleven_root_action01/AFTER_COMPLETE_SHEET.json').read_bytes())
results=[]
def check(name,fn,expect_reject):
 try:value=fn();observed_reject=False;err=None
 except Exception as e:value=None;observed_reject=True;err=repr(e)
 need(observed_reject is expect_reject,'Unexpected control result '+name)
 results.append({'inert_control':name,'expected_reject':expect_reject,'observed_reject':observed_reject,'error':err})
def alter(name,fn,helper_accept=False):
 x=copy.deepcopy(s);fn(x);check('strict_snapshot_'+name,lambda:I['strict_sheet'](x),True)
 if helper_accept:check('frozen_join_known_gap_'+name,lambda:n['validated_sheet'](x),False)
def target(x):return next(t['properties']for t in x['metadata']['sheets']if t['properties']['sheetId']==I['GID'])
def both_filter(x,key,v):
 for role in ['value_raw','formula_raw']:x[role]['valueRanges'][0]['dataFilters'][0]['gridRange'][key]=v
def both_value(x,key,v):
 for role in ['value_raw','formula_raw']:x[role]['valueRanges'][0]['valueRange'][key]=v
check('strict_dated252_full1178_positive',lambda:I['strict_sheet'](s),False)
alter('no_metadata_sheets',lambda x:x['metadata'].update(sheets=[]),True)
alter('wrong_metadata_target_title',lambda x:target(x).update(title='Wrong sheet'),True)
alter('wrong_metadata_target_columns4',lambda x:target(x)['gridProperties'].update(columnCount=4),True)
alter('truncated_full_allocated_filter252',lambda x:both_filter(x,'endRowIndex',252),True)
alter('wrong_A1_endpoint',lambda x:both_value(x,'range',"'Other'!A1:AQ1178"),True)
alter('wrong_major_dimension',lambda x:both_value(x,'majorDimension','COLUMNS'),True)
alter('numeric_gid_wrong',lambda x:both_filter(x,'sheetId',0))
alter('range_columns42',lambda x:both_filter(x,'endColumnIndex',42))
alter('range_startrow1',lambda x:both_filter(x,'startRowIndex',1))
alter('typed_startrow_false',lambda x:both_filter(x,'startRowIndex',False),True)
alter('wrong_metadata_book',lambda x:x['metadata'].update(spreadsheetId='wrong'))
alter('duplicate_target_metadata',lambda x:x['metadata']['sheets'].append(copy.deepcopy(x['metadata']['sheets'][-1])),True)
alter('VALUE_FORMULA_disagree',lambda x:x['formulas'][1].append('changed'))
alter('derived_raw_disagree',lambda x:x['values'][1].append('changed'))
details=I['strict_sheet'](s)
def fixture(role):
 if role in ['metadata_before','metadata_after']:
  argv=[I['GWS'],'sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':I['BOOK'],'includeGridData':False})];body=s['metadata']
 else:
  argv=[I['GWS'],'sheets','spreadsheets','values','batchGetByDataFilter','--params',json.dumps({'spreadsheetId':I['BOOK']}),'--json',json.dumps({'dataFilters':details['full_filter'],'majorDimension':'ROWS','valueRenderOption':'UNFORMATTED_VALUE'if role=='values'else'FORMULA'})];body=s['value_raw'if role=='values'else'formula_raw']
 return {'argv':argv,'returncode':0,'stdout_base64':base64.b64encode(C(body)).decode(),'stderr_base64':''}
for role in ['metadata_before','values','formulas','metadata_after']:check('inert_original_fullargv_positive_'+role,lambda role=role:I['raw_cli'](fixture(role),role,details),False)
def cli_attack(name,role,fn):
 e=fixture(role);fn(e);check('strict_native_'+name,lambda:I['raw_cli'](e,role,details),True)
cli_attack('wrong_binary','values',lambda e:e['argv'].__setitem__(0,'/wrong/gws'))
cli_attack('projected_fields_option','values',lambda e:e['argv'].extend(['--fields','valueRanges']))
cli_attack('returncode_nonzero','values',lambda e:e.update(returncode=1))
cli_attack('returncode_bool','values',lambda e:e.update(returncode=False))
cli_attack('stderr_missing','values',lambda e:e.pop('stderr_base64'))
cli_attack('stderr_not_base64','values',lambda e:e.update(stderr_base64='invalid%'))
cli_attack('truncated_numeric_request','values',lambda e:e['argv'].__setitem__(8,json.dumps({'dataFilters':[{'gridRange':{'sheetId':I['GID'],'startRowIndex':0,'endRowIndex':252,'startColumnIndex':0,'endColumnIndex':43}}],'majorDimension':'ROWS','valueRenderOption':'UNFORMATTED_VALUE'})))
cli_attack('wrong_mode','values',lambda e:e['argv'].__setitem__(8,json.dumps({'dataFilters':details['full_filter'],'majorDimension':'ROWS','valueRenderOption':'FORMULA'})))
cli_attack('extra_params_fields','metadata_before',lambda e:e['argv'].__setitem__(5,json.dumps({'spreadsheetId':I['BOOK'],'includeGridData':False,'fields':'spreadsheetId'})))
cli_attack('includeGridData_true','metadata_before',lambda e:e['argv'].__setitem__(5,json.dumps({'spreadsheetId':I['BOOK'],'includeGridData':True})))
cli_attack('duplicate_JSON_param','metadata_before',lambda e:e['argv'].__setitem__(5,'{"spreadsheetId":"'+I['BOOK']+'","spreadsheetId":"'+I['BOOK']+'","includeGridData":false}'))
cli_attack('duplicate_JSON_stdout','metadata_before',lambda e:e.update(stdout_base64=base64.b64encode(b'{"x":0,"x":0}').decode()))
cli_attack('nonfinite_JSON_stdout','metadata_before',lambda e:e.update(stdout_base64=base64.b64encode(b'{"x":NaN}').decode()))
# Whole future-overlay presence/claim logic: explicit INERT memory loader only.
# No fake ROOT/receipt/authority file is created. No completion outcome is supplied.
v=n['baseline']();full=n['frozen_prior_nodes']()
nodes={k:{a:q.get(a)for a in ['number','title','body','head','state','draft','merged_at','merge_commit_sha']}for k,q in full.items()}
for q in nodes.values():q['head']={'sha':q['head']['sha']}
original_objpin=n['objpin'];registry={};counter=[0]
def mp(obj):
 counter[0]+=1;key='INERT_MEMORY_FIXTURE:'+str(counter[0]);registry[key]=copy.deepcopy(obj)
 return {'path':key,'bytes':len(C(obj)),'sha256':H(C(obj))}
def model_objpin(pin):
 if pin['path'].startswith('INERT_MEMORY_FIXTURE:'):
  obj=registry[pin['path']];need(pin['bytes']==len(C(obj))and pin['sha256']==H(C(obj)),'Inert model pin');return copy.deepcopy(obj)
 return original_objpin(pin)
n['objpin']=model_objpin
def env(obj,url):return {'method':'GET','url':url,'status':200,'raw_body_base64':base64.b64encode(C(obj)).decode(),'raw_sha256':H(C(obj))}
def model_payload(modify=None):
 registry.clear();counter[0]=0;d=copy.deepcopy(nodes);x=copy.deepcopy(s)
 if modify:modify(d,x)
 pages=[];a=[d[k]for k in sorted(d)]
 for start in range(0,len(a),100):pages.append(mp(env(a[start:start+100],'https://api.github.com/repos/AlecKriebel/Math/pulls?state=all&sort=created&direction=asc&per_page=100&page='+str(len(pages)+1))))
 pages.append(mp(env([],'https://api.github.com/repos/AlecKriebel/Math/pulls?state=all&sort=created&direction=asc&per_page=100&page='+str(len(pages)+1))))
 newest=mp(env([d[max(d)]],'https://api.github.com/repos/AlecKriebel/Math/pulls?state=all&sort=created&direction=desc&per_page=1'))
 originals={}
 for role,key in [('metadata_before','metadata'),('values','value_raw'),('formulas','formula_raw'),('metadata_after','metadata')]:
  originals[role]=mp({'returncode':0,'stdout_base64':base64.b64encode(C(x[key])).decode()})
 return {'final_inventory':{'pages':pages,'newest':newest,'observed_at':'INERT_NOT_AN_ACTUAL_TIME'},'final_ledger':{'snapshot':mp(x),'original_transports':originals,'observed_at':'INERT_NOT_AN_ACTUAL_TIME'}}
def apply(p):
 root=mp({'kind':'ROOT_ADOPTED_FINAL_JOIN_OVERLAY','all_native_receipts_reviewed':True,'payload_sha256':H(C(p))})
 return n['apply_overlay'](v,mp({'schema':'root-adopted-final-join-overlay-v1','payload':p,'root_adoption':root}))
p=model_payload();r=apply(p);need(r['final_observations_current']is True and r['final_reconciliation_requirements_satisfied']is False and r['pending_family_count']==34,'Inert presence world/pending state')
results.append({'inert_control':'whole_overlay_consistent_but_actual_outcomes_pending','observed_requirements_satisfied':False,'actual_completion_claimed':False})
for name,mut in [('changed_head',lambda d,x:d[415]['head'].update(sha='0'*40)),('changed_body',lambda d,x:d[415].update(body=d[415]['body']+' INERT CHANGE')),('changed_title',lambda d,x:d[415].update(title='INERT CHANGED TITLE')),('unconfirmed_missing_number',lambda d,x:d.pop(415))]:
 p=model_payload(mut);r=apply(p);need(r['final_observations_current']is False and any(z['pr']==415 for z in r['unresolved_new_changed_or_gap_claims']),name+' must remain unresolved');results.append({'inert_control':'whole_overlay_'+name,'coverage_unresolved':True})
p=model_payload();p['final_inventory']['pages'].pop();check('whole_overlay_missing_terminal',lambda:apply(p),True)
p=model_payload();p['final_inventory']['pages'][1]=p['final_inventory']['pages'][0];check('whole_overlay_duplicate_page',lambda:apply(p),True)
p=model_payload();reg=registry[p['final_inventory']['newest']['path']];reg['raw_body_base64']=base64.b64encode(C([nodes[1445]])).decode();reg['raw_sha256']=H(C([nodes[1445]]));p['final_inventory']['newest']=mp(reg);check('whole_overlay_highest_mismatch',lambda:apply(p),True)
for name,mut in [('changed_original252_prefix',lambda d,x:x['values'][1].append('INERT PREFIX CHANGE')),('duplicate_existing_DOI',lambda d,x:x['values'].append(copy.deepcopy(x['values'][173])))]:
 def consistent(d,x,mut=mut):
  mut(d,x);x['formulas']=copy.deepcopy(x['values'])
  for key in ['value_raw','formula_raw']:x[key]['valueRanges'][0]['valueRange']['values']=copy.deepcopy(x['values'])
 p=model_payload(consistent);check('whole_overlay_'+name,lambda:apply(p),True)
print(json.dumps({'status':'PASS_FRESH_INERT_CONTROLS_WITH_KNOWN_JOIN_INGRESS_LIMITATIONS','count':len(results),'results':results,'actual_service_effects':0,'actual_final_inputs_tested':False,'actual_completion_outcome_or_authority_files_created':False,'no_mathematical_reproof':True},indent=2,sort_keys=True))
