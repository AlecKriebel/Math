#!/usr/bin/env python3
"""Inert source-free guard/semantic controls; all fixtures in an owned tempdir.

Run with -I -S -B; externally authenticate this test and verifier first.
Output is engineering evidence, not independent review credit.
"""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('use -I -S -B')
import argparse,copy,datetime,hashlib,io,json,os,shutil,stat,struct,subprocess,tempfile,types,warnings,zipfile
from pathlib import Path
HERE=Path(__file__).absolute().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--originals',required=True,type=Path);p.add_argument('--verifier-sha256',required=True);p.add_argument('--work-dir',required=True,type=Path)
a=p.parse_args()
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
source=(HERE/'verify_package.py').read_bytes();need(sha(source)==a.verifier_sha256,'external verifier seal')
v=types.ModuleType('verified_profile');v.__file__=str(HERE/'verify_package.py');exec(compile(source,v.__file__,'exec',optimize=sys.flags.optimize),v.__dict__)
work=v.root_without_links(str(a.work_dir));originals=v.root_without_links(str(a.originals))
EVENTS=[]
original_excepthook=sys.excepthook
def preserve_failure(kind,error,tb):
    sys.stderr.write(json.dumps({'schema':'pr952-engineering-failed-run-v1','status':'FAILED_OR_INCOMPLETE_NO_CLEAN_CREDIT','events_before_failure':EVENTS,'failure_type':kind.__name__,'failure':str(error)},sort_keys=True)+'\n')
    original_excepthook(kind,error,tb)
sys.excepthook=preserve_failure
def event(name,status,**kw):EVENTS.append({'test':name,'outcome':status,**kw})
def reject(name,call,substring=None):
    try:call()
    except (v.Reject,OSError,zipfile.BadZipFile) as e:
        need(substring is None or substring in str(e),name+': unexpected rejection '+str(e));event(name,'REJECTED',reason=str(e))
    else:raise RuntimeError(name+' ACCEPTED')
def package_manifest(root):
    files={q.relative_to(root).as_posix():{'bytes':q.stat().st_size,'sha256':sha(q.read_bytes()),'mode':'100644'} for q in sorted(root.rglob('*')) if q.is_file() and q.name!=v.MANIFEST}
    return {'schema':v.SCHEMA,'version':1,'problem_id':10400145,'original_head':v.HEAD,'files':files,'archives':{}}
def write_manifest(root,doc=None,raw=None):
    b=raw if raw is not None else (json.dumps(doc or package_manifest(root),sort_keys=True,indent=2)+'\n').encode()
    (root/v.MANIFEST).write_bytes(b);(root/v.MANIFEST).chmod(0o644);return sha(b)
def zip_fixture(items,compression=zipfile.ZIP_STORED):
    b=io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',UserWarning)
        with zipfile.ZipFile(b,'w') as z:
            for name,body,mode in items:
                i=zipfile.ZipInfo(name);i.create_system=3;i.external_attr=(mode<<16)|(0x10 if name.endswith('/') else 0);i.compress_type=compression;z.writestr(i,body)
    return b.getvalue()
def zip_root(root):return zip_fixture([(q.relative_to(root).as_posix(),q.read_bytes(),0o100644) for q in sorted(root.rglob('*')) if q.is_file()])
def expected(items):return {n:{'bytes':len(b),'sha256':sha(b),'mode':'100644'} for n,b,_ in items if not n.endswith('/')}
def central_patch(raw,offset,value,fmt='<I'):
    b=bytearray(raw);at=0
    while True:
        at=b.find(b'PK\x01\x02',at)
        if at<0:break
        struct.pack_into(fmt,b,at+offset,value);at+=4
    return bytes(b)
