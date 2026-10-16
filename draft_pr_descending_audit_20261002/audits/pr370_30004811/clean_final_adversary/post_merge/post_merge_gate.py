"""Standalone actual post-merge readback. Read-only Git/API, append-only scoped outputs.

Usage: python3 post_merge_gate.py --label unique_name
No fetch, checkout, Git object/index/ref write, service mutation, PDFs, or proof replay.
Raw streams are losslessly compressed; only scoped recursive maps are retained.
"""
from pathlib import Path
import argparse, base64, concurrent.futures, datetime, gzip, hashlib, json, re
import subprocess, sys, traceback

HERE=Path(__file__).resolve().parent
OWN=HERE.parent
REPO=OWN.parents[3]
PINS=json.loads((HERE/'PINS.json').read_text())
TARGET='problems/30004811_capacity_volume_mass'
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def blobsha(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def require(v,why):
    if not v: raise ValueError(why)
ap=argparse.ArgumentParser()
ap.add_argument('--label',default=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
args=ap.parse_args()
require(bool(re.fullmatch(r'[A-Za-z0-9_-]+',args.label)),'unsafe label')
RUN=HERE/'private'/args.label
RUN.mkdir(parents=True,exist_ok=False)
receipt={'status':'RUNNING','started_utc':utc(),'label':args.label,'pins':PINS,
         'program_sha256':sha(Path(__file__).read_bytes()),'pins_sha256':sha((HERE/'PINS.json').read_bytes()),
         'checks':[],'commands':{},'observations':{}}
def ck(name,ok,evidence=None):
    receipt['checks'].append({'name':name,'pass':bool(ok),'evidence':evidence})
    require(ok,name)
def cmd(name,argv,expected=0):
    p=subprocess.run([str(a) for a in argv],cwd=REPO,capture_output=True)
    for suffix,b in [('stdout',p.stdout),('stderr',p.stderr)]:
        (RUN/(name+'.'+suffix+'.gz')).write_bytes(gzip.compress(b,mtime=0))
    receipt['commands'][name]={'argv':[str(a) for a in argv],'returncode':p.returncode,
        'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),
        'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr),'streams':'gzip lossless mtime=0'}
    require(p.returncode==expected,name+' command exit')
    return p.stdout
def git(name,*args): return cmd(name,['git',*args])
def api(name,path): return json.loads(cmd(name,['gh','api','-H','Cache-Control: no-cache','repos/'+PINS['repository']+'/'+path]))
def content(name,rev,path): return git(name,'show',rev+':'+path)
def scoped_map(name,rev,*paths):
    out=git(name,'ls-tree','-r','-z',rev,'--',*paths)
    result={}
    for line in out.split(b'\0'):
        if not line: continue
        meta,path=line.split(b'\t',1);mode,kind,blob=meta.decode().split()
        result[path.decode()]={'mode':mode,'kind':kind,'blob':blob}
    return result
def rows(b):
    result={}
    for line in b.decode().splitlines():
        c=[x.strip() for x in line.split('|')]
        if len(c)==14 and c[1].isdigit():
            require(c[2] not in result,'duplicate queue ID')
            result[c[2]]=c
    return result
def preserves(older,newer):
    a,b=rows(older),rows(newer)
    key='30004811 / OWR-8415343-014'
    require(key in b and b[key][8:10]==['already_solved','1/5'],'accepted own queue disposition changed')
    for k,c in a.items():
        require(k in b,'queue row removed')
        if c[8]!='queued': require(b[k]==c,'previously accepted queue row changed: '+k)
    return [{'id':k,'status':c[8],'turns':c[9]} for k,c in b.items() if k in a and a[k]!=c]
def merge_view(phase):
    pr=api(phase+'_pr','pulls/'+str(PINS['pr']))
    main=api(phase+'_api_main','git/ref/heads/main')['object']['sha']
    remote=git(phase+'_refs','ls-remote','origin','refs/heads/main','refs/heads/'+PINS['branch']).decode()
    refs={ref:commit for commit,ref in (l.split('\t') for l in remote.splitlines())}
    local=git(phase+'_local_main','rev-parse','HEAD').decode().strip()
    require(pr['number']==370 and pr['base']['repo']['full_name']==PINS['repository'],'wrong PR/repository')
    require(pr['state']=='closed' and pr['merged'] is True and pr['merge_commit_sha']==PINS['accepted_merge'],'actual merge state/commit mismatch')
    require(pr['merged_at']==PINS['merged_at'],'merge time mismatch')
    require(pr['head']['sha']==PINS['head'] and pr['head']['repo']['full_name']==PINS['repository'],'accepted head mismatch')
    require(pr['base']['ref']=='main' and sha(pr['body'].encode())==PINS['body_sha256'],'base ref/body mismatch')
    require(refs.get('refs/heads/main')==main,'API versus remote main mismatch')
    require(refs.get('refs/heads/'+PINS['branch'],PINS['head'])==PINS['head'],'retained PR branch moved')
    for label,rev in [('local',local),('remote',main)]:
        git(phase+'_'+label+'_merge_ancestor','merge-base','--is-ancestor',PINS['accepted_merge'],rev)
    remote_commit=api(phase+'_current_main_commit','git/commits/'+main)
    local_tree=git(phase+'_current_remote_tree','rev-parse',main+'^{tree}').decode().strip()
    require(remote_commit['sha']==main and remote_commit['tree']['sha']==local_tree,'current main commit/tree API-local mismatch')
    remote_queue_map=scoped_map(phase+'_remote_queue_map',main,PINS['queue_path'])
    qblob=remote_queue_map[PINS['queue_path']]['blob']
    qb=api(phase+'_remote_queue_blob','git/blobs/'+qblob)
    require(qb['encoding']=='base64','queue blob encoding')
    q=base64.b64decode(qb['content'])
    require(qb['sha']==qblob and blobsha(q)==qblob and q==content(phase+'_remote_queue_local',main,PINS['queue_path']),'actual current queue readback mismatch')
    local_q=content(phase+'_local_queue',local,PINS['queue_path'])
    observation={'merged_at':pr['merged_at'],'merge_commit_sha':pr['merge_commit_sha'],'head':pr['head']['sha'],
        'body_sha256':sha(pr['body'].encode()),'state':pr['state'],'merged':pr['merged'],'api_base_sha_observed':pr['base']['sha'],
        'local_main':local,'remote_main':main,'remote_refs':refs,'current_remote_tree':local_tree,
        'remote_queue_sha256':sha(q),'local_queue_sha256':sha(local_q),'updated_at':pr['updated_at']}
    receipt['observations'][phase]=observation
    return {'local':local,'remote':main,'remote_queue':q,'local_queue':local_q,'pr':pr}

try:
    initial=merge_view('initial')
    ck('literal_initial_actual_merge_readback',True,receipt['observations']['initial'])
    ck('checkout_main',git('checkout_branch','branch','--show-current').decode().strip()=='main')
    origin=git('origin','remote','get-url','origin').decode().strip()
    ck('origin_repository_binding',origin in ['https://github.com/'+PINS['repository']+'.git','https://github.com/'+PINS['repository'],'git@github.com:'+PINS['repository']+'.git'])
    local_merge=json.loads(cmd('accepted_local_commit',['git','show','-s','--format={"sha":"%H","tree":"%T","parents":"%P"}',PINS['accepted_merge']]))
    ck('accepted_local_tree_ordered_parents',local_merge['sha']==PINS['accepted_merge'] and local_merge['tree']==PINS['accepted_tree'] and local_merge['parents'].split()==PINS['merge_parents'],local_merge)
    ac=api('accepted_api_commit','git/commits/'+PINS['accepted_merge'])
    ck('accepted_api_tree_ordered_parents',ac['sha']==PINS['accepted_merge'] and ac['tree']['sha']==PINS['accepted_tree'] and [e['sha'] for e in ac['parents']]==PINS['merge_parents'])
    repaired_tree=git('repaired_tree','rev-parse',PINS['head']+'^{tree}').decode().strip()
    ck('accepted_entire_tree_equals_reviewed_repaired_tree',repaired_tree==PINS['accepted_tree'])
    accepted=scoped_map('accepted_19_recursive_map',PINS['accepted_merge'],TARGET,PINS['queue_path'])
    repaired=scoped_map('repaired_19_recursive_map',PINS['head'],TARGET,PINS['queue_path'])
    ck('full_exact19_recursive_paths_modes_blobs',len(accepted)==19 and accepted==repaired and all(e['kind']=='blob' and e['mode']=='100644' for e in accepted.values()),accepted)
    local_blobs={p:content('accepted_blob_'+str(i),PINS['accepted_merge'],p) for i,p in enumerate(sorted(accepted))}
    for p,b in local_blobs.items(): ck('actual_local_blob_'+p,blobsha(b)==accepted[p]['blob'])
    def remote_blob(task):
        i,p=task
        data=api('accepted_remote_blob_'+str(i),'git/blobs/'+accepted[p]['blob'])
        require(data['encoding']=='base64','unexpected actual blob encoding')
        b=base64.b64decode(data['content'])
        return {'path':p,'pass':data['sha']==accepted[p]['blob'] and b==local_blobs[p],
                'bytes':len(b),'sha256':sha(b),'mode':accepted[p]['mode'],'blob':accepted[p]['blob']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rb=list(pool.map(remote_blob,enumerate(sorted(accepted))))
    ck('actual_remote_all19_complete_bytes',all(e['pass'] for e in rb),rb)
    queue=local_blobs[PINS['queue_path']]
    base_queue=content('accepted_parent_queue',PINS['base'],PINS['queue_path'])
    prior_queue=content('original_prior_current_queue',PINS['prior_current_main'],PINS['queue_path'])
    ck('full_frozen_prior_current_queue_equals_merge_parent',base_queue==prior_queue and sha(prior_queue)==PINS['prior_current_queue_sha256'])
    lines=base_queue.splitlines(keepends=True);i=PINS['queue_line']-1;cells=lines[i].decode().split('|')
    ck('original_own_physical_queue_cells',len(cells)==14 and '30004811 / OWR-8415343-014' in cells[2] and cells[8].strip()=='queued' and cells[9].strip()=='0/5')
    cells[8]=' already_solved ';cells[9]=' 1/5 ';lines[i]='|'.join(cells).encode()
    ck('full_accepted_queue_only_line410_cells8_9',queue==b''.join(lines) and sha(queue)==PINS['repaired_queue_sha256'],{'queue_sha256':sha(queue),'bytes':len(queue),'line':410,'cells':[8,9],'status':'already_solved','turns':'1/5'})
    ck('initial_new_main_queue_dispositions_preserved',True,{'remote_changes':preserves(queue,initial['remote_queue']),'local_changes':preserves(queue,initial['local_queue'])})
    bad=queue.replace(b'| already_solved | 1/5 |',b'| queued | 0/5 |',1)
    try: preserves(queue,bad)
    except ValueError: rejected=True
    else: rejected=False
    ck('negative_queue_rollback_rejected',rejected)
    short={p[len(TARGET)+1:]:b for p,b in local_blobs.items() if p.startswith(TARGET+'/')}
    parsed={p:json.loads(b) for p,b in short.items() if p.endswith('.json')}
    ck('seven_candidate_json_complete_parsed',len(parsed)==7,parsed)
    binding=[]
    for mf,prefix in [('FINAL_AUTHOR_MANIFEST.json',''),('PUBLICATION_MANIFEST.json',''),('review/REVIEW_MANIFEST.json','review/')]:
        for e in parsed[mf]['files']:
            b=short[prefix+e['path']];binding.append({'manifest':mf,'path':prefix+e['path'],'pass':len(b)==e['bytes'] and sha(b)==e['sha256']})
    ck('29_nested_binding_actual_postmerge',len(binding)==29 and all(e['pass'] for e in binding),binding)
    ck('review_author_binding',parsed['review/REVIEW_MANIFEST.json']['author_manifest_sha256']==sha(short['FINAL_AUTHOR_MANIFEST.json']))
    ck('exact_17_nonself_publication_paths',sorted(e['path'] for e in parsed['PUBLICATION_MANIFEST.json']['files'])==sorted(p for p in short if p!='PUBLICATION_MANIFEST.json'))
    original=scoped_map('original_18_target_map',PINS['original_head'],TARGET)
    ck('all18_unchanged_from_original_frozen_publication',original=={p:e for p,e in accepted.items() if p.startswith(TARGET+'/')})
    for i,e in enumerate(parsed['FINAL_AUTHOR_MANIFEST.json']['files']+[{'path':'FINAL_AUTHOR_MANIFEST.json'}]):
        p=e['path'];ck('ten_author_parent_'+p,content('author_parent_'+str(i),PINS['author_parent'],TARGET+'/'+p)==short[p])
    author_map=scoped_map('author_original_tree',PINS['author_parent'],TARGET)
    rp=['review/'+e['path'] for e in parsed['review/REVIEW_MANIFEST.json']['files']]+['review/REVIEW_MANIFEST.json']
    ck('historical_review_exact_provenance',len(rp)==4 and all(TARGET+'/'+p not in author_map for p in rp),{'earlier_author_parent_git_anchor':False,'binding':'original frozen publication, repaired publication, actual merge and nested manifests'})
    family_paths=[];family_records=[];total_seals=0
    for family,fp in PINS['families'].items():
        mp=fp['manifest_path'];mb=content('family_'+family+'_manifest',PINS['accepted_merge'],mp)
        ck('original_published_manifest_'+family,sha(mb)==fp['manifest_sha256'] and (REPO/mp).read_bytes()==mb)
        mf=json.loads(mb);parent=str(Path(mp).parent);family_paths.append(mp);seals=[]
        for i,e in enumerate(mf['files']):
            path=parent+'/'+e['path'];family_paths.append(path)
            b=content('family_'+family+'_'+str(i),PINS['accepted_merge'],path)
            ck('family51_actual_'+family+'/'+e['path'],len(b)==e['bytes'] and sha(b)==e['sha256'] and (REPO/path).read_bytes()==b)
            if 'SEAL' in e['path']:
                sd=json.loads(b);links=sd['files'].items() if isinstance(sd.get('files'),dict) else [(sd.get('artifact',sd.get('file')),sd['sha256'])]
                for j,(rel,h) in enumerate(links): ck('original_seal_'+family+'/'+e['path']+'/'+rel,sha(content('seal_'+family+'_'+str(i)+'_'+str(j),PINS['accepted_merge'],parent+'/'+rel))==h)
                seals.append(e['path']);total_seals+=1
        family_records.append({'family':family,'files':len(mf['files']),'seals':seals,'manifest_sha256':sha(mb)})
    ck('three_original_families_51_files_7_seals',sum(e['files'] for e in family_records)==51 and total_seals==7,family_records)
    accepted_proofs=scoped_map('accepted_scoped_published_proof_map',PINS['accepted_merge'],*[str(Path(x['manifest_path']).parent) for x in PINS['families'].values()])
    fm_path=REPO/PINS['final_live_manifest_path'];fm_bytes=fm_path.read_bytes()
    ck('nine_bound_final_live_manifest_preserved',sha(fm_bytes)==PINS['final_live_manifest_sha256'])
    fm=json.loads(fm_bytes)
    ck('nine_final_live_allowlist_count',len(fm['files'])==9 and all(e['path']!='PUBLIC_MANIFEST.json' and not e['path'].startswith('private/') for e in fm['files']))
    for e in fm['files']:
        b=(fm_path.parent/e['path']).read_bytes();ck('final_live9_'+e['path'],len(b)==e['bytes'] and sha(b)==e['sha256'])
        if e['path']=='FINAL_LIVE_SEAL.json':
            sd=json.loads(b)
            for rel,h in sd['files'].items(): ck('final_live_seal_'+rel,sha((fm_path.parent/rel).read_bytes())==h)
    for phase,view in [('initial',initial),('final',merge_view('final'))]:
        for which in ['local','remote']:
            rev=view[which]
            cmap=scoped_map(phase+'_'+which+'_current_19_map',rev,TARGET,PINS['queue_path'])
            ck(phase+'_'+which+'_accepted18_paths_modes_blobs_preserved',{p:e for p,e in cmap.items() if p.startswith(TARGET+'/')}=={p:e for p,e in accepted.items() if p.startswith(TARGET+'/')})
            ck(phase+'_'+which+'_current_queue_regular_mode_preserved',cmap[PINS['queue_path']]['kind']=='blob' and cmap[PINS['queue_path']]['mode']=='100644')
            protected=scoped_map(phase+'_'+which+'_current_published_family_map',rev,*[str(Path(x['manifest_path']).parent) for x in PINS['families'].values()])
            ck(phase+'_'+which+'_original51_and_manifests_preserved',all(protected.get(p)==accepted_proofs[p] for p in family_paths))
            ck(phase+'_'+which+'_queue_preserved',True,preserves(queue,view[which+'_queue']))
        if phase=='final':
            ck('new_dispositions_preserved_between_start_end',True,{'local':preserves(initial['local_queue'],view['local_queue']),'remote':preserves(initial['remote_queue'],view['remote_queue'])})
    ck('no_pdf_or_proof_replay_needed_unchanged18',True,{'basis':'exact original/repaired/actual/current target map identities, prior sealed source-first proof and complete replays; no new mathematical claims'})
    receipt['status']='PASS_ACTUAL_POST_MERGE_QUALIFIED'
    receipt['limitations']=['Only the credited original-class equality and separately qualified negative-curvature all-AF counterexample are accepted; no novelty or exact global mCV certification.',
       'Current main may advance only as an accepted-merge descendant; target artifacts and original published proofs remain identical and accepted queue rows cannot be rolled back.',
       'The nine final_live artifacts are checked as immutable sealed local artifacts; Git publication of them is not inferred. Root extra replay receipts lie outside that nine-file allowlist.',
       'Remote current-main objects must be locally available to verify ancestry/maps; this read-only gate never fetches missing objects.',
       'No DOI/paper/release or CI-success assertion. Raw streams stay ignored/private and are losslessly compressed; labels never overwrite prior observations.']
except Exception as exc:
    receipt['status']='REJECTED';receipt['failure']=repr(exc)
    (RUN/'failure.stderr.gz').write_bytes(gzip.compress(traceback.format_exc().encode(),mtime=0))
finally:
    receipt['completed_utc']=utc();receipt['private_run_relative']=str(RUN.relative_to(HERE))
    out=HERE/('RECEIPT_'+args.label+'.json');require(not out.exists(),'existing receipt')
    out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':receipt['status'],'receipt':str(out),'checks':len(receipt['checks']),'failure':receipt.get('failure')},indent=2))
if receipt['status']!='PASS_ACTUAL_POST_MERGE_QUALIFIED': sys.exit(1)
