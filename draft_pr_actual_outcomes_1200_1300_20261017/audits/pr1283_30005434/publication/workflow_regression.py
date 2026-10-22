#!/usr/bin/env python3
"""Synthetic offline guard and complete-main checks; no live service or Git call.

All fabricated metadata, gates, PDFs, source and reviewer records live only in
ignored _local temporary fixtures. These tests do not clear a real release.
"""
from pathlib import Path
import contextlib,copy,datetime,hashlib,importlib.util,io,json,os,shutil,subprocess,sys,tempfile,types,zipfile
ROOT=Path(__file__).resolve().parent
COORDINATOR=ROOT.parents[2]/'publication_coordinators/pr1283.py'
POSTMERGE=ROOT.parents[2]/'publication_coordinators/verify_pr1283_merge.py'
READY=ROOT.parent/'_local/ready_and_merge.py'
REPORT_ROOT=Path('/Users/alec/Documents/Math/draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1283_30005434/reviews/workflow_tooling')
NAMES=['prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py']
DEPLOY={name:(('verification_verify.py' if (ROOT/'verification_verify.py').exists() else name) if name=='verification/verify.py' else name) for name in NAMES}
ALIAS_VARIANTS={'alias':'oWr12697693005','aliasHyphen':'OWR-12697693-005','aliasSpace':'oWR 12697693 005','aliasUnderscore':'OWR_12697693_005','aliasMixed':'oWr - 12697693_005','aliasUnpadded':'OWR-12697693-5','aliasZeroPad':'OWR_0012697693_0005','aliasZeroPadCompact':'OWR00126976930005'}
ALIAS_NEAR_COLLISIONS={'nearHyphen':'OWR-12697693-0059','nearSpace':'OWR 12697693 0059','nearUnderscore':'OWR_12697693_0059','nearCompact':'OWR126976930059','nearWrongGroup':'OWR-112697693-005','nearTrailingLetter':'OWR-12697693-005x','nearLeadingLetter':'XOWR-12697693-005'}
PROBLEM_IDENTITIES={'numeric':'30005434','numericProse':'Problem (30005434), checked.',**ALIAS_VARIANTS,'PR':'https://github.com/AlecKriebel/Math/pull/1283','PRColon':'PR:https://github.com/AlecKriebel/Math/pull/1283','PRFiles':'https://github.com/AlecKriebel/Math/pull/1283/files','PRCommits':'https://github.com/AlecKriebel/Math/pull/1283/commits','PRChecks':'https://github.com/AlecKriebel/Math/pull/1283/checks','PRQuery':'https://github.com/AlecKriebel/Math/pull/1283?extra','PRFragment':'https://github.com/AlecKriebel/Math/pull/1283#extra','PRProse':'Reviewed (https://github.com/AlecKriebel/Math/pull/1283).','PRMarker':'PR1283','PRSpace':'PR 1283','PRHash':'PR#1283','PRSpaceHash':'PR #1283','PRMarkerProse':'Reviewed PR1283; accepted.','PRSpaceProse':'Reviewed (PR 1283).','PRHashProse':'Reviewed PR #1283, accepted.'}
DOI_IDENTITIES={'DOIColon':'DOI:10.5281/zenodo.123;','DOIURLColon':'See:https://doi.org/10.5281/zenodo.123;','DOIURLDownload':'https://doi.org/10.5281/zenodo.123?download=1','DOIURLQuery':'https://doi.org/10.5281/zenodo.123?extra','DOIURLFragment':'https://doi.org/10.5281/zenodo.123#extra','bareDOI':'  10.5281/zenodo.123  ','DOIURL':'  https://doi.org/10.5281/zenodo.123  ','bareDOIProse':'Published result (10.5281/zenodo.123), checked.','DOIURLProse':'Published result https://doi.org/10.5281/zenodo.123.'}
IDENTITY_NEAR_COLLISIONS={'nearPRSubviewSuffix':'PR:https://github.com/AlecKriebel/Math/pull/1283/filesx','nearPRSubviewNumber':'https://github.com/AlecKriebel/Math/pull/12830/files','nearPRColonNumber':'PR:https://github.com/AlecKriebel/Math/pull/12830','nearDOIColonSuffix':'DOI:10.5281/zenodo.1234;','nearDOIURLColonSuffix':'See:https://doi.org/10.5281/zenodo.1234;','nearDOIQueryNumber':'https://doi.org/10.5281/zenodo.1234?download=1','bareProblemHash':'#1283','bareProblemHashProse':'Math problem #1283, independent.',**ALIAS_NEAR_COLLISIONS,'nearNumericSuffix':'300054340','nearNumericPrefix':'130005434','nearNumericLetterPrefix':'X30005434','nearNumericLetterSuffix':'30005434x','nearPRURLSuffix':'https://github.com/AlecKriebel/Math/pull/12830','nearPRURLPrefix':'xhttps://github.com/AlecKriebel/Math/pull/1283','nearPRURLLetter':'https://github.com/AlecKriebel/Math/pull/1283x','nearPRURLPath':'https://github.com/AlecKriebel/Math/pull/1283/extra','nearPRMarkerSuffix':'PR12830','nearPRSpaceSuffix':'PR 12830','nearPRHashSuffix':'#12830','nearPRMarkerPrefix':'XPR1283','nearPRMarkerLetter':'PR1283x','nearPRHashPrefix':'X#1283','nearDOISuffix':'10.5281/zenodo.1234','nearDOIPrefix':'x10.5281/zenodo.123','nearDOILetter':'10.5281/zenodo.123x','nearDOIPath':'10.5281/zenodo.123/extra','nearDOIDot':'10.5281/zenodo.123.1','nearDOIHyphen':'10.5281/zenodo.123-extra','nearDOIURLSuffix':'https://doi.org/10.5281/zenodo.1234','nearDOIURLPrefix':'xhttps://doi.org/10.5281/zenodo.123','nearDOIURLPath':'https://doi.org/10.5281/zenodo.123/extra','otherDOI':'An unrelated DOI 10.5281/zenodo.456.','otherDOIURL':'An unrelated DOI https://doi.org/10.5281/zenodo.456.'}


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

