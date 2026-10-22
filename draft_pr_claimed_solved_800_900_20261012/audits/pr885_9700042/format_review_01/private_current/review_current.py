#!/usr/bin/env python3
"""Independent initial format review of the actual r1 publication candidate.

No default replay. Only authentication-only CLI calls and malformed clones run.
Every clone starts as explicit hardlinks; mutations unlink before replacement.
The candidate, the initial 13-file review snapshot and original sources stay read only.
"""
from pathlib import Path, PurePosixPath
import copy
import datetime
import hashlib
import io
import json
import math
import os
import re
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
import zipfile
import zlib

HERE=Path(__file__).resolve().parent.parent
AUDIT=HERE.parent
PRIVATE=HERE/'private_current'
CANDIDATE=AUDIT/'replay/revision_r1'
CURRENT_PIN='bd07582e02490a57d5edd3f4438659b57b0fef8b5397f5865e3fe53220b5ec2a'
INDEX_PIN='a45d6799b5770cd51cfb4e0bdbcd4461d981f13be733dfb1f57236ad838f51b9'
TOOL_PIN='8832a44a53f0df4867cb8196d725209dd7ac5944c82b4f296b7514155fe72e6c'
SOURCE_PIN='6b1d1281848190f616f6759f40454183c937b65e65219b893202254be6c3617d'
PDF_PIN='e8ef086a61d1425c0e4892279a42f64079be1216c7936fff81628471c1ed2fba'
ZIP_PIN='824b7f037be72f7c7337dba4ea00c6d72b11be5a8cf026e928e4e1b751753f3b'
OLD_REVIEW_PIN='5555859e806cc78e973c976b244b054b283579c674b4744f82d06db53f6b0fb9'
MANIFEST='CURRENT_PUBLICATION_MANIFEST.json'
INDEX='verification/package_index.json'
FIXED_DATE=(2026,10,16,0,0,0)
PROBE=r'''from pathlib import Path
import json,runpy,sys
tool=Path(sys.argv[1]);args=json.loads(sys.argv[2]);log=Path(sys.argv[3])
events={'subprocess_popen_events':0,'current_inputs_returned':0,'original_inputs_returned':0}
def audit(name,values):
    if name=='subprocess.Popen':events['subprocess_popen_events']+=1
def profile(frame,event,arg):
    if event=='return' and frame.f_code.co_filename==str(tool):
        if frame.f_code.co_name=='current_inputs' and isinstance(arg,tuple):events['current_inputs_returned']+=1
        if frame.f_code.co_name=='original_inputs' and isinstance(arg,dict):events['original_inputs_returned']+=1
sys.addaudithook(audit);sys.setprofile(profile)
sys.argv=[str(tool),*args]
try:
    runpy.run_path(str(tool),run_name='__main__')
finally:
    sys.setprofile(None);log.write_text(json.dumps(events,sort_keys=True))
'''


def check(ok,reason):
    if not ok:raise RuntimeError(reason)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def encode(value):return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()


def strict(raw):
    def pairs(items):
        result={}
        for key,value in items:
            check(key not in result,'duplicate JSON key')
            result[key]=value
        return result
    def constant(value):raise ValueError('nonfinite constant')
    def number(value):
        answer=float(value);check(math.isfinite(answer),'nonfinite numeric overflow');return answer
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant,parse_float=number)


def safe(name):
    check(type(name) is str and 0<len(name)<=512 and re.fullmatch(r'[A-Za-z0-9_./-]+',name),'safe ASCII path')
    check(not PurePosixPath(name).is_absolute() and all(p not in ('','.','..') for p in name.split('/')),'safe path components')


