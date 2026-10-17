#!/usr/bin/env python3
"""Portable integrity checker; requires outside anchors, makes no theorem claim.

Deploy this file as publication/verification/verify.py. Registry schemas are
explicit: absolute-path fields in historical receipts are never followed.
"""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parent
PR, PROBLEM = 1262, 30001248
ORIGINAL = 'fb7b750865f3e220590f128661c487c5984bae75'
BRANCH = 'publication/triangle-modular-threshold-30001248-recovered-20261011'
BODY = '3ab8f23a031f563bb7b5367792af9b723b1d637ada5cc78d44c717197be51d3c'
BASE = 'unsolved_math_prioritization/attempts/30001248'
NAMES = {'ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json'}
PROSE = {'ACCEPTANCE.md','AUDIT.md','PROOF.md','README.md'}
STRUCTURED = {'ACCEPTANCE.json','SOURCES.json','VERIFICATION.json'}
FIELDS = {'title','upload_type','publication_type','description','creators','access_right','license','version','publication_date','keywords','related_identifiers'}
SCHEMAS = {('files','relative_path','size_bytes'),('files','relative_path','bytes'),('authored_files','relative_path','bytes'),('authored_artifacts','relative_path','bytes'),('entries','path','bytes'),('entries','relative_path','bytes'),('entries','file','bytes'),('authored_files','path','bytes'),('files','path','bytes'),('all_authored_content_files','path_relative_to_authored_root','bytes'),('members','path','bytes'),('authored_members','path','bytes'),('authored_outputs','path','bytes')}
MINIMUM = {'reviews/source_question_family/manifest.json':('reviews/source_question_family','files','relative_path','size_bytes'), 'reviews/analytic_adversary/MANIFEST.json':('reviews/analytic_adversary','authored_files','path','bytes')}

def need(value, message):
    if not value: raise ValueError(message)

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def binding(path): return {'bytes':path.stat().st_size,'sha256':digest(path)}
def safe(raw):
    need(isinstance(raw,str) and bool(raw) and '\\' not in raw and '\x00' not in raw,'invalid relative path')
    rel=PurePosixPath(raw)
    need(not rel.is_absolute() and '..' not in rel.parts and str(rel)==raw and raw!='.','unsafe relative path '+raw)
    return raw

def member(root, raw):
    path=root/safe(raw)
    cursor=path
    while cursor!=root:
        need(not cursor.is_symlink(),'symlink path '+raw);cursor=cursor.parent
    need(not root.is_symlink(),'symlink root')
    try: path.resolve().relative_to(root.resolve())
    except ValueError: raise ValueError('path escapes root '+raw)
    return path

def check_binding(path, entry, size_key='bytes'):
    need(type(entry.get(size_key)) is int and entry[size_key]>=0,'invalid size '+str(path))
    need(isinstance(entry.get('sha256'),str) and re.fullmatch('[0-9a-f]{64}',entry['sha256']) is not None,'invalid digest '+str(path))
    need(binding(path)=={'bytes':entry[size_key],'sha256':entry['sha256']},'binding differs '+str(path))

def metadata_contract(metadata):
    need(isinstance(metadata,dict) and set(metadata)==FIELDS,'exact eleven supplied metadata fields required')
    need(metadata['upload_type']=='publication' and metadata['publication_type']=='preprint','preprint metadata required')
    need(metadata['version']=='1.0' and metadata['access_right']=='open','version/open metadata differs')
    for key in ['title','description','license','publication_date']:
        need(isinstance(metadata[key],str) and bool(metadata[key].strip()),'empty metadata '+key)
    need(metadata['title'].isascii() and metadata['description'].isascii(),'title/description require explicit ASCII punctuation/text to avoid normalization')
    need(isinstance(metadata['creators'],list) and bool(metadata['creators']),'creators required')
    for creator in metadata['creators']:
        need(isinstance(creator,dict) and bool(creator.get('name')) and 'affiliation' in creator,'explicit creator name and affiliation (null allowed) required')
    need(isinstance(metadata['keywords'],list) and isinstance(metadata['related_identifiers'],list),'metadata list fields required')
    for item in metadata['related_identifiers']:
        need(isinstance(item,dict) and bool(item.get('identifier')) and bool(item.get('relation')) and bool(item.get('scheme')),'explicit related identifier schema required')
        if item['scheme']=='doi': need(re.fullmatch(r'10\.\d{4,9}/\S+',item['identifier']) is not None and not item['identifier'].startswith('https:'),'DOI identifier must be bare canonical DOI')
    return metadata

