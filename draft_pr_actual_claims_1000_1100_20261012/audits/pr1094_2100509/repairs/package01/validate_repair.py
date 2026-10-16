"""Actual local tests in one disposable extraction; never compile or render."""
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

sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent; A=R.parent.parent
P=A/'preprint_v1_0'; K=P/'kit'; T=R/'tmp'
ARCH=P/'pr1094_supportkit_v1.0.zip'
commands=[]; faults=[]; cleanups=[]

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def need(ok,text):
    if not ok: raise ValueError(text)
def writej(p,d): p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def pins(root):
    return {p.relative_to(root).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
            for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()}
def cleanup(path,label):
    if not path.exists() and not path.is_symlink():return
    if path.is_symlink():
        cleanups.append({'label':label,'path':path.relative_to(R).as_posix(),'symlink_target':os.readlink(path)})
        path.unlink(); return
    if path.is_file():
        b=path.read_bytes();cleanups.append({'label':label,'path':path.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)})
        path.unlink();return
    for p in sorted(path.rglob('*')):
        if p.is_file() and not p.is_symlink():
            b=p.read_bytes();cleanups.append({'label':label,'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)})
        elif p.is_symlink():
            cleanups.append({'label':label,'path':p.relative_to(R).as_posix(),'symlink_target':os.readlink(p)})
    shutil.rmtree(path)
def command(cwd,args,ok=True,label='',error=None):
    done=subprocess.run(args,cwd=cwd,capture_output=True)
    row={'label':label,'argv':[str(x) for x in args],'cwd':str(cwd),'exit':done.returncode,
         'stdout':done.stdout.decode(errors='replace'),'stderr':done.stderr.decode(errors='replace'),
         'stdout_sha256':sha(done.stdout),'stderr_sha256':sha(done.stderr)}
    commands.append(row)
    writej(R/'COMMAND_RECEIPTS_IN_PROGRESS.json',{'utc':now(),'commands':commands,'status':'IN_PROGRESS'})
    need((done.returncode==0)==ok,'unexpected command outcome: '+label)
    if error is not None: need(error in row['stderr'],'wrong rejection: '+label)
    return done
def restore():
    root=T/'kitroot'
    cleanup(root,'disposable extraction reset')
    root.mkdir()
    with zipfile.ZipFile(ARCH) as archive:archive.extractall(root)
    return root
def immutable_since_freeze():
    frozen=json.loads((R/'FROZEN_INPUT_PINS.json').read_text())
    changes=json.loads((R/'INPUT_PRESERVATION.json').read_text())['allowed_changes']
    changed={x['path']:x for x in changes}
    for row in frozen['records']:
        p=A/row['path']; actual={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
        want=changed[row['path']]['after'] if row['path'] in changed else {k:row[k] for k in ('bytes','sha256')}
        need(actual==want,'protected input changed during tests: '+row['path'])
    return len(frozen['records']),len(changed)

def main():
    need(not T.exists(),'scratch must be absent; preserve any interrupted evidence before continuation')
    T.mkdir()
    original=pins(K)
    need(immutable_since_freeze()==(309,8),'unexpected frozen boundary')
    # Independent implementation: read bytes only AFTER ZipFile is closed.
    names=sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file())
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w') as archive:
        for name in names:
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.create_system=3
            info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_STORED
            archive.writestr(info,(K/name).read_bytes())
    need(buffer.getvalue()==ARCH.read_bytes(),'independent CLOSED archive differs')
    with zipfile.ZipFile(ARCH) as archive:
        need(archive.namelist()==names and len(names)==len(set(names)),'archive inventory')
        need(archive.testzip() is None,'archive CRC')
        for info in archive.infolist():
            need(info.date_time==(1980,1,1,0,0,0) and info.create_system==3
                 and info.external_attr==0o100644<<16 and info.compress_type==zipfile.ZIP_STORED,'archive header')
            need(archive.read(info.filename)==(K/info.filename).read_bytes(),'archive payload')
    root=restore();results=[]
    case_identity=[]
    for optimized in (False,True):
        mode='optimized' if optimized else 'ordinary'
        py=[sys.executable,'-B']+(['-O'] if optimized else [])
        command(root,py+['scripts/verify_kit.py'],label=mode+' clean documented verifier, default absent')
        result=command(root,py+['scripts/run_checks.py','--out','../safe-checks-'+mode+'.json'],label=mode+' documented checker and safe dot-dot sibling')
        results.append(json.loads(result.stdout))
        need(json.loads((T/('safe-checks-'+mode+'.json')).read_text())==results[-1],'saved exact checks differ')
        out=T/('safe-support-'+mode+'.zip')
        command(root,py+['scripts/build_support.py','--out','../'+out.name],label=mode+' documented archive and safe dot-dot sibling')
        need(out.read_bytes()==ARCH.read_bytes(),'safe sibling archive differs')
        cleanup(out,'completed byte-identical archive')
        # The source and PDF are unchanged and compilation is expressly out
        # of this repair. Test the PDF writer preflight positively by reaching
        # its specific compiler-unavailable check after a safe ../ target.
        command(root,py+['scripts/build_pdf.py','--out-dir','../safe-pdf-'+mode,
                        '--tectonic','pr1094-no-compiler-for-path-test'],ok=False,
                label=mode+' PDF safe dot-dot passes path guard; no compilation',error='tectonic compiler unavailable')
        need(not (T/('safe-pdf-'+mode)).exists(),'compiler-unavailable case wrote output')
        command(K,py+['scripts/verify_kit.py','--require-binding'],label=mode+' canonical present strict binding')
        command(K,py+['scripts/verify_kit.py','--binding','../DEPOSIT_BINDING.json','--require-binding'],label=mode+' explicit present strict binding')
        for script,flag in (('run_checks.py','--out'),('build_support.py','--out'),('build_pdf.py','--out-dir')):
            for kind in ('existing_input','existing_external','hardlink_external','leaf_symlink',
                         'ancestor_symlink','symlink_dotdot','dangling_symlink_dotdot',
                         'inside_kit','ancestor_of_kit','case_alias_direct','case_alias_missing_chain'):
                case=T/'writer_case';cleanup(case,'completed previous writer fault');case.mkdir()
                protected=case/'external_paper.pdf';protected.write_bytes((P/'paper.pdf').read_bytes())
                if kind=='existing_input':target=root/'paper.tex';error='output must be absent'
                elif kind=='existing_external':target=protected;error='output must be absent'
                elif kind=='hardlink_external':
                    target=case/'hardlink';os.link(protected,target);error='output must be absent'
                elif kind=='leaf_symlink':
                    target=case/'link';target.symlink_to(protected);error='symlink component'
                elif kind=='ancestor_symlink':
                    link=case/'link';link.symlink_to(root,target_is_directory=True);target=link/'fresh';error='symlink component'
                elif kind in ('symlink_dotdot','dangling_symlink_dotdot'):
                    link=case/'lexical-link';link.symlink_to(root if kind=='symlink_dotdot' else case/'absent-target',target_is_directory=True)
                    target=link/'..'/'fresh';error='symlink component'
                elif kind=='inside_kit':target=root/'fresh';error='output overlaps protected kit'
                elif kind=='ancestor_of_kit':target=root.parent;error='output must be absent'
                else:
                    alias=root.with_name(root.name.upper())
                    need(alias.samefile(root),'this actual host did not supply the asserted case alias')
                    case_identity.append({'mode':mode,'writer':script,'kind':kind,
                        'alias':str(alias),'root':str(root),'samefile':True,
                        'dev':root.stat().st_dev,'inode':root.stat().st_ino})
                    target=alias/'fresh' if kind=='case_alias_direct' else alias/'absent1'/'absent2'/'fresh'
                    error='output physically overlaps protected kit'
                before=pins(root);outside=protected.read_bytes()
                command(root,py+['scripts/'+script,flag,str(target)],ok=False,
                        label=mode+' writer '+script+' '+kind,error=error)
                need(pins(root)==before and protected.read_bytes()==outside,'writer fault mutated inputs')
                need(not (root/'fresh').exists() and not (root/'absent1').exists(),'writer created a protected descendant')
                need(not (case/'fresh').exists(),'lexical dot-dot guard wrote sibling')
                faults.append({'mode':mode,'writer':script,'fault':kind,'rejected_before_any_write':True})
        cleanup(T/'writer_case','completed writer fault')
        for kind in ('manifest_symlink','manifest_duplicate','member_symlink','missing_member','extra_member','payload_corrupt'):
            root=restore()
            if kind=='manifest_symlink':
                member=root/'MANIFEST.json';saved=T/'saved_manifest.json';saved.write_bytes(member.read_bytes());member.unlink();member.symlink_to(saved)
                error='symlink component'
            elif kind=='manifest_duplicate':
                path=root/'MANIFEST.json';data=json.loads(path.read_text());data['records'].append(data['records'][0]);path.write_text(json.dumps(data));error='duplicate manifest paths'
            elif kind=='member_symlink':
                member=root/'paper.tex';saved=T/'saved_paper.tex';saved.write_bytes(member.read_bytes());member.unlink();member.symlink_to(saved);error='symlink component'
            elif kind=='missing_member':(root/'paper.tex').unlink();error='manifest inventory differs'
            elif kind=='extra_member':(root/'unexpected').write_text('new');error='manifest inventory differs'
            else:(root/'paper.tex').write_bytes((root/'paper.tex').read_bytes()+b'changed');error='payload mismatch'
            before=pins(root)
            for script,args in (('verify_kit.py',[]),('run_checks.py',[]),('build_support.py',['--out',str(T/'must-not-exist.zip')])):
                command(root,py+['scripts/'+script]+args,ok=False,label=mode+' input '+kind+' '+script,error=error)
                need(pins(root)==before and not (T/'must-not-exist.zip').exists(),'invalid input wrote bytes')
            faults.append({'mode':mode,'input_fault':kind,'all_readers_and_archive_rejected':True})
        root=restore()
        for args,label in ((['--require-binding'],'required default absent'),
                           (['--binding',str(T/'absent-binding.json')],'explicit absent')):
            command(root,py+['scripts/verify_kit.py']+args,ok=False,label=mode+' '+label,error='required or explicit binding is absent')
        bad=T/'DEPOSIT_BINDING.json';bad.write_text('{}\n')
        command(root,py+['scripts/verify_kit.py'],ok=False,label=mode+' present default corrupt cannot fall back',error='binding keys')
        command(root,py+['scripts/verify_kit.py','--binding',str(bad)],ok=False,label=mode+' explicit present corrupt',error='binding keys')
        bad.unlink()
        link=T/'binding-link';link.symlink_to(P/'DEPOSIT_BINDING.json')
        command(root,py+['scripts/verify_kit.py','--binding',str(link)],ok=False,label=mode+' binding leaf symlink',error='symlink component')
        command(root,py+['scripts/verify_kit.py','--binding',str(link/'..'/'absent-binding.json')],ok=False,
                label=mode+' binding lexical symlink dot-dot',error='symlink component')
        link.unlink()
    need(results[0]==results[1]==json.loads((K/'NEW_CONTROLS_RESULT.json').read_text()),'full normal/optimized exact result differs')
    repo=A
    while not (repo/'zenodo_deposit_tool/zenodo.py').exists():repo=repo.parent
    native=command(repo,[sys.executable,'-B',str(repo/'zenodo_deposit_tool/zenodo.py'),'check',str(P/'zenodo-deposit.json')],label='actual repository LOCAL uploader check')
    (R/'REPOSITORY_UPLOADER_LOCAL_CHECK.json').write_bytes(native.stdout)
    need(pins(K)==original,'canonical kit changed during tests')
    before,changed=immutable_since_freeze()
    report={'utc':now(),'status':'PASS','python':platform.python_version(),'platform':platform.platform(),
        'command_count':len(commands),'expected_rejections':sum(x['exit']!=0 for x in commands),
        'commands':commands,'fault_cases':faults,'actual_case_alias_identity_checks':case_identity,
        'independent_CLOSED_archive_byte_equal':True,'archive_members':len(names),
        'normal_optimized_full_math_JSON_equal':True,'math_result':results[0],
        'protected_before_inputs':before,'only_allowed_changes':changed,'canonical_kit_unchanged_during_tests':True,
        'all_three_writers_lexical_symlink_dotdot_rejected':True,
        'all_three_writers_case_alias_and_missing_chain_rejected':True,
        'safe_dotdot_checker_archive_positive':True,
        'safe_dotdot_PDF_preflight_reached_compiler_unavailable_without_writing':True,
        'new_compile_or_render':False,'paper_PDF_metadata_unchanged':True,'services_performed':False}
    writej(R/'VALIDATION.json',report)
    cleanup(T,'completed own disposable extraction and derivatives only')
    writej(R/'OWN_SCRATCH_CLEANUP.json',{'utc':now(),'records':cleanups,'only_own_repair_tmp_removed':True})
    print(json.dumps({k:v for k,v in report.items() if k not in ('commands','fault_cases','math_result','actual_case_alias_identity_checks')},indent=2))

if __name__=='__main__':main()
