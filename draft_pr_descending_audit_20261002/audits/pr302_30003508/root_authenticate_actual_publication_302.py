"""ROOT whole-body reconstruction of actual publication and one tracker append.

Read-only services: none. Writes only a new own acceptance artifact and log.
No project import occurs before all four frozen source and registry checks.
"""
from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, json, os, stat, sys
A = Path(__file__).parent
R = Path('/Users/alec/Documents/Math')
D = A / 'publication_preparation'
F = A / 'preprint_package_v02'
O = A / 'publication_actual'

def require(v, m):
    if not v: raise RuntimeError(m)

def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(Path(p).read_bytes())
def pin(p):
    p = Path(p); require(p.is_file() and not p.is_symlink(), 'literal file '+str(p))
    b = p.read_bytes(); return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))

def match(x):
    require(pin(x['path']) == x, 'full input/body/mode changed '+x['path'])

def ts(x):
    t = datetime.fromisoformat(x); require(t.tzinfo is not None, 'timezone'); return t

def native(base, label, argv):
    w = base / label; q = load(w/'request.json'); j = load(w/'execution.json'); started=load(w/'started.json')
    require(j['argv']==argv and j['cwd']==str(R) and all(j[k]==v for k,v in q.items()), 'request/argv/cwd agreement '+label)
    require(type(j['actual_PID']) is int and type(j['actual_launcher_PID']) is int and min(j['actual_PID'],j['actual_launcher_PID'])>0, 'real recorder PIDs')
    require(started==dict(actual_PID=j['actual_PID'],start_UTC=j['start_UTC'],state='STARTED_OUTCOME_PENDING'), 'actual start')
    require(ts(j['requested_UTC'])<=ts(j['start_UTC'])<=ts(j['end_UTC']) and j['exit_code']==0 and j['timed_out'] is False and j['automatic_retry'] is False, 'actual native outcome')
    require(j['resolved_executable']==pin(Path(argv[0]).resolve()) and j['resolved_caller_interpreter']==pin(Path('/opt/homebrew/bin/python3').resolve()), 'resolved executable')
    expected={str(D/n) for n in ['publication_guard.py','run_zenodo_step.py','verify_public_record.py','append_tracker.py']}
    if str(R/'zenodo_deposit_tool/zenodo.py') in argv:expected.add(str(R/'zenodo_deposit_tool/zenodo.py'))
    for k, paths in [('full_prelaunch_sources',expected),('full_prelaunch_approvals',{str(A/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json'),str(A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json'),str(D/'REVISED_OPERATOR_MANIFEST.json')})]:
        copies=j[k];require(len(copies)==len(paths) and {x['input']['path'] for x in copies}==paths,'all exact prelaunch source/approval roles')
        for x in copies:
            match(x['input']);match(x['stored_full_source'])
            require(gzip.decompress(Path(x['stored_full_source']['path']).read_bytes())==Path(x['input']['path']).read_bytes(),'entire archived input')
    bodies=[]
    for n in ['stdout','stderr']:
        x=j[n];match(x['stored']);require(x['stored']['path']==str(w/(n+'.bin.gz')),'actual stream path')
        b=gzip.decompress(Path(x['stored']['path']).read_bytes());require(len(b)==x['logical_bytes'] and sha(b)==x['logical_sha256'],'complete stored/logical stream');bodies.append(b)
    return j,bodies

