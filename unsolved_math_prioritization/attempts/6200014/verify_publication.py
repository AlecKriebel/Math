#!/usr/bin/env python3
"""Verify immutable packets, exact publication inventory, and bounded replay."""
import argparse,hashlib,json,os,pathlib,shutil,stat,subprocess,sys,tempfile,zipfile
sys.dont_write_bytecode=True
AUTHOR=('kleinian_boundary_6200014_author_frozen.zip',14171,'a7085468b08f93b8422c2764799a0712b806e2772292cbafe5514b38851fb5b9','a06410f384f30791a067a97d639b0ec73eaf7df75334fcc4dd0cb896987b9b61')
AUDIT=('kleinian_boundary_6200014_independent_audit.zip',17965,'60646b6f169f6dead89e291c00b2aeaae1279082963535b28ca92b0c8ab4da50','e2bcf03e1c5c311f7e30a7cad657633e06dd8336f70c74c79fb76c6361fea914')
AUTHOR_FILES={'APPROACHES.md','IDENTITY.json','MANIFEST.json','PROOF.md','README.md','SOURCES.json','code/checks.py','results/checks.json','verify.py'}
AUDIT_FILES={'AUDIT_REPORT.md','IDENTITY_AUDIT.json','MANIFEST.json','README.md','REPOSITORY_AUDIT.json','SOURCE_AUDIT.json','code/audit_checks.py','code/check_identity.py','corrections/BIBLIOGRAPHY_ADDENDUM.md','results/author_replay.json','results/finite_controls.json','verify.py'}
ROOT_FILES={'README.md','RESULT.json','QUEUE_DELTA.json','REPOSITORY_RECHECK.json','RESEARCH_LOG.md','verify_publication.py','PUBLICATION_MANIFEST.json'}
ALL_FILES=ROOT_FILES|{'author/'+n for n in AUTHOR_FILES}|{'audit/'+n for n in AUDIT_FILES}|{'frozen_archives/'+x[0] for x in [AUTHOR,AUDIT]}
ALL_DIRS={'author','author/code','author/results','audit','audit/code','audit/results','audit/corrections','frozen_archives'}
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def meta(b):return {'bytes':len(b),'sha256':sha(b)}
def unique(pairs):
    out={}
    for k,v in pairs:need(k not in out,'Duplicate JSON key: '+k);out[k]=v
    return out
def read(p):return json.loads(p.read_bytes(),object_pairs_hook=unique)
def secure_root(root):
    root=pathlib.Path(os.path.abspath(root))
    for p in [root,*root.parents]:need(not p.is_symlink(),'Package or ancestor symlink forbidden')
    need(root.is_dir(),'Package root missing')
    return root
def inventory(root):
    root=secure_root(root);files=set();dirs=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'Symlink forbidden');mode=p.lstat().st_mode
        name=p.relative_to(root).as_posix()
        if stat.S_ISREG(mode):files.add(name)
        elif stat.S_ISDIR(mode):dirs.add(name)
        else:raise ValueError('Special file forbidden: '+name)
    need(files==ALL_FILES,'Exact publication file inventory mismatch')
    need(dirs==ALL_DIRS,'Exact publication directory inventory mismatch')
    return root
def run(path,*args,optimized=False,cwd='/'):
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONOPTIMIZE']='0'
    p=subprocess.run([sys.executable,*(['-O'] if optimized else []),'-B',str(path),*map(str,args)],cwd=cwd,env=env,capture_output=True,text=True)
    need(p.returncode==0,'Replay failed: '+str(path)+': '+p.stderr)
    return json.loads(p.stdout,object_pairs_hook=unique)
