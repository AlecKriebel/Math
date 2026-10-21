"""Explicit selected-record recovery of an owned preview-loss guarded stop."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'zenodo_deposit_tool'))
import zenodo
import metadata_updates as legacy
from baseline import PacedClient
from preview_preservation import repair_owned_preview, validate_display_payload

class RepairClient(PacedClient):
    def __init__(self,record_id,baseline):
        self.record_id=record_id
        self.baseline=baseline
        super().__init__('production',zenodo.token_for('production'))
    def request(self,method,url,*args,**kwargs):
        if method!='GET' and (method,urlsplit(url).path)!=('PUT',f'/api/records/{self.record_id}/draft'):
            raise RuntimeError('Prohibited preview recovery mutation route')
        if method!='GET':
            payload=args[0] if args else kwargs.get('payload')
            file_argument=args[1] if len(args)>1 else kwargs.get('file')
            validate_display_payload(payload,self.baseline,file_argument)
        return super().request(method,url,*args,**kwargs)

def run(record_id):
    dest=HERE/'receipts'/str(record_id)
    before_path=dest/'before.json'
    baseline=json.loads(before_path.read_text())
    patch_path=HERE/'patches'/f'{record_id}.json'
    session_path=legacy.snapshot_path(record_id,'production')
    with legacy.record_lock(record_id,'production'):
        session=json.loads(session_path.read_text())
        # Keep the exact old session and the raw guard details as distinct evidence.
        original_path=dest/'preview_repair_original_session.json'
        if not original_path.exists():
            zenodo.save_state(original_path,session)
        result=repair_owned_preview(RepairClient(record_id,baseline),record_id,baseline,patch_path,session,dest)
        session['native_staged']=result['native_staged']
        session['preview_restoration']={k:v for k,v in result.items() if k not in {'draft','native_staged'}}
        legacy.checkpoint(session_path,session,'staged')
        # A new independently verifiable recovery marker; old raw guard files untouched.
        guard={'id':record_id,'patch_sha256':result['patch_sha256'],
               'baseline_sha256':hashlib.sha256(before_path.read_bytes()).hexdigest(),
               'native_staged':result['native_staged'],'preview_state':result['state'],
               'verified_complete_draft_files_and_original_public_identity':True}
        zenodo.save_state(dest/'preview_repair_recovery.json',guard)
        return {k:v for k,v in result.items() if k not in {'draft','native_staged'}}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('record_id',type=int)
    print(json.dumps(run(parser.parse_args().record_id),indent=2))