def registry_schema(item):
    fields={'path','base','entries_key','path_key','size_key','sha256'}
    need(isinstance(item,dict) and set(item) in [fields,fields|{'path_mode'},fields|{'path_mode','absolute_root_key'}],'registry exact schema required')
    triple=tuple(item[k] for k in ['entries_key','path_key','size_key'])
    need(triple in SCHEMAS,'unsupported explicit registry schema')
    mode=item.get('path_mode','relative')
    need(mode in {'relative','absolute_under_family_root'},'unsupported explicit member path mode')
    need((triple in {('members','path','bytes'),('authored_members','path','bytes'),('authored_outputs','path','bytes')}) == (mode=='absolute_under_family_root'),'legacy absolute membership requires explicit absolute_under_family_root mode')
    need(item.get('absolute_root_key','family_root') in {'family_root','review_root'} and ('absolute_root_key' not in item or mode=='absolute_under_family_root'),'unsupported explicit absolute root key')
    return mode

def manifest_member_name(registry, entry, manifest):
    """Normalize strings only; never resolve or open historical host absolutes."""
    mode=registry_schema(registry);raw=entry.get(registry['path_key'])
    if mode=='relative':return safe(raw)
    anchor=manifest.get(registry.get('absolute_root_key','family_root'))
    need(isinstance(anchor,str) and isinstance(raw,str) and '\\' not in anchor and '\\' not in raw,'absolute legacy path/anchor required')
    base=PurePosixPath(anchor);path=PurePosixPath(raw)
    need(base.is_absolute() and path.is_absolute() and '..' not in base.parts and '..' not in path.parts and str(base)==anchor and str(path)==raw and anchor.endswith('/'+safe(registry['base'])),'noncanonical/mismatched historical family root')
    try:name=path.relative_to(base).as_posix()
    except ValueError:raise ValueError('historical absolute member outside anchored family root')
    return safe(name)

def authenticate_nested_manifests(root, registry, require_complete=True):
    need(isinstance(registry,list) and bool(registry),'explicit nonempty authored freeze registry required')
    listed={}; checked=[]
    for item in registry:
        registry_schema(item)
        raw=safe(item['path']); base=safe(item['base'])
        need(raw not in listed and raw.startswith(('reviews/','priority/')),'duplicate/outside authored freeze')
        need(raw.startswith(base+'/') and base.startswith(('reviews/','priority/')),'freeze/base family mismatch')
        path=member(root,raw); need(digest(path)==item['sha256'],'outside freeze anchor differs '+raw)
        listed[raw]=item
        obj=json.loads(path.read_text());entries=obj.get(item['entries_key'])
        need(isinstance(entries,list) and bool(entries),'invalid nested entries '+raw)
        seen=set()
        for entry in entries:
            name=manifest_member_name(item,entry,obj); need(name not in seen,'duplicate nested member'); seen.add(name)
            need(base+'/'+name!=raw,'self reference in authored freeze')
            check_binding(member(member(root,base),name),entry,item['size_key'])
        checked.append({'path':raw,'base':base,'entries':len(entries),'schema_keys':[item[k] for k in ['entries_key','path_key','size_key']]})
    if require_complete:
        for raw,shape in MINIMUM.items():
            need(raw in listed and tuple(listed[raw][k] for k in ['base','entries_key','path_key','size_key'])==shape,'required freeze/schema '+raw)
        need(any(raw.startswith(('priority/','reviews/priority_')) for raw in listed),'final explicitly registered priority family authored freeze required')
    return checked

def authenticate_snapshot(root, snapshot):
    need(snapshot.get('pr')==PR and snapshot.get('problem_id')==PROBLEM and snapshot.get('head')==ORIGINAL and snapshot.get('branch')==BRANCH and snapshot.get('body_sha256')==BODY,'original snapshot identity differs')
    entries=snapshot.get('files',[])
    need(len(entries)==8 and {e['path'] for e in entries}=={BASE+'/'+n for n in NAMES},'exact original eight-file scope required')
    for entry in entries:
        path=member(root,Path(entry['path']).name);check_binding(path,entry)
        data=path.read_bytes();need(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['blob'],'original Git blob differs')
    authenticate_edition(root)

