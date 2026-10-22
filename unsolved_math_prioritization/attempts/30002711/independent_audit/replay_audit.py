#!/usr/bin/env python3
"""Bind and adversarially replay a frozen author packet without changing it."""
import argparse, hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile, zipfile
PIN='362a6ed1502b421e00efab914b4f02d125e7788a906f7273cb25cf074a83f177'
ZIP_PIN='ae4193f1e0c8a555b5d46ec59ae3aacea615a2536d578eaf4aa9a97e0a5ee9c0'
ZIP_SIZE=20745
FILES={'EXACT_RESULTS.json','PRIOR_ATTEMPT_CHECK.md','README.md','RESEARCH_LOG.md','RESULTS.md','SOURCE_VERIFICATION.json','STATUS.json','verify_math.py','verify_package.py'}
def digest(b): return hashlib.sha256(b).hexdigest()
def require(c,m):
    if not c: raise ValueError(m)
def bind(root,pin=PIN):
    require(root.is_dir(),'not a directory')
    require({p.name for p in root.iterdir()}==FILES|{'MANIFEST.json'},'exact inventory mismatch')
    manifest=root/'MANIFEST.json'
    require(manifest.is_file() and not manifest.is_symlink(),'manifest is not a regular unlinked file')
    mb=manifest.read_bytes()
    require(digest(mb)==pin,'external manifest pin mismatch')
    m=json.loads(mb)
    require(set(m)=={'files','schema'} and m['schema']=='cyclic-lifts-author-freeze-v1','manifest schema mismatch')
    require(set(m['files'])==FILES,'manifest membership mismatch')
    for name,v in m['files'].items():
        p=root/name
        require(p.is_file() and not p.is_symlink(),'payload is not a regular unlinked file')
        b=p.read_bytes()
        require(set(v)=={'bytes','sha256'} and type(v['bytes']) is int,'entry schema mismatch')
        require(len(b)==v['bytes'] and digest(b)==v['sha256'],'payload bytes mismatch')
    return m,mb

def bind_zip(path,root):
    b=path.read_bytes()
    require(len(b)==ZIP_SIZE and digest(b)==ZIP_PIN,'archive pin or byte-count mismatch')
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        require(len(names)==len(set(names))==10 and set(names)==FILES|{'MANIFEST.json'},'archive inventory mismatch')
        for info in z.infolist():
            require(not info.is_dir() and not (info.flag_bits & 1),'unexpected directory or encrypted member')
            require((info.external_attr >> 16) & 0o170000 != 0o120000,'archive symlink member')
            require(z.read(info.filename)==(root/info.filename).read_bytes(),'archive member differs from frozen directory')
        require(z.testzip() is None,'archive CRC failure')
    return {'sha256':digest(b),'bytes':len(b),'members':sorted(names),'all_members_byte_identical':True}