def fixture(folder, source_mode='documented_correction'):
    audit=folder/'program/audits/pr1283_30005434';pub=audit/'publication';pub.mkdir(parents=True)
    for deployed,source in DEPLOY.items():
        path=pub/deployed;path.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/source,path)
    coordinator=pub.parents[2]/'publication_coordinators/pr1283.py';coordinator.parent.mkdir();shutil.copyfile(COORDINATOR,coordinator);postmerge=coordinator.parent/'verify_pr1283_merge.py';shutil.copyfile(POSTMERGE,postmerge)
    ready=audit/'_local/ready_and_merge.py';ready.parent.mkdir();shutil.copyfile(READY,ready)
    v=load(pub/'verification/verify.py');submitted=audit/'submitted';submitted.mkdir()
    actual=Path('/Users/alec/Documents/Math/draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1283_30005434')
    need(sha(actual/'SUBMITTED_SNAPSHOT.json')=='da2152816bbcd548e4db411ab57992c121009d935e2de59b3f6de93ae304a1d6','pinned actual submitted snapshot changed')
    for name in v.NAMES:shutil.copyfile(actual/'submitted'/name,submitted/name)
    snapshot=json.loads((actual/'SUBMITTED_SNAPSHOT.json').read_text());save(audit/'SUBMITTED_SNAPSHOT.json',snapshot)
    v.authenticate_snapshot(submitted,snapshot)
    current=audit/'current_edition';shutil.copytree(submitted,current)
    if source_mode=='documented_correction':(current/'PROOF_CLASSIFICATION.md').write_text((current/'PROOF_CLASSIFICATION.md').read_text()+'SYNTHETIC CONTROLLED DOCUMENTARY QUALIFICATION; THEOREM UNCHANGED\n')
    current_manifest=json.loads((submitted/'MANIFEST.json').read_text());current_manifest['files']=[{'file':n,**binding(current/n)} for n in sorted(v.NAMES-{'MANIFEST.json'})];current_manifest['covered_bytes']=sum(e['bytes'] for e in current_manifest['files'])
    if source_mode=='documented_correction':save(current/'MANIFEST.json',current_manifest)
    original_map={n:binding(submitted/n) for n in v.NAMES};current_map={n:binding(current/n) for n in v.NAMES}
    correction={'schema':'math-pr1283-current-edition-correction-v1','at_utc':'2026-10-17T21:00:00Z','pr':v.PR,'problem_id':v.PROBLEM,'original_head':v.ORIGINAL,'submitted_snapshot_sha256':sha(audit/'SUBMITTED_SNAPSHOT.json'),'original_files':original_map,'current_files':current_map,'changes':[{'path':n,'original_sha256':original_map[n]['sha256'],'current_sha256':current_map[n]['sha256'],'reason':'SYNTHETIC CONTROLLED DOCUMENTARY CORRECTION ONLY'} for n in sorted(v.NAMES) if original_map[n]!=current_map[n]],'scope':'SYNTHETIC CORRECTION FIXTURE ONLY; NO ACTUAL MATHEMATICAL APPROVAL'}
    if source_mode=='documented_correction':save(audit/'CURRENT_EDITION_CORRECTION.json',correction)
    source_bindings={'submitted_snapshot_sha256':sha(audit/'SUBMITTED_SNAPSHOT.json'),'current_edition_correction_sha256':sha(audit/'CURRENT_EDITION_CORRECTION.json') if source_mode=='documented_correction' else None,'current_edition':current_map}
    for name in ['MATH_GATE.json','PRIORITY_ADJUDICATION.json']:save(audit/name,{'pr':v.PR,'problem_id':v.PROBLEM,'original_head':v.ORIGINAL,'status':'PASS','synthetic_fixture_only':True,'firstness_claim':False,'current_openness_claim':False,'novelty_clearance':False,**({'mathematical_gate_sha256':sha(audit/'MATH_GATE.json')} if name.startswith('PRIORITY') else {})})
    source_program="from pathlib import Path\nimport json\nif 2+2!=4:raise RuntimeError('fixture arithmetic check')\n(Path(__file__).parent/'result.json').write_text(json.dumps({'synthetic_exact':4})+'\\n')\n"
    analyst_program="from pathlib import Path\nimport argparse,json,sys\np=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()\nr=Path(__file__).parents[2];s=json.loads((r/'SUBMITTED_SNAPSHOT.json').read_text())\nif len(s['files'])!=8:raise RuntimeError('fixture original count')\nfor e in s['files']:\n if not (r/e['local_path']).is_file():raise RuntimeError('fixture original file missing')\nPath(a.output).write_text(json.dumps({'synthetic_exact':8,'run_utc':'fixture runtime','python':sys.version,'optimization':sys.flags.optimize})+'\\n')\n"
    registry=[];portable=[]
    shapes=[('reviews/source_question_family/manifest.json','files','relative_path','size_bytes',source_program),('reviews/analytic_adversary/MANIFEST.json','authored_files','path','bytes',analyst_program),('reviews/explicit_members_family/MANIFEST.json','members','path','bytes',None),('priority/fixture/FREEZE_MANIFEST.json','entries','path','bytes',None)]
    for raw,entries_key,path_key,size_key,program in shapes:
        path=audit/raw;path.parent.mkdir(parents=True,exist_ok=True);(path.parent/'payload.md').write_text('SYNTHETIC FROZEN EVIDENCE\n')
        if program:
            (path.parent/'checker.py').write_text(program)
            (path.parent/'result.json').write_text(json.dumps({'synthetic_exact':4} if 'source_question' in raw else {'synthetic_exact':8,'run_utc':'prior fixture runtime','python':'prior fixture Python','optimization':0})+'\n')
        entries=[]
        for child in sorted(path.parent.iterdir()):
            data=binding(child);entries.append({path_key:child.name,size_key:data['bytes'],'sha256':data['sha256'],'input_path':'/ABSOLUTE/INPUT/MUST/NEVER/BE/FOLLOWED',**({'path':'/ABSOLUTE/FIELD/MUST/NEVER/BE/FOLLOWED'} if path_key!='path' else {})})
            portable.append({'path':child.relative_to(audit).as_posix(),**data,'role':'authored_evidence'})
        save(path,{entries_key:entries,'ignored_source_and_scratch_inventory':[{'path':'/not/retained/source.pdf','bytes':100,'sha256':'0'*64}]})
        registry.append({'path':raw,'base':path.parent.relative_to(audit).as_posix(),'entries_key':entries_key,'path_key':path_key,'size_key':size_key,'sha256':sha(path),'role':'priority' if raw.startswith('priority/') else 'math'})
        portable.append({'path':raw,**binding(path),'role':'authored_evidence'})
    save(audit/'RAW_SOURCE_INVENTORY.json',{'files':[{'path':'omitted.pdf','bytes':100,'sha256':'0'*64}],'read_not_retained':True})
    portable.append({'path':'RAW_SOURCE_INVENTORY.json',**binding(audit/'RAW_SOURCE_INVENTORY.json'),'role':'source_receipt'})
    metadata={'title':'SYNTHETIC OFFLINE FIXTURE ONLY','upload_type':'publication','publication_type':'preprint','description':'Synthetic A & B fixture; no real paper or clearance.','creators':[{'name':'Fixture author','affiliation':None}],'access_right':'open','license':'cc-by-4.0','version':'1.0','publication_date':'2026-10-17','keywords':['synthetic fixture'],'related_identifiers':[{'identifier':'https://github.com/AlecKriebel/Math/pull/1283','relation':'isDerivedFrom','scheme':'url'}]}
    context={'edition_mode':source_mode,'source_bindings':source_bindings,'schema':'math-pr1283-current-context-v1','pr':v.PR,'problem_id':v.PROBLEM,'original_head':v.ORIGINAL,'original_branch':v.BRANCH,'original_body_sha256':v.BODY,'title':metadata['title'],'expected_pdf_pages':3,'source_date_epoch':'1792195200','edition_text':{},'structured_records':{},'disclosures':{'firstness_claim':False,'current_openness_claim':False,'ai_assisted':True,'unrefereed':True},'metadata':metadata,'publication_text':{'summary':'Synthetic summary.','priority_statement':'Synthetic priority statement; no real adjudication.','verification_scope':'Synthetic finite controls only.'},'tracker':{'original_problem':'Synthetic fixture (30005434)','notes':'Synthetic notes.'},'authored_freezes':registry,'portable_files':portable,'diagnostic_replays':[{'program':'reviews/source_question_family/checker.py','mode':'normal','result':'reviews/source_question_family/result.json','output_mode':'file','scope':'Synthetic explicit-check fixture only.','layout':'isolated','arguments':[],'comparison':'bytes_exact'},{'program':'reviews/analytic_adversary/checker.py','mode':'normal_O_OO','result':'reviews/analytic_adversary/result.json','output_mode':'file','scope':'Synthetic original-layout replay fixture only.','layout':'original_submission','arguments':['--output','{output}'],'comparison':'json_ignore_runtime'}],'gate_bindings':{'math_gate_sha256':sha(audit/'MATH_GATE.json'),'priority_adjudication_sha256':sha(audit/'PRIORITY_ADJUDICATION.json'),'submitted_snapshot_sha256':sha(audit/'SUBMITTED_SNAPSHOT.json')},'document_bindings':{key:'0'*64 for key in ['source_sha256','pdf_sha256','compile_receipt_sha256','layout_receipt_sha256']}}
    save(audit/'CURRENT_PR1283_CONTEXT.json',context);(pub/'manuscript').mkdir();(pub/'manuscript/main.tex').write_text('SYNTHETIC TEX FIXTURE ONLY\n')
    bin_dir=folder/'bin';bin_dir.mkdir();compiler=bin_dir/'tectonic'
    compiler.write_text('#!'+sys.executable+"\nimport pathlib,sys\nif '--version' in sys.argv:print('synthetic compiler only');raise SystemExit\no=pathlib.Path(sys.argv[sys.argv.index('--outdir')+1]);o.mkdir(parents=True,exist_ok=True);(o/'main.pdf').write_bytes(b'SYNTHETIC PDF BYTES ONLY')\n");compiler.chmod(0o755)
    info=bin_dir/'pdfinfo';info.write_text('#!'+sys.executable+"\nprint('Pages: 3')\n");info.chmod(0o755)
    env=dict(os.environ,PATH=str(bin_dir)+os.pathsep+os.environ['PATH'],PYTHONDONTWRITEBYTECODE='1')
    compilation_context=copy.deepcopy(context);compilation_context.pop('document_bindings');save(audit/'CURRENT_PR1283_CONTEXT.json',compilation_context)
    run=subprocess.run([sys.executable,'-B',str(pub/'compile_note.py')],env=env,capture_output=True,text=True);need(run.returncode==0,run.stderr)
    compiled=json.loads((pub/'COMPILE_RECEIPT.json').read_text());need(compiled['source_date_epoch']==context['source_date_epoch'] and compiled['at_utc']!='2026-10-17T20:00:00Z','actual time confused with build stamp')
    save(pub/'LAYOUT_VERIFICATION.json',{'status':'pass','at_utc':'2026-10-17T21:00:00Z','source_sha256':sha(pub/'manuscript/main.tex'),'pdf_sha256':sha(pub/'output/pdf/main.pdf'),'all_pages_visually_inspected':True,'pages':3,'page_indices_inspected':[1,2,3],'synthetic_fixture_only':True})
    context['document_bindings']={'source_sha256':sha(pub/'manuscript/main.tex'),'pdf_sha256':sha(pub/'output/pdf/main.pdf'),'compile_receipt_sha256':sha(pub/'COMPILE_RECEIPT.json'),'layout_receipt_sha256':sha(pub/'LAYOUT_VERIFICATION.json')};save(audit/'CURRENT_PR1283_CONTEXT.json',context)
    run=subprocess.run([sys.executable,'-B',str(pub/'build_package.py')],env=env,capture_output=True,text=True);need(run.returncode==0,run.stderr)
    build=json.loads((pub/'BUILD_RECEIPT.json').read_text());save(pub/'zenodo-deposit.json',{'metadata':metadata,'files':[{'path':build[key]['path']} for key in ['pdf','verification_zip']]})
    # An actual release must obtain different fresh reviewers. These fabricated
    # records are fixture data in ignored scratch and confer no approval.
    u=load(pub/'update_pr_publication.py');required=[pub/name for name in NAMES]+[pub/name for name in [build['pdf']['path'],build['verification_zip']['path'],'zenodo-deposit.json','manuscript/main.tex','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json','BUILD_RECEIPT.json']]+[audit/name for name in ['CURRENT_PR1283_CONTEXT.json','MATH_GATE.json','PRIORITY_ADJUDICATION.json','SUBMITTED_SNAPSHOT.json']]
    required+=([audit/'CURRENT_EDITION_CORRECTION.json'] if source_mode=='documented_correction' else [])+[u.SHARED_KIT,coordinator,postmerge,ready]+[audit/part/name for part in ['submitted','current_edition'] for name in v.NAMES]+[audit/e['path'] for e in context['portable_files']]+[p for p in (pub/'verification').rglob('*') if p.is_file()];records=[]
    for i in [1,2]:
        review=audit/'reviews'/('synthetic_final_'+str(i));review.mkdir();(review/'REPORT.md').write_text('SYNTHETIC REVIEW FIXTURE ONLY; NOT AN ACTUAL REVIEW\n')
        save(review/'INPUT_FREEZE.json',{'synthetic_fixture_only':True,'files':[{'path':str(path),**binding(path)} for path in dict.fromkeys(required)],'external_readonly_inputs':[]})
        save(review/'VERDICT.json',{'schema':'math-pr1283-whole-package-review-v1','status':'CLEAN','actual_review':True,'fresh_reviewer':True,'synthetic_fixture_only':True,'reviewer_id':'fixture-'+str(i),'pr':1283,'problem_id':30005434,'original_head':v.ORIGINAL,'current_context_sha256':sha(audit/'CURRENT_PR1283_CONTEXT.json'),'input_freeze_sha256':sha(review/'INPUT_FREEZE.json'),'at_utc':'2026-10-17T21:00:0'+str(i)+'Z'})
        save(review/'MANIFEST.json',{'authored_files':[{'path':name,**binding(review/name)} for name in ['REPORT.md','VERDICT.json']]})
        records.append({'status':'CLEAN','actual_review':True,'fresh_reviewer':True,'reviewer_id':'fixture-'+str(i),'context_sha256':sha(audit/'CURRENT_PR1283_CONTEXT.json'),'manifest_schema':{'entries_key':'authored_files','path_key':'path','size_key':'bytes'},**{key:('../reviews/'+review.name+'/'+filename) for key,filename in [('report','REPORT.md'),('verdict','VERDICT.json'),('manifest','MANIFEST.json'),('input_freeze','INPUT_FREEZE.json')]},**{key+'_sha256':sha(review/filename) for key,filename in [('report','REPORT.md'),('verdict','VERDICT.json'),('manifest','MANIFEST.json'),('input_freeze','INPUT_FREEZE.json')]}})
        required += [review/name for name in ['REPORT.md','VERDICT.json','MANIFEST.json','INPUT_FREEZE.json']]
    gate={'schema':'math-preprint-final-review-gate-v1','pr':1283,'problem_id':30005434,'original_head':v.ORIGINAL,'status':'pass','workflow':{name:sha(pub/name) for name in NAMES},'deposit_coordinator_sha256':sha(coordinator),'postmerge_coordinator_sha256':sha(postmerge),'pdf_sha256':sha(pub/build['pdf']['path']),'verification_zip_sha256':sha(pub/build['verification_zip']['path']),'metadata_sha256':sha(pub/'zenodo-deposit.json'),'source_sha256':sha(pub/'manuscript/main.tex'),'current_context_sha256':sha(audit/'CURRENT_PR1283_CONTEXT.json'),'reviews':records,'latest_review':records[-1],'synthetic_fixture_only':True}
    gate['shared_kit_sha256']=sha(u.SHARED_KIT);save(pub/'FINAL_REVIEW_GATE.json',gate);u.validate_workflow_gate(gate)
    return {'audit':audit,'pub':pub,'v':v,'context':context,'snapshot':snapshot,'build':build,'gate':gate,'env':env}