def authenticate_edition(root):
    need({p.name for p in root.iterdir()}==NAMES,'edition must contain exactly eight regular files')
    manifest=json.loads(member(root,'MANIFEST.json').read_text());entries=manifest.get('entries');members=manifest.get('members')
    need(manifest.get('problem_id')==PROBLEM and manifest.get('self_hash_excluded')=='MANIFEST.json','explicit target and MANIFEST self exclusion required')
    need(isinstance(members,list) and len(members)==8 and len(set(members))==8 and set(members)==NAMES,'exact eight string MANIFEST members required')
    need(isinstance(entries,list) and len(entries)==7 and {e.get('file') for e in entries}==NAMES-{'MANIFEST.json'},'exact seven nonself entries/file/bytes/sha256 required')
    for entry in entries:
        need(set(entry)=={'file','bytes','sha256'},'exact original/current MANIFEST entry schema required')
        check_binding(member(root,entry['file']),entry)

def load_context(audit, document_root=None, evidence_root=None):
    evidence_root=audit if evidence_root is None else evidence_root
    context=json.loads(member(audit,'CURRENT_PR1262_CONTEXT.json').read_text())
    keys={'schema','pr','problem_id','original_head','original_branch','original_body_sha256','title','expected_pdf_pages','source_date_epoch','edition_text','structured_records','disclosures','metadata','publication_text','tracker','authored_freezes','portable_files','diagnostic_replays','gate_bindings','document_bindings'}
    need(set(context)==keys,'current context exact keys required')
    need(context['schema']=='math-pr1262-current-context-v1' and context['pr']==PR and context['problem_id']==PROBLEM and context['original_head']==ORIGINAL and context['original_branch']==BRANCH and context['original_body_sha256']==BODY,'current context identity differs')
    need(type(context['expected_pdf_pages']) is int and context['expected_pdf_pages']>0,'actual expected PDF page count required')
    need(isinstance(context['source_date_epoch'],str) and context['source_date_epoch'].isdigit(),'explicit reproducible build stamp required')
    need(set(context['edition_text'])==PROSE and all(isinstance(t,str) and t.strip() for t in context['edition_text'].values()),'exact four explicit current prose records required')
    need(set(context['structured_records'])==STRUCTURED and all(isinstance(t,dict) and t for t in context['structured_records'].values()),'exact three explicit structured records required')
    need(context['disclosures']=={'firstness_claim':False,'current_openness_claim':False,'ai_assisted':True,'unrefereed':True},'explicit no-firstness/AI/unrefereed disclosures required')
    metadata_contract(context['metadata']);need(context['title']==context['metadata']['title'],'explicit current title differs')
    need(set(context['publication_text'])=={'summary','priority_statement','verification_scope'} and all(isinstance(t,str) and t.strip() for t in context['publication_text'].values()),'explicit publication text required')
    need(set(context['tracker'])=={'original_problem','notes'} and all(isinstance(t,str) and t.strip() for t in context['tracker'].values()) and str(PROBLEM) in context['tracker']['original_problem'],'explicit tracker wording/identity required')
    for field,filename in [('math_gate_sha256','MATH_GATE.json'),('priority_adjudication_sha256','PRIORITY_ADJUDICATION.json'),('submitted_snapshot_sha256','SUBMITTED_SNAPSHOT.json')]:
        need(set(context['gate_bindings'])=={'math_gate_sha256','priority_adjudication_sha256','submitted_snapshot_sha256'},'exact gate anchors required')
        need(digest(member(audit,filename))==context['gate_bindings'][field],'context gate anchor differs '+filename)
    for filename in ['MATH_GATE.json','PRIORITY_ADJUDICATION.json']:
        gate=json.loads(member(audit,filename).read_text())
        need(gate.get('pr')==PR and gate.get('problem_id')==PROBLEM and gate.get('original_head')==ORIGINAL and gate.get('status')=='PASS','exact actual PASS gate required '+filename)
        if filename=='PRIORITY_ADJUDICATION.json':
            need(gate.get('firstness_claim') is False and gate.get('current_openness_claim') is False,'priority no-firstness/open disclaimer required')
    authenticate_nested_manifests(evidence_root,context['authored_freezes'])
    need(isinstance(context['portable_files'],list) and bool(context['portable_files']),'explicit portable authored/receipt inventory required')
    seen=set()
    for item in context['portable_files']:
        need(set(item)=={'path','bytes','sha256','role'} and item['role'] in {'authored_evidence','source_receipt','historical_receipt'},'portable inventory exact schema/role required')
        raw=safe(item['path']);need(raw not in seen and raw.split('/')[0] not in {'submitted','current_edition','publication','workflow','_local','provenance','manuscript','verify.py','MANIFEST.json'},'duplicate/reserved portable inventory');seen.add(raw)
        check_binding(member(evidence_root,raw),item)
    # Every frozen manifest/member must be portable; inventories remain ordinary
    # receipts and are never recursively interpreted as retained source bodies.
    for reg in context['authored_freezes']:
        need(reg['path'] in seen,'frozen manifest omitted from portable inventory')
        obj=json.loads(member(evidence_root,reg['path']).read_text())
        for item in obj[reg['entries_key']]:need(reg['base']+'/'+manifest_member_name(reg,item,obj) in seen,'frozen member omitted from portable inventory')
    registered={reg['path'] for reg in context['authored_freezes']}
    for item in context['portable_files']:
        filename=Path(item['path']).name.lower()
        if item['role']=='authored_evidence' and (filename=='manifest.json' or filename.endswith(('_manifest.json','_freeze.json'))):need(item['path'] in registered,'unregistered portable authored freeze '+item['path'])
    need(isinstance(context['diagnostic_replays'],list),'explicit diagnostic replay list required')
    for replay in context['diagnostic_replays']:
        need(set(replay)=={'program','mode','result','output_mode','scope','layout','arguments','comparison'} and replay['mode'] in {'normal','normal_O_OO'} and replay['output_mode'] in {'stdout','file'} and replay['layout'] in {'isolated','original_submission'} and replay['arguments'] in [[],['--output','{output}']] and replay['comparison'] in {'json_exact','json_ignore_runtime','json_ignore_at_utc','json_ignore_start_end_utc','bytes_exact'} and bool(replay['scope']),'explicit replay contract required')
        need(safe(replay['program']) in seen and safe(replay['result']) in seen,'replay program/result must be retained authored members')
    need(set(context['document_bindings'])=={'source_sha256','pdf_sha256','compile_receipt_sha256','layout_receipt_sha256'},'exact document anchors required')
    if document_root is not None:
        for key,raw in [('source_sha256','manuscript/main.tex'),('pdf_sha256','output/pdf/main.pdf'),('compile_receipt_sha256','COMPILE_RECEIPT.json'),('layout_receipt_sha256','LAYOUT_VERIFICATION.json')]:need(digest(member(document_root,raw))==context['document_bindings'][key],'context document drift '+raw)
    return context

