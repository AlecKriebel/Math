from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
from urllib.parse import urlparse,parse_qs
import sys,json,copy,subprocess,tempfile
R=Path(__file__).resolve().parent;A=R.parents[1];E=A.parents[1];PVT=E/'private/pr0280_package_adversary_03'
sys.path.insert(0,str(A))
import ops_binding as B, prepublication_check as P, publication_live_gates as G, record_publication_ledger as D, verify_published_files as V
RESULT=[];FORBIDDEN=[]
def req(v,m):
 if not v:raise RuntimeError(m)
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v)+'\n')
def forbidden(*a,**k):FORBIDDEN.append(True);raise RuntimeError('REAL PROVIDER FORBIDDEN')
def recon():return {'pr':280,'root_identity_reconciliation_complete':True,'unresolved_leads':[],'release_manifest_sha256':B.RELEASE_SHA,'account_leads':[],'ledger_leads':[]}
def fixture(root,rows):
 rec={'id':999,'metadata':{'title':B.TITLE},'files':[]};write(root/'account_complete.json',{'total':1,'records':[rec]})
 g={'started_utc':B.stamp(),'completed_utc':B.stamp(),'phase':'before_ledger','expected_pr_head':'a'*40,'expected_deposit_id':999,'read_only':True,'release_manifest_sha256':B.RELEASE_SHA,'release_files':B.release()['files'],'account_positive_control':'PASS_23174283','raw_receipts':str(root),'receipt':str(root/'gate.json'),'account_complete_sha256':B.sha((root/'account_complete.json').read_bytes()),'account_complete_total':1,'unexpected_account_matches':[],'ledger_matches':[],'local_deposit_state_matches':[],'ledger_sha256':B.digest(rows)}
 write(root/'gate.json',g);write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',recon());return g

def full_chain(root,existing,label,expect_reject):
 rows=[B.HEADERS,existing];write(root/'raw/pr0280/ledger_live.json',{'values':rows})
 full={'id':999,'metadata':{'title':B.TITLE},'files':[]}
 class Client:
  base='https://synthetic.invalid'
  def __init__(self,*a):pass
  def request(self,method,url):
   q=parse_qs(urlparse(url).query).get('q',[''])[0]
   records=[{'id':23174283,'metadata':{},'files':[]}] if q=='Fibonacci' else ([full] if not q else [])
   return {'hits':{'total':len(records),'hits':records},'links':{}}
 def readcmd(args):
  if args[0]=='gws':return {'values':rows}
  if 'pulls/280' in args[-1]:return {'number':280,'head':{'sha':'a'*40,'repo':{'full_name':'AlecKriebel/Math'}},'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}},'state':'closed','merged':True,'draft':False}
  return {'object':{'sha':'b'*40}}
 write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',recon())
 with patch.object(P,'ROOT',root),patch.object(P,'PRIVATE',root/'collector_private'),patch.object(P,'REPO',root),patch.object(P,'verify_destination',lambda:True),patch.object(P,'read_command',readcmd),patch.object(B.zenodo,'ZenodoClient',Client),patch.object(B.zenodo,'token_for',lambda e:'synthetic'):
  g=P.gather('before_ledger','a'*40,999)
 gate_ok=False;gate_error=None
 try:
  with patch.object(G,'AUDIT',root):acc=G.reconcile(g,'before_ledger','a'*40,999,True)
  gate_ok=True
 except Exception as ex:gate_error=str(ex)
 desired=D.desired_row(999);after=rows+[desired];appends=[];readseq=iter([rows,after])
 write(root/'ZENODO_PUBLIC_FILE_VERIFICATION.json',{'synthetic':True})
 public={'record':999,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200},'release_manifest_sha256':B.RELEASE_SHA}
 def append(*args):
  req((root/'LEDGER_APPEND_INTENT.json').exists(),'intent before append');appends.append(args)
  return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':[desired]}}}
 append_ok=False;append_error=None
 try:
  # Exercise append's own independent predicate even when the upstream gate is rejected.
  with patch.object(D,'AUDIT',root),patch.object(D,'require_release_clearance',lambda:True),patch.object(D,'verify_live',lambda i:public),patch.object(D,'collect',lambda *a,**k:(g,{})),patch.object(D,'read',lambda *a:next(readseq)),patch.object(D,'gws',append):
   receipt=D.append_verified('a'*40,999)
  append_ok=True
 except Exception as ex:append_error=str(ex)
 semantic_count=sum('10.5281/zenodo.999' in ' '.join(row).lower() for row in after)
 out={'case':label,'collector_ledger_matches':len(g['ledger_matches']),'gate_accepted':gate_ok,'gate_error':gate_error,'actual_append_function_accepted':append_ok,'append_error':append_error,'synthetic_append_calls':len(appends),'semantic_casefold_DOI_rows_after_synthetic_append':semantic_count,'existing_row':existing}
 RESULT.append(out)
 if expect_reject:req(not append_ok and not appends,'canonical negative control')
 else:req(gate_ok and append_ok and len(appends)==1 and semantic_count==2,'new duplicate mechanism not reproduced')
with ExitStack() as guards:
 guards.enter_context(patch.object(subprocess,'run',forbidden));guards.enter_context(patch.object(V,'urlopen',forbidden))
 for method in ['request','create','upload','update','publish','get']:guards.enter_context(patch.object(B.zenodo.ZenodoClient,method,forbidden))
 with tempfile.TemporaryDirectory(dir=PVT,prefix='ops_independent_') as td:
  work=Path(td)
  fixtures=[('upper_suffix_DOI_column',['Unrelated wording','','https://doi.org/10.5281/ZENODO.999',''],False),('mixed_case_DOI_only_Notes',['Unrelated wording','','','See DOI:10.5281/ZeNoDo.999'],False),('canonical_lowercase_negative',['Unrelated wording','','https://doi.org/10.5281/zenodo.999',''],True)]
  for label,row,rej in fixtures:
   root=work/label;root.mkdir();full_chain(root,row,label,rej)
req(not FORBIDDEN,'actual provider attempt')
res={'timestamp':B.stamp(),'optimization':sys.flags.optimize,'scope':'Actual collector account pagination + actual reconcile + actual append predicates; synthetic boundaries. Gate bypass at append only establishes independent layer behavior.','actual_provider_attempts':len(FORBIDDEN),'finding':'P280-OPS-03','cases':RESULT}
(R/('INDEPENDENT_OPS_RESULTS_OPTIMIZED.json' if sys.flags.optimize else 'INDEPENDENT_OPS_RESULTS.json')).write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
