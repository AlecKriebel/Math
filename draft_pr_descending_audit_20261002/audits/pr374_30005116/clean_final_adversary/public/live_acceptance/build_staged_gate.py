#!/usr/bin/env python3
"""Build a separately sealed metadata-stage gate from the immutable first gate."""
import ast,difflib,hashlib,json,pathlib
HERE=pathlib.Path(__file__).parent
ORIGINAL=HERE.parent/'controls'/'final_gate.py'
ORIGINAL_SHA='2b613efcc4d41616277c7fd259d1357dbcc69e0aeb4d330efb9618167442a2de'
ORIGINAL_MF='989de56033f3d980c2a1f8f79829ebab74f57580af2e283a73b9462deb244612'
MERGE_BODY='d05c7698cd384c8fc7f1431b420e9d871e2e6552277fd2a3066c5f497f7c0771'
def stage(name,head,parent,tree,manifest,repair,body):
    return {'name':name,'head':head,'parent':parent,'tree':tree,
            'input_metadata_sha256':{'snapshot_manifest.json':ORIGINAL_MF,'repaired_snapshot_manifest.json':manifest,
            'queue_repair_receipt.json':repair,'accepted_pr_body.txt':body,'merge_body.txt':MERGE_BODY}}
DESCRIPTOR={'schema':1,'pr':374,'immutable_original_gate_sha256':ORIGINAL_SHA,
 'original_and_current_unique_API_blobs':47,'all_stage_unique_API_blobs':48,
 'stages':[
 stage('initial','26df33899c95d860403ab311c568e0328bc87eeb','ceada39994b1cd2c4935709143b53e2f7a581a45','7d3b187011047ab8944dc2fdb8bf940c2110ce2c','3c10ad4c9cd3f636494a8234edbf0d05d4ffde967bfc4bbaabc6b9583580d8d3','b40773493c5ae91047af8e942dc3d5ed47904a59cbc8b380ba6ee94452cdfb55','662fbbeac83e2709a4374f540da4eebf137f5ef4240f1cb820b23814d1cb6b0f'),
 stage('round1','4afe89d1439e0d0d2a28a55f27709192cd56738e','8e04757bff6e5c6c25d2dbf23ce10f736da8c5c8','9b4c96e230fc3aecca24760e6804ea671d559ca4','e155b73d64556bf991513c4247af3e90d4631ea3085481cfe3d910529ccae42e','04523b4c9e55c83a5901d29b2a0c4c6b3dba21e8b5970ce06820398d98e3d5ea','0933d8a02e24cc2c441134fbf077108805537fe7370ce2b49a84e0b3a094a6ed'),
 stage('round2','2bb07868e8fb5ac48cae8ec0b7f69aed02b36807','eb3c6dbe6a1d978e39c30518137264bdc69ec30b','1464f6e71c9db2ab696db9e75373413267030156','fdc33848034bfb7f92cfaf54a3c124c82a4aa913564d4250eedf1ed79e160483','9ad7470c49bfd5c4287a2b319a3753ac1f0f82b6a2a72369338f07ef71c465cb','9ad5abe497cd57008059cd42d373fb4d4bfed716b4d2718805f8b3fb9a9335c5')],
 'historical_body_bindings_do_not_assert_which_body_is_currently_live':True}

SETUP='''    descriptor_bytes=pathlib.Path(args.stage_descriptor).read_bytes()
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
'''
STAGE_CHECKS='''    original_and_current_unique_API_blobs=len(blob_expectations)
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
'''
STAGE_QUEUES='''    queue_stages=[]
    for s,rr in zip(stages,stage_repairs):
        delta=queue_delta(s['parent'],s['head'],s['name'])
        assert delta['old_row']==rr['old_row'] and delta['new_row']==rr['new_row']
        queue_stages.append(delta)
'''

