#!/usr/bin/env python3
"""PR894 implementation-only two-stage assembler. No subprocess execution.

Parent must authenticate this program, supply final pinned inputs, capture a
genuine full-replay portable.py build, and review the completed candidate.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
TOOL_SHA = 'a5b5ab7a3b0397e1d21bd70d3637ef1e200a7eba50419c0052e357b46a0e1d9c'
SOURCE_SHA = '1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c'
ROOT_SHA = '8e9fba86534cfb75167f9b47a24206d6ca2e03ada94c91725b9023dd026e125b'
RESULT_SHA = '2a0062610f5116c92c3689cbb2d12747260d0f42664a277cbb41aee3424046ff'
ENVELOPES = {
    'global_action_audit_01': (4173, '8e31bc656f0551e97e34e21235130685df007e3ce880ec1316af143712dc26e1', 25),
    'topology_audit_01': (4451, '2651ac14f3d691e65022244b8b70477bbcaab34488d320726bd8d9789abfa7d4', 26),
    'algebra_audit_01': (3885, '9fe64e75b8b36b31851ecedb6364881c33ddb21af1f723baee732a8d1ac4f3f2', 21),
    'artifact_audit_01': (6424, '2929eb25058552fb7fa9401d1214d07998c254b205325a1b4590f4e45ca5c696', 37),
    'priority_classical_01': (3522, 'c57790bcd6a18dedf43a8d5a0f4ebb961153a2853bd8132b07d923950fe06525', 21),
    'priority_recent_01': (2661, '46df79bf24fbe51098680e8c5ab22d230e89c6c8da27b24eddb47020d0bd8424', 15),
    'publication_tools_01': (4062, '179b1a05f8fb8f3243a171e8a3a584423ee75f373cfbf6280a7c7d7636a59310', 20),
    'format_review_01': (2988, 'fa77e04a4d5cdb6d046bed268e80ae110bcebc7c4c5fd60e6d2e6ee4fb2b63d6', 16),
}
REQUIRED_RECEIPTS = {
    'SOURCE_MANIFEST.json', 'ROOT_NATIVE_RECEIPT.json', 'ROOT_SCOPE_AND_VALIDATION_PLAN.md',
    'PRIMARY_SCOPE_PARENT_READBACK.json', 'PRIMARY_FETCH_RECEIPTS.json',
    'ROOT_ORIGINAL_REPLAY_RECEIPT.json', 'MATH_DISPOSITION.json',
    'MATH_FAMILY_PARENT_READBACK.json', 'ARTIFACT_PARENT_READBACK.json',
    'FINAL_PRIORITY_DISPOSITION.json', 'PRIORITY_PARENT_FRESH_FETCH.json',
    'PRIORITY_PARENT_KOSZUL_NEW_BODY.json', 'TOOL_FORMAT_PARENT_READBACK.json',
    'NOTE_EDITORIAL_DISPOSITION.json', 'PDF_BUILD_RECEIPT.json', 'PDF_RENDER_RECEIPT.json',
    'PDF_VISUAL_QA.json', 'EDITOR_COMPILE_RECEIPT.json',
}
OPTIONAL_RECEIPTS = {'ROOT_CLASSICAL_TOPOLOGY_SOURCE_NOTE.json', 'ROOT_CLASSICAL_TOPOLOGY_SOURCE_NOTE.md'}
PAPER_NAMES = {'note.tex', 'metadata.json', 'zenodo-deposit.json', 'post-lie-note.pdf'}
PACKAGE_SCHEMA = 'post-lie-30005737-verification-v1'
CURRENT_SCHEMA = 'post-lie-30005737-current-publication-v1'
MAX_FILE, MAX_TOTAL = 256*1024*1024, 512*1024*1024

def require(ok, why):
    if not ok: raise ValueError(why)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def pin(raw): return {'bytes':len(raw), 'sha256':sha(raw)}
def encoded(obj): return (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
def strict_json(raw):
    def pairs(items):
        out={}
        for k,v in items: require(k not in out,'duplicate JSON key');out[k]=v
        return out
    def finite(v):
        x=float(v);require(math.isfinite(x),'nonfinite/overflow JSON');return x
    def reject(v): raise ValueError('nonfinite JSON constant')
    return json.loads(raw,object_pairs_hook=pairs,parse_float=finite,parse_constant=reject)
def digest(value):
    require(type(value) is str and re.fullmatch('[0-9a-f]{64}',value),'lowercase SHA256 required');return value
def safe(name):
    require(type(name) is str and 0<len(name)<=512 and re.fullmatch('[A-Za-z0-9_./-]+',name),'ASCII relative path required')
    require(all(p not in ('','.','..') for p in name.split('/')) and not PurePosixPath(name).is_absolute(),'unsafe path')
    return name
def root(path):
    path=path.absolute()
    for p in (path,*path.parents): require(stat.S_ISDIR(p.lstat().st_mode),'nonsymlink ordinary directory required')
    return path.resolve()
def path_within(folder,name):
    safe(name)
    for p in PurePosixPath(name).parents:
        if str(p)!='.': require(stat.S_ISDIR((folder/str(p)).lstat().st_mode),'symlink/non-directory input ancestor')
    return folder/name
def read(path, size=None):
    info=path.lstat();require(stat.S_ISREG(info.st_mode),'regular input required')
    require(info.st_size<=MAX_FILE and (size is None or info.st_size==size),'input size mismatch/limit')
    fd=os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)|getattr(os,'O_NONBLOCK',0))
    with os.fdopen(fd,'rb') as f:
        actual=os.fstat(f.fileno());require((actual.st_dev,actual.st_ino)==(info.st_dev,info.st_ino),'input changed during open')
        raw=f.read(info.st_size+1);after=os.fstat(f.fileno())
        require(len(raw)==info.st_size and (actual.st_size,actual.st_mtime_ns)==(after.st_size,after.st_mtime_ns),'input changed during read')
    return raw
def authenticate(raw,row): require(pin(raw)=={k:row[k] for k in ('bytes','sha256')},'input byte pin mismatch: '+row.get('path','input'))
def rows(items, source=False):
    require(type(items) is list and 0<len(items)<=10000,'nonempty bounded rows required')
    out={};aliases=set();dirs={}
    for item in items:
        require(type(item) is dict and set(item)==({'source','path','bytes','sha256'} if source else {'path','bytes','sha256'}),'exact row schema')
        n=safe(item['path']);digest(item['sha256'])
        require(type(item['bytes']) is int and 0<=item['bytes']<=MAX_FILE,'typed byte count')
        if source:safe(item['source'])
        require(n.casefold() not in aliases,'duplicate/case-aliased row');aliases.add(n.casefold());out[n]=item
    for n in out:
        for p in PurePosixPath(n).parents:
            if str(p)=='.':continue
            k=str(p).casefold();require(k not in aliases,'file/directory collision')
            require(k not in dirs or dirs[k]==str(p),'directory spelling alias');dirs[k]=str(p)
    require(sum(x['bytes'] for x in items)<=MAX_TOTAL,'aggregate size limit')
    return out
def public(name,raw, pdf=False, historical_zip=False):
    # Accepted safe envelopes may contain their curated stdout excerpts. Never
    # copy any unlisted/private process stream, primary body, wheel or runtime.
    safe(name)
    require(not any(p.lower() in {'private_tmp','private_native','private_sources','__pycache__','site-packages','wheels','runtime','rendered_pages'} for p in PurePosixPath(name).parts),'private/runtime subtree forbidden')
    require(not name.lower().endswith(('.whl','.pyc','.so','.dylib','.gz','.xz','.zst')),'runtime/compressed raw material forbidden')
    if name.endswith('.pdf'):
        require(pdf and name=='post-lie-note.pdf','only separate current paper PDF allowed');return
    if name.endswith('.zip'):
        require(historical_zip,'unapproved archive forbidden');return
    for marker in (b'/Users/',b'/home/',b'/private/var/',b'/var/folders/',b'BEGIN PRIVATE KEY',b'github_pat_',b'ghp_'):
        require(marker not in raw,'private-path/credential marker in '+name)
    if name.endswith('.json'):strict_json(raw)
    if name.endswith('.jsonl'):
        for line in raw.splitlines():
            if line.strip():strict_json(line)
def add(blobs,name,raw):
    safe(name);require(name not in blobs or blobs[name]==raw,'output collision');blobs[name]=raw
def envelope(folder, expected_sha, expected_size=None, expected_count=None):
    folder=root(folder);raw=read(folder/'SAFE_MANIFEST.json');digest(expected_sha)
    require(sha(raw)==expected_sha and (expected_size is None or len(raw)==expected_size),'external safe manifest pin mismatch')
    obj=strict_json(raw);require(type(obj) is dict and 'files' in obj,'safe manifest files missing')
    listed=rows(obj['files']);require('SAFE_MANIFEST.json' not in listed,'self-listed safe manifest')
    require(expected_count is None or len(listed)==expected_count,'safe envelope row count')
    blobs={}
    # Full manifest and every listed blob authenticate before returning/copying.
    for name,row in listed.items():
        data=read(path_within(folder,name),row['bytes']);authenticate(data,row);public(name,data);blobs[name]=data
    blobs['SAFE_MANIFEST.json']=raw
    return blobs
def index(blobs,schema):
    return encoded({'schema':schema,'problem_id':'30005737','files':[dict(path=n,**pin(raw)) for n,raw in sorted(blobs.items())]})
def inventory(folder):
    folder=root(folder);out={}
    def visit(p,prefix=''):
        entries=list(os.scandir(p));require(entries or p==folder,'empty directory forbidden')
        for e in entries:
            n=safe(prefix+e.name);mode=e.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):visit(Path(e.path),n+'/')
            else:require(stat.S_ISREG(mode),'nonregular candidate entry');out[n]=read(Path(e.path))
    visit(folder);rows([dict(path=n,**pin(raw)) for n,raw in out.items()]);return out
def write_new(path,raw):
    with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    path.chmod(0o644)
def materialize(folder,blobs):
    folder.mkdir()
    for n,raw in sorted(blobs.items()):
        p=folder/n;p.parent.mkdir(parents=True,exist_ok=True);write_new(p,raw)
def zip_bytes(blobs):
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for n,raw in sorted(blobs.items()):
            i=zipfile.ZipInfo(safe(n),(2026,10,16,0,0,0));i.create_system=3;i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(i,raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    return out.getvalue()
def fixed_metadata(blobs):
    m=strict_json(blobs['metadata.json']);d=strict_json(blobs['zenodo-deposit.json'])
    keys={'title','upload_type','publication_type','publication_date','version','description','creators','access_right','license','keywords','references','related_identifiers'}
    require(type(m) is dict and set(m)==keys,'metadata exact schema')
    for k,v in {'title':'Post-Lie nonexistence with a semisimple target','upload_type':'publication','publication_type':'preprint','publication_date':'2026-10-16','version':'1.0.0','access_right':'open','license':'cc-by-4.0'}.items():require(type(m[k]) is str and m[k]==v,'fixed metadata identity')
    require(m['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'sole creator identity')
    require(type(m['description']) is str and m['description'] and 'NOT ACTUAL PAPER' not in m['description'].upper(),'actual editorial description required')
    require(type(d) is dict and set(d)=={'metadata','files'} and d['metadata']==m,'deposit metadata exact copy')
    require(d['files']==[{'name':'post-lie-note.pdf','path':'post-lie-note.pdf'},{'name':'post-lie-verification.zip','path':'post-lie-verification.zip'}],'exact two deposit assets')
    require(b'NOT ACTUAL PAPER' not in blobs['note.tex'].upper(),'actual paper TeX required')
    require(blobs['post-lie-note.pdf'].startswith(b'%PDF-'),'PDF header only; parent PDF receipts required separately')
def input_plan(path,expected):
    digest(expected);raw=read(path);require(sha(raw)==expected,'parent input-plan pin mismatch')
    obj=strict_json(raw);require(type(obj) is dict and set(obj)=={'schema','paper','root_receipts'} and obj['schema']=='pr894-parent-assembly-inputs-v1','parent input plan schema')
    paper=rows(obj['paper']);receipts=rows(obj['root_receipts'],source=True)
    require(set(paper)==PAPER_NAMES,'exact four authoritative preprint files')
    require(REQUIRED_RECEIPTS<=set(receipts)<=REQUIRED_RECEIPTS|OPTIONAL_RECEIPTS,'explicit curated root receipt set required')
    require(len(set(receipts)&OPTIONAL_RECEIPTS)<=1,'select one classical source-note spelling')
    for name,row in receipts.items():
        allowed={name}
        if name in {'NOTE_EDITORIAL_DISPOSITION.json','PDF_BUILD_RECEIPT.json','PDF_RENDER_RECEIPT.json','PDF_VISUAL_QA.json','EDITOR_COMPILE_RECEIPT.json'}:allowed.add('preprint/'+name)
        require(row['source'] in allowed,'receipt source must be explicit approved root/preprint path')
    return raw,paper,receipts
def prepare(args):
    # No directory creation until ALL input bodies, safe envelopes and templates
    # have authenticated. No archival execution occurs in either subcommand.
    source_root=root(BASE/'source');preprint=root(args.preprint_dir)
    require(preprint==root(BASE/'preprint'),'authoritative preprint directory must be parent preprint')
    plan,paper_rows,receipt_rows=input_plan(args.inputs,args.inputs_sha256)
    safe_envelopes={n:envelope(BASE/n,h,size,count) for n,(size,h,count) in ENVELOPES.items()}
    if args.noteauthor_manifest_sha256:
        author_root=root(args.noteauthor_dir)
        require(author_root.parent==root(BASE) and author_root.name in {'noteauthor_01','note_author_01'},'explicit parent note-author folder required')
        noteauthor=envelope(author_root,args.noteauthor_manifest_sha256,expected_count=6)
    else:noteauthor=None
    sm=read(BASE/'SOURCE_MANIFEST.json');require(len(sm)==4654 and sha(sm)==SOURCE_SHA,'immutable source manifest')
    source_manifest=strict_json(sm);require(type(source_manifest.get('files')) is list and len(source_manifest['files'])==18,'18 original source rows')
    source={}
    for row in source_manifest['files']:
        require(set(row)=={'path','bytes','sha256','git_blob','git_mode'} and row['git_mode']=='100644','original source schema')
        rows([{k:row[k] for k in ('path','bytes','sha256')}]);data=read(path_within(source_root,row['path']),row['bytes']);authenticate(data,row)
        require(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob'],'original Git blob mismatch')
        public(row['path'],data,historical_zip=row['path']=='AUTHOR_CANDIDATE.zip');source[row['path']]=data
    require(len(source)==18 and sum(map(len,source.values()))==91564,'exact original packet count/size')
    paper={}
    for n,row in paper_rows.items():data=read(path_within(preprint,n),row['bytes']);authenticate(data,row);public(n,data,pdf=n=='post-lie-note.pdf');paper[n]=data
    fixed_metadata(paper)
    receipts={}
    for n,row in receipt_rows.items():data=read(path_within(root(BASE),row['source']),row['bytes']);authenticate(data,row);public(n,data);receipts[n]=data
    require(receipts['SOURCE_MANIFEST.json']==sm,'root receipt source manifest differs')
    tools=safe_envelopes['publication_tools_01'];tool=tools['portable.py'];require(len(tool)==49920 and sha(tool)==TOOL_SHA and tools['verification/portable.py']==tool,'authenticated tool copy equality')
    readme=read(HERE/'CANDIDATE_README_TEMPLATE.md');history=read(HERE/'EDITION_HISTORY_TEMPLATE.md')
    public('README.md',readme);public('EDITION_HISTORY.md',history)
    portable={'portable.py':tool,'dependencies.json':tools['verification/dependencies.json'],'README.md':readme,'EDITION_HISTORY.md':history}
    for n in ('note.tex','metadata.json','zenodo-deposit.json'):portable[n]=paper[n]
    for n,data in source.items():add(portable,'source/'+n,data)
    for n,data in receipts.items():add(portable,'root_evidence/'+n,data)
    for folder,blobs in safe_envelopes.items():
        for n,data in blobs.items():add(portable,'audits/'+folder+'/'+n,data)
    if noteauthor:
        for n,data in noteauthor.items():add(portable,'history/note_author_01/'+n,data)
    provenance={'schema':'pr894-assembly-provenance-v1','input_plan':pin(plan),'tool_sha256':TOOL_SHA,'source_manifest_sha256':SOURCE_SHA,'safe_envelopes':{n:{'manifest_sha256':h,'rows':count} for n,(size,h,count) in ENVELOPES.items()},'noteauthor_manifest_sha256':args.noteauthor_manifest_sha256,'noteauthor_role':'dated draft snapshot; parent preprint files are authoritative','parent_receipts':{n:pin(raw) for n,raw in sorted(receipts.items())},'scope':'Assembly engineering only; no new mathematical, priority, PDF or publication acceptance.'}
    portable['ASSEMBLY_PROVENANCE.json']=encoded(provenance)
    portable['package_index.json']=index(portable,PACKAGE_SCHEMA)
    outer={n:paper[n] for n in PAPER_NAMES};outer.update({'portable.py':tool,'README.md':readme,'EDITION_HISTORY.md':history,'CURRENT_PUBLICATION.json':tools['CURRENT_LAYOUT_TEMPLATE.json']})
    outer.update({'verification/'+n:raw for n,raw in portable.items()})
    rows([dict(path=n,**pin(raw)) for n,raw in outer.items()])
    candidate=HERE/'candidate';state=HERE/'private_tmp'/'prepared-state.json'
    require(not candidate.exists() and not candidate.is_symlink() and not state.exists(),'prepare requires fresh candidate/state')
    (HERE/'private_tmp').mkdir(exist_ok=True);root(HERE/'private_tmp')
    materialize(candidate,outer)
    prepared={'schema':'pr894-assembly-prepared-v1','package_index_sha256':sha(portable['package_index.json']),'files':[dict(path=n,**pin(raw)) for n,raw in sorted(outer.items())],'input_plan':pin(plan),'noteauthor_manifest_sha256':args.noteauthor_manifest_sha256,'scope':'Prepared inputs only; no verification ZIP or current manifest exists yet.'}
    state_bytes=encoded(prepared);write_new(state,state_bytes)
    return {'status':'PREPARED_NOT_FINALIZED','candidate':'candidate','prepared_state':'private_tmp/prepared-state.json','prepared_state_pin':pin(state_bytes),'package_index_pin':pin(portable['package_index.json']),'portable_sha256':TOOL_SHA,'next':'Parent independently authenticates pins, captures mandatory portable.py build outside candidate, then invokes finalize.'}
def outside(path,candidate):
    parent=root(path.absolute().parent);protected=[candidate,BASE/'preprint',BASE/'source',BASE/'publication_tools_01/verification',*[BASE/n for n in ENVELOPES]]
    for name in ('noteauthor_01','note_author_01'):
        if (BASE/name).exists():protected.append(BASE/name)
    ids={(p.stat().st_dev,p.stat().st_ino) for p in protected if p.exists()}
    for p in (parent,*parent.parents):require((p.stat().st_dev,p.stat().st_ino) not in ids,'build/capture/replay input must be physically outside candidate and source input trees')
    return parent/path.name
def record(folder,stem):
    meta=strict_json(read(folder/(stem+'.json')));out=read(folder/(stem+'.stdout.bin'));err=read(folder/(stem+'.stderr.bin'))
    require(meta['stdout']==pin(out) and meta['stderr']==pin(err),'raw process stream pins differ')
    require(type(meta['pid']) is int and type(meta['returncode']) is int and meta['started_utc']<=meta['ended_utc'] and meta['timeout'] is False,'actual process metadata required')
    return meta,out,err
def replay_evidence(directory,replay,portable):
    require(replay.get('status')=='PASS' and replay.get('label')=='ORIGINAL_ROOT_AND_FINITE_DIAGNOSTICS_REPLAYED' and replay.get('archival_code_executed') is True,'mandatory full replay missing')
    for k,v in {'direct_root_wrapper_processes':1,'unchanged_original_root_executions':1,'original_requested_diagnostic_children':2,'extra_control_children':6,'positive_runs':2,'semantic_invalid_product_rejections':2,'explicit_require_false_rejections':2,'corrupt_preexecution_rejections':2}.items():require(type(replay.get(k)) is int and replay[k]==v,'full replay schedule missing')
    require(replay.get('originals_unchanged') is True and replay['receipt_directory']==str(directory),'actual private replay directory must match build output')
    meta,out,err=record(directory,'root-wrapper');require(meta==replay['wrapper_process'] and meta['returncode']==0 and err==b'','root wrapper receipt differs')
    launcher=strict_json(out);require(launcher==replay['launcher'] and launcher['root_sha256']==ROOT_SHA,'actual wrapper stdout differs')
    events=launcher['events'];require(type(events) is list and len(events)==8,'eight genuine child receipts required')
    kinds=['positive','positive','semantic_negative','require_false','corrupt','semantic_negative','require_false','corrupt'];modes=[0,1,0,0,0,1,1,1]
    for i,(kind,mode,e) in enumerate(zip(kinds,modes,events)):
        flags={'optimize':mode,'isolated':1,'no_site':1,'dont_write_bytecode':1,'ignore_environment':1,'safe_path':True}
        require(e['kind']==kind and e['measured_flags']==flags and e['raw_receipt_stem']=='child-%02d'%i,'real child schedule/flags differ')
        child,stdout,stderr=record(directory/'processes',e['raw_receipt_stem']);require(child==e['process'],'actual child metadata differs')
        measured=strict_json(read(directory/'processes'/(e['raw_receipt_stem']+'.flags.json')));require(measured==flags,'on-disk child flags differ')
        began=(directory/'processes'/(e['raw_receipt_stem']+'.began')).exists();require(began==(kind!='corrupt'),'original-execution marker differs')
        if kind=='positive':require(child['returncode']==0 and stderr==b'' and pin(stdout)=={'bytes':966,'sha256':RESULT_SHA},'positive output differs')
        else:require(child['returncode']!=0,'negative actual process did not reject')
    frozen=inventory(directory/'frozen');expected={n[7:]:raw for n,raw in portable.items() if n.startswith('source/')};require(frozen==expected,'private unchanged original packet differs')
def finalize(args):
    candidate=root(HERE/'candidate');state_raw=read(HERE/'private_tmp/prepared-state.json');digest(args.prepared_state_sha256);require(sha(state_raw)==args.prepared_state_sha256,'independent prepared-state pin required')
    state=strict_json(state_raw);require(state['schema']=='pr894-assembly-prepared-v1','prepared schema')
    prepared_rows=rows(state['files']);outer=inventory(candidate);require(set(outer)==set(prepared_rows),'candidate changed since prepare')
    for n,row in prepared_rows.items():authenticate(outer[n],row)
    portable={n[13:]:raw for n,raw in outer.items() if n.startswith('verification/')}
    require(sha(portable['package_index.json'])==state['package_index_sha256'],'prepared package index changed')
    require(outer['portable.py']==portable['portable.py'] and sha(outer['portable.py'])==TOOL_SHA,'startup copy differs')
    for n in ('note.tex','metadata.json','zenodo-deposit.json'):require(outer[n]==portable[n],'outer/inner authoritative copy differs')
    fixed_metadata(outer)
    archive=outside(args.zip,candidate);require(archive.name=='post-lie-verification.zip','exact ZIP name required');raw=read(archive)
    # Mandatory actual tool build is external. These are retained real capture
    # files supplied by the parent, never synthetic stdout or guessed approval.
    build_stdout=read(outside(args.build_stdout,candidate));build_stderr=read(outside(args.build_stderr,candidate));capture_raw=read(outside(args.build_process,candidate));capture=strict_json(capture_raw)
    require(capture['returncode']==0 and type(capture['pid']) is int and capture['started_utc']<=capture['ended_utc'] and capture['stdout']==pin(build_stdout) and capture['stderr']==pin(build_stderr) and not capture.get('timeout',False),'successful original parent process capture required')
    require(build_stderr==b'','build stderr must be empty');build=strict_json(build_stdout)
    require(build['status']=='PASS' and build['archive_name']==archive.name and {'bytes':build['bytes'],'sha256':build['sha256']}==pin(raw) and build['member_count']==len(portable) and build['same_runtime_exact_rebuild'] is True,'actual build stdout differs')
    verification=build['verification'];require(verification['status']=='PASS' and verification['index_sha256']==state['package_index_sha256'],'build verified another package')
    replay_dir=root(args.replay_receipts);outside(replay_dir/'sentinel',candidate);replay_evidence(replay_dir,verification['replay'],portable)
    require(raw==zip_bytes(portable),'independent same-runtime ZIP rebuild differs')
    binding={'schema':'pr894-assembly-build-binding-v1','archive':pin(raw),'package_index_sha256':state['package_index_sha256'],'prepared_state_sha256':args.prepared_state_sha256,'actual_parent_build_stdout':pin(build_stdout),'actual_parent_build_stderr':pin(build_stderr),'actual_parent_process_capture':pin(capture_raw),'genuine_replay_processes':9,'root_execution':'unchanged original root inside one measured wrapper process','diagnostic_children':2,'extra_negative_control_children':6,'scope':'Build provenance only; no theorem, novelty, PDF visual or publication approval.'}
    outer['post-lie-verification.zip']=raw;outer['ASSEMBLY_BUILD_BINDING.json']=encoded(binding)
    # The outer manifest is made only AFTER the actual successful ZIP build.
    manifest=index(outer,CURRENT_SCHEMA)
    for n in ('post-lie-verification.zip','ASSEMBLY_BUILD_BINDING.json','CURRENT_PUBLICATION_MANIFEST.json'):require(not (candidate/n).exists() and not (candidate/n).is_symlink(),'finalize never overwrites')
    write_new(candidate/'post-lie-verification.zip',raw);write_new(candidate/'ASSEMBLY_BUILD_BINDING.json',outer['ASSEMBLY_BUILD_BINDING.json']);write_new(candidate/'CURRENT_PUBLICATION_MANIFEST.json',manifest)
    final=inventory(candidate);require(final=={**outer,'CURRENT_PUBLICATION_MANIFEST.json':manifest},'final closed candidate mismatch')
    return {'status':'ASSEMBLED_REQUIRES_PARENT_CURRENT_AND_EDITORIAL_REVIEW','candidate':'candidate','files':len(final),'package_index_pin':pin(portable['package_index.json']),'current_manifest_pin':pin(manifest),'archive':pin(raw),'tool_sha256':TOOL_SHA,'scope':'Assembly engineering only; parent still runs authenticated current and integrated whole-publication acceptance.'}
def main():
    require(sys.version_info>=(3,11) and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and sys.flags.optimize in (0,1),'run Python >=3.11 with actual -I -S -B, normal or single -O')
    p=argparse.ArgumentParser(description=__doc__,allow_abbrev=False);sub=p.add_subparsers(dest='mode',required=True)
    q=sub.add_parser('prepare',allow_abbrev=False);q.add_argument('--preprint-dir',type=Path,required=True);q.add_argument('--inputs',type=Path,required=True);q.add_argument('--inputs-sha256',required=True);q.add_argument('--noteauthor-manifest-sha256');q.add_argument('--noteauthor-dir',type=Path,default=BASE/'note_author_01')
    q=sub.add_parser('finalize',allow_abbrev=False);q.add_argument('--prepared-state-sha256',required=True);q.add_argument('--zip',type=Path,required=True);q.add_argument('--build-stdout',type=Path,required=True);q.add_argument('--build-stderr',type=Path,required=True);q.add_argument('--build-process',type=Path,required=True);q.add_argument('--replay-receipts',type=Path,required=True)
    args=p.parse_args();print(json.dumps(prepare(args) if args.mode=='prepare' else finalize(args),indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,OverflowError,RecursionError,UnicodeError,zipfile.BadZipFile) as e:
        print(json.dumps({'status':'REJECTED','reason':str(e)},sort_keys=True));sys.exit(1)
