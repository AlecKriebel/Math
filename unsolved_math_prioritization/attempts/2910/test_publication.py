import hashlib,json,pathlib,shutil,subprocess,sys,tempfile,zipfile,datetime
SOURCE=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent
OUT=pathlib.Path(tempfile.gettempdir())
def need(ok,message):
    if not ok:raise ValueError(message)
def writable(root):
    for f in root.rglob('*'):
        if f.is_file() and not f.is_symlink():f.chmod(0o600)
def sha(b):return hashlib.sha256(b).hexdigest()
def rebind(root):
    m=json.loads((root/'PUBLICATION_MANIFEST.json').read_bytes())
    for e in m['files']:
        b=(root/e['path']).read_bytes();e.update(bytes=len(b),sha256=sha(b))
    (root/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
def call(root,opt=False,anchor=None,flags=True):
    anchor=anchor or sha((root/'PUBLICATION_MANIFEST.json').read_bytes())
    return subprocess.run([sys.executable]+(['-I','-S','-B'] if flags else [])+(['-O'] if opt else [])+[str(root/'verify_publication.py'),'--expected-manifest',anchor],cwd=OUT,capture_output=True,timeout=600)
results=[]
with tempfile.TemporaryDirectory(prefix='torus publication adversarial ') as td:
    td=pathlib.Path(td)
    clean=td/'relocated clean';shutil.copytree(SOURCE,clean)
    for opt in [False,True]:
        r=call(clean,opt);need(r.returncode==0 and not r.stderr,r.stderr.decode())
        results.append({'case':'relocated_positive','optimized':opt,'result':json.loads(r.stdout)})
    cases=['changed_proof','missing_file','extra_file','symlink_member','extra_directory','wrong_anchor','duplicate_manifest_key','traversal_manifest','rebound_solved_claim','rebound_acceptance','rebound_zip','changed_child_code','missing_interpreter_flags','symlink_root']
    for case in cases:
        root=td/case;shutil.copytree(SOURCE,root);writable(root);anchor=sha((root/'PUBLICATION_MANIFEST.json').read_bytes())
        if case=='changed_proof':(root/'clarified/PROOF.md').write_bytes((root/'clarified/PROOF.md').read_bytes()+b'\n')
        elif case=='missing_file':(root/'README.md').unlink()
        elif case=='extra_file':(root/'EXTRA').write_text('fixture')
        elif case=='extra_directory':(root/'empty directory').mkdir()
        elif case=='symlink_member':(root/'README.md').unlink();(root/'README.md').symlink_to(SOURCE/'README.md')
        elif case=='wrong_anchor':anchor='0'*64
        elif case=='duplicate_manifest_key':
            f=root/'PUBLICATION_MANIFEST.json';f.write_bytes(f.read_bytes().replace(b'"schema":',b'"schema":"fixture","schema":',1));anchor=sha(f.read_bytes())
        elif case=='traversal_manifest':
            f=root/'PUBLICATION_MANIFEST.json';m=json.loads(f.read_bytes());m['files'][0]['path']='../outside';f.write_text(json.dumps(m));anchor=sha(f.read_bytes())
        elif case=='rebound_solved_claim':
            f=root/'PUBLICATION_METADATA.json';s=json.loads(f.read_bytes());s['full_problem_solved']=True;f.write_text(json.dumps(s));rebind(root);anchor=sha((root/'PUBLICATION_MANIFEST.json').read_bytes())
        elif case=='rebound_acceptance':
            f=root/'audit/ACCEPTANCE.json';s=json.loads(f.read_bytes());s['full_problem_solved']=True;f.write_text(json.dumps(s));rebind(root);anchor=sha((root/'PUBLICATION_MANIFEST.json').read_bytes())
        elif case=='rebound_zip':
            f=root/'AUDIT_SAFE.zip';f.write_bytes(f.read_bytes()+b'fixture');rebind(root);anchor=sha((root/'PUBLICATION_MANIFEST.json').read_bytes())
        elif case=='changed_child_code':(root/'audit/replay.py').write_text('raise RuntimeError("untrusted child code executed")')
        elif case=='symlink_root':
            actual=root;root=td/'linked root';root.symlink_to(actual,target_is_directory=True)
        for opt in [False,True]:
            r=call(root,opt,anchor,case!='missing_interpreter_flags');need(r.returncode!=0,case+' accepted mutation')
            need(b'untrusted child code executed' not in r.stderr,'untrusted child code executed')
            results.append({'case':case,'optimized':opt,'result':'rejected','reason':r.stderr.decode().strip()})
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'pass','publication_manifest_sha256':sha((SOURCE/'PUBLICATION_MANIFEST.json').read_bytes()),'relocation_positive_runs':2,'negative_families':len(cases),'negative_rejections':len(cases)*2,'results':results}
print(json.dumps(receipt,indent=2))