def source_schema_controls(folder):
    v=load(ROOT/DEPLOY['verification/verify.py']);actual=Path('/Users/alec/Documents/Math/draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1283_30005434');target=folder/'submitted';shutil.copytree(actual/'submitted',target)
    snapshot=json.loads((actual/'SUBMITTED_SNAPSHOT.json').read_text());v.authenticate_snapshot(target,snapshot);mp=target/'MANIFEST.json';original=mp.read_bytes();rejected=[]
    for name in sorted(v.NAMES):
        path=target/name;old=path.read_bytes();path.write_bytes(old+b'UNDECLARED CORRUPTION');rejected.append(reject(lambda:v.authenticate_snapshot(target,snapshot),'original_member_'+name));path.write_bytes(old)
    mutations=[('dictionary_not_list',lambda x:x.update(files={e['file']:e for e in x['files']})),('duplicate_member',lambda x:x['files'].__setitem__(1,copy.deepcopy(x['files'][0]))),('missing_member',lambda x:x['files'].pop()),('self_member',lambda x:x['files'][0].update(file='MANIFEST.json')),('absolute_member',lambda x:x['files'][0].update(file='/tmp/arbitrary')),('nested_inventory_not_membership',lambda x:x.update(files={'inventories':[{'path':'PROOF_CLASSIFICATION.md'}]})),('undeclared_path_key',lambda x:x['files'][0].update(path='PROOF_CLASSIFICATION.md')),('wrong_covered_bytes',lambda x:x.update(covered_bytes=x['covered_bytes']+1)),('wrong_covered_count',lambda x:x.update(covered_file_count=8)),('boolean_covered_count',lambda x:x.update(covered_file_count=True)),('wrong_schema',lambda x:x.update(schema_version=2)),('boolean_schema',lambda x:x.update(schema_version=True)),('wrong_problem',lambda x:x.update(problem_id='30005434')),('duplicate_allowlist',lambda x:x['allowlist'].__setitem__(1,x['allowlist'][0])),('historical_member_not_present',lambda x:x['files'][0].update(file='EARLIER_PROOF.md'))]
    for label,change in mutations:
        obj=json.loads(original);change(obj);save(mp,obj);rejected.append(reject(lambda:v.authenticate_edition(target),label));mp.write_bytes(original)
    rejected.append(reject(lambda:v.fixture_boundary(actual,{'synthetic_fixture_only':True}),'fixture_record_on_actual_audit'))
    v.fixture_boundary(folder,{'synthetic_fixture_only':True})
    return {'actual_original8_bytes':sum(e['bytes'] for e in snapshot['files']),'seven_list_members_and_totals_verified':True,'historical_inventory_never_guessed':True,'all8_original_corruptions_rejected':True,'negative_controls':rejected}

def context_and_portable_controls(f):
    audit=f['audit'];pub=f['pub'];v=f['v'];context=f['context'];cp=audit/'CURRENT_PR1283_CONTEXT.json';rejected=[]
    for label,change in [('wrong_pr',lambda x:x.update(pr=1)),('wrong_head',lambda x:x.update(original_head='0'*40)),('wrong_original_body',lambda x:x.update(original_body_sha256='0'*64)),('wrong_original_branch',lambda x:x.update(original_branch='other')),('wrong_title',lambda x:x.update(title='wrong')),('fixed_bad_pages',lambda x:x.update(expected_pdf_pages=0)),('injected_prose',lambda x:x['edition_text'].update({'PROOF_CLASSIFICATION.md':'injected'})),('extra_prose',lambda x:x['edition_text'].update({'UNEXPECTED.md':'stale'})),('injected_structured',lambda x:x['structured_records'].update({'INJECTED_RECORD.json':{'injected':True}})),('firstness',lambda x:x['disclosures'].update(firstness_claim=True)),('missing_size_key',lambda x:x['authored_freezes'][0].pop('size_key')),('absolute_selected_path',lambda x:x['authored_freezes'][0].update(path_key='path')),('escaped_base',lambda x:x['authored_freezes'][0].update(base='../outside')),('schema_guessing',lambda x:x['authored_freezes'][0].update(entries_key='entries')),('wrong_freeze_anchor',lambda x:x['authored_freezes'][0].update(sha256='0'*64)),('missing_priority_freeze',lambda x:x['authored_freezes'].pop()),('omitted_frozen_member',lambda x:x['portable_files'].pop(0)),('wrong_document_anchor',lambda x:x['document_bindings'].update(pdf_sha256='0'*64)),('extra_metadata',lambda x:x['metadata'].update(extra='wrong')),('nonascii_metadata_punctuation',lambda x:x['metadata'].update(description='curly apostrophe \u2019'))]:
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
    portable_context=root/'provenance/CURRENT_PR1283_CONTEXT.json';old_context=portable_context.read_bytes();obj=json.loads(old_context);obj['authored_freezes'][0]['base']='priority/fixture';save(portable_context,obj)
    rejected.append(reject(run,'outside_context_anchor_coupled_registry_rewrite'));portable_context.write_bytes(old_context)
    for unsafe in ['../escape','/absolute','a/../b','a//b','a\\b','.', 'a/./b']:rejected.append(reject(lambda raw=unsafe:v.safe(raw),'unsafe_'+unsafe))
    for flags in [[],['-O'],['-OO']]:
        args=[arg for key,val in anchors.items() for arg in ['--expected-'+key+'-sha256',val]]
        result=subprocess.run([sys.executable,'-B',*flags,str(root/'verify.py'),*args],capture_output=True,text=True,env=f['env']);need(result.returncode==0,result.stderr)
    return {'rejected':rejected,'all_three_verifier_modes':True,'original8_current8':True,'documented_current_changes_allowed':True,'historical_acceptance_md_not_reinterpreted':True,'actual_custom_schema_ignores_absolute_path':True,'receipt_inventory_not_treated_as_retained_source_manifest':True,'synthetic_pdf_pages':3}

