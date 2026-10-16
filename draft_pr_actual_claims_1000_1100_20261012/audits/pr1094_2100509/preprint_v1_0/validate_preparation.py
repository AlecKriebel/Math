"""Actual preparation harness; mutates only disposable copies in own tmp/."""
from pathlib import Path
import datetime
import hashlib
import io
import json
import os
import platform
import shutil
import subprocess
import sys
import zipfile

P=Path(__file__).resolve().parent
K=P/'kit'; V=P/'validation'; T=P/'tmp'
ARCH=P/'pr1094_supportkit_v1.0.zip'
commands=[]; faults=[]
def need(ok,msg):
    if not ok: raise ValueError(msg)
def sha(data): return hashlib.sha256(data).hexdigest()
def pins(root):
    return {x.relative_to(root).as_posix():sha(x.read_bytes())
            for x in root.rglob('*') if x.is_file() and not x.is_symlink()}
def command(cwd,args,ok=True,label=''):
    r=subprocess.run(args,cwd=cwd,capture_output=True)
    row={'label':label,'argv':args,'exit':r.returncode,'stdout_sha256':sha(r.stdout),
         'stderr_sha256':sha(r.stderr),'stdout':r.stdout.decode(errors='replace'),
         'stderr':r.stderr.decode(errors='replace')}
    commands.append(row)
    need((r.returncode==0)==ok,'unexpected command outcome '+label)
    return r
def restore():
    root=T/'adversarial_copy'
    if root.exists(): shutil.rmtree(root)
    root.mkdir()
    with zipfile.ZipFile(ARCH) as z: z.extractall(root)
    return root