def replay_diagnostics(root, context):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';checks=[]
    with tempfile.TemporaryDirectory(prefix='triangle-modular-finite-replay-') as folder:
        for i,spec in enumerate(context['diagnostic_replays']):
            tmp=Path(folder)/str(i);tmp.mkdir()
            program=tmp/(spec['program'] if spec['layout']=='original_submission' else Path(spec['program']).name)
            program.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(member(root,spec['program']),program)
            if spec['layout']=='original_submission':
                shutil.copyfile(root/'provenance/SUBMITTED_SNAPSHOT.json',tmp/'SUBMITTED_SNAPSHOT.json');(tmp/'submitted').mkdir()
                for name in NAMES:shutil.copyfile(root/'original_submitted'/name,tmp/'submitted'/name)
            modes=[[],['-O'],['-OO']] if spec['mode']=='normal_O_OO' else [[]]
            for flags in modes:
                result=program.parent/Path(spec['result']).name
                if result.exists():result.unlink()
                arguments=[str(result) if arg=='{output}' else arg for arg in spec['arguments']]
                run=subprocess.run([sys.executable,'-B',*flags,str(program),*arguments],cwd=tmp,env=env,capture_output=True,text=True,timeout=180)
                need(run.returncode==0,'finite replay failed '+spec['program']+' '+run.stderr)
                expected=member(root,spec['result']).read_bytes()
                actual=run.stdout.encode() if spec['output_mode']=='stdout' else result.read_bytes()
                if spec['comparison']=='bytes_exact':equal=actual==expected
                else:
                    actual_obj=json.loads(actual);expected_obj=json.loads(expected)
                    if spec['comparison']=='json_ignore_runtime':
                        for obj in [actual_obj,expected_obj]:
                            for key in ['run_utc','python','optimization']:obj.pop(key,None)
                    elif spec['comparison']=='json_ignore_start_end_utc':
                        for obj in [actual_obj,expected_obj]:
                            for key in ['run_started_utc','run_completed_utc']:obj.pop(key,None)
                    elif spec['comparison']=='json_ignore_at_utc':
                        for obj in [actual_obj,expected_obj]:obj.pop('at_utc',None)
                    equal=actual_obj==expected_obj
                need(equal,'finite replay differs '+spec['program'])
            checks.append({'program':spec['program'],'mode':spec['mode'],'scope':spec['scope'],'temporary_copy_only':True})
    return checks

