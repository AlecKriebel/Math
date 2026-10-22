"""Explicit authenticated final-candidate assembly; no Git or publication action."""
from pathlib import Path
import datetime,hashlib,json,stat

HERE=Path(__file__).absolute().parent
A=HERE.parent
CANDIDATE=A/'candidate'
def require(ok,message):
    if not ok:raise ValueError(message)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
toolraw=(A/'publication_tools_01/portable.py').read_bytes()
require(pin(toolraw)=={'bytes':44752,'sha256':'bcaac73bf1620098e0d24f2a2cb9399613567be6018b99329c0a58b6e0101910'},'frozen launcher changed')
m={'__name__':'frozen_portable_API','__file__':str(A/'publication_tools_01/portable.py')}
exec(compile(toolraw,m['__file__'],'exec',optimize=0),m)
read=m['read_regular'];parse=m['strict_json'];safe=m['safe_name']
FAMILIES=[
 ('geometry_audit_01','SAFE_PAYLOAD_MANIFEST.json',9,1836,'e41107e83541337050cf1d86bbbd57163dca3a19ea460ed657c3bbb6ed9c1cd8'),
 ('minimizer_audit_01','SAFE_PAYLOAD_MANIFEST.json',8,1764,'adf85d42c6070f3f043c87d6687e1221e6c41465d7ecd06ecc06e2f82e98a518'),
 ('rank_audit_01','SAFE_PAYLOAD_MANIFEST.json',7,2242,'3d9ad20866c7707f26ae7c97abade9ba12d9abc1c9a558385f40ad7288f0c83e'),
 ('artifact_audit_01','SAFE_MANIFEST.json',17,3404,'759f375ce2f2ba897a0b8cd344b2b3d4c20da42ca5905d2ad1123210a7d7d8af'),
 ('priority_classical_01','SAFE_MANIFEST.json',10,1768,'3f10fdf0401ede8c0e7476c943d7f425459d057c57c8d6ebf37f2a0f12c7824e'),
 ('priority_recent_01','SAFE_PAYLOAD_MANIFEST.json',10,1937,'ab1892b46f8eca5ba5a24532da132008c139c5c97bf38a254e776331c9931b69'),
 ('note_math_review_01','DELIVERABLE_MANIFEST.json',5,1208,'89d3212039582b9bcdfc550b83c9b19e0f3401b26694b2966ab46a291b22adce'),
 ('publication_tools_01','SAFE_PAYLOAD_MANIFEST.json',17,2919,'c9aa60cab50dc3498c346aab5a417664bb0ccc49c9c8defa82e2bb1950cf15d0'),
 ('format_review_01','SAFE_MANIFEST.json',17,3684,'2187e82e1e8c26e66122c30aabf46e114bf89c421249415f1c9d928c8676b256'),
]
PAPER={
 'note.tex':(17432,'58fc08b947c20e4d00fb6a379a109e8489aa6a22b1f2161587980ada95c318bc'),
 'rank-two-fano-note.pdf':(81144,'38b4897c731fe9916a7ae8eaf3cb6c62352631f24776b9b93f9af61807ab0060'),
 'metadata.json':(4213,'a1ad1976efd1680dd626714ed7c659ab6f372b7dd305ba816465ee355a677618'),
 'zenodo-deposit.json':(4532,'aea4f16050e959a4a8c4d075f70e54626a1b7fcae51ec489698cfcbcfee1244d'),
}
ROOT_INPUTS=['ROOT_NATIVE_RECEIPT.json','PRIMARY_FETCH_RECEIPT.json','ROOT_SCOPE_RECONSTRUCTION.md','MATHEMATICAL_DISPOSITION.json','PROOF_READER_CLARIFICATIONS.md','FINAL_PRIORITY_DISPOSITION.json','FINAL_PRIORITY_DISPOSITION.md','NOTE_TOOL_FORMAT_PARENT_READBACK.json','PREPRINT_EDITORIAL_DELTA.json','preprint/PDF_BUILD_RECEIPT.json','preprint/PDF_QA_RECEIPT.json']

