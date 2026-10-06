#!/usr/bin/env python3
"""Independent frozen-input audit. Tests bytes/finite diagnostics, not continuum math."""
import hashlib,io,json,pathlib,shutil,stat,subprocess,sys,tempfile,zipfile
PIN='47cf2deb9dc39191fe5a7ff78aa2cef3bf245f4e9e47eae3092583e6735ea5c9'
ZIP_PIN='5bd8726384871fa1f3f97543db1a88d7340d2474287f8e90feb4509a73746523'

def require(c,m):
    if not c: raise ValueError(m)
def digest(b): return hashlib.sha256(b).hexdigest()
def strict_json(b):
    def pairs(xs):
        d={}
        for k,v in xs:
            require(k not in d,'duplicate JSON key')
            d[k]=v
        return d
    return json.loads(b,object_pairs_hook=pairs)
def freeze_gate(zraw,mraw,pin=PIN):
    require(digest(mraw)==pin,'external manifest pin')
    m=strict_json(mraw)
    require(len(zraw)==m['zip']['bytes'] and digest(zraw)==m['zip']['sha256'],'archive bytes')
    with zipfile.ZipFile(io.BytesIO(zraw)) as z:
        infos=z.infolist();names=[i.filename for i in infos]
        require(len(names)==len(set(names)),'duplicate ZIP member')
        require(set(names)==set(m['files']),'ZIP inventory')
        for info in infos:
            require('/' not in info.filename and '\\' not in info.filename,'unsafe ZIP name')
            require(not info.is_dir() and stat.S_IFMT(info.external_attr>>16) != stat.S_IFLNK,'ZIP special node')
            b=z.read(info.filename);e=m['files'][info.filename]
            require(len(b)==e['bytes'] and digest(b)==e['sha256'],'ZIP member bytes')
            if info.filename.endswith('.json'): strict_json(b)
    return m