def main():
    require(not sys.flags.optimize, 'optimization forbidden')
    registry = D/'REVISED_OPERATOR_MANIFEST.json'
    require(pin(registry)['sha256']=='aabb136882570e39d3646a67137fe1d49a8e73132e2c8fea67388feab654f6a4','exact independently reviewed registry')
    rows=load(registry)['approved_operational_sources']
    require(len(rows)==4 and {Path(x['path']).name for x in rows}=={'publication_guard.py','run_zenodo_step.py','verify_public_record.py','append_tracker.py'},'four nonvacuous frozen source pins')
    for x in rows:match(x)
    require(pin(A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json')['sha256']=='2649390025a4d5e4d9afaf3338af51f6a9efb214715aeffb0a729cb759452588','exact genuine ROOT operations approval')
    sys.path.insert(0,str(D))
    from publication_guard import clearance
    from verify_public_record import verify_public_evidence, public_argv
    from run_zenodo_step import inspected_publication
    clearance();published=inspected_publication();public=verify_public_evidence(published)
    require(published['id']==23157237 and published['doi']=='10.5281/zenodo.23157237','exact actual production DOI')
    native_rows=[];results={};streams={}
    prefix=['/opt/homebrew/bin/python3','-E','-B',str(R/'zenodo_deposit_tool/zenodo.py')]
    for label,op,extra in [('stage','stage',[]),('inspect_draft','inspect',[]),('publish','publish',['--confirm-id','23157237']),('inspect_published','inspect',['--check-doi'])]:
        j,b=native(O/'private_processes',label,prefix+[op,str(F/'zenodo-deposit.json')]+extra)
        require(not b[1] and json.loads(b[0])==load(O/(label+'_receipt.json')),'full actual Zenodo receipt')
        x=json.loads(b[0]);require(x['id']==23157237 and x['environment']=='production' and x['title']==published['title'],'stage/inspect/publish identity')
        require(x['state']==('ready_to_publish' if label in ['stage','inspect_draft'] else 'published'),'each true phase outcome')
        for f in x['files']:require(len((F/f['name']).read_bytes())==f['size'] and sha((F/f['name']).read_bytes())==f['sha256'],'whole upload file')
        native_rows.append(j);results[label]=j;streams[label]=b
    for label,url in [('record','https://zenodo.org/api/records/23157237')]+[('file_'+n,'https://zenodo.org/api/records/23157237/files/'+n+'/content') for n in ['spectral_tensor_consistency.pdf','spectral_tensor_verification.zip']]:
        j,b=native(O/'private_public_readback',label,public_argv(url));require(not b[1],'anonymous public error stream');native_rows.append(j)
    request=load(O/'TRACKER_ROW_REQUEST.json');done=load(O/'TRACKER_COMPLETE.json')
    cli='/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws';sid='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
    require(request['explicit_user_authorization'] is True and request['duplicate_found'] is False and request['gid']==1254632077,'actual authorized tracker request')
    require(request['params']==dict(spreadsheetId=sid,range="'Math Puzzles'!A:AQ",valueInputOption='RAW',insertDataOption='INSERT_ROWS',includeValuesInResponse=True),'literal RAW one-row params')
    require(request['body']['majorDimension']=='ROWS' and len(request['body']['values'])==1 and len(request['body']['values'][0])==4,'one four-cell row')
    for label in ['sheet_metadata','all_rows_before','tracker_dry_run','tracker_append','appended_row_readback','all_rows_after']:
        if label=='sheet_metadata':argv=[cli,'sheets','spreadsheets','get','--params',json.dumps(dict(spreadsheetId=sid,fields='spreadsheetId,sheets(properties(sheetId,title,gridProperties(rowCount,columnCount)))'))]
        elif label in ['tracker_dry_run','tracker_append']:
            argv=[cli,'sheets','spreadsheets','values','append','--params',json.dumps(request['params']),'--json',json.dumps(request['body'])]+(['--dry-run'] if label=='tracker_dry_run' else [])
        else:
            if label=='all_rows_before':
                sheet=json.loads(streams['sheet_metadata'][0]);props=[x['properties'] for x in sheet['sheets'] if x['properties']['sheetId']==1254632077];require(sheet['spreadsheetId']==sid and len(props)==1 and props[0]['title']=='Math Puzzles' and props[0]['gridProperties']['columnCount']==43,'complete actual tab schema')
                target="'Math Puzzles'!A1:AQ"+str(props[0]['gridProperties']['rowCount'])
            elif label=='appended_row_readback':target="'Math Puzzles'!A26:D26"
            else:target="'Math Puzzles'!A1:AQ"
            argv=[cli,'sheets','spreadsheets','values','get','--params',json.dumps(dict(spreadsheetId=sid,range=target,valueRenderOption='FORMULA'))]
        j,b=native(O/'private_processes',label,argv);native_rows.append(j);results[label]=j;streams[label]=b
    before=json.loads(streams['all_rows_before'][0])['values'];after=json.loads(streams['all_rows_after'][0])['values'];row=request['body']['values'][0]
    require(before[0][:4]==['Original Problem','Solution Chat URL','DOI','Notes'] and len(before)==25 and after==before+[row] and len(after)==26,'entire table exact prefix plus one row')
    require(row==done['row'] and row[1]=='' and row[2]==published['doi_url'] and '30003508' in row[0] and published['title'] in row[3],'all four actual cells')
    require(not any('30003508' in str(x) or published['doi'] in str(x) or published['title'].lower() in str(x).lower() for x in before[1:]),'prior duplicate')
    require(sum('30003508' in str(x) for x in after[1:])==sum(published['doi'] in str(x) for x in after[1:])==1,'unique problem/DOI')
    append=json.loads(streams['tracker_append'][0]);updates=append['updates']
    require(append['spreadsheetId']==sid and updates['updatedRange']=="'Math Puzzles'!A26:D26" and (updates['updatedRows'],updates['updatedColumns'],updates['updatedCells'])==(1,4,4),'actual append shape/range')
    require(json.loads(streams['appended_row_readback'][0])['values']==[row] and done['single_actual_append_PID']==results['tracker_append']['actual_PID']==1555,'actual single append/readback PID')
    require(done['status']=='PASS_EXACT_ONE_DOI_ROW_AND_WHOLE_TABLE_READBACK' and done['all_prior_rows_unchanged'] is True and done['all_original_columns_scanned']==43 and done['automatic_retry'] is False,'truthful completion interpretation')
    require(len(native_rows)==13 and len({x['actual_PID'] for x in native_rows})==13,'all thirteen actual process captures')
    clearance()
    out=dict(status='ROOT_ACCEPTS_ACTUAL_PUBLICATION_AND_EXACT_ONE_TRACKER_ROW',UTC=datetime.now(timezone.utc).isoformat(),actual_ROOT_recorder_PID=os.getpid(),source=pin(__file__),original_PR=302,original_head='eb6e0e999521d84a65f9857d338cad76b84d30db',original_status='claimed_solved',original_author_history='2/5',DOI=published['doi'],doi_url=published['doi_url'],record_url=published['record_url'],science_gate=pin(A/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json'),operations_gate=pin(A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json'),candidate_manifest=pin(F/'SECOND_CANDIDATE_MANIFEST.json'),metadata=pin(F/'record_metadata.json'),public_files=[pin(F/n) for n in ['spectral_tensor_consistency.pdf','spectral_tensor_verification.zip']],public_verification=pin(O/'PUBLIC_RECORD_VERIFICATION.json'),tracker_completion=pin(O/'TRACKER_COMPLETE.json'),actual_native_processes=native_rows,full_actual_captures_authenticated=13,all_reviewed_metadata_fields_exact=True,both_full_public_downloads_equal_frozen_files=True,tracker_range="'Math Puzzles'!A26:D26",all_prior_43_columns_and_25_rows_preserved=True,single_actual_append_PID=1555,no_individual_contacted=True,no_Git_native_acceptance_control_write=True,automatic_retry=False,scope='Independent ROOT whole-body replay of thirteen genuine retained captures, full archived prelaunch inputs, two complete public downloads, exact metadata and whole-table prefix. Recorder observations are not independent OS/clock/upstream attestations.',estimates_percent=dict(mathematics=100,bounded_priority=100,preprint=100,publication_and_tracker=100,total_PR_workflow=85,native_integration=25))
    q=A/'ROOT_ACTUAL_PUBLICATION_AND_TRACKER_ACCEPTANCE.json'
    with q.open('x') as f:json.dump(out,f,indent=2,ensure_ascii=False);f.write('\n')
    q.chmod(0o444)
    with (F/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+out['UTC']+' — ROOT authenticates all thirteen actual service processes, complete sources/approvals/raw streams, production publication DOI '+published['doi']+', two full matching public files and exact one RAW tracker row A26:D26 preserving all43 columns and all25 prior rows. Publication/tracker100%; total PR302 workflow85%; native integration25%. No shared Git/native/control action.\n')
    print(json.dumps(dict(status=out['status'],actual_ROOT_recorder_PID=os.getpid(),DOI=out['DOI'],tracker_range=out['tracker_range'],full_actual_captures_authenticated=13,acceptance=pin(q))))

if __name__=='__main__':main()
