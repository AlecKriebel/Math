#!/usr/bin/env python3
"""Small in-memory synthetic component fixtures, never genuine service evidence."""
import copy, io, json, pathlib, sys, unittest, zipfile
import protocol as p

D=pathlib.Path(__file__).resolve().parent
A=D.parent
UTC='2026-10-06T14:10:00Z'
DOI='10.5281/zenodo.999999999999999'  # Deliberately fictitious fixture DOI; not evidence.
NOTE='Bounded attributed proof of ordinary focal antipedal equality for strictly nested elliptical caustics.'

class FixtureInputs:
    def __init__(self): self.bodies={};self.specs=[]
    def add(self,path,body):
        if not isinstance(body,bytes): body=p.canonical(body)
        spec={'path':path,**p.pin(body)};self.bodies[path]=body;self.specs.append(spec);return spec
    def read(self,spec):
        p.pin_shape(spec);body=self.bodies[spec['path']]
        p.need(p.pin(body)=={k:spec[k] for k in ['bytes','sha256']},'Fixture pin drift');return body
    def obj(self,spec): return p.loads(self.read(spec))

def proc(f,label,response,argv,minute):
    out=f.add(label+'.stdout',response);err=f.add(label+'.stderr',b'')
    return {'actual_receipt':True,'template_only':False,'PID':100+minute,'exit_code':0,'argv':argv,
      'cwd':'/offline/synthetic-fixture','environment_sha256':p.sha(b'synthetic-clean-env'),
      'UTC_start':f'2026-10-06T13:{minute:02}:00Z','UTC_end':f'2026-10-06T13:{minute:02}:01Z',
      'stdout':out,'stderr':err,'reaped':True,'termination_reason':None}

def service_fixture(archive=False):
    f=FixtureInputs()
    manifest=f.add('package/PACKAGE_MANIFEST.json',{'fixture_only':True,'files':['PROOF.md']})
    proof=f.add('package/PROOF.md',b'Synthetic proof body; never evidence.\n')
    package={'manifest':manifest,'logical_inventory':{'PACKAGE_MANIFEST.json':manifest,'PROOF.md':proof},'effective_proof':proof}
    source=json.loads((A/'original_head_authentication_20261006/original_attempt/source_record.json').read_bytes())
    get=proc(f,'zenodo_metadata',{'id':DOI.rsplit('.',1)[1],'doi':DOI,'submitted':True},['/offline/python','-E','-S','-B','fixture-http'],0)
    get.update(HTTP_method='GET',status_code=200,URL='https://zenodo.org/api/records/'+DOI.rsplit('.',1)[1])
    pub={'schema':'pr110-actual-publication-receipt/v1','actual_receipt':True,'template_only':False,
      'PR':110,'problem_id':5100032,'original_head':p.HEAD,'package_manifest_sha256':manifest['sha256'],
      'DOI':DOI,'published':True,'metadata_GET':get,'logical_readbacks':{}}
    archive_spec=None
    if archive:
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w') as z:
            for name,spec in package['logical_inventory'].items(): z.writestr(name,f.read(spec))
        archive_spec=f.add('transport/package.zip',stream.getvalue())
    for index,(name,spec) in enumerate(package['logical_inventory'].items(),1):
        transport=archive_spec or spec
        request=proc(f,'zenodo_payload'+str(index),{'response_bytes':transport['bytes'],'response_sha256':transport['sha256']},['/offline/python','-E','-S','-B','fixture-http'],index)
        request.update(HTTP_method='GET',status_code=200,URL='https://zenodo.org/api/records/'+DOI.rsplit('.',1)[1]+'/files/package.zip/content',
                       response_sha256=transport['sha256'],response_bytes=transport['bytes'])
        pub['logical_readbacks'][name]={'body':spec,'transport_body':transport,'transport':'zip_member' if archive else 'individual_file','GET':request}
        if archive: pub['logical_readbacks'][name]['member_path']=name
    row=47;selected="'Math Puzzles'!A47:D47"
    source_url=source.get('source_url') or p.re.search(r'Source URL:\s*(https?://[^\s<>]+)',source['background']).group(1)
    values=[source_url,'','https://doi.org/'+DOI,p.K+' / '+p.CODE+' synthetic-only fixture']
    sh={'schema':'pr110-actual-gws-sheet-receipt/v1','actual_receipt':True,'template_only':False,
      'problem_id':5100032,'problem_code':p.CODE,'original_head':p.HEAD,'DOI':DOI,'spreadsheet_id':p.SHEET,
      'sheet_id':p.SHEET_GID,'sheet_title':p.SHEET_TITLE,'columns':p.COLUMNS,'row_index':row,'range':selected,
      'values':values,'existing_chat_authorized':False,'processes':{}}
    for minute,role in enumerate(['metadata','header','append','readback','independent_readback'],3):
        if role=='metadata':
            verb=['sheets','spreadsheets','get'];params={'spreadsheetId':p.SHEET}
            response={'spreadsheetId':p.SHEET,'sheets':[{'properties':{'sheetId':p.SHEET_GID,'title':p.SHEET_TITLE}}]}
        elif role=='header':
            verb=['sheets','spreadsheets','values','get'];params={'spreadsheetId':p.SHEET,'range':"'Math Puzzles'!A1:D1"};response={'values':[p.COLUMNS]}
        elif role=='append':
            verb=['sheets','spreadsheets','values','append'];params={'spreadsheetId':p.SHEET,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW',
                 'insertDataOption':'INSERT_ROWS','includeValuesInResponse':True}
            response={'updates':{'updatedRange':selected,'updatedRows':1,'updatedColumns':4,'updatedCells':4,'updatedData':{'values':[values]}}}
        else:
            verb=['sheets','spreadsheets','values','get'];params={'spreadsheetId':p.SHEET,'range':selected};response={'range':selected,'values':[values]}
        param_text=json.dumps(params);argv=['/offline/gws',*verb,'--params',param_text]
        if role=='append': argv+=['--json',json.dumps({'majorDimension':'ROWS','values':[values]})]
        record=proc(f,'sheet_'+role,response,argv,minute);record['params_pin']=p.pin(param_text.encode())
        if role=='append': record['json_pin']=p.pin(argv[-1].encode())
        sh['processes'][role]=record
    return f,package,pub,sh,source

