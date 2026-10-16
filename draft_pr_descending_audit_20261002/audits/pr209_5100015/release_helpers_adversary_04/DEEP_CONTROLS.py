"""New bounded downstream attacks; candidate functions and source are unedited."""
from pathlib import Path
import copy, importlib, json, sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from REPRODUCE import rejected, result, write, pin
import REPRODUCE as harness
import release_binding as rb
import integrate_reviewed_pr as native
import verify_and_merge as m
CASE=HERE/'minimal_synthetic_case'
R,PUB=CASE/'preprint',CASE/'publication'
CTX=rb.context(R)
Z=rb.publication(R,PUB,CTX)
T=rb.tracker(R,PUB,CTX,Z)
AUTH=json.loads((HERE/'LEGITIMATE_AUTHORITY.json').read_text())
RECEIPT=AUTH['receipt']
DETAIL=[]

def validate(receipt):
    m.validate_completion_receipt(receipt,RECEIPT,R,PUB,CTX,Z,T,AUTH['release_utc'])

def mutate_observation(label,kind,member,change):
    """Change a child AND its self-consistent local pins/colocated record.

    This passes simple equality and pin checks to actually exercise semantic
    checks against independent publication/tracker/clearance facts.
    """
    bad=copy.deepcopy(RECEIPT)
    observation=bad['live_release_evidence'][kind]
    if kind=='publication':
        folder=CASE/Path(observation['inspect_readback']['path']).parent
        path=folder/'INSPECT_READBACK.json'
        pointer=observation['inspect_readback']
    else:
        folder=CASE/Path(observation['evidence']['properties']['path']).parent
        key={'properties':'properties','target':'target_readback','after':'after_scan'}[member]
        pointer=observation['evidence'][key]
        path=CASE/pointer['path']
    live=folder/'LIVE_VERIFIED.json'
    old,oldlive=path.read_bytes(),live.read_bytes()
    body=json.loads(old)
    change(body)
    try:
        write(path,body)
        pointer.update(pin(path,CASE))
        write(live,observation)
        error=rejected(lambda:validate(bad))
        DETAIL.append(dict(label=label,rejection=error,coherent_colocated_record_and_new_child_pin=True))
    finally:
        path.write_bytes(old)
        live.write_bytes(oldlive)
    validate(RECEIPT)

def history():
    mutate_observation('provider_wrong_title','publication','inspect',lambda v:v.update(title='Other theorem'))
    mutate_observation('provider_wrong_environment','publication','inspect',lambda v:v.update(environment='sandbox'))
    mutate_observation('provider_file_size_type_float','publication','inspect',lambda v:v['files'][0].update(size=float(v['files'][0]['size'])))
    mutate_observation('provider_wrong_version_doi','publication','inspect',lambda v:v.update(doi='10.5281/zenodo.99999'))
    mutate_observation('provider_DOI_resolves_wrong_record','publication','inspect',lambda v:v['doi_resolution'].update(resolved_url='https://zenodo.org/records/99999'))
    mutate_observation('provider_DOI_non_2xx','publication','inspect',lambda v:v['doi_resolution'].update(http_status=302))
    mutate_observation('tracker_wrong_gid','tracker','properties',lambda v:v['sheets'][0]['properties'].update(sheetId=999))
    mutate_observation('tracker_boolean_grid','tracker','properties',lambda v:v['sheets'][0]['properties']['gridProperties'].update(rowCount=True))
    mutate_observation('tracker_target_wrong_tab','tracker','target',lambda v:v['response'].update(range="'Wrong tab'!A2:D2"))
    mutate_observation('tracker_target_COLUMNN','tracker','target',lambda v:v['response'].update(majorDimension='COLUMNS'))
    mutate_observation('tracker_target_wrong_DOI','tracker','target',lambda v:v['response']['values'][0].__setitem__(2,'https://doi.org/10.5281/zenodo.99999'))
    mutate_observation('tracker_full_scan_truncated_range','tracker','after',lambda v:v['response'].update(range="'Math Puzzles'!A1:D1"))
    mutate_observation('tracker_full_scan_extra_duplicate','tracker','after',lambda v:v['response']['values'].append(copy.deepcopy(T['values'])))
    write(HERE/'COHERENT_HISTORY_ATTACKS.json',DETAIL)
    return dict(rejected_coherently_re_pinned_child_attacks=len(DETAIL),positive_restored_after_every_attack=True,provider_calls=0)

