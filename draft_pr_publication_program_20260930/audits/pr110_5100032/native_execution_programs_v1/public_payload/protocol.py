"""PR110 pure offline protocol and scoped overlays. No I/O or execution entry point.

Caller supplies authenticated immutable bytes. Structural validation does not prove
service authenticity; the independently reviewed root attestation remains required.
All checks use explicit exceptions and remain effective with Python optimization.
"""
import collections, csv, datetime, hashlib, io, json, re, stat, zipfile
from pathlib import PurePosixPath
from urllib.parse import urlsplit

K, CODE = '5100032', 'AMR-050-0032'
HEAD = '3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35'
REV = '37e53eabe540fb458758e198be61634bd02ee008'
REVIEW = '8c27c02e2166d29815cdd362f6b62e398684393679565c5033e616e7e8ac467d'
STATEMENT = 'cb9077b72de618c4d0dba292a8b4cedd3d06993b0f38897b644e1ee44e56dd1b'
ORIGINAL_PROOF = '8478d2a792944c5fb9e8a53324e0c6bce8eba317de29c31a6fcbd6ca0205709d'
SOURCE_PIN = {'bytes':3926,'sha256':'488f04aa9db8b1bb428d3331b96773786cfbd3cfe225192f5182941edfbef1c5'}
PRIOR_PIN = {'bytes':2977,'sha256':'e08288b320663363873db0ad9c67de1cd4557bc82315be672d26f0f1bd425b0f'}
ORIGINAL_MANIFEST_PIN = {'bytes':7595,'sha256':'6b8bec0003cca392fe9fd2e6f558d212ec4d1a0c0dea0c40790b1ee3e38a5f62'}
ORIGINAL_QUEUE_PIN = {'bytes':369655,'sha256':'5a8bdd830dc67a9c58d3c75e6fac9b81f0e6ebece83955b52c724d6fedd75f9b'}
SOURCEPAIR_AUTH_PIN = {'bytes':2951,'sha256':'dfe6e436ddb92a93d73734a1af383980b3784eafe161745a8ef94723a374eef9'}
ORIGINAL_ROW_SHA = '60934e0282d754524af8012cd5aab27d3e847d7b9eb8a57553ef452f5a0b3c14'
ORIGINAL_LOG_SHA = 'd3e44c3d463e16018f0c48671f65ebe6fb516bba987e2638ea0112027bac4ebb'
QUEUE_SHA = 'f72aee023f837bad092da58531c2cc069ce2cf094e835d090221107d20f07ab2'
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
SHEET_TITLE, SHEET_GID = 'Math Puzzles', 1254632077
COLUMNS = ['Original Problem','Solution Chat URL','DOI','Notes']
CLAIM = ('For every regular closed billiard/Poncelet orbit between an outer ellipse a>b>0 and a fixed strictly nested confocal ellipse 0<lambda<b², '
         'the sums of ordinary Euclidean distances from each outer focus to consecutive antipedal supporting-line intersections are finite, positive and equal; '
         'literal k603 ratio1, all admissible periods/windings, including stars, reversals and repeated traversals.')