def native_fixture():
    context=json.loads((D/'CONTEXT_INSPECTION.json').read_bytes())
    target=context['target_catalog'];target=copy.deepcopy(target)
    b=copy.deepcopy(target);b.update(id='2',title='Unrelated two',rank=1)
    a=copy.deepcopy(target);a.update(id='1',title='Unrelated one',rank=2)
    cat=[b,target,a]
    assessment=copy.deepcopy(context['target_assessment'])
    assessments={p.K:assessment,'1':{**assessment,'id':'1'},'2':{**assessment,'id':'2'}}
    state={'2':{'status':'claimed_solved','turns_used':1,'review_hash':p.REVIEW}}
    event=p.imported_baseline(UTC,p.ORIGINAL_ROW_SHA,p.ORIGINAL_LOG_SHA)
    overlay={'note':NOTE,'original_budget':'2/5','new_central_proof_search_turns':0,'original_structured_ledger_present':False,
             'publication_DOI':DOI,'package_manifest_sha256':p.sha(b'fixture-only-package-manifest')}
    ass1=copy.deepcopy(assessments);ass1[p.K].update(**overlay,reviewed_at=UTC)
    generated=copy.deepcopy(cat)
    generated[0].update(local_status='claimed_solved',turns_used=1,eligible=False,rank=None)
    generated[1].update(local_status='claimed_solved',turns_used=2,eligible=False,rank=None,desk_note=NOTE)
    generated[2]['rank']=1
    ranking=('rank,id,local_status,turns_used,eligible,holds,reasons,title\r\n'
             '1,2,queued,0,True,,individual_desk_review,"Unrelated\nmultiline two"\r\n'
             '124,5100032,queued,0,True,,individual_desk_review,k603\r\n'
             '2,1,queued,0,True,,individual_desk_review,Unrelated one').encode()
    campaign=(context['campaign_target_row']+'\r\n'+'| preserve unrelated bytes   here |\r').encode()
    before={'queue.py':(D/'private_context/native_queue_from_git.py').read_bytes(),
      'manifest.json':p.canonical({'revision':p.REV,'records':15458}), 'policy.json':p.canonical({'turn_limit':5}),
      'catalog.json':p.canonical(cat),'assessments.json':p.canonical(assessments),'state.json':p.canonical(state),
      'history.jsonl':b'{"id":"2","old_history":true}\n','assessment_history.jsonl':b'{"id":"2","old_review":true}\n',
      'ranking.csv':ranking,'summary.json':p.canonical({'records':3,'eligible':3,'assessed':3,'holds':{},'extra':'preserved'}),
      'SHORTLIST.md':b'# Existing shortlist\nUnrelated prose.\n','QUEUE.md':campaign}
    after={**before,'catalog.json':p.canonical(generated),'assessments.json':p.canonical(ass1),'state.json':p.canonical({**state,p.K:event}),
      'history.jsonl':before['history.jsonl']+json.dumps(event).encode()+b'\n',
      'assessment_history.jsonl':before['assessment_history.jsonl']+json.dumps({'id':p.K,**ass1[p.K]}).encode()+b'\n'}
    return before,after,overlay,event

