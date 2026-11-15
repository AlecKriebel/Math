"""Independent source/root-only freeze. No writer, website, Git, source imports, network or subprocess."""
from pathlib import Path,PurePosixPath
import hashlib,json,stat,datetime,os
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');D=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()

def read(p):
 p=Path(p);assert p.resolve()==p and stat.S_ISREG(p.lstat().st_mode)
 assert 'supported-cycle-focal-private-stage-sol-20261115' not in p.parts and '.git' not in p.parts
 assert p.is_relative_to(P)
 return p.read_bytes()
def pin(p):
 b=read(p);return {'path':str(p),'bytes':len(b),'SHA256':H(b)}
def checked(p,r):
 b=read(p);assert len(b)==r['bytes'] and H(b)==r['SHA256'];return b
def write(n,x):
 with open(D/n,'x') as f:json.dump(x,f,indent=2,ensure_ascii=False);f.write('\n')
def copy(p,rel):
 b=read(p);q=D/rel;q.parent.mkdir(parents=True,exist_ok=True)
 with open(q,'xb') as f:f.write(b)
 return {'original':pin(p),'literal_copy':pin(q)}
def extent(root):
 files=[];dirs=[]
 assert root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode)
 for p in root.rglob('*'):
  mode=p.lstat().st_mode;assert p.resolve()==p and (stat.S_ISREG(mode) or stat.S_ISDIR(mode))
  (files if stat.S_ISREG(mode) else dirs).append(p.relative_to(root).as_posix())
 return sorted(files),sorted(dirs)

