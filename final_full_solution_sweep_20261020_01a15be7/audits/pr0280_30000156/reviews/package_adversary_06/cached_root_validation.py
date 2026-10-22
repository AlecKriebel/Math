#!/usr/bin/env python3
"""Actual cached primary account/sheet bodies, synthetic provider interface/fresh stamps."""
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
from urllib.parse import urlsplit,parse_qs,urlencode
import json,hashlib,sys,copy,socket,subprocess
A=Path(__file__).resolve().parents[2];R=A.parents[1];P=R/'private/pr0280_package06'
sys.path.insert(0,str(A))
import ops_binding as B
import prepublication_check as C
import publication_live_gates as G
def ck(v,m):
    if not v:raise RuntimeError(m)
def main():
    root=json.loads((A/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_text())
    receipt=json.loads((A/'ROOT_SHARED_FRESH_ACCOUNT_RECHECK_20261021T1522.json').read_text())
    account_path=Path(receipt['shared_complete_authenticated_account_receipt']);raw=account_path.parent
    ck(hashlib.sha256(account_path.read_bytes()).hexdigest()==receipt['shared_account_sha256'],'cached account bytes')
    account=json.loads(account_path.read_text());sheet=json.loads((raw/'ledger.json').read_text());rows=B.schema_rows(sheet)
    ck(account['total']==len(account['records'])==195 and len(rows)==176,'complete cached counts')
    ck(B.sha((raw/'ledger.json').read_bytes())==receipt['whole_sheet_sha256'],'sheet raw-body SHA256')
    parsed=[B.row_identity_leads(r) for r in rows]
    known=next(r for r in account['records'] if int(r['id'])==23137834)
    ck(B.digest(B.identity_projection(known))==root['account_leads'][0]['metadata_and_files_sha256'],'known full metadata/files')
    ck(B.digest(rows[20])==root['ledger_leads'][0]['values_sha256'],'whole row21')
    state=R.parent/root['unrelated_local_state_exemptions'][0]['path']
    ck(B.sha(state.read_bytes())==root['unrelated_local_state_exemptions'][0]['sha256'],'exact unrelated state')
    positive=next(r for r in account['records'] if int(r['id'])==23174283)
    def command(args):
        if args[0]=='gws':return copy.deepcopy(sheet)
        if args[-1].endswith('pulls/280'):return {'number':280,'state':'open','merged':False,'draft':True,'head':{'sha':IHEAD,'ref':'codex/synthetic'},'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}|{'head':{'sha':IHEAD,'ref':'codex/synthetic','repo':{'full_name':'AlecKriebel/Math'}}}
        if args[-1].endswith('heads/main'):return {'object':{'sha':'e'*40}}
        raise RuntimeError('Unknown synthetic command')
    class Client:
        base='https://zenodo.org'
        def request(self,method,url):
            ck(method=='GET','GET-only account fixture');params=parse_qs(urlsplit(url).query);query=params.get('q',[''])[0];page=int(params.get('page',['1'])[0])
            recs=[positive] if query=='Fibonacci' else [known] if query else account['records']
            selected=recs[(page-1)*25:page*25];nxt=None
            if page*25<len(recs):nxt=self.base+'/api/user/records?'+urlencode({'q':query,'size':25,'page':page+1})
            return {'hits':{'total':{'value':len(recs),'relation':'eq'},'hits':copy.deepcopy(selected)},'links':{'next':nxt}}
    IHEAD='8aebb819bfac9c12340d2f1469408943549ab530';attempts=[]
    def forbidden(*a,**kw):attempts.append(True);raise RuntimeError('Actual provider forbidden')
    with ExitStack() as stack:
        stack.enter_context(patch.object(C,'PRIVATE',P/'cached_collection'))
        stack.enter_context(patch.object(C,'verify_destination',lambda:True));stack.enter_context(patch.object(C,'read_command',command))
        stack.enter_context(patch.object(B.zenodo,'token_for',lambda *a:'SYNTHETIC'))
        stack.enter_context(patch.object(B.zenodo,'ZenodoClient',lambda *a:Client()))
        stack.enter_context(patch.object(subprocess,'run',forbidden));stack.enter_context(patch.object(socket,'socket',forbidden))
        gate=C.gather('before_integration',IHEAD)
        acceptance=G.reconcile(gate,'before_integration',IHEAD)
        ck(gate['account_complete_total']==195 and gate['account_complete_pages']==8 and gate['ledger_rows']==176,'actual gather complete cached model')
        ck(gate['account_targets']==[23137834] and [m['row'] for m in gate['ledger_matches']]==[21],'known target/row leads')
        # Keep exact collected account; modify only scratch copy and hash in gate,
        # proving semantic comparisons, rather than only a stale hash rejection.
        test_path=Path(gate['raw_receipts'])/'account_complete.json';original=test_path.read_bytes()
        mutated=json.loads(original);target=next(r for r in mutated['records'] if int(r['id'])==23137834)
        target['files'][-1]['checksum']='md5:changed'
        test_path.write_text(json.dumps(mutated));fake=copy.deepcopy(gate);fake['account_complete_sha256']=B.sha(test_path.read_bytes())
        try:G.reconcile(fake,'before_integration',IHEAD)
        except RuntimeError as e:reason=str(e)
        else:raise RuntimeError('Changed last complete file projection accepted')
        test_path.write_bytes(original)
        ck(not attempts,'provider attempted')
    result={'status':'PASS','all176_rows_parse':True,'actual_cached_account_records':195,'synthetic_collection_pages':8,'only_known_non_target_lead':23137834,'whole_known_metadata_and_files_verified':True,'whole_row21_verified':True,'local_state_preserved':True,'semantic_last_file_mutation_rejected':reason,'actual_provider_attempts':0,'source_account_sha256':receipt['shared_account_sha256'],'root_lead_sha256':B.sha((A/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_bytes()),'scope':'Actual15:22 cached bodies with synthetic provider/pagination/fresh timestamps; no new live observation or live freshness authority.'}
    (Path(__file__).parent/'CACHED_ROOT_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
