#!/usr/bin/env python3
"""Authenticate real raw publication GETs and extract the exact reviewed archive."""
from pathlib import Path, PurePosixPath
from datetime import datetime,timezone
import hashlib,importlib.util,json,os,stat,sys,zipfile
A=Path(__file__).resolve().parents[1];P=A/'publication_ready_v1';D=A/'published_record_fullbody_verification_20261006'
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def now():return datetime.now(timezone.utc).isoformat()
def read(p):return json.loads(p.read_text())
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p):return {'path':p.relative_to(A).as_posix(),**hp(p.read_bytes())}
def main():
    start=now();rid=int(sys.argv[1]);doi='10.5281/zenodo.'+str(rid)
    seal=read(A/'publication_ready_v1_SEAL.json')
    for e in seal['files']:need(hp((P/e['path']).read_bytes())=={k:e[k] for k in ('bytes','sha256')},'Reviewed candidate drift')
    tool=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
    need(hashlib.sha256(tool.read_bytes()).hexdigest()=='26f264df93b657137b343acc05ae87a3e8e60d46cbbb8b822bc327d77b89c277','Repository kit source changed')
    spec=importlib.util.spec_from_file_location('zenodo_metadata_verifier',tool);z=importlib.util.module_from_spec(spec);spec.loader.exec_module(z)
    md,local=z.load_manifest(P/'zenodo-deposit.json')
    depo=read(D/'actual_deposition_get.json');record=read(D/'actual_record_get.json')
    z.validate_record(depo,rid);need(depo['submitted'] is True,'Actual deposition not published')
    depo_normalizations=z.verify(depo,md,local)
    need(record['id']==rid and record['doi']==doi and (record.get('submitted') is True or record.get('is_published') is True),'Public record identity/state')
    publicmd=dict(record['metadata']);rt=publicmd['resource_type']
    need(rt['type']==md['upload_type'] and rt['subtype']==md['publication_type'] and publicmd['license']['id']==md['license'],'Public metadata type/license representation')
    publicmd['upload_type']=rt['type'];publicmd['publication_type']=rt['subtype'];publicmd['license']=publicmd['license']['id']
    public_normalizations=z.verify({'metadata':publicmd,'files':record['files']},md,local)
    operations={};requests={};pids=[]
    labels={'deposition':'zenodo_deposition_GET_20261006','metadata':'zenodo_record_GET_20261006','PDF':'zenodo_pdf_content_GET_20261006','ZIP':'zenodo_zip_GET_20261006'}
    filenames={'deposition':'actual_deposition_get.json','metadata':'actual_record_get.json','PDF':'focal_antipedal_sum.pdf','ZIP':'focal_antipedal_sum_support.zip'}
    for role,label in labels.items():
        op=A/'actual_operations'/label;ex=read(op/'execution.json');h=read(D/(filenames[role]+'.HTTP_RECEIPT.json'));body=(D/filenames[role]).read_bytes()
        need(ex['exit_code']==0 and ex['reaped'] is True and ex['termination']['signal'] is None and ex['stderr']['bytes']==0,'Actual transport process failed')
        need(ex['child_PID']==h['actual_process_PID'] and ex['environment_sha256']==h['environment_sha256'],'Actual HTTP/process PID/environment binding')
        need(ex['UTC_start']<=h['UTC_start']<=h['UTC_end']<=ex['UTC_end'],'Actual HTTP/process chronology')
        need(h['HTTP_status']==200 and h['method']=='GET' and h['record_id']==rid and h['transport_body']=={'path':filenames[role],**hp(body)},'Actual HTTP/body identity')
        out=(op/'stdout.bin').read_bytes();err=(op/'stderr.bin').read_bytes()
        need(hp(out)=={k:ex['stdout'][k] for k in ('bytes','sha256')} and hp(err)=={k:ex['stderr'][k] for k in ('bytes','sha256')},'Actual CLI stream pins')
        if role in ('metadata','deposition'):need(out==body,'Metadata stdout is not exact raw HTTP body')
        else:need(json.loads(out)=={'response_bytes':len(body),'response_sha256':hashlib.sha256(body).hexdigest()} and body==(P/filenames[role]).read_bytes(),'File summary/body/full local equality')
        norm={'actual_receipt':True,'template_only':False,'PID':ex['child_PID'],'exit_code':0,'argv':ex['argv'],'cwd':ex['cwd'],
          'environment_sha256':ex['environment_sha256'],'UTC_start':ex['UTC_start'],'UTC_end':ex['UTC_end'],
          'stdout':pin(op/'stdout.bin'),'stderr':pin(op/'stderr.bin'),'reaped':True,'termination_reason':None,
          'HTTP_method':'GET','status_code':200,'URL':h['request_url'],'response_bytes':len(body),'response_sha256':hashlib.sha256(body).hexdigest(),
          'raw_execution':pin(op/'execution.json'),'raw_HTTP_receipt':pin(D/(filenames[role]+'.HTTP_RECEIPT.json'))}
        operations[role]=norm;requests[role]=h;pids.append(ex['child_PID'])
    need(len(set(pids))==4,'Distinct genuine transport CLI processes')
    need(operations['metadata']['UTC_end']<=operations['PDF']['UTC_start'] and operations['PDF']['UTC_end']<=operations['ZIP']['UTC_start'],'Actual record before file readbacks')
    E=D/'extracted';need(not E.exists(),'Unique extracted publication directory');E.mkdir()
    inventory={e['path']:e for e in seal['files'] if e['path']!='focal_antipedal_sum_support.zip'};logical={}
    with zipfile.ZipFile(D/'focal_antipedal_sum_support.zip') as archive:
        infos=archive.infolist();need(len(infos)==len(inventory)==33 and {e.filename for e in infos}==set(inventory) and not archive.testzip(),'Exact remote archive scope/CRC')
        for entry in infos:
            name=entry.filename;p=PurePosixPath(name);mode=entry.external_attr>>16
            need(not p.is_absolute() and '..' not in p.parts and p.as_posix()==name and not entry.is_dir() and not stat.S_ISLNK(mode) and not entry.flag_bits&1,'Unsafe remote archive entry')
            body=archive.read(entry);need(hp(body)=={k:inventory[name][k] for k in ('bytes','sha256')} and body==(P/name).read_bytes(),'Full remote logical member mismatch')
            dest=E/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(body)
            logical[name]={'body':pin(dest),'transport':'zip_member','transport_body':pin(D/'focal_antipedal_sum_support.zip'),'member_path':name,'GET':operations['ZIP']}
    logical['focal_antipedal_sum.pdf']={'body':pin(D/'focal_antipedal_sum.pdf'),'transport':'individual_file','transport_body':pin(D/'focal_antipedal_sum.pdf'),'GET':operations['PDF']}
    normalized={'schema':'pr110-actual-publication-receipt/v1','actual_receipt':True,'template_only':False,'PR':110,'problem_id':5100032,
      'original_head':'3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35','DOI':doi,'package_manifest_sha256':hashlib.sha256((P/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest(),
      'published':True,'metadata_GET':operations['metadata'],'logical_readbacks':logical}
    (D/'PUBLICATION_RECEIPT.json').write_text(json.dumps(normalized,indent=2,sort_keys=True)+'\n')
    result={'schema':'pr110-actual-publication-fullbody-authentication/v1','actual_root_PID':os.getpid(),'UTC_start':start,'UTC_end':now(),
      'record_id':rid,'DOI':doi,'record_url':'https://zenodo.org/records/'+str(rid),'published':True,'source_package_unchanged':True,
      'deposition_exact_kit_metadata_verification':True,'public_record_exact_kit_metadata_verification':True,
      'public_API_representation_mapping':['resource_type.type -> upload_type','resource_type.subtype -> publication_type','license.id -> license'],
      'deposition_metadata_normalizations':depo_normalizations,'public_metadata_normalizations':public_normalizations,
      'actual_transport_processes':operations,'raw_deposition':pin(D/'actual_deposition_get.json'),'raw_public_record':pin(D/'actual_record_get.json'),
      'full_PDF_ZIP_bytes_match':True,'full_logical_archive_members_checked':33,'publication_receipt':pin(D/'PUBLICATION_RECEIPT.json'),
      'tracker_pending':True,'native_integration_pending':True,'workflow_completion_percent':75}
    (D/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='actual_transport_processes'},indent=2))
if __name__=='__main__':main()