def canonical_manifest_fixture():
    """In-memory shape fixture only; no emitted configuration or reviewed outcome."""
    f,package,pub,sh,source=service_fixture(True)
    context=json.loads((D/'CONTEXT_INSPECTION.json').read_bytes())
    original_manifest=json.loads((A/'original_head_authentication_20261006/ORIGINAL_BLOB_MANIFEST.json').read_bytes())
    auth=json.loads((A/'original_head_authentication_20261006/SOURCEPAIR_AUTHENTICATION.json').read_bytes())
    raw={item['path'].rsplit('/',1)[-1]:{key:item[key] for key in ['bytes','sha256']}
         for item in auth['input_pins'] if '/cache/' in item['path']}
    original={'manifest':f.add('original/inventory.json',original_manifest),
      'queue':f.add('original/QUEUE.md',(A/'original_head_authentication_20261006/ORIGINAL_HEAD_QUEUE.md').read_bytes()),
      'sourcepair_authentication':f.add('original/sourcepair.json',auth),'files':{}}
    for name in p.ORIGINAL_NAMES:
        original['files'][name]=f.add('original/body/'+name,(A/'original_head_authentication_20261006/original_attempt'/name).read_bytes())
    before,_,overlay,_=native_fixture()
    # Identity-only unrelated records keep the full-count gate fixture small.
    # Complete native scope semantics are tested separately on the three records.
    before['catalog.json']=p.canonical([context['target_catalog']]+[{'id':str(i)} for i in range(1,15458)])
    before['manifest.json']=p.canonical({'revision':p.REV,'records':15458,'files':{n:raw[n] for n in ['problems.json','research_results.json']}})
    native={name:f.add('native/'+name,body) for name,body in before.items()}
    transport={'actual_receipt':True,'template_only':False,'package_manifest_sha256':package['manifest']['sha256'],
      'exact_logical_inventory':package['logical_inventory'],'no_missing_duplicate_extra_or_unsafe_archive_members':True}
    package['transport_inventory_receipt']=f.add('package/transport_inventory_receipt.json',transport)
    overlay['package_manifest_sha256']=package['manifest']['sha256']
    runtime={'queue_sha256':p.QUEUE_SHA,'startup_policy':{'python_flags':['-E','-S','-B'],'ambient_environment_inherited':False},
      'private_config_metadata':[{'absolute_path':'/offline/private/config','bytes':5,'sha256':p.sha(b'dummy'),'body_private':True}]}
    for role in ['python','git','gws','gh']:runtime[role]={'absolute_path':'/offline/'+role,'bytes':1,'sha256':p.sha(role.encode()),'version':'synthetic fixture only'}
    runtime['sh']={'absolute_path':'/bin/sh','bytes':1,'sha256':p.sha(b'sh'),'version':'synthetic fixture only'}
    base=context['observed_main_parent']
    pre={'schema':'pr110-actual-main-source-runtime-preflight/v1','actual_receipt':True,'template_only':False,
      'main_parent':base,'remote_main':base,'branch':'main','live_PR_head':p.HEAD,'live_PR_base':'main','live_PR_number':110,
      'live_PR_state':'OPEN','live_PR_isDraft':True,'source_review_hash':p.REVIEW,'source_statement_hash':p.STATEMENT,
      'dataset_revision':p.REV,'SQL_prior_equals_nonempty_original':True,'SQL_source_equals_original':True,
      'SQL_revision':p.REV,'SQL_record_count':15458,'source_cache_pin':raw['catalog.sqlite'],
      'raw_source_pins':{n:raw[n] for n in ['problems.json','research_results.json']},'native_target_absent':True,
      'SQL_sidecars_absent':True,'runtime':runtime,'native_before':native,'root_independently_authenticated_processes':True,
      'UTC':'2026-10-06T13:12:00Z','processes':[]}
    contracts={}
    for i,role in enumerate(['local_main','remote_main','live_PR','source_and_runtime'],8):
        record=proc(f,'preflight'+str(i),{'synthetic_only':True},['/offline/python','-E','-S','-B','fixture-only-'+role],i)
        record['role']=role;pre['processes'].append(record)
        contracts[role]={'argv':record['argv'],'cwd':record['cwd'],'environment_sha256':record['environment_sha256'],
                         'executable_role':'python','program_inputs':[]}
    service_contracts={}
    records={'zenodo.metadata':pub['metadata_GET'],
             **{'zenodo.payload.'+name:item['GET'] for name,item in pub['logical_readbacks'].items()},
             **{'gws.'+role:record for role,record in sh['processes'].items()}}
    for role,record in records.items():
        service_contracts[role]={'argv':record['argv'],'cwd':record['cwd'],'environment_sha256':record['environment_sha256'],
                                'executable_role':'gws' if role.startswith('gws.') else 'python','program_inputs':[]}
    prefix='unsolved_math_prioritization/attempts/'+p.K+'/'
    attempt={prefix+'historical_original/'+name for name in p.ORIGINAL_NAMES}|{
      prefix+name for name in ['source_record.json','prior_imported_report.json','IMPORT_BASELINE.json',
                              'HISTORICAL_DESK_ASSESSMENT.json','assessment.json','PUBLICATION_EVIDENCE.json','README.md','RESEARCH_LOG.md']}
    program_hashes={'protocol.py':p.sha((D/'protocol.py').read_bytes())}
    program_sources={}
    for name in ['native_worker.py','native_runner.py','native_launcher.sh']:
        spec=f.add('future_programs/'+name,b'Synthetic nonexecuted source-shape fixture.\n')
        program_sources[name]=spec;program_hashes[name]=spec['sha256']
    workspace=str(D)+'/future_candidates/synthetic_fixture_only'
    run={'program_sources':program_sources,'workspace_root':workspace,'launcher_shell':'/bin/sh',
      'read_only_SQL_pin':raw['catalog.sqlite'],'native_baseline':native,'allowed_native_output_names':p.NATIVE+['assessment.json'],
      'mode':'private_native_assess_then_scoped_offer_only',
      'resource_limits':{'CPU_seconds':90,'FSIZE_bytes':32*1024*1024,'NOFILE':64,'memory_advisory_bytes':512*1024*1024,'Darwin_hard_memory_limit_claimed':False},
      'parent_watchdog':{'deadline_seconds':120,'stdout_cap_bytes':1024*1024,'stderr_cap_bytes':65536,'free_headroom_bytes':32*1024*1024,
         'future_commit_reserve_bytes':16*1024*1024,'runtime_reserve_bytes':8*1024*1024,'allocation_cap_bytes':160*1024*1024,
         'file_count_cap':512,'TERM_then_KILL_and_reap':True}}
    for role in ['worker','runner']:
        run[role+'_launch']={'argv':['/offline/python','-E','-S','-B',workspace+'/'+role+'.py','--control',workspace+'/CONTROL.json'],
          'cwd':workspace,'environment':{'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC'}}
    run['program_staging']={'native_worker.py':workspace+'/worker.py','native_runner.py':workspace+'/runner.py','native_launcher.sh':workspace+'/launcher.sh'}
    run['launcher_launch']={'argv':['/bin/sh',workspace+'/launcher.sh','/offline/python',workspace+'/runner.py','--control',workspace+'/CONTROL.json'],
                           'cwd':workspace,'environment':run['runner_launch']['environment']}
    target={'PR':110,'id':p.K,'code':p.CODE,'original_head':p.HEAD,'literal_status':'claimed_solved','turns_used':2,
      'new_central_proof_search_turns':0,'review_hash':p.REVIEW,'statement_hash':p.STATEMENT,'dataset_revision':p.REV,'exact_claim':p.CLAIM}
    effective={'main_parent':base,'target':target,'native_before':native,'original':original,'package':package,
      'publication_receipt':f.add('services/publication.json',pub),'sheet_receipt':f.add('services/sheet.json',sh),
      'runtime':runtime,'preflight_receipt':f.add('preflight/receipt.json',pre),'preflight_process_contracts':contracts,
      'service_process_contracts':service_contracts,'native_run_contract':run,'assessment_overlay':overlay,
      'campaign_note':NOTE,'attempt_inventory':sorted(attempt),'scope_policy':'preserve_unrelated_bytes_records_ranks_and_positions'}
    doc={'schema':'pr110-native-integration-inputs/v1','template_only':False,'execution_mode':'offline_candidate_verification_only',
      'effective':effective,'input_files':f.specs,'program_hashes':program_hashes}
    document=p.canonical(doc);gates={}
    binding={'execution_inputs_sha256':p.sha(document),'main_parent':base,'original_head':p.HEAD,
      'review_hash':p.REVIEW,'statement_hash':p.STATEMENT,'package_manifest_sha256':package['manifest']['sha256'],'exact_claim':p.CLAIM}
    for role in p.ROLES:
        gate={'schema':'pr110-root-native-input-review/v1','actual_receipt':True,'template_only':False,'role':role,'PR':110,
          'problem_id':5100032,**binding,'clearance':True,'actual_root_review':True,'original_budget':'2/5',
          'new_central_proof_search_turns':0,'checked_artifacts':[package['manifest']],'UTC':'2026-10-06T13:13:00Z'}
        if role=='mathematics':gate['mathematical_clearance']=True
        if role=='priority':gate.update(bounded_priority_clearance=True,source_observation_credited=True,absolute_priority_claimed=False)
        if role=='package':gate['package_clearance']=True
        if role.startswith('whole_package_'):gate.update(reviewer_run_id='synthetic-'+role,independent_whole_package_review=True,zero_blocking_findings=True)
        if role in ['pre_execution_adversary','final']:gate['reviewed_program_hashes']=program_hashes
        if role=='final':gate.update(antecedent_gate_sha256={r:p.sha(b) for r,b in gates.items()},
          publication_receipt_sha256=effective['publication_receipt']['sha256'],sheet_receipt_sha256=effective['sheet_receipt']['sha256'],
          actual_Zenodo_service_independently_authenticated=True,actual_GWS_service_independently_authenticated=True,native_candidate_preparation_commissioned=True)
        gates[role]=p.canonical(gate)
    return document,f.bodies,gates,program_hashes