def correction_controls(f):
    v=f['v'];a=f['audit'];p=f['pub'];context=f['context'];cp=a/'CURRENT_PR1283_CONTEXT.json';rp=a/'CURRENT_EDITION_CORRECTION.json';rejected=[]
    v.load_context(a,p);need((a/'current_edition/PROOF_CLASSIFICATION.md').read_bytes()!=(a/'submitted/PROOF_CLASSIFICATION.md').read_bytes(),'documented correction fixture must differ')
    for label,mutate in [('wrong_snapshot_anchor',lambda c:c['source_bindings'].update(submitted_snapshot_sha256='0'*64)),('wrong_correction_anchor',lambda c:c['source_bindings'].update(current_edition_correction_sha256='0'*64)),('wrong_current_binding',lambda c:c['source_bindings']['current_edition']['PROOF_CLASSIFICATION.md'].update(sha256='0'*64)),('missing_current_binding',lambda c:c['source_bindings']['current_edition'].pop('README.md')),('preserve_mode_changed_bytes',lambda c:c.update(edition_mode='preserve_submitted'))]:
        bad=copy.deepcopy(context);mutate(bad);save(cp,bad);rejected.append(reject(lambda:v.load_context(a,p),label));save(cp,context)
    original=rp.read_bytes()
    for label,mutate in [('undeclared_change',lambda r:r['changes'].pop()),('wrong_before_sha',lambda r:r['changes'][0].update(original_sha256='0'*64)),('wrong_after_sha',lambda r:r['changes'][0].update(current_sha256='0'*64)),('empty_reason',lambda r:r['changes'][0].update(reason='')),('duplicate_change',lambda r:r['changes'].append(copy.deepcopy(r['changes'][0]))),('wrong_current_map',lambda r:r['current_files']['PROOF_CLASSIFICATION.md'].update(sha256='0'*64)),('wrong_original_map',lambda r:r['original_files']['PROOF_CLASSIFICATION.md'].update(sha256='0'*64)),('wrong_correction_target',lambda r:r.update(pr=1))]:
        bad=json.loads(original);mutate(bad);save(rp,bad);ctx=copy.deepcopy(context);ctx['source_bindings']['current_edition_correction_sha256']=sha(rp);save(cp,ctx);rejected.append(reject(lambda:v.load_context(a,p),label));rp.write_bytes(original);save(cp,context)
    for raw in ['current_edition/PROOF_CLASSIFICATION.md','current_edition/MANIFEST.json','submitted/PROOF_CLASSIFICATION.md','SUBMITTED_SNAPSHOT.json']:
        path=a/raw;old=path.read_bytes();path.write_bytes(old+b'UNDECLARED TAMPERING');rejected.append(reject(lambda:v.load_context(a,p),'tampered_'+raw));path.write_bytes(old)
    return {'explicit_corrected_proof_and_updated_list_manifest_accepted':True,'original_submission_stays_exact':True,'only_exact_declared_relative_source_bindings_followed':True,'negative_controls':rejected}

def review_controls(f):
    pub=f['pub'];u=load(pub/'update_pr_publication.py');gate=f['gate'];rejected=[]
    for label,change in [('empty_workflow',lambda x:x.update(workflow={})),('missing_eighth_script',lambda x:x['workflow'].pop('workflow_regression.py')),('wrong_script_hash',lambda x:x['workflow'].update({'append_tracker.py':'0'*64})),('extra_equivalent_path',lambda x:x['workflow'].update({'./append_tracker.py':'0'*64})),('wrong_coordinator',lambda x:x.update(deposit_coordinator_sha256='0'*64)),('wrong_postmerge',lambda x:x.update(postmerge_coordinator_sha256='0'*64)),('wrong_shared_kit',lambda x:x.update(shared_kit_sha256='0'*64)),('wrong_pdf',lambda x:x.update(pdf_sha256='0'*64)),('one_review',lambda x:x.update(reviews=x['reviews'][:1])),('nonactual_review',lambda x:x['reviews'][0].update(actual_review=False)),('not_fresh_reviewer',lambda x:x['reviews'][0].update(fresh_reviewer=False)),('wrong_verdict_hash',lambda x:x['reviews'][0].update(verdict_sha256='0'*64)),('outside_report',lambda x:x['reviews'][0].update(report='../SUBMITTED_SNAPSHOT.json')),('stale_latest',lambda x:x.update(latest_review=x['reviews'][0]))]:
        bad=copy.deepcopy(gate);change(bad);rejected.append(reject(lambda:u.validate_workflow_gate(bad),label))
    verdict=f['audit']/'reviews/synthetic_final_2/VERDICT.json';old=verdict.read_bytes();obj=json.loads(old);obj['status']='FAIL';save(verdict,obj);bad=copy.deepcopy(gate);bad['reviews'][1]['verdict_sha256']=sha(verdict);bad['latest_review']=bad['reviews'][1]
    rejected.append(reject(lambda:u.validate_workflow_gate(bad),'actual_file_nonclean_despite_clean_gate'));verdict.write_bytes(old)
    return rejected

def document_controls(f):
    pub=f['pub'];cp=f['audit']/'CURRENT_PR1283_CONTEXT.json';b=load(pub/'build_package.py');os.environ['PATH']=f['env']['PATH'];b.document_bindings();rejected=[]
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
    for n,(ek,pk,sk) in enumerate([('files','relative_path','bytes'),('authored_files','relative_path','bytes'),('entries','relative_path','bytes'),('members','relative_path','bytes'),('members','path','bytes')]):
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
    relative=next(item for item in registry if (item['entries_key'],item['path_key'],item['size_key'])==('members','relative_path','bytes'));path=folder/relative['path'];original=path.read_bytes()
    for label,value in [('members_relative_absolute','/ABSOLUTE'),('members_relative_traversal','../escape')]:
        obj=json.loads(original);obj['members'][0]['relative_path']=value;save(path,obj);changed=copy.deepcopy(relative);changed['sha256']=sha(path);rejected.append(reject(lambda:v.authenticate_nested_manifests(folder,[changed],require_complete=False),label));path.write_bytes(original)
    obj=json.loads(original);obj['members'].append(copy.deepcopy(obj['members'][0]));save(path,obj);changed=copy.deepcopy(relative);changed['sha256']=sha(path);rejected.append(reject(lambda:v.authenticate_nested_manifests(folder,[changed],require_complete=False),'members_relative_duplicate'));path.write_bytes(original)
    program=folder/'root_exact_fixture.py';program.write_text("from pathlib import Path\nimport datetime,hashlib,json\np=Path(__file__);print(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'program_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'result':{'static':7,'at_utc':'NESTED_MUST_REMAIN'}}))\n")
    expected={'at_utc':'HISTORICAL TOP LEVEL ONLY','program_sha256':sha(program),'result':{'static':7,'at_utc':'NESTED_MUST_REMAIN'}};save(folder/'expected.json',expected);ctx={'diagnostic_replays':[{'program':program.name,'mode':'normal_O_OO','result':'expected.json','output_mode':'stdout','scope':'Synthetic root deterministic replay contract only.','layout':'isolated','arguments':[],'comparison':'json_ignore_at_utc'}]};v.replay_diagnostics(folder,ctx)
    bad=copy.deepcopy(expected);bad['result']['at_utc']='CORRUPTED';save(folder/'expected.json',bad);rejected.append(reject(lambda:v.replay_diagnostics(folder,ctx),'nested_time_not_ignored'))
    return {'explicit_relative_schemas_relocate':True,'explicit_members_path_bytes_relocates':True,'explicit_members_relative_path_bytes_relocates':True,'members_input_path_never_inferred':True,'unused_absolute_inputs_never_followed_as_membership':True,'no_absolute_membership_mode':True,'only_top_level_runtime_omissions':True,'negative_controls':rejected}

