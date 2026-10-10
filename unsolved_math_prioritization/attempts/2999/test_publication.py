#!/usr/bin/env python3
"""Synthetic adversarial tests; use a trusted, previously authenticated checkout."""
import hashlib,json,pathlib,shutil,subprocess,sys,tempfile
SOURCE=pathlib.Path(sys.argv[1]).absolute() if len(sys.argv)>1 else pathlib.Path(__file__).absolute().parent
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def rebind(root):
    m=json.loads((root/'PUBLICATION_MANIFEST.json').read_bytes())
    for e in m['files']:
        b=(root/e['path']).read_bytes();e.update(bytes=len(b),sha256=sha(b))
    (root/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m));return sha((root/'PUBLICATION_MANIFEST.json').read_bytes())
def call(root,opt=False,anchor=None,flags=True):
    anchor=anchor or sha((root/'PUBLICATION_MANIFEST.json').read_bytes())
    return subprocess.run([sys.executable]+(['-I','-S','-B'] if flags else [])+(['-O'] if opt else [])+[str(root/'verify_publication.py'),'--expected-manifest',anchor],cwd=tempfile.gettempdir(),capture_output=True,timeout=180)
results=[]
with tempfile.TemporaryDirectory(prefix='taut publication controls ') as td:
    td=pathlib.Path(td);clean=td/'relocated clean';shutil.copytree(SOURCE,clean)
    for opt in [False,True]:
        r=call(clean,opt);need(r.returncode==0 and not r.stderr,r.stderr.decode());results.append({'case':'relocated_positive','optimized':opt,'result':json.loads(r.stdout)})
    cases=['changed_proof','missing_file','extra_file','symlink_member','extra_directory','wrong_anchor','duplicate_manifest_key','duplicate_manifest_entry','traversal_manifest','rebound_solved_claim','rebound_s2_claim','rebound_acceptance','rebound_zip','rebound_second_review','changed_child_code','missing_interpreter_flags','symlink_root','rebound_extracted_proof']
    for case in cases:
        root=td/case;shutil.copytree(SOURCE,root);anchor=sha((root/'PUBLICATION_MANIFEST.json').read_bytes())
        if case in ['changed_proof','rebound_extracted_proof']:
            f=root/'corrected/PROOF.md';f.write_bytes(f.read_bytes()+b'\n')
            if case.startswith('rebound'):anchor=rebind(root)
        elif case=='missing_file':(root/'README.md').unlink()
        elif case=='extra_file':(root/'EXTRA').write_text('fixture')
        elif case=='extra_directory':(root/'extra directory').mkdir()
        elif case=='symlink_member':(root/'README.md').unlink();(root/'README.md').symlink_to(SOURCE/'README.md')
        elif case=='wrong_anchor':anchor='0'*64
        elif case=='duplicate_manifest_key':
            f=root/'PUBLICATION_MANIFEST.json';f.write_bytes(f.read_bytes().replace(b'"schema":',b'"schema":"fixture","schema":',1));anchor=sha(f.read_bytes())
        elif case in ['duplicate_manifest_entry','traversal_manifest']:
            f=root/'PUBLICATION_MANIFEST.json';m=json.loads(f.read_bytes())
            if case=='duplicate_manifest_entry':m['files'].append(m['files'][0])
            else:m['files'][0]['path']='../outside'
            f.write_text(json.dumps(m));anchor=sha(f.read_bytes())
        elif case in ['rebound_solved_claim','rebound_s2_claim']:
            f=root/'PUBLICATION_METADATA.json';s=json.loads(f.read_bytes());s['full_original_resolution' if case=='rebound_solved_claim' else 'S2_times_S2_subquestion']=True;f.write_text(json.dumps(s));anchor=rebind(root)
        elif case=='rebound_acceptance':
            f=root/'audit/EXACT_ACCEPTANCE.json';s=json.loads(f.read_bytes());s['full_original_resolution']=True;f.write_text(json.dumps(s));anchor=rebind(root)
        elif case=='rebound_zip':
            f=root/'AUDIT_SAFE.zip';f.write_bytes(f.read_bytes()+b'fixture');anchor=rebind(root)
        elif case=='rebound_second_review':
            f=root/'second_review/INDEPENDENT_MATHEMATICAL_SOURCE_REVIEW.md';f.write_bytes(f.read_bytes()+b'\n');anchor=rebind(root)
        elif case=='changed_child_code':(root/'corrected/check.py').write_text('raise RuntimeError("untrusted child executed")')
        elif case=='symlink_root':
            actual=root;root=td/'linked root';root.symlink_to(actual,target_is_directory=True)
        for opt in [False,True]:
            r=call(root,opt,anchor,case!='missing_interpreter_flags');need(r.returncode!=0,case+' accepted mutation');need(b'untrusted child executed' not in r.stderr,'untrusted child code executed');results.append({'case':case,'optimized':opt,'result':'rejected','reason':r.stderr.decode().strip()})
    mutations={'id':2998,'turns_used':3,'literal_weak_formulation':'solved','original_closed_formulation':'solved','novelty_claim':True,'status':'solved','s2_times_s2_subquestion':'solved','recommended_queue_status':'solved'}
    for key,value in mutations.items():
        root=td/('scope '+key);shutil.copytree(SOURCE/'corrected',root);s=json.loads((root/'STATUS.json').read_bytes());s[key]=value;(root/'STATUS.json').write_text(json.dumps(s))
        for opt in [False,True]:
            r=subprocess.run([sys.executable,'-I','-S','-B']+(['-O'] if opt else [])+[str(root/'check.py'),'--self-test'],cwd=td,capture_output=True,timeout=30)
            need(r.returncode!=0,'checker accepted overclaim '+key);results.append({'case':'corrected_scope_'+key,'optimized':opt,'result':'rejected','reason':r.stderr.decode().strip()})
print(json.dumps({'result':'pass','publication_manifest_sha256':sha((SOURCE/'PUBLICATION_MANIFEST.json').read_bytes()),'relocation_positive_runs':2,'wrapper_negative_families':len(cases),'wrapper_negative_rejections':2*len(cases),'corrected_scope_negative_rejections':2*len(mutations),'results':results},indent=2))
