#!/usr/bin/env python3
"""Build a concrete packet from real preflight/service bytes; never runs assess."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,sqlite3,subprocess,sys
A=Path(__file__).resolve().parents[1]
def need(v,m):
    if not v:raise RuntimeError(m)
def canonical(v):return (json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_text())
def pin(p):return {'path':p.relative_to(A).as_posix(),**hp(p.read_bytes())}
def stream_file_pin(p):
    h=hashlib.sha256();n=0
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
    return {'bytes':n,'sha256':h.hexdigest()}
def authenticate_preflight(F):
    pre=read(F);C=A.parents[2];journal=read(F.parent/'PROCESS_JOURNAL.json');need(journal['actual_operator_PID']==pre['actual_reader_PID'],'Raw probe PID/journal')
    opfolder=A/'actual_operations/root_fresh_native_preflight_20261006';ex=read(opfolder/'execution.json')
    need(ex['exit_code']==0 and ex['reaped'] is True and ex['child_PID']==pre['actual_reader_PID'] and ex['termination']['signal'] is None,'Genuine actual probe completion')
    for s in ('stdout','stderr'):need(hp((opfolder/ex[s]['path']).read_bytes())=={k:ex[s][k] for k in ('bytes','sha256')},'Actual probe parent stream')
    outer=read(opfolder/'stdout.bin');need(outer['actual_reader_PID']==pre['actual_reader_PID'] and outer['preflight_path']==str(F) and outer['main_parent']==pre['main_parent'],'Real stdout/raw probe identity')
    physical=pre['runtime']['binaries']['python']['resolved_absolute_path'];helper=A/'publication_build_v1/prepare_native_preflight.py'
    need(ex['argv']==[physical,'-E','-S','-B','-P',str(helper),pre['main_parent'],F.parent.name] and ex['cwd']==str(A) and ex['UTC_start']<=pre['UTC']<=ex['UTC_end'],'Exact actual physical Python/helper/flags/cwd/start chronology')
    operations=journal['operations'];need(len({r['actual_PID'] for r in operations})==len(operations),'Genuine distinct probe child PIDs');dynamic={}
    git=pre['runtime']['binaries']['git']['resolved_absolute_path'];native_checks=[];baseenv=pre['runtime']['python_environment']
    gitenv={**baseenv,'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_CONFIG_SYSTEM':'/dev/null','GIT_OPTIONAL_LOCKS':'0','GIT_NO_REPLACE_OBJECTS':'1','GIT_TERMINAL_PROMPT':'0'}
    gitbase=[git,'-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null','-c','credential.helper='];gh=pre['runtime']['binaries']['gh']['resolved_absolute_path']
    ghenv={**baseenv,'GH_CONFIG_DIR':pre['runtime']['gh_config_directory'],'GH_HOST':'github.com','GH_PROMPT_DISABLED':'1','GH_PAGER':'','GH_BROWSER':'/usr/bin/false','GH_EDITOR':'/usr/bin/false','GH_NO_UPDATE_NOTIFIER':'1'}
    digest=lambda env:hashlib.sha256(json.dumps(env,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    contracts=[]
    for role in ('python','git','gh','gws','node'):
        path=pre['runtime']['dependency_files']['gws_native_backend']['absolute_path'] if role=='gws' else pre['runtime']['binaries'][role]['resolved_absolute_path']
        contracts.append(([path,'--version'],ex['environment_sha256']))
    for args in (['rev-parse','HEAD'],['symbolic-ref','--short','HEAD'],['ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main'],['diff','--cached','--name-only','-z']):contracts.append((gitbase+args,digest(gitenv)))
    contracts.append(([gh,'pr','view','https://github.com/AlecKriebel/Math/pull/110','--json','number,state,isDraft,headRefOid,baseRefName,headRefName'],digest(ghenv)))
    for spec in pre['native_baseline'].values():contracts.append((gitbase+['show',pre['main_parent']+':'+spec['path']],digest(gitenv)))
    # JSON canonicalization sorts native_baseline keys; recover the literal
    # queue/manifest/policy/... ordering used by the audited probe source.
    order=['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
    contracts=contracts[:10]+[(gitbase+['show',pre['main_parent']+':'+pre['native_baseline'][name]['path']],digest(gitenv)) for name in order]
    need(len(operations)==len(contracts),'Exact actual probe child count')
    for operation,(argv,envsha) in zip(operations,contracts):
        need(operation['argv']==argv and operation['cwd']==str(C) and operation['environment_sha256']==envsha,'Exact current probe child argv/cwd/environment contract')
        need(operation['exit_code']==0 and operation['reaped'] is True and operation['termination_reason'] is None and ex['UTC_start']<=operation['UTC_start']<=operation['UTC_end']<=pre['UTC'],'Successful actual readonly child/whole chronology')
        for stream in ('stdout','stderr'):
            row=operation[stream];need(row['streams_fully_drained'] is True and row['observed_bytes']==row['bytes'] and row['observed_sha256']==row['sha256'],'Full observed successful stream')
            if 'path' in row:need(hp((A/row['path']).read_bytes())=={k:row[k] for k in ('bytes','sha256')},'Raw actual dynamic child stream')
            else:
                need(stream=='stdout' and row['body_custody']=='immutable_Git_blob_full_body' and row['git_commit_path'].startswith(pre['main_parent']+':'),'Exact retained Git custody')
                replayargv=gitbase+['show',row['git_commit_path']];started=datetime.now(timezone.utc).isoformat();p=subprocess.Popen(replayargv,cwd=C,env=gitenv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);termination=None
                try:body,err=p.communicate(timeout=30)
                except subprocess.TimeoutExpired:p.kill();body,err=p.communicate();termination='deadline_KILL_and_reap'
                native_checks.append({'actual_PID':p.pid,'argv':replayargv,'cwd':str(C),'environment_sha256':digest(gitenv),'exit_code':p.returncode,'reaped':True,'termination_reason':termination,'UTC_start':started,'UTC_end':datetime.now(timezone.utc).isoformat(),'full_stdout':hp(body),'full_stderr':hp(err)})
                (F.parent/'ROOT_GIT_REPLAY_JOURNAL.json').write_bytes(canonical({'actual_operator_PID':os.getpid(),'operations':native_checks}))
                need(p.returncode==0 and termination is None and not err and hp(body)=={k:row[k] for k in ('bytes','sha256')},'Independent full Git body replay; actual failure retained')
        if 'path' in operation['stdout']:dynamic[tuple(operation['argv'])]=(A/operation['stdout']['path']).read_bytes()
    for name,spec in pre['native_baseline'].items():
        need(any(row['argv'][-1]==pre['main_parent']+':'+spec['path'] and row['full_stdout']=={k:spec[k] for k in ('bytes','sha256')} for row in native_checks),'Every native baseline independently checked')
    need(dynamic[tuple(gitbase+['rev-parse','HEAD'])].decode().strip()==pre['main_parent'] and dynamic[tuple(gitbase+['symbolic-ref','--short','HEAD'])].strip()==b'main' and dynamic[tuple(gitbase+['diff','--cached','--name-only','-z'])]==b'','Exact actual local main/branch/empty-index raw bodies')
    ghraw=next(body for argv,body in dynamic.items() if argv[0]==gh and argv[1:3]==('pr','view'));ghvalue=json.loads(ghraw)
    need(ghvalue['headRefOid']==pre['original_head'] and ghvalue['state']=='OPEN' and ghvalue['isDraft'] is True and ghvalue['baseRefName']=='main' and ghvalue['number']==110,'Actual raw live PR response')
    remote=next(body for argv,body in dynamic.items() if 'ls-remote' in argv);need(remote.decode().split()[0]==pre['main_parent'],'Actual raw remote main response')
    sourceargv=gitbase+['show',pre['main_parent']+':'+str(helper.relative_to(C))];started=datetime.now(timezone.utc).isoformat()
    p=subprocess.Popen(sourceargv,cwd=C,env=gitenv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);termination=None
    try:source,err=p.communicate(timeout=30)
    except subprocess.TimeoutExpired:p.kill();source,err=p.communicate();termination='deadline_KILL_and_reap'
    sourcecheck={'actual_PID':p.pid,'argv':sourceargv,'cwd':str(C),'environment_sha256':digest(gitenv),'exit_code':p.returncode,'reaped':True,'termination_reason':termination,'UTC_start':started,'UTC_end':datetime.now(timezone.utc).isoformat(),'full_stdout':hp(source),'full_stderr':hp(err)}
    native_checks.append(sourcecheck)
    (F.parent/'ROOT_GIT_REPLAY_JOURNAL.json').write_bytes(canonical({'actual_operator_PID':os.getpid(),'operations':native_checks}))
    need(p.returncode==0 and termination is None and not err and source==helper.read_bytes(),'Exact committed helper body custody; actual failure retained')
    pre['committed_probe_source_authentication']={**sourcecheck,'body_pin':pin(helper)}
    for binary in pre['runtime']['binaries'].values():need(stream_file_pin(binary['resolved_absolute_path'])=={k:binary[k] for k in ('bytes','sha256')},'Fresh runtime body pin')
    for dependency in pre['runtime']['dependency_files'].values():need(stream_file_pin(dependency['absolute_path'])=={k:dependency[k] for k in ('bytes','sha256')},'Fresh current GWS dependency body')
    for config in pre['runtime']['private_configuration_pins']:need(stream_file_pin(config['absolute_path'])=={k:config[k] for k in ('bytes','sha256')},'Fresh private configuration body pin')
    for name,spec in pre['raw_source_pins'].items():need(stream_file_pin(Path('/Users/alec/Documents/Math/unsolved_math_prioritization/cache')/name)==spec,'Raw source independently checked')
    cache=pre['source_cache'];need(stream_file_pin(cache['absolute_path'])==cache['pin'] and not any(os.path.lexists(cache['absolute_path']+s) for s in ('-wal','-shm','-journal')),'Actual immutable SQL body/sidecars')
    db=sqlite3.connect('file:'+cache['absolute_path']+'?mode=ro&immutable=1',uri=True)
    try:
        need(db.execute('SELECT revision FROM metadata').fetchone()==(pre['dataset_revision'],) and db.execute('SELECT count(*) FROM records').fetchone()[0]==15458,'Actual SQL identity')
        row=db.execute('SELECT payload,report FROM records WHERE key=?',('5100032',)).fetchone()
        for i,name in enumerate(('source_record.json','prior_imported_report.json')):need(canonical(json.loads(row[i]))==canonical(read(A/'original_head_authentication_20261006/original_attempt'/name)),'Actual root sourcepair SQL comparison')
        need(bool(json.loads(row[1])),'Actual nonempty SQL prior')
    finally:db.close()
    pre['raw_probe_receipt']=pin(F);pre['actual_parent_execution']=pin(opfolder/'execution.json');pre['root_authentication_PID']=os.getpid();pre['root_authentication_UTC']=datetime.now(timezone.utc).isoformat();pre['root_independently_authenticated_actual_preflight_processes']=True;pre['independent_full_native_Git_checks']=native_checks
    output=F.parent/'PREFLIGHT_ROOT_AUTHENTICATED.json';need(not output.exists(),'Unique actual authenticated preflight');output.write_bytes(canonical(pre));return output
def main():
    F=Path(sys.argv[1]);need(F.is_relative_to(A) and F.is_file(),'Actual preflight file');D=F.parent
    rawF=F;F=authenticate_preflight(F)
    pre=read(F);need(pre['actual_receipt'] is True and pre['native_assess_executed'] is False,'Actual readonly preflight')
    family=A/'native_execution_programs_v1';need((family/'OUTPUT_MANIFEST.json').is_file() and (family/'SEAL_RECEIPT.json').is_file(),'Final concrete family not sealed')
    m=read(family/'OUTPUT_MANIFEST.json')
    for e in m['files']:
        p=family/e['path'];need(all(pin(p)[k]==e[k] for k in ('bytes','sha256')),'Sealed concrete family drift')
    registry={}
    def use(p):
        p=Path(p);s=pin(p)
        if s['path'] in registry:need(registry[s['path']]==s,'Conflicting input pin')
        registry[s['path']]=s;return s
    originalroot=A/'original_head_authentication_20261006';original={'manifest':use(originalroot/'ORIGINAL_BLOB_MANIFEST.json'),'queue':use(originalroot/'ORIGINAL_HEAD_QUEUE.md'),'sourcepair_authentication':use(originalroot/'SOURCEPAIR_AUTHENTICATION.json'),'files':{}}
    orig=read(originalroot/'ORIGINAL_BLOB_MANIFEST.json')
    for row in orig['files']:original['files'][row['relative_path']]=use(originalroot/'original_attempt'/row['relative_path'])
    candidate=A/'publication_ready_v1';seal=read(A/'publication_ready_v1_SEAL.json');logical={row['path']:use(candidate/row['path']) for row in seal['files'] if row['path']!='focal_antipedal_sum_support.zip'}
    transport={'actual_receipt':True,'template_only':False,'package_manifest_sha256':logical['PACKAGE_MANIFEST.json']['sha256'],'exact_logical_inventory':logical,'no_missing_duplicate_extra_or_unsafe_archive_members':True,'actual_root_authentication':pin(A/'ROOT_ACTUAL_PUBLICATION_TRACKER_AUTHENTICATION_20261006.json')}
    (D/'TRANSPORT_INVENTORY.json').write_bytes(canonical(transport))
    package={'manifest':logical['PACKAGE_MANIFEST.json'],'logical_inventory':logical,'effective_proof':logical['focal_antipedal_sum.tex'],'transport_inventory_receipt':use(D/'TRANSPORT_INVENTORY.json')}
    pubfile=A/'published_record_fullbody_verification_20261006/PUBLICATION_RECEIPT.json';sheetfile=A/'actual_tracker_20261006/SHEET_RECEIPT.json';pub=read(pubfile);sheet=read(sheetfile)
    records={'zenodo.metadata':pub['metadata_GET'],**{'zenodo.payload.'+name:item['GET'] for name,item in pub['logical_readbacks'].items()},**{'gws.'+name:r for name,r in sheet['processes'].items()}}
    checked=[]
    def checked_use(p):
        spec=use(p)
        if spec not in checked:checked.append(spec)
    for item in pub['logical_readbacks'].values():
        for key in ('body','transport_body'):use(A/item[key]['path'])
    contracts={}
    for role,record in records.items():
        for key in ('stdout','stderr'):use(A/record[key]['path'])
        for key in ('raw_execution','raw_HTTP_receipt'):
            if key in record:checked_use(A/record[key]['path'])
        inputs=[]
        if role.startswith('zenodo.'):
            # The committed initial helper preceded the actual metadata GET;
            # later file GETs used its Accept-header correction, preserved here.
            fname='publication_transport_source_custody_v1/initial_fetch_publication_resource.py' if role=='zenodo.metadata' else 'publication_build_v1/fetch_publication_resource.py'
            inputs=[use(A/fname),use(A/'publication_build_v1/record_transport.py'),use(A/'publication_transport_source_custody_v1/zenodo_bound_source.py')]
        contracts[role]={k:record[k] for k in ('argv','cwd','environment_sha256')};contracts[role].update(executable_role='gws' if role.startswith('gws.') else 'python',program_inputs=inputs)
    prefix='unsolved_math_prioritization/attempts/5100032/';offers={prefix+'historical_original/'+name:spec for name,spec in original['files'].items()}
    for name in ('source_record.json','prior_imported_report.json'):offers[prefix+name]=original['files'][name]
    offers[prefix+'PROOF.md']=use(A/'native_acceptance_source_v1/PROOF.md')
    for row in seal['files']:offers[prefix+'publication/'+row['path']]=use(candidate/row['path'])
    evidence=['ROOT_MATHEMATICAL_GATE_20261006.json','ROOT_PRIORITY_CLEARANCE_AFTER_M1_20261006.json','ROOT_WHOLE_PACKAGE_R1_AUTHENTICATION_20261006.json','ROOT_WHOLE_PACKAGE_R2_AUTHENTICATION_20261006.json','ROOT_PUBLICATION_READINESS_V1_20261006.json','ROOT_ACTUAL_PUBLICATION_TRACKER_AUTHENTICATION_20261006.json','publication_ready_v1_SEAL.json','whole_publication_adversary_r1_20261006/REPORT.md','whole_publication_adversary_r1_20261006/VERDICT.json','whole_publication_adversary_r1_20261006/OUTPUT_MANIFEST.json','whole_publication_adversary_r1_20261006/SEAL_RECEIPT.json','whole_publication_adversary_r2_20261006/REPORT.md','whole_publication_adversary_r2_20261006/VERDICT.json','whole_publication_adversary_r2_20261006/OUTPUT_MANIFEST.json','whole_publication_adversary_r2_20261006/SEAL_RECEIPT.json']
    for name in evidence:
        checked_use(A/name);offers[prefix+'acceptance_audit/'+name]=use(A/name)
    checked_use(D/'PROCESS_JOURNAL.json')
    checked_use(D/'ROOT_GIT_REPLAY_JOURNAL.json')
    checked_use(rawF)
    for name in ('execution.json','stdout.bin','stderr.bin'):checked_use(A/'actual_operations/root_fresh_native_preflight_20261006'/name)
    for name in ('publication_build_v1/prepare_native_preflight.py','publication_build_v1/prepare_native_packet.py','publication_transport_source_custody_v1/SOURCE_CUSTODY.json'):
        checked_use(A/name)
    for operation in read(D/'PROCESS_JOURNAL.json')['operations']:
        for stream in ('stdout','stderr'):
            if 'path' in operation[stream]:checked_use(A/operation[stream]['path'])
    for name in ('OUTPUT_MANIFEST.json','SEAL_RECEIPT.json'):checked_use(family/name)
    overlay={'original_budget':'2/5','new_central_proof_search_turns':0,'original_structured_ledger_present':False,'publication_DOI':pub['DOI'],'package_manifest_sha256':logical['PACKAGE_MANIFEST.json']['sha256'],'native_import_provenance':'Dated import of authenticated incoming QUEUE/author-log two-turn count; original structured turn ledger absent; all seventeen original files and nonempty prior retained.','note':'Independently reviewed full focal antipedal k603 resolution published as DOI '+pub['DOI']+'. Original observation credited; dated bounded priority audit, extensive AI-use and unrefereed status disclosed.','rationale':'Ordinary positive focal antipedal edge-norm difference is a fixed caustic coefficient times vertical displacement. Consistent caustic-left orientation and cyclic closure prove equality for all regular admitted periods/windings, including odd primitives and stars. Two fresh whole-publication reviews found no substantive issue.','remaining_gap':'No mathematical gap in the stated strictly nested elliptical-caustic domain; literature corpus/version limits remain explicit, and conventional human refereeing has not occurred.'}
    importUTC=datetime.now(timezone.utc).isoformat()
    # Constants are independently checked against original sourcepair and seals
    # by the fresh reviewer and the concrete runner before any assess action.
    packet={'schema':'pr110-concrete-native-inputs/v1','template_only':False,'identity':{'PR':110,'id':'5100032','code':'AMR-050-0032','original_head':'3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35','review_hash':'8c27c02e2166d29815cdd362f6b62e398684393679565c5033e616e7e8ac467d','statement_hash':'cb9077b72de618c4d0dba292a8b4cedd3d06993b0f38897b644e1ee44e56dd1b','dataset_revision':'37e53eabe540fb458758e198be61634bd02ee008','literal_status':'claimed_solved','turns_used':2,'new_central_proof_search_turns':0,'exact_claim':('For every regular closed billiard/Poncelet orbit between an outer ellipse a>b>0 and a fixed strictly nested confocal ellipse 0<lambda<b², the sums of ordinary Euclidean distances from each outer focus to consecutive antipedal supporting-line intersections are finite, positive and equal; literal k603 ratio1, all admissible periods/windings, including stars, reversals and repeated traversals.')},'main_parent':pre['main_parent'],'workspace_parent':str(family/'workspaces'),'program_files':{name:pin(family/name) for name in ('protocol.py','native_worker.py','native_runner.py','native_launcher.sh')},'native_baseline':pre['native_baseline'],'input_files':[],'original':original,'package':package,'publication_receipt':use(pubfile),'sheet_receipt':use(sheetfile),'service_process_contracts':contracts,'preflight_receipt':use(F),'runtime':pre['runtime'],'source_cache':pre['source_cache'],'raw_source_pins':pre['raw_source_pins'],'resources':{'cpu_seconds':90,'file_size_bytes':32*1024*1024,'open_files':64,'memory_advisory_bytes':768*1024*1024,'hard_memory_claimed':False},'parent_policy':{'deadline_seconds':120,'stdout_cap':32*1024*1024,'stderr_cap':65536,'retain_bytes':4096,'max_processes':32,'term_grace_seconds':2,'allocation_cap':160*1024*1024,'file_count_cap':512,'headroom_bytes':32*1024*1024,'commit_reserve_bytes':8*1024*1024,'runtime_reserve_bytes':8*1024*1024},'assessment_overlay':overlay,'campaign_note':'Accepted full focal antipedal k603 proof; ordinary positive sums for all regular nested-ellipse periods; original 2/5 effort preserved; publication DOI '+pub['DOI'],'import_UTC':importUTC,'attempt_offer_sources':offers,'checked_artifacts':checked}
    packet['input_files']=sorted(registry.values(),key=lambda s:s['path']);need(len(registry)<=256,'Input registry count');body=canonical(packet)
    need(len(body)<=512*1024 and sum(s['bytes'] for s in registry.values())<=32*1024*1024,'Packet/registry bounds')
    target=D/'EXECUTION_INPUTS.json';need(not target.exists(),'Unique packet');target.write_bytes(body);print(json.dumps({'packet':str(target),**hp(body),'input_count':len(registry),'attempt_sources':len(offers),'actual_native_execution':False}))
if __name__=='__main__':main()
