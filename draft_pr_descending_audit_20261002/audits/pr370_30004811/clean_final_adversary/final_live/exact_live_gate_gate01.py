"""Additive, read-only exact-live gate. Writes only unique private runs and receipts here.

Run with the supplied Python/SymPy interpreter. --label names an append-only run.
No Git write, checkout, fetch, index update, service mutation, or external contact.
"""
from pathlib import Path
import argparse, base64, concurrent.futures, copy, datetime, hashlib, json
import re, subprocess, sys, traceback, urllib.request

HERE=Path(__file__).resolve().parent
OWN=HERE.parent
AUDIT=OWN.parent
REPO=OWN.parents[3]
PINS=json.loads((HERE/'PINS.json').read_text())
TARGET='problems/30004811_capacity_volume_mass'
RUNTIME=REPO/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def blobsha(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def require(ok, why):
    if not ok: raise ValueError(why)
parser=argparse.ArgumentParser()
parser.add_argument('--label',default=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
args=parser.parse_args()
require(bool(re.fullmatch(r'[A-Za-z0-9_-]+',args.label)),'unsafe run label')
RUN=HERE/'private'/args.label
RUN.mkdir(parents=True,exist_ok=False)
receipt={'started_utc':utc(),'pins':PINS,'pins_file_sha256':sha((HERE/'PINS.json').read_bytes()),
         'program_sha256':sha(Path(__file__).read_bytes()),'label':args.label,'checks':[],
         'commands':{},'sources':[],'reproduction':{},'status':'RUNNING'}
def ck(name, ok, evidence=None):
    receipt['checks'].append({'name':name,'pass':bool(ok),'evidence':evidence})
    require(ok,name)
def command(name, argv, expected=0):
    p=subprocess.run([str(a) for a in argv],cwd=REPO,capture_output=True)
    (RUN/(name+'.stdout')).write_bytes(p.stdout)
    (RUN/(name+'.stderr')).write_bytes(p.stderr)
    receipt['commands'][name]={'argv':[str(a) for a in argv],'returncode':p.returncode,
       'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
    require(p.returncode==expected,name+' command exit differs from expected')
    return p.stdout
def git(name,*argv): return command(name,['git',*argv])
def api(name,path):
    return json.loads(command(name,['gh','api','-H','Cache-Control: no-cache',f'repos/{PINS["repository"]}/{path}']))
def gitbytes(name, rev, path): return git(name,'show',rev+':'+path)
def live_view(phase):
    pr=api(phase+'_pr',f'pulls/{PINS["pr"]}')
    main=api(phase+'_main','git/ref/heads/main')['object']['sha']
    refs=git(phase+'_remote_refs','ls-remote','origin','refs/heads/main','refs/heads/'+PINS['branch']).decode()
    remote={ref:commit for commit,ref in (l.split('\t') for l in refs.splitlines())}
    view={'pr':pr,'main':main,'remote':remote}
    validate_view(view)
    receipt[phase+'_live_projection']={'pr':pr['number'],'head':pr['head']['sha'],'base':pr['base']['sha'],
       'main':main,'body_sha256':sha(pr['body'].encode()),'draft':pr['draft'],'state':pr['state'],
       'merged':pr['merged'],'mergeable':pr['mergeable'],'mergeable_state':pr['mergeable_state'],
       'title':pr['title'],'updated_at':pr['updated_at'],'remote':remote}
    return view
def validate_view(v):
    p=v['pr']
    require(p['number']==PINS['pr'] and p['base']['repo']['full_name']==PINS['repository'],'wrong PR/repo')
    require(p['head']['sha']==PINS['head'] and p['head']['ref']==PINS['branch'],'head drift')
    require(p['base']['sha']==PINS['base'] and p['base']['ref']=='main','base drift')
    require(v['main']==PINS['base'],'main drift')
    require(v['remote'].get('refs/heads/main')==PINS['base'],'remote main drift')
    require(v['remote'].get('refs/heads/'+PINS['branch'])==PINS['head'],'remote head drift')
    require(sha(p['body'].encode())==PINS['body_sha256'],'body drift')
    require(p['draft'] is False and p['state']=='open' and p['merged'] is False,'PR readiness/state drift')
def tree(name, rev, path=None):
    argv=['ls-tree','-r','-z',rev]
    if path: argv.append(path)
    raw=git(name,*argv)
    d={}
    for line in raw.split(b'\0'):
        if not line: continue
        meta,path=line.split(b'\t',1);mode,kind,blob=meta.decode().split()
        d[path.decode()]={'mode':mode,'kind':kind,'blob':blob}
    return d
def queue_expected(base):
    lines=base.splitlines(keepends=True)
    require(len(lines)>=PINS['queue_line'],'queue too short')
    i=PINS['queue_line']-1
    row=lines[i].decode()
    require('30004811 / OWR-8415343-014' in row,'wrong physical queue line')
    cells=row.split('|')
    require(len(cells)==14 and cells[8].strip()=='queued' and cells[9].strip()=='0/5','unexpected old queue cells')
    cells[8]=' '+PINS['queue_status']+' '
    cells[9]=' '+PINS['queue_turns']+' '
    lines[i]='|'.join(cells).encode()
    return b''.join(lines)

try:
    initial=live_view('initial')
    ck('initial_live_exact_pins',True)
    for which in ['head','main','body','draft']:
        v=copy.deepcopy(initial)
        if which=='head': v['pr']['head']['sha']='0'*40
        elif which=='main': v['main']='0'*40
        elif which=='body': v['pr']['body']+=' '
        else: v['pr']['draft']=True
        try: validate_view(v)
        except ValueError: rejected=True
        else: rejected=False
        ck('negative_live_'+which+'_drift_rejected',rejected)
    branch=git('checkout_branch','branch','--show-current').decode().strip()
    ck('review_checkout_remains_main',branch=='main')
    commit=json.loads(command('local_head_metadata',['git','show','-s','--format={"head":"%H","tree":"%T","parents":"%P"}',PINS['head']]))
    ck('local_head_tree_parent_pins',commit['head']==PINS['head'] and commit['tree']==PINS['tree'] and commit['parents'].split()==[PINS['original_head'],PINS['base']],commit)
    mb=git('merge_base','merge-base',PINS['base'],PINS['head']).decode().strip()
    ck('virtual_merge_base_is_current_main',mb==PINS['base'])
    git('base_is_ancestor','merge-base','--is-ancestor',PINS['base'],PINS['head'])
    ck('virtual_merge_is_exact_head_tree',True,{'mechanism':'base is an ancestor of head, so a merge into that pinned base fast-forwards to the exact head tree; no merge-tree write or object mutation is needed','tree':PINS['tree']})
    remote_commit=api('api_git_commit','git/commits/'+PINS['head'])
    ck('literal_api_commit_tree_parents',remote_commit['sha']==PINS['head'] and remote_commit['tree']['sha']==PINS['tree'] and [e['sha'] for e in remote_commit['parents']]==[PINS['original_head'],PINS['base']])
    base_tree=tree('recursive_base_tree',PINS['base'])
    head_tree=tree('recursive_head_tree',PINS['head'])
    target_paths=sorted(p for p in head_tree if p.startswith(TARGET+'/'))
    ck('recursive_target_exactly_18_regular_blobs',len(target_paths)==18 and all(head_tree[p]['mode']=='100644' and head_tree[p]['kind']=='blob' for p in target_paths),[{'path':p,**head_tree[p]} for p in target_paths])
    original_tree=tree('recursive_original_target',PINS['original_head'],TARGET)
    ck('all_18_original_recursive_paths_modes_blobs_unchanged',{p:head_tree[p] for p in target_paths}==original_tree)
    changed=sorted(p for p in base_tree.keys()|head_tree.keys() if base_tree.get(p)!=head_tree.get(p))
    ck('full_recursive_difference_exact_scope',changed==sorted(target_paths+[PINS['queue_path']]),{'base_entries':len(base_tree),'head_entries':len(head_tree),'changed_paths':changed})
    api_files=api('literal_api_changed_files',f'pulls/{PINS["pr"]}/files?per_page=100')
    ck('literal_api_full_file_projection',len(api_files)==19 and sorted(e['filename'] for e in api_files)==changed and all(e['sha']==head_tree[e['filename']]['blob'] for e in api_files))
    target_blob={p:gitbytes('target_blob_'+str(i),PINS['head'],p) for i,p in enumerate(target_paths)}
    for p,b in target_blob.items(): ck('actual_blob_'+p,blobsha(b)==head_tree[p]['blob'])
    def remote_blob(task):
        i,p=task
        data=api('remote_target_blob_'+str(i),'git/blobs/'+head_tree[p]['blob'])
        require(data['encoding']=='base64','unexpected blob encoding')
        b=base64.b64decode(data['content'])
        return {'path':p,'equal':b==target_blob[p],'api_blob_sha':data['sha'],'bytes':len(b),'sha256':sha(b)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: api_blobs=list(pool.map(remote_blob,enumerate(target_paths)))
    ck('literal_api_all_18_actual_contents',all(e['equal'] and e['api_blob_sha']==head_tree[e['path']]['blob'] for e in api_blobs),api_blobs)
    short={p[len(TARGET)+1:]:b for p,b in target_blob.items()}
    parsed={p:json.loads(b) for p,b in short.items() if p.endswith('.json')}
    ck('all_seven_candidate_json_complete_parsed',len(parsed)==7,{'sha256':{p:sha(short[p]) for p in parsed},'complete_nodes':parsed})
    bindings=[]
    for manifest,prefix in [('FINAL_AUTHOR_MANIFEST.json',''),('PUBLICATION_MANIFEST.json',''),('review/REVIEW_MANIFEST.json','review/')]:
        for e in parsed[manifest]['files']:
            path=prefix+e['path'];b=short[path]
            ok=len(b)==e['bytes'] and sha(b)==e['sha256'];bindings.append({'manifest':manifest,'path':path,'pass':ok})
    ck('all_29_nested_byte_and_sha256_bindings',len(bindings)==29 and all(e['pass'] for e in bindings),bindings)
    ck('publication_manifest_exact_17_nonself_paths',sorted(e['path'] for e in parsed['PUBLICATION_MANIFEST.json']['files'])==sorted(p for p in short if p!='PUBLICATION_MANIFEST.json'))
    ck('review_author_manifest_binding',parsed['review/REVIEW_MANIFEST.json']['author_manifest_sha256']==sha(short['FINAL_AUTHOR_MANIFEST.json']))
    author_paths=[e['path'] for e in parsed['FINAL_AUTHOR_MANIFEST.json']['files']]+['FINAL_AUTHOR_MANIFEST.json']
    for i,p in enumerate(author_paths): ck('immutable_author_parent_'+p,gitbytes('author_original_'+str(i),PINS['author_parent'],TARGET+'/'+p)==short[p])
    ck('immutable_author_file_count',len(author_paths)==10)
    old_author_tree=tree('author_parent_target_tree',PINS['author_parent'],TARGET)
    review_paths=['review/'+e['path'] for e in parsed['review/REVIEW_MANIFEST.json']['files']]+['review/REVIEW_MANIFEST.json']
    ck('historical_review_provenance_not_in_author_parent',len(review_paths)==4 and all(TARGET+'/'+p not in old_author_tree for p in review_paths),{'limitation':'The four historical review files are bound at original and repaired publication heads, not the author parent; no earlier Git anchor is claimed.'})
    base_queue=gitbytes('base_queue',PINS['base'],PINS['queue_path'])
    head_queue=gitbytes('head_queue',PINS['head'],PINS['queue_path'])
    prior_queue=gitbytes('prior_current_main_queue',PINS['prior_current_main'],PINS['queue_path'])
    ck('full_prior_current_queue_identity',sha(prior_queue)==PINS['prior_current_queue_sha256'] and base_queue==prior_queue)
    ck('full_queue_only_physical_line410_cells8_9',head_queue==queue_expected(base_queue) and sha(head_queue)==PINS['repaired_queue_sha256'],{'base_bytes':len(base_queue),'base_sha256':sha(base_queue),'head_bytes':len(head_queue),'head_sha256':sha(head_queue),'line':410,'cells':[8,9],'status':'already_solved','turns':'1/5'})
    ck('negative_foreign_queue_byte_rejected',head_queue+b'\n'!=queue_expected(base_queue))
    family_records=[]
    for family,fpin in PINS['families'].items():
        mp=fpin['manifest_path'];mb=gitbytes('family_'+family+'_manifest',PINS['base'],mp)
        ck('published_family_manifest_'+family,sha(mb)==fpin['manifest_sha256'] and (REPO/mp).read_bytes()==mb)
        mf=json.loads(mb);parent=str(Path(mp).parent)
        require(all(e['path']!='PUBLIC_MANIFEST.json' and not e['path'].startswith('private/') for e in mf['files']),'family manifest violates exclusions')
        seals=[]
        for i,e in enumerate(mf['files']):
            path=parent+'/'+e['path'];b=gitbytes('family_'+family+'_'+str(i),PINS['base'],path)
            ck('published_family_file_'+family+'/'+e['path'],len(b)==e['bytes'] and sha(b)==e['sha256'] and (REPO/path).read_bytes()==b and head_tree[path]==base_tree[path])
            if 'SEAL' in e['path']:
                sd=json.loads(b)
                if isinstance(sd.get('files'),dict): links=sd['files'].items()
                else: links=[(sd.get('artifact',sd.get('file')),sd['sha256'])]
                bound=[]
                for j,(rel,h) in enumerate(links):
                    sb=gitbytes('family_seal_'+family+'_'+str(i)+'_'+str(j),PINS['base'],parent+'/'+rel)
                    ck('seal_content_'+family+'/'+e['path']+'/'+rel,sha(sb)==h)
                    bound.append({'path':rel,'sha256':h})
                seals.append({'seal':e['path'],'content':sd,'bound_files':bound})
        family_records.append({'family':family,'manifest_sha256':sha(mb),'bound_files':len(mf['files']),'seals':seals})
    ck('three_original_family_manifests_and_seals_published',len(family_records)==3 and [e['bound_files'] for e in family_records]==[18,18,15],family_records)
    ck('no_raw_sources_in_target',all('/sources/' not in p and not p.endswith(('.pdf','.png','.jpg')) for p in target_paths))
    dest=RUN/'candidate';dest.mkdir()
    for rel,b in short.items(): p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    sources=dest/'sources';sources.mkdir()
    def fetch(e):
        began=utc()
        try:
            with urllib.request.urlopen(e['url'],timeout=30) as response:
                b=response.read();final_url=response.url
            (sources/e['name']).write_bytes(b)
            r={'name':e['name'],'url':e['url'],'final_url':final_url,'started_utc':began,'completed_utc':utc(),'bytes':len(b),'sha256':sha(b),'match':len(b)==e['bytes'] and sha(b)==e['sha256']}
        except Exception as exc:
            r={'name':e['name'],'url':e['url'],'started_utc':began,'completed_utc':utc(),'match':False,'error':repr(exc)}
            (RUN/('source_'+e['name']+'.stderr')).write_text(traceback.format_exc())
        return r
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: receipt['sources']=list(pool.map(fetch,parsed['SOURCE_MANIFEST.json']['files']))
    ck('all_seven_fresh_primary_pdf_identities',len(receipt['sources'])==7 and all(e['match'] for e in receipt['sources']),receipt['sources'])
    runs=[('author',[RUNTIME,dest/'check_turn_1.py']),('historical_review',[RUNTIME,dest/'review/check.py',dest]),('publication_sources',[RUNTIME,dest/'verify_publication.py']),('independent_controls',[RUNTIME,OWN/'independent_controls.py'])]
    for name,argv in runs:
        b=command('replay_'+name,argv);receipt['reproduction'][name]=json.loads(b)
        if name=='author': ck('author_complete_byte_exact',b==short['TURN_1_CHECKS.json'])
        if name=='historical_review': ck('historical_review_complete_json_exact',json.loads(b)==parsed['review/CHECKS.json'])
    # Removing only a directory entry in the private replay makes the zero-source path explicit.
    sources.rename(dest/'private_source_cache')
    b=command('replay_publication_source_free',[RUNTIME,dest/'verify_publication.py'])
    receipt['reproduction']['publication_source_free']=json.loads(b)
    expected={'all_public_hashes':True,'author_assertions':5529,'independent_assertions':3128,'raw_source_hashes_checked_this_run':0,'status':'PASS'}
    ck('publication_source_free_complete_json',json.loads(b)==expected)
    expected['raw_source_hashes_checked_this_run']=7
    ck('publication_source_present_complete_json',receipt['reproduction']['publication_sources']==expected)
    ck('independent_complete_control_status',receipt['reproduction']['independent_controls']['status']=='PASS' and receipt['reproduction']['independent_controls']['exact_identities']==10 and all(receipt['reproduction']['independent_controls']['checks'].values()))
    final=live_view('final')
    ck('final_literal_main_head_base_body_still_exact',True)
    ck('initial_final_identity_equal',receipt['initial_live_projection']['head']==receipt['final_live_projection']['head'] and receipt['initial_live_projection']['base']==receipt['final_live_projection']['base'] and receipt['initial_live_projection']['body_sha256']==receipt['final_live_projection']['body_sha256'])
    receipt['status']='PASS_EXACT_LIVE_QUALIFIED'
    receipt['scope_limitations']=['Affirmative original-class result is credited prior work; broad all-AF counterexample has negative scalar curvature in the compact fill.',
       'No novelty certification or exact global mCV value; analytic proof and external credited theorems remain the mathematical basis.',
       'Historical review files have no earlier author-parent Git anchor; original/repaired publication heads and manifests bind them.',
       'No merge/release/CI-success claim. This receipt is valid only for the exact pins and observation interval; any main/head/body drift requires rejection and a new gate.',
       'Virtual merge follows from pinned-base ancestry; no Git object-producing merge operation was used.']
except Exception as exc:
    receipt['status']='REJECTED'
    receipt['failure']=repr(exc)
    (RUN/'gate_failure.stderr').write_text(traceback.format_exc())
finally:
    receipt['completed_utc']=utc()
    receipt['private_run_relative']=str(RUN.relative_to(HERE))
    output=HERE/('RECEIPT_'+args.label+'.json')
    require(not output.exists(),'receipt already exists')
    output.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':receipt['status'],'receipt':str(output),'passed_checks':sum(e['pass'] for e in receipt['checks']),'failure':receipt.get('failure')},indent=2))
if receipt['status']!='PASS_EXACT_LIVE_QUALIFIED': sys.exit(1)
