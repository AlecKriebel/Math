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
receipts=json.loads((HERE/"COMMAND_RECEIPTS.json").read_text())
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

scratch=Path(json.loads((HERE/'SCRATCH_ROOT.json').read_text())['root'])
kit=scratch/'CleanKit'
summary={'resume_after_harness_correction':True}
guard=scratch/'GuardKit'
# Bootstrap manifest refusal is checked without parsing the malicious bytes.
# Existing isolated guard kit retained from the first run.
manifest=guard/'MANIFEST.json';mb=manifest.read_bytes();bad=scratch/'malformed-manifest';bad.write_bytes(b'not json')
manifest.unlink();manifest.symlink_to(bad)
for opt in (False,True):
    mode='optimized' if opt else 'normal';base=[PY]+(['-O'] if opt else [])+['-B']
    r=cmd('resume_manifest_symlink_'+mode,base+[guard/'scripts/verify.py'],guard,ok=1)
    check(b'symlink component' in r.stderr and b'JSONDecodeError' not in r.stderr,'manifest preparse check')
manifest.unlink();manifest.write_bytes(mb)
ancestral=scratch/'LinkedAncestor'
check(ancestral.is_symlink(),'retained alias premise')
for opt in (False,True):
    mode='optimized' if opt else 'normal';base=[PY]+(['-O'] if opt else [])+['-B']
    r=cmd('direct_manifest_ancestor_'+mode,base+['-c',"import sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import common;common.KIT=Path(sys.argv[2]);common.inventory()",str(guard/'scripts'),str(ancestral)],guard,ok=1)
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
print(json.dumps({'status':'PASS','scratch':str(scratch),'commands':len(receipts),'ZIP_members':json.loads((HERE/'ZIP_CLOSED.json').read_text())['count'],'guard_rejections':len(guard_checks)},sort_keys=True))
