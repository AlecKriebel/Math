"""One tracker append, or read-only recovery. Importing this module performs no action."""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Release helpers refuse optimized Python before any action')
from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess
from release_binding import (context,binding,unchanged,publication,tracker,acquire,exclusive_json,
    require,digest,durable_mkdir,pin,load,expected_tracker_row,SHEET,SHEET_ID,FULL_RANGE,
    tracker_properties,tracker_matches,require_unique_tracker,tracker_row_number,
    validate_append_attempt,validate_append_result,tracker_readback,save_process_streams)

GWS='/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'


def now():return datetime.now(timezone.utc).isoformat()


def reader(folder):
    """Save every provider stream, including lossless partial exception output."""
    def call(label,args,request=None):
        out=folder/(label+'-stdout.json');err=folder/(label+'-stderr.txt')
        require(not out.exists() and not err.exists(),'Readback evidence collision')
        try:p=subprocess.run([GWS,*args],capture_output=True,text=False,timeout=60)
        except Exception as e:
            save_process_streams(out,err,e)
            exclusive_json(folder/(label+'-exception.json'),{'utc':now(),'error_type':type(e).__name__,'error':str(e)})
            raise
        raw,_=save_process_streams(out,err,p)
        require(p.returncode==0,label+' failed; retained outcome requires read-only reconciliation')
        result=json.loads(raw.decode('utf-8'))
        saved=folder/(label+'-readback.json')
        exclusive_json(saved,{'request':request,'response':result} if request is not None else result)
        return result,saved
    return call


def get_values(call,label,target,properties):
    params={'spreadsheetId':SHEET,'range':target}
    result,path=call(label,['sheets','spreadsheets','values','get','--params',json.dumps(params)],params)
    return tracker_readback({'request':params,'response':result},target,properties),path


def fresh_folder(pub,kind):
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    path=Path(pub)/'private_transport'/kind/stamp
    durable_mkdir(path,exist_ok=False)
    return path


def verify_tracker_live(R,PUB,CTX,z):
    """Caller holds release lock. Only provider GETs; immutable accepted receipts stay intact."""
    R=Path(R);PUB=Path(PUB)
    t=tracker(R,PUB,CTX,z);folder=fresh_folder(PUB,'tracker_live');call=reader(folder)
    try:
        meta,properties=call('01-properties',['sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':SHEET})])
        tracker_properties(meta)
        values,target=get_values(call,'02-target',t['updated_range'],meta)
        require(values==[t['values']],'Live target all-four-cell readback differs')
        all_values,after=get_values(call,'03-after',FULL_RANGE,meta)
        require_unique_tracker(all_values,t['values'],z,tracker_row_number(t['updated_range']))
        unchanged(R,CTX);require(tracker(R,PUB,CTX,z)==t,'Tracker receipt changed during live validation')
        result={'utc':now(),'release_binding':binding(CTX),'publication_receipt_sha256':digest(PUB/'ZENODO_VERIFIED_PUBLICATION.json'),
            'tracker_receipt_sha256':digest(PUB/'TRACKER_VERIFIED_APPEND.json'),'updated_range':t['updated_range'],'values':t['values'],
            'evidence':{'properties':pin(properties,R.parent),'target_readback':pin(target,R.parent),'after_scan':pin(after,R.parent)}}
        exclusive_json(folder/'LIVE_VERIFIED.json',result)
        return result
    except Exception as e:
        exclusive_json(folder/'LIVE_PENDING.json',{'utc':now(),'error':str(e),'recovery':'Read-only tracker reconciliation; no second append'})
        raise