def check(root,pin=None,replay=False):
    root=inventory(root);raw=(root/'PUBLICATION_MANIFEST.json').read_bytes()
    if pin is not None:need(sha(raw)==pin,'External manifest pin mismatch')
    m=read(root/'PUBLICATION_MANIFEST.json');need(set(m)=={'schema_version','problem_id','files'},'Manifest schema')
    need(type(m['schema_version']) is int and m['schema_version']==1 and type(m['problem_id']) is int and m['problem_id']==6200014,'Manifest identity')
    need(isinstance(m['files'],dict) and set(m['files'])==ALL_FILES-{'PUBLICATION_MANIFEST.json'},'Manifest file set')
    for n,entry in m['files'].items():
        need(isinstance(entry,dict) and set(entry)=={'sha256','bytes'} and type(entry['bytes']) is int,'Manifest entry schema')
        need(entry==meta((root/n).read_bytes()),'Publication byte identity: '+n)
    members=0
    for folder,spec,files in [('author',AUTHOR,AUTHOR_FILES),('audit',AUDIT,AUDIT_FILES)]:
        name,size,digest,mpin=spec;p=root/'frozen_archives'/name
        need(meta(p.read_bytes())=={'bytes':size,'sha256':digest},'Immutable ZIP anchor mismatch')
        with zipfile.ZipFile(p) as z:
            names=z.namelist();need(len(names)==len(set(names))==len(files) and set(names)==files,'ZIP member inventory')
            for info in z.infolist():
                parts=pathlib.PurePosixPath(info.filename).parts
                need(not info.filename.startswith('/') and '\\' not in info.filename and all(x not in {'','..','.'} for x in parts),'Unsafe ZIP member')
                need(stat.S_ISREG(info.external_attr>>16),'Nonregular ZIP member')
                need(z.read(info.filename)==(root/folder/info.filename).read_bytes(),'Extracted file differs from freeze')
                members+=1
        need(sha((root/folder/'MANIFEST.json').read_bytes())==mpin,'Frozen manifest anchor mismatch')
    result=read(root/'RESULT.json')
    need(result['problem_id']==6200014 and result['disposition']=='already_solved','Result identity')
    need(result['classification']=='full_positive_consequence_of_credited_published_theorems','Result classification')
    need(result['substantive_approaches_used']==2 and result['permitted_approaches']==5,'Approach budget')
    need(result['novelty_claim'] is False and result['human_peer_review'] is False and result['formal_mathematical_certification'] is False,'Status flags')
    need(result['scope']['flag'] is True and result['scope']['no_induced_four_cycle'] is True and result['scope']['PL_assumed_separately'] is False,'Scope')
    out={'status':'PASS','publication_files':len(ALL_FILES),'matched_frozen_members':members,'manifest_sha256':sha(raw),'external_manifest_pin_checked':pin is not None,'replay':'NOT_RUN','corpus_identity':'NOT_RUN: optional external inputs are not bundled','topological_theorems_formally_verified':False}
    if replay:
        for mode in [False,True]:
            a=run(root/'author/verify.py',optimized=mode);b=run(root/'audit/verify.py',optimized=mode)
            need(a['integrity_pass'] is True and b['audit_integrity_pass'] is True,'Frozen verifier result')
            r=run(root/'audit/code/audit_checks.py','--author-archive',root/'frozen_archives'/AUTHOR[0],optimized=mode)
            need(r==read(root/'audit/results/author_replay.json'),'Author replay output mismatch')
        out['replay']={'normal_and_optimized':'PASS','author_clean_and_mutation_cases_per_runner':30,'author_mutation_rejections_per_runner':28,'independent_labeled_graphs':1100,'author_runner_relocated_replay':True,'imported_topological_theorems_certified':False}
    return out

def queue_check(root,before,after):
    b=pathlib.Path(before).read_bytes();a=pathlib.Path(after).read_bytes();d=read(root/'QUEUE_DELTA.json')
    need(meta(b)==d['before'] and meta(a)==d['after'],'Queue snapshot identity')
    x,y=b.splitlines(keepends=True),a.splitlines(keepends=True);need(len(x)==len(y),'Queue line count')
    changed=[i for i,(u,v) in enumerate(zip(x,y)) if u!=v];need(len(changed)==1,'Exactly one changed row required');i=changed[0]
    need(b'| 808 | 6200014 / AMR-061-0014 |' in x[i],'Queue target')
    c,e=x[i].split(b'|'),y[i].split(b'|');need(len(c)==len(e)==14,'Queue column count')
    need([j for j,(u,v) in enumerate(zip(c,e)) if u!=v]==[8,9,11],'Only Status, Turns, Findings')
    for k,j in [('Status',8),('Turns',9),('Findings',11)]:need(d['changes'][k]=={'from':c[j].decode().strip(),'to':e[j].decode().strip()},'Queue field '+k)
    need(e[8].strip()==b'already_solved' and e[9].strip()==b'2/5','Queue disposition')
    return {'status':'PASS','changed_rows':1,'changed_columns':['Status','Turns','Findings'],'all_other_bytes_preserved':True}

