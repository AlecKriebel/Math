#!/usr/bin/env python3
"""Independent repair protocol/full96streams and four closed namespaces."""
import gzip,hashlib,json,pathlib
from capture import ROOT,PRIVATE,run,sha,now
A=ROOT.parent;F=A/'clean_final_adversary';BASE='728b48109a11e83769b24ec5b30978c1c5ed7ec9'
checks=[]
def check(n,c):assert c,n;checks.append(n)
failure=json.loads((A/'ROOT_TRUNCATED_API_REPLAY_FAILURE.json').read_bytes())
for old,r in failure['lossless_relocation_map'].items():
    b=(A/r['new_path']).read_bytes();check('failure preserved '+old,len(b)==r['bytes'] and sha(b)==r['sha256'])
check('failure exact reason',b'AssertionError: prepared_base_api_tree entirestdout' in (A/'root_whole_verification.stderr.failed01').read_bytes())
root=json.loads((A/'root_whole_verification_receipt.json').read_bytes())
check('whole76467checks',root['check_count']==76467 and len(root['checks'])==76467 and all(x['passed'] is True for x in root['checks']))
check('complete96captures',len(root['captures'])==len(root['every_prepared_readonly_command'])==96)
p=run('fixed_base_tree',['git','ls-tree','-rtzl','--full-tree',BASE]);check('fixedbase capture exit',p.returncode==0 and p.stderr==b'')
fixed={}
for row in p.stdout.split(b'\0'):
    if row:
        h,path=row.split(b'\t',1);mode,kind,oid,size=h.decode().split()
        fixed[path.decode()]=dict(mode=mode,type=kind,sha=oid,size=None if size=='-' else int(size))
old_records={r['name']:r for r in json.loads((F/'COMMANDS.json').read_bytes())}
allowed={(end,'repo',field) for end in ['head','base'] for field in ['open_issues_count','open_issues','pushed_at','updated_at']}
diffs=[];partial_facts=[];streams_count=0
def walk(a,b,capture,path=()):
    if isinstance(a,dict) and isinstance(b,dict):
        check(capture+str(path)+' keyset',a.keys()==b.keys())
        for k in a:walk(a[k],b[k],capture,path+(k,))
    elif isinstance(a,list) and isinstance(b,list):
        check(capture+str(path)+' arraylen',len(a)==len(b))
        for i,(x,y) in enumerate(zip(a,b)):walk(x,y,capture,path+(i,))
    elif a!=b:
        check(capture+str(path)+' typedpermitted',path in allowed and type(a) is type(b));diffs.append(dict(capture=capture,path=list(path),before=a,after=b))
def reported_subset(obj,label):
    check(label+' immutable root',obj['sha']=='2ef2e883ac42114d7ad82ca7248a1e0d90d52c2b' and obj['truncated'] is True)
    check(label+' unique reportedpaths',len(obj['tree'])==len({r['path'] for r in obj['tree']}))
    for r in obj['tree']:
        check(label+' supported keys '+r['path'],set(r) in [set(['path','mode','type','sha','url']),set(['path','mode','type','sha','url','size'])])
        ref=fixed[r['path']]
        check(label+' everyreportedentry '+r['path'],all(r[k]==ref[k] for k in ['mode','type','sha']) and ('size' not in r or r['size']==ref['size'])
          and r['url']=='https://api.github.com/repos/AlecKriebel/Math/git/'+('trees/' if r['type']=='tree' else 'blobs/')+r['sha'])
    partial_facts.append(dict(label=label,reported_entries=len(obj['tree']),sha=obj['sha'],truncated=True,coverage_certified=False))
for r in root['captures']:
    values={}
    for name,s in r['streams'].items():
        stored=(A/s['path']).read_bytes();data=gzip.decompress(stored)
        check(r['name']+' '+name+' stored',len(stored)==s['stored_bytes'] and sha(stored)==s['stored_sha256'])
        check(r['name']+' '+name+' logical',len(data)==s['bytes'] and sha(data)==s['sha256']);values[name]=data;streams_count+=1
    old=old_records[r['name']]
    prior={s:gzip.decompress((F/old['streams'][s]['path']).read_bytes()) for s in ['stdout','stderr']}
    check(r['name']+' exit/fullstderr',r['exit']==old['exit_code'] and values['stderr']==prior['stderr'])
    if r['name']=='prepared_base_api_tree':
        x=json.loads(prior['stdout']);y=json.loads(values['stdout'])
        check('truncated metadata exact',{k:v for k,v in x.items() if k!='tree'}=={k:v for k,v in y.items() if k!='tree'})
        reported_subset(x,'historical');reported_subset(y,'successful replay')
        last=json.loads(gzip.decompress((A/'root_replay_private/whole_prepared.failed01/prepared_base_api_tree.stdout.gz').read_bytes()))
        check('failed replay metadata exact',{k:v for k,v in x.items() if k!='tree'}=={k:v for k,v in last.items() if k!='tree'})
        reported_subset(last,'failed replay')
        rec=r['complete_fixed_local_tree_capture'];b=gzip.decompress((A/rec['path']).read_bytes())
        check('rootfixedfulltree wholeequalsfresh',b==p.stdout and len(b)==rec['bytes'] and sha(b)==rec['sha256'])
    elif r['name'].endswith(('_begin_pr','_end_pr')) and values['stdout']!=prior['stdout']:
        walk(json.loads(prior['stdout']),json.loads(values['stdout']),r['name'])
    else:check(r['name']+' complete stdout',values['stdout']==prior['stdout'])
