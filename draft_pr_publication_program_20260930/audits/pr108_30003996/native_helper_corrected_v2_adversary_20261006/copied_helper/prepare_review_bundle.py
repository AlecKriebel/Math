#!/usr/bin/env python3
"""UNEXECUTED V2: commissioned future review bundle; no install/export/Git/service writes.

Templates intentionally reject before any external read. Current tests never call prepare.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import argparse, collections, datetime, hashlib, io, json, os, re, shutil, sqlite3, stat, zipfile
import v2_guards as g
from bounded_process import BoundedRunner, validate_policy as validate_process_policy, now
from native_assess_worker import validate_policy as validate_worker_policy
sys.dont_write_bytecode = True
D = Path(__file__).resolve().parent
V1 = D.parent
A = V1.parent
C = A.parents[2]
R = Path('/Users/alec/Documents/Math')
K,CODE,N,HEAD = g.K,g.CODE,g.N,g.HEAD
P = 'unsolved_math_prioritization/'
REV = '37e53eabe540fb458758e198be61634bd02ee008'
REVIEW = '9a2816afbdd3750d36f550dc6e91c7201aa024344a7b83fdb420aafe6c86df0d'
STATEMENT = '65c107bf152773ed079cc344cfcf853c4f7da15a10453ca6f7fb411bbf5aab97'
PROOF = '2818eab189445649ae1ba98d55e3da3e5fab918de88f1779de86962ba99a3393'
ORIGINAL_PROOF = '1a6c267c6240b66c1d804397f4bbbe246f5b6147c3930e1a68396e60b618d615'
ORIGINAL = A/'original_source_authentication_20261006'
BASE_NAMES = ['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json',
              'history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
EXPORT = ['assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json',
          'ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
require,sha,encode,rel,regular = g.require,g.sha,g.canonical,g.relative,g.regular

def disk_pin(path):
    info=regular(path); h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''): h.update(block)
    require(regular(path).st_size == info.st_size, 'Streamed input size changed')
    return {'bytes':info.st_size,'sha256':h.hexdigest()}

def bounded_local_pin(spec,root=A,cap=128*1024):
    g.pin_shape(spec); path=C/rel(spec['path'])
    require(path.is_relative_to(root) and spec['bytes'] <= cap and regular(path).st_size == spec['bytes'], 'Local control pin/root/cap')
    data=path.read_bytes(); require(len(data)==spec['bytes'] and sha(data)==spec['sha256'],'Local control changed')
    return path,data

def validate_gate(obj,role,manifest_sha,inputs_sha,program_hashes,base):
    require(obj.get('schema')=='pr108-publication-root-gate/v2' and obj.get('role')==role and
        obj.get('PR')==108 and obj.get('problem_id')==30003996,'Gate identity/schema/role')
    bindings={'main_parent':base,'original_head':HEAD,'review_hash':REVIEW,'statement_hash':STATEMENT,
        'effective_proof_sha256':PROOF,'package_manifest_sha256':manifest_sha,'execution_inputs_sha256':inputs_sha}
    require(all(obj.get(k)==v for k,v in bindings.items()),'Gate input binding')
    require(obj.get('actual_root_review') is True and obj.get('clearance') is True and
        not any(obj.get(x) is True for x in ['fixture','simulated','dry_run']),'Actual root clearance required')
    require(obj.get('new_central_proof_search_turns')==0 and obj.get('original_budget')=='2/5','Gate effort interpretation')
    require(isinstance(obj.get('exact_claim'),str) and obj['exact_claim'].strip() and obj.get('checked_artifacts'),'Gate claim/artifacts')
    require(g.utc(obj['UTC']) <= datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=5),'Gate future UTC')
    fields={'mathematics':['mathematical_clearance'],
        'priority':['priority_clearance','bounded_substantive_resolution_note_clearance','attribution_checked','no_concrete_antecedent_in_recorded_search'],
        'package':['package_clearance','metadata_and_attribution_checked'],
        'whole_package_R1':['independent_whole_package_review','zero_blocking_findings'],
        'whole_package_R2':['independent_whole_package_review','zero_blocking_findings'],
        'pre_execution_adversary':['native_scope_and_invariants_checked'],
        'final':['mathematical_clearance','priority_clearance','package_clearance','whole_package_R1_clearance',
            'whole_package_R2_clearance','native_integration_clearance','pre_execution_adversary_clearance',
            'actual_Zenodo_service_authenticated','actual_Google_Sheet_service_authenticated']}
    require(all(obj.get(x) is True for x in fields[role]),'Missing role clearance: '+role)
    if role in ['pre_execution_adversary','final']:
        require(obj.get('reviewed_program_sha256')==program_hashes,'Entire helper/worker family was not reviewed')
        require(obj.get('scoped_rank_interpretation')=='preserve_baseline_labels_and_positions_not_global_rerank','Rank interpretation gate')

class Reader:
    def __init__(self,runner,git_executable): self.runner,self.git_executable=runner,git_executable
    def run(self,argv,cap=None): return self.runner.run(argv,stdout_cap=cap)[0]
    def git(self,*args,cap=None): return self.run([self.git_executable,*args],cap)

def campaign_overlay(data,note,doi):
    require(isinstance(note,str) and len(note.split())>=8 and not any(x in note for x in ['|','\r','\n']),'Campaign note')
    lines=g.physical_lines(data.decode()); idx=[i for i,line in enumerate(lines) if '| '+K+' / '+CODE+' |' in line]
    require(len(idx)==1,'Unique campaign target'); index=idx[0]; line=lines[index]
    ending='\r\n' if line.endswith('\r\n') else '\r' if line.endswith('\r') else '\n' if line.endswith('\n') else ''
    cells=line.rstrip('\r\n').split('|')
    require(len(cells)==14 and cells[8].strip()=='queued' and cells[9].strip()=='0/5' and not cells[12].strip(),'Campaign baseline')
    cells[8],cells[9],cells[11],cells[12]=' claimed_solved ',' 2/5 ',' '+note+' ',' https://doi.org/'+doi+' '
    result=list(lines);result[index]='|'.join(cells)+ending
    require(all(a==b for i,(a,b) in enumerate(zip(lines,result)) if i!=index),'Unrelated campaign bytes')
    return ''.join(result).encode()

def zip_member(data,name,size):
    rel(name);require(len(data)<=8*1024*1024,'Archive transport cap')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        require(len(archive.infolist())<=65,'Archive entry cap')
        selected=[x for x in archive.infolist() if x.filename==name];require(len(selected)==1,'Archive member uniqueness')
        entry=selected[0];mode=entry.external_attr>>16
        require(not entry.is_dir() and not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in [0,stat.S_IFREG] and
            not entry.flag_bits&1 and entry.file_size==size,'Archive member mode/size')
        return archive.read(entry)

def validate_published_archive(data,package_files,package_bytes):
    expected={**package_files,'PACKAGE_MANIFEST.json':package_bytes}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names=[x.filename for x in archive.infolist()]
        require(len(names)==len(set(names)) and set(names)==set(expected),'Published archive exact logical inventory plus manifest')
    for name,body in expected.items():
        require(zip_member(data,name,len(body))==body,'Published archive file/manifest differs: '+name)

def publication_check(cfg,package_files,package_bytes,read):
    package_sha=sha(package_bytes)
    _,data=read(cfg['publication']['receipt']);obj=g.loads(data);doi=obj.get('DOI','')
    require(re.fullmatch(r'10\.5281/zenodo\.[1-9][0-9]*',doi),'Actual Zenodo DOI missing');record_id=doi.rsplit('.',1)[1]
    require(obj.get('schema')=='pr108-actual-publication-receipt/v2' and obj.get('actual_receipt') is True and
        obj.get('published') is True and obj.get('PR')==108 and obj.get('problem_id')==30003996 and
        obj.get('original_head')==HEAD and obj.get('effective_proof_sha256')==PROOF and obj.get('package_manifest_sha256')==package_sha and
        not any(obj.get(x) is True for x in ['fixture','simulated','dry_run']),'Publication receipt binding')
    require(type(obj.get('PID')) is int and obj['PID']>0 and obj.get('exit_code')==0 and obj.get('HTTP_method')=='GET' and
        obj.get('status_code')==200 and obj.get('URL')=='https://zenodo.org/api/records/'+record_id and
        g.utc(obj['UTC_start'])<=g.utc(obj['UTC_end']),'Actual Zenodo process/request/time')
    _,response_bytes=read(obj['metadata_response']);response=g.loads(response_bytes)
    require(str(response.get('id'))==record_id and response.get('doi')==doi and
        (response.get('submitted') is True or response.get('is_published') is True),'Actual published metadata')
    require(isinstance(obj.get('payload_readbacks'),list) and len(obj['payload_readbacks'])<=64,'Payload readback count')
    seen=set();archives=set()
    for item in obj['payload_readbacks']:
        name=rel(item['relative_path']);require(name in package_files and name not in seen,'Published payload identity');seen.add(name)
        _,downloaded=read(item['downloaded_file']);require(downloaded==package_files[name],'Published package file mismatch')
        transport=downloaded
        require(item['transport'] in ['individual_file','zip_member'],'Explicit published transport')
        if item['transport']=='zip_member':
            _,transport=read(item['archive_file']);require(zip_member(transport,item['member_path'],len(downloaded))==downloaded,'Published archive member')
            if sha(transport) not in archives:
                validate_published_archive(transport,package_files,package_bytes);archives.add(sha(transport))
        _,request_bytes=read(item['HTTP_GET_receipt']);request=g.loads(request_bytes)
        require(request.get('actual_receipt') is True and request.get('HTTP_method')=='GET' and request.get('status_code')==200 and
            type(request.get('PID')) is int and request['PID']>0 and request.get('exit_code')==0 and
            request.get('response_bytes')==len(transport) and request.get('response_sha256')==sha(transport) and
            str(request.get('URL','')).startswith('https://zenodo.org/api/records/'+record_id+'/files/') and
            g.utc(request['UTC_start'])<=g.utc(request['UTC_end']) and
            not any(request.get(x) is True for x in ['fixture','simulated','dry_run']),'Actual payload custody')
    require(seen==set(package_files),'Published payload inventory incomplete')
    return obj,doi

def prepare(config_path):
    require(config_path.absolute().is_relative_to(D),'Future actual thin config must reside in V2')
    require(regular(config_path.absolute()).st_size<=128*1024,'Config cap')
    cfg_bytes=config_path.read_bytes();thin=g.loads(cfg_bytes);g.validate_thin_config(thin)
    _,inputs_bytes=bounded_local_pin(thin['execution_inputs'],D)
    inputs=g.loads(inputs_bytes);g.validate_execution_manifest(inputs,inputs_bytes);cfg=inputs['effective'];inputs_sha=sha(inputs_bytes)
    validate_process_policy(cfg['process_policy']);validate_worker_policy(cfg['worker_policy'])
    runtime=cfg['runtime']
    require(set(runtime)=={'python_executable','python_version','python_binary','git_executable','git_binary','gh_executable','gh_binary'},'Explicit runtime choices')
    require(str(Path(sys.executable).resolve())==runtime['python_executable'] and sys.version==runtime['python_version'],'Reviewed Python runtime differs')
    for name in ['python','git','gh']:
        path=Path(runtime[name+'_executable'])
        require(path.is_absolute() and disk_pin(path)==runtime[name+'_binary'],'Reviewed runtime binary pin: '+name)
    require(set(cfg['package'])=={'root','manifest'} and set(cfg['publication'])=={'receipt'} and
        set(cfg['google_sheet'])=={'receipt','row_index','values'},'Unrepresented package/service choice')
    program_hashes={}
    require(len(inputs['program_files'])==len(g.PROGRAMS),'Program count')
    for pin in inputs['program_files']:
        path,data=bounded_local_pin(pin,D,128*1024);require(path.parent==D and path.name in g.PROGRAMS,'Program exact location')
        require(path.name not in program_hashes,'Program duplicate');program_hashes[path.name]=sha(data)
    reviewed=g.ReviewedInputs(inputs,C,A);read=reviewed.read
    base=cfg['main_parent'];require(re.fullmatch('[0-9a-f]{40}',base),'Fresh explicit main parent')
    native_pins=cfg['native_baseline_pins'];require(len(native_pins)==len(BASE_NAMES),'Native baseline count')
    base_map={}
    for pin in native_pins:
        g.pin_shape(pin);name=Path(pin['path']).name
        require(pin['path']==P+name and name in BASE_NAMES and name not in base_map and pin['bytes']<=32*1024*1024,'Native baseline exact mapping/cap')
        base_map[name]=pin
    require(set(base_map)==set(BASE_NAMES) and base_map['queue.py']['sha256']==cfg['queue_py_sha256'],'Native source code binding')
    package_root=C/rel(cfg['package']['root']);require(package_root.is_relative_to(A) and not package_root.is_relative_to(V1),'Package root distinct/future')
    _,package_bytes=read(cfg['package']['manifest']);package_sha=sha(package_bytes);package=g.loads(package_bytes)
    require(package.get('schema') in ['pr108-publication-package-manifest/v1','pr108-publication-package-manifest/v2'] and
        package.get('PR')==108 and package.get('problem_id')==30003996 and package.get('original_head')==HEAD and
        package.get('review_hash')==REVIEW and package.get('statement_hash',STATEMENT)==STATEMENT and package.get('dataset_revision')==REV and
        package.get('imported_prior_report')=={} and package.get('author_orcid')=='https://orcid.org/0009-0001-9320-500X' and
        package.get('effective_proof_sha256')==PROOF and package.get('files'),'Package bindings')
    require(len(package['files'])<=64,'Package file cap');package_files={}
    for entry in package['files']:
        name=rel(entry['relative_path']);require(name not in package_files,'Package duplicate')
        _,data=read({'path':str((package_root/name).relative_to(C)),'bytes':entry['bytes'],'sha256':entry['sha256']},package_root)
        package_files[name]=data
    require(any(sha(x)==PROOF for x in package_files.values()),'Package omits pinned effective proof')
    gates,gate_bytes={},{}
    for role in g.GATE_ROLES:
        _,data=bounded_local_pin(thin['gates'][role],A,65536);obj=g.loads(data)
        validate_gate(obj,role,package_sha,inputs_sha,program_hashes,base)
        for pin in obj['checked_artifacts']:read(pin)
        gates[role],gate_bytes[role]=obj,data
    require(len({x['exact_claim'] for x in gates.values()})==1,'Gate exact claims differ')
    require(gates['final']['gate_sha256']=={r:sha(x) for r,x in gate_bytes.items() if r!='final'},'Final gate antecedent hashes')
    require(all(isinstance(gates[r].get('reviewer_run_id'),str) and gates[r]['reviewer_run_id'].strip() for r in ['whole_package_R1','whole_package_R2']) and
        gates['whole_package_R1']['reviewer_run_id']!=gates['whole_package_R2']['reviewer_run_id'],'Two distinct whole-package reviewer runs required')
    publication,doi=publication_check(cfg,package_files,package_bytes,read)
    _,sheet_bytes=read(cfg['google_sheet']['receipt']);sheet=g.loads(sheet_bytes)
    expected={'DOI':doi,'row_index':cfg['google_sheet']['row_index'],'values':cfg['google_sheet']['values']}
    sheet_checked=g.validate_sheet(sheet,expected,publication['UTC_end'],read)
    require(g.utc(gates['final']['UTC'])>=g.utc(sheet['processes']['independent_readback']['UTC_end']),'Final service gate predates actual Sheet authentication')
    require(gates['final'].get('publication_receipt_sha256')==cfg['publication']['receipt']['sha256'] and
        gates['final'].get('google_sheet_receipt_sha256')==cfg['google_sheet']['receipt']['sha256'],'Final actual service receipt binding')
    # Original manifests and preserved files are reviewed inputs, not trusted unpinned paths.
    ap=cfg['original_authentication_pins'];require(set(ap)=={'blob_manifest','queue_projection','sourcepair','selected_prior','original_files'},'Original auth pin roles')
    for role,name in [('blob_manifest','ORIGINAL_BLOB_MANIFEST.json'),('queue_projection','QUEUE_STATUS_PROJECTION.json'),
                     ('sourcepair','SOURCEPAIR_AUTHENTICATION.json'),('selected_prior','SELECTED_IMPORTED_PRIOR_REPORT.json')]:
        require(ap[role]['path']==str((ORIGINAL/name).relative_to(C)),'Original authentication exact pathname')
    _,auth_bytes=read(ap['blob_manifest'],ORIGINAL);auth=g.loads(auth_bytes)
    _,qauth_bytes=read(ap['queue_projection'],ORIGINAL);qauth=g.loads(qauth_bytes)
    _,sourcepair_bytes=read(ap['sourcepair'],ORIGINAL);sourcepair=g.loads(sourcepair_bytes)
    _,prior_bytes=read(ap['selected_prior'],ORIGINAL);require(g.loads(prior_bytes)=={},'Selected prior must remain empty')
    require(sourcepair.get('schema')=='pr108-sourcepair-authentication/v1' and sourcepair.get('dataset_revision')==REV and
        sourcepair.get('problem_id')==30003996 and sourcepair.get('problem_code')==CODE and
        sourcepair.get('authenticated_no_join_prior_report') is True and sourcepair.get('submitted_source_equals_raw_and_SQL') is True and
        sourcepair.get('submitted_prior_equals_raw_and_SQL') is False and sourcepair.get('catalog_selected',{}).get('review_hash')==REVIEW and
        sourcepair.get('catalog_selected',{}).get('statement_hash')==STATEMENT,'Source-pair authentication binding/missing submitted prior')
    require(len(ap['original_files'])==15,'Original preserved pin count');original_files={}
    for pin in ap['original_files']:
        path,data=read(pin,ORIGINAL/'original_attempt');name=str(path.relative_to(ORIGINAL/'original_attempt'))
        require(name not in original_files,'Original duplicate');original_files[name]=data
    require(set(original_files)==g.ORIGINAL_NAMES and sha(original_files['PROOF.md'])==ORIGINAL_PROOF,'Original exact file names/proof')
    original_record=g.loads(original_files['source_record.json'])
    require(original_record.get('id')==30003996 and original_record.get('problem_number')==CODE and
        cfg['google_sheet']['values'][0]==original_record.get('source_url'),'Sheet Original Problem URL must match authenticated target source')
    effective={}
    for pin in cfg['effective_diagnostics_pins']:
        path,data=read(pin,A/'repaired_diagnostics_v1');name=str(path.relative_to(A/'repaired_diagnostics_v1'))
        require(name not in effective,'Effective duplicate');effective[name]=data
    actual_names={str(x.relative_to(A/'repaired_diagnostics_v1')) for x in (A/'repaired_diagnostics_v1').rglob('*') if x.is_file()}
    require(set(effective)==actual_names and len(effective)<=32 and sha(effective['PROOF.md'])==PROOF and
        sha(effective['verify.py'])=='46173f3fa54eae9da12a0525494b7d73d1544980cefea9040f8341340cf7385e' and
        sha(effective['independent_review/independent_checks.py'])=='a298835e88bf4a6528d3ff3d39f6036a5edfb4e6dc525cae13f3f9f631357a7c','Effective inventory/proof/diagnostic pins')
    reviewed.finish()  # ALL effective nongate receipt bodies have been captured once.
    copies=[(N+'publication/authenticated_inputs/'+str((C/path).relative_to(A)),len(data)) for path,data in reviewed.captured.items()]
    copies += [(N+'historical_original/'+name,len(data)) for name,data in original_files.items()]
    copies += [(N+('EFFECTIVE_DIAGNOSTICS_README.md' if name=='README.md' else name),len(data)) for name,data in effective.items()]
    copies += [(N+'source_record.json',len(original_files['source_record.json'])),(N+'prior_imported_report.json',len(prior_bytes)),
               (N+'publication/EXECUTION_INPUTS.json',len(inputs_bytes))]
    capacity=g.capacity_inventory(native_pins,[('bundle/'+path,size) for path,size in copies],thin['gates'],package_files,cfg['capacity_policy'],cfg['process_policy'])
    require(shutil.disk_usage(D).free>=capacity['required_free_bytes'],'Insufficient enumerated capacity/headroom; no copy/download fallback')
    output=D/('candidate_'+inputs_sha[:16]);output.mkdir(exist_ok=False)
    allowed={x['path']:x['max_bytes'] for x in capacity['entries']}
    def put(path,data):
        require(path in allowed and len(data)<=allowed[path],'Unenumerated/oversized materialization: '+path)
        target=output/path;require(not target.exists(),'Destination collision: '+path)
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    put('CONFIG.json',cfg_bytes);put('EXECUTION_INPUTS.json',inputs_bytes);put('CAPACITY_PLAN.json',encode(capacity))
    runner=BoundedRunner(output,C,cfg['process_policy']);reader=Reader(runner,runtime['git_executable'])
    def watch():
        total,count=0,0;temporary=[]
        for path in output.rglob('*'):
            require(not path.is_symlink(),'Materialized symlink')
            if path.is_file():
                name=str(path.relative_to(output));size=path.stat().st_size;total+=size;count+=1
                if name.endswith('.tmp') and name.startswith('private_native_backend/'):
                    require(Path(name).name in capacity['exclusive_atomic_write_slot_names'],'Unreviewed temporary filename')
                    temporary.append(name);require(size<=capacity['exclusive_atomic_write_slot_max_bytes'],'Atomic slot cap')
                else:require(name in allowed and size<=allowed[name],'Materialized path/file cap: '+name)
        require(len(temporary)<=1 and total<=capacity['max_materialized_bytes'] and count<=capacity['file_count_cap'],'Aggregate materialization cap')
        require(shutil.disk_usage(D).free>=capacity['headroom_bytes']+capacity['future_commit_overhead_bytes'],'Free-space headroom/future-commit reserve crossed')
    try:
        require(reader.git('rev-parse','HEAD',cap=4096).decode().strip()==base,'Main parent stale')
        require(reader.git('symbolic-ref','--short','HEAD',cap=4096).strip()==b'main','Not main')
        def remote():return reader.git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main',cap=4096).decode().split()[0]
        require(remote()==base,'Remote main changed')
        live_args=[runtime['gh_executable'],'pr','view','108','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefName,headRefOid,baseRefName,url']
        expected_live={'number':108,'state':'OPEN','isDraft':True,'headRefName':'dot/math-30003996','headRefOid':HEAD,'baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/108'}
        require(g.loads(reader.run(live_args,4096))==expected_live,'Live original PR changed')
        require(not reader.git('ls-tree','-r','--name-only',base,'--',N,cap=4096) and not (C/N).exists(),'Native attempt already exists')
        before={}
        for name,pin in base_map.items():
            data=reader.git('show',base+':'+P+name,cap=pin['bytes']+1)
            require(len(data)==pin['bytes'] and sha(data)==pin['sha256'],'Native baseline pin changed: '+name)
            local=C/P/name;require(not local.is_symlink() and (not local.exists() or disk_pin(local)=={'bytes':len(data),'sha256':sha(data)}),'Native worktree edit: '+name)
            before[name]=data
        tree=g.parse_tree(reader.git('ls-tree','-rz',HEAD,'--',N,cap=65536));original_map=g.validate_original_map(auth,tree)
        for name,data in original_files.items():
            entry=original_map[name];require(len(data)==entry['bytes'] and sha(data)==entry['sha256'] and
                reader.git('show',HEAD+':'+entry['path'],cap=len(data)+1)==data,'Original HEAD/blob pin changed')
        original_queue=reader.git('show',HEAD+':'+P+'QUEUE.md',cap=qauth['whole_QUEUE_bytes']+1)
        queue_row_sha=g.validate_original_queue(qauth,original_queue)
        manifest=g.loads(before['manifest.json']);require(manifest['revision']==REV,'Dataset revision')
        source_cache=R/P/'cache/catalog.sqlite'
        immutable_auth={x['path']: {'bytes':x['bytes'],'sha256':x['sha256']} for x in sourcepair['input_pins']}
        require(immutable_auth.get(str(source_cache))==cfg['source_cache_pin'],'Original/runtime SQL byte binding')
        for name in ['problems.json','research_results.json']:
            require(immutable_auth.get(str(R/P/'cache'/name))==cfg['raw_source_pins'][name],'Original/runtime raw byte binding')
        def sourcecheck():
            require(not any(Path(str(source_cache)+suffix).exists() for suffix in ['-wal','-shm','-journal']),'SQL writer sidecar present')
            require(disk_pin(source_cache)==cfg['source_cache_pin'],'Shared SQL byte pin changed')
            require(set(cfg['raw_source_pins'])=={'problems.json','research_results.json'},'Raw source pin roles')
            for name,pin in cfg['raw_source_pins'].items():
                require(pin==manifest['files'][name] and disk_pin(R/P/'cache'/name)==pin,'Raw source changed')
        sourcecheck()
        db=sqlite3.connect('file:'+str(source_cache)+'?mode=ro&immutable=1',uri=True)
        try:
            require(db.execute('SELECT revision FROM metadata').fetchone()==(REV,) and db.execute('SELECT count(*) FROM records').fetchone()[0]==manifest['records'],'SQL revision/count')
            raw,report=db.execute('SELECT payload,report FROM records WHERE key=?',(K,)).fetchone()
        finally:db.close()
        problem,imported=g.loads(raw),g.loads(report)
        require(imported==g.loads(prior_bytes)=={} and problem==g.loads(original_files['source_record.json']) and
            sha(json.dumps([problem,imported],sort_keys=True).encode())==REVIEW and sha(problem['statement'].encode())==STATEMENT,'SQL/raw statement/review/source pair')
        oldrows=g.loads(before['catalog.json']);row={x['id']:x for x in oldrows}[K]
        oldass,oldstate=g.loads(before['assessments.json']),g.loads(before['state.json'])
        require(K not in oldstate and row['local_status']=='queued' and row['turns_used']==0 and row['review_hash']==REVIEW and row['statement_hash']==STATEMENT,'Target baseline reconciliation required')
        assessment={**oldass[K],**cfg['assessment']}
        require(assessment.get('review_hash')==REVIEW and assessment.get('review_policy')=='2.0-five-turn-proof' and
            all(assessment.get(x)==oldass[K].get(x) for x in ['impact','p_solve','p_valid_open','route','decision','resolution','holds','clear_holds']),'Unreviewed target score/resolution/hold change')
        baseline={'schema':'pr108-dated-native-import-baseline/v2','at':now(),'id':K,'status':'claimed_solved','turns_used':2,
            'review_hash':REVIEW,'statement_hash':STATEMENT,'original_budget':'2/5','original_structured_ledger_present':False,
            'original_effort_provenance':'Authenticated QUEUE plus two-approach prose; dated 2026 audit/native-import baseline, never recovered original event.',
            'new_central_proof_search_turns':0,'original_head':HEAD,'original_queue_selected_row_sha256':queue_row_sha,
            'original_research_log_sha256':sha(original_files['RESEARCH_LOG.md'])}
        states={**oldstate,K:baseline};backend=output/'private_native_backend';backend.mkdir()
        for name,data in before.items():put('private_native_backend/'+name,data)
        (backend/'state.json').write_bytes(encode(states))
        require(not before['history.jsonl'] or before['history.jsonl'].endswith(b'\n'),'Historical terminal newline')
        with (backend/'history.jsonl').open('ab') as stream:
            stream.write((json.dumps({**baseline,'event':'dated_import_of_authenticated_historical_author_count'},ensure_ascii=False)+'\n').encode())
        assessment.update(original_budget='2/5',new_central_proof_search_turns=0,original_structured_ledger_present=False,
            publication_DOI=doi,package_manifest_sha256=package_sha)
        put('private_native_backend/assessment.json',encode(assessment))
        control={'schema':'pr108-native-assess-control/v2','fixture':False,'ROOT':str(backend),'SQL_cache':str(source_cache),
            'dataset_revision':REV,'record_count':manifest['records'],'queue_py_sha256':cfg['queue_py_sha256'],
            'execution_inputs_sha256':inputs_sha,'worker_policy':cfg['worker_policy'],
            'backend_file_caps':{Path(path).name:cap for path,cap in allowed.items() if path.startswith('private_native_backend/')}}
        put('WORKER_CONTROL.json',encode(control));watch()
        _,_,proc=runner.run([runtime['python_executable'],'-B',str(D/'native_assess_worker.py'),'--control',str(output/'WORKER_CONTROL.json')],
            stdout_cap=65536,deadline=cfg['worker_policy']['deadline_seconds'],watchdog=watch,allow_failure=True)
        require(proc['exit_code']==0 and proc['termination_reason'] is None and (output/'WORKER_RESULT.json').exists(),'Native worker failed; actual process receipt retained')
        result=g.loads((output/'WORKER_RESULT.json').read_bytes())
        require(result.get('outcome')=='success' and result.get('native_assess_returned_without_exception') is True and
            result.get('actual_operator_PID')==proc['PID'] and result.get('execution_inputs_sha256')==inputs_sha,'Actual worker success receipt')
        watch()
        afterass,afterstate=g.loads((backend/'assessments.json').read_bytes()),g.loads((backend/'state.json').read_bytes())
        require({k:v for k,v in afterass.items() if k!=K}=={k:v for k,v in oldass.items() if k!=K} and afterstate==states,'Unrelated assessment/state changed')
        for name in ['history.jsonl','assessment_history.jsonl']:
            data=(backend/name).read_bytes();require(data.startswith(before[name]) and (not before[name] or before[name].endswith(b'\n')),'Historical ledger prefix')
            extra=data[len(before[name]):].decode().splitlines();require(len(extra)==1 and g.loads(extra[0])['id']==K,'Ledger append scope/count')
        regenerated=g.loads((backend/'catalog.json').read_bytes());target={x['id']:x for x in regenerated}[K]
        require(target['local_status']=='claimed_solved' and target['turns_used']==2 and target['review_hash']==REVIEW and target['statement_hash']==STATEMENT and target['eligible'] is False,'Target projection')
        rows,drift=g.scoped_catalog(oldrows,regenerated,states,g.loads(before['policy.json']),afterass)
        (backend/'catalog.json').write_bytes(encode(rows));(backend/'ranking.csv').write_bytes(g.csv_overlay(before['ranking.csv'],target))
        (backend/'QUEUE.md').write_bytes(campaign_overlay(before['QUEUE.md'],cfg['campaign_note'],doi))
        require(('## '+K+' —').encode() not in before['SHORTLIST.md'],'Target shortlist overlay needs separate review')
        (backend/'SHORTLIST.md').write_bytes(before['SHORTLIST.md']);summary=g.loads(before['summary.json'])
        summary.update(records=len(rows),eligible=sum(x['eligible'] for x in rows),assessed=len(afterass),holds=dict(collections.Counter(h.split(':')[0] for x in rows for h in x['holds'])))
        (backend/'summary.json').write_bytes(encode(summary));watch()
        sourcecheck();require(reader.git('rev-parse','HEAD',cap=4096).decode().strip()==base and remote()==base and
            reader.git('symbolic-ref','--short','HEAD',cap=4096).strip()==b'main' and g.loads(reader.run(live_args,4096))==expected_live and not (C/N).exists(),'Final live/head/main parent comparison')
        for name,data in before.items():
            local=C/P/name;require(not local.is_symlink() and (not local.exists() or disk_pin(local)=={'bytes':len(data),'sha256':sha(data)}),'Concurrent native input edit')
        affected=[]
        def offer(path,data,old=None):
            require(path.startswith(N) or path in [P+x for x in EXPORT],'Affected path outside native allowlist')
            if data==old:return
            put('bundle/'+path,data);affected.append({'path':path,'before':None if old is None else {'bytes':len(old),'sha256':sha(old)},'after':{'bytes':len(data),'sha256':sha(data)}})
        for name in EXPORT:offer(P+name,(backend/name).read_bytes(),before[name])
        for path,data in reviewed.captured.items():offer(N+'publication/authenticated_inputs/'+str((C/path).relative_to(A)),data)
        for name,data in original_files.items():offer(N+'historical_original/'+name,data)
        for name,data in effective.items():offer(N+('EFFECTIVE_DIAGNOSTICS_README.md' if name=='README.md' else name),data)
        offer(N+'source_record.json',original_files['source_record.json']);offer(N+'prior_imported_report.json',prior_bytes)
        offer(N+'publication/EXECUTION_INPUTS.json',inputs_bytes)
        for role,data in gate_bytes.items():offer(N+'publication/gates/'+role+'.json',data)
        for name,data in package_files.items():offer(N+'publication/package/'+name,data)
        offer(N+'IMPORT_BASELINE.json',encode(baseline));offer(N+'HISTORICAL_DESK_ASSESSMENT.json',encode(oldass[K]));offer(N+'assessment.json',encode(afterass[K]))
        evidence={'original_head':HEAD,'review_hash':REVIEW,'statement_hash':STATEMENT,'dataset_revision':REV,
            'imported_prior_report':{},'original_budget':'2/5','original_structured_ledger_present':False,'new_central_proof_search_turns':0,
            'effective_proof_sha256':PROOF,'original_proof_sha256':ORIGINAL_PROOF,'exact_claim':gates['final']['exact_claim'],'DOI':doi,
            'package_manifest_sha256':package_sha,'execution_inputs_sha256':inputs_sha,'original_status_retained':'claimed_solved','Google_Sheet':sheet_checked}
        offer(N+'PUBLICATION_EVIDENCE.json',encode(evidence))
        offer(N+'README.md',('# '+K+': native attributed resolution note\n\nLiteral status claimed_solved; historical author effort 2/5. '
            'No original status.json or turns.jsonl was submitted. IMPORT_BASELINE.json is a dated 2026 audit/native import, not a recovered original structured event. '
            'New central proof-search turns: 0. The fifteen original files and their proof remain under historical_original/. Imported prior report remains {}.\n\n'
            'The clarified proof and diagnostics are source-pinned. Attributed substantive resolution-note novelty is bounded by the recorded searches; absolute first publication and still-open status in 2026 are not certified. '
            'The frozen package, final gates, actual Zenodo and actual target-row Google Sheet custody are archived under publication/. '
            'Scoped rank labels and positions preserve the established baseline; they are not a fresh global rerank. '
            'AI-assisted validation is disclosed; conventional human peer review is not claimed. DOI: https://doi.org/'+doi+'\n').encode())
        offer(N+'RESEARCH_LOG.md',('# Native import research log\n\n'+now()+': Bundle preparation 95% pending independent DIFF/readbacks and explicit export; '
            'no merge/export/commit/publication by helper. Historical 2/5 imported with provenance, original structured ledger absent; new central proof turns 0.\n').encode())
        receipt={'schema':'pr108-native-review-bundle/v2','UTC':now(),'actual_operator_PID':os.getpid(),'main_parent':base,'original_head':HEAD,
            'live_head':HEAD,'config_sha256':sha(cfg_bytes),'execution_inputs_sha256':inputs_sha,'reviewed_program_sha256':program_hashes,
            'native_status':'claimed_solved','turns_used':2,'original_structured_ledger_present':False,'new_central_proof_search_turns':0,
            'native_assess_executed_in_private_backend':True,'native_worker_process_PID':proc['PID'],'unrelated_catalog_projection_drift_preserved':drift,
            'scoped_rank_interpretation':cfg['scoped_rank_interpretation'],'DOI':doi,'Google_Sheet':sheet_checked,'affected_paths':affected,
            'native_export_executed':False,'Git_index_branch_remote_or_service_mutated':False,'merge_executed':False,
            'publication_executed_by_helper':False,'parent_review_and_explicit_export_required':True}
        receipt['post_execution_free_bytes']=shutil.disk_usage(D).free
        put('CANDIDATE_RECEIPT.json',encode(receipt));watch()
        print(json.dumps({'candidate':str(output),'affected_path_count':len(affected),'native_export_executed':False}))
    except BaseException as error:
        failure={'schema':'pr108-actual-prepare-failure/v2','UTC':now(),'actual_operator_PID':os.getpid(),
            'execution_inputs_sha256':inputs_sha,'error_type':type(error).__name__,'error':str(error)[:1200],
            'candidate_must_not_be_exported':True,'native_export_executed':False}
        path=output/'PREPARE_FAILURE.json';data=encode(failure)
        require(len(data)<=allowed['PREPARE_FAILURE.json'],'Failure receipt cap');path.write_bytes(data)
        raise

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--config',type=Path,required=True)
    prepare(parser.parse_args().config)
