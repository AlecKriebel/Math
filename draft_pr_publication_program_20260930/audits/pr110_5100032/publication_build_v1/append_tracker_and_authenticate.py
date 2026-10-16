#!/usr/bin/env python3
"""Perform the authorized single GWS append and authenticate two actual reads."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,importlib.util,json,os,re,subprocess,sys
A=Path(__file__).resolve().parents[1];D=A/'actual_tracker_20261006'
GWS='/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'
SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';TITLE='Math Puzzles';GID=1254632077
def need(v,m):
    if not v:raise RuntimeError(m)
def now():return datetime.now(timezone.utc).isoformat()
def read(p):return json.loads(p.read_text())
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p):return {'path':p.relative_to(A).as_posix(),**hp(p.read_bytes())}
def compact(v):return json.dumps(v,separators=(',',':'),ensure_ascii=False)
def call(role,verb,params,body=None):
    label='gws_actual_'+role+'_20261006';argv=[GWS,'sheets','spreadsheets',*verb,'--params',compact(params)]
    if body is not None:argv+=['--json',compact(body)]
    p=subprocess.run([sys.executable,'-E','-S','-B',str(A/'publication_build_v1/record_transport.py'),label,*argv],cwd=A,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    need(p.returncode==0,'GWS operation failed; inspect retained receipt, never repeat append blindly: '+role)
    folder=A/'actual_operations'/label;e=read(folder/'execution.json')
    for stream in ('stdout','stderr'):need(hp((folder/e[stream]['path']).read_bytes())=={k:e[stream][k] for k in ('bytes','sha256')},'Actual GWS stream binding')
    need(e['exit_code']==0 and e['reaped'] is True and e['argv']==argv and e['termination']['signal'] is None,'Actual GWS process completion')
    response=read(folder/'stdout.bin')
    norm={'actual_receipt':True,'template_only':False,'PID':e['child_PID'],'exit_code':0,'argv':argv,'cwd':e['cwd'],'environment_sha256':e['environment_sha256'],'UTC_start':e['UTC_start'],'UTC_end':e['UTC_end'],'stdout':pin(folder/'stdout.bin'),'stderr':pin(folder/'stderr.bin'),'reaped':True,'termination_reason':None,'params_pin':hp(argv[argv.index('--params')+1].encode()),'raw_execution':pin(folder/'execution.json')}
    if body is not None:norm['json_pin']=hp(argv[argv.index('--json')+1].encode())
    return response,norm
def main():
    started=now();need(not D.exists(),'Tracker workflow already started; inspect before any retry');D.mkdir()
    published=read(A/'published_record_fullbody_verification_20261006/RESULT.json');need(published['published'] is True and published['full_PDF_ZIP_bytes_match'] is True and published['record_id']==23191247,'Actual publication must already be authenticated')
    doi=published['DOI'];values=['https://arxiv.org/abs/2004.12497','','https://doi.org/'+doi,'A telescoping proof of the focal antipedal sum invariant — Alec Kriebel, v1.0 (2026-10-06). PR110; 5100032 / AMR-050-0032. Full proof for regular closed nonretracing orbits between strictly nested confocal ellipses, including odd periods and stars. Original observation credited to Reznik–Garcia–Koiller. Bounded priority audit; no absolute-first claim. PDF and portable verification package; extensive AI use; unrefereed, no conventional human peer review; two fresh independent AI adversarial reviews.']
    (D/'INTENDED_ROW.json').write_text(json.dumps({'UTC':started,'values':values,'single_append_authorized_by_persistent_goal':True},indent=2,ensure_ascii=False)+'\n')
    processes={};metadata,processes['metadata']=call('metadata',['get'],{'spreadsheetId':SHEET,'includeGridData':False,'fields':'spreadsheetId,properties(title),sheets(properties)'})
    need(metadata['spreadsheetId']==SHEET and any(s['properties']['sheetId']==GID and s['properties']['title']==TITLE for s in metadata['sheets']),'Target spreadsheet/tab')
    header,processes['header']=call('header',['values','get'],{'spreadsheetId':SHEET,'range':"'Math Puzzles'!A1:D1"})
    columns=['Original Problem','Solution Chat URL','DOI','Notes'];need(header['values']==[columns],'Exact actual sheet columns')
    scan,scanprocess=call('private_duplicate_check',['values','get'],{'spreadsheetId':SHEET,'range':"'Math Puzzles'!A1:D2000"})
    matches=[i+1 for i,row in enumerate(scan.get('values',[])) if any('5100032 / AMR-050-0032' in str(c) or doi in str(c) for c in row)]
    need(not matches,'Existing matching row; do not append duplicate. Recover/inspect matching rows.')
    (D/'DUPLICATE_CHECK.json').write_text(json.dumps({'UTC':now(),'target_DOI':doi,'target_problem':'5100032 / AMR-050-0032','matching_rows':matches,'actual_scan_execution':scanprocess['raw_execution'],'other_row_bodies_private':True},indent=2)+'\n')
    appended,processes['append']=call('append',['values','append'],{'spreadsheetId':SHEET,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True},{'majorDimension':'ROWS','values':[values]})
    update=appended['updates'];selected=update['updatedRange'];matched=re.fullmatch(r"'Math Puzzles'!A([2-9][0-9]*|1[0-9]+):D\1",selected)
    need(matched and update['updatedRows']==1 and update['updatedColumns']==4 and update['updatedCells']==4 and update['updatedData']['values']==[values],'Actual append exact returned range/cells')
    row=int(matched.group(1));params={'spreadsheetId':SHEET,'range':selected}
    for role in ('readback','independent_readback'):
        r,processes[role]=call(role,['values','get'],params);need(r['range']==selected and r['values']==[values],'Actual independent exact row readback')
    need(len({p['PID'] for p in processes.values()})==5,'Five actual distinct GWS child processes')
    end=published['actual_transport_processes']['ZIP']['UTC_end']
    for role in ('metadata','header','append','readback','independent_readback'):
        need(processes[role]['UTC_start']>=end,'Actual service ordering');end=processes[role]['UTC_end']
    norm={'schema':'pr110-actual-gws-sheet-receipt/v1','actual_receipt':True,'template_only':False,'problem_id':5100032,'problem_code':'AMR-050-0032','original_head':'3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35','DOI':doi,'spreadsheet_id':SHEET,'sheet_id':GID,'sheet_title':TITLE,'columns':columns,'row_index':row,'range':selected,'values':values,'processes':processes,'existing_chat_authorized':False}
    (D/'SHEET_RECEIPT.json').write_text(json.dumps(norm,indent=2,ensure_ascii=False)+'\n')
    result={'schema':'pr110-actual-tracker-completion/v1','actual_root_PID':os.getpid(),'UTC_start':started,'UTC_end':now(),'DOI':doi,'range':selected,'single_append':True,'actual_five_distinct_cli_processes':True,'both_independent_full_row_readbacks_equal':True,'sheet_receipt':pin(D/'SHEET_RECEIPT.json'),'workflow_completion_percent':80,'native_integration_pending':True}
    (D/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