check('all permitted metadata exactlyrecorded',diffs==root['allowed_repository_metadata_differences'])

closures=[]
for directory,mf,msha,seal_sha,count,private_count in [
    ('path_geometry_review','PUBLIC_MANIFEST.json','44d334caa6835c18388a67f58f5d8756637c76c355268cddfd5160569f61c80c','d27fb0fabce2459ade5afdf28586f0831d7d16815f04b8306c9dd6da4dfa74e9',105,38),
    ('poisson_components_review','PUBLIC_MANIFEST.json','5a6ef2af64d435ecce35a305a7de91295ea6ccd02c2290edfab0c7c7fa70be9d','082d6d7886f5d9b50903020a0f4698589f27bc7a66df2a9668146466100314a3',19,122),
    ('poisson_components_corrections','SUPPLEMENT_MANIFEST.json','66c0589d7cf86634850201c04a6016a3fdd24f2a94e5789d134036841884ab1c','eb94d2c623d6ee2d542d690393216468b3391158c04577d1686c09a318aa8d9b',4,4),
    ('clean_final_adversary','PUBLIC_MANIFEST.json','3cbb5c58f9ba3a879882d0c9c7d4813adce2a2b0180cb478b73fa99b45ea7954','13febe54f43886b1f2bbaeeab7b056fce6437469b4bc368feec6ebc5c8a2cd08',236,588)]:
    d=A/directory;m=json.loads((d/mf).read_bytes())
    check(directory+' sealedpins',sha((d/mf).read_bytes())==msha and sha((d/'FINAL_SEAL.json').read_bytes())==seal_sha)
    if directory=='clean_final_adversary':pub=m['public_files'];private=m['private_files']
    else:
        fs=m['files'];pub={r['path']:r for r in fs} if isinstance(fs,list) else fs
        if directory=='path_geometry_review':private={r['path']:r for r in m['private_inventory']}
        else:private=json.loads((d/('receipts/private_inventory.json' if directory=='poisson_components_review' else 'PRIVATE_INVENTORY.json')).read_bytes())['files']
    check(directory+' counts',len(pub)==count and len(private)==private_count)
    expected=set(pub)|set(private)|{mf,'FINAL_SEAL.json'}
    check(directory+' exactnamespace',{p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()}==expected)
    for path,r in (pub|private).items():
        data=(d/path).read_bytes()
        if 'stored_bytes' in r:
            check(directory+'/'+path+' stored',len(data)==r['stored_bytes'] and sha(data)==r['stored_sha256'])
            logical=gzip.decompress(data) if r['encoding']=='gzip' else data
            check(directory+'/'+path+' logical',len(logical)==r['logical_bytes'] and sha(logical)==r['logical_sha256'])
        else:
            check(directory+'/'+path+' bytes',len(data)==r['bytes'] and sha(data)==r['sha256'])
            if 'logical_bytes' in r:
                logical=gzip.decompress(data);check(directory+'/'+path+' logical',len(logical)==r['logical_bytes'] and sha(logical)==r['logical_sha256'])
    closures.append(dict(directory=directory,manifest=mf,manifest_sha256=msha,seal_sha256=seal_sha,public_count=count,private_count=private_count))
out=dict(completed_utc=now(),whole_root_streams=streams_count,root96capturedcommands=96,root_checks=76467,partial_subsets=partial_facts,
    no_partial_whole_byte_or_coverage_claim=True,root_missing_subprocess_auxiliary_stderr_receipt='Original ROOT check_output auxiliary tree omitted explicit stderr/exit/timing receipt; this independent full command supplies all fields and identical stdout.',
    closures=closures,checks=checks,closed_namespaces_unchanged=True,mathematics_credited_percent=100,novel_theorems=0)
(ROOT/'REPAIR_AND_CLOSURES.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
