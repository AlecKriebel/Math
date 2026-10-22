#!/usr/bin/env python3
"""Portable integrity checker; requires outside anchors, makes no theorem claim.

Deploy this file as publication/verification/verify.py. Registry schemas are
explicit: absolute-path fields in historical receipts are never followed.
"""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parent
PR, PROBLEM = 1268, 10900050
ORIGINAL = 'cecd7da6e8b5bb84b4294e169d940189b269a956'
BRANCH = 'research/10900050-prime-difference-counterexample'
BODY = '80632e6a02d184fe4a5818161493a40b57af96a03a2cfd2f99e912c1e80d5162'
BASE = 'unsolved_math_prioritization/attempts/10900050'
NAMES = {'ACCEPTANCE.json','ACCEPTANCE_REPORT.md','AUDIT_MANIFEST.json','EDITORIAL_MAP.json','LITERATURE_CHECK.json','PROOF.md','PUBLIC_MANIFEST.json','README.md','RESEARCH_LOG.md','SOURCE_MANIFEST.json'}
PROSE = {'ACCEPTANCE_REPORT.md','PROOF.md','README.md','RESEARCH_LOG.md'}
STRUCTURED = {'ACCEPTANCE.json','AUDIT_MANIFEST.json','EDITORIAL_MAP.json','LITERATURE_CHECK.json','SOURCE_MANIFEST.json'}
FIELDS = {'title','upload_type','publication_type','description','creators','access_right','license','version','publication_date','keywords','related_identifiers'}
SCHEMAS = {('files','relative_path','size_bytes'),('files','relative_path','bytes'),('authored_files','relative_path','bytes'),('authored_artifacts','relative_path','bytes'),('entries','path','bytes'),('entries','relative_path','bytes'),('entries','file','bytes'),('authored_files','path','bytes'),('files','path','bytes'),('all_authored_content_files','path_relative_to_authored_root','bytes')}


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
    cursor=root
    for part in PurePosixPath(raw).parts:
        if cursor.is_dir():
            matches=[entry.name for entry in cursor.iterdir() if entry.name.casefold()==part.casefold()]
            need(len(matches)<=1 and (not matches or matches[0]==part),'case mismatch or collision '+raw)
        cursor=cursor/part;need(not cursor.is_symlink(),'symlink path '+raw)
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
    need(metadata['title'].isascii() and metadata['description'].isascii(),'title/description require explicit ASCII text')
    need(not any(c in metadata['title'] for c in '<>'),'title must use words/stable notation, no angle signs')
    description=metadata['description'];need(not any(c in description for c in '<>') or re.fullmatch(r'(?:<p>[^<>]*</p>)+',description) is not None,'description must be angle-free plain text or paragraph HTML with stable entities and no raw internal less/greater signs')
    need(isinstance(metadata['creators'],list) and bool(metadata['creators']),'creators required')
    for creator in metadata['creators']:
        need(isinstance(creator,dict) and bool(creator.get('name')) and 'affiliation' in creator,'explicit creator name and affiliation (null allowed) required')
    need(isinstance(metadata['keywords'],list) and isinstance(metadata['related_identifiers'],list),'metadata list fields required')
    for item in metadata['related_identifiers']:
        need(isinstance(item,dict) and bool(item.get('identifier')) and bool(item.get('relation')) and bool(item.get('scheme')),'explicit related identifier schema required')
        if item['scheme']=='doi': need(re.fullmatch(r'10\.\d{4,9}/\S+',item['identifier']) is not None and not item['identifier'].startswith('https:'),'DOI identifier must be bare canonical DOI')
    return metadata

def registry_schema(item):
    fields={'path','base','entries_key','path_key','size_key','sha256','role'}
    need(isinstance(item,dict) and set(item) in [fields,fields|{'path_mode'}],'explicit registry role and exact schema required')
    triple=tuple(item[k] for k in ['entries_key','path_key','size_key'])
    need(triple in SCHEMAS and triple[0] not in {'members','authored_members','authored_outputs'},'supported explicit relative membership schema required')
    need(item.get('path_mode','relative')=='relative','absolute input paths are never authored membership')
    need(item['role'] in {'math','priority','workflow','documentary'},'explicit family role required')
    return 'relative'

def manifest_member_name(registry, entry, manifest):
    # Only the exact declared relative member key is selected. Historical
    # absolute inputs/source receipts in unused fields are never followed.
    registry_schema(registry);return safe(entry.get(registry['path_key']))

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
        need(any(item['role']=='math' for item in registry),'explicit mathematical authored evidence required')
        need(any(item['role']=='priority' for item in registry),'explicit priority authored evidence required')
    return checked

def authenticate_snapshot(root, snapshot):
    need(snapshot.get('pr')==PR and snapshot.get('problem_id')==PROBLEM and snapshot.get('head')==ORIGINAL and snapshot.get('branch')==BRANCH and snapshot.get('body_sha256')==BODY,'original snapshot identity differs')
    entries=snapshot.get('files',[])
    need(len(entries)==10 and {e['path'] for e in entries}=={BASE+'/'+n for n in NAMES},'exact original ten-file scope required')
    for entry in entries:
        path=member(root,Path(entry['path']).name);check_binding(path,entry)
        data=path.read_bytes();need(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['blob'],'original Git blob differs')
    authenticate_edition(root)

def authenticate_edition(root):
    need({p.name for p in root.iterdir()}==NAMES,'edition must contain exactly ten regular files')
    manifest=json.loads(member(root,'PUBLIC_MANIFEST.json').read_text());entries=manifest.get('files')
    need(manifest.get('problem_id')==PROBLEM and manifest.get('file_count')==10,'exact PUBLIC_MANIFEST target/file_count required')
    need(isinstance(entries,list) and len(entries)==9 and {e.get('path') for e in entries}==NAMES-{'PUBLIC_MANIFEST.json'},'nine nonself files/path/bytes/sha256 rows required')
    for entry in entries:
        need(set(entry)=={'path','bytes','sha256'},'exact PUBLIC_MANIFEST row schema required')
        check_binding(member(root,entry['path']),entry)

