#!/usr/bin/env python3
"""EXTERNAL MUTATIONS: separately guarded stage, publish, then exactly-once ledger append.
This file was prepared only. No mutation action was executed by its preparer.
"""
if not globals().get('_PR1131_SOURCE_VERIFIED',False):
    raise RuntimeError('Use the externally SHA-verified source bootstrap; direct helper imports are forbidden')
import argparse
from urllib.parse import quote
from urllib.request import Request,urlopen
from ops_common import *
from collect_live import collect,draft_row,row_ids
from native_policy import observe as observe_target,public_projection,legacy_concept

MANIFEST=OPS/'proposed/preprint/zenodo-deposit.json'

def require_action(args,action):
    c=clearance(args.clearance_sha256,args.operations_sha256);need(action in c['allowed_actions'],'Action not cleared')
    r=strict_json((RUNTIME/'MERGE_VERIFIED.json').read_bytes())
    need(r['merged'] is True and r['head']==args.expected_pr_head and r['unselected_siblings_and_queue_preserved'] is True and r['preprint_files']==5 and r['original_files']==8 and r['framing_replacements']==3,'Exact merge preservation receipt absent')
    pr=gh('pulls/1131');validate_pr(pr,args.expected_pr_head,True);validate_description(pr,args.expected_pr_head);need(pr['merge_commit_sha']==r['commit'],'Actual PR merge commit changed')
    commit=gh('git/commits/'+r['commit'])
    need([p['sha'] for p in commit['parents']]==r['parents'] and commit['tree']['sha']==r['tree'],'Recorded actual merge parents/tree drifted')
    return c

class GuardedClient:
    def __init__(self,args,action,identifier,delegate=None):
        self.args,self.action,self.identifier=args,action,identifier
        self.delegate=delegate if delegate is not None else zenodo.ZenodoClient('production',zenodo.token_for('production'))
        self.metadata,self.uploads=zenodo.load_manifest(MANIFEST)
        self.snapshot=None
    def accept(self,snapshot,added=None):
        if self.snapshot is not None:
            prior=self.snapshot
            for key in ['record','concept','owner','doi','native_metadata']:
                need(prior[key]==snapshot[key],'Native target infrastructure/metadata changed across operation')
            need(prior['published'] is False or snapshot['published'] is True,'Published target reverted to draft')
            if not snapshot['published']:need(prior['bucket']==snapshot['bucket'],'Target upload bucket changed')
            expected=set(prior['files'])|({added} if added is not None else set())
            need(set(snapshot['files'])==expected,'Native file inventory changed outside one intended upload')
            need(all(snapshot['files'][n]==f for n,f in prior['files'].items()),'Native content/version/bucket identifier changed')
        self.snapshot=snapshot
    def observation(self,published,required_names=None,added=None):
        legacy,snapshot=observe_target(self.delegate,self.identifier,published,self.metadata,self.uploads,required_names)
        self.accept(snapshot,added);return legacy,snapshot
    def before(self,identifier,required_names=None):
        need(identifier==self.identifier,'Lifecycle ID changed')
        c=require_action(self.args,self.action)
        gate,_,_=collect('before_'+self.action,self.args.expected_pr_head,identifier,cleared=c)
        require_action(self.args,self.action)
        snapshot=None
        if identifier is not None:
            # These exact legacy/native/finalized-file GETs occur AFTER the last
            # long account/GWS gate and immediately beside the delegated write.
            _,snapshot=self.observation(False,required_names)
            fresh(snapshot['observed_at'],seconds=30)
        fresh(gate['at_start']);return snapshot
    def get(self,identifier):
        need(identifier==self.identifier,'Unexpected lifecycle read ID')
        first=self.delegate.get(identifier);zenodo.validate_record(first,identifier);legacy_concept(first)
        names={v['name'] for v in self.uploads} if self.action=='publish' or first['submitted'] else None
        legacy,_=self.observation(first['submitted'],names);return legacy
    def create(self,metadata):
        need(self.action=='stage' and self.identifier is None,'No second draft allocation')
        need(metadata==self.metadata,'Create supplied unreviewed metadata')
        self.before(None);result=self.delegate.create(metadata)
        need(type(result.get('id')) is int and result['id']>0,'Unknown create outcome; reconcile full owned account, never restage')
        self.identifier=result['id'];legacy_concept(result);self.observation(False,set());return result
    def upload(self,bucket,entry):
        need(self.action=='stage' and self.identifier is not None,'Upload outside stage')
        intended={v['name']:v for v in self.uploads};need(entry.get('name') in intended and entry==intended[entry['name']],'Upload argument differs from sealed intended bytes/path')
        snapshot=self.before(self.identifier)
        need(bucket==snapshot['bucket'] and entry['name'] not in snapshot['files'],'Upload bucket/file already changed')
        result=self.delegate.upload(bucket,entry)
        self.observation(False,set(snapshot['files'])|{entry['name']},added=entry['name']);return result
    def update(self,identifier,metadata):
        need(self.action=='stage' and metadata==self.metadata,'Unreviewed metadata update or wrong phase')
        names={v['name'] for v in self.uploads};self.before(identifier,names)
        result=self.delegate.update(identifier,metadata);legacy_concept(result);self.observation(False,names);return result
    def publish(self,identifier):
        need(self.action=='publish','Stage may not publish')
        names={v['name'] for v in self.uploads};self.before(identifier,names)
        # No provider read, root gate or unrelated work intervenes after the
        # final target observation. Provider APIs still offer no atomic lock.
        result=self.delegate.publish(identifier);legacy_concept(result)
        try:self.observation(True,names)
        except RuntimeError as exc:raise zenodo.DepositError('Post-publication native/legacy verification failed; retain ID and never create a replacement') from exc
        return result