def historical_review_controls(f):
    pub=f['pub'];audit=f['audit'];u=load(pub/'update_pr_publication.py');gate=copy.deepcopy(f['gate']);first=gate['reviews'][0];latest=gate['reviews'][-1]
    def refresh(record):
        review=(pub/record['verdict']).parent;record['input_freeze_sha256']=sha(review/'INPUT_FREEZE.json');verdict=json.loads((review/'VERDICT.json').read_text());verdict.update(status=record['status'],current_context_sha256=record['context_sha256'],input_freeze_sha256=record['input_freeze_sha256']);save(review/'VERDICT.json',verdict);record['verdict_sha256']=sha(review/'VERDICT.json');manifest=json.loads((review/'MANIFEST.json').read_text())
        for entry in manifest['authored_files']:entry.update(binding(review/entry['path']))
        save(review/'MANIFEST.json',manifest);record['manifest_sha256']=sha(review/'MANIFEST.json')
    first['status']='CHANGES_REQUIRED';first['context_sha256']='1'*64;review=(pub/first['input_freeze']).parent;freeze=json.loads((review/'INPUT_FREEZE.json').read_text())
    for entry in freeze['files']:
        if entry['path']==str(audit/'CURRENT_PR1283_CONTEXT.json'):entry['sha256']='1'*64
        if entry['path']==str(audit/'current_edition/PROOF_CLASSIFICATION.md'):entry['sha256']='2'*64;entry['bytes']=1
    save(review/'INPUT_FREEZE.json',freeze);refresh(first)
    resolution=audit/'ROOT_R1_RESOLUTION.json';resolved={'schema':'math-pr1283-review-resolution-v1','status':'RESOLVED','pr':1283,'problem_id':30005434,'original_head':u.ORIGINAL,'reviewer_id':first['reviewer_id'],'review_verdict_sha256':first['verdict_sha256'],'review_input_freeze_sha256':first['input_freeze_sha256'],'review_context_sha256':first['context_sha256'],'resolved_context_sha256':gate['current_context_sha256'],'at_utc':'2026-10-17T21:00:01.500000Z','items':[{'finding':'Synthetic first-review correction.','resolution':'Synthetic repair in current context.','evidence':'Synthetic current proof bytes, not actual mathematical approval.'}]};save(resolution,resolved);first['resolution']='../ROOT_R1_RESOLUTION.json';first['resolution_sha256']=sha(resolution)
    later=(pub/latest['input_freeze']).parent;current=json.loads((later/'INPUT_FREEZE.json').read_text())
    for entry in current['files']:entry.update(binding(Path(entry['path'])))
    current['files'].append({'path':str(resolution),**binding(resolution)});save(later/'INPUT_FREEZE.json',current);refresh(latest);gate['latest_review']=latest;u.validate_workflow_gate(gate)
    save(pub/'FINAL_REVIEW_GATE.json',gate);os.environ['PATH']=f['env']['PATH'];operative=load(pub.parents[2]/'publication_coordinators/pr1283.py');need(operative.P.resolve()==pub.resolve(),'operative coordinator layout differs');need(operative.authenticate_release()==gate,'actual release preflight rejected repaired historical review sequence')
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
    pub=f['pub'];c=load(pub.parents[2]/'publication_coordinators/pr1283.py');kit=c.load_exact_kit();kit.STATE_DIR=pub/'synthetic-kit-state';kit.doi_status=lambda doi:{'status':'not_checked_fixture'}
    events=[];state={'deposit':None,'mutate_second_get':False,'lost_publish':False,'lose_followup':False,'wrong_id':False}
    class Client:
        def create(self,metadata):events.append('POST create');state['deposit']={'id':123,'submitted':False,'metadata':copy.deepcopy(metadata),'files':[],'links':{'bucket':'fixture://bucket'}};return copy.deepcopy(state['deposit'])
        def get(self,number):
            events.append('GET '+str(number));need(number==123,'wrong requested ID')
            if state['lose_followup']:state['lose_followup']=False;raise kit.DepositError('synthetic lost follow-up GET')
            out=copy.deepcopy(state['deposit'])
            if state['wrong_id']:out['id']=124;state['wrong_id']=False
            if state['mutate_second_get']:
                field=state['mutate_second_get'];state['mutate_second_get']=False
                if field is True:out['metadata']['description']=out['metadata']['description'].replace('&','&amp;')
                else:out['metadata'][field]=None
            return out
        def upload(self,bucket,entry):
            events.append('PUT file');state['deposit']['files'].append({'filename':entry['name'],'filesize':entry['size'],'checksum':'md5:'+entry['md5']})
            if case=='uncertain_stage_known_id_recovery' and len(state['deposit']['files'])==2:raise kit.DepositError('synthetic successful final upload response lost')
        def update(self,number,metadata):events.append('PUT metadata');state['deposit']['metadata']=copy.deepcopy(metadata)
        def publish(self,number):
            events.append('POST publish');state['deposit']['submitted']=True;state['deposit']['doi']='10.5281/zenodo.123'
            if state['lost_publish']:state['lose_followup']=True;raise kit.DepositError('synthetic lost POST response')
    client=Client();c.live_preflight=lambda:events.append('mock live original PR/tracker preflight')
    def actual_call(loaded,command,known_id=None,check_doi=False):
        need(loaded is kit,'actual exact kit object changed')
        if command=='publish' and case=='wrong_id_second_fresh_inspection':state['wrong_id']=True
        if command=='publish' and case=='normalization_between_inspect_and_POST':state['mutate_second_get']=True
        if command=='publish' and case.startswith('server_field_'):state['mutate_second_get']=case.removeprefix('server_field_')
        return kit.run(types.SimpleNamespace(command=command,manifest=pub/'zenodo-deposit.json',sandbox=False,confirm_id=known_id,check_doi=check_doi),client=client)
    c.call_kit=actual_call
    if case=='uncertain_stage_known_id_recovery':
        reject(lambda:c.execute('stage',kit),'uncertain_stage_response',errors=(kit.DepositError,RuntimeError));reject(lambda:c.execute('stage',kit),'uncertain_stage_no_blind_retry');before=len(events);recovered=c.execute('inspect',kit);need(events[before:]==['GET 123'] and recovered['id']==123 and recovered['state']=='ready_to_publish','stage recovery was not same-ID read-only');need(events.count('POST create')==1 and 'POST publish' not in events,'stage recovery repeated creation or published');return {'case':case,'events':events,'actual_shared_kit_run_used':True,'all_network_methods_mocked':True}
    c.execute('stage',kit);reject(lambda:c.execute('stage',kit),'second_stage_intent')
    if case=='wrong_id_first_fresh_inspection':
        state['wrong_id']=True;reject(lambda:c.execute('publish',kit),'first_fresh_inspection_same_id',errors=(kit.DepositError,RuntimeError,ValueError));need('POST publish' not in events,'wrong first inspection ID reached publish POST');need(not (pub/'PUBLISH_INTENT.json').exists(),'first failed inspection wrote publish intent')
    elif case in {'normalization_between_inspect_and_POST','wrong_id_second_fresh_inspection'} or case.startswith('server_field_'):
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
    corrupted_downloads=set()
    def fetch(url,limit):
        if url in corrupted_downloads:return b'SYNTHETIC CORRUPT PUBLIC DOWNLOAD'
        data=json.dumps(public).encode() if url=='https://zenodo.org/api/records/123' else (pub/url.rsplit('/',1)[-1]).read_bytes();need(len(data)<=limit,'fixture response limit');return data
    m.fetch=fetch;capture(m.main);public_negatives=[];original_files=copy.deepcopy(public['files'])
    for label,files in [('missing_artifact',original_files[:1]),('duplicate_artifact',[original_files[0],original_files[0]]),('extra_artifact',original_files+[{'key':'unexpected','links':{'self':'https://fixture.invalid/unexpected'}}])]:
        public['files']=files;public_negatives.append(reject(lambda:capture(m.main),label));public['files']=copy.deepcopy(original_files)
    for entry in original_files:
        url=entry['links']['self'];corrupted_downloads.add(url);public_negatives.append(reject(lambda:capture(m.main),'corrupt_'+entry['key']));corrupted_downloads.remove(url)
    return p,receipt,{'canonical_identity_rejections':badpub,'full_row_range_rejections':badrows,'one_append_despite_lost_response':True,'all11_public_fields':sorted(metadata),'each_field_corruption_rejected':sorted(badmeta),'full_public_check_main_mocked':True,'public_download_main_negative_controls':public_negatives}

def update_controls(f,pubrecord,tracker):
    pub=f['pub'];u=load(pub/'update_pr_publication.py');files,publication,note=u.desired_files(f['build'],pubrecord,tracker,f['snapshot']);need(len(files)==13 and len(publication)==5,'wrong intended8+5 scope')
    body=note+'\nThe current eight-file MANIFEST.json binds the seven other current edition records through its explicit files list of file/bytes/sha256. The current source mode and immutable submitted snapshot are separately authenticated; historical acceptance and byte-preservation declarations do not certify current review or missing earlier inputs. publication_20261017/ adds the reviewed preprint, portable verification archive, matching deposit metadata, publication receipt and README. Original historical files are preserved in the portable archive.\n'
    wanted=u.expected_identity(pubrecord,tracker,files,body);commit='a'*40;calls=[];mode={'bad':None};state={'headRefOid':commit,'headRefName':u.BRANCH,'baseRefName':'main','state':'OPEN','isDraft':True,'body':body}
    def git(*args,data=None):
        calls.append(args)
        if args==('branch','--show-current'):return b'main\n'
        if args[0]=='rev-list':return (commit+' '+('b'*40 if mode['bad']=='parent' else u.ORIGINAL)+'\n').encode()
        if args[0]=='diff-tree':return ('\n'.join(sorted(files)+(['foreign/path'] if mode['bad']=='paths' else []))+'\n').encode()
        if args[0]=='show':return b'wrong' if mode['bad']=='bytes' else files[args[1].split(':',1)[1]]
        if args[0]=='ls-remote':return ((u.ORIGINAL if mode.get('remote_original') else commit)+' refs/heads/'+u.BRANCH+'\n').encode()
        raise RuntimeError('Forbidden unmocked/new Git operation '+repr(args))
    u.git=git;actual_pr=u.pr;query_calls=[]
    def query(args,**kwargs):query_calls.append(args);return json.dumps(state)
    u.subprocess=types.SimpleNamespace(check_output=query)
    need(actual_pr()['baseRefName']=='main','central PR query rejected main')
    base_rejections=[]
    for base in ['other',None]:
        if base is None:state.pop('baseRefName')
        else:state['baseRefName']=base
        base_rejections.append(reject(actual_pr,'central_base_'+str(base)))
    state['baseRefName']='main';need(all('baseRefName' in args[args.index('--json')+1].split(',') for args in query_calls),'central live query omitted baseRefName')
    u.pr=lambda:copy.deepcopy(state);intent={**wanted,'commit':commit};u.validate_saved(intent,wanted,files);badkeys=[]
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
    # Direct pr stubs deliberately bypass the central guard: every phase must
    # independently reject a changed or absent base before accepting its state.
    saved_receipt=(pub/'PR_BRANCH_RECEIPT.json').read_bytes()
    for base in ['other',None]:
        if base is None:state.pop('baseRefName')
        else:state['baseRefName']=base
        base_rejections.append(reject(lambda:capture(u.main),'branch_initial_base_'+str(base)))
        base_rejections.append(reject(lambda:u.synchronize_pr_body(commit,body,'0'*64),'body_before_base_'+str(base)))
        need((pub/'PR_BRANCH_RECEIPT.json').read_bytes()==saved_receipt,'wrong base changed completed receipt')
    state['baseRefName']='main'
    for base in ['other',None]:
        reads=[]
        def changed_base():
            out=copy.deepcopy(state)
            if reads:
                if base is None:out.pop('baseRefName')
                else:out['baseRefName']=base
            reads.append(True);return out
        u.pr=changed_base;base_rejections.append(reject(lambda:u.synchronize_pr_body(commit,body,'0'*64),'body_after_base_'+str(base)))
        need(len(reads)==2,'body post-readback base control did not reach second query')
    (pub/'PR_BRANCH_RECEIPT.json').unlink();state['headRefOid']=u.ORIGINAL;mode['remote_original']=True
    for base in ['other',None]:
        reads=[]
        u.pr=changed_base;base_rejections.append(reject(lambda:capture(u.main),'branch_prepush_base_'+str(base)))
        need(len(reads)==1 and not (pub/'PR_BRANCH_RECEIPT.json').exists(),'resumed uncertain branch intent did not stop read-only before a repush')
    mode['remote_original']=False;state['headRefOid']=commit;state['baseRefName']='main';u.pr=lambda:copy.deepcopy(state);(pub/'PR_BRANCH_RECEIPT.json').write_bytes(saved_receipt)
    need(all(args[0] in {'branch','rev-list','diff-tree','show','ls-remote'} for args in calls),'recovery/base rejection made Git mutation')
    (pub/'PR_BRANCH_RECEIPT.json').unlink();state['headRefOid']=u.ORIGINAL;mode['remote_original']=False
    reject(lambda:capture(u.main),'api_head_lag_after_known_remote_push');need(not (pub/'PR_BRANCH_RECEIPT.json').exists(),'Lagging PR API recorded a completed body receipt')
    state['headRefOid']=commit;(pub/'PR_BRANCH_RECEIPT.json').write_bytes(saved_receipt)
    race=pub/'SYNTHETIC_EXCLUSIVE_INTENT.json';u.exclusive_intent(race,{'fixture':True});reject(lambda:u.exclusive_intent(race,{'fixture':False}),'exclusive_branch_body_intent_race');race.unlink()
    bodycalls=[];state['body']='synthetic original body';original=hashlib.sha256(state['body'].encode()).hexdigest();(pub/'PR_BODY_FINAL.md').write_text(body)
    def edit(args,**kwargs):bodycalls.append(args);state['body']=body;return types.SimpleNamespace(returncode=1,stderr='synthetic lost edit response')
    u.subprocess=types.SimpleNamespace(run=edit);reject(lambda:u.synchronize_pr_body(commit,body,original),'lost_body_response');u.synchronize_pr_body(commit,body,original);need(len(bodycalls)==1,'lost body response repeated already accepted edit')
    state['body']='synthetic original body';reject(lambda:u.synchronize_pr_body(commit,body,original),'unconfirmed_prior_body_intent_no_retry');need(len(bodycalls)==1,'unconfirmed body intent retried edit')
    state['body']='unknown outside edit';reject(lambda:u.synchronize_pr_body(commit,body,original),'outside_body_change')
    return {'desired_files':len(files),'current_edition':8,'publication_additions':5,'stale_identity_and_actual_tree_rejected':badkeys,'complete_update_main_saved_intent_recovery_and_completed_readback':True,'body_lost_response_exact_readback_and_outside_change':True,'unconfirmed_body_intent_no_mutating_retry':True,'exclusive_branch_and_body_intents':True,'unconfirmed_branch_intent_no_repush':True,'lagging_api_head_stops_before_body_sync':True,'central_and_explicit_phase_base_rejections':base_rejections,'no_index_or_force_or_git_mutation_in_test':True,'fresh_object_construction_not_executed':'Actual Git object/tree creation and branch push remain a later integration operation.'}