def main():
 with open(D/'.gitignore','x') as f:f.write('/inputs/\n')
 (D/'inputs').mkdir();(D/'EXPECTED_MAINS').mkdir()
 roots=[];copies=[];namespaces=[];expected=[];all_original_bindings={}
 for rid,root_name,h,size in [('23578142','root-editorial-23578142-20261115.json','97d56a98f09193fc57734f494f049e4223df5a0ec99ebd50865ad181cba80af5',32540),('23306203','root-editorial-23306203-20261115.json','8d1bf740eaa8b686ef953a9ba83603459e27229be854ded0156a3a523162dc95',32820)]:
  root_path=P/'verification'/root_name;rb=read(root_path);assert len(rb)==size and H(rb)==h;root=json.loads(rb);roots.append(copy(root_path,'inputs/'+root_name))
  assert root['root_full_copy_config_code_adopted'] is True and root['private_stage_preparation_authorized'] is True and root['production_installation_authorized'] is False
  E=P/'papers'/rid/'reviews/editorial';S=P/'papers'/rid/'sources'
  seal_row=root.get('owner_final_seal',root.get('editorial_final_seal'));seal=json.loads(checked(E/'SEAL.json',seal_row));mb=checked(E/'MANIFEST.json',seal['manifest']);manifest=json.loads(mb)
  rows=manifest['payloads'];assert isinstance(rows,dict)
  files,dirs=extent(E);assert files==sorted(list(rows)+['MANIFEST.json','SEAL.json']) and dirs==manifest['directories']
  for name,row in rows.items():checked(E/name,row)
  binding_rows=root.get('root_read_artifact_bindings',root.get('root_current_and_history_artifact_bindings'))
  for row in binding_rows:checked(Path(row['path']),row)
  for root_dir in [S,E]:
   files,dirs=extent(root_dir);snap=[]
   for n in files:
    row=pin(root_dir/n);snap.append(row);all_original_bindings[row['path']]=row
   namespaces.append({'path':str(root_dir),'files':files,'directories':dirs,'whole_file_bindings':snap})
  names=['PUBLIC_COPY.md','PUBLIC_MAIN.html','publication.json','promotion.json','RIGHTS_AND_IDENTITY.json','SCHOLARLY_METADATA.json','SCHEMA_ADAPTER.json','PUBLICATION_REQUIREMENTS.json','citation.bib','CUSTOM_VERDICT.json','REPORT.md','SEAL.json','MANIFEST.json','READ_LEDGER.json','AUTHORING_RECEIPT.json','WHOLE_AUTHORING_COMPARISON.json','CODE_MANIFEST.json','PRIMARY_SCOPE_AND_EDITION_LIMITS.json','PROTECTED_INPUTS.json','SOURCE_PROTOCOL_BINDINGS.json','public-sections.json','history/first-authoring/HISTORY_RECEIPT.json']
  names += ['ORIGINAL_ABSTRACT.tex'] if rid=='23578142' else ['ORIGINAL_PRINTED_ABSTRACT.tex','NATIVE_DEPOSIT_DESCRIPTION.html']
  for n in names:copies.append(copy(E/n,'inputs/'+rid+'/editorial/'+n))
  copies.append(copy(E/'PUBLIC_MAIN.html','EXPECTED_MAINS/'+rid+'.html'))
  for n in ['SOURCE_READY.json','SOURCE_READY_SEAL.json','SOURCE_READY_MANIFEST.json','SOURCE_READY_CLOSURE.json','record.response.body','latest.response.body','versions-page001.response.body','files.response.body','ALL_TRANSPORT_RECEIPTS.json','NATIVE_SCHEMA_TYPES.json','NATIVE_IDENTITY_MATCH.json','ARCHIVE_CUSTODY.json','MANUSCRIPT_CUSTODY.json']:
   copies.append(copy(S/n,'inputs/'+rid+'/sources/'+n))
  config=json.loads(read(E/'publication.json'));scholar=json.loads(read(E/'SCHOLARLY_METADATA.json'));native=json.loads(read(S/'record.response.body'))
  assert config['abstract']==scholar['abstract'];assert config['native_assets_in_original_order']==config['source_binding'].get('native_assets_in_original_order',config['native_assets_in_original_order'])
  asset_rows=[]
  for a in config['native_assets_in_original_order']:
   checked(Path(a['path']),a);c=copy(Path(a['path']),'inputs/'+rid+'/assets/'+Path(a['path']).name);copies.append(c);asset_rows.append({'whole_original_native_object':a,'frozen_asset':c['literal_copy'],'public_relative_path':'research/'+config['slug']+'/'+Path(a['path']).name})
  main=read(E/'PUBLIC_MAIN.html');assert main.startswith(b'<main id="main">') and b'#view=FitH' in main and b'<iframe' in main and b'<object' not in main
  public_paths=['research/'+config['slug']+'/'+n for n in ['index.html',config['supplement_filename'],config['pdf_filename'],'citation.bib']]
  expected.append({'record_id':rid,'row':root['sheet_row'],'root_full_editorial_adoption':pin(root_path),'complete_unchanged_expected_MAIN':pin(D/'EXPECTED_MAINS'/ (rid+'.html')),'MAIN_allowed_transforms':[],'whole_original_publication_typed_object':config,'whole_original_scholarly_typed_object':scholar,'whole_original_rights_typed_object':json.loads(read(E/'RIGHTS_AND_IDENTITY.json')),'whole_original_public_sections':json.loads(read(E/'public-sections.json')),'whole_original_native_asset_objects_in_order':asset_rows,'original_native_API_file_array':native['files'],'full_printed_abstract':config['abstract'],'full_native_deposit_description_HTML':native['metadata']['description'],'printed_abstract_is_native_deposit_description':False,'native_version_field_present':'version' in native['metadata'],'native_version':native['metadata'].get('version'),'printed_version_field_present':config['printed_version_field_present'],'printed_version':config['printed_version'],'original_date':config['publication_date'],'expected_four_article_root_leaf_paths':public_paths,'complete_original_Bib':pin(D/'inputs'/rid/'editorial/citation.bib'),'historical_custom_verdicts_and_status_not_rewritten':True})
 write('SOURCE_ROOT_BINDINGS.json',{'schema':'independent-supported-cycle-focal-source-root-custody-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root_adoptions':roots,'whole_literal_copies':copies,'complete_original_namespaces':namespaces,'whole_distinct_original_bindings':list(all_original_bindings.values()),'website_Git_writer_native_or_scientific_programmes_executed_or_inspected':False})
 write('EXPECTED_SOURCE_OBJECTS.json',{'schema':'independent-supported-cycle-focal-complete-source-expectations-v1','records':expected,'source_objects_are_whole_typed_and_raw_copies_preserve_exact_order_types_nulls_absence_history':True,'no_source_or_science_defect_repair_or_narrowing_authorized':True})
 print(json.dumps({'root_adoptions':len(roots),'literal_copies':len(copies),'source_editorial_namespace_file_counts':[len(n['files']) for n in namespaces],'source_editorial_namespace_directory_counts':[len(n['directories']) for n in namespaces],'distinct_original_files':len(all_original_bindings),'complete_MAINs':[e['complete_unchanged_expected_MAIN'] for e in expected]},indent=2))
if __name__=='__main__':main()
