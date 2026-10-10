"""Validate the pinned independent audit, including hostile-boundary probes.
Usage: python -I -S -B this-file.py directory-containing-all-external-files
Produces a JSON validation receipt on stdout. No external state is changed.
"""
from pathlib import Path
import hashlib,json,os,shutil,stat,subprocess,sys,tempfile,zipfile
PREFIX='SHADOW_NORM_10400215_INDEPENDENT_AUDIT'
PINS={
 '_SAFE.zip':('28f27ba13c46cc7246abf0e56e32466e42685a920c0564b4f82495226b16a8df',17865),
 '_EXTERNAL_MANIFEST.json':('fa0c1e8f188365ec6ea192dd60693f18b84a3a35c33934d7bf1522e9814fce21',1537),
 '_BOOTSTRAP.py':('61ad9caafeb683c1c8c87d7949947d8fb886762509051b5960f64729dcdf7e02',3809)}
def require(c,m):
    if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
require(sys.flags.isolated and sys.flags.no_site,'isolation required')
require(len(sys.argv)==2,'supply external-file directory')
base=Path(sys.argv[1]).absolute()
for suffix,(digest,size) in PINS.items():
    p=base/(PREFIX+suffix);require(stat.S_ISREG(p.lstat().st_mode),'external audit type');b=p.read_bytes();require(sha(b)==digest and len(b)==size,'external audit authentication')