def run(root,optimized=False):
    cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(root/'verify_package.py'),'--expected-manifest',PIN,'--self-test']
    p=subprocess.run(cmd,cwd=root.parent,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    require(p.returncode==0,'author wrapper failed')
    r=json.loads(p.stdout)
    require(r['mathematical_checks_per_replay']==6527 and r['integrity_negative_controls']==6,'unexpected replay count')
    return p.stdout

def main(root):
    before,mb=bind(root)
    archive=bind_zip(root.parent/'AUTHOR_PACKET.zip',root)
    normal=run(root); optimized=run(root,True)
    require(normal==optimized,'author optimized output differs')
    with tempfile.TemporaryDirectory(prefix='cyclic-audit-relocation-') as td:
        relocated=pathlib.Path(td)/'arbitrary-name'/'publication'
        relocated.parent.mkdir();shutil.copytree(root,relocated)
        r1=run(relocated);r2=run(relocated,True)
        require(normal==r1==r2,'relocated output differs')
    negatives=[]
    def reject(name,mutator,pin=PIN):
        with tempfile.TemporaryDirectory(prefix='cyclic-audit-negative-') as td:
            dest=pathlib.Path(td)/'publication';shutil.copytree(root,dest)
            mutator(dest)
            try: bind(dest,pin)
            except (ValueError,OSError,json.JSONDecodeError): independent=True
            else: raise ValueError('independent guard accepted '+name)
            p=subprocess.run([sys.executable,'-B','-O',str(dest/'verify_package.py'),'--expected-manifest',pin],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            require(p.returncode!=0,'author guard accepted '+name)
            negatives.append({'case':name,'independent_guard_rejected':independent,'author_optimized_guard_rejected':True})
    def change(p):
        f=p/'RESULTS.md';b=f.read_bytes();f.write_bytes(b[:-1]+bytes([b[-1]^1]))
    def rewrite_manifest(p):
        change(p);f=p/'MANIFEST.json';m=json.loads(f.read_text());b=(p/'RESULTS.md').read_bytes();m['files']['RESULTS.md']={'sha256':digest(b),'bytes':len(b)};f.write_text(json.dumps(m))
    def sym(p):
        f=p/'README.md';f.unlink();f.symlink_to(p/'STATUS.json')
    def manifest_sym(p):
        f=p/'MANIFEST.json';s=p.parent/'manifest-copy.json';s.write_bytes(f.read_bytes());f.unlink();f.symlink_to(s)
    reject('same_length_payload_byte_flip',change)
    reject('missing_payload',lambda p:(p/'STATUS.json').unlink())
    reject('extra_regular_file',lambda p:(p/'unexpected.txt').write_text('extra'))
    reject('manifest_whitespace_change',lambda p:(p/'MANIFEST.json').write_bytes((p/'MANIFEST.json').read_bytes()+b' '))
    reject('payload_symlink',sym)
    reject('wrong_external_pin',lambda p:None,'0'*64)
    reject('self_consistent_payload_and_manifest_rewrite',rewrite_manifest)
    reject('missing_manifest',lambda p:(p/'MANIFEST.json').unlink())
    reject('manifest_symlink',manifest_sym)
    reject('extra_subdirectory',lambda p:(p/'unexpected').mkdir())
    reject('renamed_payload',lambda p:(p/'README.md').rename(p/'RENAMED.md'))
    # These checks do not execute code from the changed archives.
    with tempfile.TemporaryDirectory(prefix='cyclic-audit-archive-') as td:
        a=pathlib.Path(td)/'changed.zip';a.write_bytes((root.parent/'AUTHOR_PACKET.zip').read_bytes()+b'x')
        try: bind_zip(a,root)
        except ValueError: negatives.append({'case':'archive_appended_byte','independent_guard_rejected':True,'author_optimized_guard_rejected':None})
        else: raise ValueError('changed archive accepted')
    controls=pathlib.Path(__file__).with_name('independent_controls.py')
    outputs=[]
    for opt in (False,True):
        r=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(controls)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        require(r.returncode==0,'independent controls failed')
        outputs.append(r.stdout)
    require(outputs[0]==outputs[1],'independent controls optimized output differs')
    results=controls.with_name('INDEPENDENT_RESULTS.json')
    require(outputs[0]==results.read_bytes(),'independent retained output differs')
    after,ma=bind(root)
    require(before==after and mb==ma,'original freeze changed')
    bind_zip(root.parent/'AUTHOR_PACKET.zip',root)
    return {'schema':'cyclic-lifts-audit-replay-v1','author_manifest_sha256':PIN,'payload_files':len(FILES),'archive':archive,'author_wrapper_runs':4,'mathematical_replays_inside_author_wrappers':8,'author_checks_per_mathematical_replay':6527,'author_wrapper_output_sha256':digest(normal),'author_normal_optimized_relocated_byte_identical':True,'author_self_test_corruptions_per_wrapper':6,'independent_adversarial_cases':negatives,'independent_normal_optimized_byte_identical':True,'independent_checks_per_run':json.loads(outputs[0])['total_checks'],'independent_output_sha256':digest(outputs[0]),'originals_rechecked_unchanged':True,'remote_writes_performed':False}
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('publication',type=pathlib.Path);args=a.parse_args()
    print(json.dumps(main(args.publication.resolve()),indent=2,sort_keys=True))
