#!/usr/bin/env python3
"""Read-only live Git/API/queue/body gate. All writes are confined to --own.

The input root and output own are deliberately separate. No Git mutation, fetch,
merge, service write, publication or external communication is performed.
"""
import argparse,base64,concurrent.futures,datetime,hashlib,json,pathlib,re,subprocess,sys

ORIGINAL='c683fc4b84266a6a153c087e182cf427ed502d6c'
ORIGINAL_BASE='efd29c05204703acca9a0860812f54b94fae54b1'
WIP='e27668a5dd99e38705ec6a97d15710b7eb1b0f41'
HEAD='26df33899c95d860403ab311c568e0328bc87eeb'
PARENT='ceada39994b1cd2c4935709143b53e2f7a581a45'
TREE='7d3b187011047ab8944dc2fdb8bf940c2110ce2c'
PREFIX='problems/30005116_induced_four_cycle_profile'
QUEUE='unsolved_math_prioritization/QUEUE.md'
REPO='AlecKriebel/Math'
BRANCH='math/30005116-induced-four-cycle-wip'
PREPARED_SHA='662fbbeac83e2709a4374f540da4eebf137f5ef4240f1cb820b23814d1cb6b0f'
MERGE_BODY_SHA='d05c7698cd384c8fc7f1431b420e9d871e2e6552277fd2a3066c5f497f7c0771'

def sha(b):return hashlib.sha256(b).hexdigest()
def blobsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def canonical_tree_sha(mapping):
    root={}
    for path,(mode,oid) in mapping.items():
        parts=path.split('/');node=root
        for component in parts[:-1]:node=node.setdefault(component,{})
        assert parts[-1] not in node
        node[parts[-1]]=(mode,oid)
    def digest(node):
        entries=[]
        for name,value in node.items():
            if isinstance(value,dict):mode,oid='40000',digest(value);key=name.encode()+b'/'
            else:mode,oid=value;key=name.encode()
            entries.append((key,mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(oid)))
        raw=b''.join(value for _,value in sorted(entries))
        return hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    return digest(root)
