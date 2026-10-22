#!/usr/bin/env python3
"""Externally pinned public-only binding and replay; not a theorem prover."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(data):
    return {'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest()}

def safe_name(name):
    require(isinstance(name,str) and bool(name), 'invalid relative path')
    p=PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and p.as_posix()==name and
            '\\' not in name and ':' not in name and '\x00' not in name,
            'unsafe relative path')
    return name

def inventory(root):
    result=set()
    require(root.is_dir() and not root.is_symlink(), 'linked or absent root')
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'symlink forbidden')
        require(p.is_dir() or p.is_file(), 'nonregular file forbidden')
        if p.is_file(): result.add(p.relative_to(root).as_posix())
    return result

def verify(root, expected_manifest_sha256, replay=True):
    require(re.fullmatch('[0-9a-f]{64}',expected_manifest_sha256) is not None,
            'invalid external manifest digest')
    files=inventory(root)
    raw=(root/'PUBLICATION_MANIFEST.json').read_bytes()
    require(digest(raw)['sha256']==expected_manifest_sha256,'external manifest pin mismatch')
    m=json.loads(raw)
    require((m['version'],m['problem_id'],m['rank'],m['status'],m['turns'])==
            ('public-safe-v2',2303023,677,'already_solved','1/5'), 'identity or disposition mismatch')
    require(m['audit_status']=='PASS_DEDUCTION_WITH_DECLARED_EXTERNAL_PREMISE','audit status mismatch')
    names=set()
    for item in m['files']:
        name=safe_name(item['path'])
        require(name not in names,'duplicate manifest path')
        names.add(name)
        require(name in files,'missing file '+name)
        require(digest((root/name).read_bytes())=={k:item[k] for k in ('bytes','sha256')},
                'file digest mismatch '+name)
    require(files==names|{'PUBLICATION_MANIFEST.json'},'exact inventory mismatch')
    require(len(m['archives'])==2,'archive count mismatch')
    archive_counts={}
    archive_by_folder={}
    for archive,meta in m['archives'].items():
        safe_name(archive)
        require('/' not in archive and meta['folder'] in ('author','audit'),'invalid archive mapping')
        folder=meta['folder']
        require(folder not in archive_by_folder,'duplicate archive folder')
        archive_by_folder[folder]=(archive,meta)
        require(digest((root/'archives'/archive).read_bytes())=={k:meta[k] for k in ('bytes','sha256')},'archive digest mismatch')
        with zipfile.ZipFile(root/'archives'/archive) as z:
            members=z.namelist()
            require(len(members)==len(set(members)),'duplicate archive member')
            for info in z.infolist():
                safe_name(info.filename)
                mode=info.external_attr>>16
                require(not info.is_dir() and stat.S_IFMT(mode) in (0,stat.S_IFREG),'archive nonregular member')
                require(not info.flag_bits&1,'encrypted archive member')
            require({folder+'/'+n for n in members}=={n for n in names if n.startswith(folder+'/')},'archive inventory mismatch')
            for name in members:
                require(z.read(name)==(root/folder/name).read_bytes(),'archive member byte mismatch')
            archive_counts[folder]=len(members)
    for folder,manifest in [('author','RECONSTRUCTION_MANIFEST.json'),('author/safe_output','SAFE_OUTPUT_MANIFEST.json'),('audit','SAFE_AUDIT_MANIFEST.json')]:
        binding=json.loads((root/folder/manifest).read_text())
        require(binding['version']=='public-safe-v2' and binding['problem_id']==2303023,'submanifest identity mismatch')
        expected={n.removeprefix(folder+'/') for n in names if n.startswith(folder+'/')}-{manifest}
        require(set(binding['files'])==expected,'submanifest inventory mismatch')
        for name,pin in binding['files'].items():
            require(digest((root/folder/safe_name(name)).read_bytes())==pin,'submanifest file mismatch')
    ar=json.loads((root/'audit/AUDIT_RESULT.json').read_text())
    require(ar['version']=='public-safe-v2' and ar['audit_status']==m['audit_status'] and ar['classification']=='already_solved1','audit verdict mismatch')
    for item in ar['input'].values():
        require(digest((root/safe_name(item['path'])).read_bytes())=={k:item[k] for k in ('bytes','sha256')},'audit input mismatch')
    author_name,_=archive_by_folder['author']
    require(ar['input']['author_archive']['path']=='archives/'+author_name,'audit archive mapping mismatch')
    result={'status':'PASS_PUBLIC_SAFE_V2_INTEGRITY','files':len(files),'archive_members':archive_counts,'externally_pinned_manifest':digest(raw),'all_submanifest_entries_are_actual_public_files':True}
    if replay:
        with tempfile.TemporaryDirectory() as tmp:
            def run(name):
                proc=subprocess.run([sys.executable,'-I',str(root/name)],cwd=tmp,check=True,text=True,capture_output=True)
                return json.loads(proc.stdout)
            author=run('author/verify_arithmetic.py')
            require(author==json.loads((root/'author/CHECK_RESULTS.json').read_text()),'author report mismatch')
            require(author['total_assertions']==16452 and author['sample_threshold_count']==1028,'author counts mismatch')
            independent=run('audit/verify_independent.py')
            expected=json.loads((root/'audit/INDEPENDENT_CHECK_RESULTS.json').read_text())
            require(set(independent)==set(expected),'independent report field mismatch')
            for key in set(expected)-{'dependencies'}:
                require(independent[key]==expected[key],'independent report mismatch '+key)
            require(independent['independent_assertions']==3340 and independent['negative_controls']==7,'independent counts mismatch')
            result.update(author_assertions=16452,author_thresholds=1028,independent_assertions=3340,independent_thresholds=98,mathematical_negative_controls=7,author_report_exact_match=True,independent_report_match_except_runtime_versions=True,dependencies=independent['dependencies'],replay_working_directory='unrelated temporary directory')
    return result

def negative_controls(root,pin):
    passed=[]
    cases={
        'altered_file':'file digest mismatch',
        'missing_file':'missing file',
        'extra_file':'exact inventory mismatch',
        'linked_file':'symlink forbidden',
        'wrong_manifest_identity':'identity or disposition mismatch',
        'rewritten_manifest_without_external_repin':'external manifest pin mismatch',
        'duplicate_archive_member':'duplicate archive member',
        'unsafe_archive_path':'unsafe relative path',
        'linked_archive_member':'archive nonregular member',
        'changed_archive_member':'archive member byte mismatch',
    }
    for label,message in cases.items():
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'packet';shutil.copytree(root,p)
            expected_pin=pin
            m=json.loads((p/'PUBLICATION_MANIFEST.json').read_text())
            if label=='altered_file':
                with (p/'author/PROOF.md').open('ab') as f:f.write(b'\nMUTATION\n')
            elif label=='missing_file':(p/'audit/FULL_AUDIT.md').unlink()
            elif label=='extra_file':(p/'UNLISTED.txt').write_text('unexpected')
            elif label=='linked_file':(p/'UNLISTED_LINK').symlink_to(p/'author/PROOF.md')
            elif label in ('wrong_manifest_identity','rewritten_manifest_without_external_repin'):
                m['problem_id']=0
                (p/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
                if label=='wrong_manifest_identity':expected_pin=digest((p/'PUBLICATION_MANIFEST.json').read_bytes())['sha256']
            else:
                archive=next(n for n,meta in m['archives'].items() if meta['folder']=='author')
                zpath=p/'archives'/archive
                with zipfile.ZipFile(zpath) as z:entries=[(info,z.read(info.filename)) for info in z.infolist()]
                if label=='duplicate_archive_member':entries.append(entries[0])
                elif label=='unsafe_archive_path':entries.append((zipfile.ZipInfo('../outside.txt'),b'negative control'))
                elif label=='linked_archive_member':
                    info=zipfile.ZipInfo('LINK');info.external_attr=(stat.S_IFLNK|0o777)<<16;entries.append((info,b'PROOF.md'))
                elif label=='changed_archive_member':
                    entries=[(info,data+b'\nMUTATION\n' if info.filename=='PROOF.md' else data) for info,data in entries]
                with zipfile.ZipFile(zpath,'w') as z:
                    for info,data in entries:z.writestr(info,data)
                newpin=digest(zpath.read_bytes())
                m['archives'][archive].update(newpin)
                for item in m['files']:
                    if item['path']=='archives/'+archive:item.update(newpin)
                (p/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
                expected_pin=digest((p/'PUBLICATION_MANIFEST.json').read_bytes())['sha256']
            try:verify(p,expected_pin,replay=False)
            except ValueError as exc:
                require(message in str(exc),'negative control failed for unexpected reason: '+label+': '+str(exc))
                passed.append(label)
            else:raise ValueError('negative control accepted: '+label)
    return passed

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected-manifest-sha256',required=True)
    parser.add_argument('--negative-controls',action='store_true')
    args=parser.parse_args()
    result=verify(HERE,args.expected_manifest_sha256)
    if args.negative_controls:result['publication_negative_controls_rejected']=negative_controls(HERE,args.expected_manifest_sha256)
    print(json.dumps(result,indent=2,sort_keys=True))
