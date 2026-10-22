#!/usr/bin/env python3
"""Independent manifest adversarial tests use only disposable synthetic packets."""
import hashlib,json,pathlib,subprocess,sys,tempfile
checker=pathlib.Path(__file__).resolve().parent/'verify_packet.py'
records=[]
with tempfile.TemporaryDirectory(prefix='seshadri_audit_controls_') as temp:
    base=pathlib.Path(temp)
    def trial(name,mutate,good=False):
        root=base/name;root.mkdir();(root/'file.txt').write_bytes(b'example\n')
        m={'files':[{'path':'file.txt','bytes':8,'sha256':hashlib.sha256(b'example\n').hexdigest()}]}
        mutate(root,m);(root/'MANIFEST.json').write_text(json.dumps(m))
        p=subprocess.run([sys.executable,str(checker),str(root)],capture_output=True)
        if (p.returncode==0)!=good:raise AssertionError(name)
        records.append({'name':name,'expected':'accept' if good else 'reject','observed':'accept' if p.returncode==0 else 'reject'})
    trial('valid',lambda p,m:None,True)
    trial('wrong_byte',lambda p,m:(p/'file.txt').write_bytes(b'Example\n'))
    trial('missing',lambda p,m:(p/'file.txt').unlink())
    trial('extra',lambda p,m:(p/'unexpected.pdf').write_bytes(b'not allowed'))
    trial('duplicate',lambda p,m:m['files'].append(dict(m['files'][0])))
    trial('traversal',lambda p,m:m['files'][0].update(path='../file.txt'))
    trial('absolute',lambda p,m:m['files'][0].update(path='/file.txt'))
    trial('backslash',lambda p,m:m['files'][0].update(path='a\\b'))
    trial('nonnormalized',lambda p,m:m['files'][0].update(path='./file.txt'))
    trial('self_manifest',lambda p,m:m['files'][0].update(path='MANIFEST.json'))
    trial('bad_hash',lambda p,m:m['files'][0].update(sha256='x'*64))
    trial('bad_size',lambda p,m:m['files'][0].update(bytes=True))
    def sym(p,m):
        (p/'file.txt').unlink();(p/'file.txt').symlink_to(p/'missing.txt')
    trial('symlink',sym)
    def nested(p,m):
        (p/'nested').mkdir();(p/'nested/MANIFEST.json').write_text('{}')
    trial('nested_manifest',nested)
print(json.dumps({'status':'PASS','controls':records},indent=2,sort_keys=True))
