"""New independent inventory/pin/claim-boundary verifier; read-only inputs.

No candidate/preparer/sibling verifier is imported or executed. No provider,
network or Git call occurs. Stored old actual replay outputs are compared in
full rather than relabelled as new executions. Only this review folder is written.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from urllib.parse import urlsplit, unquote
import ast, copy, hashlib, json, re

W=Path(__file__).resolve().parent
B=W.parent
E=B/'final_findings_export_preparation_01/durable_facing_v02'
C=B/'final_findings_export_preparation_01/coverage_addendum_01'
F=B/'fresh_public_findings_export_adversary_01'
prefix='draft_pr_descending_audit_20261002/audits/pr259_5100026/initial_review_20261012'
A=E/'payloads'/prefix
checks=[]
inputs={}

def ck(test,label,details=None):
    checks.append({'check':label,'pass':bool(test),'details':details})
    if not test:
        raise AssertionError(label)

def pin(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
            'git_blob_oid':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}

def read(p):
    p=Path(p)
    ck(p.is_file() and not p.is_symlink(),'regular input: '+str(p))
    raw=p.read_bytes()
    ck(raw==p.read_bytes(),'stable immediate read: '+str(p))
    inputs[str(p)]=pin(raw)
    return raw

def load(p):
    return json.loads(read(p))

def check_pin(p,declared,label):
    measured=pin(read(p))
    for k in ['bytes','sha256']+(['git_blob_oid'] if 'git_blob_oid' in declared else []):
        ck(k in declared and measured[k]==declared[k],label+': '+k)
    return measured

def safe(rel):
    return isinstance(rel,str) and rel and not rel.startswith('/') and '\\' not in rel and all(x not in ('','..','.') for x in PurePosixPath(rel).parts)

def records(rows,key,label):
    ck(all(safe(x[key]) for x in rows),label+': safe relative paths')
    out={x[key]:x for x in rows}
    ck(len(out)==len(rows),label+': no repeated path')
    return out

def physical(root):
    ck(root.is_dir() and not root.is_symlink(),'regular directory: '+str(root))
    allpaths=list(root.rglob('*'))
    ck(not any(x.is_symlink() for x in allpaths),'no symlink in inventory: '+str(root))
    return {x.relative_to(root).as_posix():x for x in allpaths if x.is_file()}

def check_inventory(actual,rows,key,label):
    indexed=records(rows,key,label)
    ck(set(indexed)==set(actual),label+': exact inventory, no omitted or extra path',
       {'unlisted':sorted(set(actual)-set(indexed)),'phantom':sorted(set(indexed)-set(actual))})
    for rel,row in indexed.items():
        check_pin(actual[rel],row,label+' '+rel)
    return indexed

def pointer(obj,ptr):
    if ptr=='':return obj
    assert ptr.startswith('/')
    for item in ptr.split('/')[1:]:
        item=item.replace('~1','/').replace('~0','~')
        obj=obj[int(item)] if isinstance(obj,list) else obj[item]
    return obj

def strip_headers(obj,path=''):
    if isinstance(obj,dict):
        return {k:strip_headers(v,path+'/'+k) for k,v in obj.items()
                if k.lower() not in {'headers','response_headers','raw_headers','set-cookie','cookie','cookies'}}
    if isinstance(obj,list):return [strip_headers(v,path+'/'+str(i)) for i,v in enumerate(obj)]
    return obj

def no_raw_headers(obj):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k.lower() in {'headers','response_headers','raw_headers','set-cookie','cookie','cookies'} and v:
                return False
            if not no_raw_headers(v):return False
    elif isinstance(obj,list):return all(no_raw_headers(v) for v in obj)
    return True

def norm(obj):
    if isinstance(obj,dict):return {k:norm(v) for k,v in obj.items() if k not in {'UTC','utc','checked_utc'}}
    if isinstance(obj,list):return [norm(v) for v in obj]
    return obj

def main():
    assigned={
       E/'FINAL_MANIFEST.json':(70728,'c71f44ad8778e2f6b6345a039482ceac81f42b9d64ddc9dfaaa98969c38c0503'),
       E/'SCOPED_FILE_PLAN.json':(242597,'fdc9191a8871ea9d3e87fdb20f7bb33f33774a6444334239fb625113f6ffee2d'),
       C/'ADDENDUM_MANIFEST.json':(3058,'94bd6588eb89218411974ac6976bf4c3779e0b2d22835c04932166be77f30eb9'),
       C/'EXHAUSTIVE_V02_249_FILE_INVENTORY.json':(103770,'b2824c70b5832bc3119370c01e4ccc4d270915b4fd523812f17f4d34805ebe5a'),
       C/'OUTER_COVERAGE_ADDENDUM.json':(7304,'c84a0cb2b9009b918d27e4c1e93f44ad20d10068223b58748efc4923cd7dcd42')}
    for p,(size,digest) in assigned.items():
        check_pin(p,{'bytes':size,'sha256':digest},'explicit assigned source pin')

    actual=physical(E)
    ck(len(actual)==249,'independently enumerated exact 249 original export files')
    outer=load(E/'FINAL_MANIFEST.json')
    old=records(outer['files'],'path','original outer247')
    ck(len(old)==247,'original outer has247 entries')
    ck(not(set(old)-set(actual)),'no original outer phantom entry')
    for rel,row in old.items():check_pin(actual[rel],row,'original247 still exact '+rel)
    nested='payloads/'+prefix+'/elliptic_centroid_adversary/FINAL_MANIFEST.json'
    omissions=sorted(set(actual)-set(old))
    ck(omissions==['FINAL_MANIFEST.json',nested],'exact old two omissions, independently derived')
    ck(outer['self_pin_excluded'] is True,'old outer self exclusion was declared')
    inv=load(C/'EXHAUSTIVE_V02_249_FILE_INVENTORY.json')
    invrows=check_inventory(actual,inv['files'],'path','new exhaustive249 inventory')
    ck(inv['actual_file_count']==249 and inv['root']==str(E) and inv['declared_exclusions']==[],
       'new249 inventory scope and no exclusions')

    addmf=load(C/'ADDENDUM_MANIFEST.json')
    addactual=physical(C)
    ck(len(addactual)==10,'exact10 addendum files including self')
    ck(addmf['self_pin_excluded_exact_path']=='ADDENDUM_MANIFEST.json','addendum excludes exact self path')
    check_inventory({k:v for k,v in addactual.items() if k!='ADDENDUM_MANIFEST.json'},addmf['files'],'path','addendum9 plus bound self')
    for diag in addmf['full_local_diagnostic_pins']:
        check_pin(Path(diag['path']),diag,'external full local diagnostic')
        dj=load(diag['path'])
        labels=dj.get('check_labels',dj.get('checks'))
        ck(isinstance(labels,list) and len(labels)==diag['exact_check_label_count'],'exact diagnostic label count')
        compact=json.dumps(labels,separators=(',',':')).encode()
        ck(hashlib.sha256(compact).hexdigest()==diag['compact_label_sequence_sha256'],'complete diagnostic label sequence hash')
    local=load(C/'LOCAL_COVERAGE_VERIFICATION.json')
    ck(local['check_count']==2243 and local['fresh_adversary_and_Root_acceptance_pending'] is True,
       'preparer local2243 is explicitly not fresh review acceptance')
    build=load(C/'BUILD_VERIFICATION.json')
    db=load(build['full_check_diagnostic']['path'])
    ck(db['checks']==1617 and len(db['check_labels'])==1618 and db['check_labels'][-1]=='new-addendum-only:BUILD_VERIFICATION.json',
       'build1617 evaluated before final exclusive-write guard,1618 labels; no hidden failure')
    ck(build['full_check_diagnostic']['exact_check_label_count']==1618,
       'compacted build explicitly identifies1618 actual labels')

    plan=load(E/'SCOPED_FILE_PLAN.json')
    selected=records(plan['paths'],'payload_relative_path','scientific231 plan')
    ck(len(selected)==plan['selected_count']==231,'exact231 selected scientific files')
    payload_actual=physical(E/'payloads')
    ck(set(payload_actual)=={r['target_repository_path'] for r in selected.values()},'exact physical payload inventory equals plan')
    ck(sum(x['bytes'] for x in selected.values())==plan['selected_bytes']==4152796,'exact4152796 selected bytes')
    for rel,row in selected.items():
        ck(rel=='payloads/'+row['target_repository_path'] and row['target_repository_path']==prefix+'/'+row['audit_relative_path'],
           'exact canonical payload/repository/audit path relation '+rel)
        ck(row['mode']=='100644' and row['operation']=='UNDECIDED_UNTIL_FRESH_MAIN_PREIMAGE','file-only nonexecuting row '+rel)
        measured=check_pin(actual[rel],row,'unchanged selected science '+rel)
        ck(all(invrows[rel][k]==measured[k] for k in ('bytes','sha256','git_blob_oid')),'science row exact in new249 coverage '+rel)
        raw=read(actual[rel]);text=raw.decode('utf-8')
        if rel.endswith('.py'):ast.parse(text,filename=rel)
        if rel.endswith('.json'):
            ck(no_raw_headers(json.loads(raw)),'no raw header/cookie dictionary in selected JSON '+rel)
        src=row.get('source_audit_relative_path')
        if src and not rel.endswith('_PUBLIC_METADATA.json'):
            ck(raw==read(B/src),'verbatim owned historical source '+rel)
        ck(not any(x in {'private_reading','private_sources','private_evidence','vendor'} for x in PurePosixPath(rel).parts),
           'no excluded private/vendor directory selected '+rel)
        ck(not rel.endswith(('.pdf','.zip','.png','.html','.jpg','.jpeg','.webp','.gif')),'no primary binary/fullHTML selected '+rel)

    public=load(A/'PUBLIC_FINDINGS_EXPORT_MANIFEST.json')
    publicrows=records(public['files'],'audit_relative_path','public230 selected manifest')
    ck(set(publicrows)=={r['audit_relative_path'] for r in selected.values()}-{'PUBLIC_FINDINGS_EXPORT_MANIFEST.json'},
       'public manifest omits only its exact recursive self')
    for rel,row in publicrows.items():check_pin(A/rel,row,'public230 still exact '+rel)
    mapdata=load(A/'PUBLIC_FINDINGS_EVIDENCE_LOCATIONS.json')
    maprows=records(mapdata['selected_owned_files'],'audit_relative_path','compact229 evidence inventory')
    ck(set(maprows)==set(publicrows)-{'PUBLIC_FINDINGS_EVIDENCE_LOCATIONS.json'},'compact229 excludes only self and selection manifest')
    for rel,row in maprows.items():check_pin(A/rel,row,'map229 still exact '+rel)
    maps=load(E/'CANONICAL_PUBLIC_MAP_PINS.json')
    ck(len(maps['pins'])==6,'six original author-facing canonical pins')
    for name,row in maps['pins'].items():
        ck(row['repository_path']==prefix+'/'+name,'canonical path '+name)
        check_pin(A/name,row,'canonical payload original pin '+name)
    add=load(C/'OUTER_COVERAGE_ADDENDUM.json')
    ck([x['path'] for x in add['exact_omissions_from_original_outer_manifest']]==omissions,'addendum omission disclosure exact')
    for omission in add['exact_omissions_from_original_outer_manifest']:
        check_pin(E/omission['path'],omission['pin'],'explicit omitted original covered')
    n=add['exact_omissions_from_original_outer_manifest'][1]
    ck(n['original_outer_second_exclusion_declared'] is False,'old silent omission honestly recorded')
    ck(n['existing_scoped_plan_entry']==selected[nested],'nested exact original scientific plan entry')
    ck(n['existing_public_selection_manifest_entry']==publicrows['elliptic_centroid_adversary/FINAL_MANIFEST.json'],
       'nested exact original public selection entry')
    check_pin(B/'elliptic_centroid_adversary/FINAL_MANIFEST.json',n['historical_family_original_pin'],'nested original historical family pin')
    ck(read(B/'elliptic_centroid_adversary/FINAL_MANIFEST.json')==read(E/nested),'nested original and selected body byte identical')
    for item in add['six_canonical_author_facing_payloads_unchanged']:
        check_pin(E/item['path'],item,'addendum preserves six canonical pins '+item['name'])
        ck(all(item[k]==maps['pins'][item['name']][k] for k in ('bytes','sha256','git_blob_oid')),
           'addendum canonical binding equals original pin '+item['name'])
    ck(len(add['six_canonical_author_facing_payloads_unchanged'])==6 and add['scientific_selected_count']==231 and add['scientific_selected_bytes']==4152796,
       'addendum preserves exact six/231/4152796 dimensions')
    ck(add['other_omissions']==[] and add['original_phantom_entries']==[] and add['no_execution_authority'] is True and add['case_complete'] is False,
       'addendum makes no additional omission/action/case claim')

    bindings=load(C/'FRESH_REVIEW_AND_ROOT_FAILURE_BINDINGS.json')
    factactual=physical(F)
    ck(len(factactual)==38,'exact38 complete previous fresh review files')
    check_inventory(factactual,bindings['complete_fresh_review_files'],'path','bound complete38 previous review')
    fm=load(F/'PUBLIC_MANIFEST.json')
    check_inventory({k:v for k,v in factactual.items() if k!='PUBLIC_MANIFEST.json'},fm['files'],'path','previous fresh37 plus exact self')
    for item in bindings['direct_input_bindings']:check_pin(Path(item['path']),item,'addendum direct provenance binding')
    d=load(F/'DECISION.json')
    ck(d['completed'] is True and d['scientific_selection_verdict']=='PASS' and [x['id'] for x in d['findings']]==['EXPORT-PREP-001'],
       'previous fresh actual decision was sciencePASS with this sole metadata issue')
    v=load(F/'VERIFICATION.json')
    ck(v['completed'] is True and v['check_count']==len(v['checks'])==5863 and all(x['pass'] is True for x in v['checks']),
       'previous fresh5863 explicit recorded checks are complete and passed')
    for rel,declared in d['review_artifact_pins'].items():check_pin(F/rel,declared,'previous decision own artifact pin '+rel)
    inp=load(F/'INPUT_PINS.json')
    ck(len(inp['files'])==528,'previous review actual528 recorded input pins')
    for item in inp['files']:check_pin(Path(item['path']),item,'complete previous review historical input')
    for failure in bindings['all_known_Root_failures_preserved']:
        folder=B/failure['folder'];j=load(folder/'FAILURE_RECEIPT.json')
        check_pin(folder/'FAILURE_RECEIPT.json',failure['receipt_pin'],'known Root failure receipt')
        cp=check_pin(folder/'FAILED_CHECKER.py',failure['failed_checker_pin'],'known Root failed checker')
        ck(j['completed'] is False and j['observed_exit_code']==1 and cp['sha256']==j['checker_sha256'],
           'failed Root check not forged into completion '+failure['folder'])
        ck(failure['source_defect']==(failure['folder']=='root_public_export_v02_verification_01'),
           'actual source coverage defect distinguished from own harness errors '+failure['folder'])
    rootv=load(B/'root_public_export_v02_selection_verification_04/VERIFICATION.json')
    check_pin(B/'root_public_export_v02_selection_verification_04/VERIFICATION.json',bindings['later_Root_selection_only_receipt_pin'],'later bounded Root selection-only receipt')
    ck(rootv['completed'] is True and rootv['outer_preparation_inventory_exhaustive'] is False and rootv['whole_preparation_promotion_acceptance'] is False,
       'old Root bounded PASS does not falsely claim exhaustive coverage')

    replay=load(F/'public_helper_replay_01/VERIFICATION.json')
    ck(replay['completed'] is True and len(replay['rows'])==4 and replay['ignored_json_keys']==['UTC','checked_utc','utc'],
       'four previous actual stored helper replays with exactly timestamp exceptions')
    replay_comparisons=[]
    for row in replay['rows']:
        scratch=Path(row['scratch_output']);D=scratch.parent
        ck(row['exit_code']==0 and row['mathematical_output_equal_excluding_UTC_only'] is True,'previous actual child success '+row['label'])
        ck(read(D/Path(row['script_relative_path']).name)==read(A/row['script_relative_path']),'previous actual copied script unchanged '+row['label'])
        ck(pin(read(A/row['script_relative_path']))['sha256']==row['script_sha256'],'stored child source hash '+row['label'])
        ck(pin(read(A/row['expected_receipt_relative_path']))['sha256']==row['expected_receipt_sha256'],'stored expected output hash '+row['label'])
        ck(pin(read(D/'stdout.txt'))['sha256']==row['stdout_sha256'] and read(D/'stderr.txt')==b'' and pin(read(D/'stderr.txt'))['sha256']==row['stderr_sha256'],
           'stored actual child streams consistent '+row['label'])
        ck(norm(load(scratch))==norm(load(A/row['expected_receipt_relative_path'])),'complete stored actual mathematical output comparison '+row['label'])
        replay_comparisons.append({'label':row['label'],'original_actual_replay_utc':row['started_utc'],'output_pin':pin(read(scratch)),
                                   'new_execution_performed':False,'complete_output_equal_except_UTC_only':True})

    ck(len(plan['exclusions'])==9 and plan['exclusions']==public['excluded_original_header_receipts']==mapdata['excluded_header_receipts'],
       'nine exact header exclusions consistent in all original maps')
    for exclusion in plan['exclusions']:
        rel=exclusion['audit_relative_path'];der=exclusion['replacement_derivative']
        ck(not (A/rel).exists() and (A/der).exists(),'excluded original absent and derivative selected '+rel)
        check_pin(B/rel,exclusion['pin'],'exact excluded historical original pin '+rel)
        original=load(B/rel);derived=load(A/der)
        ck(derived['original_pin']==exclusion['pin'] and derived['preserves_original_bytes'] is False,'derivative cannot satisfy old original pins '+rel)
        ck(strip_headers(original)==derived['records'],'exact non-header metadata preservation '+rel)

    fetch=load(A/'PUBLIC_FINDINGS_PRIMARY_SOURCE_FETCH_MAP.json')
    ck(fetch['records']==mapdata['private_primary_source_metadata'] and len(fetch['records'])==133 and fetch['bodies_selected'] is False,
       '133 primary URL/pin locators consistent and no bodies selected')
    for item in fetch['records']:
        source=load(A/item['metadata_source'])
        source_obj=pointer(source,item['json_pointer'])
        ck(all(source_obj[k]==value for k,value in item['pin'].items()),'actual original source pin object correspondence')
        ck(all(source_obj[k]==value for k,value in item['urls'].items()),'actual original source URL object correspondence')
        ck(item['body_selected'] is False,'primary source body explicitly excluded')
    all_links=[]
    for rel,p in payload_actual.items():
        if not rel.endswith('.md'):continue
        for match in re.finditer(r'!?\[[^\]]*\]\(([^)]+)\)',read(p).decode()):
            literal=match.group(1).strip().strip('<>');loc=literal.split(' ',1)[0]
            if urlsplit(loc).scheme or loc.startswith('#'):continue
            target=(p.parent/unquote(loc.split('#',1)[0])).resolve()
            ck(target.is_file() and target.is_relative_to(E/'payloads'),'actual selected local Markdown link resolves '+literal)
            all_links.append({'from':rel,'literal':literal,'target':target.relative_to(E/'payloads').as_posix()})

    readme=read(A/'PUBLIC_FINDINGS_README.md').decode();deps=read(A/'PUBLIC_FINDINGS_REPLAY_DEPENDENCIES.md').decode()
    for phrase in ['even least period','full perpendicular supporting lines','original focus','arithmetic vertex mean','finite and unique','every coprime star','least” is an explicit adopted convention','unrefereed','not represented as human peer reviewed','AI tools were used extensively','novelty is not cleared','do not prove absolute first public visibility','1 October 2026','metadata states 30 September']:
        ck(phrase in readme,'public accepted scope/credit/disclosure phrase '+phrase)
    for phrase in ['not assert that future receipt exists','Current author-package, case and actual publication status are maintained separately','No new open-target resolution paper, DOI, tracker credit, native merge or closure']:
        ck(phrase in readme,'no false future action/case-publication promise '+phrase)
    for phrase in ['not executed by this preparation or the portable helper','No network fetch, Git operation','Finite numerical outputs are diagnostics','Mutable official metadata','historical preparation limits','Do not run the original output-writing programs in a frozen packet directory']:
        ck(phrase in deps,'precise public replay dependency boundary '+phrase)
    science=load(A/'ROOT_WHOLE_MATH_SOURCE_QUALIFIED_ACCEPTANCE.json')
    priority=load(A/'ROOT_FRESH_PRIORITY_DISPOSITION_ACCEPTANCE.json')
    ck(science['proof_sha256']==pin(read(B/'submitted/unsolved_math_prioritization/attempts/5100026/PROOF.md'))['sha256'],
       'accepted original proof exact source pin')
    ck(priority['completed'] is True and priority['proposed_adjudicated_status']=='already_solved' and priority['no_absolute_first_visibility_or_causal_order_claim'] is True and priority['no_value_formula_novelty_clearance'] is True,
       'public priority framing agrees with actual qualified Root acceptance')
    ck(priority['case_counted_complete'] is False and priority['provider_authority'] is False,'historical scientific acceptance has no action/case authority')

    # Falsification controls act only on in-memory clones; no source mutation.
    exact_set=set(actual)
    controls=[]
    for label,bad in [('drop originally omitted nested manifest',[x for x in inv['files'] if x['path']!=nested]),
                      ('drop outer self',[x for x in inv['files'] if x['path']!='FINAL_MANIFEST.json']),
                      ('inject phantom',[*inv['files'],{'path':'PHANTOM.json','bytes':0,'sha256':'0'*64}])]:
        rejected={x['path'] for x in bad}!=exact_set
        ck(rejected,'negative inventory control rejects: '+label)
        controls.append({'mutation':label,'rejected':rejected})
    bad=copy.deepcopy(invrows[nested]);bad['sha256']='0'*64
    ck(pin(read(E/nested))['sha256']!=bad['sha256'],'negative nested payload hash substitution detected')
    controls.append({'mutation':'substitute nested SHA256','rejected':True})
    ck(pin(read(B/plan['exclusions'][0]['audit_relative_path']))['sha256']!=pin(read(A/plan['exclusions'][0]['replacement_derivative']))['sha256'],
       'negative derivative-as-original equivalence rejected')
    controls.append({'mutation':'use sanitized derivative as old receipt','rejected':True})

    # Re-authenticate every read input after all checks. This proves no source
    # writes during this run and detects changes from concurrent agents.
    for path,oldpin in list(inputs.items()):
        ck(pin(Path(path).read_bytes())==oldpin,'end-of-review read input unchanged '+path)
    receipt={'schema':'pr259-new-fresh-independent-export-coverage-verification-v1','utc':datetime.now(timezone.utc).isoformat(),
             'decision':'PASS_EXACT_OUTER_COVERAGE_ADDENDUM_AND_UNCHANGED_PUBLIC_SCIENTIFIC_EXPORT','completed':True,
             'check_count':len(checks),'checks':checks,'original_export_files':249,'new_exhaustive_inventory_files':249,
             'original_outer_entries':247,'exact_original_omissions':omissions,'scientific_files':231,'scientific_bytes':4152796,
             'canonical_author_map_pins_unchanged':6,'complete_previous_fresh_review_files':38,'previous_review_input_pins_checked':528,
             'previous_recorded_checks_authenticated':5863,'known_Root_failures_preserved':3,'exact_stored_replay_output_comparisons':replay_comparisons,
             'new_mathematical_core_executions':0,'falsification_controls':controls,'local_markdown_links_checked':all_links,
             'source_inputs_unchanged':True,'provider_calls':0,'shared_git_writes':0,'outside_person_communications':0,
             'scientific_novelty_acceptance':False,'execution_authority':False,'case_complete':False,
             'scope_limit':'New fresh review of metadata repair and unchanged scientific export only; no author/Main/operator/action/case completion authority. Previously completed mathematical/priority reviews remain historically scoped; stored actual core outputs were independently compared, not reported as new executions.'}
    (W/'VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
    (W/'INPUT_PINS.json').write_text(json.dumps({'utc':receipt['utc'],'files':[{'path':p,**v} for p,v in sorted(inputs.items())],
                                             'no_primary_bodies_or_headers_copied':True},indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ('decision','completed','check_count','original_export_files','scientific_files','scientific_bytes','complete_previous_fresh_review_files','new_mathematical_core_executions')},indent=2))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        (W/'FAILED_VERIFICATION.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'completed':False,
             'error':repr(exc),'checks':checks,'input_pins':[{'path':p,**v} for p,v in sorted(inputs.items())]},indent=2)+'\n')
        raise