def negative_controls(root,pin):
    rejected=[]
    def trial(name,mutate):
        with tempfile.TemporaryDirectory(prefix='boundary-publication-control-') as temp:
            p=pathlib.Path(temp)/'packet';shutil.copytree(root,p);mutate(p)
            try:check(p,pin)
            except (ValueError,OSError,zipfile.BadZipFile):rejected.append(name)
            else:raise ValueError('Mutation accepted: '+name)
    trial('missing_file',lambda p:(p/'RESULT.json').unlink())
    trial('changed_proof',lambda p:(p/'author/PROOF.md').write_bytes(b'changed'))
    trial('changed_audit',lambda p:(p/'audit/AUDIT_REPORT.md').write_bytes(b'changed'))
    trial('changed_code',lambda p:(p/'audit/code/audit_checks.py').write_bytes(b'pass\n'))
    trial('changed_author_zip',lambda p:(p/'frozen_archives'/AUTHOR[0]).write_bytes(b'bad'))
    trial('changed_audit_zip',lambda p:(p/'frozen_archives'/AUDIT[0]).write_bytes(b'bad'))
    trial('extra_file',lambda p:(p/'extra.txt').write_text('extra'))
    trial('extra_directory',lambda p:(p/'extra').mkdir())
    trial('symlink',lambda p:(p/'link').symlink_to('README.md'))
    trial('special_file',lambda p:os.mkfifo(p/'pipe'))
    def duplicate(p):
        f=p/'PUBLICATION_MANIFEST.json';f.write_text(f.read_text().replace('"schema_version": 1','"schema_version": 1, "schema_version": 1'))
    trial('duplicate_manifest_key',duplicate)
    def rebound(p):
        f=p/'RESULT.json';r=read(f);r['disposition']='claimed_solved';f.write_text(json.dumps(r));m=read(p/'PUBLICATION_MANIFEST.json');m['files']['RESULT.json']=meta(f.read_bytes());(p/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
    trial('rebound_manifest',rebound)
    with tempfile.TemporaryDirectory(prefix='boundary-link-control-') as temp:
        t=pathlib.Path(temp);(t/'ancestor').mkdir();shutil.copytree(root,t/'ancestor/packet');(t/'linked').symlink_to(t/'ancestor',target_is_directory=True)
        try:check(t/'linked/packet',pin)
        except ValueError:rejected.append('ancestor_symlink')
        else:raise ValueError('Ancestor symlink accepted')
    # Independently challenge the unchanged audit verifier, including semantic rehashes.
    audit_rejected=[]
    for optimized in [False,True]:
        for case in ['missing_report','altered_report','extra_file','symlink','duplicate_manifest_key','manifest_traversal','wrong_size','rehash_false_replay','rehash_false_finite_result']:
            with tempfile.TemporaryDirectory(prefix='boundary-audit-control-') as temp:
                p=pathlib.Path(temp)/'audit';shutil.copytree(root/'audit',p);f=p/'MANIFEST.json'
                if case=='missing_report':(p/'AUDIT_REPORT.md').unlink()
                elif case=='altered_report':(p/'AUDIT_REPORT.md').write_bytes(b'bad')
                elif case=='extra_file':(p/'extra').write_text('extra')
                elif case=='symlink':(p/'link').symlink_to('AUDIT_REPORT.md')
                elif case=='duplicate_manifest_key':f.write_text(f.read_text().replace('"schema_version": 1','"schema_version": 1, "schema_version": 1'))
                elif case in {'manifest_traversal','wrong_size'}:
                    m=read(f)
                    if case=='manifest_traversal':m['files']['../escape']=meta(b'')
                    else:m['files']['AUDIT_REPORT.md']['bytes']+=1
                    f.write_text(json.dumps(m))
                else:
                    name='results/author_replay.json' if case=='rehash_false_replay' else 'results/finite_controls.json';j=read(p/name)
                    if case=='rehash_false_replay':j['all_pass']=False
                    else:j['exhaustive_labeled_graphs_vertices_0_through_5']=1
                    (p/name).write_text(json.dumps(j));m=read(f);m['files'][name]=meta((p/name).read_bytes());f.write_text(json.dumps(m))
                proc=subprocess.run([sys.executable,*(['-O'] if optimized else []),'-B',str(p/'verify.py')],cwd='/',capture_output=True,text=True)
                need(proc.returncode!=0,'Audit mutation accepted: '+case);audit_rejected.append({'case':case,'optimized':optimized})
    return {'publication_rejections':rejected,'audit_rejections':audit_rejected}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256');ap.add_argument('--replay',action='store_true');ap.add_argument('--negative-controls',action='store_true');ap.add_argument('--queue-base');ap.add_argument('--queue-updated');args=ap.parse_args()
    try:
        root=pathlib.Path(os.path.abspath(__file__)).parent
        out=check(root,args.manifest_sha256,args.replay)
        need(bool(args.queue_base)==bool(args.queue_updated),'Supply both queue snapshots')
        if args.queue_base:out['queue_check']=queue_check(root,args.queue_base,args.queue_updated)
        if args.negative_controls:out['negative_controls']=negative_controls(root,args.manifest_sha256 or out['manifest_sha256'])
        if args.manifest_sha256 is None:out['qualification']='Publication internal consistency only; authenticate the external manifest digest separately. Original freezes have hard-coded pins.'
        print(json.dumps(out,indent=2,sort_keys=True))
    except Exception as exc:print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