class ProtocolFixtures(unittest.TestCase):
    def rejected(self,fn,*args):
        with self.assertRaises((ValueError,KeyError,TypeError,zipfile.BadZipFile)): fn(*args)
    def test_exact_original_nonempty_sourcepair(self):
        source=(A/'original_head_authentication_20261006/original_attempt/source_record.json').read_bytes()
        prior=(A/'original_head_authentication_20261006/original_attempt/prior_imported_report.json').read_bytes()
        s,r=p.sourcepair(source,prior);self.assertTrue(r);self.assertEqual(str(s['id']),p.K)
    def test_empty_prior_rejected(self):
        source=(A/'original_head_authentication_20261006/original_attempt/source_record.json').read_bytes()
        self.rejected(p.sourcepair,source,b'{}\n')
    def test_source_drift_rejected(self):
        source=(A/'original_head_authentication_20261006/original_attempt/source_record.json').read_bytes()
        prior=(A/'original_head_authentication_20261006/original_attempt/prior_imported_report.json').read_bytes()
        self.rejected(p.sourcepair,source+b' ',prior)
    def test_template_cannot_be_execution_evidence(self):
        self.rejected(p.validate_execution,p.canonical({'schema':'pr110-native-integration-inputs/v1','template_only':True}),{}, {},{},UTC)
    def test_full_in_memory_structural_gate_path(self):
        document,bodies,gates,programs=canonical_manifest_fixture()
        out=p.validate_execution(document,bodies,gates,programs,UTC)
        self.assertTrue(out['structural_preconditions_checked']);self.assertFalse(out['authorizes_native_execution'])
        self.assertFalse(out['native_acceptance_executed'])
    def test_stale_manifest_bound_gate_reject(self):
        document,bodies,gates,programs=canonical_manifest_fixture()
        final=p.loads(gates['final']);final['execution_inputs_sha256']=p.sha(b'stale inputs');gates['final']=p.canonical(final)
        self.rejected(p.validate_execution,document,bodies,gates,programs,UTC)
    def test_full_gate_source_head_bool_effort_or_runtime_pin_drift_reject(self):
        document,bodies,gates,programs=canonical_manifest_fixture()
        for mutation in ['head','effort','runtime']:
            doc=p.loads(document)
            if mutation=='head':doc['effective']['target']['original_head']='0'*40
            elif mutation=='effort':doc['effective']['target']['new_central_proof_search_turns']=False
            else:doc['effective']['runtime']['queue_sha256']='0'*64
            self.rejected(p.validate_execution,p.canonical(doc),bodies,gates,programs,UTC)
    def test_future_native_workspace_and_resource_contract_reject(self):
        document,bodies,gates,programs=canonical_manifest_fixture()
        for mutation in ['workspace','bool_CPU','extra_output','unreviewed_program']:
            doc=p.loads(document);run=doc['effective']['native_run_contract']
            if mutation=='workspace':run['workspace_root']='/Users/alec/Documents/Math'
            elif mutation=='bool_CPU':run['resource_limits']['CPU_seconds']=True
            elif mutation=='extra_output':run['allowed_native_output_names']+=['unrelated.json']
            else:run['program_sources']['native_worker.py']['sha256']='0'*64
            self.rejected(p.validate_execution,p.canonical(doc),bodies,gates,programs,UTC)
    def test_invalid_source_hash_and_out_of_order_final_gate_reject(self):
        document,bodies,gates,programs=canonical_manifest_fixture();doc=p.loads(document)
        doc['program_hashes']['protocol.py']='malformed';badprograms={**programs,'protocol.py':'malformed'}
        self.rejected(p.validate_execution,p.canonical(doc),bodies,gates,badprograms,UTC)
        later=p.loads(gates['pre_execution_adversary']);later['UTC']='2026-10-06T14:09:00Z';gates['pre_execution_adversary']=p.canonical(later)
        final=p.loads(gates['final']);final['antecedent_gate_sha256']={r:p.sha(b) for r,b in gates.items() if r!='final'};gates['final']=p.canonical(final)
        self.rejected(p.validate_execution,document,bodies,gates,programs,UTC)
    def test_century_old_payload_service_timestamp_reject(self):
        f,package,pub,_,_=service_fixture();item=pub['logical_readbacks']['PROOF.md']['GET']
        item['UTC_start']='1900-01-01T00:00:00Z';item['UTC_end']='1900-01-01T00:00:01Z'
        self.rejected(p.publication,pub,package,f)
    def test_counterfeit_import_provenance_pin_reject(self):
        self.rejected(p.imported_baseline,UTC,'0'*64,'1'*64)
    def test_duplicate_json_and_nonfinite_reject(self):
        for text in [b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":Infinity}']: self.rejected(p.loads,text)
    def test_pin_byte_drift_and_unused_body_reject(self):
        spec={'path':'receipt.json',**p.pin(b'{}')};registry=p.Inputs([spec],{'receipt.json':b'{}'})
        self.rejected(registry.finish);registry.read(spec);registry.finish()
        registry.bodies['receipt.json']=b'{ }';self.rejected(registry.read,spec)
    def test_individual_publication_structure(self):
        f,package,pub,sh,s=service_fixture();doi,_,end=p.publication(pub,package,f);selected,_=p.sheet(sh,doi,s,end,f)
        self.assertEqual(selected,"'Math Puzzles'!A47:D47")
    def test_zip_publication_exact_structure(self):
        f,package,pub,_,_=service_fixture(True);self.assertEqual(p.publication(pub,package,f)[0],DOI)
    def test_zip_extra_member_reject(self):
        f,package,pub,_,_=service_fixture(True);spec=pub['logical_readbacks']['PROOF.md']['transport_body']
        stream=io.BytesIO(f.read(spec))
        with zipfile.ZipFile(stream,'a') as z:z.writestr('extra.txt','unauthorized')
        extra=f.add('bad_archive.zip',stream.getvalue())
        pub['logical_readbacks']['PROOF.md']['transport_body']=extra
        self.rejected(p.publication,pub,package,f)
    def test_fixture_receipt_flag_rejects(self):
        f,package,pub,_,_=service_fixture();pub['fixture']=True;self.rejected(p.publication,pub,package,f)
    def test_stale_package_receipt_rejects(self):
        f,package,pub,_,_=service_fixture();pub['package_manifest_sha256']=p.sha(b'stale package');self.rejected(p.publication,pub,package,f)
    def test_stale_service_body_pin_rejects(self):
        f,package,pub,_,_=service_fixture();path=pub['metadata_GET']['stdout']['path'];f.bodies[path]=b'{}';self.rejected(p.publication,pub,package,f)
    def test_wrong_doi_and_wrong_target_reject(self):
        for field,value in [('DOI','10.5281/zenodo.123'),('original_head','0'*40),('problem_id',5100023)]:
            f,package,pub,_,_=service_fixture();pub[field]=value;self.rejected(p.publication,pub,package,f)
    def test_sheet_prepublication_and_wrong_range_reject(self):
        f,package,pub,sh,s=service_fixture();doi,_,end=p.publication(pub,package,f)
        sh['processes']['append']['UTC_start']='2026-10-06T12:00:00Z';self.rejected(p.sheet,sh,doi,s,end,f)
        f,package,pub,sh,s=service_fixture();doi,_,end=p.publication(pub,package,f);sh['range']="'Math Puzzles'!A48:D48";self.rejected(p.sheet,sh,doi,s,end,f)
    def test_sheet_blank_chat_and_existing_url_contract(self):
        f,package,pub,sh,s=service_fixture();doi,_,end=p.publication(pub,package,f);p.sheet(sh,doi,s,end,f)
        for bad in ['https://bad user/path','http://chatgpt.com/c/test','https://user:pass@chatgpt.com/c/test']:
            sh['values'][1]=bad;sh['existing_chat_authorized']=True;self.rejected(p.sheet,sh,doi,s,end,f)
    def test_gws_append_flags_reject_dry_run(self):
        f,package,pub,sh,s=service_fixture();doi,_,end=p.publication(pub,package,f)
        sh['processes']['append']['argv']+=['--dry-run'];self.rejected(p.sheet,sh,doi,s,end,f)
    def test_scoped_offer_preserves_records_positions_ranks_and_scores(self):
        before,after,overlay,event=native_fixture();out,drift=p.scoped_outputs(before,after,overlay,event,NOTE,DOI)
        old=p.loads(before['catalog.json']);new=p.loads(out['catalog.json'])
        self.assertEqual([r['id'] for r in old],[r['id'] for r in new]);self.assertEqual(old[0],new[0]);self.assertEqual(old[2],new[2])
        self.assertEqual(new[1]['local_status'],'claimed_solved');self.assertEqual(new[1]['turns_used'],2);self.assertEqual(len(drift),1)
        self.assertEqual(new[1]['impact'],old[1]['impact']);self.assertEqual(set(out),set(p.DERIVED))
        oldcampaign=before['QUEUE.md'].decode().split('|');newcampaign=out['QUEUE.md'].decode().split('|')
        self.assertEqual(oldcampaign[1],newcampaign[1]);self.assertEqual(oldcampaign[5],newcampaign[5]);self.assertEqual(oldcampaign[10],newcampaign[10])
        _,oldcsv=p.csv_records(before['ranking.csv']);_,newcsv=p.csv_records(out['ranking.csv'])
        for i in [0,1,3]:self.assertEqual(oldcsv[i]['body'],newcsv[i]['body'])
    def test_unrelated_assessment_metadata_reject(self):
        before,after,overlay,event=native_fixture();a=p.loads(after['assessments.json']);a['1']['note']='Unauthorized';after['assessments.json']=p.canonical(a)
        self.rejected(p.scoped_outputs,before,after,overlay,event,NOTE,DOI)
    def test_unrelated_state_change_reject(self):
        before,after,overlay,event=native_fixture();s=p.loads(after['state.json']);s['2']['turns_used']=0;after['state.json']=p.canonical(s)
        self.rejected(p.scoped_outputs,before,after,overlay,event,NOTE,DOI)
    def test_target_score_change_reject(self):
        before,after,overlay,event=native_fixture();a=p.loads(after['assessments.json']);a[p.K]['impact']=10;after['assessments.json']=p.canonical(a)
        self.rejected(p.scoped_outputs,before,after,overlay,event,NOTE,DOI)
    def test_unrelated_catalog_score_source_hold_metadata_reject(self):
        for field,value in [('impact',9),('review_hash','0'*64),('holds',['invented']),('title','changed')]:
            before,after,overlay,event=native_fixture();rows=p.loads(after['catalog.json']);rows[0][field]=value;after['catalog.json']=p.canonical(rows)
            self.rejected(p.scoped_outputs,before,after,overlay,event,NOTE,DOI)
    def test_null_protected_key_addition_or_deletion_reject(self):
        for i in [0,1]:
            for mode in ['add','delete']:
                before,after,overlay,event=native_fixture();old=p.loads(before['catalog.json']);rows=p.loads(after['catalog.json'])
                if mode=='add':rows[i]['unauthorized_null']=None
                else:old[i]['protected_null']=None;rows[i]['protected_null']=None;del rows[i]['protected_null']
                before['catalog.json']=p.canonical(old);after['catalog.json']=p.canonical(rows)
                self.rejected(p.scoped_outputs,before,after,overlay,event,NOTE,DOI)
    def test_import_schema_source_provenance_missing_or_changed_reject(self):
        for field in ['schema','review_hash','statement_hash','original_queue_row_sha256','original_author_log_sha256']:
            before,after,overlay,event=native_fixture();event.pop(field);self.rejected(p.scoped_outputs,before,after,overlay,event,NOTE,DOI)
    def test_false_eligibility_without_explanation_reject(self):
        before,after,overlay,event=native_fixture();rows=p.loads(after['catalog.json']);rows[2]['eligible']=False;after['catalog.json']=p.canonical(rows)
        self.rejected(p.scoped_outputs,before,after,overlay,event,NOTE,DOI)
    def test_historical_ledger_edit_or_extra_event_reject(self):
        for change in ['prefix','extra']:
            before,after,overlay,event=native_fixture()
            after['history.jsonl']=(b'X'+after['history.jsonl'][1:]) if change=='prefix' else after['history.jsonl']+b'{"id":"1"}\n'
            self.rejected(p.scoped_outputs,before,after,overlay,event,NOTE,DOI)
    def test_no_invented_candidate_or_readiness_ledger(self):
        for field in ['candidate_turn','readiness_review_hash']:
            before,after,overlay,event=native_fixture();event[field]=2;self.rejected(p.scoped_outputs,before,after,overlay,event,NOTE,DOI)
    def test_preserve_nonphysical_unicode_separator_and_csv_endings(self):
        target={'id':p.K,'title':'Target\rinside\nfield still field','holds':[],'reasons':[]}
        for ending in ['\n','\r\n','\r','']:
            body=('id,title\r\n1,"Before separator"\r\n5100032,Target'+ending).encode()
            result=p.csv_overlay(body,target);_,before=p.csv_records(body);_,after=p.csv_records(result)
            self.assertEqual(before[0]['body'],after[0]['body']);self.assertEqual(before[1]['body'],after[1]['body'])
            self.assertEqual(after[2]['fields'][1],target['title'])
    def test_duplicate_id_or_header_reject(self):
        target={'id':p.K,'holds':[],'reasons':[]}
        for body in [b'id,id\n5100032,5100032\n',b'id,title\n5100032,a\n5100032,b\n']:
            self.rejected(p.csv_overlay,body,target)
    def test_bool_turn_count_reject(self):
        before,after,overlay,event=native_fixture();event['turns_used']=True;self.rejected(p.scoped_outputs,before,after,overlay,event,NOTE,DOI)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ProtocolFixtures)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({'schema':'pr110-offline-component-fixtures/v1','synthetic_fixture_only':True,
      'optimization':sys.flags.optimize,'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
      'actual_service_calls':0,'native_assess_executions':0,'full_native_fixture_snapshots':0,
      'full_execution_input_gate_path_positive_fixture':True,'proof_search_turns':0}))
    raise SystemExit(0 if result.wasSuccessful() else 1)
