#!/usr/bin/env python3
"""Synthetic offline guard and complete-main checks; no live service or Git call.

All fabricated metadata, gates, PDFs, source and reviewer records live only in
ignored _local temporary fixtures. These tests do not clear a real release.
"""
from pathlib import Path
import contextlib,copy,datetime,hashlib,importlib.util,io,json,os,shutil,subprocess,sys,tempfile,types,zipfile
ROOT=Path(__file__).resolve().parent
COORDINATOR=ROOT.parents[2]/'publication_coordinators/pr1274.py'
POSTMERGE=ROOT.parents[2]/'publication_coordinators/verify_pr1274_merge.py'
REPORT_ROOT=ROOT.parent/'reviews/workflow_identity_revision1'
NAMES=['prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py']
DEPLOY={name:(('verification_verify.py' if (ROOT/'verification_verify.py').exists() else name) if name=='verification/verify.py' else name) for name in NAMES}
ALIAS_VARIANTS={'alias':'aMr0227072','aliasHyphen':'AMR-022-7072','aliasSpace':'aMR 022 7072','aliasUnderscore':'AMR_022_7072','aliasMixed':'aMr - 022_7072','aliasUnpadded':'AMR-22-7072','aliasZeroPad':'AMR_00022_0007072','aliasZeroPadCompact':'AMR000220007072'}
ALIAS_NEAR_COLLISIONS={'nearHyphen':'AMR-022-70729','nearSpace':'AMR 022 70729','nearUnderscore':'AMR_022_70729','nearCompact':'AMR02270729','nearWrongGroup':'AMR-122-7072','nearTrailingLetter':'AMR-022-7072x','nearLeadingLetter':'XAMR-022-7072'}

def need(value,message):
    if not value:raise RuntimeError(message)