def lifecycle(args):
    action=args.action;c=require_action(args,action);identifier=args.deposit_id
    place,state=zenodo.local_state(MANIFEST.resolve(),'production')
    if action=='stage':need(identifier is None and state is None,'Initial stage requires no ID/state; reconcile existing work')
    else:need(type(identifier) is int and identifier>0 and state is not None and state['id']==identifier and state['manifest']==str(MANIFEST.resolve()) and state['environment']=='production','Publish requires exact saved manifest/production draft ID')
    g,_,_=collect('before_'+action,args.expected_pr_head,identifier,cleared=c)
    durable(RUNTIME/('ZENODO_'+action.upper()+'_INTENT.json'),{'at':stamp(),'action':action,'head':args.expected_pr_head,'id':identifier,'manifest':str(MANIFEST),'manifest_sha256':sha(MANIFEST.read_bytes()),'gate':g['private_capture'],'rule':'Unknown outcome: GET-only inspect exact state/account; preserve intent; never automatically allocate or publish again.'})
    result=zenodo.run(argparse.Namespace(command=action,manifest=MANIFEST,sandbox=False,confirm_id=identifier,check_doi=True),client=GuardedClient(args,action,identifier))
    need(result.get('state')==('ready_to_publish' if action=='stage' else 'published') and type(result.get('id')) is int and result['id']>0 and (identifier is None or result['id']==identifier),'Lifecycle outcome unconfirmed; no retry')
    durable(RUNTIME/('ZENODO_'+action.upper()+'_VERIFIED.json'),result)
    return {k:result.get(k) for k in ['id','state','doi','doi_url','record_url','doi_resolution']}

def fetch(url,limit):
    with urlopen(Request(url,headers={'User-Agent':'Math-PR1131-publication-verification/1.0'}),timeout=60) as r:
        body=r.read(limit+1);need(len(body)<=limit,'Oversized public response');return body,r.status,r.url

def verify_public(args):
    require_action(args,'ledger');identifier=args.deposit_id
    need(type(identifier) is int and identifier>0,'Exact published record ID required')
    metadata,uploads=zenodo.load_manifest(MANIFEST)
    client=zenodo.ZenodoClient('production',zenodo.token_for('production'))
    record,native_verified=observe_target(client,identifier,True,metadata,uploads,{v['name'] for v in uploads})
    doi='10.5281/zenodo.'+str(identifier);need(record.get('doi')==doi,'Unexpected exact DOI')
    import uuid
    raw=PRIVATE/('public_'+uuid.uuid4().hex);raw.mkdir(mode=0o700)
    data,status,url=fetch('https://zenodo.org/api/records/'+str(identifier),16*1024*1024)
    public=strict_json(data);durable(raw/'record.json',public)
    need(status==200 and int(public['id'])==identifier and public['doi']==doi,'Public record identity mismatch')
    zenodo.verify(public_projection(public,metadata,native_verified),metadata,uploads)
    checked=[]
    for entry in uploads:
        body,code,destination=fetch('https://zenodo.org/records/'+str(identifier)+'/files/'+quote(entry['name'],safe='')+'?download=1',entry['size']+1)
        need(code==200 and len(body)==entry['size'] and sha(body)==entry['sha256'] and hashlib.md5(body).hexdigest()==entry['md5'],'Published file bytes differ')
        checked.append({'name':entry['name'],'bytes':len(body),'sha256':sha(body),'md5':entry['md5']})
    # Full response is not saved; final status and exact destination are evidence.
    _,code,destination=fetch('https://doi.org/'+doi,16*1024*1024)
    need(code==200 and destination=='https://zenodo.org/records/'+str(identifier),'DOI does not resolve with HTTP200 to exact intended record')
    receipt={'at':stamp(),'record':identifier,'doi':doi,'files':checked,'metadata_verified':True,'native_target_verified':native_verified,'doi_status':code,'doi_destination':destination,'private_capture':str(raw)}
    durable(raw/'verification.json',receipt);return receipt

