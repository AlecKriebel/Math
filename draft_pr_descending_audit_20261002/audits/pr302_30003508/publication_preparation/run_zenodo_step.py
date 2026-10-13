"""One authorized production kit operation; any uncertainty requires readback."""
from publication_guard import *
import argparse

def identity(record,required):
    require(type(record['id'])==int and record['id']>0,'Invalid exact record ID')
    doi='10.5281/zenodo.'+str(record['id'])
    if required or record.get('doi') is not None:
        require(record['doi']==doi and record['doi_url']=='https://doi.org/'+doi,'DOI/record mismatch')
    if required or record.get('record_url') is not None:
        require(record['record_url']=='https://zenodo.org/records/'+str(record['id']),'Record URL mismatch')

def require_published(record):
    identity(record,True);metadata=load(F/'record_metadata.json')
    require(record['environment']=='production' and record['state']=='published' and record['title']==metadata['title'],'Actual published production/title/state differs')
    files=record['files'];names={'spectral_tensor_consistency.pdf','spectral_tensor_verification.zip'}
    require(type(files)==list and len(files)==2 and {x['name'] for x in files}==names,'Exact published two-file list required')
    for row in files:
        b=(F/row['name']).read_bytes();require(len(b)==row['size'] and sha(b)==row['sha256'],'Published inspected file size/hash differs')
    return record

def inspected_publication():
    record=require_published(load(OUT/'inspect_published_receipt.json'))
    argv=[PYTHON,'-E','-B',str(KIT),'inspect',str(F/'zenodo-deposit.json'),'--check-doi']
    out,err,native=authenticate_execution('inspect_published',argv)
    require(json.loads(out)==record and not err,'Actual inspected production outcome differs from complete native stream')
    return record

def main():
    ap=argparse.ArgumentParser();ap.add_argument('step',choices=['stage','inspect_draft','publish','inspect_published']);args=ap.parse_args()
    lock=acquire();clear=clearance();step=args.step
    output=OUT/(step+'_receipt.json');require(not output.exists(),'An actual prior result already exists')
    command={'stage':'stage','inspect_draft':'inspect','publish':'publish','inspect_published':'inspect'}[step]
    argv=['/opt/homebrew/bin/python3','-E','-B',str(R/'zenodo_deposit_tool/zenodo.py'),command,str(F/'zenodo-deposit.json')]
    staged=None
    if step!='stage':
        staged=load(OUT/'stage_receipt.json');require(staged['environment']=='production' and type(staged['id'])==int,'Actual production draft required')
        if step=='publish':
            draft=load(OUT/'inspect_draft_receipt.json');require(draft['id']==staged['id'] and draft['state']=='ready_to_publish','Exact inspected draft required')
            argv+=['--confirm-id',str(staged['id'])]
        elif step=='inspect_published':argv+=['--check-doi']
    clearance();record,actual=execute(step,argv)
    identity(record,step in ('publish','inspect_published'))
    metadata=load(F/'record_metadata.json')
    require(record['environment']=='production' and record['title']==metadata['title'],'Production identity/metadata differs')
    require(len(record['files'])==2 and {x['name'] for x in record['files']}=={'spectral_tensor_consistency.pdf','spectral_tensor_verification.zip'},'Exact two upload files required')
    for row in record['files']:
        b=(F/row['name']).read_bytes();require(len(b)==row['size'] and sha(b)==row['sha256'],'Actual remote files differ')
    require(record['state']==('published' if step in ('publish','inspect_published') else 'ready_to_publish'),'Actual publication state differs')
    if staged:require(record['id']==staged['id'],'Record changed between operations')
    clearance();write(output,record)
    print(json.dumps(dict(record,actual_operation_PID=actual['actual_PID']),indent=2))
if __name__=='__main__':main()