def load(path):
    spec=importlib.util.spec_from_file_location('fixture_'+path.stem+str(id(path)),path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def save(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def binding(path):return {'bytes':path.stat().st_size,'sha256':sha(path)}
def reject(fn,label,errors=(RuntimeError,ValueError,FileNotFoundError,KeyError)):
    try:fn()
    except errors:return label
    raise RuntimeError('Invalid fixture unexpectedly accepted: '+label)
def capture(fn):
    with contextlib.redirect_stdout(io.StringIO()):return fn()

def fixture(folder):
    audit=folder/'program/audits/pr1274_2307072';pub=audit/'publication';pub.mkdir(parents=True)
    for deployed,source in DEPLOY.items():
        path=pub/deployed;path.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/source,path)
    coordinator=pub.parents[2]/'publication_coordinators/pr1274.py';coordinator.parent.mkdir();shutil.copyfile(COORDINATOR,coordinator);postmerge=coordinator.parent/'verify_pr1274_merge.py';shutil.copyfile(POSTMERGE,postmerge)
    v=load(pub/'verification/verify.py');submitted=audit/'submitted';submitted.mkdir()
    for name in sorted(v.NAMES-{'PUBLIC_MANIFEST.json'}):
        (submitted/name).write_text(json.dumps({'synthetic_historical_fixture':name})+'\n' if name.endswith('.json') else 'SYNTHETIC HISTORICAL FIXTURE '+name+'\n')
    save(submitted/'PUBLIC_MANIFEST.json',{'schema':1,'problem_id':v.PROBLEM,'file_count':6,'files':[{'path':n,**binding(submitted/n)} for n in sorted(v.NAMES-{'PUBLIC_MANIFEST.json'})]})
    snapshot={'pr':v.PR,'problem_id':v.PROBLEM,'head':v.ORIGINAL,'branch':v.BRANCH,'body_sha256':v.BODY,'synthetic_fixture_only':True,'parents':['4b27092a448d53b61408355ce44ec38d103a1ce4'],'files':[]}
    for name in sorted(v.NAMES):
        data=(submitted/name).read_bytes();snapshot['files'].append({'path':v.BASE+'/'+name,'local':'submitted/'+name,**binding(submitted/name),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()})
    save(audit/'SUBMITTED_SNAPSHOT.json',snapshot)
    for name in ['MATH_GATE.json','PRIORITY_ADJUDICATION.json']:save(audit/name,{'pr':v.PR,'problem_id':v.PROBLEM,'original_head':v.ORIGINAL,'status':'PASS','synthetic_fixture_only':True,'firstness_claim':False,'current_openness_claim':False})
    source_program="from pathlib import Path\nimport json\nassert 2+2==4\n(Path(__file__).parent/'result.json').write_text(json.dumps({'synthetic_exact':4})+'\\n')\n"
    analyst_program="from pathlib import Path\nimport argparse,json,sys\np=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()\nr=Path(__file__).parents[2];s=json.loads((r/'SUBMITTED_SNAPSHOT.json').read_text());assert len(s['files'])==6\nfor e in s['files']: assert (r/e['local']).is_file()\nPath(a.output).write_text(json.dumps({'synthetic_exact':6,'run_utc':'fixture runtime','python':sys.version,'optimization':sys.flags.optimize})+'\\n')\n"
    registry=[];portable=[]
    shapes=[('reviews/source_question_family/manifest.json','files','relative_path','size_bytes',source_program),('reviews/analytic_adversary/MANIFEST.json','authored_files','path','bytes',analyst_program),('reviews/explicit_members_family/MANIFEST.json','members','path','bytes',None),('priority/fixture/FREEZE_MANIFEST.json','entries','path','bytes',None)]
    for raw,entries_key,path_key,size_key,program in shapes:
        path=audit/raw;path.parent.mkdir(parents=True,exist_ok=True);(path.parent/'payload.md').write_text('SYNTHETIC FROZEN EVIDENCE\n')
        if program:
            (path.parent/'checker.py').write_text(program)
            (path.parent/'result.json').write_text(json.dumps({'synthetic_exact':4} if 'source_question' in raw else {'synthetic_exact':6,'run_utc':'prior fixture runtime','python':'prior fixture Python','optimization':0})+'\n')
        entries=[]
        for child in sorted(path.parent.iterdir()):
            data=binding(child);entries.append({path_key:child.name,size_key:data['bytes'],'sha256':data['sha256'],'input_path':'/ABSOLUTE/INPUT/MUST/NEVER/BE/FOLLOWED',**({'path':'/ABSOLUTE/FIELD/MUST/NEVER/BE/FOLLOWED'} if path_key!='path' else {})})
            portable.append({'path':child.relative_to(audit).as_posix(),**data,'role':'authored_evidence'})
        save(path,{entries_key:entries,'ignored_source_and_scratch_inventory':[{'path':'/not/retained/source.pdf','bytes':100,'sha256':'0'*64}]})
        registry.append({'path':raw,'base':path.parent.relative_to(audit).as_posix(),'entries_key':entries_key,'path_key':path_key,'size_key':size_key,'sha256':sha(path),'role':'priority' if raw.startswith('priority/') else 'math'})
        portable.append({'path':raw,**binding(path),'role':'authored_evidence'})
    save(audit/'RAW_SOURCE_INVENTORY.json',{'files':[{'path':'omitted.pdf','bytes':100,'sha256':'0'*64}],'read_not_retained':True})
    portable.append({'path':'RAW_SOURCE_INVENTORY.json',**binding(audit/'RAW_SOURCE_INVENTORY.json'),'role':'source_receipt'})
    metadata={'title':'SYNTHETIC OFFLINE FIXTURE ONLY','upload_type':'publication','publication_type':'preprint','description':'Synthetic A & B fixture; no real paper or clearance.','creators':[{'name':'Fixture author','affiliation':None}],'access_right':'open','license':'cc-by-4.0','version':'1.0','publication_date':'2026-10-17','keywords':['synthetic fixture'],'related_identifiers':[{'identifier':'https://github.com/AlecKriebel/Math/pull/1274','relation':'isDerivedFrom','scheme':'url'}]}
    context={'edition_mode':'preserve_submitted','schema':'math-pr1274-current-context-v1','pr':v.PR,'problem_id':v.PROBLEM,'original_head':v.ORIGINAL,'original_branch':v.BRANCH,'original_body_sha256':v.BODY,'title':metadata['title'],'expected_pdf_pages':3,'source_date_epoch':'1792267200','edition_text':{},'structured_records':{},'disclosures':{'firstness_claim':False,'current_openness_claim':False,'ai_assisted':True,'unrefereed':True},'metadata':metadata,'publication_text':{'summary':'Synthetic summary.','priority_statement':'Synthetic priority statement; no real adjudication.','verification_scope':'Synthetic finite controls only.'},'tracker':{'original_problem':'Synthetic fixture (2307072)','notes':'Synthetic notes.'},'authored_freezes':registry,'portable_files':portable,'diagnostic_replays':[{'program':'reviews/source_question_family/checker.py','mode':'normal','result':'reviews/source_question_family/result.json','output_mode':'file','scope':'Synthetic assertion-based fixture only.','layout':'isolated','arguments':[],'comparison':'bytes_exact'},{'program':'reviews/analytic_adversary/checker.py','mode':'normal_O_OO','result':'reviews/analytic_adversary/result.json','output_mode':'file','scope':'Synthetic original-layout replay fixture only.','layout':'original_submission','arguments':['--output','{output}'],'comparison':'json_ignore_runtime'}],'gate_bindings':{'math_gate_sha256':sha(audit/'MATH_GATE.json'),'priority_adjudication_sha256':sha(audit/'PRIORITY_ADJUDICATION.json'),'submitted_snapshot_sha256':sha(audit/'SUBMITTED_SNAPSHOT.json')},'document_bindings':{key:'0'*64 for key in ['source_sha256','pdf_sha256','compile_receipt_sha256','layout_receipt_sha256']}}
    save(audit/'CURRENT_PR1274_CONTEXT.json',context);(pub/'manuscript').mkdir();(pub/'manuscript/main.tex').write_text('SYNTHETIC TEX FIXTURE ONLY\n')
    bin_dir=folder/'bin';bin_dir.mkdir();compiler=bin_dir/'tectonic'
    compiler.write_text('#!'+sys.executable+"\nimport pathlib,sys\nif '--version' in sys.argv:print('synthetic compiler only');raise SystemExit\no=pathlib.Path(sys.argv[sys.argv.index('--outdir')+1]);o.mkdir(parents=True,exist_ok=True);(o/'main.pdf').write_bytes(b'SYNTHETIC PDF BYTES ONLY')\n");compiler.chmod(0o755)
    info=bin_dir/'pdfinfo';info.write_text('#!'+sys.executable+"\nprint('Pages: 3')\n");info.chmod(0o755)
    env=dict(os.environ,PATH=str(bin_dir)+os.pathsep+os.environ['PATH'],PYTHONDONTWRITEBYTECODE='1')
    run=subprocess.run([sys.executable,'-B',str(pub/'compile_note.py')],env=env,capture_output=True,text=True);need(run.returncode==0,run.stderr)
    compiled=json.loads((pub/'COMPILE_RECEIPT.json').read_text());need(compiled['source_date_epoch']==context['source_date_epoch'] and compiled['at_utc']!='2026-10-17T20:00:00Z','actual time confused with build stamp')
    save(pub/'LAYOUT_VERIFICATION.json',{'status':'pass','at_utc':'2026-10-17T21:00:00Z','source_sha256':sha(pub/'manuscript/main.tex'),'pdf_sha256':sha(pub/'output/pdf/main.pdf'),'all_pages_visually_inspected':True,'pages':3,'page_indices_inspected':[1,2,3],'synthetic_fixture_only':True})
    context['document_bindings']={'source_sha256':sha(pub/'manuscript/main.tex'),'pdf_sha256':sha(pub/'output/pdf/main.pdf'),'compile_receipt_sha256':sha(pub/'COMPILE_RECEIPT.json'),'layout_receipt_sha256':sha(pub/'LAYOUT_VERIFICATION.json')};save(audit/'CURRENT_PR1274_CONTEXT.json',context)
    run=subprocess.run([sys.executable,'-B',str(pub/'build_package.py')],env=env,capture_output=True,text=True);need(run.returncode==0,run.stderr)
    build=json.loads((pub/'BUILD_RECEIPT.json').read_text());save(pub/'zenodo-deposit.json',{'metadata':metadata,'files':[{'path':build[key]['path']} for key in ['pdf','verification_zip']]})
    # An actual release must obtain different fresh reviewers. These fabricated
    # records are fixture data in ignored scratch and confer no approval.
    u=load(pub/'update_pr_publication.py');required=[pub/name for name in NAMES]+[pub/name for name in [build['pdf']['path'],build['verification_zip']['path'],'zenodo-deposit.json','manuscript/main.tex','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json','BUILD_RECEIPT.json']]+[audit/name for name in ['CURRENT_PR1274_CONTEXT.json','MATH_GATE.json','PRIORITY_ADJUDICATION.json','SUBMITTED_SNAPSHOT.json']]
    required+=[u.SHARED_KIT,coordinator,postmerge]+[audit/part/name for part in ['submitted','current_edition'] for name in v.NAMES]+[audit/e['path'] for e in context['portable_files']]+[p for p in (pub/'verification').rglob('*') if p.is_file()];records=[]
    for i in [1,2]:
        review=audit/'reviews'/('synthetic_final_'+str(i));review.mkdir();(review/'REPORT.md').write_text('SYNTHETIC REVIEW FIXTURE ONLY; NOT AN ACTUAL REVIEW\n')
        save(review/'INPUT_FREEZE.json',{'synthetic_fixture_only':True,'files':[{'path':str(path),**binding(path)} for path in dict.fromkeys(required)],'external_readonly_inputs':[]})
        save(review/'VERDICT.json',{'schema':'math-pr1274-whole-package-review-v1','status':'CLEAN','actual_review':True,'fresh_reviewer':True,'synthetic_fixture_only':True,'reviewer_id':'fixture-'+str(i),'pr':1274,'problem_id':2307072,'original_head':v.ORIGINAL,'current_context_sha256':sha(audit/'CURRENT_PR1274_CONTEXT.json'),'input_freeze_sha256':sha(review/'INPUT_FREEZE.json'),'at_utc':'2026-10-17T21:00:0'+str(i)+'Z'})
        save(review/'MANIFEST.json',{'authored_files':[{'path':name,**binding(review/name)} for name in ['REPORT.md','VERDICT.json']]})
        records.append({'status':'CLEAN','actual_review':True,'fresh_reviewer':True,'reviewer_id':'fixture-'+str(i),'context_sha256':sha(audit/'CURRENT_PR1274_CONTEXT.json'),'manifest_schema':{'entries_key':'authored_files','path_key':'path','size_key':'bytes'},**{key:('../reviews/'+review.name+'/'+filename) for key,filename in [('report','REPORT.md'),('verdict','VERDICT.json'),('manifest','MANIFEST.json'),('input_freeze','INPUT_FREEZE.json')]},**{key+'_sha256':sha(review/filename) for key,filename in [('report','REPORT.md'),('verdict','VERDICT.json'),('manifest','MANIFEST.json'),('input_freeze','INPUT_FREEZE.json')]}})
        required += [review/name for name in ['REPORT.md','VERDICT.json','MANIFEST.json','INPUT_FREEZE.json']]
    gate={'schema':'math-preprint-final-review-gate-v1','pr':1274,'problem_id':2307072,'original_head':v.ORIGINAL,'status':'pass','workflow':{name:sha(pub/name) for name in NAMES},'deposit_coordinator_sha256':sha(coordinator),'postmerge_coordinator_sha256':sha(postmerge),'pdf_sha256':sha(pub/build['pdf']['path']),'verification_zip_sha256':sha(pub/build['verification_zip']['path']),'metadata_sha256':sha(pub/'zenodo-deposit.json'),'source_sha256':sha(pub/'manuscript/main.tex'),'current_context_sha256':sha(audit/'CURRENT_PR1274_CONTEXT.json'),'reviews':records,'latest_review':records[-1],'synthetic_fixture_only':True}
    gate['shared_kit_sha256']=sha(u.SHARED_KIT);save(pub/'FINAL_REVIEW_GATE.json',gate);u.validate_workflow_gate(gate)
    return {'audit':audit,'pub':pub,'v':v,'context':context,'snapshot':snapshot,'build':build,'gate':gate,'env':env}

def context_and_portable_controls(f):
    audit=f['audit'];pub=f['pub'];v=f['v'];context=f['context'];cp=audit/'CURRENT_PR1274_CONTEXT.json';rejected=[]
    for label,change in [('wrong_pr',lambda x:x.update(pr=1)),('wrong_head',lambda x:x.update(original_head='0'*40)),('wrong_original_body',lambda x:x.update(original_body_sha256='0'*64)),('wrong_original_branch',lambda x:x.update(original_branch='other')),('wrong_title',lambda x:x.update(title='wrong')),('fixed_bad_pages',lambda x:x.update(expected_pdf_pages=0)),('injected_prose',lambda x:x['edition_text'].update({'PROOF.md':'injected'})),('extra_prose',lambda x:x['edition_text'].update({'UNEXPECTED.md':'stale'})),('injected_structured',lambda x:x['structured_records'].update({'SOURCE_VERIFICATION.json':{'injected':True}})),('firstness',lambda x:x['disclosures'].update(firstness_claim=True)),('missing_size_key',lambda x:x['authored_freezes'][0].pop('size_key')),('absolute_selected_path',lambda x:x['authored_freezes'][0].update(path_key='path')),('escaped_base',lambda x:x['authored_freezes'][0].update(base='../outside')),('schema_guessing',lambda x:x['authored_freezes'][0].update(entries_key='entries')),('wrong_freeze_anchor',lambda x:x['authored_freezes'][0].update(sha256='0'*64)),('missing_priority_freeze',lambda x:x['authored_freezes'].pop()),('omitted_frozen_member',lambda x:x['portable_files'].pop(0)),('wrong_document_anchor',lambda x:x['document_bindings'].update(pdf_sha256='0'*64)),('extra_metadata',lambda x:x['metadata'].update(extra='wrong')),('nonascii_metadata_punctuation',lambda x:x['metadata'].update(description='curly apostrophe \u2019'))]:
        bad=copy.deepcopy(context);change(bad);save(cp,bad);rejected.append(reject(lambda:v.load_context(audit,pub),label));save(cp,context)
    for filename in ['MATH_GATE.json','PRIORITY_ADJUDICATION.json']:
        path=audit/filename;old=path.read_bytes();obj=json.loads(old);obj['status']='PASS_fixture_pending';save(path,obj)
        # Update anchor too: actual literal PASS is still required.
        changed=copy.deepcopy(context);changed['gate_bindings']['math_gate_sha256' if filename=='MATH_GATE.json' else 'priority_adjudication_sha256']=sha(path);save(cp,changed)
        rejected.append(reject(lambda:v.load_context(audit,pub),filename+'_nonliteral_PASS'));path.write_bytes(old);save(cp,context)
    root=pub/'verification';anchors=f['build']['verification_anchors'];run=lambda:v.verify(root,anchors['manifest'],anchors['context'],anchors['snapshot']);run()
    path=root/'reviews/source_question_family/payload.md';old=path.read_bytes();path.write_bytes(b'tampered');manifest=root/'MANIFEST.json';original_manifest=manifest.read_bytes();outer=json.loads(original_manifest)
    for entry in outer['files']:
        if entry['path']==path.relative_to(root).as_posix():entry.update(binding(path))
    save(manifest,outer)
    rejected.append(reject(lambda:v.verify(root,sha(manifest),anchors['context'],anchors['snapshot']),'coupled_outer_payload_rewrite_nested_anchor'))
    path.write_bytes(old);manifest.write_bytes(original_manifest)
    nested=root/'reviews/source_question_family/manifest.json';old_nested=nested.read_bytes();obj=json.loads(old_nested);obj['files'][0]['sha256']='0'*64;save(nested,obj)
    rejected.append(reject(lambda:v.authenticate_nested_manifests(root,context['authored_freezes']),'outside_nested_manifest_anchor'));nested.write_bytes(old_nested)
    portable_context=root/'provenance/CURRENT_PR1274_CONTEXT.json';old_context=portable_context.read_bytes();obj=json.loads(old_context);obj['authored_freezes'][0]['base']='priority/fixture';save(portable_context,obj)
    rejected.append(reject(run,'outside_context_anchor_coupled_registry_rewrite'));portable_context.write_bytes(old_context)
    for unsafe in ['../escape','/absolute','a/../b','a//b','a\\b','.', 'a/./b']:rejected.append(reject(lambda raw=unsafe:v.safe(raw),'unsafe_'+unsafe))
    for flags in [[],['-O'],['-OO']]:
        args=[arg for key,val in anchors.items() for arg in ['--expected-'+key+'-sha256',val]]
        result=subprocess.run([sys.executable,'-B',*flags,str(root/'verify.py'),*args],capture_output=True,text=True,env=f['env']);need(result.returncode==0,result.stderr)
    return {'rejected':rejected,'all_three_verifier_modes':True,'original6_current6':True,'actual_custom_schema_ignores_absolute_path':True,'receipt_inventory_not_treated_as_retained_source_manifest':True,'synthetic_pdf_pages':3}

def review_controls(f):
    pub=f['pub'];u=load(pub/'update_pr_publication.py');gate=f['gate'];rejected=[]
    for label,change in [('empty_workflow',lambda x:x.update(workflow={})),('missing_eighth_script',lambda x:x['workflow'].pop('workflow_regression.py')),('wrong_script_hash',lambda x:x['workflow'].update({'append_tracker.py':'0'*64})),('extra_equivalent_path',lambda x:x['workflow'].update({'./append_tracker.py':'0'*64})),('wrong_coordinator',lambda x:x.update(deposit_coordinator_sha256='0'*64)),('wrong_postmerge',lambda x:x.update(postmerge_coordinator_sha256='0'*64)),('wrong_shared_kit',lambda x:x.update(shared_kit_sha256='0'*64)),('wrong_pdf',lambda x:x.update(pdf_sha256='0'*64)),('one_review',lambda x:x.update(reviews=x['reviews'][:1])),('nonactual_review',lambda x:x['reviews'][0].update(actual_review=False)),('not_fresh_reviewer',lambda x:x['reviews'][0].update(fresh_reviewer=False)),('wrong_verdict_hash',lambda x:x['reviews'][0].update(verdict_sha256='0'*64)),('outside_report',lambda x:x['reviews'][0].update(report='../SUBMITTED_SNAPSHOT.json')),('stale_latest',lambda x:x.update(latest_review=x['reviews'][0]))]:
        bad=copy.deepcopy(gate);change(bad);rejected.append(reject(lambda:u.validate_workflow_gate(bad),label))
    verdict=f['audit']/'reviews/synthetic_final_2/VERDICT.json';old=verdict.read_bytes();obj=json.loads(old);obj['status']='FAIL';save(verdict,obj);bad=copy.deepcopy(gate);bad['reviews'][1]['verdict_sha256']=sha(verdict);bad['latest_review']=bad['reviews'][1]
    rejected.append(reject(lambda:u.validate_workflow_gate(bad),'actual_file_nonclean_despite_clean_gate'));verdict.write_bytes(old)
    return rejected

def document_controls(f):
    pub=f['pub'];cp=f['audit']/'CURRENT_PR1274_CONTEXT.json';b=load(pub/'build_package.py');os.environ['PATH']=f['env']['PATH'];b.document_bindings();rejected=[]
    for label in ['failed_compile','missing_actual_compile_time','wrong_epoch','wrong_compile_source','wrong_compile_pdf','partial_visual','wrong_layout_source','wrong_layout_pdf','missing_actual_layout_time','wrong_positive_page_count','partial_page_indices']:
        compiled_path=pub/'COMPILE_RECEIPT.json';layout_path=pub/'LAYOUT_VERIFICATION.json';originals=[path.read_bytes() for path in [cp,compiled_path,layout_path]];context=json.loads(originals[0]);compiled=json.loads(originals[1]);layout=json.loads(originals[2])
        if label=='failed_compile':compiled['returncode']=1
        elif label=='missing_actual_compile_time':compiled.pop('at_utc')
        elif label=='wrong_epoch':compiled['source_date_epoch']='0'
        elif label=='wrong_compile_source':compiled['source_sha256']='0'*64
        elif label=='wrong_compile_pdf':compiled['pdf_sha256']='0'*64
        elif label=='partial_visual':layout['all_pages_visually_inspected']=False
        elif label=='wrong_layout_source':layout['source_sha256']='0'*64
        elif label=='wrong_layout_pdf':layout['pdf_sha256']='0'*64
        elif label=='missing_actual_layout_time':layout.pop('at_utc')
        elif label=='wrong_positive_page_count':context['expected_pdf_pages']=4;layout['pages']=4;layout['page_indices_inspected']=[1,2,3,4]
        else:layout['page_indices_inspected']=[1,2]
        save(compiled_path,compiled);save(layout_path,layout);context['document_bindings']['compile_receipt_sha256']=sha(compiled_path);context['document_bindings']['layout_receipt_sha256']=sha(layout_path);save(cp,context)
        rejected.append(reject(b.document_bindings,label))
        for path,data in zip([cp,compiled_path,layout_path],originals):path.write_bytes(data)
    return rejected

def relocation_and_root_replay_controls(folder):
    v=load(ROOT/DEPLOY['verification/verify.py']);folder.mkdir(parents=True);registry=[]
    for n,(ek,pk,sk) in enumerate([('files','relative_path','bytes'),('authored_files','relative_path','bytes'),('entries','relative_path','bytes'),('members','path','bytes')]):
        base='reviews/extra'+str(n);path=folder/base/'MANIFEST.json';path.parent.mkdir(parents=True);payload=path.parent/'payload.md';payload.write_text('SYNTHETIC RELATIVE SCHEMA PAYLOAD\n');save(path,{ek:[{pk:'payload.md',sk:payload.stat().st_size,'sha256':sha(payload),'input_path':'/MUST/NOT/READ/THIS',**({'path':'/MUST/NOT/READ/THIS'} if pk!='path' else {})}]});registry.append({'path':path.relative_to(folder).as_posix(),'base':base,'entries_key':ek,'path_key':pk,'size_key':sk,'role':'math','sha256':sha(path)})
    v.authenticate_nested_manifests(folder,registry,require_complete=False);relocated=folder.parent/'relocated-copy';shutil.copytree(folder,relocated);v.authenticate_nested_manifests(relocated,registry,require_complete=False);rejected=[]
    for label,mutate in [('absolute_mode',lambda r:r.update(path_mode='absolute_under_family_root')),('guessed_key',lambda r:r.update(path_key='path')),('outside_base',lambda r:r.update(base='../outside')),('missing_role',lambda r:r.pop('role')),('wrong_role',lambda r:r.update(role='guessed'))]:
        changed=copy.deepcopy(registry[0]);mutate(changed);rejected.append(reject(lambda:v.authenticate_nested_manifests(folder,[changed],require_complete=False),label))
    # Selected relative membership alone is followed; absolute inputs never are.
    path=folder/registry[0]['path'];original=path.read_bytes();obj=json.loads(original);obj['files'][0]['relative_path']='/ABSOLUTE';save(path,obj);changed=copy.deepcopy(registry[0]);changed['sha256']=sha(path);rejected.append(reject(lambda:v.authenticate_nested_manifests(folder,[changed],require_complete=False),'absolute_selected_member'));path.write_bytes(original)
    # A literal declared members/path/bytes schema is supported; members is not
    # guessed from absolute input receipts or an arbitrary selected input key.
    explicit=registry[-1];path=folder/explicit['path'];original=path.read_bytes()
    changed=copy.deepcopy(explicit);changed['path_key']='input_path';rejected.append(reject(lambda:v.authenticate_nested_manifests(folder,[changed],require_complete=False),'members_input_path_schema_refused'))
    obj=json.loads(original);obj['members'][0].pop('path');save(path,obj);changed=copy.deepcopy(explicit);changed['sha256']=sha(path);rejected.append(reject(lambda:v.authenticate_nested_manifests(folder,[changed],require_complete=False),'members_missing_path_no_input_path_inference'));path.write_bytes(original)
    obj=json.loads(original);obj['members'].append(copy.deepcopy(obj['members'][0]));save(path,obj);changed=copy.deepcopy(explicit);changed['sha256']=sha(path);rejected.append(reject(lambda:v.authenticate_nested_manifests(folder,[changed],require_complete=False),'members_duplicate_relative_member'));path.write_bytes(original)
    program=folder/'root_exact_fixture.py';program.write_text("from pathlib import Path\nimport datetime,hashlib,json\np=Path(__file__);print(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'program_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'result':{'static':7,'at_utc':'NESTED_MUST_REMAIN'}}))\n")
    expected={'at_utc':'HISTORICAL TOP LEVEL ONLY','program_sha256':sha(program),'result':{'static':7,'at_utc':'NESTED_MUST_REMAIN'}};save(folder/'expected.json',expected);ctx={'diagnostic_replays':[{'program':program.name,'mode':'normal_O_OO','result':'expected.json','output_mode':'stdout','scope':'Synthetic root deterministic replay contract only.','layout':'isolated','arguments':[],'comparison':'json_ignore_at_utc'}]};v.replay_diagnostics(folder,ctx)
    bad=copy.deepcopy(expected);bad['result']['at_utc']='CORRUPTED';save(folder/'expected.json',bad);rejected.append(reject(lambda:v.replay_diagnostics(folder,ctx),'nested_time_not_ignored'))
    return {'explicit_relative_schemas_relocate':True,'explicit_members_path_bytes_relocates':True,'members_input_path_never_inferred':True,'unused_absolute_inputs_never_followed_as_membership':True,'no_absolute_membership_mode':True,'only_top_level_runtime_omissions':True,'negative_controls':rejected}

def historical_review_controls(f):
    pub=f['pub'];audit=f['audit'];u=load(pub/'update_pr_publication.py');gate=copy.deepcopy(f['gate']);first=gate['reviews'][0];latest=gate['reviews'][-1]
    def refresh(record):
        review=(pub/record['verdict']).parent;record['input_freeze_sha256']=sha(review/'INPUT_FREEZE.json');verdict=json.loads((review/'VERDICT.json').read_text());verdict.update(status=record['status'],current_context_sha256=record['context_sha256'],input_freeze_sha256=record['input_freeze_sha256']);save(review/'VERDICT.json',verdict);record['verdict_sha256']=sha(review/'VERDICT.json');manifest=json.loads((review/'MANIFEST.json').read_text())
        for entry in manifest['authored_files']:entry.update(binding(review/entry['path']))
        save(review/'MANIFEST.json',manifest);record['manifest_sha256']=sha(review/'MANIFEST.json')
    first['status']='CHANGES_REQUIRED';first['context_sha256']='1'*64;review=(pub/first['input_freeze']).parent;freeze=json.loads((review/'INPUT_FREEZE.json').read_text())
    for entry in freeze['files']:
        if entry['path']==str(audit/'CURRENT_PR1274_CONTEXT.json'):entry['sha256']='1'*64
        if entry['path']==str(audit/'current_edition/PROOF.md'):entry['sha256']='2'*64;entry['bytes']=1
    save(review/'INPUT_FREEZE.json',freeze);refresh(first)
    resolution=audit/'ROOT_R1_RESOLUTION.json';resolved={'schema':'math-pr1274-review-resolution-v1','status':'RESOLVED','pr':1274,'problem_id':2307072,'original_head':u.ORIGINAL,'reviewer_id':first['reviewer_id'],'review_verdict_sha256':first['verdict_sha256'],'review_input_freeze_sha256':first['input_freeze_sha256'],'review_context_sha256':first['context_sha256'],'resolved_context_sha256':gate['current_context_sha256'],'at_utc':'2026-10-17T21:00:01.500000Z','items':[{'finding':'Synthetic first-review correction.','resolution':'Synthetic repair in current context.','evidence':'Synthetic current proof bytes, not actual mathematical approval.'}]};save(resolution,resolved);first['resolution']='../ROOT_R1_RESOLUTION.json';first['resolution_sha256']=sha(resolution)
    later=(pub/latest['input_freeze']).parent;current=json.loads((later/'INPUT_FREEZE.json').read_text())
    for entry in current['files']:entry.update(binding(Path(entry['path'])))
    current['files'].append({'path':str(resolution),**binding(resolution)});save(later/'INPUT_FREEZE.json',current);refresh(latest);gate['latest_review']=latest;u.validate_workflow_gate(gate)
    save(pub/'FINAL_REVIEW_GATE.json',gate);os.environ['PATH']=f['env']['PATH'];operative=load(pub.parents[2]/'publication_coordinators/pr1274.py');need(operative.P.resolve()==pub.resolve(),'operative coordinator layout differs');need(operative.authenticate_release()==gate,'actual release preflight rejected repaired historical review sequence')
    rejected=[]
    for label,mutate in [('missing_resolution',lambda x:x['reviews'][0].pop('resolution')),('wrong_resolution_hash',lambda x:x['reviews'][0].update(resolution_sha256='0'*64)),('wrong_historical_context_identity',lambda x:x['reviews'][0].update(context_sha256='3'*64)),('wrong_historical_manifest_anchor',lambda x:x['reviews'][0].update(manifest_sha256='0'*64)),('latest_historical_context',lambda x:x['reviews'][-1].update(context_sha256='1'*64)),('latest_changes_required',lambda x:x['reviews'][-1].update(status='CHANGES_REQUIRED'))]:
        bad=copy.deepcopy(gate);mutate(bad);rejected.append(reject(lambda:u.validate_workflow_gate(bad),label))
    original=resolution.read_bytes()
    for label,mutate in [('unresolved_status',lambda x:x.update(status='PENDING')),('wrong_resolution_head',lambda x:x.update(original_head='0'*40)),('wrong_resolved_context',lambda x:x.update(resolved_context_sha256='0'*64)),('empty_resolution_items',lambda x:x.update(items=[])),('resolution_after_clean',lambda x:x.update(at_utc='2026-10-17T21:00:03Z'))]:
        changed=copy.deepcopy(resolved);mutate(changed);save(resolution,changed);bad=copy.deepcopy(gate);bad['reviews'][0]['resolution_sha256']=sha(resolution)
        if label=='resolution_after_clean':
            changed_freeze=json.loads((later/'INPUT_FREEZE.json').read_text())
            for entry in changed_freeze['files']:
                if entry['path']==str(resolution):entry.update(binding(resolution))
            save(later/'INPUT_FREEZE.json',changed_freeze);refresh(bad['reviews'][-1]);bad['latest_review']=bad['reviews'][-1]
        rejected.append(reject(lambda:u.validate_workflow_gate(bad),label))
    resolution.write_bytes(original)
    # Update the latest inventory hash after corrupting its own member binding:
    # current-byte verification must still reject it; historical bytes may differ.
    original_freeze=(later/'INPUT_FREEZE.json').read_bytes();bad=copy.deepcopy(gate);changed=json.loads(original_freeze)
    for entry in changed['files']:
        if entry['path']==str(pub/'prepare_package.py'):entry['sha256']='0'*64
    save(later/'INPUT_FREEZE.json',changed);refresh(bad['reviews'][-1]);bad['latest_review']=bad['reviews'][-1];rejected.append(reject(lambda:u.validate_workflow_gate(bad),'latest_current_bytes_still_required'))
    return {'changes_required_then_one_clean_accepted':True,'operative_full_authenticate_release_accepts_repaired_sequence':True,'earlier_historical_context_and_proof_hashes_preserved_without_current_byte_demand':True,'explicit_root_resolution_required':True,'actual_review_manifest_report_verdict_input_anchors_required':True,'negative_controls':rejected}

def coordinator_case(f,case):
    os.environ['PATH']=f['env']['PATH']  # This worker process contains only synthetic fixtures.
    pub=f['pub'];c=load(pub.parents[2]/'publication_coordinators/pr1274.py');kit=c.load_exact_kit();kit.STATE_DIR=pub/'synthetic-kit-state';kit.doi_status=lambda doi:{'status':'not_checked_fixture'}
    events=[];state={'deposit':None,'mutate_second_get':False,'lost_publish':False,'lose_followup':False}
    class Client:
        def create(self,metadata):events.append('POST create');state['deposit']={'id':123,'submitted':False,'metadata':copy.deepcopy(metadata),'files':[],'links':{'bucket':'fixture://bucket'}};return copy.deepcopy(state['deposit'])
        def get(self,number):
            events.append('GET '+str(number));need(number==123,'wrong requested ID')
            if state['lose_followup']:state['lose_followup']=False;raise kit.DepositError('synthetic lost follow-up GET')
            out=copy.deepcopy(state['deposit'])
            if state['mutate_second_get']:
                field=state['mutate_second_get'];state['mutate_second_get']=False
                if field is True:out['metadata']['description']=out['metadata']['description'].replace('&','&amp;')
                else:out['metadata'][field]=None
            return out
        def upload(self,bucket,entry):events.append('PUT file');state['deposit']['files'].append({'filename':entry['name'],'filesize':entry['size'],'checksum':'md5:'+entry['md5']})
        def update(self,number,metadata):events.append('PUT metadata');state['deposit']['metadata']=copy.deepcopy(metadata)
        def publish(self,number):
            events.append('POST publish');state['deposit']['submitted']=True;state['deposit']['doi']='10.5281/zenodo.123'
            if state['lost_publish']:state['lose_followup']=True;raise kit.DepositError('synthetic lost POST response')
    client=Client();c.live_preflight=lambda:events.append('mock live original PR/tracker preflight')
    def actual_call(loaded,command,known_id=None,check_doi=False):
        need(loaded is kit,'actual exact kit object changed')
        if command=='publish' and case=='normalization_between_inspect_and_POST':state['mutate_second_get']=True
        if command=='publish' and case.startswith('server_field_'):state['mutate_second_get']=case.removeprefix('server_field_')
        return kit.run(types.SimpleNamespace(command=command,manifest=pub/'zenodo-deposit.json',sandbox=False,confirm_id=known_id,check_doi=check_doi),client=client)
    c.call_kit=actual_call;c.execute('stage',kit);reject(lambda:c.execute('stage',kit),'second_stage_intent')
    if case=='normalization_between_inspect_and_POST' or case.startswith('server_field_'):
        reject(lambda:c.execute('publish',kit),'strict_actual_kit_second_GET_normalization',errors=(kit.DepositError,RuntimeError,ValueError));need('POST publish' not in events,'strict second verification allowed publish POST')
        reject(lambda:c.execute('publish',kit),'unresolved_intent_no_blind_retry');need('POST publish' not in events,'unresolved intent retried POST')
    else:
        state['lost_publish']=case=='uncertain_then_published_recovery'
        if state['lost_publish']:reject(lambda:c.execute('publish',kit),'uncertain_post_readonly_recovery',errors=(kit.DepositError,RuntimeError));need(events.count('POST publish')==1,'wrong publish attempts')
        result=c.execute('publish',kit);need(result['state']=='published' and result['id']==123,'published recovery differs');c.execute('publish',kit);need(events.count('POST publish')==1,'published recovery repeated POST')
    return {'case':case,'events':events,'actual_shared_kit_run_used':True,'all_network_methods_mocked':True}

def publication_and_tracker_controls(f):
    pub=f['pub'];t=load(pub/'append_tracker.py');p={'environment':'production','state':'published','metadata_normalizations':[],'id':123,'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','url':'https://doi.org/10.5281/zenodo.123','title':f['context']['title'],'files':[{'name':f['build'][key]['path'],'size':f['build'][key]['bytes'],'sha256':f['build'][key]['sha256']} for key in ['pdf','verification_zip']]};save(pub/'PUBLICATION_RECEIPT.json',p)
    badpub=[]
    for key,value in [('id',True),('doi','10.5281/zenodo.124'),('doi_url','http://doi.org/10.5281/zenodo.123'),('record_url','https://zenodo.org/record/123'),('url','https://example.com'),('environment','sandbox'),('state','draft'),('title','wrong'),('metadata_normalizations',[{}])]:
        bad=copy.deepcopy(p);bad[key]=value;badpub.append(reject(lambda:t.validate_publication_identity(bad,p['title']),key))
    rows=[['Original Problem','Solution Chat URL','DOI','Notes']];appends=[];lost={'once':True};renamed={'value':False}
    def call(parts,params,body=None):
        if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':t.GID,'title':'Renamed' if renamed['value'] else 'Math Puzzles'}}]}
        if parts==['spreadsheets','values','get']:return {'values':copy.deepcopy(rows if params['range']=="'Math Puzzles'!A:D" else [rows[1]])}
        if parts==['spreadsheets','values','append']:
            appends.append(copy.deepcopy(body));rows.append(body['values'][0])
            if lost['once']:lost['once']=False;raise RuntimeError('synthetic accepted append with lost response')
            return {'updates':{'updatedRange':"'Math Puzzles'!A2:D2",'updatedRows':1,'updatedColumns':4}}
        raise RuntimeError('Unexpected service fixture call')
    t.call=call;renamed['value']=True;reject(lambda:capture(t.main),'renamed_gid');need(not appends,'renamed tab appended');renamed['value']=False
    reject(lambda:capture(t.main),'accepted_append_lost_response');capture(t.main);capture(t.main);need(len(appends)==1,'idempotent tracker recovery appended twice')
    receipt=json.loads((pub/'tracker/TRACKER_RECEIPT.json').read_text());need(receipt['row'][1]=='','column B must remain blank');t.validate_tracker_receipt(receipt,p,p['title']);badrows=[]
    for i in range(4):
        bad=copy.deepcopy(receipt);bad['row'][i]='wrong';badrows.append(reject(lambda:t.validate_tracker_receipt(bad,p,p['title']),'cell'+str(i)))
    for raw in ["'Other'!A2:D2","'Math Puzzles'!A1:D1","'Math Puzzles'!A2:C2","'Math Puzzles'!A2:D3"]:
        bad=copy.deepcopy(receipt);bad['updatedRange']=raw;badrows.append(reject(lambda:t.validate_tracker_receipt(bad,p,p['title']),raw))
    rows.append(copy.deepcopy(rows[1]));reject(lambda:capture(t.main),'duplicate_tracker_rows');rows.pop();saved=rows[1][3];rows[1][3]='same identity wrong notes';reject(lambda:capture(t.main),'identity_collision_full_row_mismatch');rows[1][3]=saved
    m=load(pub/'check_public_downloads.py');metadata=f['context']['metadata'];actual=copy.deepcopy(metadata);actual['resource_type']={'type':actual.pop('upload_type'),'subtype':actual.pop('publication_type')};actual['license']={'id':actual['license']};actual['doi']=p['doi'];m.verify_public_metadata(actual,metadata);badmeta=[]
    for key in metadata:
        bad=copy.deepcopy(actual)
        if key=='upload_type':bad['resource_type']['type']='wrong'
        elif key=='publication_type':bad['resource_type']['subtype']='wrong'
        elif key=='license':bad['license']['id']='wrong'
        else:bad[key]=None
        badmeta.append(reject(lambda:m.verify_public_metadata(bad,metadata),key))
    public={'id':123,'doi':p['doi'],'metadata':actual,'files':[{'key':f['build'][key]['path'],'links':{'self':'https://fixture.invalid/'+f['build'][key]['path']}} for key in ['pdf','verification_zip']]}
    def fetch(url,limit):
        data=json.dumps(public).encode() if url=='https://zenodo.org/api/records/123' else (pub/url.rsplit('/',1)[-1]).read_bytes();need(len(data)<=limit,'fixture response limit');return data
    m.fetch=fetch;capture(m.main)
    return p,receipt,{'canonical_identity_rejections':badpub,'full_row_range_rejections':badrows,'one_append_despite_lost_response':True,'all11_public_fields':sorted(metadata),'each_field_corruption_rejected':sorted(badmeta),'full_public_check_main_mocked':True}

def update_controls(f,pubrecord,tracker):
    pub=f['pub'];u=load(pub/'update_pr_publication.py');files,publication,note=u.desired_files(f['build'],pubrecord,tracker,f['snapshot']);need(len(files)==11 and len(publication)==5,'wrong intended6+5 scope')
    body=note+'\nThe six-file PUBLIC_MANIFEST.json binds the five other current edition records through files/path/bytes/sha256. publication_20261017/ adds the reviewed preprint, portable verification archive, matching deposit metadata, publication receipt and README. Original historical files are preserved in the portable archive.\n'
    wanted=u.expected_identity(pubrecord,tracker,files,body);commit='a'*40;calls=[];mode={'bad':None};state={'headRefOid':commit,'headRefName':u.BRANCH,'state':'OPEN','isDraft':True,'body':body}
    def git(*args,data=None):
        calls.append(args)
        if args==('branch','--show-current'):return b'main\n'
        if args[0]=='rev-list':return (commit+' '+('b'*40 if mode['bad']=='parent' else u.ORIGINAL)+'\n').encode()
        if args[0]=='diff-tree':return ('\n'.join(sorted(files)+(['foreign/path'] if mode['bad']=='paths' else []))+'\n').encode()
        if args[0]=='show':return b'wrong' if mode['bad']=='bytes' else files[args[1].split(':',1)[1]]
        if args[0]=='ls-remote':return (commit+' refs/heads/'+u.BRANCH+'\n').encode()
        raise RuntimeError('Forbidden unmocked/new Git operation '+repr(args))
    u.git=git;u.pr=lambda:copy.deepcopy(state);intent={**wanted,'commit':commit};u.validate_saved(intent,wanted,files);badkeys=[]
    for key in wanted:
        bad=copy.deepcopy(intent)
        if key=='files':bad[key][sorted(files)[0]]['sha256']='0'*64
        elif isinstance(bad[key],list):bad[key].append('foreign/path')
        elif isinstance(bad[key],bool):bad[key]=not bad[key]
        elif isinstance(bad[key],int):bad[key]+=1
        else:bad[key]='wrong'
        badkeys.append(reject(lambda:u.validate_saved(bad,wanted,files),key))
    for key in ['parent','paths','bytes']:
        mode['bad']=key;badkeys.append(reject(lambda:u.validate_saved(intent,wanted,files),'actual_tree_'+key))
    mode['bad']=None;save(pub/'PR_BRANCH_INTENT.json',intent);capture(u.main);capture(u.main)
    need(all(args[0] in {'branch','rev-list','diff-tree','show','ls-remote'} for args in calls),'recovery made Git mutation')
    bodycalls=[];state['body']='synthetic original body';original=hashlib.sha256(state['body'].encode()).hexdigest();(pub/'PR_BODY_FINAL.md').write_text(body)
    def edit(args,**kwargs):bodycalls.append(args);state['body']=body;return types.SimpleNamespace(returncode=1,stderr='synthetic lost edit response')
    u.subprocess=types.SimpleNamespace(run=edit);reject(lambda:u.synchronize_pr_body(commit,body,original),'lost_body_response');u.synchronize_pr_body(commit,body,original);need(len(bodycalls)==1,'lost body response repeated already accepted edit')
    state['body']='unknown outside edit';reject(lambda:u.synchronize_pr_body(commit,body,original),'outside_body_change')
    return {'desired_files':len(files),'current_edition':6,'publication_additions':5,'stale_identity_and_actual_tree_rejected':badkeys,'complete_update_main_saved_intent_recovery_and_completed_readback':True,'body_lost_response_exact_readback_and_outside_change':True,'no_index_or_force_or_git_mutation_in_test':True,'fresh_object_construction_not_executed':'Actual Git object/tree creation and branch push remain a later integration operation.'}

def identity_matrix(folder):
    """Current operative preflight/append predicates in every one of four cells."""
    folder.mkdir(parents=True);out=[]
    context={'title':'SYNTHETIC IDENTITY MATRIX','tracker':{'original_problem':'2307072 (AMR0227072); https://github.com/AlecKriebel/Math/pull/1274','notes':'Synthetic notes'}}
    pub={'environment':'production','state':'published','metadata_normalizations':[],'id':123,'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','title':context['title']}
    identities={'numeric':'2307072',**ALIAS_VARIANTS,'PR':'https://github.com/AlecKriebel/Math/pull/1274','bareDOI':'  10.5281/zenodo.123  ','DOIURL':'  https://doi.org/10.5281/zenodo.123  ','unrelated':'Unrelated42',**ALIAS_NEAR_COLLISIONS}
    for kind in ['preflight_unknown','preflight_known','append']:
      for label,identity in identities.items():
       for column in range(4):
        root=folder/(kind+'_'+label+'_'+str(column));p=root/'publication';p.mkdir(parents=True)
        t=load(ROOT/'append_tracker.py');t.ROOT=p;c=load(COORDINATOR);c.P=p;c.A=root
        save(p/'PUBLICATION_RECEIPT.json',pub);save(p/'zenodo-deposit.json',{'metadata':{'title':context['title']}});save(p/'FINAL_REVIEW_GATE.json',{'synthetic_fixture_only':True})
        if kind=='preflight_unknown':(p/'PUBLICATION_RECEIPT.json').unlink()
        if kind=='preflight_known':save(p/'STAGE_RECEIPT.json',{'id':123})
        rows=[['Original Problem','Solution Chat URL','DOI','Notes'],['','','','']];rows[1][column]=identity;events=[]
        def call(parts,params,body=None):
            events.append(parts)
            if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':t.GID,'title':'Math Puzzles'}}]}
            if parts==['spreadsheets','values','get']:return {'values':copy.deepcopy(rows if params['range']=="'Math Puzzles'!A:D" else [rows[-1]])}
            if parts==['spreadsheets','values','append']:rows.append(copy.deepcopy(body['values'][0]));return {'updates':{'updatedRange':"'Math Puzzles'!A3:D3",'updatedRows':1,'updatedColumns':4}}
            raise RuntimeError('Unexpected mocked call')
        t.call=call
        def run_path(path):
            name=Path(path).name
            if name=='append_tracker.py':return t.__dict__
            if name=='prepare_package.py':return {'load_context':lambda:copy.deepcopy(context)}
            if name=='update_pr_publication.py':return {'validate_workflow_gate':lambda gate:None}
            raise RuntimeError('Unexpected mocked module '+name)
        t.runpy=types.SimpleNamespace(run_path=run_path);c.runpy=types.SimpleNamespace(run_path=run_path)
        body='SYNTHETIC ORIGINAL BODY';snapshot={'head':'fc334f4bd5d8cbc2a241293e2b1419d35c7eead1','branch':'research/2307072-beurling-annihilator-witnesses','body_sha256':hashlib.sha256(body.encode()).hexdigest()};save(root/'SUBMITTED_SNAPSHOT.json',snapshot)
        live={'state':'OPEN','isDraft':True,'headRefOid':snapshot['head'],'headRefName':snapshot['branch'],'body':body}
        def external(args,**kw):return json.dumps(live) if args[0]=='gh' else snapshot['head']+' refs/heads/'+snapshot['branch']+'\n'
        c.subprocess=types.SimpleNamespace(check_output=external)
        try:capture(t.main if kind=='append' else c.live_preflight);accepted=True
        except (RuntimeError,ValueError,KeyError):accepted=False
        unrelated=label=='unrelated' or label in ALIAS_NEAR_COLLISIONS
        wanted=unrelated or kind=='preflight_unknown' and label in {'bareDOI','DOIURL'}
        count=events.count(['spreadsheets','values','append']);need(accepted==wanted and count==(1 if kind=='append' and unrelated else 0),'Identity action matrix differs '+repr((kind,label,column,accepted,count)))
        out.append({'stage':kind,'identity':label,'column':column,'accepted':accepted,'appends':count})
    # Exact intended row is recoverable without any append mutation, even with no previous intent.
    row=t.expected_row(pub,context['title']);rows[:]=[rows[0],row];capture(t.main);need(events.count(['spreadsheets','values','append'])==1,'Exact row recovery made another append')
    return {'cases':out,'exact_full_row_recovered_readonly':True,'predicate_source':'actual append_tracker.py shared by all three action times','known_DOI_preflight_required':True,'all_external_operations_mocked':True}

def postmerge_controls(f):
    """Complete actual current verifier main; all services/Git calls are mocked."""
    pubpath=f['pub'];audit=f['audit'];program=audit.parents[1];u=load(pubpath/'update_pr_publication.py');t=load(pubpath/'append_tracker.py');m=load(pubpath.parents[2]/'publication_coordinators/verify_pr1274_merge.py')
    original_pub=json.loads((pubpath/'PUBLICATION_RECEIPT.json').read_text());original_tracker=json.loads((pubpath/'tracker/TRACKER_RECEIPT.json').read_text());original_public=json.loads((pubpath/'PUBLIC_DOWNLOAD_VERIFICATION.json').read_text())
    cases=['baseline','doi_fallback_valid','wrong_gid_same_title','missing_gid','duplicate_designated_gid','wrong_title','bad_headers','missing_row',*[f'wrong_cell_{i}' for i in range(4)],'range_wrong','checkout_wrong','merge_parent_wrong','merge_single_parent','merge_three_parents','merged_bytes_wrong','live_open','live_head_wrong','live_branch_wrong','live_body_wrong','live_url_wrong','saved_body_unverified','saved_remote_unverified','public_false','public_identity_false','public_id_wrong','public_doi_wrong','doi_unresolved','doi_wrong_status','state_current_wrong','state_completed_wrong','state_eligible_wrong','state_publications_wrong']
    aliases={'numeric':'2307072',**ALIAS_VARIANTS,'PR':'https://github.com/AlecKriebel/Math/pull/1274','bareDOI':'  10.5281/zenodo.123  ','DOIURL':'  https://doi.org/10.5281/zenodo.123  '}
    cases += ['duplicate_'+label+'_'+str(column) for label in aliases for column in range(4)]
    cases += ['unrelated_'+label+'_'+str(column) for label in ALIAS_NEAR_COLLISIONS for column in range(4)]
    cases += ['merged_blob_'+str(index) for index in range(11)]
    cases += ['state_eligible_count_wrong','state_completed_duplicate','state_publications_duplicate'];out=[]
    for case in cases:
        pub=copy.deepcopy(original_pub);tracker=copy.deepcopy(original_tracker);public=copy.deepcopy(original_public);events=[];head='a'*40;merge='c'*40;first='d'*40
        pub['doi_resolution']={'status':'resolved','http_status':200}
        if case.startswith('doi_'):pub['doi_resolution']={'status':'not_checked'};save(pubpath/'DOI_INSPECT.json',{**pub,'doi_resolution':{'status':'resolved','http_status':200 if case=='doi_fallback_valid' else 201} if case!='doi_unresolved' else {'status':'not_resolved','http_status':404}})
        save(pubpath/'PUBLICATION_RECEIPT.json',pub)
        if case=='range_wrong':tracker['updatedRange']="'Math Puzzles'!A3:D3"
        save(pubpath/'tracker/TRACKER_RECEIPT.json',tracker)
        files,_,_=u.desired_files(f['build'],pub,tracker,f['snapshot']);body=(pubpath/'PR_BODY_FINAL.md').read_text()
        for label,key,value in [('public_false','all_supplied_metadata_exact',False),('public_identity_false','public_record_identity_verified',False),('public_id_wrong','id',124),('public_doi_wrong','doi','10.5281/zenodo.124')]:
            if case==label:public[key]=value
        save(pubpath/'PUBLIC_DOWNLOAD_VERIFICATION.json',public);wanted=u.expected_identity(pub,tracker,files,body)
        for name in ['PR_BRANCH_INTENT.json','PR_BRANCH_RECEIPT.json']:save(pubpath/name,{**wanted,'commit':head,'body_readback_verified':case!='saved_body_unverified','remote_readback_verified':case!='saved_remote_unverified'})
        def git(*args,data=None):
            events.append({'git':list(args)})
            if args==('branch','--show-current'):return b'other\n' if case=='checkout_wrong' else b'main\n'
            if args[0]=='rev-list':
                if args[-1]==merge:
                    parents=[first,head]
                    if case=='merge_parent_wrong':parents=[head,first]
                    if case=='merge_single_parent':parents=[head]
                    if case=='merge_three_parents':parents=[first,head,'e'*40]
                    return (' '.join([merge]+parents)+'\n').encode()
                return (head+' '+u.ORIGINAL+'\n').encode()
            if args[0]=='diff-tree':return ('\n'.join(sorted(files))+'\n').encode()
            if args[0]=='show':
                name=args[1].split(':',1)[1]
                corrupt=case=='merged_bytes_wrong' or case.startswith('merged_blob_') and name==sorted(files)[int(case.removeprefix('merged_blob_'))]
                return b'corrupt' if corrupt and args[1].startswith(merge+':') else files[name]
            if args[0] in {'fetch','update-ref'}:return b''
            raise RuntimeError('Forbidden unmocked Git operation '+repr(args))
        u.git=git
        tabs=[{'properties':{'sheetId':t.GID,'title':'Math Puzzles'}}]
        if case=='wrong_gid_same_title':tabs=[{'properties':{'sheetId':t.GID,'title':'Other'}},{'properties':{'sheetId':999,'title':'Math Puzzles'}}]
        if case=='missing_gid':tabs=[{'properties':{'sheetId':999,'title':'Math Puzzles'}}]
        if case=='duplicate_designated_gid':tabs+=copy.deepcopy(tabs)
        if case=='wrong_title':tabs[0]['properties']['title']='Other'
        rows=[['Original Problem','Solution Chat URL','DOI','Notes'],copy.deepcopy(tracker['row'])]
        if case=='bad_headers':rows[0][1]='Wrong'
        if case=='missing_row':rows=rows[:1]
        if case.startswith('wrong_cell_'):rows[1][int(case[-1])]='Wrong'
        if case.startswith('duplicate_') and case!='duplicate_designated_gid':
            _,label,column=case.split('_');row=['','','',''];row[int(column)]=aliases[label];rows.append(row)
        if case.startswith('unrelated_'):
            _,label,column=case.split('_');row=['','','',''];row[int(column)]=ALIAS_NEAR_COLLISIONS[label];rows.append(row)
        def call(parts,params,body=None):
            events.append({'gws':parts})
            if parts==['spreadsheets','get']:return {'sheets':copy.deepcopy(tabs)}
            if parts==['spreadsheets','values','get']:return {'values':copy.deepcopy(rows)}
            raise RuntimeError('Forbidden service mutation')
        t.call=call
        def run_path(path):
            if Path(path).name=='update_pr_publication.py':return u.__dict__
            if Path(path).name=='append_tracker.py':return t.__dict__
            raise RuntimeError('Unexpected mocked module')
        m.runpy=types.SimpleNamespace(run_path=run_path)
        live={'state':'MERGED','headRefOid':head,'headRefName':u.BRANCH,'mergeCommit':{'oid':merge},'mergedAt':'2026-10-17T21:00:00Z','body':body,'url':'https://github.com/AlecKriebel/Math/pull/1274'}
        for label,key,value in [('live_open','state','OPEN'),('live_head_wrong','headRefOid','e'*40),('live_branch_wrong','headRefName','other'),('live_body_wrong','body','wrong'),('live_url_wrong','url','https://github.com/AlecKriebel/Math/pull/1280')]:
            if case==label:live[key]=value
        def external(args,**kwargs):events.append({'gh':args});return json.dumps(live)
        m.subprocess=types.SimpleNamespace(check_output=external)
        state={'current_pr':1274,'completed_prs':copy.deepcopy(m.COMPLETED_BEFORE),'publications':[{'pr':n} for n in m.COMPLETED_BEFORE],'eligible_prs':copy.deepcopy(m.ELIGIBLE),'eligible_count':12}
        if case=='state_current_wrong':state['current_pr']=1280
        if case=='state_completed_wrong':state['completed_prs']=state['completed_prs'][:-1]
        if case=='state_eligible_wrong':state['eligible_prs']=[]
        if case=='state_publications_wrong':state['publications']=[]
        if case=='state_eligible_count_wrong':state['eligible_count']=13
        if case=='state_completed_duplicate':state['completed_prs'].append(m.COMPLETED_BEFORE[-1])
        if case=='state_publications_duplicate':state['publications'].append({'pr':m.COMPLETED_BEFORE[-1]})
        save(program/'PROGRAM_STATE.json',state)
        rejection=None
        try:capture(m.main);accepted=True
        except (RuntimeError,ValueError,KeyError,FileNotFoundError) as error:accepted=False;rejection=str(error)
        after=json.loads((program/'PROGRAM_STATE.json').read_text());wanted_accept=case in {'baseline','doi_fallback_valid'} or case.startswith('unrelated_');need(accepted==wanted_accept,'Postmerge guard differs '+case)
        need(after['current_pr']==(1280 if wanted_accept else state['current_pr']),'Postmerge state advanced despite failure '+case)
        if not wanted_accept:need(after==state,'Postmerge program state mutated despite failure '+case)
        if case.startswith('duplicate_') and case!='duplicate_designated_gid':need(rejection=='Missing/different/duplicate problem or DOI row','Alias duplicate did not reach the exact actual postmerge identity check '+case)
        if case.startswith('merged_blob_'):
            target=sorted(files)[int(case.removeprefix('merged_blob_'))]
            need(rejection=='Merged bytes differ '+target,'Per-file corruption did not reach its exact merged-blob check '+case)
        if wanted_accept:need(after['completed_prs']==m.COMPLETED_BEFORE+[1274] and len(after['publications'])==10,'Expected9 to10 completed only');observed=json.loads((pubpath/'tracker/POSTMERGE_READBACK.json').read_text());need(observed['observed_sheet_properties']=={'sheetId':t.GID,'title':'Math Puzzles'},'Current observed tab receipt differs')
        out.append({'case':case,'accepted':accepted,'state_advanced':wanted_accept,'events':events,'corrupt_path':sorted(files)[int(case.removeprefix('merged_blob_'))] if case.startswith('merged_blob_') else None})
    return {'cases':out,'current_source_sha256':sha(POSTMERGE),'all_operations_mocked':True,'scope':'Actual current source complete main on synthetic receipts; no production integration.'}

def worker():
    scratch=REPORT_ROOT/'_local';scratch.mkdir(parents=True,exist_ok=True);os.environ['TMPDIR']=str(scratch);tempfile.tempdir=str(scratch)
    with tempfile.TemporaryDirectory(prefix='synthetic-offline-',dir=scratch) as tmp:
        base=Path(tmp);f=fixture(base/'main');context=context_and_portable_controls(f);documents=document_controls(f);reviews=review_controls(f);p,t,public=publication_and_tracker_controls(f);updates=update_controls(f,p,t)
        identities=identity_matrix(base/'identity-matrix');postmerge=postmerge_controls(f);relocation=relocation_and_root_replay_controls(base/'relocation');history=historical_review_controls(fixture(base/'historical-reviews'));coordinator=[]
        for case in ['successful_publish','normalization_between_inspect_and_POST','uncertain_then_published_recovery']+['server_field_'+name for name in sorted(f['context']['metadata'])]:
            other=fixture(base/case);coordinator.append(coordinator_case(other,case))
        current_metadata={'scope':'Actual current metadata absent; only eleven-field synthetic metadata was tested.','sha256':None}
        if (ROOT/'zenodo-deposit.json').exists():
            wanted=json.loads((ROOT/'zenodo-deposit.json').read_text())['metadata'];v=load(ROOT/DEPLOY['verification/verify.py']);v.metadata_contract(wanted);m=load(ROOT/'check_public_downloads.py');actual=copy.deepcopy(wanted);actual['resource_type']={'type':actual.pop('upload_type'),'subtype':actual.pop('publication_type')};actual['license']={'id':actual['license']};fields=m.verify_public_metadata(actual,wanted)
            current_metadata={'scope':'Actual current local metadata projected and compared offline; no public API/record is implied.','sha256':sha(ROOT/'zenodo-deposit.json'),'fields':fields}
        return {'status':'PASS','context_and_portable':context,'identity_action_matrix':identities,'postmerge_complete_main':postmerge,'document_assurance_rejections':documents,'review_gate_rejections':reviews,'relocation_and_root_replay':relocation,'historical_review_sequence':history,'tracker_and_public':public,'current_local_metadata_projection':current_metadata,'PR_update':updates,'deposit_coordinator_actual_kit_mocked_clients':coordinator,'operative_coordinator_layout':'program/publication_coordinators/pr1274.py resolves program/audits/pr1274_2307072/publication','scope':'Synthetic fixture metadata/gates/compiler/pdfinfo/reviewer evidence only, except any explicitly reported actual local metadata projection. No real mathematical/priority adjudication, actual PDF compilation/rendering, service integration, Git mutation, staging/upload/publication/tracker append or PR change occurred.'}

def main():
    if '--worker' in sys.argv:print(json.dumps(worker(),sort_keys=True));return
    runs=[]
    for flags in [[],['-O'],['-OO']]:
        run=subprocess.run([sys.executable,'-B',*flags,str(Path(__file__).resolve()),'--worker'],capture_output=True,text=True);need(run.returncode==0,run.stderr);runs.append({'flags':flags,'result':json.loads(run.stdout)})
    need(all(item['result']==runs[0]['result'] for item in runs),'optimization-dependent guards')
    receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':runs,'all_modes_identical':True,'authored_workflow_sha256':{str(ROOT/source):sha(ROOT/source) for source in DEPLOY.values()}|{str(COORDINATOR):sha(COORDINATOR),str(POSTMERGE):sha(POSTMERGE)},'scope':'Offline synthetic fixture regressions only; final actual package requires rerun and independent whole-package review.'}
    save(REPORT_ROOT/'_local/WORKFLOW_REGRESSION_RECEIPT.json',receipt);print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