def append_once(R,PUB):
    R=Path(R);PUB=Path(PUB)
    require(not (PUB/'TRACKER_VERIFIED_APPEND.json').exists(),'Already verified; use read-only reconciliation')
    lock=acquire(PUB)
    try:
        CTX=context(R);z=publication(R,PUB,CTX);row=expected_tracker_row(CTX,z)
        folder=fresh_folder(PUB,'tracker_runs');call=reader(folder);evidence={}
        meta,properties=call('01-properties',['sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':SHEET})])
        tracker_properties(meta);evidence['properties_before']=pin(properties,R.parent)
        values,before=get_values(call,'02-before',FULL_RANGE,meta)
        evidence['before_scan']=pin(before,R.parent)
        problems,existing=tracker_matches(values,row,z)
        attempt=PUB/'private_transport/tracker/APPEND_ATTEMPT.json'
        durable_mkdir(attempt.parent)
        if problems or existing:
            require(len(existing)==1 and problems==existing and existing[0][1]==row and attempt.exists(),'Conflicting/existing tracker row requires read-only reconciliation')
            validate_append_attempt(load(attempt),CTX,z,PUB)
            target="'Math Puzzles'!A"+str(existing[0][0])+':D'+str(existing[0][0])
            require_unique_tracker(values,row,z,tracker_row_number(target))
            append_count=0;evidence['reconciliation_before']=pin(before,R.parent)
        else:
            require(not attempt.exists(),'Previous append outcome unresolved; no second write permitted')
            unchanged(R,CTX);publication(R,PUB,CTX)
            payload={'majorDimension':'ROWS','values':[row]}
            exclusive_json(attempt,{'utc':now(),'spreadsheet_id':SHEET,'sheet_id':SHEET_ID,'range':FULL_RANGE,
                'doi_url':z['doi_url'],'payload':payload,'release_binding':binding(CTX),
                'publication_receipt_sha256':digest(PUB/'ZENODO_VERIFIED_PUBLICATION.json'),'status':'single append about to be attempted'})
            params={'spreadsheetId':SHEET,'range':FULL_RANGE,'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True}
            result,response=call('03-append',['sheets','spreadsheets','values','append','--params',json.dumps(params),'--json',json.dumps(payload)])
            target=result.get('updates',{}).get('updatedRange');validate_append_result(result,row,target)
            append_count=1;evidence['append_result']=pin(response,R.parent)
        final_meta,final_properties=call('04-properties',['sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':SHEET})])
        tracker_properties(final_meta);evidence['properties']=pin(final_properties,R.parent)
        target_values,readback=get_values(call,'04-target',target,final_meta)
        require(target_values==[row],'Target all-four-cell readback differs')
        after_values,after=get_values(call,'05-after',FULL_RANGE,final_meta)
        require_unique_tracker(after_values,row,z,tracker_row_number(target))
        evidence.update(target_readback=pin(readback,R.parent),after_scan=pin(after,R.parent))
        unchanged(R,CTX);publication(R,PUB,CTX);validate_append_attempt(load(attempt),CTX,z,PUB)
        receipt={'utc':now(),'verified':True,'spreadsheet_id':SHEET,'sheet_id':SHEET_ID,'updated_range':target,
            'doi_url':z['doi_url'],'values':row,'cli':'Google Workspace CLI','append_count':append_count,
            'reconciled_existing_attempt':append_count==0,'exact_all_four_cells_readback':True,
            'release_binding':binding(CTX),'publication_receipt_sha256':digest(PUB/'ZENODO_VERIFIED_PUBLICATION.json'),
            'append_attempt_sha256':digest(attempt),'evidence':evidence}
        exclusive_json(PUB/'TRACKER_VERIFIED_APPEND.json',receipt)
        return tracker(R,PUB,CTX,z)
    except Exception as e:
        if 'folder' in locals():exclusive_json(folder/'PENDING.json',{'utc':now(),'error':str(e),'recovery':'Retain every outcome; reconcile read-only. Existing APPEND_ATTEMPT forbids another append.'})
        raise
    finally:lock.close()


if __name__=='__main__':
    PUB=Path(__file__).resolve().parent
    print(json.dumps(append_once(PUB.parent/'preprint',PUB),indent=2,ensure_ascii=False))
