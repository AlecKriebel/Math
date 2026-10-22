#!/usr/bin/env python3
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
import hashlib,importlib.util,json,socket,subprocess,sys,tempfile
O=Path(__file__).resolve().parent;A=O.parents[1];R=A.parents[1];W=R/'private/pr0280_package05';H=W/'operations'/('optimized' if sys.flags.optimize else 'normal')/'994';sys.path.insert(0,str(H));import controls_support as S;S.AUDIT=A
B,P,G,V,D=S.implementation(False)
results=[];attacks=[]
def ck(v,m):
 if not v:raise RuntimeError(m)
def reject(call):
 try:call()
 except RuntimeError as e:return str(e)
 raise RuntimeError('Expected rejection did not occur')
aliases=['https://ZENODO.ORG.:00443/record/./000999/export/json?x=1#files','https://zenodo.org/records/0001/../000999/versions/all','https://www.zenodo.org:443/%72ecord/%30%30%39%39%39/export/json','(https://zenodo.org/records/999/export/json),','https://zenodo.org/api//records/./000999/files/paper.pdf?download=1','//zenodo.org.:0443//records/999/unknown/future','HTTPS://ZENODO.ORG/records/999/#view','zenodo.org:443/api/records/999/export/json']
with ExitStack() as guards:
 guards.enter_context(patch.object(subprocess,'run',S.forbidden));guards.enter_context(patch.object(socket,'socket',S.forbidden));guards.enter_context(patch.object(V,'urlopen',S.forbidden))
 for n in ['request','create','upload','update','publish','get']:guards.enter_context(patch.object(B.zenodo.ZenodoClient,n,S.forbidden))
 with tempfile.TemporaryDirectory(dir=W,prefix='own_ops_') as tmp:
  root=Path(tmp)
  for alias in aliases:
   ck(B.target_in_row([alias],999),'own scalar new combination')
   for col in range(4):
    for ex in [False,True]:
     row=['','','',''];row[col]=alias;x=S.run_pipeline(root/str(len(results)),(B,P,G,V,D),[row],True,ex)
     ck(x['collector_matching_rows']==1 and not x['gate_accepted'] and x['append_calls']==0,'own alias pipeline rejection');results.append({'alias':alias,'column':col+1,'exemption':ex,**x})
  sample='OWR-14218-004 / problem 30003060: Solotar, Koszul Calculus, OWR 10/2016 pp.479–481. https://doi.org/10.4171/OWR/2016/10'
  ledgerpath=R/'private/record_route_retrospective/ledger.json';raw=ledgerpath.read_bytes();ck(hashlib.sha256(raw).hexdigest()=='d513b4cfef1ca47f654a6f677693ae7186f3f193f6d892c5e043ad318c0061b3','actual cached sheet hash');sheet=json.loads(raw);rows=B.schema_rows(sheet);ck(len(rows)==176 and rows[95][0]==sample,'actual row96')
  parsed=[]
  for i,row in enumerate(rows,1):
   try:B.row_identity_leads(row)
   except RuntimeError as e:parsed.append({'row':i,'reason':str(e)})
  ck(parsed==[{'row':96,'reason':'Unresolved DOI/URL encoding requires root identity review'}],'single actual obstruction')
  work=root/'whole_actual_cached_sheet';work.mkdir();reads=[];client=[]
  def read_whole(args):reads.append(args);return sheet
  def client_whole(*a):client.append(True);raise RuntimeError('UNEXPECTED progressed past whole-sheet parser')
  with patch.object(P,'PRIVATE',work),patch.object(P,'ROOT',work),patch.object(P,'REPO',work),patch.object(P,'verify_destination',lambda:True),patch.object(P,'read_command',read_whole),patch.object(P.zenodo,'token_for',lambda *a:'synthetic'),patch.object(P.zenodo,'ZenodoClient',client_whole):reason=reject(lambda:P.gather('before_integration','a'*40,None))
  ck(len(reads)==1 and not client and reason.startswith('Unresolved DOI'),'actual whole cached sheet fails before account collection');attacks.append({'layer':'actual_gather_complete_cached176rows','failure':reason,'further_provider_calls':0})
  for col in range(4):
   row=['','','',''];row[col]=sample
   work=root/('gate_bibliographic_'+str(col));work.mkdir();S.write(work/'account_complete.json',{'total':0,'records':[]})
   S.write(work/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',{'pr':280,'root_identity_reconciliation_complete':True,'unresolved_leads':[],'release_manifest_sha256':B.RELEASE_SHA,'account_leads':[],'unrelated_local_state_exemptions':[],'ledger_leads':[{'values_sha256':B.digest(row),'disposition':'distinct_non_target'}]})
   gate={'started_utc':B.stamp(),'completed_utc':B.stamp(),'phase':'before_integration','expected_pr_head':'a'*40,'expected_deposit_id':None,'read_only':True,'release_manifest_sha256':B.RELEASE_SHA,'release_files':B.release()['files'],'account_positive_control':'PASS_23174283','raw_receipts':str(work),'receipt':str(work/'gate.json'),'account_complete_sha256':B.sha((work/'account_complete.json').read_bytes()),'account_complete_total':0,'unexpected_account_matches':[],'ledger_matches':[{'row':2,'values':row}],'local_deposit_state_matches':[]};S.write(work/'gate.json',gate)
   with patch.object(G,'AUDIT',work):reason=reject(lambda:G.reconcile(gate,'before_integration','a'*40,None))
   ck(reason.startswith('Unresolved DOI'),'actual reconciliation cannot apply exact digest exemption');attacks.append({'layer':'actual_reconcile','column':col+1,'failure':reason,'exact_non_target_digest_cannot_resolve':True})
   for target in [None,999]:
    work=root/('bibliographic_'+str(col)+'_'+str(target));work.mkdir();reads=[];client=[]
    def read(args):reads.append(args);return {'values':[B.HEADERS,row]}
    def client_ctor(*a):client.append(True);raise RuntimeError('UNEXPECTED progressed past parser')
    with patch.object(P,'PRIVATE',work),patch.object(P,'ROOT',work),patch.object(P,'REPO',work),patch.object(P,'verify_destination',lambda:True),patch.object(P,'read_command',read),patch.object(P.zenodo,'token_for',lambda *a:'synthetic'),patch.object(P.zenodo,'ZenodoClient',client_ctor):reason=reject(lambda:P.gather('before_integration','a'*40,target))
    ck(len(reads)==1 and not client and reason.startswith('Unresolved DOI'),'preallocation block')
    attacks.append({'layer':'actual_gather','column':col+1,'target':target,'failure':reason,'further_provider_calls':0})
   # Independent append protection cannot be waived by a trusted row digest.
   work=root/('append_bibliographic_'+str(col));work.mkdir();before=[B.HEADERS,row];appends=[];S.write(work/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',{'ledger_leads':[{'values_sha256':B.digest(row),'disposition':'distinct_non_target'}]});S.write(work/'ZENODO_PUBLIC_FILE_VERIFICATION.json',{'synthetic':True})
   gate={'started_utc':B.stamp(),'ledger_sha256':B.digest(before),'receipt':str(work/'gate.json')};public={'record':999,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200},'release_manifest_sha256':B.RELEASE_SHA}
   with patch.object(D,'AUDIT',work),patch.object(D,'require_release_clearance',lambda:True),patch.object(D,'verify_live',lambda *a:public),patch.object(D,'collect',lambda *a,**k:(gate,{})),patch.object(D,'read',lambda *a:before),patch.object(D,'gws',lambda *a:appends.append(a)):reason=reject(lambda:D.append_verified('a'*40,999))
   ck(not appends and reason.startswith('Unresolved DOI'),'independent append false block');attacks.append({'layer':'actual_append_with_upstream_bypassed','column':col+1,'failure':reason,'append_calls':0,'exact_non_target_digest_cannot_resolve':True})
  reason=reject(B.require_release_clearance);ck('clearance' in reason.lower(),'suspended clearance fails closed')
  attacks.append({'layer':'actual_root_clearance','failure':reason})
ck(not S.ATTEMPTS,'no actual provider attempts')
out={'optimization':sys.flags.optimize,'new_alias_pipeline_cases':len(results),'aliases':results,'actual_cached_sheet_rows':176,'actual_cached_sheet_sha256':hashlib.sha256(raw).hexdigest(),'actual_row_parse_failures':parsed,'independent_falseblock_reproductions':attacks,'actual_provider_attempts':len(S.ATTEMPTS),'finding':'P280-OPS-05','minimal_failure_cell':sample,'scope':'Actual canonical functions, provider boundaries synthetic; cached actual full-sheet lexical compatibility checked, not a fresh live gate.'}
(O/('INDEPENDENT_OPERATIONS_OPTIMIZED.json' if sys.flags.optimize else 'INDEPENDENT_OPERATIONS.json')).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'new_pipeline_cases':len(results),'falseblock_cases':len(attacks),'real_provider_attempts':len(S.ATTEMPTS)}))