def preimport_controls(f):
    a=f['audit'];p=f['pub'];r=load(a/'_local/ready_and_merge.py');r.load_updater();gate_path=p/'FINAL_REVIEW_GATE.json';gate=json.loads(gate_path.read_text());freeze_path=(p/gate['latest_review']['input_freeze']).resolve();saved={path:path.read_bytes() for path in [gate_path,freeze_path,p/'update_pr_publication.py',a/'_local/ready_and_merge.py']};marker=p/'SYNTHETIC_IMPORT_DRIFT_MARKER';rejected=[]
    def restore():
        for path,data in saved.items():path.write_bytes(data)
        if marker.exists():marker.unlink()
    try:
        updater=p/'update_pr_publication.py';updater.write_bytes(saved[updater]+b"\n(ROOT/'SYNTHETIC_IMPORT_DRIFT_MARKER').write_text('UNREVIEWED IMPORT EXECUTED')\n")
        rejected.append(reject(r.load_updater,'changed_updater_rejected_before_import'));need(not marker.exists(),'Changed updater executed before reviewed hash validation');restore()
        private=a/'_local/ready_and_merge.py';private.write_bytes(saved[private]+b'\n# UNREVIEWED PRIVATE ENTRYPOINT DRIFT\n');rejected.append(reject(r.load_updater,'private_entrypoint_bytes_match_latest_freeze'));restore()
        inventory=json.loads(saved[freeze_path]);inventory['files']=[e for e in inventory.get('files',[]) if Path(e['path']).resolve()!=private.resolve()];inventory['external_readonly_inputs']=[e for e in inventory.get('external_readonly_inputs',[]) if Path(e['path']).resolve()!=private.resolve()];save(freeze_path,inventory);changed=copy.deepcopy(gate);changed['latest_review']['input_freeze_sha256']=sha(freeze_path);save(gate_path,changed);rejected.append(reject(r.load_updater,'private_entrypoint_missing_from_latest_freeze'));restore()
        inventory=json.loads(saved[freeze_path]);inventory['files'][0]['sha256']='0'*64;save(freeze_path,inventory);changed=copy.deepcopy(gate);changed['latest_review']['input_freeze_sha256']=sha(freeze_path);save(gate_path,changed);rejected.append(reject(r.load_updater,'latest_frozen_input_drift_before_import'));restore()
        changed=copy.deepcopy(gate);changed['workflow']['update_pr_publication.py']='0'*64;save(gate_path,changed);rejected.append(reject(r.load_updater,'updater_gate_hash_before_import'));restore()
        r.load_updater()
    finally:restore()
    return {'independent_preimport_byte_authentication':True,'changed_updater_import_marker_never_executed':True,'exact8_helpers_2coordinators_pinned_kit_and_private_ready_required':True,'all_latest_frozen_inputs_checked_without_project_code':True,'negative_controls':rejected}