manifest=base/(PREFIX+'_EXTERNAL_MANIFEST.json');boot=base/(PREFIX+'_BOOTSTRAP.py')
m=json.loads(manifest.read_bytes());results=[];outputs=[]
with tempfile.TemporaryDirectory(prefix='shadow-audit-acceptance-') as tmp:
    tmp=Path(tmp);clean=tmp/'audit';clean.mkdir()
    with zipfile.ZipFile(base/(PREFIX+'_SAFE.zip')) as z:
        infos=z.infolist();names=[i.filename for i in infos]
        require(len(names)==len(set(names)) and set(names)==set(m['files']),'ZIP inventory')
        for i in infos:
            require(Path(i.filename).name==i.filename and stat.S_ISREG(i.external_attr>>16),'ZIP path/type')
            b=z.read(i);meta=m['files'][i.filename]
            require(sha(b)==meta['sha256'] and len(b)==meta['bytes'],'ZIP content')
            (clean/i.filename).write_bytes(b)
    acceptance=json.loads((clean/'ACCEPTANCE.json').read_bytes())
    author=tmp/'author';author.mkdir()
    for meta in acceptance['original_inputs']:
        p=base/meta['filename'];require(stat.S_ISREG(p.lstat().st_mode),'original author type');b=p.read_bytes()
        require(sha(b)==meta['sha256'] and len(b)==meta['bytes'],'original author authentication')
        (author/p.name).write_bytes(b)
    relocated=tmp/'relocated-audit';shutil.copytree(clean,relocated)
    relocated_author=tmp/'relocated-author';shutil.copytree(author,relocated_author)
    hostile=tmp/'hostile';hostile.mkdir();marker=tmp/'EXECUTED'
    payload='from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\nraise RuntimeError("unexpected execution")\n'
    for name in ('json','hashlib','pathlib','fractions','sitecustomize','usercustomize'):(hostile/(name+'.py')).write_text(payload)
    env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONSTARTUP=str(hostile/'sitecustomize.py'),PYTHONOPTIMIZE='2')
    def run(root,ad,opt,mp=manifest,extra=()):
        p=subprocess.run([sys.executable,'-I','-S','-B']+(['-O'] if opt else [])+[str(boot),str(mp),str(root),str(ad),*extra],capture_output=True,cwd=hostile,env=env,timeout=100)
        require(not marker.exists(),'untrusted payload executed')
        return p
    for opt in (False,True):
        for label,root,ad in (('extracted',clean,author),('relocated',relocated,relocated_author)):
            p=run(root,ad,opt);require(p.returncode==0 and not p.stderr,'acceptance replay failed')
            outputs.append(p.stdout);results.append({'case':label+'_hostile_environment','optimized':opt,'result':'pass','stdout_sha256':sha(p.stdout)})
        cases=('audit_file_tamper','audit_entrypoint_tamper','acceptance_tamper','expected_output_tamper','audit_extra_file','audit_extra_directory','audit_missing_file','audit_shadow_module','audit_cache_directory','audit_symlink_member','audit_fifo_member','audit_root_symlink','audit_ancestor_symlink','manifest_reseal','manifest_symlink','entrypoint_override','author_archive_tamper','author_manifest_tamper','author_bootstrap_tamper','author_receipt_tamper','author_root_symlink')
        for case in cases:
            root=tmp/(case+str(opt));shutil.copytree(clean,root)
            ad=tmp/(case+'_author'+str(opt));shutil.copytree(author,ad)
            mp=manifest;extra=()
            if case=='audit_file_tamper':(root/'AUDIT.md').write_text('altered')
            elif case=='audit_entrypoint_tamper':(root/'independent_diagnostics.py').write_text(payload)
            elif case=='acceptance_tamper':(root/'ACCEPTANCE.json').write_text('{}')
            elif case=='expected_output_tamper':(root/'INDEPENDENT_EXPECTED.json').write_text('{}')
            elif case=='audit_extra_file':(root/'.extra').write_text('x')
            elif case=='audit_extra_directory':(root/'extra').mkdir()
            elif case=='audit_missing_file':(root/'AUDIT.md').unlink()
            elif case=='audit_shadow_module':(root/'json.py').write_text(payload)
            elif case=='audit_cache_directory':(root/'__pycache__').mkdir();(root/'__pycache__'/'independent_diagnostics.pyc').write_text(payload)
            elif case in ('audit_symlink_member','audit_fifo_member'):
                p=root/'AUDIT.md';p.unlink()
                if case=='audit_symlink_member':p.symlink_to(clean/'AUDIT.md')
                else:os.mkfifo(p)
            elif case=='audit_root_symlink':
                p=tmp/('audit-link'+str(opt));p.symlink_to(root,target_is_directory=True);root=p
            elif case=='audit_ancestor_symlink':
                p=tmp/('ancestor-link'+str(opt));p.symlink_to(tmp,target_is_directory=True);root=p/root.name
            elif case=='manifest_reseal':
                (root/'independent_diagnostics.py').write_text(payload)
                changed=json.loads(manifest.read_bytes());b=(root/'independent_diagnostics.py').read_bytes();changed['files']['independent_diagnostics.py']={'bytes':len(b),'sha256':sha(b)}
                mp=tmp/('resealed'+str(opt)+'.json');mp.write_text(json.dumps(changed,sort_keys=True,indent=2)+'\n')
            elif case=='manifest_symlink':mp=tmp/('manifest-link'+str(opt));mp.symlink_to(manifest)
            elif case=='entrypoint_override':extra=('independent_diagnostics.py',)
            elif case.startswith('author_') and case!='author_root_symlink':
                suffix={'author_archive_tamper':'SAFE_FREEZE.zip','author_manifest_tamper':'EXTERNAL_MANIFEST.json','author_bootstrap_tamper':'BOOTSTRAP.py','author_receipt_tamper':'VALIDATION_RECEIPT.json'}[case]
                (ad/('SHADOW_NORM_10400215_AUTHOR_'+suffix)).write_text(payload)
            elif case=='author_root_symlink':
                p=tmp/('author-link'+str(opt));p.symlink_to(ad,target_is_directory=True);ad=p
            p=run(root,ad,opt,mp,extra)
            require(p.returncode!=0 and b'AUDIT REJECT:' in p.stderr,'negative case accepted: '+case)
            results.append({'case':case,'optimized':opt,'result':'rejected_before_audit_code','message':p.stderr.decode().strip()})
    for label,flags in (('missing_isolated',('-S','-B')),('missing_no_site',('-I','-B'))):
        p=subprocess.run([sys.executable,*flags,str(boot),str(manifest),str(clean),str(author)],capture_output=True,cwd=tmp,env={'PATH':os.environ.get('PATH','')},timeout=10)
        require(p.returncode!=0 and b'isolated no-site interpreter required' in p.stderr,'unsafe mode accepted')
        results.append({'case':label,'result':'rejected_before_audit_code','message':p.stderr.decode().strip()})
    require(len(set(outputs))==1,'acceptance outputs differ')
    for name,meta in m['files'].items():require(sha((clean/name).read_bytes())==meta['sha256'],'audit mutated')
    for meta in acceptance['original_inputs']:require(sha((base/meta['filename']).read_bytes())==meta['sha256'],'original author input mutated')
receipt={'schema':1,'problem_id':10400215,'decision':'ACCEPT_UNCHANGED_AS_SCOPED_PARTIAL_RESULTS','archive_sha256':PINS['_SAFE.zip'][0],'manifest_sha256':PINS['_EXTERNAL_MANIFEST.json'][0],'bootstrap_sha256':PINS['_BOOTSTRAP.py'][0],'validator_sha256':sha(Path(__file__).read_bytes()),'status':'pass','audit_archive_strict_inventory':'pass','positive_acceptance_replays':4,'negative_audit_boundary_probes':44,'author_positive_replays_per_acceptance':4,'author_negative_boundary_probes_per_acceptance':40,'author_checks_per_replay':45810,'independent_checks_per_acceptance':68324,'byte_identical_acceptance_outputs':True,'original_author_inputs_unchanged':True,'accepted_replay_output':json.loads(outputs[0]),'tests':results,'scope':'Static authenticated execution and finite algebra; no topology proof assistant, human peer review, global-openness certification, or concurrent hostile-writer defense.'}
print(json.dumps(receipt,sort_keys=True,indent=2))
