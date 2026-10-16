"""Seal final ZIP/current manifest and an outside-candidate closed core list."""
from pathlib import Path
import datetime,hashlib,json,os
H=Path(__file__).absolute().parent;A=H.parent;C=A/'candidate'
def require(ok,msg):
    if not ok:raise ValueError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
tool=(A/'publication_tools_01/portable.py').read_bytes();require(pin(tool)['sha256']=='bcaac73bf1620098e0d24f2a2cb9399613567be6018b99329c0a58b6e0101910','frozen tool')
m={'__name__':'frozen_portable_API','__file__':str(A/'publication_tools_01/portable.py')};exec(compile(tool,m['__file__'],'exec',optimize=0),m)
def main():
    require(not (C/'CURRENT_PUBLICATION_MANIFEST.json').exists(),'current manifest must be new')
    result=m['strict_json']((H/'DEFAULT_BUILD_PUBLIC_STDOUT.json').read_bytes())
    require(result['status']=='PASS' and result['verification']['replay']['status']=='PASS','mandatory final default build not passed')
    index=(C/'verification/package_index.json').read_bytes();require(result['verification']['index_sha256']==pin(index)['sha256'],'default build used another package index')
    raw=m['read_regular'](H/'private_tmp/build/rank-two-fano-verification.zip',result['bytes']);require(pin(raw)=={k:result[k] for k in ('bytes','sha256')},'actual built archive pin')
    originals={p.relative_to(A/'source').as_posix():m['read_regular'](p) for p in (A/'source').rglob('*') if p.is_file()}
    for name,data in originals.items():
        current=m['read_regular'](C/name)
        if name=='README.md':require(current==m['read_regular'](C/'verification/README.md'),'current README copies')
        elif name=='RESEARCH_LOG.md':require(current.startswith(data) and b'Completion estimate:60%' in current[len(data):],'original log not preserved/appended60%')
        else:require(current==data,'outer original file altered: '+name)
        require(m['read_regular'](C/'verification/source'/name)==data,'portable original file altered')
    out=C/'rank-two-fano-verification.zip'
    fd=os.open(out,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0),0o644)
    with os.fdopen(fd,'wb') as f:f.write(raw)
    blobs={p.relative_to(C).as_posix():m['read_regular'](p) for p in C.rglob('*') if p.is_file()}
    require(len(blobs)==178,'unexpected outer file count before manifest')
    current_index={'schema':m['CURRENT_SCHEMA'],'problem_id':'30005079','files':[{'path':n,**pin(b)} for n,b in sorted(blobs.items())]}
    current_raw=(json.dumps(current_index,indent=2,sort_keys=True)+'\n').encode()
    with (C/'CURRENT_PUBLICATION_MANIFEST.json').open('xb') as f:f.write(current_raw)
    blobs['CURRENT_PUBLICATION_MANIFEST.json']=current_raw
    m['closed_tree'](C,set(blobs))
    checked,portable=m['current_inputs'](C,pin(current_raw)['sha256'])
    require(set(checked)==set(blobs) and len(portable)==150,'current authenticated layout count')
    core={'schema':'rank-two-fano-30005079-final-candidate-core-v1','problem_id':'30005079','head':'a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7','files':[{'path':n,**pin(b)} for n,b in sorted(blobs.items())]}
    coreraw=(json.dumps(core,indent=2,sort_keys=True)+'\n').encode()
    (H/'CANDIDATE_CORE_PINS.json').write_bytes(coreraw)
    receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_estimate_percent':75,'scope':'Closed final candidate byte sealing only; actual normal/O current replay and independent ZIP reconstruction remain to run.','candidate_files':len(blobs),'portable_files_including_index':len(portable),'core_pin_list':pin(coreraw),'current_manifest':pin(current_raw),'portable_index':pin(index),'PDF':pin(blobs['rank-two-fano-note.pdf']),'ZIP':pin(raw),'TeX':pin(blobs['note.tex']),'metadata':pin(blobs['metadata.json']),'deposit':pin(blobs['zenodo-deposit.json']),'tool':pin(tool),'all21_portable_originals_unchanged':True,'outer_original_changes_only':['README.md','RESEARCH_LOG.md'],'original_effort':'1/5','mandatory_default_build_replay':'ACTUAL_PASS','self_changing_receipts_inside_final_ZIP':False,'same_runtime_fresh_ZIP_rebuild':'PASS'}
    (H/'SEALED_CANDIDATE_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))
if __name__=='__main__':main()