def ready_controls(f):
    """Real guarded ready main and full operative updater; services/Git mocked."""
    pub=f['pub'];r=load(f['audit']/'_local/ready_and_merge.py');u=load(pub/'update_pr_publication.py').__dict__
    publication=json.loads((pub/'PUBLICATION_RECEIPT.json').read_text());tracker=json.loads((pub/'tracker/TRACKER_RECEIPT.json').read_text())
    files,_,_=u['desired_files'](f['build'],publication,tracker,f['snapshot']);body=(pub/'PR_BODY_FINAL.md').read_text();head='a'*40
    baseline={path:path.read_bytes() for path in f['audit'].rglob('*') if path.is_file()}
    attempts=['READY_REQUEST_INTENT.json','MERGE_REQUEST_INTENT.json','READY_COMMAND_RECEIPT.json','MERGE_COMMAND_RECEIPT.json']
    results=[];mode={};state={};events=[];reads=[]
    def reset():
        for name in attempts:
            path=pub/name
            if path.exists() or path.is_symlink():path.unlink()
        for path,data in baseline.items():
            if path.is_symlink():path.unlink()
            if not path.exists() or path.read_bytes()!=data:path.write_bytes(data)
        state.clear();state.update({'url':r.URL,'state':'OPEN','isDraft':True,'headRefOid':head,'headRefName':r.BRANCH,'baseRefName':'main','body':body,'files':[{'path':name} for name in sorted(files)]})
        mode.clear();events.clear();reads.clear()
        u['main']=actual_main
    def git(*args,data=None):
        reads.append(args)
        if args==('branch','--show-current'):return b'main\n'
        if args[0]=='rev-list':return (head+' '+mode.get('parents',u['ORIGINAL'])+'\n').encode()
        if args[0]=='diff-tree':return ('\n'.join(sorted(files)+mode.get('extra_paths',[]))+'\n').encode()
        if args[0]=='show':
            name=args[1].split(':',1)[1]
            return b'CORRUPT ACTUAL COMMIT BLOB' if mode.get('blob')==name else files[name]
        if args[0]=='ls-remote':return (mode.get('remote',head)+' refs/heads/'+r.BRANCH+'\n').encode()
        raise RuntimeError('Forbidden Git mutation in ready regression '+repr(args))
    def pr():return copy.deepcopy(state)
    u['git']=git;u['pr']=pr
    # Even a missing completed receipt cannot fall through into updater writes.
    def forbidden(*args,**kwargs):raise RuntimeError('No subprocess mutation permitted in ready fixture')
    u['subprocess']=types.SimpleNamespace(run=forbidden,check_output=forbidden)
    actual_main=u['main']
    class Service:
        def live(self):
            if mode.get('live_hook'):mode['live_hook']()
            return copy.deepcopy(state)
        def ready(self):
            events.append(('ready',head));state['isDraft']=False
            if mode.get('after_ready'):mode['after_ready']()
            if mode.get('ready_unknown'):raise TimeoutError('Synthetic accepted ready with lost response')
            return types.SimpleNamespace(returncode=mode.get('ready_return',0),stdout='fixture ready',stderr='')
        def merge(self,expected):
            events.append(('merge',expected));need(expected==head,'merge omitted expected head')
            if not mode.get('merge_unaccepted'):state['state']='MERGED'
            if mode.get('merge_unknown'):raise TimeoutError('Synthetic accepted merge with lost response')
            return types.SimpleNamespace(returncode=mode.get('merge_return',0),stdout='fixture merge',stderr='')
    service=Service()
    def invoke():return r.guarded_main(u,service)
    def mutate_json(name,key,value):
        path=pub/name;obj=json.loads(path.read_text());obj[key]=value;save(path,obj)
    def negative(label,change):
        reset();change();reject(invoke,'ready_'+label);need(not events,'Invalid ready case mutated a service: '+label);results.append(label)
    reset();result=invoke();need(events==[('ready',head),('merge',head)] and result['new_merge_requests']==1,'Valid ready/expected-head merge did not occur exactly once')
    recovered=invoke();need(recovered['status']=='existing_attempt_read_only_reconciliation' and events==[('ready',head),('merge',head)],'Completed attempt retried a mutation')
    positives=['draft_ready_merge_once_and_readonly_reconcile']
    reset();state['isDraft']=False;invoke();need(events==[('merge',head)],'Already-ready positive changed draft again');positives.append('already_ready_merge_once')
    for name in ['PR_BRANCH_RECEIPT.json','PR_BRANCH_INTENT.json','PR_BODY_FINAL.md']:
        negative('missing_'+name,lambda name=name:(pub/name).unlink())
        def symlink(name=name):
            path=pub/name;path.unlink();path.symlink_to(pub/'BUILD_RECEIPT.json')
        negative('symlink_'+name,symlink)
    negative('forged_minimal_receipt',lambda:save(pub/'PR_BRANCH_RECEIPT.json',{'commit':head,'branch':r.BRANCH,'paths':sorted(files),'body_readback_verified':True,'remote_readback_verified':True,'operation_stage':'reviewed_branch_and_final_body_verified'}))
    for name in ['PR_BRANCH_RECEIPT.json','PR_BRANCH_INTENT.json']:
        wanted=json.loads(baseline[pub/name])
        for key in u['expected_identity'](publication,tracker,files,body):
            def bad(name=name,key=key,wanted=wanted):
                value=copy.deepcopy(wanted[key])
                if isinstance(value,dict):value={}
                elif isinstance(value,list):value=[]
                elif isinstance(value,bool):value=not value
                elif isinstance(value,int):value+=1
                else:value='CORRUPT IDENTITY'
                mutate_json(name,key,value)
            negative(name+'_'+key,bad)
        negative(name+'_commit',lambda name=name:mutate_json(name,'commit','b'*40))
    for key in ['body_readback_verified','remote_readback_verified','operation_stage']:
        negative('completed_'+key,lambda key=key:mutate_json('PR_BRANCH_RECEIPT.json',key,False))
    for name in sorted(files):negative('blob_'+name,lambda name=name:mode.update(blob=name))
    for label,parents in [('no_parent',''),('wrong_parent','b'*40),('two_parents',u['ORIGINAL']+' '+'b'*40)]:negative(label,lambda parents=parents:mode.update(parents=parents))
    negative('foreign_changed_path',lambda:mode.update(extra_paths=['foreign/path']))
    negative('body_control',lambda:(pub/'PR_BODY_FINAL.md').write_text('FORGED BODY'))
    for key,value in [('url','https://github.com/AlecKriebel/Math/pull/12830'),('state','CLOSED'),('headRefOid','b'*40),('headRefName','other'),('baseRefName','other'),('body','FORGED LIVE BODY'),('isDraft',None),('files',[{'path':name} for name in sorted(files)[:-1]])]:negative('live_'+key,lambda key=key,value=value:state.update({key:value}))
    negative('live_base_missing',lambda:state.pop('baseRefName'))
    negative('live_duplicate_paths',lambda:state.update(files=[{'path':sorted(files)[0]}]*13))
    negative('remote_head',lambda:mode.update(remote='b'*40))
    for name,key,value in [('PUBLICATION_RECEIPT.json','state','draft'),('PUBLICATION_RECEIPT.json','doi','10.5281/zenodo.124'),('PUBLICATION_RECEIPT.json','metadata_normalizations',[{}]),('tracker/TRACKER_RECEIPT.json','readback_verified',False),('tracker/TRACKER_RECEIPT.json','row',['wrong','','','']),('PUBLIC_DOWNLOAD_VERIFICATION.json','all_supplied_metadata_exact',False),('PUBLIC_DOWNLOAD_VERIFICATION.json','files',[])]:negative(name+'_'+key,lambda name=name,key=key,value=value:mutate_json(name,key,value))
    negative('artifact_bytes',lambda:(pub/f['build']['pdf']['path']).write_bytes(b'CORRUPT PDF'))
    negative('final_gate',lambda:mutate_json('FINAL_REVIEW_GATE.json','status','fail'))
    for name in ['PR_BRANCH_RECEIPT.json','PR_BRANCH_INTENT.json','PR_BODY_FINAL.md']:
        def during(name=name):
            def wrapped():
                actual_main();path=pub/name;path.write_bytes(path.read_bytes()+b'\n')
            u['main']=wrapped
        negative('control_changed_during_auth_'+name,during)
    reset()
    # Authentication is repeated immediately before both service boundaries.
    def after_ready():state['baseRefName']='other'
    mode['after_ready']=after_ready;reject(invoke,'retarget_after_ready');need(events==[('ready',head)],'Retargeted PR merged');results.append('retarget_after_ready_blocks_merge')
    for kind in ['ready','merge']:
        reset();mode[kind+'_unknown']=True
        reject(invoke,'uncertain_'+kind);before=list(events);recovery=invoke();need(events==before and recovery['new_ready_requests']==0 and recovery['new_merge_requests']==0,'Uncertain request was retried');positives.append('uncertain_'+kind+'_readonly_recovery')
    reset();mode.update(merge_unaccepted=True,merge_return=1);reject(invoke,'failed_merge');before=list(events);invoke();need(events==before,'Failed unaccepted merge retried');positives.append('failed_merge_readonly_recovery')
    reset()
    def race():
        if mode.get('raced'):return
        # The second service read follows the second complete authentication.
        mode['live_count']=mode.get('live_count',0)+1
        if mode['live_count']==2:
            mode['raced']=True;save(pub/'READY_REQUEST_INTENT.json',{'concurrent_fixture':True})
    mode['live_hook']=race;reject(invoke,'exclusive_ready_intent_race');need(not events,'Concurrent ready intent allowed mutation');results.append('exclusive_ready_intent_race')
    reset();auth=r.authenticate_completed(u)
    need(len(auth['paths'])==13 and all(args[0] in {'branch','rev-list','diff-tree','show','ls-remote'} for args in reads),'Ready validator omitted exact intended tree checks or made Git mutation')
    # Service query shape is checked independently from its mocked state.
    seen=[];original_subprocess=r.subprocess
    r.subprocess=types.SimpleNamespace(check_output=lambda args,**kwargs:(seen.append(args) or json.dumps(state)))
    try:r.Services().live()
    finally:r.subprocess=original_subprocess
    need('baseRefName' in seen[0][seen[0].index('--json')+1].split(','),'Ready live query omitted baseRefName')
    reset()
    return {'full_operative_update_main_reexecuted':True,'all_thirteen_commit_blobs_corrupted_separately':13,'single_original_parent_required':True,'negative_controls':results,'positive_controls':positives,'base_query_and_phase_checked':True,'all_external_operations_mocked':True,'existing_attempts_never_mutate':True}

def identity_matrix(folder):
    """Current operative preflight/append predicates in every one of four cells."""
    folder.mkdir(parents=True);out=[];previous=None
    context={'title':'SYNTHETIC IDENTITY MATRIX','tracker':{'original_problem':'30005434 (OWR12697693005); https://github.com/AlecKriebel/Math/pull/1283','notes':'Synthetic notes'}}
    pub={'environment':'production','state':'published','metadata_normalizations':[],'id':123,'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','title':context['title']}
    identities={**PROBLEM_IDENTITIES,**DOI_IDENTITIES,'unrelated':'Unrelated42',**IDENTITY_NEAR_COLLISIONS}
    for kind in ['preflight_unknown','preflight_known','append']:
      for label,identity in identities.items():
       for column in range(4):
        if previous is not None:shutil.rmtree(previous)
        root=folder/(kind+'_'+label+'_'+str(column));previous=root;p=root/'publication';p.mkdir(parents=True)
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
        body='SYNTHETIC ORIGINAL BODY';snapshot={'head':'4624244af725a80a2b7faf111f6b1ca62aaefe37','branch':'dot/semibrace-30005434-complete-existence-20261011','body_sha256':hashlib.sha256(body.encode()).hexdigest()};save(root/'SUBMITTED_SNAPSHOT.json',snapshot)
        live={'state':'OPEN','isDraft':True,'headRefOid':snapshot['head'],'headRefName':snapshot['branch'],'baseRefName':'main','body':body}
        def external(args,**kw):
            if args[0]=='gh':need('baseRefName' in args[args.index('--json')+1].split(','),'deposit live query omitted baseRefName');return json.dumps(live)
            return snapshot['head']+' refs/heads/'+snapshot['branch']+'\n'
        c.subprocess=types.SimpleNamespace(check_output=external)
        try:capture(t.main if kind=='append' else c.live_preflight);accepted=True
        except (RuntimeError,ValueError,KeyError):accepted=False
        unrelated=label=='unrelated' or label in IDENTITY_NEAR_COLLISIONS
        wanted=unrelated or kind=='preflight_unknown' and label in DOI_IDENTITIES
        count=events.count(['spreadsheets','values','append']);need(accepted==wanted and count==(1 if kind=='append' and unrelated else 0),'Identity action matrix differs '+repr((kind,label,column,accepted,count)))
        out.append({'stage':kind,'identity':label,'column':column,'accepted':accepted,'appends':count})
    # Exact intended row is recoverable without any append mutation, even with no previous intent.
    row=t.expected_row(pub,context['title']);rows[:]=[rows[0],row];capture(t.main);need(events.count(['spreadsheets','values','append'])==1,'Exact row recovery made another append')
    base_rejections=[]
    for base in ['other',None]:
        if base is None:live.pop('baseRefName')
        else:live['baseRefName']=base
        before=len(events);base_rejections.append(reject(c.live_preflight,'deposit_preflight_base_'+str(base)));need(len(events)==before,'wrong-base deposit preflight reached tracker service')
    shutil.rmtree(previous)
    return {'cases':out,'deposit_preflight_base_rejections':base_rejections,'exact_full_row_recovered_readonly':True,'predicate_source':'actual append_tracker.py shared by all three action times','known_DOI_preflight_required':True,'unknown_DOI_preflight_allows_unrelated_DOIs':True,'embedded_known_DOI_and_explicit_PR_markers_checked':True,'all_external_operations_mocked':True}

