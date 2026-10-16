#!/usr/bin/env python3
"""Bounded read-only canonical inventory plus disposable case-alias tests."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, zipfile

HERE = Path(__file__).resolve().parent
PROGRAM = HERE.parents[1]
AUDITS = PROGRAM / 'audits'
CONFIG = {
 1033: ('pr1033_11000026','publication','teichmuller_original_ball_paths_source_audits_v1.zip','research_note.pdf'),
 1034: ('pr1034_10400035','publication','source_audit_kit.zip','research_note.pdf'),
 1037: ('pr1037_30003822','preprint','pr1037_supportkit_v1.0.zip','paper/forest_transfer_catalan.pdf'),
 1041: ('pr1041_30003934','preprint_v1_0','supportkit-v1.0.tar.gz','output/pdf/paper.pdf'),
 1047: ('pr1047_30004909','preprint_v1_0','pr1047_supportkit_v1.0.zip','paper/matroid_rank_obstruction.pdf'),
 1052: ('pr1052_30005118','preprint_v1_0','pr1052_support_v1_0.zip','paper.pdf'),
 1064: ('pr1064_30001073','preprint_v1_0','support.zip','paper.pdf'),
 1071: ('pr1071_30002170','NEWpreprint_v1_0','PR1071_preprint_v1_0_support.zip','paper.pdf'),
 1085: ('pr1085_20000488','preprint_v1_0','pr1085_support_v1_0.zip','paper.pdf'),
}
def require(ok, msg):
    if not ok: raise RuntimeError(msg)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def record(p, base=PROGRAM):
    return {'path':p.relative_to(base).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(name, obj):
    (HERE/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def inventory():
    rows=[]
    for pr,(audit,kit,archive,pdf) in CONFIG.items():
        root=AUDITS/audit/kit
        files=sorted(p for p in root.rglob('*') if p.is_file())
        if pr==1033: files.append(AUDITS/audit/'build_package.py')
        for name in ('FINAL_SEAL.json','FINAL_INTEGRITY.json'):
            p=AUDITS/audit/name
            if p.is_file(): files.append(p)
        rows.append({'pr':pr,'root':str(root),'archive':record(root/archive),
                     'paper_pdf':record(root/pdf),'README':record(root/'README.md'),
                     'files':[record(p) for p in files]})
    return rows
def cmd(args,cwd,label):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    p=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True,timeout=120)
    result={'label':label,'argv':args,'cwd':str(cwd),'returncode':p.returncode,
            'stdout':p.stdout,'stderr':p.stderr}
    save('command_%03d.json'%len(COMMANDS),result)
    COMMANDS.append(result)
    return result
def physical(p):
    st=p.stat()
    return {'path':str(p),'resolve':str(p.resolve()),'device':st.st_dev,'inode':st.st_ino}
def tree(root):
    return {p.relative_to(root).as_posix():(p.stat().st_size,sha(p))
            for p in root.rglob('*') if p.is_file()}
def extract(archive,clean):
    clean.mkdir()
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None,'bad canonical ZIP')
        for i in z.infolist():
            p=Path(i.filename)
            require(not p.is_absolute() and '..' not in p.parts,'unsafe test extraction')
            require((i.external_attr>>16)&0o170000 !=0o120000,'no symlink extraction')
        z.extractall(clean)

COMMANDS=[]
def tests():
    results=[]
    for pr in (1052,1064,1071,1085):
        audit,kit,archive,pdf=CONFIG[pr]
        canonical=AUDITS/audit/kit
        scratch=HERE/'scratch'
        require(not scratch.exists(),'scratch must be absent')
        scratch.mkdir()
        clean=scratch/'clean'
        upper=scratch/'CLEAN'
        try:
            extract(canonical/archive,clean)
            require(os.path.samefile(clean,upper),'case alias must actually have same physical identity')
            require(clean.resolve()!=upper.resolve(),'lexical resolution must retain case difference')
            before=tree(clean)
            row={'pr':pr,'canonical_archive':record(canonical/archive),
                 'directory_alias':{'canonical':physical(clean),'uppercase':physical(upper),
                                    'samefile':os.path.samefile(clean,upper),
                                    'resolved_paths_equal':clean.resolve()==upper.resolve()},
                 'tests':[]}
            if pr==1052: script='build_support.py';flag='--output'
            elif pr==1064: script='build_archive.py';flag='--output'
            elif pr==1071: script='scripts/build_archive.py';flag='--out'
            else: script='build_archive.py';flag='--output'
            for optimized in (False,True):
                py=[sys.executable]+(['-O'] if optimized else [])+['-B']
                label='pr%d_%s'%(pr,'optimized' if optimized else 'normal')
                # An absolute, physically internal path spelled through uppercase
                # existing parent is the case under investigation.
                alias_out=upper/('case_alias_'+str(int(optimized))+'.zip')
                expected_physical=clean/alias_out.name
                require(not expected_physical.exists(),'fresh output only')
                got=cmd(py+[str(clean/script),flag,str(alias_out)],clean,label+'_case_alias')
                created=expected_physical.is_file()
                test={'optimized':optimized,'requested_output':str(alias_out),
                      'physically_internal_output':str(expected_physical),
                      'returncode':got['returncode'],'created':created,
                      'old_files_unchanged':all((clean/k).is_file() and
                         ((clean/k).stat().st_size,sha(clean/k))==v for k,v in before.items())}
                if created:
                    test.update(output_sha256=sha(expected_physical),
                                output_bytes=expected_physical.stat().st_size,
                                output_equals_canonical_archive=sha(expected_physical)==sha(canonical/archive),
                                same_output_inode=os.path.samefile(alias_out,expected_physical))
                    expected_physical.unlink()
                    sidecar=Path(str(expected_physical)+'.sha256')
                    if sidecar.exists(): sidecar.unlink()
                require(tree(clean)==before,'test did not preserve original extracted files')
                if pr in (1071,1085,1064):
                    require(got['returncode']==0 and created and test['old_files_unchanged'],
                            'hypothesized bypass NOT confirmed for PR'+str(pr))
                else:
                    require(got['returncode']!=0 and not created,'1052 uppercase input should be rejected')
                # Same spelling canonical containment control: 1064/1071/1085
                # forbid the fresh path tested above; 1052 intentionally permits it.
                direct=clean/('direct_'+str(int(optimized))+'.zip')
                got_direct=cmd(py+[str(clean/script),flag,str(direct)],clean,label+'_direct_control')
                direct_created=direct.is_file()
                test['canonical_spelling_control']={'returncode':got_direct['returncode'],
                                                    'created':direct_created}
                if direct_created:
                    direct.unlink()
                    sidecar=Path(str(direct)+'.sha256')
                    if sidecar.exists(): sidecar.unlink()
                require(tree(clean)==before,'direct control changed old extracted files')
                require((got_direct['returncode']==0 and direct_created) if pr==1052 else
                        (got_direct['returncode']!=0 and not direct_created),
                        'unexpected direct containment control')
                row['tests'].append(test)
            row['extracted_original_files_unchanged']=tree(clean)==before
            results.append(row)
            save('TEST_RESULTS.json',results)
        finally:
            # Only this audit-owned disposable extraction and its created outputs.
            shutil.rmtree(scratch)
    return results

if __name__=='__main__':
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    require(not (HERE/'CANONICAL_INPUT_PINS.json').exists(),'immutable first baseline already exists')
    baseline=inventory();save('CANONICAL_INPUT_PINS.json',{'utc':started,'packages':baseline})
    result=tests()
    current=inventory()
    save('CANONICAL_UNCHANGED.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'canonical_input_pins_sha256':sha(HERE/'CANONICAL_INPUT_PINS.json'),
         'exact_inventory_and_hash_equality':current==baseline,
         'packages':len(current),'files':sum(len(p['files']) for p in current)})
    require(current==baseline,'canonical inventory changed during audit; investigate external state')
    print(json.dumps({'passed':True,'tested':len(result),'commands':len(COMMANDS),
                      'canonical_files':sum(len(p['files']) for p in current),
                      'confirmed_case_alias_contract_failures':[r['pr'] for r in result
                       if all(t['created'] for t in r['tests'])]}))