def index_rows(raw,schema):
    value=strict(raw)
    check(type(value) is dict and set(value)=={'schema','problem_id','files'} and value['schema']==schema and type(value['schema']) is str and value['problem_id']=='9700042' and type(value['problem_id']) is str,'typed index identity')
    rows=value['files'];check(type(rows) is list and 0<len(rows)<=10000,'row array')
    answer={};folded=set();directories={}
    for row in rows:
        check(type(row) is dict and set(row)=={'path','bytes','sha256'},'typed row keys')
        name=row['path'];safe(name)
        check(type(row['bytes']) is int and 0<=row['bytes']<=256*1024*1024,'typed bytes')
        check(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']),'digest syntax')
        check(name.casefold() not in folded,'case or duplicate row')
        folded.add(name.casefold());answer[name]=row
        for directory in PurePosixPath(name).parents:
            directory=str(directory)
            if directory!='.':
                key=directory.casefold()
                check(key not in directories or directories[key]==directory,'directory case alias')
                directories[key]=directory
    check(sum(r['bytes'] for r in rows)<=512*1024*1024,'inventory bound')
    check(not (set(directories)&folded),'file directory collision')
    return answer


def closed(root,names):
    expected=set(names);seen=set();wanted_dirs={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'}
    check(stat.S_ISDIR(root.lstat().st_mode),'ordinary root')
    for folder,dirs,files in os.walk(root,followlinks=False):
        relative=Path(folder).relative_to(root)
        for name in dirs:
            path=Path(folder)/name;label=str(relative/name)
            check(stat.S_ISDIR(path.lstat().st_mode) and label in wanted_dirs,'closed ordinary directory')
        for name in files:
            path=Path(folder)/name;label=str(relative/name)
            check(stat.S_ISREG(path.lstat().st_mode) and label in expected,'closed ordinary file')
            seen.add(label)
    check(seen==expected,'exact closed inventory')


def zip_build(payloads):
    target=io.BytesIO()
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name in sorted(payloads):
            entry=zipfile.ZipInfo(name,FIXED_DATE);entry.create_system=3
            entry.external_attr=(stat.S_IFREG|0o644)<<16;entry.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(entry,payloads[name],compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    return target.getvalue()


def independent_zip(raw,payloads):
    # Independent raw sequential scan, then standard-library CRC/member reads.
    check(len(raw)>=22,'ZIP terminal record')
    ending=struct.unpack_from('<4s4H2IH',raw,len(raw)-22)
    check(ending[:3]==(b'PK\x05\x06',0,0) and ending[3]==ending[4]==len(payloads) and ending[7]==0,'ZIP closed EOCD')
    central=ending[6];check(central+ending[5]==len(raw)-22,'ZIP central extent')
    cursor=0;records=[];names=sorted(payloads)
    date=((2026-1980)<<9)|(10<<5)|16
    for name in names:
        head=struct.unpack_from('<4s5H3I2H',raw,cursor)
        check(head[0]==b'PK\x03\x04' and head[1]==20 and head[2] in (0,0x800) and head[3]==8 and head[4]==0 and head[5]==date and head[10]==0,'ZIP fixed local metadata')
        encoded=name.encode('ascii');start=cursor+30+head[9]
        check(head[9]==len(encoded) and raw[cursor+30:start]==encoded,'ZIP exact local name')
        want=payloads[name];check(head[8]==len(want) and head[6]==zlib.crc32(want)&0xffffffff,'ZIP expected size and CRC')
        stop=start+head[7];check(stop<=central,'ZIP local payload extent')
        decoder=zlib.decompressobj(-15);output=decoder.decompress(raw[start:stop],len(want)+1)
        check(output==want and decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,'ZIP exact complete raw DEFLATE')
        records.append((cursor,name,head));cursor=stop
    check(cursor==central,'ZIP no local gaps')
    at=central
    for offset,name,head in records:
        c=struct.unpack_from('<4s6H3I5H2I',raw,at)
        expected=(b'PK\x01\x02',0x0314,20,head[2],8,0,date,head[6],head[7],head[8],len(name),0,0,0,0,(stat.S_IFREG|0o644)<<16,offset)
        check(c==expected and raw[at+46:at+46+len(name)]==name.encode('ascii'),'ZIP exact central metadata/name')
        at+=46+len(name)
    check(at==len(raw)-22,'ZIP no central gaps')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        check(archive.namelist()==names,'ZIP exact sorted member set')
        for name in names:check(archive.read(name)==payloads[name],'ZIP library exact member/CRC')
    rebuilt=zip_build(payloads);check(raw==rebuilt,'same-runtime independent ZIP rebuild')
    return {'members':len(names),'bytes':len(raw),'sha256':sha(raw),'raw_local_central_EOCD_closed':True,'raw_DEFLATE_exact_consumption_all_members':True,'all_metadata_fixed_epoch_mode_method':True,'library_CRC_and_member_bytes':True,'same_runtime_exact_rebuild':True,'python':sys.version.split()[0],'zlib_runtime':zlib.ZLIB_RUNTIME_VERSION,'cross_runtime_byte_promise':False}


def old_snapshot():
    raw=(HERE/'V4_PUBLIC_MANIFEST.json').read_bytes();check(sha(raw)==OLD_REVIEW_PIN,'frozen old manifest')
    manifest=strict(raw)
    for row in manifest['files']:
        value=(HERE/row['path']).read_bytes();check(len(value)==row['bytes'] and sha(value)==row['sha256'],'frozen 13-file snapshot')


def authenticate_candidate():
    raw=(CANDIDATE/MANIFEST).read_bytes();check(sha(raw)==CURRENT_PIN,'external actual current pin')
    rows=index_rows(raw,'oriented-flow-9700042-current-publication-v1')
    check(len(rows)==196 and MANIFEST not in rows,'197 exact files including manifest')
    closed(CANDIDATE,set(rows)|{MANIFEST})
    blobs={MANIFEST:raw}
    for name,row in rows.items():
        value=(CANDIDATE/name).read_bytes();check(len(value)==row['bytes'] and sha(value)==row['sha256'],'outer pin '+name)
        if name.endswith('.json'):strict(value)
        blobs[name]=value
    check(sha(blobs[INDEX])==INDEX_PIN,'external portable index pin')
    inner=index_rows(blobs[INDEX],'oriented-flow-9700042-verification-v1')
    portable={name[13:]:value for name,value in blobs.items() if name.startswith('verification/')}
    check(len(portable)==159 and set(portable)==set(inner)|{'package_index.json'},'159 exact portable members')
    for name,row in inner.items():check(len(portable[name])==row['bytes'] and sha(portable[name])==row['sha256'],'portable pin '+name)
    for name in ('portable.py','note.tex','metadata.json','zenodo-deposit.json'):
        check(blobs[name]==portable[name],'outer portable copy '+name)
    check(len(blobs['portable.py'])==41629 and sha(blobs['portable.py'])==TOOL_PIN and blobs['portable.py']==(AUDIT/'publication_tools_03/portable.py').read_bytes(),'three tool copies and written V4')
    for name in ('note.tex','metadata.json','zenodo-deposit.json'):
        check(blobs[name]==(AUDIT/'preprint'/name).read_bytes(),'authored preprint copy '+name)
    source_raw=portable['root_evidence/SOURCE_MANIFEST.json']
    check(sha(source_raw)==SOURCE_PIN and source_raw==(AUDIT/'SOURCE_MANIFEST.json').read_bytes() and portable['SOURCE_MANIFEST.json']==source_raw,'source manifest copy group')
    source_manifest=strict(source_raw);check(source_manifest['head']=='4b1ef9bbeb723a4171949a6c3934db98962ac615' and source_manifest['original_effort']=='5/5' and len(source_manifest['files'])==30,'source assigned identity')
    source_rows=[];originals={};outer_replacements=[]
    for row in source_manifest['files']:
        name=row['path'];value=portable['source/'+name]
        check(value==(AUDIT/'source'/name).read_bytes(),'all30 portable and authoritative source copy group '+name)
        if blobs[name]!=value:
            check(name in ('README.md','RESEARCH_LOG.md'),'unexpected changed historical outer file '+name)
            outer_replacements.append({'path':name,'bytes':len(blobs[name]),'sha256':sha(blobs[name]),'role':'Current authored outer document; original remains unchanged under verification/source.'})
        blob=hashlib.sha1(b'blob '+str(len(value)).encode()+b'\0'+value).hexdigest()
        check(len(value)==row['bytes'] and sha(value)==row['sha256'] and blob==row['git_blob'],'all30 original pins '+name)
        originals[name]=value;source_rows.append(row)
    check(sum(len(v) for v in originals.values())==214980 and {r['path'] for r in outer_replacements}=={'README.md','RESEARCH_LOG.md'},'original total and declared outer document replacements')
    check(len(blobs['oriented-flow-note.pdf'])==82047 and blobs['oriented-flow-note.pdf'].startswith(b'%PDF-') and sha(blobs['oriented-flow-note.pdf'])==PDF_PIN,'actual PDF bytes and magic')
    layout=strict(blobs['CURRENT_PUBLICATION.json'])
    check(layout=={'pdf_path':'oriented-flow-note.pdf','portable_prefix':'verification','problem_id':'9700042','schema':'oriented-flow-9700042-current-layout-v1','tex_path':'note.tex','zip_path':'oriented-flow-verification.zip'},'actual layout')
    metadata=strict(blobs['metadata.json']);deposit=strict(blobs['zenodo-deposit.json'])
    check(set(metadata)=={'title','upload_type','publication_type','publication_date','version','description','creators','access_right','license','keywords','references','related_identifiers'},'metadata exact12 keys')
    check(set(deposit)=={'metadata','files'} and type(deposit['metadata']) is dict and deposit['metadata']==metadata,'typed nested deposit metadata')
    check(deposit['files']==[{'name':'oriented-flow-note.pdf','path':'oriented-flow-note.pdf'},{'name':'oriented-flow-verification.zip','path':'oriented-flow-verification.zip'}],'exact two-asset kit')
    check(metadata['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'creator identity')
    check(len(blobs['oriented-flow-verification.zip'])==388193 and sha(blobs['oriented-flow-verification.zip'])==ZIP_PIN,'actual ZIP external pin')
    zip_receipt=independent_zip(blobs['oriented-flow-verification.zip'],portable)
    path_scan=[{'path':name,'literal_private_path_patterns_found':sum(value.count(pattern) for pattern in (b'/Users/',b'/private/var/folders/',b'/var/folders/'))} for name,value in blobs.items() if name.endswith(('.py','.json','.md','.tex'))]
    return blobs,portable,originals,{'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_estimate_percent':80,'current_manifest_sha256':CURRENT_PIN,'outer_file_count':len(blobs),'portable_index_sha256':INDEX_PIN,'portable_member_count':len(portable),'outer_rows':[{'path':n,'bytes':len(v),'sha256':sha(v)} for n,v in sorted(blobs.items())],'portable_rows':[{'path':n,'bytes':len(v),'sha256':sha(v)} for n,v in sorted(portable.items())],'all30_original_rows':source_rows,'all30_portable_authoritative_equal':True,'unchanged_historical_outer_files':28,'declared_current_outer_document_replacements':outer_replacements,'tool_TeX_metadata_deposit_copy_groups_equal':True,'PDF':{'bytes':82047,'sha256':PDF_PIN,'PDF_magic':True,'visual_render_or_page_count':'NOT_RUN'},'ZIP':zip_receipt,'metadata_exact_two_asset_kit':True,'bounded_literal_path_scan_hits':[r for r in path_scan if r['literal_private_path_patterns_found']],'fresh_assigned_head_Git_tree_comparison':'NOT_RUN: Git forbidden','scope':'Independent byte/format authentication and same-runtime ZIP rebuild only; no archival execution or mathematical/priority approval.'}


def replace(root,name,value):
    path=root/name
    if path.exists() or path.is_symlink():path.unlink()
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream:stream.write(value)


def rows_for(root,names):
    return [{'path':n,'bytes':(root/n).stat().st_size,'sha256':sha((root/n).read_bytes())} for n in sorted(names)]


def refresh_inner(root,portable_names):
    rows=rows_for(root,['verification/'+n for n in portable_names if n!='package_index.json'])
    for row in rows:row['path']=row['path'][13:]
    replace(root,INDEX,encode({'schema':'oriented-flow-9700042-verification-v1','problem_id':'9700042','files':rows}))
    current={n:(root/'verification'/n).read_bytes() for n in portable_names}
    replace(root,'oriented-flow-verification.zip',zip_build(current))


def refresh_outer(root,names):
    raw=encode({'schema':'oriented-flow-9700042-current-publication-v1','problem_id':'9700042','files':rows_for(root,[n for n in names if n!=MANIFEST])})
    replace(root,MANIFEST,raw);return sha(raw)


def zip_variant(raw,kind):
    if kind=='suffix':return raw+b'X'
    data=bytearray(raw);end=len(data)-22;central=struct.unpack_from('<I',data,end+16)[0]
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:infos=archive.infolist()
    last=infos[-1];c_last=central+sum(46+len(i.filename.encode('ascii')) for i in infos[:-1])
    if kind in ('deflate_trailing','deflate_second_stream'):
        extra=b'JUNK' if kind=='deflate_trailing' else b'\x03\x00'
        data[central:central]=extra;delta=len(extra)
        struct.pack_into('<I',data,last.header_offset+18,last.compress_size+delta)
        struct.pack_into('<I',data,c_last+delta+20,last.compress_size+delta)
        struct.pack_into('<I',data,end+delta+16,central+delta)
    elif kind=='epoch':
        wrong=((2026-1980)<<9)|(10<<5)|15
        struct.pack_into('<H',data,last.header_offset+12,wrong);struct.pack_into('<H',data,c_last+14,wrong)
    elif kind=='symlink':struct.pack_into('<I',data,c_last+38,(stat.S_IFLNK|0o777)<<16)
    elif kind=='stored':
        struct.pack_into('<H',data,last.header_offset+8,0);struct.pack_into('<H',data,c_last+10,0)
    elif kind=='CRC':
        wrong=last.CRC^1
        struct.pack_into('<I',data,last.header_offset+14,wrong);struct.pack_into('<I',data,c_last+16,wrong)
    else:raise RuntimeError('unknown ZIP mutation')
    return bytes(data)


def main():
    old_snapshot()
    run=PRIVATE/'run_02';run.mkdir()
    blobs,portable,originals,auth=authenticate_candidate()
    (HERE/'current_AUTHENTICATION.json').write_bytes(encode(auth))
    observations=[];journal=(run/'observations.jsonl').open('x')
    def execute(label,root,pin,extras=None,flags=None,expected=None,positive=False):
        tool=root/'portable.py';events=run/(label+'.events.json')
        argv=['current',pin,'--root',str(root),'--verify-only',*(extras or [])]
        actual_flags=flags if flags is not None else ['-I','-S','-B']
        process=subprocess.run([sys.executable,*actual_flags,'-c',PROBE,str(tool),json.dumps(argv),str(events)],cwd=run,capture_output=True,timeout=60)
        (run/(label+'.stdout')).write_bytes(process.stdout);(run/(label+'.stderr')).write_bytes(process.stderr)
        measurement=strict(events.read_bytes())
        check(measurement['subprocess_popen_events']==0,label+' reached archival subprocess')
        result=strict(process.stdout) if process.stdout.strip().startswith(b'{') else None
        if positive:
            check(process.returncode==0 and not process.stderr and result['status']=='PASS' and result['portable']['replay']=='NOT_RUN' and measurement['current_inputs_returned']==1,label+' positive authentication')
        else:
            check(process.returncode!=0,label+' malformed input accepted')
            if expected is not None:check(result is not None and result['status']=='REJECTED' and expected in result['reason'],label+' did not reach intended format guard')
        normalized=json.loads(json.dumps(result).replace(str(root),'<control-root>').replace(str(CANDIDATE),'<actual-candidate>')) if result is not None else None
        receipt={'case':label,'returncode':process.returncode,'interpreter_flags':actual_flags,'stdout_bytes':len(process.stdout),'stdout_sha256':sha(process.stdout),'stderr_bytes':len(process.stderr),'stderr_sha256':sha(process.stderr),**measurement,'result_normalized':normalized,'expected_guard_substring':expected,'archival_execution':False}
        observations.append(receipt);journal.write(json.dumps(receipt,sort_keys=True)+'\n');journal.flush()
        return receipt
    for optimized in (False,True):
        execute('actual_current_authentication_'+('optimized' if optimized else 'normal'),CANDIDATE,CURRENT_PIN,flags=['-I','-S','-B']+(['-O'] if optimized else []),positive=True)
    for label,extras,flags,expected,pin in [
        ('unknown_option',['--unknown'],None,None,CURRENT_PIN),('abbreviated_option',['--verify-o'],None,None,CURRENT_PIN),
        ('missing_I',[],['-S','-B'],'run with -I -S -B',CURRENT_PIN),('missing_S',[],['-I','-B'],'run with -I -S -B',CURRENT_PIN),('missing_B',[],['-I','-S'],'run with -I -S -B',CURRENT_PIN),
        ('partial_sources',['--catalog','unavailable'],None,'all three corpus paths together',CURRENT_PIN),('bad_external_pin',[],None,'external current manifest pin mismatch','0'*64)]:
        execute(label,CANDIDATE,pin,extras,flags,expected)
    mutations=[
        ('outer_unknown_key','typed index identity/schema'),('outer_bool_bytes','typed byte count'),('outer_duplicate_path','duplicate/aliased inventory path'),('outer_directory_case_alias','directory name alias'),
        ('extra_empty_directory','unlisted directory'),('extra_fifo','nonregular tree entry'),('listed_symlink','nonregular tree entry'),('missing_file','missing inventory file'),
        ('tex_copy_mismatch','outer/portable actual TeX equality'),('metadata_copy_mismatch','outer/portable metadata copies differ'),('tool_copy_mismatch','outer/portable tool copies differ'),
        ('changed_original_reindexed','pin mismatch: source/verify_resume_turn1.py'),('changed_source_manifest_reindexed','immutable source manifest pin'),
        ('metadata_unknown_key','publication metadata exact keys'),('metadata_description_type','publication metadata string: description'),('metadata_date','publication metadata identity'),('metadata_creator','exact publication creator/affiliation/ORCID'),('metadata_references_type','publication metadata string list: references'),
        ('deposit_metadata_string','typed deposit metadata contract'),('deposit_extra_asset','exact two deposit asset names/paths'),('deposit_metadata_mismatch','typed deposit metadata contract'),
        ('layout_asset_name','exact two publication asset names and TeX'),('layout_prefix_type','relative path alphabet/length'),('inner_bool_bytes','typed byte count'),
        ('zip_suffix','ZIP end metadata/extent'),('zip_deflate_trailing','ZIP raw DEFLATE exact-consumption mismatch'),('zip_deflate_second_stream','ZIP raw DEFLATE exact-consumption mismatch'),('zip_epoch','ZIP unsafe central metadata'),('zip_symlink','ZIP unsafe central metadata'),('zip_stored','ZIP unsafe central metadata'),('zip_CRC','Bad CRC-32')]
    deleted=0
    for ordinal,(label,expected) in enumerate(mutations):
        with tempfile.TemporaryDirectory(prefix='clone-%02d-'%ordinal,dir=run) as td:
            root=Path(td)/'packet';root.mkdir()
            for name in sorted(blobs):
                target=root/name;target.parent.mkdir(parents=True,exist_ok=True);os.link(CANDIDATE/name,target)
            pin=CURRENT_PIN;inner_changed=False;outer_changed=False
            if label.startswith('outer_'):
                value=strict(blobs[MANIFEST])
                if label=='outer_unknown_key':value['unexpected']=True
                elif label=='outer_bool_bytes':value['files'][0]['bytes']=True
                elif label=='outer_duplicate_path':value['files'].append(copy.deepcopy(value['files'][0]))
                elif label=='outer_directory_case_alias':value['files'].append({'path':'Verification/unlisted.txt','bytes':0,'sha256':sha(b'')})
                raw=encode(value);replace(root,MANIFEST,raw);pin=sha(raw)
            elif label=='extra_empty_directory':(root/'unlisted_empty').mkdir()
            elif label=='extra_fifo':os.mkfifo(root/'unlisted_fifo')
            elif label=='listed_symlink':
                (root/'note.tex').unlink();(root/'note.tex').symlink_to(CANDIDATE/'note.tex')
            elif label=='missing_file':(root/'note.tex').unlink()
            elif label in ('tex_copy_mismatch','tool_copy_mismatch','changed_original_reindexed','changed_source_manifest_reindexed'):
                name={'tex_copy_mismatch':'note.tex','tool_copy_mismatch':'portable.py','changed_original_reindexed':'source/verify_resume_turn1.py','changed_source_manifest_reindexed':'root_evidence/SOURCE_MANIFEST.json'}[label]
                replace(root,'verification/'+name,portable[name]+b'\n');inner_changed=True
            elif label=='metadata_copy_mismatch':
                value=strict(portable['metadata.json']);value['description']+=' '
                replace(root,'verification/metadata.json',encode(value));inner_changed=True
            elif label.startswith('metadata_'):
                value=strict(blobs['metadata.json'])
                if label=='metadata_unknown_key':value['unexpected']=True
                elif label=='metadata_description_type':value['description']=5
                elif label=='metadata_date':value['publication_date']='2026-10-15'
                elif label=='metadata_creator':value['creators'][0]['orcid']='0000-0000-0000-0000'
                elif label=='metadata_references_type':value['references']={}
                for name in ('metadata.json','verification/metadata.json'):replace(root,name,encode(value))
                deposit=strict(blobs['zenodo-deposit.json']);deposit['metadata']=value
                for name in ('zenodo-deposit.json','verification/zenodo-deposit.json'):replace(root,name,encode(deposit))
                inner_changed=True
            elif label.startswith('deposit_'):
                value=strict(blobs['zenodo-deposit.json'])
                if label=='deposit_metadata_string':value['metadata']='not an object'
                elif label=='deposit_extra_asset':value['files'].append({'name':'extra','path':'extra'})
                elif label=='deposit_metadata_mismatch':value['metadata']['description']+=' '
                for name in ('zenodo-deposit.json','verification/zenodo-deposit.json'):replace(root,name,encode(value))
                inner_changed=True
            elif label.startswith('layout_'):
                value=strict(blobs['CURRENT_PUBLICATION.json'])
                value['pdf_path' if label=='layout_asset_name' else 'portable_prefix']='other.pdf' if label=='layout_asset_name' else False
                replace(root,'CURRENT_PUBLICATION.json',encode(value));outer_changed=True
            elif label=='inner_bool_bytes':
                value=strict(blobs[INDEX]);value['files'][0]['bytes']=True
                replace(root,INDEX,encode(value));outer_changed=True
            elif label.startswith('zip_'):
                replace(root,'oriented-flow-verification.zip',zip_variant(blobs['oriented-flow-verification.zip'],label[4:]));outer_changed=True
            else:raise RuntimeError('unimplemented mutation')
            if inner_changed:refresh_inner(root,portable);outer_changed=True
            if outer_changed:pin=refresh_outer(root,blobs)
            # For coherent semantic mutations all altered file hashes, inner
            # index bytes, ZIP bytes and outer manifest pins were recomputed.
            receipt=execute(label,root,pin,expected=expected)
            receipt['outer_pin_recomputed']=pin!=CURRENT_PIN
            receipt['inner_index_and_ZIP_rebuilt']=inner_changed
            receipt['own_clone_removed_after_receipt']=True
        deleted+=1
    journal.close()
    # Final reauthentication of all 197 actual files and authoritative originals.
    closed(CANDIDATE,blobs)
    for name,value in blobs.items():check((CANDIDATE/name).read_bytes()==value,'candidate changed after tests '+name)
    for name,value in originals.items():check((AUDIT/'source'/name).read_bytes()==value,'authoritative original changed after tests '+name)
    old_snapshot()
    final={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_estimate_percent':90,'current_manifest_sha256':CURRENT_PIN,'portable_index_sha256':INDEX_PIN,'tool_sha256':TOOL_PIN,'scope':'Actual current candidate independent format authentication, authentication-only CLI and coherent negative clones; no default archival replay, mathematical or priority acceptance.','cases':observations,'actual_current_files_unchanged_before_after':197,'authoritative_originals_unchanged':30,'old_13_file_review_snapshot_unchanged':True,'own_derived_clones_removed':deleted,'default_archival_replay':'NOT_RUN by this reviewer','outside_default_build':'NOT_RUN by this reviewer','earlier_parent_optimized_build_failure_cause':'UNESTABLISHED; independent ENOSPC observation does not prove child failure cause','final_whole_package_clear':False}
    (HERE/'current_CLI_RECEIPTS.json').write_bytes(encode(final))
    print(json.dumps({'status':'PASS','cases':len(observations),'own_clones_removed':deleted,'candidate_files_unchanged':197,'zero_subprocesses_all_cases':True,'archival_execution':False},sort_keys=True))


if __name__=='__main__':main()
