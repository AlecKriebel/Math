#!/usr/bin/env python3
"""Actual isolated filesystem probes of v1.1's archive builder, static boundary.

Only fresh owned regular copies are changed. No hardlink to canonical files.
Every fixture identity is recorded before an owned unlink or rename mutation.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys

R=Path(__file__).absolute().parent
K=R.parents[1]/'preprint_v1_1/kit'
FIX=R/(sys.argv[1] if len(sys.argv)>1 else 'builder_fixtures')
RESULT_NAME=sys.argv[2] if len(sys.argv)>2 else 'BUILDER_TEST_RESULTS.json'

def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def identity(root):
    rows=[]
    for p in sorted(root.rglob('*')):
        s=p.lstat()
        v={'path':p.relative_to(root).as_posix(),'mode':stat.S_IFMT(s.st_mode),'inode':s.st_ino,'nlink':s.st_nlink}
        if stat.S_ISREG(s.st_mode):v.update(bytes=s.st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        elif stat.S_ISLNK(s.st_mode):v['target']=os.readlink(p)
        rows.append(v)
    return rows

def target_identity(path):
    if not os.path.lexists(path):return None
    s=path.lstat();d={'mode':stat.S_IFMT(s.st_mode),'inode':s.st_ino,'nlink':s.st_nlink}
    if stat.S_ISREG(s.st_mode):d['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    if stat.S_ISLNK(s.st_mode):d['target']=os.readlink(path)
    return d

CASES=['relative_inside','absolute_inside','nested_inside','case_alias_target','case_alias_root',
 'missing_inside_parent','missing_outside_parent','above_absent_via_traversal',
 'outside_traversal','existing_file','existing_directory','existing_symlink',
 'dangling_symlink','existing_hardlink','case_alias_existing','symlink_parent_to_inside',
 'symlink_parent_to_outside','symlink_root','changed_member','extra_member','missing_member',
 'member_symlink','member_symlink_ancestry','nonregular_fifo','duplicate_allowlist',
 'traversal_allowlist','bad_manifest','duplicate_manifest','success_absolute','success_outside_cwd']

def run():
    if FIX.exists():raise RuntimeError('fresh fixture directory required')
    FIX.mkdir()
    canonical_before=identity(K)
    records=[]
    first_success=None
    for index,name in enumerate(CASES):
        case=FIX/f'{index:02d}_{name}';case.mkdir()
        kit=case/'Kit';shutil.copytree(K,kit)
        out=case/'outside';out.mkdir()
        # Persist the complete new-copy ledger before any unlink/rename.
        dump(case/'INITIAL_COPY_IDENTITY.json',identity(kit))
        script=kit/'scripts/build_archive.py'
        cwd=kit;target=out/'new.zip';expected_success=False
        if name=='relative_inside':target=Path('inside.zip')
        elif name=='absolute_inside':target=kit/'inside.zip'
        elif name=='nested_inside':target=kit/'scripts/inside.zip'
        elif name=='case_alias_target':
            alias=case/'kIT'
            if not alias.exists() or not alias.samefile(kit):raise RuntimeError('case alias test needs case-insensitive fixture filesystem')
            target=alias/'inside.zip'
        elif name=='case_alias_root':
            alias=case/'kIT'
            if not alias.exists() or not alias.samefile(kit):raise RuntimeError('case alias test needs case-insensitive fixture filesystem')
            script=alias/'scripts/build_archive.py';target=kit/'inside.zip'
        elif name=='missing_inside_parent':target=kit/'absent/new.zip'
        elif name=='missing_outside_parent':target=out/'absent/new.zip'
        elif name=='above_absent_via_traversal':target=kit/'absent/../inside.zip'
        elif name=='outside_traversal':target=out/'../new.zip'
        elif name=='existing_file':target.write_bytes(b'existing target')
        elif name=='existing_directory':target.mkdir()
        elif name=='existing_symlink':target.symlink_to(kit/'paper.pdf')
        elif name=='dangling_symlink':target.symlink_to(out/'absent-target')
        elif name=='existing_hardlink':os.link(kit/'paper.pdf',target)
        elif name=='case_alias_existing':
            target.write_bytes(b'pre-existing target');target=out/'NEW.ZIP'
        elif name=='symlink_parent_to_inside':
            link=out/'link';link.symlink_to(kit,target_is_directory=True);target=link/'new.zip'
        elif name=='symlink_parent_to_outside':
            real=out/'real';real.mkdir();link=out/'link';link.symlink_to(real,target_is_directory=True);target=link/'new.zip'
        elif name=='symlink_root':
            link=case/'rootlink';link.symlink_to(kit,target_is_directory=True);script=link/'scripts/build_archive.py'
        elif name=='changed_member':
            with (kit/'README.md').open('ab') as stream:stream.write(b'changed')
        elif name=='extra_member':(kit/'extra.txt').write_bytes(b'extra')
        elif name=='missing_member':(kit/'paper.pdf').unlink()
        elif name=='member_symlink':
            member=kit/'paper.pdf';saved=out/'saved.pdf';member.rename(saved);member.symlink_to(saved)
        elif name=='member_symlink_ancestry':
            directory=kit/'historical';saved=out/'saved-historical';directory.rename(saved);directory.symlink_to(saved,target_is_directory=True)
        elif name=='nonregular_fifo':os.mkfifo(kit/'bad.fifo')
        elif name=='duplicate_allowlist':
            p=kit/'ALLOWLIST.json';a=json.loads(p.read_text());a['files'].append(a['files'][0]);dump(p,a)
        elif name=='traversal_allowlist':
            p=kit/'ALLOWLIST.json';a=json.loads(p.read_text());a['files'][0]='../escape';dump(p,a)
        elif name=='bad_manifest':(kit/'MANIFEST.json').write_text('{')
        elif name=='duplicate_manifest':
            p=kit/'MANIFEST.json';m=json.loads(p.read_text());m['files'][-1]=m['files'][0];dump(p,m)
        elif name=='success_absolute':expected_success=True
        elif name=='success_outside_cwd':expected_success=True;cwd=out;target=Path('new.zip')
        else:raise RuntimeError(name)
        before=identity(kit)
        dump(case/'PRE_COMMAND_KIT_IDENTITY.json',before)
        actual_target=target if target.is_absolute() else cwd/target
        existed=os.path.lexists(actual_target)
        before_target=target_identity(actual_target)
        baseline_output=None
        for flags in ([],['-O'],['-OO']):
            # Each successful mode has a fresh exclusive output name.
            mode_target=target
            if expected_success:
                suffix='normal' if not flags else flags[0][1:]
                mode_target=target.with_name('success-'+suffix+'.zip')
            cmd=[sys.executable,'-I','-B',*flags,str(script),str(mode_target)]
            proc=subprocess.run(cmd,cwd=cwd,capture_output=True,timeout=15)
            if (proc.returncode==0)!=expected_success:raise RuntimeError(name+' wrong outcome '+repr(proc.stderr))
            after=identity(kit)
            if after!=before:raise RuntimeError(name+' modified input tree')
            rec={'case':name,'mode':flags or ['normal'],'argv':cmd,'cwd':str(cwd),'exit':proc.returncode,'stdout':proc.stdout.decode(),'stderr':proc.stderr.decode(),'kit_before_after_identical':True}
            if expected_success:
                output=mode_target if mode_target.is_absolute() else cwd/mode_target
                data=output.read_bytes()
                if baseline_output is None:baseline_output=data
                if data!=baseline_output:raise RuntimeError('mode archive mismatch')
                if first_success is None:first_success=data
                if data!=first_success:raise RuntimeError('outside path changes archive bytes')
                rec.update(output_bytes=len(data),output_sha256=hashlib.sha256(data).hexdigest())
            else:
                if not existed and os.path.lexists(actual_target):raise RuntimeError(name+' created output on rejection')
                if target_identity(actual_target)!=before_target:raise RuntimeError(name+' changed existing target')
                rec['no_output_created_on_rejection']=not existed
            records.append(rec)
        dump(case/'COMMANDS.json',records[-3:])
    if identity(K)!=canonical_before:raise RuntimeError('canonical revision kit drift')
    result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','static_filesystem_only':True,
      'cases':len(CASES),'mode_processes':len(records),'negative_cases':len(CASES)-2,
      'successful_path_and_mode_archives_identical':True,'canonical_revision_kit_unchanged':True,
      'case_alias_both_directions_actually_exercised':True,'hardlinks_only_between_owned_fixture_files':True,'records':records}
    dump(R/RESULT_NAME,result)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))

if __name__=='__main__':run()