def final_native():
    accepted=RECEIPT
    head,merge=accepted['reviewed_head'],accepted['merge_commit']
    intent=dict(reviewed_head=head,parents=accepted['merge_parents'])
    objects=dict(head=merge,tree=accepted['verified_merge_tree'])
    metadata=native.expected_pr_metadata(Z,T)
    record=dict(number=209,state='closed',merged=True,draft=False,html_url=accepted['url'],merge_commit_sha=merge,
        head=dict(sha=head,ref=native.BRANCH,repo=dict(full_name='AlecKriebel/Math')),
        base=dict(ref='main',repo=dict(full_name='AlecKriebel/Math')),**metadata)
    valid={
        'pulls/209':record,
        'git/ref/heads/'+native.BRANCH:dict(object=dict(sha=head)),
        'git/commits/'+merge:dict(tree=dict(sha=objects['tree']),parents=[dict(sha=s) for s in intent['parents']]),
        'git/ref/heads/main':dict(object=dict(sha=merge)),
        'compare/'+merge+'...foreign-descendant':dict(status='ahead',merge_base_commit=dict(sha=merge))}
    def call(table):
        calls=[]
        def api(method,path,payload=None,**kw):
            assert method=='GET' and payload is None, 'Forbidden provider mutation'
            calls.append(path)
            return copy.deepcopy(table[path])
        answer=m.refresh_completion_native(api,intent,objects,Z,T)
        return answer,calls
    answer,calls=call(valid)
    assert answer==record and calls[-1]=='git/ref/heads/main'
    attacks=[]
    def attack(label,change):
        table=copy.deepcopy(valid);change(table)
        error=rejected(lambda:call(table))
        attacks.append(dict(label=label,rejection=error))
    attack('late_PR_body',lambda d:d['pulls/209'].update(body=metadata['body']+' '))
    attack('late_PR_title',lambda d:d['pulls/209'].update(title=metadata['title']+' '))
    attack('late_wrong_PR_event',lambda d:d['pulls/209'].update(merge_commit_sha='different-merge'))
    attack('late_merged_false',lambda d:d['pulls/209'].update(merged=False))
    attack('late_branch_ref',lambda d:d['git/ref/heads/'+native.BRANCH]['object'].update(sha='wrong-head'))
    attack('late_commit_parent',lambda d:d['git/commits/'+merge]['parents'][0].update(sha='wrong-parent'))
    attack('late_commit_tree',lambda d:d['git/commits/'+merge]['tree'].update(sha='wrong-tree'))
    advanced=copy.deepcopy(valid);advanced['git/ref/heads/main']['object']['sha']='foreign-descendant'
    assert call(advanced)[0]==record
    for label,change in [('noncontaining_current_main',lambda d:d['compare/'+merge+'...foreign-descendant'].update(status='diverged')),
        ('wrong_merge_base_current_main',lambda d:d['compare/'+merge+'...foreign-descendant']['merge_base_commit'].update(sha='other-base'))]:
        d=copy.deepcopy(advanced);change(d);attacks.append(dict(label=label,rejection=rejected(lambda:call(d))))
    write(HERE/'FINAL_NATIVE_ATTACKS.json',attacks)
    return dict(exact_merge_positive=True,foreign_descendant_positive=True,rejected_late_native_attacks=len(attacks),GET_only_synthetic_provider=True,source_sequence_inspected_separately=True)

def tracker_and_public():
    meta=dict(spreadsheetId=rb.SHEET,sheets=[dict(properties=dict(sheetId=rb.SHEET_ID,title='Math Puzzles',sheetType='GRID',gridProperties=dict(rowCount=1115,columnCount=43)))])
    rows=[rb.HEADER, T['values']]
    response=dict(request=dict(spreadsheetId=rb.SHEET,range=rb.FULL_RANGE),response=dict(range="'Math Puzzles'!A1:D1115",majorDimension='ROWS',values=rows))
    assert rb.tracker_readback(response,rb.FULL_RANGE,meta)==rows
    assert rb.require_unique_tracker(rows,T['values'],Z,2) is None
    bads=[]
    for key,value in [('range',"'Math Puzzles'!A1:D1114"),('range',"'Other'!A1:D1115"),('majorDimension','COLUMNS'),('range',"'Math Puzzles'!B1:E1115")]:
        x=copy.deepcopy(response);x['response'][key]=value;bads.append(rejected(lambda:rb.tracker_readback(x,rb.FULL_RANGE,meta)))
    x=copy.deepcopy(meta);x['sheets'].append(copy.deepcopy(x['sheets'][0]));bads.append(rejected(lambda:rb.tracker_readback(response,rb.FULL_RANGE,x)))
    bads.append(rejected(lambda:rb.require_unique_tracker(rows+[T['values']],T['values'],Z,2)))
    # Retained actual package is not released: absence of the real clearance is
    # an intentional fail-closed condition, while draft proposals cannot grant it.
    assert not (HERE.parent/'preprint/FINAL_CLEARANCE.json').exists()
    try:rb.context(HERE.parent/'preprint')
    except FileNotFoundError:pass
    else:raise AssertionError('Actual package unexpectedly granted release context')
    return dict(canonical_finite_grid_trimmed_values_positive=True,wrong_coverage_tab_dimension_grid_duplicate_rejected=len(bads),real_final_clearance_absent=True,draft_proposal_not_authority=True)

def native_tree_cap():
    # The complete recursive tree delta sees paths beyond the compare API's300
    # boundary. This fresh direct control uses tiny in-memory Git responses.
    def entry(i,after):
        return dict(path='file_%04d.txt'%i,mode='100644',type='blob',sha=('new' if after else 'old')+str(i))
    tables={'old':dict(truncated=False,tree=[entry(i,False) for i in range(305)]),
            'new':dict(truncated=False,tree=[entry(i,True) for i in range(305)])}
    calls=[]
    def api(method,path):
        assert method=='GET';calls.append(path);return tables[path.split('/')[-1]]
    trees=native.NativeTrees(api)
    delta=trees.difference('old','new')
    assert len(delta)==305 and 'file_0304.txt' in delta
    return dict(full_changed_paths=305,tail_path_detected=True,GET_calls=calls)

if __name__=='__main__':
    # Preserve the first completed program's results, then retain this separately.
    assert not (HERE/'DEEP_RESULTS.json').exists()
    harness.RESULTS=[]
    original_write=harness.write
    def separate_write(path,value):
        path=Path(path)
        if path==HERE/'RESULTS.json':path=HERE/'DEEP_RESULTS.json'
        original_write(path,value)
    harness.write=separate_write
    result('coherent_historical_child_and_pin_semantic_attacks',history)
    result('final_native_refresh_exact_and_foreign_descendant',final_native)
    result('tracker_and_actual_absent_clearance_boundary',tracker_and_public)
    result('complete_native_tree_delta_beyond300',native_tree_cap)
