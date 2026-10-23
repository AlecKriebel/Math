"""Read-only independently pinned actual34 outcome audit. Never calls service or bridge."""
from pathlib import Path
import json,hashlib,base64,gzip,lzma,datetime
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
W=R/'audits/final_reconciliation_new_independent_adversary01'
def load(p,h):
 b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==h
 n={'__file__':str(p),'__name__':'_independent_actual34_'+p.stem};exec(compile(b,str(p),'exec',optimize=0),n);return n
I=load(W/'independent_checks.py','63f9f0d1cd4d8e8d87b3c087ce8db2535ef526db3f359e2df7f4c13ce550aa8a')
J=load(R/'audits/final_reconciliation_join_preparation01/join_readonly.py','612b8e085f388e133e94a4c87cc3514e69d0f2931cec5999809f80d7ffaf0b1d')
H=I['H'];C=I['C'];typed=I['typed'];objpin=I['objpin'];strict=I['strict']
PINS={}
def read(p,h=None):
 b=p.read_bytes();assert h is None or H(b)==h
 pin={'path':str(p),'bytes':len(b),'sha256':H(b)};PINS[str(p)]=pin
 return objpin(pin)
def raw(p,h=None):
 b=p.read_bytes();assert h is None or H(b)==h
 PINS[str(p)]={'path':str(p),'bytes':len(b),'sha256':H(b)}
 return b
def dt(s):
 t=datetime.datetime.fromisoformat(s);assert t.tzinfo is not None and t.utcoffset()==datetime.timedelta(0);return t
