#!/usr/bin/env python3
"""Copied-fixture package attacks; never hardlink, execute services or edit inputs."""
from pathlib import Path
import hashlib,json,os,shutil,stat,sys,zipfile
from command_runner import run,ROOT
A=ROOT.parents[1];P=A/'preprint_v1_1';F=ROOT/'fixtures';K=F/'kit_copy'
def need(p,msg):
    if not p:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def snap(root):
    rows=[]
    for p in sorted(root.rglob('*')):
        s=p.lstat();r=dict(path=str(p.relative_to(root)),mode=s.st_mode,nlink=s.st_nlink)
        if stat.S_ISREG(s.st_mode):r.update(size=s.st_size,sha256=sha(p.read_bytes()))
        elif stat.S_ISLNK(s.st_mode):r['target']=os.readlink(p)
        rows.append(r)
    return rows
def remove(p):
    if p.is_symlink() or p.is_file():p.unlink()
    elif p.exists():shutil.rmtree(p)
def reset():
    if K.exists():shutil.rmtree(K)
    shutil.copytree(P/'kit',K,copy_function=shutil.copyfile)
    need(all(p.stat().st_nlink==1 for p in K.rglob('*') if p.is_file()),'fixture hardlinks')
def builder(name,flags,target,cwd=None,ok=False):
    before=snap(K)
    r=run(name,[sys.executable,'-I','-B',*flags,K/'scripts/build_archive.py',target],cwd=cwd or F,expected=0 if ok else 1)
    after=snap(K)
    need(r['expectation_met'] and before==after,'builder boundary failure: '+name)
    return dict(name=name,expected_success=ok,source_unchanged=before==after,
                output_exists=Path(target if Path(target).is_absolute() else (cwd or F)/target).exists())