def verify(root, expected_manifest_sha256, expected_context_sha256, expected_snapshot_sha256):
    need(digest(root/'MANIFEST.json')==expected_manifest_sha256,'outside root manifest anchor differs')
    need(digest(root/'provenance/CURRENT_PR1262_CONTEXT.json')==expected_context_sha256,'outside context anchor differs')
    need(digest(root/'provenance/SUBMITTED_SNAPSHOT.json')==expected_snapshot_sha256,'outside snapshot anchor differs')
    manifest=json.loads((root/'MANIFEST.json').read_text());need(manifest.get('schema')=='triangle-modular-threshold-verification-v1','root manifest target/schema differs');seen=set()
    for entry in manifest['files']:
        raw=safe(entry['path']);need(raw!='MANIFEST.json' and raw not in seen,'duplicate/self root member');seen.add(raw);check_binding(member(root,raw),entry)
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    need(actual==seen|{'MANIFEST.json'},'unlisted/missing archive member')
    context=load_context(root/'provenance',evidence_root=root)
    need(context['schema']=='math-pr1262-current-context-v1' and context['pr']==PR and context['problem_id']==PROBLEM and context['original_head']==ORIGINAL,'portable context target differs')
    nested=authenticate_nested_manifests(root,context['authored_freezes'])
    for filename,key in [('MATH_GATE.json','math_gate_sha256'),('PRIORITY_ADJUDICATION.json','priority_adjudication_sha256'),('SUBMITTED_SNAPSHOT.json','submitted_snapshot_sha256')]:need(digest(root/'provenance'/filename)==context['gate_bindings'][key],'portable gate anchor differs')
    authenticate_snapshot(root/'original_submitted',json.loads((root/'provenance/SUBMITTED_SNAPSHOT.json').read_text()));authenticate_edition(root/'current_edition')
    for name,text in context['edition_text'].items():need((root/'current_edition'/name).read_text()==text,'current explicit prose differs')
    for name,obj in context['structured_records'].items():need(json.loads((root/'current_edition'/name).read_text())==obj,'current explicit structured record differs')
    for entry in context['portable_files']:check_binding(member(root,entry['path']),entry)
    for raw,key in [('manuscript/main.tex','source_sha256'),('provenance/COMPILE_RECEIPT.json','compile_receipt_sha256'),('provenance/LAYOUT_VERIFICATION.json','layout_receipt_sha256')]:need(digest(root/raw)==context['document_bindings'][key],'portable document assurance differs')
    checks=replay_diagnostics(root,context)
    for entry in manifest['files']:check_binding(member(root,entry['path']),entry)
    return {'status':'PASS','authenticated_members':len(seen),'submitted_files':8,'current_edition_files':8,'nested_manifests':nested,'finite_diagnostic_replays':checks,'limits':'Integrity and explicitly scoped finite diagnostics only. Written proofs and actual mathematical/priority adjudication remain separate. Read/retained source inventories are receipts; omitted third-party source bodies and omitted historical code are not reauthenticated or replayed.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['manifest','context','snapshot']:parser.add_argument('--expected-'+name+'-sha256',required=True)
    args=parser.parse_args();print(json.dumps(verify(ROOT,args.expected_manifest_sha256,args.expected_context_sha256,args.expected_snapshot_sha256),indent=2))
if __name__=='__main__':main()