def main():
    original=ORIGINAL.read_text();assert hashlib.sha256(original.encode()).hexdigest()==ORIGINAL_SHA
    code=original;replacements=[]
    def replace(old,new,count=1):
        nonlocal code
        assert code.count(old)==count,(old,code.count(old),count)
        code=code.replace(old,new);replacements.append({'old':old,'new':new,'occurrences':count})
    replace('def main():\n','def main():\n    global HEAD,PARENT,TREE,PREPARED_SHA\n')
    replace("parser.add_argument('--source-dir',required=True)","parser.add_argument('--source-dir',required=True)\n    parser.add_argument('--stage-descriptor',required=True)\n    parser.add_argument('--stage-descriptor-sha256',required=True)\n    parser.add_argument('--stage-input',action='append',required=True)")
    replace('    original_manifest=json.loads',SETUP+'    original_manifest=json.loads')
    replace("repair['parents']==[ORIGINAL,PARENT]","repair['parents']==[previous_head,PARENT]")
    replace('    # Fetch every unique immutable remote blob independently.',STAGE_CHECKS+'    # Fetch every unique immutable remote blob independently.')
    replace("    queue_refreshed=queue_delta(PARENT,HEAD,'refreshed')",STAGE_QUEUES+"    queue_refreshed=queue_delta(PARENT,HEAD,'refreshed')")
    replace('    assert HEAD in text and ORIGINAL in text and WIP in text and PARENT in text','    assert HEAD in text and ORIGINAL in text and WIP in text and PARENT in text\n    assert TREE in text\n    for s in stages:assert s[\'head\'] in text and s[\'parent\'] in text')
    replace('check_commit(HEAD,[ORIGINAL,PARENT],TREE),check_commit(PARENT)','*historical_commits')
    replace("'original_head':ORIGINAL,'original_base':ORIGINAL_BASE","'original_head':ORIGINAL,'previous_reviewed_head':previous_head,'refresh_stages':stage_maps,'normal_refresh_every_other_parent_path_preserved':True,'original_base':ORIGINAL_BASE")
    replace("'unique_original_and_refreshed_API_blobs':len(api_blobs)","'unique_original_and_refreshed_API_blobs':original_and_current_unique_API_blobs,'unique_all_stage_API_blobs':len(api_blobs)")
    replace("'queue_original':queue_original,'queue_refreshed':queue_refreshed","'queue_original':queue_original,'queue_historical_stages':queue_stages,'queue_refreshed':queue_refreshed")
    replace("'commits':commits","'stage_descriptor_sha256':sha(descriptor_bytes),'stage_input_metadata_sha256':{s['name']:s['input_metadata_sha256'] for s in stages},'immutable_original_gate_sha256':'"+ORIGINAL_SHA+"','commits':commits")
    ast.parse(code)
    (HERE/'final_gate_staged.py').write_text(code)
    descriptor_bytes=(json.dumps(DESCRIPTOR,indent=2)+'\n').encode();(HERE/'ROUND2_STAGE_DESCRIPTOR.json').write_bytes(descriptor_bytes)
    diff=''.join(difflib.unified_diff(original.splitlines(keepends=True),code.splitlines(keepends=True),fromfile='immutable/public/controls/final_gate.py',tofile='additive/public/live_acceptance/final_gate_staged.py'))
    (HERE/'final_gate_staged.diff').write_text(diff)
    r={'immutable_original_gate_sha256':ORIGINAL_SHA,'staged_gate_sha256':hashlib.sha256(code.encode()).hexdigest(),'stage_descriptor_sha256':hashlib.sha256(descriptor_bytes).hexdigest(),'full_diff_sha256':hashlib.sha256(diff.encode()).hexdigest(),'literal_replacements':replacements,'all_initial_checks_retained':True,'all_three_stages_checked_independently':True,'original_and_round1_code_and_inputs_unmodified':True,'original_current_API_blob_count':47,'all_stage_API_blob_count':48,'count_difference_explanation':'The second native refresh carries independently changed other queue bytes, adding one prior-stage queue blob to the original/current union.'}
    (HERE/'staged_gate_adaptation_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['staged_gate_sha256','stage_descriptor_sha256','immutable_original_gate_sha256']},sort_keys=True))
if __name__=='__main__':main()