def main():
    original=pins(K)
    # Independent closed archive implementation, followed by read of every
    # central header and every decompressed payload.
    names=sorted(x.relative_to(K).as_posix() for x in K.rglob('*') if x.is_file())
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w') as z:
        for name in names:
            q=zipfile.ZipInfo(name,(1980,1,1,0,0,0));q.create_system=3
            q.external_attr=0o100644<<16;q.compress_type=0
            z.writestr(q,(K/name).read_bytes())
    need(b.getvalue()==ARCH.read_bytes(),'independent closed ZIP rebuild')
    with zipfile.ZipFile(ARCH) as z:
        need(z.namelist()==names and z.testzip() is None,'ZIP inventory/CRC')
        for q in z.infolist():
            need(q.date_time==(1980,1,1,0,0,0) and q.create_system==3
                 and q.external_attr==0o100644<<16 and q.compress_type==0,'ZIP header')
            need(z.read(q.filename)==(K/q.filename).read_bytes(),'ZIP payload')
    clean=T/'clean_extract';clean.mkdir()
    with zipfile.ZipFile(ARCH) as z:z.extractall(clean)
    results=[]
    for optimized in [False,True]:
        mode='optimized' if optimized else 'ordinary'
        py=[sys.executable,'-B']+(['-O'] if optimized else [])
        command(clean,py+['scripts/verify_kit.py'],label=mode+' default absent binding')
        out=T/('clean_checks_'+mode+'.json')
        command(clean,py+['scripts/run_checks.py','--out',str(out)],label=mode+' exact mathematical checks')
        results.append(json.loads(out.read_text()))
        support=T/('clean_support_'+mode+'.zip')
        command(clean,py+['scripts/build_support.py','--out',str(support)],label=mode+' support rebuild')
        need(support.read_bytes()==ARCH.read_bytes(),'clean archive byte equality')
        pdfdir=T/('clean_pdf_'+mode)
        command(clean,py+['scripts/build_pdf.py','--out-dir',str(pdfdir)],label=mode+' actual PDF rebuild')
        need((pdfdir/'paper.pdf').read_bytes()==(P/'paper.pdf').read_bytes(),'clean PDF byte equality')
        command(K,py+['scripts/verify_kit.py','--require-binding'],label=mode+' canonical strict binding')
    need(results[0]==results[1]==json.loads((V/'new_controls.json').read_text()),'full check output comparison')
    # Every case starts from a new byte-identical extraction, never canonical
    # files. A rejected writer must leave all preexisting regular bytes alone.
    for optimized in [False,True]:
        py=[sys.executable,'-B']+(['-O'] if optimized else [])
        for script,flag in [('run_checks.py','--out'),('build_support.py','--out'),('build_pdf.py','--out-dir')]:
            for kind in ['existing','hardlink_external','symlink_leaf','symlink_ancestor','inside_kit','ancestor_of_kit']:
                root=restore(); case=T/'writer_case'
                if case.exists():shutil.rmtree(case)
                case.mkdir(); protected=case/'external_descriptor.json';protected.write_bytes(b'protected input\n')
                if kind=='existing': target=root/'paper.tex'
                elif kind=='hardlink_external': target=case/'alias';os.link(protected,target)
                elif kind=='symlink_leaf': target=case/'alias';target.symlink_to(protected)
                elif kind=='symlink_ancestor':
                    (case/'alias').symlink_to(root,target_is_directory=True);target=case/'alias'/'new-output'
                elif kind=='inside_kit':target=root/'new-output'
                else:target=root.parent
                before=pins(root); outside=protected.read_bytes()
                command(root,py+['scripts/'+script,flag,str(target)],ok=False,label='writer '+script+' '+kind+' '+str(optimized))
                need(pins(root)==before and protected.read_bytes()==outside,'writer mutated protected inputs')
                need(not (root/'new-output').exists(),'writer created forbidden output')
                faults.append({'mode_optimized':optimized,'writer':script,'fault':kind,'rejected_without_mutation':True})
        for kind in ['manifest_symlink','member_symlink','ancestor_symlink','missing_member','extra_member','payload_corrupt']:
            root=restore()
            if kind=='manifest_symlink':
                value=(root/'MANIFEST.json').read_bytes();(root/'MANIFEST.json').unlink()
                saved=T/'saved_manifest.json';saved.write_bytes(value);(root/'MANIFEST.json').symlink_to(saved)
            elif kind=='member_symlink':
                member=root/'paper.tex'; value=member.read_bytes();member.unlink()
                saved=T/'saved_paper.tex';saved.write_bytes(value);member.symlink_to(saved)
            elif kind=='ancestor_symlink':
                moved=T/'saved_historical'
                if moved.exists():shutil.rmtree(moved)
                (root/'historical').rename(moved);(root/'historical').symlink_to(moved,target_is_directory=True)
            elif kind=='missing_member':(root/'paper.tex').unlink()
            elif kind=='extra_member':(root/'extra.txt').write_text('unexpected')
            else:(root/'paper.tex').write_bytes((root/'paper.tex').read_bytes()+b'\nchanged\n')
            before=pins(root)
            for script,args in [('verify_kit.py',[]),('run_checks.py',[]),('build_support.py',['--out',str(T/'must_not_exist.zip')])]:
                command(root,py+['scripts/'+script]+args,ok=False,label='input '+kind+' '+script+' '+str(optimized))
                need(pins(root)==before,'input rejection mutated files')
                need(not (T/'must_not_exist.zip').exists(),'invalid kit reached archive writer')
            faults.append({'mode_optimized':optimized,'input_fault':kind,'all_readers_and_archive_rejected':True})
        root=restore()
        for args,label in [(['--require-binding'],'required default absent'),
                           (['--binding',str(T/'missing_binding.json')],'explicit absent')]:
            command(root,py+['scripts/verify_kit.py']+args,ok=False,label=label+' '+str(optimized))
        # Explicit present corrupt binding and symlink bootstrap both fail.
        bad=T/'bad_binding.json';bad.write_text('{}\n')
        command(root,py+['scripts/verify_kit.py','--binding',str(bad)],ok=False,label='present corrupt binding '+str(optimized))
        link=T/'linked_binding.json'
        if link.is_symlink():link.unlink()
        link.symlink_to(P/'DEPOSIT_BINDING.json')
        command(root,py+['scripts/verify_kit.py','--binding',str(link)],ok=False,label='binding symlink '+str(optimized))
    repo=P
    while not (repo/'zenodo_deposit_tool/zenodo.py').exists():repo=repo.parent
    native=command(repo,[sys.executable,str(repo/'zenodo_deposit_tool/zenodo.py'),'check',str(P/'zenodo-deposit.json')],label='actual repository local uploader check')
    (V/'REPOSITORY_UPLOADER_LOCAL_CHECK.json').write_bytes(native.stdout)
    # Byte custody for every preexisting file, including private bodies; they
    # are rehashed only and are not copied to the publication payload.
    frozen=json.loads((P/'FROZEN_INPUT_PINS.json').read_text());preserved=[]
    for r in frozen['records']:
        value=(P.parent/r['path']).read_bytes()
        need(len(value)==r['bytes'] and sha(value)==r['sha256'],'preexisting input changed')
        preserved.append(r['path'])
    need(pins(K)==original,'canonical kit changed during validation')
    report={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'python':platform.python_version(),'platform':platform.platform(),
            'commands':commands,'command_count':len(commands),'fault_cases':faults,
            'expected_rejections':sum(x['exit']!=0 for x in commands),
            'full_new_math_result':results[0],'normal_optimized_full_result_equal':True,
            'independent_closed_archive_byte_equal':True,'archive_members':len(names),
            'clean_normal_optimized_pdf_byte_equal':True,'all_prior_inputs_unchanged':len(preserved),
            'canonical_payload_unchanged':True,'services_performed':False}
    (V/'FINAL_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'commands','fault_cases','full_new_math_result'}},indent=2))
if __name__=='__main__':main()
