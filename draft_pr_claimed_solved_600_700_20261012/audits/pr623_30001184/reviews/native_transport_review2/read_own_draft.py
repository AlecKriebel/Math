"""Read only known own draft. Never persist/log token or private API fields."""
from pathlib import Path
from datetime import datetime,timezone
import json
import run_supplied as source
nt=source.nt
HERE=Path(__file__).resolve().parent
calls=[]
class OwnRead(nt.NativeOwnDraftClient):
    def _wire_request(self,method,url,payload=None,file=None,accept='application/json'):
        if method!='GET' or url not in {nt.DRAFT,nt.DRAFT+'/files'}:
            raise nt.zenodo.DepositError('Reviewer permits known own draft GET only')
        calls.append({'method':method,'endpoint':url,'accept':accept})
        return super()._wire_request(method,url,payload=payload,file=file,accept=accept)
try:
    captured=nt.capture_inputs()
    client=OwnRead(nt.zenodo.token_for('production'),captured.metadata,captured.files,allow_writes=False,journal_path=HERE/'tmp/readonly-native-journal.json')
    record=client.get(nt.RECORD_ID)
    result={'checked_utc':datetime.now(timezone.utc).isoformat(),'id':record['id'],'submitted':record['submitted'],
            'exact_native_metadata_verified':True,'completed_files':[f['filename'] for f in record['files']],
            'pending_files':sorted(client.last_pending),'doi_assigned':bool(record.get('doi')),
            'authenticated_gets':calls,'mutations':0,'private_response_persisted':False,
            'limit':'Unpublished read-only preflight. No upload/content/commit/publication or receipt is established.'}
except Exception as exc:
    result={'checked_utc':datetime.now(timezone.utc).isoformat(),'success':False,'failure_type':type(exc).__name__,'mutations':0,'authenticated_gets':calls,'private_response_persisted':False}
(HERE/'LIVE_READONLY_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