def authenticate_current(root,context,original):
    authenticate_edition(root)
    if context['edition_mode']=='preserve_submitted':
        for name in NAMES:need(member(root,name).read_bytes()==member(original,name).read_bytes(),'preserved current original differs '+name)
    else:
        for name,text in context['edition_text'].items():need(member(root,name).read_text()==text,'explicit current prose differs')
        for name,obj in context['structured_records'].items():need(json.loads(member(root,name).read_text())==obj,'explicit current structured record differs')

def load_context(audit, document_root=None, evidence_root=None):
    evidence_root=audit if evidence_root is None else evidence_root
    context=json.loads(member(audit,'CURRENT_PR1268_CONTEXT.json').read_text())
    keys={'edition_mode','schema','pr','problem_id','original_head','original_branch','original_body_sha256','title','expected_pdf_pages','source_date_epoch','edition_text','structured_records','disclosures','metadata','publication_text','tracker','authored_freezes','portable_files','diagnostic_replays','gate_bindings','document_bindings'}
    need(set(context)==keys,'current context exact keys required')
    need(context['schema']=='math-pr1268-current-context-v1' and context['pr']==PR and context['problem_id']==PROBLEM and context['original_head']==ORIGINAL and context['original_branch']==BRANCH and context['original_body_sha256']==BODY,'current context identity differs')
    need(type(context['expected_pdf_pages']) is int and context['expected_pdf_pages']>0,'actual expected PDF page count required')
    need(isinstance(context['source_date_epoch'],str) and context['source_date_epoch'].isdigit(),'explicit reproducible build stamp required')
    need(context['edition_mode'] in {'preserve_submitted','explicit_current'},'explicit current edition mode required')
    if context['edition_mode']=='preserve_submitted':
        need(context['edition_text']=={} and context['structured_records']=={},'preserved submission mode cannot invent current prose/records')
    else:
        need(set(context['edition_text'])==PROSE and all(isinstance(t,str) and t.strip() for t in context['edition_text'].values()),'exact four explicit current prose records required')
        need(set(context['structured_records'])==STRUCTURED and all(isinstance(t,dict) and t for t in context['structured_records'].values()),'exact five explicit current structured records required')
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
    with tempfile.TemporaryDirectory(prefix='prime-difference-finite-replay-') as folder:
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
    need(digest(root/'provenance/CURRENT_PR1268_CONTEXT.json')==expected_context_sha256,'outside context anchor differs')
    need(digest(root/'provenance/SUBMITTED_SNAPSHOT.json')==expected_snapshot_sha256,'outside snapshot anchor differs')
    manifest=json.loads((root/'MANIFEST.json').read_text());need(manifest.get('schema')=='prime-difference-counterexample-verification-v1','root manifest target/schema differs');seen=set()
    for entry in manifest['files']:
        raw=safe(entry['path']);need(raw!='MANIFEST.json' and raw not in seen,'duplicate/self root member');seen.add(raw);check_binding(member(root,raw),entry)
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    need(actual==seen|{'MANIFEST.json'},'unlisted/missing archive member')
    context=load_context(root/'provenance',evidence_root=root)
    need(context['schema']=='math-pr1268-current-context-v1' and context['pr']==PR and context['problem_id']==PROBLEM and context['original_head']==ORIGINAL,'portable context target differs')
    nested=authenticate_nested_manifests(root,context['authored_freezes'])
    for filename,key in [('MATH_GATE.json','math_gate_sha256'),('PRIORITY_ADJUDICATION.json','priority_adjudication_sha256'),('SUBMITTED_SNAPSHOT.json','submitted_snapshot_sha256')]:need(digest(root/'provenance'/filename)==context['gate_bindings'][key],'portable gate anchor differs')
    authenticate_snapshot(root/'original_submitted',json.loads((root/'provenance/SUBMITTED_SNAPSHOT.json').read_text()));authenticate_current(root/'current_edition',context,root/'original_submitted')
    for name,text in context['edition_text'].items():need((root/'current_edition'/name).read_text()==text,'current explicit prose differs')
    for name,obj in context['structured_records'].items():need(json.loads((root/'current_edition'/name).read_text())==obj,'current explicit structured record differs')
    for entry in context['portable_files']:check_binding(member(root,entry['path']),entry)
    for raw,key in [('manuscript/main.tex','source_sha256'),('provenance/COMPILE_RECEIPT.json','compile_receipt_sha256'),('provenance/LAYOUT_VERIFICATION.json','layout_receipt_sha256')]:need(digest(root/raw)==context['document_bindings'][key],'portable document assurance differs')
    checks=replay_diagnostics(root,context)
    for entry in manifest['files']:check_binding(member(root,entry['path']),entry)
    return {'status':'PASS','authenticated_members':len(seen),'submitted_files':10,'current_edition_files':10,'nested_manifests':nested,'finite_diagnostic_replays':checks,'limits':'Integrity and explicitly scoped finite diagnostics only. Written proofs and actual mathematical/priority adjudication remain separate. Read/retained source inventories are receipts; omitted third-party source bodies and omitted historical code are not reauthenticated or replayed.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['manifest','context','snapshot']:parser.add_argument('--expected-'+name+'-sha256',required=True)
    args=parser.parse_args();print(json.dumps(verify(ROOT,args.expected_manifest_sha256,args.expected_context_sha256,args.expected_snapshot_sha256),indent=2))
if __name__=='__main__':main()