NATIVE = ['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json',
          'history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
DERIVED = ['assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json',
           'ranking.csv','summary.json','QUEUE.md']
ROLES = ['mathematics','priority','package','whole_package_R1','whole_package_R2','pre_execution_adversary','final']
ORIGINAL_NAMES = {'PROOF.md','README.md','RESEARCH_LOG.md','SHA256SUMS','source_manifest.json','source_record.json',
 'prior_imported_report.json','verification.json','verify.py','independent_review/REVIEW.md',
 'independent_review/review_summary.json','independent_review/independent_results.json','independent_review/independent_checks.py',
 'independent_review/source_verification.json','independent_review/author_replay/PROOF.md',
 'independent_review/author_replay/verify.py','independent_review/author_replay/verification.json'}
ASSESSMENT_METADATA = {'note','rationale','remaining_gap','first_experiment','sources',
 'original_budget','new_central_proof_search_turns','original_structured_ledger_present',
 'publication_DOI','package_manifest_sha256','native_import_provenance'}

def need(ok, message):
    if not ok: raise ValueError(message)
def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode()
def equal(left, right): return canonical(left)==canonical(right)
def sha(body): return hashlib.sha256(body).hexdigest()
def pin(body): return {'bytes':len(body),'sha256':sha(body)}
def loads(body):
    def pairs(values):
        out={}
        for key,value in values:
            need(key not in out,'Duplicate JSON key');out[key]=value
        return out
    def invalid(value): raise ValueError('Nonfinite JSON constant: '+value)
    return json.loads(body, object_pairs_hook=pairs, parse_constant=invalid)
def stamp(value):
    need(isinstance(value,str),'UTC text required')
    time=datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
    need(time.utcoffset()==datetime.timedelta(0),'UTC offset required')
    return time
def relative(value):
    need(isinstance(value,str) and value and len(value.encode())<=512 and '\\' not in value and
         not any(ord(c)<32 or ord(c)==127 for c in value),'Path text')
    path=PurePosixPath(value)
    need(not path.is_absolute() and '..' not in path.parts and str(path)==value,'Canonical relative path')
    return value
def pin_shape(value):
    need(isinstance(value,dict) and set(value)=={'path','bytes','sha256'},'Exact file pin')
    relative(value['path'])
    need(type(value['bytes']) is int and value['bytes']>=0 and isinstance(value['sha256'],str) and
         re.fullmatch('[0-9a-f]{64}',value['sha256']),'File size/hash')
def actual(value):
    need(value.get('actual_receipt') is True and value.get('template_only') is False and
         all(value.get(k,False) is False for k in ['fixture','simulated','dry_run']),'Genuine future receipt required')
def https(value):
    if not isinstance(value,str) or not value or any(ord(c)<33 or ord(c)==127 or c=='\\' for c in value): return False
    try:
        u=urlsplit(value)
        return u.scheme=='https' and bool(u.hostname) and u.username is None and u.password is None and (u.port is None or 1<=u.port<=65535)
    except ValueError: return False

class Inputs:
    """Pure byte registry; every body must be declared, pinned and consumed."""
    def __init__(self, specs, bodies):
        need(isinstance(specs,list) and 1<=len(specs)<=256,'Input count')
        self.specs={};self.used=set();self.bodies=bodies
        for spec in specs:
            pin_shape(spec);need(spec['path'] not in self.specs,'Duplicate input')
            self.specs[spec['path']]=spec
        need(set(bodies)==set(self.specs),'Undeclared/missing input bodies')
    def read(self,spec):
        pin_shape(spec)
        need(equal(self.specs.get(spec['path']),spec),'Undeclared or changed pin')
        body=self.bodies[spec['path']]
        need(type(body) is bytes and equal(pin(body),{k:spec[k] for k in ['bytes','sha256']}),'Input byte drift')
        self.used.add(spec['path']);return body
    def obj(self,spec): return loads(self.read(spec))
    def finish(self): need(self.used==set(self.specs),'Unused execution input')

def sourcepair(source,prior):
    need(equal(pin(source),SOURCE_PIN),'Original source drift')
    need(equal(pin(prior),PRIOR_PIN),'Nonempty original prior byte drift')
    p,r=loads(source),loads(prior)
    need(isinstance(r,dict) and bool(r),'Nonempty imported prior required')
    need(str(p['id'])==K and p['problem_number']==CODE and sha(p['statement'].encode())==STATEMENT and
         sha(json.dumps([p,r],sort_keys=True).encode())==REVIEW,'Full sourcepair/hash binding')
    return p,r

def validate_original(original,read):
    need(set(original)=={'manifest','queue','sourcepair_authentication','files'},'Original choices')
    inventory_bytes=read.read(original['manifest']);need(pin(inventory_bytes)==ORIGINAL_MANIFEST_PIN,'Immutable original inventory drift')
    inventory=loads(inventory_bytes)
    need(inventory['original_head']==HEAD and inventory['PR']==110 and inventory['original_literal_status']=='claimed_solved' and
         inventory['original_budget']=='2/5' and inventory['file_count']==17,'Original identity/effort')
    files=original['files'];need(set(files)==ORIGINAL_NAMES,'Exact original seventeen-file inventory')
    entries={x['relative_path']:x for x in inventory['files']}
    need(set(entries)==ORIGINAL_NAMES and len(inventory['files'])==17,'Original manifest inventory')
    bodies={}
    for name,spec in files.items():
        body=read.read(spec);entry=entries[name]
        need(entry['git_mode']=='100644' and entry['source_path']=='unsolved_math_prioritization/attempts/'+K+'/'+name and
             equal(pin(body),{'bytes':entry['bytes'],'sha256':entry['sha256']}) and
             hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==entry['git_blob_oid'],'Original Git/blob binding')
        bodies[name]=body
    source,prior=sourcepair(bodies['source_record.json'],bodies['prior_imported_report.json'])
    need(sha(bodies['PROOF.md'])==ORIGINAL_PROOF,'Original proof binding')
    queue=read.read(original['queue']);need(pin(queue)==ORIGINAL_QUEUE_PIN,'Immutable original QUEUE drift');row=inventory['original_queue_row']
    need(equal(pin(queue),{'bytes':inventory['queue_bytes'],'sha256':inventory['queue_sha256']}) and
         queue.decode().splitlines().count(row)==1,'Original QUEUE byte/row binding')
    cells=row.split('|')
    need(len(cells)==14 and cells[2].strip()==K+' / '+CODE and cells[8].strip()=='claimed_solved' and cells[9].strip()=='2/5','Original literal row')
    auth_bytes=read.read(original['sourcepair_authentication']);need(pin(auth_bytes)==SOURCEPAIR_AUTH_PIN,'Immutable original sourcepair authentication drift')
    auth=loads(auth_bytes)
    need(auth['problem_id']==5100032 and auth['dataset_revision']==REV and auth['submitted_prior_equals_raw_and_SQL'] is True and
         auth['submitted_source_equals_raw_and_SQL'] is True and auth['authenticated_no_join_prior_report'] is False,'Original sourcepair authentication')
    return bodies,source,prior

def process(record,read,parse_json=True):
    actual(record)
    need(type(record.get('PID')) is int and record['PID']>0 and type(record.get('exit_code')) is int and record['exit_code']==0,
         'Actual successful process required')
    need(isinstance(record.get('argv'),list) and record['argv'] and all(isinstance(x,str) for x in record['argv']),'Process argv')
    need(isinstance(record.get('cwd'),str) and record['cwd'].startswith('/') and
         isinstance(record.get('environment_sha256'),str) and re.fullmatch('[0-9a-f]{64}',record['environment_sha256']),'Process cwd/environment custody')
    start,end=stamp(record['UTC_start']),stamp(record['UTC_end'])
    need(stamp('2026-10-06T00:00:00Z')<=start<=end,'Process chronology/current program boundary')
    response=read.read(record['stdout']);stderr=read.read(record['stderr'])
    need(len(stderr)<=65536 and record.get('reaped') is True and record.get('termination_reason') is None,'Process termination/custody')
    return loads(response) if parse_json else response,start,end

def publication(obj,package,read):
    actual(obj)
    doi=obj.get('DOI','');need(re.fullmatch(r'10\.5281/zenodo\.[1-9][0-9]*',doi),'Actual Zenodo DOI')
    need(obj['schema']=='pr110-actual-publication-receipt/v1' and obj['PR']==110 and obj['problem_id']==5100032 and
         obj['original_head']==HEAD and obj['package_manifest_sha256']==package['manifest']['sha256'] and obj['published'] is True,
         'Publication/package/target binding')
    record_id=doi.rsplit('.',1)[1]
    response,start,end=process(obj['metadata_GET'],read);metadata_end=end
    need(obj['metadata_GET']['HTTP_method']=='GET' and obj['metadata_GET']['status_code']==200 and
         obj['metadata_GET']['URL']=='https://zenodo.org/api/records/'+record_id,'Zenodo metadata request')
    need(str(response.get('id'))==record_id and response.get('doi')==doi and
         (response.get('submitted') is True or response.get('is_published') is True),'Published Zenodo metadata')
    expected=package['logical_inventory'];need(isinstance(expected,dict) and 1<=len(expected)<=64,'Package inventory cap')
    need(isinstance(obj['logical_readbacks'],dict) and set(obj['logical_readbacks'])==set(expected),'Complete published payload inventory')
    for name,spec in expected.items():
        relative(name);body=read.read(spec);item=obj['logical_readbacks'][name]
        need(equal(pin(read.read(item['body'])),pin(body)),'Published logical payload differs')
        transport=read.read(item['transport_body']);request=item['GET']
        need(item['transport'] in ['individual_file','zip_member'],'Explicit payload transport')
        if item['transport']=='individual_file': need(transport==body,'Individual published transport differs')
        else:
            need(len(transport)<=16*1024*1024,'Published ZIP byte cap')
            with zipfile.ZipFile(io.BytesIO(transport)) as archive:
                entries=archive.infolist();names=[e.filename for e in entries]
                need(len(names)==len(set(names)) and set(names)==set(expected),'Published ZIP exact logical inventory')
                for entry in entries:
                    relative(entry.filename);mode=entry.external_attr>>16
                    need(not entry.is_dir() and not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in [0,stat.S_IFREG] and
                         not entry.flag_bits&1 and entry.file_size==expected[entry.filename]['bytes'],'Published ZIP member mode/size')
                    need(pin(archive.read(entry))=={k:expected[entry.filename][k] for k in ['bytes','sha256']},'Published ZIP member differs')
                need(item['member_path']==name and archive.read(name)==body,'Published ZIP member binding')
        result,s,e=process(request,read)
        need(request['HTTP_method']=='GET' and request['status_code']==200 and
             request['URL'].startswith('https://zenodo.org/api/records/'+record_id+'/files/') and
             request['response_sha256']==sha(transport) and request['response_bytes']==len(transport),'Published transport request')
        need(result.get('response_sha256')==sha(transport) and result.get('response_bytes')==len(transport),'Payload capture stdout/body binding')
        need(s>=metadata_end,'Payload readback precedes actual record authentication')
        end=max(end,e)
    return doi,start,end

def gws(record,verb,read):
    response,start,end=process(record,read);argv=record['argv']
    need(PurePosixPath(argv[0]).name=='gws' and argv[1:1+len(verb)]==verb,'Exact GWS verb')
    tail=argv[1+len(verb):];flags=['--params']+(['--json'] if verb[-1]=='append' else [])
    need(len(tail)==2*len(flags) and tail[::2]==flags,'Exact GWS flags')
    params=loads(tail[1]);need(params['spreadsheetId']==SHEET and pin(tail[1].encode())==record['params_pin'],'GWS params binding')
    body=loads(tail[3]) if len(flags)==2 else None
    if body is not None: need(pin(tail[3].encode())==record['json_pin'],'GWS append body pin')
    return params,body,response,start,end

def sheet(obj,doi,source,zenodo_end,read):
    actual(obj)
    need(obj['schema']=='pr110-actual-gws-sheet-receipt/v1' and obj['problem_id']==5100032 and obj['problem_code']==CODE and
         obj['original_head']==HEAD and obj['DOI']==doi and obj['spreadsheet_id']==SHEET and
         obj['sheet_id']==SHEET_GID and obj['sheet_title']==SHEET_TITLE and obj['columns']==COLUMNS,'Sheet identity')
    row=obj['row_index'];need(type(row) is int and row>=2,'Actual Sheet row')
    selected="'Math Puzzles'!A"+str(row)+':D'+str(row)
    values=obj['values'];need(obj['range']==selected and isinstance(values,list) and len(values)==4 and
         all(isinstance(x,str) for x in values),'Exact Sheet range/cells')
    source_url=source.get('source_url') or re.search(r'Source URL:\s*(https?://[^\s<>]+)',source.get('background','')).group(1)
    need(values[0]==source_url and https(values[0]) and values[2]=='https://doi.org/'+doi and
         K+' / '+CODE in values[3] and values[3].strip(),'Source/DOI/Notes cells')
    need(values[1]=='' or (obj.get('existing_chat_authorized') is True and https(values[1])),'Only blank or existing authorized chat URL')
    records=obj['processes'];need(set(records)=={'metadata','header','append','readback','independent_readback'},'Five actual GWS operations')
    need(len({r['PID'] for r in records.values()})==5,'Distinct actual GWS process PIDs')
    end=zenodo_end
    for role in ['metadata','header','append','readback','independent_readback']:
        verb=['sheets','spreadsheets','get'] if role=='metadata' else ['sheets','spreadsheets','values','append' if role=='append' else 'get']
        params,body,response,start,finish=gws(records[role],verb,read)
        need(start>=end,'Publication-before-Sheets ordered service custody');end=finish
        if role=='metadata':
            need(response.get('spreadsheetId')==SHEET and any(x['properties']['sheetId']==SHEET_GID and
                 x['properties']['title']==SHEET_TITLE for x in response['sheets']),'Sheet metadata readback')
        elif role=='header':
            need(params.get('range')=="'Math Puzzles'!A1:D1" and response['values']==[COLUMNS],'Sheet columns readback')
        elif role=='append':
            need(equal(params,{'spreadsheetId':SHEET,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW',
                 'insertDataOption':'INSERT_ROWS','includeValuesInResponse':True}) and equal(body,{'majorDimension':'ROWS','values':[values]}),'Exact append operation')
            u=response['updates'];need(all(type(u[k]) is int for k in ['updatedRows','updatedColumns','updatedCells']) and
                 u['updatedRange']==selected and u['updatedRows']==1 and u['updatedColumns']==4 and
                 u['updatedCells']==4 and u['updatedData']['values']==[values],'Actual appended range/readback')
        else: need(params=={'spreadsheetId':SHEET,'range':selected} and response['range']==selected and response['values']==[values],'Exact row readback')
    return selected,end

def validate_execution(document_bytes,bodies,gates,program_hashes,now):
    """Structural preconditions only. Never authorizes, launches or accepts a run."""
    doc=loads(document_bytes)
    need(set(doc)=={'schema','template_only','execution_mode','effective','input_files','program_hashes'} and
         doc['schema']=='pr110-native-integration-inputs/v1' and doc['template_only'] is False and
         doc['execution_mode']=='offline_candidate_verification_only','Non-template offline execution inputs')
    need(document_bytes==canonical(doc),'Exact canonical execution bytes')
    need(equal(doc['program_hashes'],program_hashes) and set(program_hashes)=={'protocol.py','native_worker.py','native_runner.py','native_launcher.sh'},'Exact reviewed helper/adapter/runner/launcher family')
    need(all(isinstance(value,str) and re.fullmatch('[0-9a-f]{64}',value) for value in program_hashes.values()),'Helper source hash shape')
    x=doc['effective'];need(set(x)=={'main_parent','target','native_before','original','package','publication_receipt','sheet_receipt',
         'runtime','preflight_receipt','preflight_process_contracts','service_process_contracts','native_run_contract',
         'assessment_overlay','campaign_note','attempt_inventory','scope_policy'},'Every effective choice explicit')
    need(re.fullmatch('[0-9a-f]{40}',x['main_parent']) and equal(x['target'],{'PR':110,'id':K,'code':CODE,'original_head':HEAD,
         'literal_status':'claimed_solved','turns_used':2,'new_central_proof_search_turns':0,'review_hash':REVIEW,
         'statement_hash':STATEMENT,'dataset_revision':REV,'exact_claim':CLAIM}),'Literal target/full claim binding')
    need(x['scope_policy']=='preserve_unrelated_bytes_records_ranks_and_positions','Scoped preservation policy')
    need(stamp(now)>=stamp('2026-10-06T00:00:00Z'),'Future invocation UTC')
    inputs=Inputs(doc['input_files'],bodies)
    need(set(x['native_before'])==set(NATIVE),'Complete native baseline')
    before={name:inputs.read(spec) for name,spec in x['native_before'].items()}
    need(sha(before['queue.py'])==QUEUE_SHA,'Native runtime changed; fresh protocol adaptation required')
    manifest=loads(before['manifest.json']);need(manifest['revision']==REV and manifest['records']==15458,'Native revision/record count')
    cat=loads(before['catalog.json']);ass=loads(before['assessments.json']);states=loads(before['state.json'])
    need(isinstance(cat,list) and len(cat)==manifest['records'] and len({r['id'] for r in cat})==len(cat) and
         K not in states and K in ass,'Complete baseline and absent target state')
    target=next((r for r in cat if r['id']==K),{})
    need(target.get('local_status')=='queued' and type(target.get('turns_used')) is int and target['turns_used']==0 and
         target['review_hash']==REVIEW and target['statement_hash']==STATEMENT and target['present'] is True and
         target['holds']==[] and ass[K]['review_hash']==REVIEW,'Fresh target queued0 baseline')
    original,source,prior=validate_original(x['original'],inputs)
    runtime=x['runtime'];need(set(runtime)=={'python','git','gws','gh','sh','queue_sha256','startup_policy','private_config_metadata'} and
         runtime['queue_sha256']==QUEUE_SHA and equal(runtime['startup_policy'],{'python_flags':['-E','-S','-B'],'ambient_environment_inherited':False}),'Runtime/startup pins')
    for role in ['python','git','gws','gh','sh']:
        p=runtime[role];need(set(p)=={'absolute_path','bytes','sha256','version'} and p['absolute_path'].startswith('/') and
             type(p['bytes']) is int and p['bytes']>0 and re.fullmatch('[0-9a-f]{64}',p['sha256']) and
             isinstance(p['version'],str) and bool(p['version'].strip()),'Full runtime pin')
    need(isinstance(runtime['private_config_metadata'],list) and runtime['private_config_metadata'],'Private runtime/config metadata pins')
    for p in runtime['private_config_metadata']:
        need(set(p)=={'absolute_path','bytes','sha256','body_private'} and p['absolute_path'].startswith('/') and
             type(p['bytes']) is int and p['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',p['sha256']) and p['body_private'] is True,'Private config pin')
    package=x['package'];need(set(package)=={'manifest','logical_inventory','effective_proof','transport_inventory_receipt'},'Package choices')
    package_bytes=inputs.read(package['manifest']);loads(package_bytes)
    need(package['manifest'] in package['logical_inventory'].values(),'Manifest included in exact package inventory')
    need(bool(inputs.read(package['effective_proof'])) and package['effective_proof'] in package['logical_inventory'].values(),'Effective proof in package')
    transport=inputs.obj(package['transport_inventory_receipt']);actual(transport)
    need(transport['package_manifest_sha256']==sha(package_bytes) and transport['exact_logical_inventory']==package['logical_inventory'] and
         transport['no_missing_duplicate_extra_or_unsafe_archive_members'] is True,'Exact transport inventory authentication')
    pub=inputs.obj(x['publication_receipt']);doi,zstart,zend=publication(pub,package,inputs)
    sh=inputs.obj(x['sheet_receipt']);selected,send=sheet(sh,doi,source,zend,inputs)
    service_records={'zenodo.metadata':pub['metadata_GET'],
                     **{'zenodo.payload.'+name:item['GET'] for name,item in pub['logical_readbacks'].items()},
                     **{'gws.'+role:record for role,record in sh['processes'].items()}}
    service_contracts=x['service_process_contracts']
    need(isinstance(service_contracts,dict) and set(service_contracts)==set(service_records),'All exact service process contracts')
    for role,record in service_records.items():
        contract=service_contracts[role]
        need(set(contract)=={'argv','cwd','environment_sha256','executable_role','program_inputs'} and
             contract['executable_role'] in ['python','gws'] and
             contract['argv'][0]==runtime[contract['executable_role']]['absolute_path'] and
             (not role.startswith('gws.') or contract['executable_role']=='gws') and
             all(equal(record[key],contract[key]) for key in ['argv','cwd','environment_sha256']),'Exact service command/runtime contract')
        need(isinstance(contract['program_inputs'],list),'Service program input pins')
        for spec in contract['program_inputs']: inputs.read(spec)
    pre=inputs.obj(x['preflight_receipt']);actual(pre)
    sourceauth=inputs.obj(x['original']['sourcepair_authentication'])
    original_raw={item['path'].rsplit('/',1)[-1]:{key:item[key] for key in ['bytes','sha256']}
                  for item in sourceauth['input_pins'] if '/cache/' in item['path']}
    need(pre['schema']=='pr110-actual-main-source-runtime-preflight/v1' and pre['main_parent']==x['main_parent'] and
         pre['remote_main']==x['main_parent'] and pre['branch']=='main' and pre['live_PR_head']==HEAD and
         pre['live_PR_base']=='main' and pre['live_PR_number']==110 and pre['live_PR_state']=='OPEN' and pre['live_PR_isDraft'] is True and
         pre['source_review_hash']==REVIEW and pre['source_statement_hash']==STATEMENT and pre['dataset_revision']==REV and
         pre['SQL_prior_equals_nonempty_original'] is True and pre['SQL_source_equals_original'] is True and
         pre['SQL_revision']==REV and type(pre['SQL_record_count']) is int and pre['SQL_record_count']==manifest['records'] and
         equal(pre['source_cache_pin'],original_raw['catalog.sqlite']) and
         equal(pre['raw_source_pins'],{name:original_raw[name] for name in ['problems.json','research_results.json']}) and
         equal(pre['raw_source_pins'],manifest['files']) and
         pre['native_target_absent'] is True and pre['SQL_sidecars_absent'] is True and equal(pre['runtime'],runtime) and
         equal(pre['native_before'],x['native_before']) and pre['root_independently_authenticated_processes'] is True,'Fresh full main/source/runtime preflight')
    pretime=stamp(pre['UTC']);need(pretime>=send and pretime<=stamp(now),'Post-service fresh preflight chronology')
    run=x['native_run_contract']
    need(set(run)=={'program_sources','program_staging','workspace_root','worker_launch','runner_launch','launcher_launch','launcher_shell',
         'resource_limits','parent_watchdog','read_only_SQL_pin','native_baseline','allowed_native_output_names','mode'},'Exact future native-run contract')
    need(run['mode']=='private_native_assess_then_scoped_offer_only' and
         run['read_only_SQL_pin']==pre['source_cache_pin'] and equal(run['native_baseline'],x['native_before']) and
         set(run['program_sources'])=={'native_worker.py','native_runner.py','native_launcher.sh'},'Pinned read-only native adapter inputs')
    for name,spec in run['program_sources'].items():
        source=inputs.read(spec);need(bool(source) and sha(source)==program_hashes[name],'Entire actual native program family pin')
    workspace=run['workspace_root'];anchor=str(PurePosixPath(__file__).parent)+'/future_candidates/'
    need(isinstance(workspace,str) and workspace.startswith(anchor) and
         re.fullmatch('[A-Za-z0-9_-]{1,80}',workspace[len(anchor):]),'Dedicated future private candidate workspace')
    need(run['launcher_shell']=='/bin/sh' and run['allowed_native_output_names']==NATIVE+['assessment.json'],'Exact native output names/launcher')
    need(runtime['sh']['absolute_path']=='/bin/sh' and equal(run['program_staging'],{
      'native_worker.py':workspace+'/worker.py','native_runner.py':workspace+'/runner.py','native_launcher.sh':workspace+'/launcher.sh'}),
      'Exact source-to-staged-program correspondence')
    for role in ['worker','runner']:
        launch=run[role+'_launch']
        need(set(launch)=={'argv','cwd','environment'} and launch['cwd']==workspace and
             launch['argv']==[runtime['python']['absolute_path'],'-E','-S','-B',workspace+'/'+role+'.py','--control',workspace+'/CONTROL.json'] and
             isinstance(launch['environment'],dict) and launch['environment'].get('PATH')=='/usr/bin:/bin' and
             launch['environment'].get('LC_ALL')=='C' and launch['environment'].get('LANG')=='C' and launch['environment'].get('TZ')=='UTC' and
             all(isinstance(v,str) for v in launch['environment'].values()) and
             set(launch['environment'])<={'PATH','LC_ALL','LANG','TZ','__CF_USER_TEXT_ENCODING'},'Exact future clean native startup')
    launcher=run['launcher_launch']
    need(set(launcher)=={'argv','cwd','environment'} and launcher['cwd']==workspace and
         equal(launcher['environment'],run['runner_launch']['environment']) and
         launcher['argv']==['/bin/sh',workspace+'/launcher.sh',runtime['python']['absolute_path'],workspace+'/runner.py',
                            '--control',workspace+'/CONTROL.json'],'Exact pinned shell launcher invocation')
    limits=run['resource_limits'];watch=run['parent_watchdog']
    need(set(limits)=={'CPU_seconds','FSIZE_bytes','NOFILE','memory_advisory_bytes','Darwin_hard_memory_limit_claimed'} and
         all(type(limits[k]) is int and limits[k]>0 for k in ['CPU_seconds','FSIZE_bytes','NOFILE','memory_advisory_bytes']) and
         limits['CPU_seconds']<=120 and limits['NOFILE']<=128 and limits['Darwin_hard_memory_limit_claimed'] is False,'Explicit future native resource limits')
    need(set(watch)=={'deadline_seconds','stdout_cap_bytes','stderr_cap_bytes','free_headroom_bytes','future_commit_reserve_bytes',
         'runtime_reserve_bytes','allocation_cap_bytes','file_count_cap','TERM_then_KILL_and_reap'} and
         all(type(v) is int and v>0 for k,v in watch.items() if k!='TERM_then_KILL_and_reap') and
         watch['deadline_seconds']<=120 and watch['stderr_cap_bytes']<=65536 and watch['file_count_cap']<=512 and
         watch['allocation_cap_bytes']<=160*1024*1024 and watch['free_headroom_bytes']>=32*1024*1024 and
         watch['future_commit_reserve_bytes']>=8*1024*1024 and watch['runtime_reserve_bytes']>=8*1024*1024 and
         watch['TERM_then_KILL_and_reap'] is True,'Bounded future parent watchdog/capacity contract')
    contracts=x['preflight_process_contracts']
    need(isinstance(contracts,dict) and set(contracts)=={'local_main','remote_main','live_PR','source_and_runtime'},'Four exact preflight command contracts')
    need(isinstance(pre['processes'],list) and len(pre['processes'])==4 and
         {r['role'] for r in pre['processes']}==set(contracts) and len({r['PID'] for r in pre['processes']})==4,'Actual preflight role/PID custody')
    for record in pre['processes']:
        contract=contracts[record['role']]
        need(set(contract)=={'argv','cwd','environment_sha256','executable_role','program_inputs'} and
             contract['executable_role'] in ['python','git','gh'] and
             contract['argv'][0]==runtime[contract['executable_role']]['absolute_path'] and
             all(equal(record[key],contract[key]) for key in ['argv','cwd','environment_sha256']),'Exact pinned preflight command/runtime contract')
        need(isinstance(contract['program_inputs'],list),'Preflight program input pins')
        for spec in contract['program_inputs']: inputs.read(spec)
        _,start,end=process(record,inputs,parse_json=False)
        need(send<=start<=end<=pretime<=stamp(now),'Fresh bounded preflight process chronology')
    need(isinstance(x['attempt_inventory'],list) and x['attempt_inventory'] and
         len(set(x['attempt_inventory']))==len(x['attempt_inventory']) and
         all(relative(path).startswith('unsolved_math_prioritization/attempts/'+K+'/') for path in x['attempt_inventory']), 'Exact scoped future attempt paths')
    prefix='unsolved_math_prioritization/attempts/'+K+'/'
    required_attempt={prefix+'historical_original/'+name for name in ORIGINAL_NAMES}|{
      prefix+name for name in ['source_record.json','prior_imported_report.json','IMPORT_BASELINE.json',
                             'HISTORICAL_DESK_ASSESSMENT.json','assessment.json','PUBLICATION_EVIDENCE.json','README.md','RESEARCH_LOG.md']}
    need(required_attempt<=set(x['attempt_inventory']),'Mandatory preserved original/source/prior/provenance offer paths')
    need(set(x['assessment_overlay'])<=ASSESSMENT_METADATA and x['assessment_overlay'].get('original_budget')=='2/5' and
         type(x['assessment_overlay'].get('new_central_proof_search_turns')) is int and x['assessment_overlay']['new_central_proof_search_turns']==0 and
         x['assessment_overlay'].get('original_structured_ledger_present') is False and
         x['assessment_overlay'].get('publication_DOI')==doi and x['assessment_overlay'].get('package_manifest_sha256')==sha(package_bytes),'Assessment metadata and effort binding')
    need(isinstance(x['campaign_note'],str) and len(x['campaign_note'].split())>=8 and not any(c in x['campaign_note'] for c in '|\r\n'),'Reviewed campaign note')
    need(set(gates)==set(ROLES),'All seven actual review gates')
    expected={'execution_inputs_sha256':sha(document_bytes),'main_parent':x['main_parent'],'original_head':HEAD,
              'review_hash':REVIEW,'statement_hash':STATEMENT,'package_manifest_sha256':sha(package_bytes),'exact_claim':CLAIM}
    decoded={role:loads(body) for role,body in gates.items()}
    for role,gate in decoded.items():
        actual(gate)
        need(gate['schema']=='pr110-root-native-input-review/v1' and gate['role']==role and gate['PR']==110 and gate['problem_id']==5100032 and
             all(equal(gate.get(k),v) for k,v in expected.items()) and gate['clearance'] is True and gate['actual_root_review'] is True and
             gate['original_budget']=='2/5' and type(gate['new_central_proof_search_turns']) is int and
             gate['new_central_proof_search_turns']==0 and gate['checked_artifacts'],'Fresh manifest-bound root review gate')
        need(pretime<=stamp(gate['UTC'])<=stamp(now),'Fresh manifest-bound gate timestamp')
        need(isinstance(gate['checked_artifacts'],list) and gate['checked_artifacts'],'Gate checked artifacts')
        for artifact in gate['checked_artifacts']: inputs.read(artifact)
    need(decoded['mathematics']['mathematical_clearance'] is True,'Mathematical clearance')
    need(decoded['priority']['bounded_priority_clearance'] is True and decoded['priority']['source_observation_credited'] is True and
         decoded['priority']['absolute_priority_claimed'] is False,'Bounded attributed novelty')
    need(decoded['package']['package_clearance'] is True,'Package clearance')
    r1,r2=decoded['whole_package_R1'],decoded['whole_package_R2']
    need(r1['reviewer_run_id']!=r2['reviewer_run_id'] and all(r['independent_whole_package_review'] is True and
         r['zero_blocking_findings'] is True for r in [r1,r2]),'Two independent complete package reviews')
    for role in ['pre_execution_adversary','final']:
        need(equal(decoded[role]['reviewed_program_hashes'],program_hashes) and stamp(decoded[role]['UTC'])>=pretime,'Fresh helper/input review')
    final=decoded['final']
    need(all(stamp(final['UTC'])>=stamp(gate['UTC']) for gate in decoded.values()),'Final gate precedes its hashed antecedent')
    need(final['antecedent_gate_sha256']=={role:sha(gates[role]) for role in ROLES if role!='final'} and
         final['publication_receipt_sha256']==x['publication_receipt']['sha256'] and final['sheet_receipt_sha256']==x['sheet_receipt']['sha256'] and
         final['actual_Zenodo_service_independently_authenticated'] is True and final['actual_GWS_service_independently_authenticated'] is True and
         final['native_candidate_preparation_commissioned'] is True,'Final actual service/antecedent authentication')
    inputs.finish()
    return {'schema':'pr110-offline-protocol-preconditions/v1','structural_preconditions_checked':True,
            'execution_inputs_sha256':sha(document_bytes),'DOI':doi,'sheet_range':selected,
            'authorizes_native_execution':False,'native_acceptance_executed':False,
            'service_authenticity_depends_on_independent_root_review':True}

def imported_baseline(at,queue_row_sha256,author_log_sha256):
    stamp(at)
    need(queue_row_sha256==ORIGINAL_ROW_SHA and author_log_sha256==ORIGINAL_LOG_SHA,'Authenticated immutable historical evidence pins')
    return {'schema':'pr110-dated-native-import-baseline/v1','at':at,'id':K,'status':'claimed_solved','turns_used':2,
      'review_hash':REVIEW,'statement_hash':STATEMENT,'original_budget':'2/5','original_structured_ledger_present':False,
      'new_central_proof_search_turns':0,'original_head':HEAD,'original_queue_row_sha256':queue_row_sha256,
      'original_author_log_sha256':author_log_sha256,'event':'dated_import_of_authenticated_author_count',
      'provenance':'Dated native import from authenticated original QUEUE and prose; not a recovered historical structured event.'}

def validate_assessments(before,after,overlay):
    need(K in before and set(before)==set(after),'Assessment identity set')
    need(all(equal(v,after[k]) for k,v in before.items() if k!=K),'Unauthorized unrelated assessment metadata')
    need(set(overlay)<=ASSESSMENT_METADATA,'Unauthorized target score/hold/resolution edit')
    if 'new_central_proof_search_turns' in overlay:
        need(type(overlay['new_central_proof_search_turns']) is int and overlay['new_central_proof_search_turns']==0,'Exact zero search-turn count')
    expected={**before[K],**overlay}
    need(set(after[K])==set(expected)|{'reviewed_at'} and equal({k:v for k,v in after[K].items() if k!='reviewed_at'},
         {k:v for k,v in expected.items() if k!='reviewed_at'}),'Target assessment changed beyond reviewed metadata')
    stamp(after[K]['reviewed_at'])

def catalog_scope(before,generated,states,policy,assessments):
    old={r['id']:r for r in before};new={r['id']:r for r in generated}
    need(len(old)==len(before) and len(new)==len(generated) and set(old)==set(new) and K in old,'Catalog identity set')
    need(policy.get('turn_limit')==5,'Five-turn policy')
    drift=[]
    for key,row in old.items():
        other=new[key]
        if key==K:
            allowed={'local_status','turns_used','eligible','rank','desk_note'}
            need(equal({f:v for f,v in row.items() if f not in allowed},
                       {f:v for f,v in other.items() if f not in allowed}),'Target source/score/hold change')
            need(other['local_status']=='claimed_solved' and type(other['turns_used']) is int and other['turns_used']==2 and
                 other['eligible'] is False and other['rank'] is None,'Target literal scoped projection')
            need(other['desk_note']==assessments[K]['note'],'Target note matches native assessment')
            continue
        changes={f for f in set(row)|set(other) if f not in row or f not in other or not equal(row[f],other[f])}
        need(changes<={'rank','local_status','turns_used','eligible'},'Unauthorized unrelated catalog metadata')
        if changes-{'rank'}:
            state=states.get(key,{});a=assessments.get(key,{})
            if row['present']:
                default='queued' if a.get('decision')=='candidate' else 'deferred' if a.get('decision') in ['defer','exclude'] else 'unreviewed'
                if default=='queued' and row['holds']: default='unreviewed'
                if a.get('resolution')=='already_solved' and a.get('review_hash')==row['review_hash']: default='already_solved'
                status,turns=state.get('status',default),state.get('turns_used',0)
            else: status,turns=state.get('status',row['local_status']),row['turns_used']
            need(type(turns) is int and turns>=0,'Unrelated native turn count')
            eligible=bool(row['present'] and not row['holds'] and status in ['queued','unreviewed','ready'] and turns<5)
            need(other['local_status']==status and type(other['turns_used']) is int and other['turns_used']==turns and
                 other['eligible'] is eligible,'Unexplained unrelated projection drift')
            drift.append({'id':key,'fields':sorted(changes),'baseline_preserved':True})
    # Preserve complete unrelated records, rank labels and baseline list positions.
    return [dict(new[K]) if r['id']==K else dict(r) for r in before],drift

def csv_records(body):
    text=body.decode('utf8')
    lines=[m.group(0) for m in re.finditer(r'[^\r\n]*(?:\r\n|\r|\n|$)',text) if m.group(0)]
    need(''.join(lines)==text,'CSV physical coverage')
    reader=csv.reader(io.StringIO(text,newline=''),strict=True);out=[];start=0
    for fields in reader:
        end=reader.line_num;out.append({'fields':fields,'body':''.join(lines[start:end]).encode(),'start':start,'end':end});start=end
    need(start==len(lines),'CSV record spans')
    return lines,out

def csv_overlay(body,target):
    lines,rows=csv_records(body);need(rows and 'id' in rows[0]['fields'],'CSV header')
    fields=rows[0]['fields'];need(len(fields)==len(set(fields)),'Duplicate CSV header')
    index=fields.index('id');need(all(len(r['fields'])==len(fields) for r in rows),'CSV row widths')
    ids=[r['fields'][index] for r in rows[1:]];need(len(ids)==len(set(ids)) and ids.count(K)==1,'CSV target identity')
    i=ids.index(K)+1;old=rows[i];last=lines[old['end']-1]
    ending='\r\n' if last.endswith('\r\n') else '\r' if last.endswith('\r') else '\n' if last.endswith('\n') else ''
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore',lineterminator='\r\n')
    writer.writerow({**target,'holds':'; '.join(target['holds']),'reasons':'; '.join(target['reasons'])})
    replacement=stream.getvalue()[:-2]+ending
    result=(''.join(lines[:old['start']])+replacement+''.join(lines[old['end']:])).encode()
    _,after=csv_records(result)
    need(len(after)==len(rows) and [r['fields'][index] for r in after[1:]]==ids and
         all(a['body']==b['body'] for j,(a,b) in enumerate(zip(rows,after)) if j!=i),'Unrelated CSV physical bytes/order')
    return result

def campaign_overlay(body,note,doi):
    need(re.fullmatch(r'10\.5281/zenodo\.[1-9][0-9]*',doi) and isinstance(note,str) and len(note.split())>=8 and
         not any(c in note for c in '|\r\n'),'Campaign DOI/note')
    text=body.decode();lines=[m.group(0) for m in re.finditer(r'[^\r\n]*(?:\r\n|\r|\n|$)',text) if m.group(0)]
    matches=[i for i,line in enumerate(lines) if line.startswith('| ') and line.split('|')[2].strip()==K+' / '+CODE]
    need(len(matches)==1,'Campaign unique exact target');i=matches[0];old=lines[i]
    ending='\r\n' if old.endswith('\r\n') else '\r' if old.endswith('\r') else '\n' if old.endswith('\n') else ''
    cells=old.rstrip('\r\n').split('|')
    need(len(cells)==14 and cells[8].strip()=='queued' and cells[9].strip()=='0/5' and not cells[12].strip(),'Campaign queued0 preimage')
    cells[8],cells[9],cells[11],cells[12]=' claimed_solved ',' 2/5 ',' '+note+' ',' https://doi.org/'+doi+' '
    lines[i]='|'.join(cells)+ending;return ''.join(lines).encode()

def ledger_append(before,after,expected):
    need((not before or before.endswith(b'\n')) and after.startswith(before),'Historical ledger prefix')
    suffix=after[len(before):];need(suffix.endswith(b'\n') and len(suffix.splitlines())==1 and
         equal(loads(suffix),expected),'Exactly one target ledger event')

def scoped_outputs(before,native_after,overlay,import_event,note,doi):
    """Verify actual native-assess results and offer bytes; never writes/exports them."""
    need(set(before)==set(NATIVE) and set(native_after)==set(NATIVE),'Exact native input/output maps')
    for name in ['queue.py','manifest.json','policy.json']: need(before[name]==native_after[name],'Native immutable input changed')
    state=loads(before['state.json']);need(K not in state,'Target import reconciliation required')
    expected_import=imported_baseline(import_event['at'],import_event['original_queue_row_sha256'],import_event['original_author_log_sha256'])
    need(equal(import_event,expected_import),'Exact dated import derivation')
    need(import_event.get('id')==K and import_event.get('status')=='claimed_solved' and type(import_event.get('turns_used')) is int and
         import_event['turns_used']==2 and import_event.get('original_budget')=='2/5' and import_event.get('new_central_proof_search_turns')==0 and
         import_event.get('original_structured_ledger_present') is False and import_event.get('original_head')==HEAD and
         import_event.get('event')=='dated_import_of_authenticated_author_count' and
         'candidate_turn' not in import_event and 'readiness_review_hash' not in import_event,'Dated import provenance/effort')
    expected_state={**state,K:import_event};need(equal(loads(native_after['state.json']),expected_state),'Unrelated state change')
    ledger_append(before['history.jsonl'],native_after['history.jsonl'],import_event)
    ass0,ass1=loads(before['assessments.json']),loads(native_after['assessments.json'])
    validate_assessments(ass0,ass1,overlay)
    ledger_append(before['assessment_history.jsonl'],native_after['assessment_history.jsonl'],{'id':K,**ass1[K]})
    catalog,drift=catalog_scope(loads(before['catalog.json']),loads(native_after['catalog.json']),expected_state,loads(before['policy.json']),ass1)
    need(('## '+K+' —').encode() not in before['SHORTLIST.md'],'Target SHORTLIST requires separately reviewed scoped extension')
    target=next(r for r in catalog if r['id']==K)
    summary=loads(before['summary.json'])
    summary.update(records=len(catalog),eligible=sum(r['eligible'] for r in catalog),assessed=len(ass1),
                   holds=dict(collections.Counter(h.split(':')[0] for r in catalog for h in r['holds'])))
    offered={name:native_after[name] for name in ['assessments.json','state.json','history.jsonl','assessment_history.jsonl']}
    offered.update({'catalog.json':canonical(catalog),'ranking.csv':csv_overlay(before['ranking.csv'],target),
                    'summary.json':canonical(summary),'QUEUE.md':campaign_overlay(before['QUEUE.md'],note,doi)})
    return {name:b for name,b in offered.items() if b!=before[name]},drift
