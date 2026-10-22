from pathlib import Path
import json,hashlib,datetime,shutil
R=Path(__file__).resolve().parent;A=R.parents[1];T=A.parents[1];D=R/'deployed';P=D/'audits/pr1280_30003587/publication'
p=P/'verification/verify.py';s=p.read_text();s=s.replace("PROSE = {'AUDIT.md','PROOF.md','README.md'}\nSTRUCTURED = {'EDITORIAL_MAP.json','SOURCE_VERIFICATION.json'}\n",'')
a=s.index('def authenticate_current(');b=s.index('\ndef load_context',a)
s=s[:a]+'''def authenticate_current(root,context,original):
    authenticate_edition(root)
    mode=context.get('edition_mode');need(mode in {'preserve_submitted','documented_correction'},'explicit current edition mode required')
    supplied=context.get('source_bindings',{}).get('current_edition')
    if supplied is not None:
        need(isinstance(supplied,dict) and set(supplied)==NAMES,'exact nine current source bindings required')
        for name in NAMES:check_binding(member(root,name),supplied[name])
    if mode=='preserve_submitted':
        for name in NAMES:need(member(root,name).read_bytes()==member(original,name).read_bytes(),'preserved current original differs '+name)
    else:need(supplied is not None,'documented correction requires current source bindings')

def authenticate_source_bindings(audit,evidence_root,context):
    supplied=context.get('source_bindings');need(isinstance(supplied,dict) and set(supplied)=={'submitted_snapshot_sha256','current_edition_correction_sha256','current_edition'},'exact source bindings schema required')
    snapshot_path=member(audit,'SUBMITTED_SNAPSHOT.json');need(digest(snapshot_path)==supplied['submitted_snapshot_sha256'],'source original snapshot anchor differs')
    snapshot=json.loads(snapshot_path.read_text());original_map={Path(e['path']).name:{'bytes':e['bytes'],'sha256':e['sha256']} for e in snapshot['files']}
    need(len(snapshot['files'])==9 and set(original_map)==NAMES,'source snapshot exact nine names required')
    current_map=supplied['current_edition'];need(isinstance(current_map,dict) and set(current_map)==NAMES,'exact nine current source bindings required')
    same_root=audit.resolve()==evidence_root.resolve();original=evidence_root/('submitted' if same_root else 'original_submitted')
    authenticate_snapshot(original,snapshot);authenticate_current(evidence_root/'current_edition',context,original)
    if context['edition_mode']=='preserve_submitted':
        need(supplied['current_edition_correction_sha256'] is None and current_map==original_map,'preserved mode source bindings differ');return None
    correction_path=member(audit,'CURRENT_EDITION_CORRECTION.json');need(digest(correction_path)==supplied['current_edition_correction_sha256'],'current correction anchor differs')
    record=json.loads(correction_path.read_text())
    keys={'schema','at_utc','pr','problem_id','original_head','submitted_snapshot_sha256','original_files','current_files','changes','scope'}
    need(set(record)==keys and record['schema']=='math-pr1280-current-edition-correction-v1' and record['pr']==PR and record['problem_id']==PROBLEM and record['original_head']==ORIGINAL,'exact documented correction schema/target required')
    need(record['submitted_snapshot_sha256']==supplied['submitted_snapshot_sha256'] and record['original_files']==original_map and record['current_files']==current_map,'documented correction original/current bindings differ')
    need(isinstance(record['at_utc'],str) and bool(record['at_utc']) and isinstance(record['scope'],str) and bool(record['scope'].strip()),'actual correction time and scope required')
    changed={name for name in NAMES if original_map[name]!=current_map[name]};need(bool(changed),'documented correction must identify an actual byte change')
    entries=record['changes'];need(isinstance(entries,list) and len(entries)==len(changed),'one declaration for every changed current file required');seen=set()
    for entry in entries:
        need(isinstance(entry,dict) and set(entry)=={'path','original_sha256','current_sha256','reason'},'explicit correction change schema required')
        name=entry['path'];need(name in changed and name not in seen,'undeclared/duplicate current correction change');seen.add(name)
        need(entry['original_sha256']==original_map[name]['sha256'] and entry['current_sha256']==current_map[name]['sha256'] and isinstance(entry['reason'],str) and bool(entry['reason'].strip()),'correction exact before/after and reason required')
    need(seen==changed,'correction changed-file inventory differs');return record
''' +s[b:]
s=s.replace("'gate_bindings','document_bindings'}","'gate_bindings','document_bindings','source_bindings'}")
a=s.index("    need(context['edition_mode']=='preserve_submitted'");b=s.index("    need(context['disclosures']",a)
s=s[:a]+"    need(context['edition_mode'] in {'preserve_submitted','documented_correction'},'explicit current edition mode required')\n    need(context['edition_text']=={} and context['structured_records']=={},'current edition bytes must use explicit source bindings, no inferred prose/record schema')\n"+s[b:]
needle="    authenticate_nested_manifests(evidence_root,context['authored_freezes'])"
s=s.replace(needle,"    authenticate_source_bindings(audit,evidence_root,context)\n"+needle)
p.write_text(s)
p=P/'prepare_package.py';s=p.read_text();a=s.index("    v['need'](context['edition_mode']=='preserve_submitted'");b=s.index("    v['authenticate_current']",a)
s=s[:a]+"    v['need'](context['edition_mode'] in {'preserve_submitted','documented_correction'},'Explicit current edition mode required')\n    # The current edition is already exactly bound; never overwrite a reviewed correction.\n"+s[b:]
s=s.replace("    for name in ['COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json']:copy(ROOT/name,'provenance/'+name)","    if context['edition_mode']=='documented_correction':copy(AUDIT/'CURRENT_EDITION_CORRECTION.json','provenance/CURRENT_EDITION_CORRECTION.json')\n    for name in ['COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json']:copy(ROOT/name,'provenance/'+name)")
p.write_text(s)
p=P/'compile_note.py';s=p.read_text().replace("context.get('edition_mode')!='preserve_submitted'","context.get('edition_mode') not in {'preserve_submitted','documented_correction'}")
s=s.replace("    compiler=shutil.which('tectonic')","    v['authenticate_source_bindings'](ROOT.parent,ROOT.parent,context)\n    compiler=shutil.which('tectonic')");p.write_text(s)
p=P/'update_pr_publication.py';s=p.read_text().replace("if context['edition_mode']!='preserve_submitted':raise RuntimeError('PR1280 preserves the nine submitted files')","if context['edition_mode'] not in {'preserve_submitted','documented_correction'}:raise RuntimeError('Explicit bound current nine-file edition required')")
s=s.replace("if data!=(ROOT.parent/'submitted'/name).read_bytes():raise RuntimeError('Original preserved byte drift '+name)","if archive.read('original_submitted/'+name)!=(ROOT.parent/'submitted'/name).read_bytes():raise RuntimeError('Archived original byte drift '+name)\n            if context['source_bindings']['current_edition'][name]!={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}:raise RuntimeError('Current source binding drift '+name)")
s=s.replace("    pending_resolutions=[]","    if context['edition_mode']=='documented_correction':required.add(str((ROOT.parent/'CURRENT_EDITION_CORRECTION.json').resolve()))\n    pending_resolutions=[]")
p.write_text(s)
p=D/'publication_coordinators/pr1280.py';s=p.read_text();s=s.replace("  for n in ['COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json']:","  if context['edition_mode']=='documented_correction':require(z.read('provenance/CURRENT_EDITION_CORRECTION.json')==(A/'CURRENT_EDITION_CORRECTION.json').read_bytes(),'Archive correction drift')\n  for n in ['COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json']:")
p.write_text(s)
# Fixture: wrappers are ordinary bound bytes; do not assume legacy acceptance/map schemas.
p=P/'workflow_regression.py';s=p.read_text();needle="    for name in ['MATH_GATE.json','PRIORITY_ADJUDICATION.json']:save"
a=s.index(needle)
insert="""    current=audit/'current_edition';shutil.copytree(submitted,current)
    (current/'PROOF.md').write_text((current/'PROOF.md').read_text()+'SYNTHETIC CONTROLLED DOCUMENTARY QUALIFICATION; THEOREM UNCHANGED\\n')
    save(current/'ACCEPTANCE.json',{'schema':'SYNTHETIC CURRENT WRAPPER v2','historical':json.loads((submitted/'ACCEPTANCE.json').read_text()),'qualification':'SYNTHETIC FIXTURE ONLY'})
    save(current/'MANIFEST.json',{'schema':'public-proof-packet-manifest-v1','problem_id':str(v.PROBLEM),'intended_repository_path':v.BASE,'files':{n:binding(current/n) for n in sorted(v.NAMES-{'MANIFEST.json'})}})
    original_map={n:binding(submitted/n) for n in v.NAMES};current_map={n:binding(current/n) for n in v.NAMES}
    correction={'schema':'math-pr1280-current-edition-correction-v1','at_utc':'2026-10-17T21:00:00Z','pr':v.PR,'problem_id':v.PROBLEM,'original_head':v.ORIGINAL,'submitted_snapshot_sha256':sha(audit/'SUBMITTED_SNAPSHOT.json'),'original_files':original_map,'current_files':current_map,'changes':[{'path':n,'original_sha256':original_map[n]['sha256'],'current_sha256':current_map[n]['sha256'],'reason':'SYNTHETIC CONTROLLED DOCUMENTARY CORRECTION ONLY'} for n in sorted(v.NAMES) if original_map[n]!=current_map[n]],'scope':'SYNTHETIC CORRECTION FIXTURE ONLY; NO ACTUAL MATHEMATICAL APPROVAL'}
    save(audit/'CURRENT_EDITION_CORRECTION.json',correction)
    source_bindings={'submitted_snapshot_sha256':sha(audit/'SUBMITTED_SNAPSHOT.json'),'current_edition_correction_sha256':sha(audit/'CURRENT_EDITION_CORRECTION.json'),'current_edition':current_map}
"""
s=s[:a]+insert+s[a:]
s=s.replace("context={'edition_mode':'preserve_submitted'","context={'edition_mode':'documented_correction','source_bindings':source_bindings")
s=s.replace("required+=[u.SHARED_KIT,coordinator,postmerge]","required+=[audit/'CURRENT_EDITION_CORRECTION.json',u.SHARED_KIT,coordinator,postmerge]")
s=s.replace("'original9_current9':True","'original9_current9':True,'documented_current_changes_allowed':True,'current_acceptance_wrapper_schema_not_inferred':True")
s=s.replace("context=context_and_portable_controls(f);documents", "context=context_and_portable_controls(f);corrections=correction_controls(f);documents")
s=s.replace("'context_and_portable':context,","'context_and_portable':context,'documented_correction_controls':corrections,")
a=s.index('\ndef review_controls(')
insert='''
def correction_controls(f):
    v=f['v'];a=f['audit'];p=f['pub'];context=f['context'];cp=a/'CURRENT_PR1280_CONTEXT.json';rp=a/'CURRENT_EDITION_CORRECTION.json';rejected=[]
    v.load_context(a,p);need((a/'current_edition/PROOF.md').read_bytes()!=(a/'submitted/PROOF.md').read_bytes(),'documented correction fixture must differ')
    for label,mutate in [('wrong_snapshot_anchor',lambda c:c['source_bindings'].update(submitted_snapshot_sha256='0'*64)),('wrong_correction_anchor',lambda c:c['source_bindings'].update(current_edition_correction_sha256='0'*64)),('wrong_current_binding',lambda c:c['source_bindings']['current_edition']['PROOF.md'].update(sha256='0'*64)),('missing_current_binding',lambda c:c['source_bindings']['current_edition'].pop('README.md')),('preserve_mode_changed_bytes',lambda c:c.update(edition_mode='preserve_submitted'))]:
        bad=copy.deepcopy(context);mutate(bad);save(cp,bad);rejected.append(reject(lambda:v.load_context(a,p),label));save(cp,context)
    original=rp.read_bytes()
    for label,mutate in [('undeclared_change',lambda r:r['changes'].pop()),('wrong_before_sha',lambda r:r['changes'][0].update(original_sha256='0'*64)),('wrong_after_sha',lambda r:r['changes'][0].update(current_sha256='0'*64)),('empty_reason',lambda r:r['changes'][0].update(reason='')),('duplicate_change',lambda r:r['changes'].append(copy.deepcopy(r['changes'][0]))),('wrong_current_map',lambda r:r['current_files']['PROOF.md'].update(sha256='0'*64)),('wrong_original_map',lambda r:r['original_files']['PROOF.md'].update(sha256='0'*64)),('wrong_correction_target',lambda r:r.update(pr=1))]:
        bad=json.loads(original);mutate(bad);save(rp,bad);ctx=copy.deepcopy(context);ctx['source_bindings']['current_edition_correction_sha256']=sha(rp);save(cp,ctx);rejected.append(reject(lambda:v.load_context(a,p),label));rp.write_bytes(original);save(cp,context)
    for raw in ['current_edition/PROOF.md','current_edition/MANIFEST.json','submitted/PROOF.md','SUBMITTED_SNAPSHOT.json']:
        path=a/raw;old=path.read_bytes();path.write_bytes(old+b'UNDECLARED TAMPERING');rejected.append(reject(lambda:v.load_context(a,p),'tampered_'+raw));path.write_bytes(old)
    return {'different_current_proof_and_acceptance_wrapper_accepted':True,'original_submission_stays_exact':True,'only_exact_declared_relative_source_bindings_followed':True,'negative_controls':rejected}
'''
s=s[:a]+insert+s[a:];p.write_text(s)
# Deploy exactly the changed sources; all current bindings are refreshed.
names=['compile_note.py','prepare_package.py','build_package.py','verification/verify.py','workflow_regression.py','check_public_downloads.py','append_tracker.py','update_pr_publication.py']
for name in names:shutil.copyfile(P/name,A/'publication'/name)
for name in ['pr1280.py','verify_pr1280_merge.py']:shutil.copyfile(D/'publication_coordinators'/name,T/'publication_coordinators'/name)
r=json.loads((R/'ACTUAL_DEPLOYMENT_RECEIPT.json').read_text());r['at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();r['current_edition_policy']='Root-authorized documented correction, exact current9 through source_bindings and correction receipt; original submitted9 remain immutable.'
for e in r['files']:
 b=Path(e['path']).read_bytes();e.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
(R/'ACTUAL_DEPLOYMENT_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n')
print('Adapted explicit documented correction contract and redeployed ten helpers.')