def run(folder,flags):
    p=subprocess.run([sys.executable,*flags,'-B',str(folder/'verify.py')],cwd=folder.parent,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=40)
    return {'returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip().replace(str(folder.parent),'<relocated>')}
def record(out,name,result,expected):
    require((result['returncode']==0)==(expected=='pass'),name+' unexpected result')
    out.append({'test':name,'expected':expected,**result})
def rebind(folder,name):
    p=folder/'CERTIFICATE.json';d=json.loads(p.read_bytes());b=(folder/name).read_bytes();d['files'][name]={'bytes':len(b),'sha256':digest(b)};p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def packed(folder,override=None):
    bio=io.BytesIO()
    with zipfile.ZipFile(bio,'w') as z:
        for p in sorted(folder.iterdir()): z.writestr(p.name,p.read_bytes())
        if override: override(z)
    return bio.getvalue()

def main():
    root=pathlib.Path(__file__).resolve().parent
    mraw=(root/'AUTHOR_EXTERNAL_MANIFEST.json').read_bytes();zraw=(root/'AUTHOR_SAFE_FREEZE.zip').read_bytes()
    require(len(zraw)==10738 and digest(zraw)==ZIP_PIN,'author archive anchor')
    require(len(mraw)==999,'author external manifest bytes')
    manifest=freeze_gate(zraw,mraw)
    controls=[];extra=[]
    with tempfile.TemporaryDirectory(prefix='sirsn-independent-controls-') as tmp:
        t=pathlib.Path(tmp);src=t/'relocated author package';src.mkdir()
        with zipfile.ZipFile(io.BytesIO(zraw)) as z: z.extractall(src)
        for flags in [[],['-O'],['-I'],['-I','-O']]:
            record(controls,'relocated '+(' '.join(flags) or 'normal'),run(src,flags),'pass')
        mutations={
            'changed_result':lambda p:(p/'RESULT.md').write_bytes((p/'RESULT.md').read_bytes()+b'\n'),
            'missing_readme':lambda p:(p/'README.md').unlink(),
            'extra_file':lambda p:(p/'extra.txt').write_text('test'),
            'nested_manifest':lambda p:((p/'nested').mkdir(),(p/'nested/CERTIFICATE.json').write_text('{}')),
            'empty_directory':lambda p:(p/'newdir').mkdir(),
            'result_symlink':lambda p:((p/'RESULT.md').unlink(),(p/'RESULT.md').symlink_to(src/'RESULT.md')),
            'verifier_symlink':lambda p:((p/'verify.py').unlink(),(p/'verify.py').symlink_to(src/'verify.py')),
            'certificate_id':lambda p:(p/'CERTIFICATE.json').write_text((p/'CERTIFICATE.json').read_text().replace('9700033','9700034')),
        }
        for name,mutate in mutations.items():
            p=t/name;shutil.copytree(src,p);mutate(p)
            for flags in [[],['-O']]: record(controls,name+' '+(' '.join(flags) or 'normal'),run(p,flags),'reject')
        p=t/'coherent';shutil.copytree(src,p);(p/'RESULT.md').write_bytes((p/'RESULT.md').read_bytes()+b'\n');rebind(p,'RESULT.md')
        try: freeze_gate(packed(p),mraw)
        except ValueError: controls.append({'test':'external anchor detects coherent result/certificate rewrite','expected':'reject','status':'PASS'})
        else: raise ValueError('coherent rewrite accepted')
        # Fresh adversarial checks: not claimed as original author controls.
        p=t/'same_size';shutil.copytree(src,p);b=(p/'RESULT.md').read_bytes();(p/'RESULT.md').write_bytes(b.replace(b'SIRSN',b'TIRSN',1))
        for flags in [[],['-O']]: record(extra,'same-size body mutation '+(' '.join(flags) or 'normal'),run(p,flags),'reject')
        p=t/'wrong_pair';shutil.copytree(src,p);f=p/'SOURCE_MANIFEST.json';d=json.loads(f.read_bytes());d['canonical_pair']['sha256']='0'*64;f.write_text(json.dumps(d));rebind(p,f.name)
        for flags in [[],['-O']]: record(extra,'rebound false canonical hash '+(' '.join(flags) or 'normal'),run(p,flags),'reject')
        # This deliberately demonstrates the narrow scope of the original verifier.
        p=t/'unchecked_metadata';shutil.copytree(src,p);f=p/'SOURCE_MANIFEST.json';d=json.loads(f.read_bytes());d['corpora']['problems']['sha256']='0'*64;f.write_text(json.dumps(d));rebind(p,f.name)
        for flags in [[],['-O']]: record(extra,'rebound false corpus metadata internal-only '+(' '.join(flags) or 'normal'),run(p,flags),'pass')
        try: freeze_gate(packed(p),mraw)
        except ValueError: extra.append({'test':'false corpus metadata external anchor','expected':'reject','status':'PASS'})
        else: raise ValueError('false corpus metadata accepted')
        for name,payload in [('duplicate JSON key',b'{"x":1,"x":2}'),('duplicate certificate key',b'{"problem_id":9700033,"problem_id":9700034}')]:
            try: strict_json(payload)
            except ValueError: extra.append({'test':name,'expected':'reject','status':'PASS'})
            else: raise ValueError(name+' accepted')
        # Construct untrusted archives and pin their outer manifests locally to test structural gates independently.
        for name,add in [('path traversal',lambda z:z.writestr('../escape','x')),('duplicate member',lambda z:z.writestr('RESULT.md','x')),('ZIP symlink',None)]:
            if add: zr=packed(src,add)
            else:
                bio=io.BytesIO()
                with zipfile.ZipFile(bio,'w') as z:
                    for f in sorted(src.iterdir()):
                        i=zipfile.ZipInfo(f.name)
                        if f.name=='RESULT.md':i.create_system=3;i.external_attr=(stat.S_IFLNK|0o777)<<16
                        z.writestr(i,f.read_bytes())
                zr=bio.getvalue()
            mm=json.loads(mraw);mm['zip']={'bytes':len(zr),'sha256':digest(zr)}
            if name=='path traversal': mm['files']['../escape']={'bytes':1,'sha256':digest(b'x')}
            mr=json.dumps(mm).encode()
            try:freeze_gate(zr,mr,digest(mr))
            except ValueError:extra.append({'test':name,'expected':'reject','status':'PASS'})
            else:raise ValueError(name+' accepted')
        # Exact patch application must reproduce all corrected bytes.
        p=t/'patched';shutil.copytree(src,p)
        proc=subprocess.run(['patch','-p1','--batch','--forward','-i',str(root/'MEASURABILITY_CORRECTION.patch')],cwd=p,capture_output=True,text=True)
        require(proc.returncode==0,'patch apply')
        require({x.name:x.read_bytes() for x in p.iterdir()}=={x.name:x.read_bytes() for x in (root/'corrected').iterdir()},'patch output differs from derivative')
        extra.append({'test':'patch reproduces exact corrected derivative','status':'PASS'})
        for flags in [[],['-O'],['-I'],['-I','-O']]:record(extra,'corrected relocation '+(' '.join(flags) or 'normal'),run(p,flags),'pass')
    require(len(controls)==21,'author control count')
    output={'status':'PASS','problem_id':9700033,'author_control_count':len(controls),'independent_control_count':len(extra),'author_controls':controls,'independent_controls':extra,'warning':'The original verifier can accept coherently rebound false corpus metadata; the frozen external pin rejects such changes, and corpus bytes were independently recomputed. Finite tests do not certify the mathematical theorem.'}
    print(json.dumps(output,indent=2,sort_keys=True))
if __name__=='__main__':main()