def postmerge_controls(f):
    """Complete actual current verifier main; all services/Git calls are mocked."""
    pubpath=f['pub'];audit=f['audit'];program=audit.parents[1];u=load(pubpath/'update_pr_publication.py');t=load(pubpath/'append_tracker.py');m=load(pubpath.parents[2]/'publication_coordinators/verify_pr1283_merge.py')
    original_pub=json.loads((pubpath/'PUBLICATION_RECEIPT.json').read_text());original_tracker=json.loads((pubpath/'tracker/TRACKER_RECEIPT.json').read_text());original_public=json.loads((pubpath/'PUBLIC_DOWNLOAD_VERIFICATION.json').read_text())
    cases=['baseline','doi_fallback_valid','wrong_gid_same_title','missing_gid','duplicate_designated_gid','wrong_title','bad_headers','missing_row',*[f'wrong_cell_{i}' for i in range(4)],'range_wrong','checkout_wrong','merge_parent_wrong','merge_single_parent','merge_three_parents','merged_bytes_wrong','live_open','live_head_wrong','live_branch_wrong','live_base_wrong','live_base_missing','live_body_wrong','live_url_wrong','saved_body_unverified','saved_remote_unverified','public_false','public_identity_false','public_id_wrong','public_doi_wrong','doi_unresolved','doi_wrong_status','state_current_wrong','state_completed_wrong','state_eligible_wrong','state_publications_wrong']
    aliases={**PROBLEM_IDENTITIES,**DOI_IDENTITIES}
    cases += ['duplicate_'+label+'_'+str(column) for label in aliases for column in range(4)]
    cases += ['unrelated_'+label+'_'+str(column) for label in IDENTITY_NEAR_COLLISIONS for column in range(4)]
    cases += ['merged_blob_'+str(index) for index in range(13)]
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
            _,label,column=case.split('_');row=['','','',''];row[int(column)]=IDENTITY_NEAR_COLLISIONS[label];rows.append(row)
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
        live={'state':'MERGED','headRefOid':head,'headRefName':u.BRANCH,'baseRefName':'main','mergeCommit':{'oid':merge},'mergedAt':'2026-10-17T21:00:00Z','body':body,'url':'https://github.com/AlecKriebel/Math/pull/1283'}
        for label,key,value in [('live_open','state','OPEN'),('live_head_wrong','headRefOid','e'*40),('live_branch_wrong','headRefName','other'),('live_base_wrong','baseRefName','other'),('live_body_wrong','body','wrong'),('live_url_wrong','url','https://github.com/AlecKriebel/Math/pull/9999')]:
            if case==label:live[key]=value
        if case=='live_base_missing':live.pop('baseRefName')
        def external(args,**kwargs):
            events.append({'gh':args});need('baseRefName' in args[args.index('--json')+1].split(','),'postmerge live query omitted baseRefName');return json.dumps(live)
        m.subprocess=types.SimpleNamespace(check_output=external)
        state={'current_pr':1283,'completed_prs':copy.deepcopy(m.COMPLETED_BEFORE),'publications':[{'pr':n} for n in m.COMPLETED_BEFORE],'eligible_prs':copy.deepcopy(m.ELIGIBLE),'eligible_count':12}
        if case=='state_current_wrong':state['current_pr']=9999
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
        need(after['current_pr']==(None if wanted_accept else state['current_pr']),'Postmerge state advanced despite failure '+case)
        if not wanted_accept:need(after==state,'Postmerge program state mutated despite failure '+case)
        if case in {'live_base_wrong','live_base_missing'}:need(not any(event.get('git',[''])[0] in {'fetch','update-ref'} for event in events),'Wrong-base postmerge reached Git mutation')
        if case.startswith('duplicate_') and case!='duplicate_designated_gid':need(rejection=='Missing/different/duplicate problem or DOI row','Alias duplicate did not reach the exact actual postmerge identity check '+case)
        if case.startswith('merged_blob_'):
            target=sorted(files)[int(case.removeprefix('merged_blob_'))]
            need(rejection=='Merged bytes differ '+target,'Per-file corruption did not reach its exact merged-blob check '+case)
        if wanted_accept:need(after['completed_prs']==m.COMPLETED_BEFORE+[1283] and len(after['publications'])==12 and after['completion_estimate_percent']==99 and after['status']=='final_actual_outcome_reconciliation_pending','Expected11 to12 completed with final reconciliation pending');observed=json.loads((pubpath/'tracker/POSTMERGE_READBACK.json').read_text());need(observed['observed_sheet_properties']=={'sheetId':t.GID,'title':'Math Puzzles'},'Current observed tab receipt differs')
        out.append({'case':case,'accepted':accepted,'state_advanced':wanted_accept,'events':events,'corrupt_path':sorted(files)[int(case.removeprefix('merged_blob_'))] if case.startswith('merged_blob_') else None})
    return {'cases':out,'current_source_sha256':sha(POSTMERGE),'all_operations_mocked':True,'scope':'Actual current source complete main on synthetic receipts; no production integration.'}

def preserved_source_controls(folder):
    f=fixture(folder,source_mode='preserve_submitted');a=f['audit'];v=f['v']
    need(not (a/'CURRENT_EDITION_CORRECTION.json').exists(),'preserved fixture invented a correction receipt')
    v.load_context(a,f['pub']);need(all((a/'submitted'/n).read_bytes()==(a/'current_edition'/n).read_bytes() for n in v.NAMES),'preserve fixture bytes differ')
    p,t,_=publication_and_tracker_controls(f);update_controls(f,p,t);ready=ready_controls(f)
    return {'original8_current8_exact':True,'no_correction_receipt_required':True,'complete_updater_and_ready_driver_pass':True,'ready_negative_controls':len(ready['negative_controls'])}

def worker():
    scratch=REPORT_ROOT/'_local';scratch.mkdir(parents=True,exist_ok=True);os.environ['TMPDIR']=str(scratch);tempfile.tempdir=str(scratch)
    with tempfile.TemporaryDirectory(prefix='synthetic-offline-',dir=scratch) as tmp:
        base=Path(tmp);source_schema=source_schema_controls(base/'source-schema');preserved=preserved_source_controls(base/'preserved');f=fixture(base/'main');preimport=preimport_controls(f);context=context_and_portable_controls(f);corrections=correction_controls(f);documents=document_controls(f);reviews=review_controls(f);p,t,public=publication_and_tracker_controls(f);updates=update_controls(f,p,t)
        ready=ready_controls(f);identities=identity_matrix(base/'identity-matrix');postmerge=postmerge_controls(f);relocation=relocation_and_root_replay_controls(base/'relocation');history=historical_review_controls(fixture(base/'historical-reviews'));coordinator=[]
        for case in ['successful_publish','uncertain_stage_known_id_recovery','normalization_between_inspect_and_POST','wrong_id_first_fresh_inspection','wrong_id_second_fresh_inspection','uncertain_then_published_recovery']+['server_field_'+name for name in sorted(f['context']['metadata'])]:
            case_root=base/case
            try:other=fixture(case_root);coordinator.append(coordinator_case(other,case))
            finally:
                if case_root.exists():shutil.rmtree(case_root)
        current_metadata={'scope':'Actual current metadata absent; only eleven-field synthetic metadata was tested.','sha256':None}
        if (ROOT/'zenodo-deposit.json').exists():
            wanted=json.loads((ROOT/'zenodo-deposit.json').read_text())['metadata'];v=load(ROOT/DEPLOY['verification/verify.py']);v.metadata_contract(wanted);m=load(ROOT/'check_public_downloads.py');actual=copy.deepcopy(wanted);actual['resource_type']={'type':actual.pop('upload_type'),'subtype':actual.pop('publication_type')};actual['license']={'id':actual['license']};fields=m.verify_public_metadata(actual,wanted)
            current_metadata={'scope':'Actual current local metadata projected and compared offline; no public API/record is implied.','sha256':sha(ROOT/'zenodo-deposit.json'),'fields':fields}
        return {'status':'PASS','source_schema_controls':source_schema,'context_and_portable':context,'preserved_source_controls':preserved,'documented_correction_controls':corrections,'identity_action_matrix':identities,'postmerge_complete_main':postmerge,'document_assurance_rejections':documents,'review_gate_rejections':reviews,'relocation_and_root_replay':relocation,'historical_review_sequence':history,'tracker_and_public':public,'current_local_metadata_projection':current_metadata,'PR_update':updates,'ready_and_expected_head_merge':ready,'preimport_source_controls':preimport,'deposit_coordinator_actual_kit_mocked_clients':coordinator,'operative_coordinator_layout':'program/publication_coordinators/pr1283.py resolves program/audits/pr1283_30005434/publication','scope':'Synthetic fixture metadata/gates/compiler/pdfinfo/reviewer evidence only, except any explicitly reported actual local metadata projection. No real mathematical/priority adjudication, actual PDF compilation/rendering, service integration, Git mutation, staging/upload/publication/tracker append or PR change occurred.'}

def main():
    if '--worker' in sys.argv:print(json.dumps(worker(),sort_keys=True));return
    runs=[]
    for flags in [[],['-O'],['-OO']]:
        run=subprocess.run([sys.executable,'-B',*flags,str(Path(__file__).resolve()),'--worker'],capture_output=True,text=True);need(run.returncode==0,run.stderr);runs.append({'flags':flags,'result':json.loads(run.stdout)})
    need(all(item['result']==runs[0]['result'] for item in runs),'optimization-dependent guards')
    receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':runs,'all_modes_identical':True,'authored_workflow_sha256':{str(ROOT/source):sha(ROOT/source) for source in DEPLOY.values()}|{str(COORDINATOR):sha(COORDINATOR),str(POSTMERGE):sha(POSTMERGE),str(READY):sha(READY)},'scope':'Offline synthetic fixture regressions only; final actual package requires rerun and independent whole-package review.'}
    save(REPORT_ROOT/'_local/WORKFLOW_REGRESSION_RECEIPT.json',receipt);print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