def main():
    global HEAD,PARENT,TREE,PREPARED_SHA
    parser=argparse.ArgumentParser();parser.add_argument('--inputs',required=True);parser.add_argument('--own',required=True)
    parser.add_argument('--git',default='/Users/alec/Documents/Math')
    parser.add_argument('--source-dir',required=True)
    parser.add_argument('--stage-descriptor',required=True)
    parser.add_argument('--stage-descriptor-sha256',required=True)
    parser.add_argument('--stage-input',action='append',required=True)
    parser.add_argument('--require-exact-api-body','--require-exact-API-body',action='store_true')
    parser.add_argument('--require-ready',action='store_true')
    args=parser.parse_args();inputs=pathlib.Path(args.inputs);own=pathlib.Path(args.own);private=own/'private'/'final_gate';private.mkdir(parents=True,exist_ok=True)
    records=[]
    def command(label,argv):
        result=subprocess.run(argv,cwd=args.git,capture_output=True)
        (private/(label+'.stdout')).write_bytes(result.stdout);(private/(label+'.stderr')).write_bytes(result.stderr)
        records.append({'label':label,'exit':result.returncode,'stdout_sha256':sha(result.stdout),'stdout_bytes':len(result.stdout),'stderr_sha256':sha(result.stderr),'stderr_bytes':len(result.stderr)})
        assert result.returncode==0,(label,result.stderr.decode(errors='replace'))
        assert not result.stderr,(label,'unexpected stderr')
        return result.stdout
    def git(label,*argv):return command(label,['git',*argv])
    def api(label,path):return json.loads(command(label,['gh','api','repos/'+REPO+'/'+path]))
    def getblob(commit,path):return git('blob_'+commit[:12]+'_'+hashlib.sha1(path.encode()).hexdigest()[:10],'show',commit+':'+path)
    def treemap(commit,label):
        raw=git(label,'ls-tree','-r','-z',commit);out={}
        for item in raw.split(b'\0'):
            if not item:continue
            metadata,name=item.split(b'\t',1);mode,kind,oid=metadata.decode().split();assert kind=='blob'
            out[name.decode()]=(mode,oid)
        return out
    def check_commit(commit,expected_parents=None,expected_tree=None):
        local=git('commit_'+commit[:12],'cat-file','-p',commit);headers=local.split(b'\n\n',1)[0].decode().splitlines()
        tree=next(line[5:] for line in headers if line.startswith('tree '));parents=[line[7:] for line in headers if line.startswith('parent ')]
        remote=api('api_commit_'+commit[:12],'git/commits/'+commit)
        assert remote['sha']==commit and remote['tree']['sha']==tree and [p['sha'] for p in remote['parents']]==parents
        if expected_parents is not None:assert parents==expected_parents
        if expected_tree is not None:assert tree==expected_tree
        return {'sha':commit,'tree':tree,'parents':parents}
    descriptor_bytes=pathlib.Path(args.stage_descriptor).read_bytes()
    assert sha(descriptor_bytes)==args.stage_descriptor_sha256
    descriptor=json.loads(descriptor_bytes)
    assert descriptor['schema']==1 and descriptor['pr']==374
    assert descriptor['immutable_original_gate_sha256']=='2b613efcc4d41616277c7fd259d1357dbcc69e0aeb4d330efb9618167442a2de'
    stages=descriptor['stages'];assert stages and len({s['name'] for s in stages})==len(stages)
    first=stages[0]
    assert (first['head'],first['parent'],first['tree'],first['input_metadata_sha256']['accepted_pr_body.txt'])==(HEAD,PARENT,TREE,PREPARED_SHA)
    stage_roots={}
    for value in args.stage_input:
        name,separator,path=value.partition('=');assert separator and name and path and name not in stage_roots
        stage_roots[name]=pathlib.Path(path)
    assert set(stage_roots)=={s['name'] for s in stages}
    input_names={'snapshot_manifest.json','repaired_snapshot_manifest.json','queue_repair_receipt.json','accepted_pr_body.txt','merge_body.txt'}
    for s in stages:
        assert set(s['input_metadata_sha256'])==input_names
        assert s['input_metadata_sha256']['snapshot_manifest.json']=='989de56033f3d980c2a1f8f79829ebab74f57580af2e283a73b9462deb244612'
        assert s['input_metadata_sha256']['merge_body.txt']==MERGE_BODY_SHA
        root=stage_roots[s['name']]
        for name,digest in s['input_metadata_sha256'].items():assert sha((root/name).read_bytes())==digest
    current=stages[-1];assert inputs==stage_roots[current['name']]
    previous_head=ORIGINAL if len(stages)==1 else stages[-2]['head']
    HEAD,PARENT,TREE,PREPARED_SHA=current['head'],current['parent'],current['tree'],current['input_metadata_sha256']['accepted_pr_body.txt']
    original_manifest=json.loads((inputs/'snapshot_manifest.json').read_bytes())
    refreshed_manifest=json.loads((inputs/'repaired_snapshot_manifest.json').read_bytes())
    repair=json.loads((inputs/'queue_repair_receipt.json').read_bytes())
    assert original_manifest['head']==ORIGINAL and original_manifest['base']==ORIGINAL_BASE
    assert refreshed_manifest['head']==HEAD and refreshed_manifest['base']==PARENT
    assert repair['parents']==[previous_head,PARENT] and repair['tree']==TREE
    assert len(original_manifest['files'])==len(refreshed_manifest['files'])==46
    oldrows={f['path']:f for f in original_manifest['files']};newrows={f['path']:f for f in refreshed_manifest['files']}
    assert set(oldrows)==set(newrows)
    assert set(oldrows)==set(git('original_changed_paths','diff','--name-only',ORIGINAL_BASE,ORIGINAL).decode().splitlines())
    assert set(newrows)==set(git('refreshed_changed_paths','diff','--name-only',PARENT,HEAD).decode().splitlines())
    original_tree=treemap(ORIGINAL,'original_tree');refreshed_tree=treemap(HEAD,'refreshed_tree')
    assert canonical_tree_sha(refreshed_tree)==TREE
    targetpaths={path for path in oldrows if path.startswith(PREFIX+'/')};assert len(targetpaths)==45
    assert {p for p in original_tree if p.startswith(PREFIX+'/')}==targetpaths
    assert {p for p in refreshed_tree if p.startswith(PREFIX+'/')}==targetpaths
    assert all(path.endswith(('.md','.json','.py')) and '/sources/' not in path and 'WORKING_AUDIT' not in path for path in targetpaths)
    blob_expectations={}
    for path in sorted(oldrows):
        frozen=(inputs/'snapshot'/path).read_bytes();updated=(inputs/'repaired_snapshot'/path).read_bytes()
        f=oldrows[path];g=newrows[path]
        assert (len(frozen),sha(frozen),blobsha(frozen))==(f['bytes'],f['sha256'],f['git_blob_sha'])
        assert (len(updated),sha(updated))==(g['bytes'],g['sha256'])
        assert getblob(ORIGINAL,path)==frozen and getblob(HEAD,path)==updated
        assert original_tree[path][1]==blobsha(frozen) and refreshed_tree[path][1]==blobsha(updated)
        if path in targetpaths:assert frozen==updated
        blob_expectations[blobsha(frozen)]=frozen;blob_expectations[blobsha(updated)]=updated
    original_and_current_unique_API_blobs=len(blob_expectations)
    assert original_and_current_unique_API_blobs==descriptor['original_and_current_unique_API_blobs']
    historical_commits=[];stage_maps=[];stage_repairs=[];last_head=ORIGINAL
    for s in stages:
        root=stage_roots[s['name']]
        mf=json.loads((root/'repaired_snapshot_manifest.json').read_bytes());rr=json.loads((root/'queue_repair_receipt.json').read_bytes())
        assert mf['head']==s['head'] and mf['base']==s['parent']
        assert rr['parents']==[last_head,s['parent']] and rr['tree']==s['tree']
        rows={f['path']:f for f in mf['files']};assert len(mf['files'])==len(rows)==46 and set(rows)==set(newrows)
        assert set(git('stage_changed_paths_'+s['name'],'diff','--name-only',s['parent'],s['head']).decode().splitlines())==set(newrows)
        st=treemap(s['head'],'stage_head_tree_'+s['name']);parent=treemap(s['parent'],'stage_parent_tree_'+s['name'])
        assert canonical_tree_sha(st)==s['tree'] and {p for p in st if p.startswith(PREFIX+'/')}==targetpaths
        expected=dict(parent)
        for path in targetpaths|{QUEUE}:expected[path]=st[path]
        assert expected==st,'stage changed an unrelated parent path or mode'
        for path in sorted(rows):
            data=(root/'repaired_snapshot'/path).read_bytes();f=rows[path]
            assert (len(data),sha(data))==(f['bytes'],f['sha256'])
            assert blobsha(data)==st[path][1] and getblob(s['head'],path)==data
            if 'git_blob_sha' in f:assert f['git_blob_sha']==st[path][1]
            if path in targetpaths:assert data==(inputs/'snapshot'/path).read_bytes() and st[path]==original_tree[path]
            blob_expectations[blobsha(data)]=data
        body=(root/'accepted_pr_body.txt').read_bytes();text=body.decode()
        assert sha(body)==s['input_metadata_sha256']['accepted_pr_body.txt']
        assert 'unsolved, 5/5' in text and 'None supplies the missing all-host comparison' in text and 'No novelty certification' in text
        assert s['head'] in text and s['parent'] in text and ORIGINAL in text and WIP in text
        historical_commits.extend([check_commit(s['head'],[last_head,s['parent']],s['tree']),check_commit(s['parent'])])
        stage_maps.append({'name':s['name'],'head':s['head'],'parent':s['parent'],'tree':s['tree'],'prepared_body_sha256':sha(body),'scope_paths':46,'unchanged_target_files':45,'all_other_parent_paths_and_modes_preserved':True})
        stage_repairs.append(rr);last_head=s['head']
    assert len(blob_expectations)==descriptor['all_stage_unique_API_blobs']
    # Fetch every unique immutable remote blob independently. Raw copied bytes remain private.
    def remote_blob(item):
        oid,expected=item;obj=api('api_blob_'+oid,'git/blobs/'+oid);assert obj['sha']==oid and obj['encoding']=='base64'
        actual=base64.b64decode(obj['content']);assert actual==expected and blobsha(actual)==oid
        return {'git_blob_sha1':oid,'bytes':len(actual),'sha256':sha(actual)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:api_blobs=list(pool.map(remote_blob,sorted(blob_expectations.items())))
    packet=inputs/'snapshot'/PREFIX
    def manifest(name,root):
        obj=json.loads((root/name).read_bytes());seen=[]
        for f in obj['files']:
            b=(root/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
            if 'git_blob_sha1' in f:assert blobsha(b)==f['git_blob_sha1']
            seen.append(f['path'])
        assert len(seen)==len(set(seen));return obj,seen
    author,author_entries=manifest('FINAL_AUTHOR_MANIFEST.json',packet);author36=set(author_entries)|{'FINAL_AUTHOR_MANIFEST.json'};assert len(author36)==36
    scope=json.loads((packet/'FINAL_PUBLIC_SCOPE.json').read_bytes());assert set(scope['files'])==author36
    wip_tree=treemap(WIP,'wip_tree');assert {p for p in wip_tree if p.startswith(PREFIX+'/')}=={PREFIX+'/'+p for p in author36}
    for name in sorted(author36):assert getblob(WIP,PREFIX+'/'+name)==(packet/name).read_bytes()
    review,review_entries=manifest('REVIEW_MANIFEST.json',packet/'independent_review');review6={'independent_review/'+p for p in review_entries}|{'independent_review/REVIEW_MANIFEST.json'};assert len(review6)==6
    publication,pub_entries=manifest('PUBLICATION_MANIFEST.json',packet);assert set(pub_entries)|{'PUBLICATION_MANIFEST.json'}=={p[len(PREFIX)+1:] for p in targetpaths}
    assert publication['author_files']==36 and publication['review_files']==6 and publication['author_parent']==WIP and publication['integration_main']==ORIGINAL_BASE
    history=0;previous=None
    for i in range(1,6):
        name=f'TURN_{i}_MANIFEST.json';obj,entries=manifest(name,packet);assert obj['turn']==i
        if previous is not None:assert obj['previous_manifest_sha256']==previous
        previous=sha((packet/name).read_bytes());history+=len(entries)
    assert history==25
    # Source bytes checked freshly: all five primary PDFs. Historical derivative hashes are
    # provenance records, not silently represented as freshly reproduced render/HTML bytes.
    source_records=[]
    for name in ['SOURCE_HASHES.json','SOURCE_ADDENDUM_TURN_2.json','SOURCE_ADDENDUM_TURN_4.json']:source_records+=json.loads((packet/name).read_bytes())['files']
    assert len(source_records)==15
    source_names={'owr':'sources/owr2022-22.pdf','lmr':'sources/lmr-feasible.pdf','pr':'sources/pikhurko-razborov2017.pdf','semi2026':'sources/semi2026.pdf','cograph':'sources/cograph-terminology2024.pdf'}
    actual_pdf=[]
    for name,record_name in source_names.items():
        f=next(f for f in source_records if f['path']==record_name);b=(pathlib.Path(args.source_dir)/(name+'.pdf')).read_bytes()
        assert len(b)==f['bytes'] and sha(b)==f['sha256'];actual_pdf.append({'name':name,'bytes':len(b),'sha256':sha(b)})
    # Queue checks compare complete bytes, retaining every unselected cell and row exactly.
    def queue_delta(base,head,label):
        before=getblob(base,QUEUE);after=getblob(head,QUEUE);lines=before.splitlines(keepends=True)
        selected=[i for i,line in enumerate(lines) if b'| 30005116 / OWR-10252930-028 |' in line];assert selected==[410]
        old=lines[410];cells=old.split(b'|');assert cells[1].strip()==b'400' and cells[8]==b' queued ' and cells[9]==b' 0/5 '
        cells[8]=b' unsolved ';cells[9]=b' 5/5 ';new=b'|'.join(cells);lines[410]=new;expected=b''.join(lines)
        assert after==expected,(label,'nonselected queue byte changed')
        return {'label':label,'base_sha256':sha(before),'head_sha256':sha(after),'line':411,'rank':400,'only_pipe_cells':[8,9],'old_row':old.decode(),'new_row':new.decode(),'all_other_bytes_identical':True}
    queue_original=queue_delta(ORIGINAL_BASE,ORIGINAL,'original')
    queue_stages=[]
    for s,rr in zip(stages,stage_repairs):
        delta=queue_delta(s['parent'],s['head'],s['name'])
        assert delta['old_row']==rr['old_row'] and delta['new_row']==rr['new_row']
        queue_stages.append(delta)
    queue_refreshed=queue_delta(PARENT,HEAD,'refreshed')
    assert queue_refreshed['old_row']==repair['old_row'] and queue_refreshed['new_row']==repair['new_row']
    prepared=(inputs/'accepted_pr_body.txt').read_bytes();merge_body=(inputs/'merge_body.txt').read_bytes()
    assert sha(prepared)==PREPARED_SHA and sha(merge_body)==MERGE_BODY_SHA
    text=prepared.decode();assert 'unsolved, 5/5' in text and 'None supplies the missing all-host comparison' in text and 'No novelty certification' in text
    assert HEAD in text and ORIGINAL in text and WIP in text and PARENT in text
    assert TREE in text
    for s in stages:assert s['head'] in text and s['parent'] in text
    # Actual objects and live identities, never just task labels or planned operations.
    commits=[check_commit(ORIGINAL),check_commit(ORIGINAL_BASE),check_commit(WIP),*historical_commits]
    pr=api('pr_live','pulls/374');remote_main=api('main_ref','git/ref/heads/main');remote_head=api('head_ref','git/ref/heads/'+BRANCH)
    current_main=remote_main['object']['sha'];assert remote_head['object']['sha']==HEAD
    assert pr['head']['sha']==HEAD and pr['head']['ref']==BRANCH and pr['head']['repo']['full_name']==REPO
    assert pr['base']['ref']=='main' and pr['base']['repo']['full_name']==REPO and pr['state']=='open' and not pr['merged']
    assert pr['mergeable'] is True and pr['mergeable_state']=='clean'
    # A later main audit publication may advance the ref without changing this target or queue.
    git('main_descends_parent','merge-base','--is-ancestor',PARENT,current_main)
    laterpaths=git('main_advance_paths','diff','--name-only',PARENT,current_main).decode().splitlines()
    assert not any(p==QUEUE or p.startswith(PREFIX+'/') for p in laterpaths),'main target or queue drift; refreshed head required'
    assert getblob(current_main,QUEUE)==getblob(PARENT,QUEUE)
    current_main_commit=check_commit(current_main)
    current_main_map=treemap(current_main,'current_main_complete_tree')
    assert canonical_tree_sha(current_main_map)==current_main_commit['tree']
    current_expected=dict(current_main_map)
    for path in targetpaths|{QUEUE}:current_expected[path]=refreshed_tree[path]
    actual_scope={p for p in set(current_main_map)|set(current_expected) if current_main_map.get(p)!=current_expected.get(p)}
    assert actual_scope==targetpaths|{QUEUE}
    merge_base=git('actual_merge_base','merge-base',current_main,HEAD).decode().strip();assert merge_base==PARENT
    # Legacy three-tree mode computes a textual merge without writing a Git object.
    legacy=git('actual_readonly_merge_tree','merge-tree',merge_base,current_main,HEAD).decode()
    assert '<<<<<<<' not in legacy and 'CONFLICT' not in legacy
    metadata=re.findall(r'^  (?:result|our|their)\s+([0-9]{6}) ([0-9a-f]{40}) (.+)$',legacy,re.M)
    assert {path for _,_,path in metadata}==actual_scope
    results={path:(mode,oid) for mode,oid,path in re.findall(r'^  result\s+([0-9]{6}) ([0-9a-f]{40}) (.+)$',legacy,re.M)}
    incoming={path:(mode,oid) for mode,oid,path in re.findall(r'^  their\s+([0-9]{6}) ([0-9a-f]{40}) (.+)$',legacy,re.M)}
    for path in actual_scope-set(results):
        assert path not in current_main_map and path in incoming
        results[path]=incoming[path]
    assert set(results)==actual_scope
    for path in actual_scope:assert results[path]==current_expected[path]
    current_expected_tree=canonical_tree_sha(current_expected)
    api_base=pr['base']['sha'];assert api_base in (PARENT,current_main),'unrecognized live API base'
    observed_body=pr['body'].encode();observed_body_sha=sha(observed_body)
    (private/'observed_api_body.txt').write_bytes(observed_body)
    if args.require_exact_api_body:assert observed_body==prepared,'prepared acceptance body is not exactly live'
    if args.require_ready:assert pr['draft'] is False,'PR is still draft'
    # Compare complete GitHub test merge tree to an independently constructed read-only map.
    # No git merge-tree --write-tree or other object mutation is needed.
    merge_sha=pr['merge_commit_sha'];assert merge_sha
    merge_commit=api('test_merge_commit','git/commits/'+merge_sha)
    assert [p['sha'] for p in merge_commit['parents']]==[api_base,HEAD]
    expected=treemap(api_base,'api_base_tree');head_tree=treemap(HEAD,'head_tree_complete')
    for p in targetpaths|{QUEUE}:expected[p]=head_tree[p]
    expected_tree=canonical_tree_sha(expected)
    assert merge_commit['tree']['sha']==expected_tree,'test merge lost or changed an unrelated path'
    if args.require_exact_api_body or args.require_ready:assert api_base==current_main,'API/test merge base stale against actual remote main'
    final_pr=api('pr_final','pulls/374');final_main=api('main_ref_final','git/ref/heads/main');final_head=api('head_ref_final','git/ref/heads/'+BRANCH)
    for key in ('state','draft','body','merge_commit_sha'):assert final_pr[key]==pr[key]
    assert final_pr['head']['sha']==HEAD and final_pr['base']['sha']==api_base
    assert final_main['object']['sha']==current_main and final_head['object']['sha']==HEAD
    output={'status':'PASS','phase':'exact_live_acceptance' if args.require_exact_api_body else 'prepared_acceptance','head':HEAD,'original_head':ORIGINAL,'previous_reviewed_head':previous_head,'refresh_stages':stage_maps,'normal_refresh_every_other_parent_path_preserved':True,'original_base':ORIGINAL_BASE,'author_wip':WIP,'refreshed_parent':PARENT,'refreshed_tree':TREE,'api_base':api_base,'remote_main':current_main,'api_body_sha256':observed_body_sha,'prepared_body_sha256':sha(prepared),'merge_body_sha256':sha(merge_body),'prepared_body_is_live':observed_body==prepared,'draft':pr['draft'],'mergeable':pr['mergeable'],'mergeable_state':pr['mergeable_state'],'test_merge_sha':merge_sha,'test_merge_tree':merge_commit['tree']['sha'],'complete_test_merge_tree_matches_its_API_base':True,'api_base_matches_remote_main':api_base==current_main,'actual_remote_main_readonly_merge_tree_matches':True,'actual_remote_main_expected_tree':current_expected_tree,'all_other_actual_remote_main_paths_preserved':True,'frozen_changed_paths':46,'unchanged_target_files':45,'author_wip_files':36,'old_review_files':6,'historical_manifest_entries':history,'historical_source_provenance_entries':15,'fresh_primary_PDF_matches':5,'unique_original_and_refreshed_API_blobs':original_and_current_unique_API_blobs,'unique_all_stage_API_blobs':len(api_blobs),'queue_original':queue_original,'queue_historical_stages':queue_stages,'queue_refreshed':queue_refreshed,'raw_source_paths_in_PR':0,'scope_leakage_paths':0,'unrestricted_status':'unsolved5/5','novelty_certification':False,'remaining_actions':[] if args.require_exact_api_body and args.require_ready else ['root independent reproduction','send exact prepared acceptance body','mark ready','rerun same gate with exact API body and ready requirements','merge only after root acceptance']}
    receipt={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':output,'input_metadata_sha256':{name:sha((inputs/name).read_bytes()) for name in ['snapshot_manifest.json','repaired_snapshot_manifest.json','queue_repair_receipt.json','accepted_pr_body.txt','merge_body.txt']},'stage_descriptor_sha256':sha(descriptor_bytes),'stage_input_metadata_sha256':{s['name']:s['input_metadata_sha256'] for s in stages},'immutable_original_gate_sha256':'2b613efcc4d41616277c7fd259d1357dbcc69e0aeb4d330efb9618167442a2de','commits':commits,'fresh_PDFs':actual_pdf,'api_blobs':api_blobs,'command_records':sorted(records,key=lambda r:r['label']),'volatile_receipt_fields':['observed_utc'],'full_stdout_and_whole_result_JSON_must_match_except_explicit_metadata_mutation':True}
    label='final_gate_live' if args.require_exact_api_body else 'final_gate_prepared'
    (own/'public'/(label+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(output,sort_keys=True))

if __name__=='__main__':main()
