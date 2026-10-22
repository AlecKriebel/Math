#!/usr/bin/env python3
"""Seal/verify the bounded PR399 record URL repair and unchanged input lineage."""
from pathlib import Path,PurePosixPath
import argparse,datetime as dt,hashlib,json,os
H=Path(__file__).resolve().parent;A=H.parent;O=H/'pre_record_url_binding'
HELPERS={'ops_binding.py','prepublication_check.py','publication_live_gates.py','repository_integration.py','publication_lifecycle.py','record_publication_ledger.py','verify_published_files.py'}
OLD_SHA='53aeb70604d4f28f4986cf2e30f5cb90ccd900de7fff96a2d60bb31c03be886f'
LEAD_SHA='af763826f5e22bb64887496eada7e4aaa9c944faf45db3a0c93386b9833fbe39'

def sha(b):return hashlib.sha256(b).hexdigest()
def safe(root,name):
    if not isinstance(name,str) or not name or '\\' in name or ':' in name or '\0' in name or any(p in {'','.','..'} for p in name.split('/')):raise RuntimeError('Unsafe bound path')
    path=PurePosixPath(name)
    if path.is_absolute() or path.as_posix()!=name:raise RuntimeError('Unsafe path normalization')
    if root.is_symlink() or any(root.joinpath(*path.parts[:i]).is_symlink() for i in range(1,len(path.parts)+1)):raise RuntimeError('Symlink bound path')
    return root/name

def entry(root,name):
    p=safe(root,name);b=p.read_bytes();return {'path':name,'bytes':len(b),'sha256':sha(b)}
def verify(root,entries):
    if not isinstance(entries,list) or not entries:raise RuntimeError('Absent artifact list')
    seen=set()
    for e in entries:
        if not isinstance(e,dict) or set(e)!={'path','bytes','sha256'} or type(e['bytes']) is not int or e['bytes']<0:raise RuntimeError('Artifact entry schema')
        if e['path'] in seen or entry(root,e['path'])!=e:raise RuntimeError('Duplicate or changed artifact '+str(e.get('path')))
        seen.add(e['path'])
    return seen

def preserved():
    name='ops_identity_repair_20261021/MANIFEST.json';data=(A/name).read_bytes()
    if sha(data)!=OLD_SHA or data!=(O/name).read_bytes():raise RuntimeError('Historical156 manifest changed')
    checksum='ops_identity_repair_20261021/MANIFEST.sha256'
    if (A/checksum).read_bytes()!=(O/checksum).read_bytes() or (A/checksum).read_text()!=OLD_SHA+'  MANIFEST.json\n':raise RuntimeError('Historical checksum changed')
    old=json.loads(data)
    if len(old['files'])!=156:raise RuntimeError('Historical156 size changed')
    verify(O,old['files']);verify(A,[e for e in old['files'] if e['path'] not in HELPERS])
    extra=json.loads((H/'SUPPLEMENTAL_PRESERVATION.json').read_bytes())['files']
    if len(extra)!=64:raise RuntimeError('Supplemental inventory changed')
    verify(A,extra);verify(O,extra)
    original=json.loads((O/'publication_operations_preparation/MANIFEST.json').read_bytes())
    if len(original['files'])!=42 or len(original['immutable_inputs'])!=26:raise RuntimeError('Historical42/26 schema changed')
    # Its own old canonical-looking helper copies remain in the nested custody
    # created by the156 generation, never overwritten with later bytes.
    nested=O/'ops_identity_repair_20261021/pre_review02_binding'
    verify(nested,original['files']+original['immutable_inputs'])
    verify(A,[e for e in original['files']+original['immutable_inputs'] if e['path'] not in HELPERS])
    if sha((A/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_bytes())!=LEAD_SHA:raise RuntimeError('Root lead reconciliation changed')
    inputs=json.loads((H/'IMMUTABLE_INPUT_BINDING.json').read_bytes())['files'];verify(A,inputs)
    current=json.loads((H/'CURRENT_HELPER_BINDING.json').read_bytes())['files']
    if verify(A,current)!=HELPERS:raise RuntimeError('Current seven-helper set changed')
    summary=json.loads((H/'TEST_SUMMARY.json').read_bytes())
    if summary['helper_bindings']!=current or summary['formal_current_controls_per_mode']!=1651 or summary['actual_provider_attempts']!=0 or summary['publication_ready'] is not False:raise RuntimeError('Final test/helper binding changed')
    return inputs

def selection():
    inputs=preserved();paths=list(H.rglob('*'))
    if any(p.is_symlink() for p in paths):raise RuntimeError('Symlink in authored repair')
    excluded={H/'MANIFEST.json',H/'MANIFEST.sha256'}
    chosen=[A/n for n in HELPERS]+[p for p in paths if p.is_file() and p not in excluded and '__pycache__' not in p.parts]
    if len(chosen)!=len(set(chosen)):raise RuntimeError('Duplicate authored path')
    return sorted(chosen),inputs

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    paths,inputs=selection();manifest=H/'MANIFEST.json';checksum=H/'MANIFEST.sha256'
    if args.verify:
        data=manifest.read_bytes();value=json.loads(data)
        if checksum.read_text()!=sha(data)+'  MANIFEST.json\n':raise RuntimeError('Manifest checksum differs')
        if value['immutable_inputs']!=inputs or value['publication_ready'] is not False:raise RuntimeError('Input or clearance scope changed')
        if {e['path'] for e in value['files']}!={p.relative_to(A).as_posix() for p in paths}:raise RuntimeError('Exact authored inventory changed')
        verify(A,value['files']);verify(A,value['immutable_inputs'])
        print(json.dumps({'verified':True,'artifacts':len(value['files']),'immutable_inputs':len(inputs),'manifest_sha256':sha(data),'historical156_and42plus26_reconstructed':True,'current_controls_per_mode':1651,'publication_ready':False}));return
    if manifest.exists() or checksum.exists():raise RuntimeError('Do not rewrite a frozen checkpoint')
    value={'schema':1,'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'pr':399,'problem_id':'30001179','completion_estimate_percent':100,'publication_ready':False,'scope':'Bounded local record URL and OWR citation-role repair only; NEW complete history-free review04 and affirmative root decision required. No provider/Git/lifecycle action or clearance.','historical156_manifest_sha256':OLD_SHA,'historical42plus26_preserved':True,'root_lead_reconciliation_sha256':LEAD_SHA,'review03_repair_required_seal_sha256':'e797d9c8580b3dbaf64ca568e1a7516346269f9248eb1fdbeefb0562a06cfbbb','current_controls_per_mode':1651,'historical_counterexamples_per_mode':79,'cached_rows_separate':176,'files':[entry(A,p.relative_to(A).as_posix()) for p in paths],'immutable_inputs':inputs}
    data=(json.dumps(value,indent=2)+'\n').encode()
    for path,body in [(manifest,data),(checksum,(sha(data)+'  MANIFEST.json\n').encode())]:
        with path.open('xb') as stream:stream.write(body);stream.flush();os.fsync(stream.fileno())
    print(json.dumps({'artifacts':len(value['files']),'immutable_inputs':len(inputs),'manifest_sha256':sha(data),'publication_ready':False}))
if __name__=='__main__':main()