def main():
 receipt=read(R/'EXISTING_PUBLICATION_REMAINING34_RECONCILIATION.json','3679737af83a029468e82aa4ef91d2ab030b22db88c47d69049d5f5872f0035a')
 J['verify_closed']('620f22164fe099650f31196258b55ab21fc52b8da0c6a8c0912c875fe2816417')
 baseline=J['baseline']();families=baseline['pending_family_obligations']
 assert receipt['complete']is True and receipt['new_publications']==0 and receipt['old_rows']==252 and receipt['new_rows']==34 and receipt['after_rows']==286
 assert receipt['one_native_append_attempt']is True and type(receipt['native_append_popen_count'])is int and receipt['native_append_popen_count']==1
 assert receipt['all_old252_rows_all43_columns_raw_metadata_and_formula_views_preserved']is True
 assert all(type(x)is bool and x for x in receipt['required_native_checks'].values())and len(receipt['required_native_checks'])==7
 assert typed(receipt['exact_rows'],receipt['records'])and typed(receipt['exact_rows'],receipt['rows'])
 for k in ['native_transport','actual_final_protocol_TOP','original_stdout','original_stderr','original_CASE_GET_only_native','postchecks','before_snapshot','after_snapshot']:
  p=receipt[k];raw(Path(p['path']),p['sha256']);assert Path(p['path']).stat().st_size==p['bytes']
 before=objpin(receipt['before_snapshot']);after=objpin(receipt['after_snapshot'])
 bd=I['strict_sheet'](before);ad=I['strict_sheet'](after)
 assert bd['rows']==252 and ad['rows']==286 and typed(before['metadata'],after['metadata'])
 assert typed(after['values'][:252],before['values'])and typed(after['formulas'][:252],before['formulas'])
 inp=strict(lzma.decompress((J['D']/'private/LOCAL_ORIGINAL_INPUTS.json.xz').read_bytes()))
 historical=objpin(next(p for p in inp['external_pins']if p['path'].endswith('/AFTER_COMPLETE_SHEET.json')))
 assert typed(before,historical)
 rows=receipt['exact_rows'];assert len(rows)==34 and len({v['family_pr']for v in rows})==34
 assert {v['family_pr']for v in rows}=={v['family_pr']for v in families}
 by={v['family_pr']:v for v in rows};summary=[];selected=[]
 for lr,f in enumerate(families,253):
  v=by[f['family_pr']];lit=f['literal_four_cells'];assert v['pr']==v['family_pr']==f['family_pr']
  assert type(v['ledger_row'])is int and v['ledger_row']==lr and v['associated_prs']==f['associated_prs']
  assert typed(v['cells'],lit)and v['literal_four_cells_sha256']==f['literal_four_cells_sha256']==H(C(lit))
  assert typed(after['values'][lr-1],lit)and typed(after['formulas'][lr-1],lit)
  assert sum(typed(x[:4],lit)for x in after['values'])==1
  if f['selected_C_DOI']:
   assert J['one_doi'](after['values'],f['selected_C_DOI'])==lr;selected.append(f['selected_C_DOI'])
  else:assert lit[2]==''and f['family_pr']in{1292,1310,1312}
  summary.append({'family_pr':f['family_pr'],'associated_prs':f['associated_prs'],'row':lr,'literal_sha256':H(C(lit))})
 assert len(selected)==31 and len(set(selected))==31 and sum(len(x['associated_prs'])for x in rows)==35
 allc=[J['norm'](x[2])for x in after['values'][1:]if len(x)>2 and x[2]]
 assert len(allc)==len(set(allc))==271
 case=Path(receipt['original_fixed_CASE']);assert case==R/'audits/existing_publication_remaining34_action01'
 d=R/'audits/root_remaining34_source08_actual_execute01'
 top=objpin(receipt['actual_final_protocol_TOP']);native=objpin(receipt['native_transport'])
 assert native['returncode']==0 and native['error']is None and native['stderr_base64']==''
 assert base64.b64decode(native['stdout_base64'],validate=True)==raw(Path(receipt['original_stdout']['path']),receipt['original_stdout']['sha256'])
 assert base64.b64decode(native['stderr_base64'],validate=True)==raw(Path(receipt['original_stderr']['path']),receipt['original_stderr']['sha256'])==b''
 lines=[strict(x)for x in base64.b64decode(native['stdout_base64'],validate=True).splitlines()]
 assert len(lines)==2 and typed(lines[0],top)and typed(lines[1]['result'],top)and lines[1]['error']is None and lines[1]['native_append_popen_count']==1
 assert top=={'status':'VERIFIED_EXACT_ONE_ATOMIC_EXISTING_PUBLICATION_BATCH','new_rows':34,'new_publications':0,'attempts':1,'old43_rows_preserved':252,'after_rows':286,'unknown_reply_get_reconciled':False,'action_authority':False}
 driver=Path(native['caller_source_path']);raw(driver,native['caller_source_sha256']);assert native['caller_source_bytes']==driver.stat().st_size
 assert native['caller_source_sha256']=='f1348a19a8569eec10d04cb0046ed9932c8f797bcfbe1ba25a11ffe951d304d7'
 outcome=read(d/'OUTCOME.json','e4e687858e834f8354edfa4c1b4fdc2c602a30fccbbcedd12be1fa6a2d653d9b')
 assert outcome['error']is None and outcome['native_append_popen_count']==1 and outcome['CASE_exists']is True and typed(outcome['result'],top)
 post=objpin(receipt['postchecks']);assert typed(post['result'],top)and post['native_append_popen_count']==1
 assert all(post[k]is True for k in['all_expected_journal_buffers_exact','source_reverified','four_authority_rawpins_reverified'])
 service=read(case/'SERVICE_OUTCOME.json','44773c44b1b53896e7cc36b289813e6bc3c26275ebddec1a2e13388ca8dbab4c')
 assert service=={'exact_prefix_plus_batch_observed':True,'known_response':True,'contradictory_response':False,'attempts':1}
 transport=read(case/'ORIGINAL_APPEND_TRANSPORT.json','2f6b19a4eadfb12dfcbd65e754318c2bc8b75d9d9820af82657ff16c7e77061c')
 assert transport['returncode']==0 and transport['transport_error']is None
 response=strict(base64.b64decode(transport['stdout_base64'],validate=True))
 assert response['spreadsheetId']==I['BOOK']and response['replies']==[{}]
 base64.b64decode(transport['stderr_base64'],validate=True)
 edge=read(d/'SOLE_NATIVE_WRITE_POPEN_EDGE.json','2575b8da780c51b4dd8e8d57c4c043d966b1f458cda418a07d2b8e655a51d6f3')
 request={'requests':[{'appendCells':{'sheetId':1254632077,'rows':[{'values':[{'userEnteredValue':{'stringValue':c}}for c in f['literal_four_cells']]}for f in families],'fields':'userEnteredValue'}}]}
 av=edge['argv'];assert len(av)==8 and av[:5]==[I['GWS'],'sheets','spreadsheets','batchUpdate','--params']and av[6]=='--json'
 assert typed(strict(av[5]),{'spreadsheetId':I['BOOK']})and typed(strict(av[7]),request)
 marker=read(case/'WRITE_ATTEMPTED.json','8b4593466d1e5f88faf958ff143fae954c4322f802a84128e3a6cc01ca089ec4')
 assert marker['attempt']==edge['ordinal']==1 and marker['request_sha256']==edge['request_canonical_sha256']==H(C(request))
 authority=read(d/'FOUR_AUTHORITY_RAW_PINS.json','37fb51a06a8768019db14b003cc56318175827fec81f79f3426fd1048d6d00fd')
 auth=R/'audits/existing_publication_remaining34_authority01'
 names={'gate':'REVIEWED_GATE.json','root':'ROOT_ACTION_APPROVAL.json','independent':'INDEPENDENT_ACTION_REVIEW.json','activation':'ACTIVATION.json'}
 roles={k:read(auth/name,authority['pins'][k])for k,name in names.items()}
 assert roles['root']['accepted']is True and roles['independent']['accepted']is True and roles['activation']['ready_for_execution']is True
 assert all(x['source_manifest_sha256']==receipt['source_manifest_sha256']for x in roles.values()if 'source_manifest_sha256'in x)
 assert roles['root']['approved_semantic_keys']==roles['independent']['approved_semantic_keys']and len(roles['root']['approved_semantic_keys'])==4924
 assert all(x['fixed_samecase']==str(case)and x['row_count']==34 and x['new_publications']==0 and x['native_write_attempt_limit']==1 and dt(x['valid_until_utc'])>dt(edge['at'])for k,x in roles.items()if k!='gate')
 adp=read(Path(roles['root']['root_final_review_adoption_path']),roles['root']['root_final_review_adoption_sha256'])
 assert adp['accepted_for_action']is True and adp['unresolved']==[]and adp['source_manifest_sha256']==receipt['source_manifest_sha256']
 readback=objpin(receipt['original_CASE_GET_only_native'])
 assert readback['returncode']==0 and readback['transport_error']is None and readback['no_service_writes']is True and readback['original_fixed_CASE_only']is True
 rb=strict(base64.b64decode(readback['stdout_base64'],validate=True));assert rb['status']=='GET_ONLY_ORIGINAL_OUTCOME_RECONCILIATION'and rb['writes']==0 and rb['can_retry']is False and rb['approval_inferred']is False and rb['exact_own_positions']==list(range(253,287))
 assert dt(native['before'])<=dt(outcome['before'])<dt(edge['at'])<=dt(outcome['after'])<=dt(native['after'])<=dt(readback['before'])<=dt(readback['after'])<=dt(receipt['at'])
 # Readback originals retain actual provider argument vectors without executable/timestamps.
 # Compare those vectors directly; do not relabel them as timed full-argv originals.
 cap=R/'audits/existing_publication_remaining34_readonly_observations/read_04acb48d27d34787960dd75cc20d23db'
 roles4=['metadata_before','values','formulas','metadata_after'];derived={}
 for i,role in enumerate(roles4):
  p=cap/(str(i).zfill(5)+'_numeric_raw.json.gz');v=read(p)
  assert v['returncode']==0 and v['transport_error']is None and type(v['args'])is list
  expected=([I['GWS'],'sheets','spreadsheets','get','--params']+[json.dumps({'spreadsheetId':I['BOOK'],'includeGridData':False})]if i in[0,3]else[I['GWS'],'sheets','spreadsheets','values','batchGetByDataFilter','--params',json.dumps({'spreadsheetId':I['BOOK']}),'--json',json.dumps({'dataFilters':ad['full_filter'],'majorDimension':'ROWS','valueRenderOption':'UNFORMATTED_VALUE'if i==1 else'FORMULA'})])
  assert v['args'][:-1]==expected[1:-1]and typed(strict(v['args'][-1]),strict(expected[-1]))
  base64.b64decode(v['stderr_base64'],validate=True);derived[role]=strict(base64.b64decode(v['stdout_base64'],validate=True))
 assert typed(derived['metadata_before'],derived['metadata_after'])and typed(derived['metadata_before'],after['metadata'])
 assert typed(derived['values'],after['value_raw'])and typed(derived['formulas'],after['formula_raw'])
 return {'status':'PASS_INDEPENDENT_ACTUAL34_EXACT_MAPPING_NATIVE_APPEND_AND_READBACK','family_count':34,'associated_PR_count':35,'new_publications':0,'native_append_attempts':1,'sheet_rows':286,'new_existing_source_rows_cumulative':100,'actual_new_papers_still13':True,'selected_unique_DOIs':31,'source_only_blank_C_families':[1292,1310,1312],'complete_typed252_prefix_preserved':True,'all286_nonempty_C_values_unique':len(allc),'families':summary,'observation_interval':{'before':native['before'],'append_edge':edge['at'],'actual_parent_after':native['after'],'GET_only_after':readback['after']},'readback_transport_qualification':'Original provider argument vectors, rc and raw streams verified; those captures omit executable and timestamps. Four distinct timed full-argv final originals remain independently required.','external_inputs':list(PINS.values()),'no_service_calls_or_effects':True,'final_clearance':False,'remaining_gap':'PR1131 actual publication and final authentic inventory/numeric43/QUEUE-parent reconciliation'}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False))