with tempfile.TemporaryDirectory(prefix='pr952-profile-tests-',dir=work) as td:
    t=Path(td);base=t/'package';base.mkdir()
    for n,pin in v.ORIGINAL_PINS.items():
        src=originals/n;raw=v.regular_path(str(src),v.MAX_FILE_BYTES)
        need(len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],'original input pin '+n)
        dest=base/v.PREFIX/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw);dest.chmod(0o644)
    math=(HERE/'independent_math.py').read_bytes();need(sha(math)==v.MATH_SHA,'math input pin')
    (base/'checks').mkdir();(base/v.MATH).write_bytes(math);(base/v.MATH).chmod(0o644)
    (base/'verify_package.py').write_bytes(source);(base/'verify_package.py').chmod(0o644)
    anchor=write_manifest(base);doc=json.loads((base/v.MANIFEST).read_bytes())
    result,payload,manifest_raw=v.verify(str(base),anchor);need(result['original_files']==33,'original33 positive')
    event('closed_original33_positive','PASS',files=result['files'])
    archive=zip_root(base);r,zpayload,zraw=v.verify_zip(archive,anchor);need(zpayload==payload and zraw==manifest_raw,'ZIP mirrors tree')
    event('cold_ZIP_complete_positive','PASS',members=len(zpayload)+1)
    archive_path=t/'package.zip';archive_path.write_bytes(archive);archive_path.chmod(0o644)
    hostile=t/'hostile';hostile.mkdir();marker=t/'IMPORT_POISON_EXECUTED'
    for name in ('json.py','sitecustomize.py','usercustomize.py'):
        (hostile/name).write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\nraise RuntimeError("POISON")\n')
    env2=dict(os.environ,PYTHONPATH=str(hostile),PYTHONUSERBASE=str(hostile),PYTHONOPTIMIZE='2',TMPDIR=str(t))
    control=subprocess.run([sys.executable,'-B','-c','import json'],cwd=hostile,env=env2,capture_output=True,timeout=10)
    need(control.returncode!=0 and marker.exists(),'poison positive');marker.unlink();event('ambient_poison_positive','PASS')
    baseline_receipts=[]
    for label,flags,env in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('env2',[],env2)]:
        run=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(HERE/'verify_package.py'),'--archive',str(archive_path),'--archive-sha256',sha(archive),'--manifest-sha256',anchor,'--run-checkers','--work-dir',str(t)],cwd=hostile,env=env,capture_output=True,timeout=120)
        need(run.returncode==0 and not run.stderr,'cold '+label+': '+run.stderr.decode(errors='replace'))
        row=json.loads(run.stdout);need(len(row['replays'])==12 and row['outer_runtime']['optimize']==({'O':1,'OO':2}.get(label,0)),'actual cold flags/stages')
        need(row['scope']['linux_legacy_full_bwrap_EROFS']=='NOT_RUN' and not row['scope']['full_paper_acceptance'],'honest scope')
        need(not marker.exists(),'poison executed')
        baseline_receipts.append({'mode':label,'returncode':run.returncode,'receipt':row,'stdout_sha256':sha(run.stdout)})
        event('cold_'+label,'PASS',stages=12,outer_optimization=row['outer_runtime']['optimize'])
    def mutation(name,edit,rebind=False,substring=None):
        root=t/'mutation';shutil.copytree(base,root)
        try:
            edit(root);pin=write_manifest(root) if rebind else anchor
            reject(name,lambda:v.verify(str(root),pin),substring)
        finally:shutil.rmtree(root)
    mutation('extra_regular',lambda r:(r/'extra').write_bytes(b'x'),substring='closed file')
    mutation('extra_empty_directory',lambda r:(r/'empty').mkdir(),substring='closed directory')
    mutation('missing_file',lambda r:(r/v.MATH).unlink(),substring='closed file')
    mutation('file_symlink',lambda r:(r/'link').symlink_to(r/v.MATH),substring='nonregular')
    mutation('directory_symlink',lambda r:(r/'linkdir').symlink_to(r/'checks',target_is_directory=True),substring='nonregular')
    mutation('FIFO_before_read',lambda r:os.mkfifo(r/'fifo'),substring='nonregular')
    mutation('hard_link',lambda r:os.link(r/v.MATH,r/'hard'),substring='hard-linked')
    mutation('executable_mode',lambda r:(r/v.MATH).chmod(0o755),substring='disk mode')
    mutation('changed_original_rebound',lambda r:(r/v.PREFIX/'README.md').write_bytes(b'changed\n'),True,'immutable original')
    mutation('changed_independent_math_rebound',lambda r:(r/v.MATH).write_bytes(math+b'\n'),True,'math fixed pin')
    def sparse(root,name,size):
        with (root/name).open('wb') as f:f.truncate(size)
    mutation('file_size_cap',lambda r:sparse(r,'oversize',v.MAX_FILE_BYTES+1),substring='per-file size cap')
    mutation('manifest_size_cap',lambda r:sparse(r,v.MANIFEST,v.MAX_MANIFEST_BYTES+1),substring='identity/size cap')
    mutation('total_size_cap',lambda r:[sparse(r,'total'+str(i),v.MAX_FILE_BYTES) for i in range(5)],substring='total size cap')
    mutation('file_count_cap',lambda r:[(r/('count'+str(i))).write_bytes(b'') for i in range(v.MAX_FILES)],substring='file count cap')
    mutation('directory_count_cap',lambda r:[(r/('directory'+str(i))).mkdir() for i in range(v.MAX_DIRS+1)],substring='directory count cap')
    mutation('changed_manifest_stale_external',lambda r:(r/v.MANIFEST).write_bytes((r/v.MANIFEST).read_bytes()+b'\n'),substring='anchor mismatch')
    def schema_case(name,edit):
        root=t/'schema';shutil.copytree(base,root)
        try:
            d=copy.deepcopy(doc);edit(d);pin=write_manifest(root,d);reject(name,lambda:v.verify(str(root),pin))
        finally:shutil.rmtree(root)
    for key,val in [('version',True),('version',1.0),('problem_id',10400145.0),('original_head','0'*40),('extra',0)]:
        schema_case('schema_'+key+'_'+repr(val),lambda d,k=key,val=val:d.update({k:val}))
    first=next(iter(doc['files']))
    for key,val in [('bytes',True),('bytes',1.0),('sha256','A'*64),('mode','120777')]:schema_case('entry_'+key+'_'+repr(val),lambda d,k=key,val=val:d['files'][first].update({k:val}))
    for bad in ['../a','/a','a//b','a/./b','a\\b','.','NUL.txt','a.','a/../b']:
        schema_case('unsafe_'+repr(bad),lambda d,bad=bad:d['files'].update({bad:d['files'].pop(first)}))
    for name,raw in [('duplicate_key',b'{"schema":1,"schema":2}'),('nonfinite',b'{"x":NaN}'),('malformed',b'{')]:
        reject(name,lambda raw=raw:v.manifest(raw,sha(raw)))
    for name,fs,ds in [('file_ancestor',['A','A/b'],[]),('directory_alias',['A/x','a/y'],[]),('file_directory_alias',['A','a/y'],['a'])]:reject(name,lambda fs=fs,ds=ds:v.namespace(fs,ds))
    v.namespace(['A/x','A/y'],['A']);event('shared_ancestor_positive','PASS')
    link=t/'alias';link.symlink_to(base,target_is_directory=True)
    reject('root_symlink',lambda:v.verify(str(link),anchor),'root/ancestor')
    reject('ancestor_symlink',lambda:v.verify(str(link/'checks'),anchor),'root/ancestor')
    reject('root_parent_traversal',lambda:v.verify(str(base/'..'/'package'),anchor),'root canonical')
    # Metadata failures must reject before ANY member decompression.
    good_items=[('a.txt',b'hello',0o100644)];good=zip_fixture(good_items);good_expected=expected(good_items)
    need(v.inspect_archive(good,good_expected)['a.txt']==b'hello','ZIP generic positive');event('ZIP_generic_positive','PASS')
    dir_items=[('A/',b'',0o40755),('A/one',b'x',0o100644),('A/two',b'y',0o100644)]
    v.inspect_archive(zip_fixture(dir_items),expected(dir_items));event('ZIP_explicit_shared_directory_positive','PASS')
    bad_archives=[
      ('symlink',[('a',b'target',0o120777)]),('bad_mode',[('a',b'x',0o100600)]),('traversal',[('../escape',b'x',0o100644)]),('absolute',[('/a',b'x',0o100644)]),('duplicate',[('a',b'x',0o100644),('a',b'y',0o100644)]),('file_ancestor',[('A',b'x',0o100644),('A/b',b'y',0o100644)]),('directory_case_alias',[('A/x',b'x',0o100644),('a/y',b'y',0o100644)]),('file_directory_case_alias',[('A',b'x',0o100644),('a/y',b'y',0o100644)]),('empty_directory',[('empty/',b'',0o40755),('a.txt',b'hello',0o100644)])]
    bad=[('ZIP_'+n,zip_fixture(items)) for n,items in bad_archives]
    bad += [('ZIP_ratio',zip_fixture([('a',b'x'*65536,0o100644)],zipfile.ZIP_DEFLATED)),('ZIP_size',central_patch(good,24,v.MAX_FILE_BYTES+1)),('ZIP_encrypted',central_patch(good,8,1,'<H')),('ZIP_compression',central_patch(good,10,99,'<H')),('ZIP_NUL',good.replace(b'a.txt',b'a\x00txt'))]
    many=zip_fixture([(str(i),b'x',0o100644) for i in range(5)])
    bad += [('ZIP_total',central_patch(central_patch(many,20,v.MAX_FILE_BYTES),24,v.MAX_FILE_BYTES))]
    original_open=zipfile.ZipFile.open
    for name,data in bad:
        calls=[]
        def no_decompression(*args,**kw):calls.append(True);raise RuntimeError('decompression before metadata rejection')
        zipfile.ZipFile.open=no_decompression
        try:reject(name,lambda data=data:v.inspect_archive(data,good_expected));need(not calls,name+' decompressed')
        finally:zipfile.ZipFile.open=original_open
    bad_expected=copy.deepcopy(good_expected);bad_expected['a.txt']['sha256']='0'*64
    reject('ZIP_expanded_hash',lambda:v.inspect_archive(good,bad_expected),'expanded hash')
    reject('ZIP_external_manifest_anchor',lambda:v.verify_zip(archive,'0'*64),'external manifest anchor')
    # Direct semantic checks bypass all package hashes deliberately. Each mutant
    # therefore exercises mathematical/schema guards rather than only stale pins.
    author=base/v.PREFIX/'author_v3/packet';cert=json.loads((author/'CERTIFICATE.json').read_bytes())
    semantic=[('wrong_rank_three','first_coefficients',[0,-6,-12]),('zero_Casson','casson_normalization',0),('boolean_rank','ranks',[True,2,3]),('wrong_residual','second_difference',0),('wrong_parameter','quantum_parameter','q=1+2*x'),('wrong_forced','forced_rank_three',-24)]
    for mode,flag in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
        for name,key,val in semantic:
            dest=t/'semantic';shutil.copytree(author,dest)
            d=copy.deepcopy(cert);d[key]=val;(dest/'CERTIFICATE.json').write_text(json.dumps(d))
            run=subprocess.run([sys.executable,'-I','-S','-B',*flag,str(dest/'verify.py')],cwd=t,capture_output=True,timeout=10)
            need(run.returncode!=0 and b'REJECT:' in run.stderr,'semantic guard '+name+' '+mode);event('semantic_'+name+'_'+mode,'REJECTED',stderr=run.stderr.decode().strip());shutil.rmtree(dest)
    # Check output/time bounds with inert one-process fixtures only.
    reject('child_stdout_cap',lambda:v.run_bounded([sys.executable,'-I','-S','-B','-c','print("x"*10000)'],t,{},stdout_cap=50),'output cap')
    reject('child_stderr_cap',lambda:v.run_bounded([sys.executable,'-I','-S','-B','-c','import sys; sys.stderr.write("x"*10000)'],t,{},stderr_cap=50),'output cap')
    reject('child_wall_time_cap',lambda:v.run_bounded([sys.executable,'-I','-S','-B','-c','import time; time.sleep(2)'],t,{},seconds=0.03),'wall-time cap')
    noflags=subprocess.run([sys.executable,'-B',str(HERE/'verify_package.py')],capture_output=True,timeout=10)
    need(noflags.returncode!=0 and b'PROFILE_STARTUP' in noflags.stderr,'startup guard');event('startup_missing_flags','REJECTED')
    final=v.verify(str(base),anchor);need(final[1]==payload and final[2]==manifest_raw,'baseline changed')
receipt={'schema':'pr952-engineering-negative-profile-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_INERT_ENGINEERING_CONTROLS','outer_test_optimization':sys.flags.optimize,'externally_supplied_verifier_sha256':a.verifier_sha256,'event_count':len(EVENTS),'events':EVENTS,'cold_modes':baseline_receipts,'real_service_mutations':0,'clean_full_package_review_credit':False,'historical_receipts_modified':False}
print(json.dumps(receipt,sort_keys=True))