def main():
    require(not CANDIDATE.exists() and not CANDIDATE.is_symlink(),'candidate must be new')
    portable={};families=[];rootpins=[]
    manifest=read(A/'SOURCE_MANIFEST.json',5587)
    require(pin(manifest)['sha256']=='49a72d6bf90d3a74be69ed855c7a9cfc0f3b1d83a4e4e3ce997c0ca7c07d1cbc','source manifest external pin')
    source_index=parse(manifest);source={}
    m['closed_tree'](A/'source',{r['path'] for r in source_index['files']})
    for row in source_index['files']:
        name=safe(row['path']);raw=read(m['within'](A/'source',name),row['bytes'])
        require(pin(raw)=={k:row[k] for k in ('bytes','sha256')},'source input pin')
        source[name]=raw;portable['source/'+name]=raw
    portable['root_evidence/SOURCE_MANIFEST.json']=manifest
    portable['SOURCE_MANIFEST.json']=manifest
    m['original_inputs'](portable)
    for folder,envelope,count,size,digest in FAMILIES:
        raw=read(A/folder/envelope,size);require(pin(raw)['sha256']==digest,'family external manifest pin: '+folder)
        value=parse(raw);rows=m['rows_map'](value['files']);require(len(rows)==count,'family safe count')
        for name,row in rows.items():
            require(name!=envelope,'family manifest must be self-excluded')
            payload=read(m['within'](A/folder,name),row['bytes'])
            require(pin(payload)=={k:row[k] for k in ('bytes','sha256')},'family safe payload pin: '+folder+'/'+name)
            if name.endswith('.json'):parse(payload)
            target=folder+'/'+name;require(target not in portable,'portable collision');portable[target]=payload
        portable[folder+'/'+envelope]=raw
        families.append({'folder':folder,'envelope':envelope,'payload_count':count,'envelope_pin':pin(raw)})
    for name in ROOT_INPUTS:
        path=A/name
        if not path.exists():
            rootpins.append({'requested':name,'status':'OMITTED_NONEXISTENT'});continue
        raw=read(path);target='root_evidence/'+name
        if name.endswith('.json'):parse(raw)
        portable[target]=raw;rootpins.append({'input':name,'path':target,**pin(raw)})
    paper={}
    for name,(size,digest) in PAPER.items():
        raw=read(A/'preprint'/name,size);require(pin(raw)['sha256']==digest,'parent paper pin: '+name);paper[name]=raw
    readme=read(HERE/'PACKAGE_README.md')
    portable.update({'portable.py':toolraw,'dependencies.json':read(A/'publication_tools_01/dependencies.json'),'README.md':readme,**{n:paper[n] for n in ('note.tex','metadata.json','zenodo-deposit.json')}})
    m['publication_metadata'](portable)
    # No private bodies or outputs are accepted by broad recursive copying.
    for name,raw in portable.items():
        safe(name)
        require(not any(p in ('private_tmp','private_sources','private_native','wheels','runtime','__pycache__','.git') for p in name.split('/')),'private directory in portable')
        require(not name.endswith(('.pdf','.whl','.pyc','.pyo','.so','.dylib','.pyd','.png','.jpg')),'private/binary body in portable')
        require(all(t not in raw for t in (b'/' + b'Users' + b'/' + b'alec' + b'/',b'/' + b'var' + b'/' + b'folders' + b'/',b'/' + b'private' + b'/' + b'var' + b'/' + b'folders' + b'/',b'/home/alec/')),'personal absolute path in portable: '+name)
    index={'schema':m['PACKAGE_SCHEMA'],'problem_id':'30005079','files':[{'path':n,**pin(b)} for n,b in sorted(portable.items())]}
    raw=(json.dumps(index,indent=2,sort_keys=True)+'\n').encode();portable['package_index.json']=raw
    outer=dict(source);outer['README.md']=readme
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    checkpoint=('\n\n## '+now+' — Current publication candidate assembly\n\nCompletion estimate:60% toward the current review/publication stage. Original research effort1/5 is unchanged. The complete original21files are preserved under verification/source/. The actual new note and explicitly authenticated safe audit evidence were assembled. Software replay and independent ZIP reconstruction are being checked separately; whole-package reviews and publication approval remain parent-owned. No external individual was contacted.\n').encode()
    outer['RESEARCH_LOG.md']=source['RESEARCH_LOG.md']+checkpoint
    outer.update({'portable.py':toolraw,**paper})
    outer['CURRENT_PUBLICATION.json']=(json.dumps({'schema':m['LAYOUT_SCHEMA'],'problem_id':'30005079','portable_prefix':'verification','zip_path':'rank-two-fano-verification.zip','pdf_path':'rank-two-fano-note.pdf','tex_path':'note.tex'},indent=2,sort_keys=True)+'\n').encode()
    outer.update({'verification/'+n:b for n,b in portable.items()})
    m['materialize'](CANDIDATE,outer)
    receipt={'timestamp_utc':now,'completion_estimate_percent':45,'status':'ASSEMBLED_AWAITING_DEFAULT_BUILD_AND_CURRENT_REPLAYS','scope':'Explicit final candidate assembly only; no mathematical, priority, whole-package or publication verdict.','tool':pin(toolraw),'paper_inputs':{n:pin(b) for n,b in paper.items()},'families':families,'safe_family_payload_count':sum(r['payload_count'] for r in families),'safe_family_envelopes':len(families),'original_source_files':len(source),'original_source_bytes':sum(map(len,source.values())),'original_effort':'1/5','root_evidence_inputs':rootpins,'portable_files_including_self_excluded_index':len(portable),'package_index':pin(raw),'outer_before_final_ZIP_and_manifest_files':len(outer),'outer_original_changes_only':['README.md replaced with current commands/scope','RESEARCH_LOG.md appended dated60% checkpoint'],'candidate_writes_fresh_no_overwrite':True,'historical_reports_preserved_as_dated_snapshots':True}
    (HERE/'ASSEMBLY_INPUT_AUTHENTICATION.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':receipt['status'],'portable_files':len(portable),'outer_files':len(outer),'package_index':pin(raw)},indent=2))

if __name__=='__main__':main()