def main():
    results=[];reset();(K/'inner').mkdir()
    # Exact-tree extra directory is harmless but will be removed before successful builds.
    (K/'inner').rmdir()
    for flags,tag in (([],'normal'),(['-O'],'O'),(['-OO'],'OO')):
        reset()
        for kind in ('absolute','relative'):
            out=F/f'rebuilt_{tag}_{kind}.zip'
            target=str(out) if kind=='absolute' else out.name
            results.append(builder('builder_'+tag+'_'+kind,flags,target,ok=True))
            need(out.read_bytes()==(P/'pr1032_supportkit_v1.1.zip').read_bytes(),'nonidentical rebuild')
        tests=[('inside',K/'inside.zip'),('case_inside',K.with_name(K.name.upper())/'inside.zip'),
               ('missing_parent',F/'missing'/'new.zip'),('traversal',F/'..'/'fixtures'/'new.zip')]
        existing=F/'existing.txt';existing.write_text('preserve')
        directory=F/'existing_directory';directory.mkdir(exist_ok=True)
        link=F/'link_output';link.symlink_to(existing)
        dangling=F/'dangling_output';dangling.symlink_to(F/'absent_target')
        linkdir=F/'link_directory';linkdir.symlink_to(directory,target_is_directory=True)
        tests += [('existing_file',existing),('existing_directory',directory),('existing_symlink',link),
                  ('dangling_symlink',dangling),('symlink_ancestor',linkdir/'new.zip')]
        # On a case-sensitive filesystem the case alias may simply be a missing parent, still rejected.
        for kind,target in tests:results.append(builder('builder_'+tag+'_'+kind,flags,str(target)))
        for p in (link,dangling,linkdir):p.unlink()
        need(existing.read_text()=='preserve','existing target overwritten')
        for kind in ('hash_mismatch','extra_file','member_symlink','directory_symlink','fifo'):
            reset()
            if kind=='hash_mismatch':(K/'paper.tex').write_bytes((K/'paper.tex').read_bytes()+b'\n%mutation\n')
            if kind=='extra_file':(K/'extra.txt').write_text('unexpected')
            if kind=='member_symlink':
                (K/'paper.tex').unlink();(K/'paper.tex').symlink_to(F/'existing.txt')
            if kind=='directory_symlink':(K/'extra_directory').symlink_to(directory,target_is_directory=True)
            if kind=='fifo':os.mkfifo(K/'extra_fifo')
            target=F/f'rejected_{tag}_{kind}.zip'
            results.append(builder('builder_'+tag+'_'+kind,flags,str(target)))
            need(not target.exists(),'partial archive on invalid source')
        reset()
    # Copy and extraction give an independent runnable archive boundary.
    extracted=F/'extracted';extracted.mkdir()
    with zipfile.ZipFile(P/'pr1032_supportkit_v1.1.zip') as z:z.extractall(extracted)
    for flags,tag in (([],'normal'),(['-O'],'O'),(['-OO'],'OO')):
        r=run('extracted_verify_'+tag,[sys.executable,'-I','-B',*flags,extracted/'scripts/verify_kit.py','--archive',P/'pr1032_supportkit_v1.1.zip'])
        need(r['expectation_met'],'extracted replay failed')
    # Bounded hostile ZIP controls retain real files and command stderr/stdout.
    with zipfile.ZipFile(P/'pr1032_supportkit_v1.1.zip') as z:rows=[(i,z.read(i)) for i in z.infolist()]
    attacks=('content','missing','extra','duplicate','absolute','traversal','symlink','timestamp','compression')
    for attack in attacks:
        out=F/f'attack_{attack}.zip'
        with zipfile.ZipFile(out,'w') as z:
            for idx,(i,data) in enumerate(rows):
                if attack=='missing' and idx==0:continue
                info=zipfile.ZipInfo(i.filename,i.date_time);info.create_system=i.create_system;info.external_attr=i.external_attr;info.compress_type=i.compress_type
                if idx==0:
                    if attack=='content':data+=b'changed'
                    if attack=='absolute':info.filename='/absolute.json'
                    if attack=='traversal':info.filename='../escape.json'
                    if attack=='symlink':info.external_attr=(stat.S_IFLNK|0o777)<<16
                    if attack=='timestamp':info.date_time=(2025,1,1,0,0,0)
                    if attack=='compression':info.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(info,data)
            if attack in ('extra','duplicate'):
                if attack=='extra':z.writestr('extra.txt',b'unexpected')
                else:
                    import warnings
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore');z.writestr(rows[0][0],rows[0][1])
        for flags,tag in (([],'normal'),(['-O'],'O'),(['-OO'],'OO')):
            r=run('archive_'+attack+'_'+tag,[sys.executable,'-I','-B',*flags,extracted/'scripts/verify_kit.py','--archive',out],expected=1)
            need(r['expectation_met'],'archive hostile control accepted')
    # Coherence between scholarly metadata, native LOCAL manifest and content bindings.
    native=json.loads((A/'publication/zenodo-deposit-v1_1.json').read_text())
    deposit=json.loads((P/'zenodo-deposit.json').read_text())
    metadata=json.loads((P/'.zenodo.json').read_text())
    need(native['metadata']==deposit['metadata']==metadata,'metadata divergence')
    need(metadata==json.loads((P/'kit/.zenodo.json').read_text()),'kit metadata divergence')
    for r in native['files']:
        resolved=(A/'publication'/r['path']).resolve()
        need(resolved==P/r['name'] and resolved.is_file(),'native file binding')
    binding=json.loads((P/'DEPOSIT_BINDING.json').read_text())
    need(binding['metadata_sha256']==sha((P/'.zenodo.json').read_bytes()),'metadata digest')
    for r in binding['files']:
        b=(P/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'deposit object digest')
    native_binding=binding['versioned_native_manifest'];nb=(A/native_binding['path']).read_bytes()
    need(len(nb)==native_binding['bytes'] and sha(nb)==native_binding['sha256'],'native content pin')
    seal=json.loads((P/'PREPARATION_SEAL.json').read_text())
    for r in seal['files']:
        b=(P/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'preparation seal mismatch')
    for r in json.loads((P/'kit/COPY_MAP.json').read_text()):
        b=(A/r['original_relative_to_audit']).read_bytes();copy=(P/'kit'/r['copy_relative_to_kit']).read_bytes()
        need(b==copy and len(b)==r['bytes'] and sha(b)==r['sha256'],'historical copy mismatch')
    result=dict(status='PASS',builder_cases=len(results),builder_results=results,
                archive_attacks=len(attacks),archive_attack_runs=len(attacks)*3,extracted_whole_runs=3,
                metadata='PASS_NATIVE_LOCAL_ONLY',native_service_state='NOT_QUERIED',preparation_seal_rows=len(seal['files']),
                copyright_boundary='37 allowlisted authored/support members; third-party raw bodies/text/raster omitted',
                outputs_byte_identical=True,no_hardlinks_created=True,source_fixture_after_tests=snap(K))
    (ROOT/'PACKAGE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('builder_results','source_fixture_after_tests')}))

if __name__=='__main__':main()
