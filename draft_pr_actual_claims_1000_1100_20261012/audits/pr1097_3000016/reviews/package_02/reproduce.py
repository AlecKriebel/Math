#!/usr/bin/env python3
"""Fresh whole-package test harness. Never writes to candidate or prior records."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import datetime, hashlib, json, os, shutil, stat, struct, subprocess, tempfile, unicodedata, zipfile, zlib

HERE=Path(__file__).absolute().parent
AUDIT=HERE.parent.parent
CAND= AUDIT/'preprint_v1_0'
PY=sys.executable
receipts=[]
def check(q,s):
    if not q: raise ValueError(s)
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(name,data):
    (HERE/name).write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
def cmd(label,args,cwd=None,env=None,ok=0):
    t=datetime.datetime.now(datetime.timezone.utc).isoformat()
    r=subprocess.run(list(map(str,args)),cwd=cwd,env=env,capture_output=True)
    (HERE/(label+'.stdout')).write_bytes(r.stdout)
    (HERE/(label+'.stderr')).write_bytes(r.stderr)
    receipts.append({'label':label,'utc':t,'argv':list(map(str,args)),'cwd':str(cwd or HERE),'returncode':r.returncode,'stdout':pin(HERE/(label+'.stdout')),'stderr':pin(HERE/(label+'.stderr'))})
    save('COMMAND_RECEIPTS.json',receipts)
    check((r.returncode==0) if ok==0 else (r.returncode!=0),label+' unexpected exit')
    return r
def re_manifest(kit):
    p=kit/'MANIFEST.json';v=json.loads(p.read_text());v['entries']=[{'path':q.relative_to(kit).as_posix(),**pin(q)} for q in sorted(kit.rglob('*')) if q.is_file() and q!=p];p.write_text(json.dumps(v,indent=2)+'\n')
def setroots(kit,roots):
    p=kit/'PROTECTED_PATHS.json';v=json.loads(p.read_text());v['original_protected_roots']=list(map(str,roots));p.write_text(json.dumps(v,indent=2)+'\n');re_manifest(kit)

scratch=Path(tempfile.mkdtemp(prefix='pr1097-package02-',dir='/private/tmp'))
save('SCRATCH_ROOT.json',{'root':str(scratch),'scope':'Only this review owns these new derivatives; no third-party bodies or runtimes copied.'})
kit=scratch/'CleanKit';kit.mkdir()
with zipfile.ZipFile(CAND/'pr1097_support_v1_0.zip') as z:z.extractall(kit)
expected=json.loads((kit/'EXPECTED_RESULTS.json').read_text())
summary={'checks':[],'scratch':str(scratch)}
for opt in (False,True):
    mode='optimized' if opt else 'normal';base=[PY]+(['-O'] if opt else [])+['-B']
    r=cmd('checks_'+mode,base+[kit/'scripts/run_checks.py'],kit)
    check(json.loads(r.stdout)==expected,'complete expected JSON equality')
    cmd('fault_'+mode,base+[kit/'scripts/run_checks.py','--inject-failure'],kit,ok=1)
    a=json.loads(cmd('verify_optional_'+mode,base+[kit/'scripts/verify.py'],kit).stdout)
    check(a['binding']['state']=='ABSENT_OPTIONAL','default optional absent')
    cmd('verify_required_absent_'+mode,base+[kit/'scripts/verify.py','--require-binding'],kit,ok=1)
    cmd('verify_explicit_missing_'+mode,base+[kit/'scripts/verify.py','--binding',scratch/'missing.json'],kit,ok=1)
    a=json.loads(cmd('verify_explicit_present_'+mode,base+[kit/'scripts/verify.py','--binding',CAND/'DEPOSIT_BINDING.json','--require-binding'],kit).stdout)
    check(a['binding']['state']=='PRESENT_VERIFIED','explicit binding present')
    a=json.loads(cmd('verify_canonical_'+mode,base+[CAND/'kit/scripts/verify.py','--require-binding'],CAND/'kit').stdout)
    check(a['binding']['state']=='PRESENT_VERIFIED','canonical default present')
    out=scratch/('rebuilt_'+mode+'.zip');cmd('build_'+mode,base+[kit/'scripts/build_support.py','--out',out],kit)
    check(pin(out)==pin(CAND/'pr1097_support_v1_0.zip'),'byte exact ZIP rebuild')
    cmd('pdf_'+mode,base+[kit/'scripts/rebuild_pdf.py','--out-dir',scratch/('PDF_'+mode)],kit)
    summary['checks'].append(mode+' full checks equality; unconditional fault; optional/required/explicit binding; ZIP and PDF supported writers')

# A present binding is checked even in default mode. Deliveries use copied authored assets only.
for name in ('DEPOSIT_BINDING.json','paper.pdf','pr1097_support_v1_0.zip','zenodo-deposit.json','.zenodo.json','zenodo-metadata.json'):
    shutil.copyfile(CAND/name,scratch/name)
for opt in (False,True):
    mode='optimized' if opt else 'normal';base=[PY]+(['-O'] if opt else [])+['-B']
    cmd('default_present_'+mode,base+[kit/'scripts/verify.py'],kit)
    bp=scratch/'DEPOSIT_BINDING.json';orig=bp.read_bytes();v=json.loads(orig);v['metadata']['version']='corrupted';bp.write_text(json.dumps(v))
    cmd('default_corrupt_binding_'+mode,base+[kit/'scripts/verify.py'],kit,ok=1);bp.write_bytes(orig)
    bp.unlink();bp.symlink_to(scratch/'absent-binding')
    cmd('broken_binding_symlink_'+mode,base+[kit/'scripts/verify.py'],kit,ok=1);bp.unlink();bp.write_bytes(orig)
cmd('native_local_check',[PY,'-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',CAND/'zenodo-deposit.json'],'/Users/alec/Documents/Math')

# Independent complete ZIP payload and raw local-header/central-directory audit.
zp=CAND/'pr1097_support_v1_0.zip';raw=zp.read_bytes();members=[]
with zipfile.ZipFile(zp) as z:
    check(z.comment==b'','ZIP archive comment')
    names=z.namelist();actual=sorted(q.relative_to(CAND/'kit').as_posix() for q in (CAND/'kit').rglob('*') if q.is_file())
    check(names==actual==sorted(set(names)),'closed ZIP exact sorted inventory')
    for info in z.infolist():
        data=z.read(info);check(data==(CAND/'kit'/info.filename).read_bytes(),'ZIP exact member bytes')
        check(info.compress_type==0 and info.date_time==(1980,1,1,0,0,0) and info.create_system==3 and info.external_attr==(0o100644<<16) and info.extra==b'' and info.comment==b'' and info.flag_bits==0,'ZIP member header policy')
        h=struct.unpack_from('<4s5H3I2H',raw,info.header_offset)
        check(h[0]==b'PK\x03\x04' and h[2]==0 and h[3]==0 and h[4]==0 and h[5]==33 and h[6]==zlib.crc32(data) and h[7]==len(data) and h[8]==len(data) and h[10]==0,'raw local header/CRC')
        name=raw[info.header_offset+30:info.header_offset+30+h[9]];check(name.decode()==info.filename,'local member name')
        check(raw[info.header_offset+30+h[9]:info.header_offset+30+h[9]+len(data)]==data,'local payload')
        members.append({'path':info.filename,**pin(CAND/'kit'/info.filename),'CRC32':info.CRC,'header_offset':info.header_offset})
save('ZIP_CLOSED.json',{'zip':pin(zp),'members':members,'count':len(members),'header_policy':'Every local header and central entry independently checked; exact uncompressed bytes/CRC, sorted inventory, no extras/comments.'})

# Bootstrap manifest refusal is checked without parsing the malicious bytes.
guard= scratch/'GuardKit';shutil.copytree(kit,guard)
manifest=guard/'MANIFEST.json';mb=manifest.read_bytes();bad=scratch/'malformed-manifest';bad.write_bytes(b'not json')
manifest.unlink();manifest.symlink_to(bad)
for opt in (False,True):
    mode='optimized' if opt else 'normal';base=[PY]+(['-O'] if opt else [])+['-B']
    r=cmd('manifest_symlink_'+mode,base+[guard/'scripts/verify.py'],guard,ok=1)
    check(b'symlink component' in r.stderr and b'JSONDecodeError' not in r.stderr,'manifest preparse check')
manifest.unlink();manifest.write_bytes(mb)
ancestral=scratch/'LinkedAncestor';ancestral.symlink_to(guard,target_is_directory=True)
for opt in (False,True):
    mode='optimized' if opt else 'normal';base=[PY]+(['-O'] if opt else [])+['-B']
    r=cmd('manifest_ancestor_'+mode,base+[ancestral/'scripts/verify.py'],ancestral,ok=1)
    check(b'symlink component' in r.stderr,'manifest ancestry preflight')

# Both actual supported writers, disposable original-root configuration only.
# Fake compiler records invocation, making rejection-before-child directly falsifiable.
fake=scratch/'FakeBin';fake.mkdir();marker=scratch/'compiler-invoked'
compiler=fake/'tectonic';compiler.write_text('#!/bin/sh\nprintf invoked > '+str(marker)+'\nexit 91\n');compiler.chmod(0o700)
env=dict(os.environ);env['PATH']=str(fake)+os.pathsep+env.get('PATH','')
original=scratch/'OriginalProtected';original.mkdir()
unicode_root=scratch/'Prot\u00e9g\u00e9';unicode_root.mkdir()
unicode_alias=Path(unicodedata.normalize('NFD',str(unicode_root)))
check(os.path.samefile(guard,guard.with_name('gUARDkIT')),'actual case alias premise')
check(os.path.samefile(unicode_root,unicode_alias),'actual normalization alias premise')
existing=scratch/'occupied';existing.write_text('sentinel')
hard=scratch/'hardlink';os.link(existing,hard)
link=scratch/'link';link.symlink_to(existing)
linkdir=scratch/'linkdir';linkdir.symlink_to(original,target_is_directory=True)
occupied_dir=scratch/'occupied-pdf';occupied_dir.mkdir();(occupied_dir/'paper.tex').write_text('occupied compiler child')
cases=[('kit_nested',guard/'new'),('kit_case',guard.with_name('gUARDkIT')/'new'),('original_nested',original/'new'),('original_case',original.with_name('oRIGINALpROTECTED')/'new'),('normalization',unicode_alias/'new'),('regular_leaf',existing),('hardlink_leaf',hard),('symlink_leaf',link),('symlink_ancestor',linkdir/'new'),('occupied_directory',occupied_dir),('traversal',scratch/'component'/'..'/'new'),('missing_parent',scratch/'missing-parent'/'new')]
setroots(guard,[original,unicode_root])
guard_checks=[]
for opt in (False,True):
    mode='optimized' if opt else 'normal';base=[PY]+(['-O'] if opt else [])+['-B']
    for writer,flag in [('build_support.py','--out'),('rebuild_pdf.py','--out-dir')]:
        for name,target in cases:
            r=cmd('guard_'+mode+'_'+writer.split('.')[0]+'_'+name,base+[guard/'scripts'/writer,flag,target],guard,env,ok=1)
            check(not marker.exists(),'compiler invoked after guard rejection')
            check(not target.exists() or name in ('regular_leaf','hardlink_leaf','symlink_leaf','occupied_directory'),'rejected writer created output')
            guard_checks.append({'mode':mode,'writer':writer,'case':name,'returncode':r.returncode,'compiler_invoked':False})
    # Reverse direction: protected config itself uses actual aliases, output uses original spellings.
    setroots(guard,[original.with_name('oRIGINALpROTECTED'),unicode_alias])
    for writer,flag in [('build_support.py','--out'),('rebuild_pdf.py','--out-dir')]:
        for name,target in [('reverse_case',original/'reverse'),('reverse_normalization',unicode_root/'reverse')]:
            cmd('guard_'+mode+'_'+writer.split('.')[0]+'_'+name,base+[guard/'scripts'/writer,flag,target],guard,env,ok=1)
            check(not marker.exists() and not target.exists(),'reverse alias rejected prewrite')
            guard_checks.append({'mode':mode,'writer':writer,'case':name,'compiler_invoked':False})
    setroots(guard,[scratch/'absent-original-root'])
    cmd('absent_root_build_'+mode,base+[guard/'scripts/build_support.py','--out',scratch/('absent-root-'+mode+'.zip')],guard)
    cmd('absent_root_pdf_'+mode,base+[guard/'scripts/rebuild_pdf.py','--out-dir',scratch/('absent-root-pdf-'+mode)],guard)
    setroots(guard,[original,unicode_root])
save('WRITER_GUARDS.json',{'case_alias_samefile':True,'normalization_alias_samefile':True,'tests':guard_checks,'rejections':len(guard_checks),'absent_original_root_positive_both_writers_both_modes':True,'hostile_concurrent_mutation_tested':False})
save('PACKAGE_REPRODUCTION.json',summary)
# Pin every derivative before optional later cleanup; cleanup belongs to finalization.
save('SCRATCH_PINS.json',{'root':str(scratch),'files':[{'path':q.relative_to(scratch).as_posix(),**pin(q)} for q in sorted(scratch.rglob('*')) if q.is_file() and not q.is_symlink()]})
print(json.dumps({'status':'PASS','scratch':str(scratch),'commands':len(receipts),'ZIP_members':len(members),'guard_rejections':len(guard_checks)},sort_keys=True))