def append_ledger(args):
    c=require_action(args,'ledger');public=verify_public(args);identifier=args.deposit_id;row=draft_row(identifier)
    g,_,before=collect('before_ledger',args.expected_pr_head,identifier,cleared=c,allow_target=True)
    fresh(public['at']);families=set(g['family_ids'])
    existing=[(i,r) for i,r in enumerate(before,1) if families&row_ids(r)]
    need(len(existing)<=1 and (not existing or existing[0][1]==row),'Existing record/concept DOI row changed/duplicated')
    intent=RUNTIME/'LEDGER_APPEND_INTENT.json'
    if existing:
        if intent.exists():
            prior=strict_json(intent.read_bytes())
            need(prior['head']==args.expected_pr_head and prior['record']==identifier and prior['values']==row and prior['spreadsheet_id']==SHEET and prior['sheet_id']==SHEET_ID and prior['sheet_title']==SHEET_TITLE and prior['operation']=='spreadsheets.batchUpdate.appendCells','Prior append intent belongs to different identity')
            gatepath=Path(prior['gate'])
            need(PRIVATE in gatepath.parents and not gatepath.is_symlink(),'Prior ledger capture outside private folder')
            original=strict_json((gatepath/'ledger.json').read_bytes())['values']
            need(digest(original)==prior['before_sha256'] and len(original)==prior['before_rows'] and before==original+[row],'Lost-response readback does not preserve original rows plus one exact append; root reconciliation required')
        # A lost append response is reconciled by a read, never another append.
        _,after=gws_read();need(after==before,'Ledger changed during no-write reconciliation')
        durable(RUNTIME/'LEDGER_VERIFIED.json',{'at':stamp(),'record':identifier,'spreadsheet_id':SHEET,'sheet_id':SHEET_ID,'sheet_title':SHEET_TITLE,'row':existing[0][0],'values':row,'new_row':False,'read_back_exact':True,'unique_target_family':True,'gate':g['private_capture']})
        return {'record':identifier,'spreadsheet_id':SHEET,'sheet_id':SHEET_ID,'sheet_title':SHEET_TITLE,'row':existing[0][0],'new_row':False,'verified':True}
    need(not intent.exists(),'Prior append intent exists without visible exact row; root must reconcile, no retry')
    _,now=gws_read();need(now==before,'Ledger changed after full-account gate; recollect and reconcile')
    require_action(args,'ledger');fresh(g['at_start']);fresh(public['at'])
    durable(intent,{'at':stamp(),'head':args.expected_pr_head,'record':identifier,'spreadsheet_id':SHEET,'sheet_id':SHEET_ID,'sheet_title':SHEET_TITLE,'operation':'spreadsheets.batchUpdate.appendCells','columns':'A:D','values':row,'before_sha256':digest(before),'before_rows':len(before),'gate':g['private_capture'],'public_verification':public,'rule':'O_EXCL intent remains permanently. Unknown outcome: read full A:AQ and find exact unique row/DOI; never blindly append again.'})
    # The sole mutation targets the stable numeric ID, never an A1 title.
    # appendCells appends after existing data and does not overwrite a planned
    # row. Collaborators can still race; exact readback and retained intent
    # detect drift but cannot roll back or lock a provider transaction.
    request={'requests':[{'appendCells':{'sheetId':SHEET_ID,'rows':[{'values':[{'userEnteredValue':{'stringValue':cell}} for cell in row]}],'fields':'userEnteredValue'}}],'includeSpreadsheetInResponse':True,'responseIncludeGridData':False}
    result=command(['gws','sheets','spreadsheets','batchUpdate','--params',json.dumps({'spreadsheetId':SHEET}),'--json',json.dumps(request,ensure_ascii=False)])
    durable(RUNTIME/'LEDGER_APPEND_RESPONSE.json',result)
    validate_append_response(result)
    _,after=gws_read()
    found=[(i,r) for i,r in enumerate(after,1) if families&row_ids(r)]
    need(len(found)==1 and found[0][1]==row and len(after)==len(before)+1 and after[:-1]==before and after[-1]==row,'Readback/uniqueness/preservation mismatch; no retry')
    durable(RUNTIME/'LEDGER_VERIFIED.json',{'at':stamp(),'record':identifier,'spreadsheet_id':SHEET,'sheet_id':SHEET_ID,'sheet_title':SHEET_TITLE,'row':found[0][0],'values':row,'new_row':True,'read_back_exact':True,'unique_target_family':True,'all_other_rows_preserved':True,'numeric_readback_counts':{'rows':1,'columns':4,'cells':4},'numeric_readback_range':{'sheetId':SHEET_ID,'startRowIndex':found[0][0]-1,'endRowIndex':found[0][0],'startColumnIndex':0,'endColumnIndex':4},'response_counts_or_value_echo_available':False,'gate':g['private_capture']})
    return {'record':identifier,'spreadsheet_id':SHEET,'sheet_id':SHEET_ID,'sheet_title':SHEET_TITLE,'row':found[0][0],'new_row':True,'verified':True}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['stage','publish','verify-public','ledger']);p.add_argument('--expected-pr-head',required=True);p.add_argument('--deposit-id',type=int);p.add_argument('--clearance-sha256',required=True);p.add_argument('--operations-sha256',required=True)
    a=p.parse_args();result=verify_public(a) if a.action=='verify-public' else append_ledger(a) if a.action=='ledger' else lifecycle(a)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
