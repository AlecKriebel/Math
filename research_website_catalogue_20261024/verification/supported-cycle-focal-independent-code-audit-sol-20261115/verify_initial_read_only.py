"""Pure source/root-only initial custody. Never writer/site/Git/science imports or writes."""
from pathlib import Path,PurePosixPath
import hashlib,json,stat,sys
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');D=Path(__file__).resolve().parent
WRITER=P/'verification/supported-cycle-focal-private-stage-sol-20261115'
N=0;TYPED=0

def need(ok,label):
 global N
 N+=1
 if not ok:raise RuntimeError(label)
def read(p):
 p=Path(p)
 allowed=p.is_relative_to(D) or p.is_relative_to(P/'papers/23578142') or p.is_relative_to(P/'papers/23306203') or p in [P/'verification/root-editorial-23578142-20261115.json',P/'verification/root-editorial-23306203-20261115.json']
 need(allowed and p!=WRITER and WRITER not in p.parents and '.git' not in p.parts,'only approved own/source/root path before inspection')
 need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real source/root file')
 return p.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,r):
 b=read(p);need(len(b)==r['bytes'] and sha(b)==r['SHA256'],'whole exact buffer');return b
def obj(p):return json.loads(read(p))
def extent(root):
 need(root==D or root in [P/'papers/23578142/sources',P/'papers/23578142/reviews/editorial',P/'papers/23306203/sources',P/'papers/23306203/reviews/editorial'],'only approved namespace roots before listing')
 need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary source/root directory')
 files=[];dirs=[]
 for p in root.rglob('*'):
  mode=p.lstat().st_mode;need(p.resolve()==p and (stat.S_ISREG(mode) or stat.S_ISDIR(mode)),'all regular ordinary entries')
  (files if stat.S_ISREG(mode) else dirs).append(p.relative_to(root).as_posix())
 return sorted(files),sorted(dirs)
def typed(a,b):
 global TYPED
 TYPED+=1;need(type(a) is type(b),'whole original type')
 if isinstance(a,dict):
  need(list(a)==list(b),'whole key order')
  for k in a:typed(a[k],b[k])
 elif isinstance(a,list):
  need(len(a)==len(b),'whole array order/extent')
  for x,y in zip(a,b):typed(x,y)
 else:need(a==b,'whole original scalar/null')
def main():
 need(sys.argv[1:] in [[],['--preseal']],'bounded initial pure mode')
 b=obj(D/'SOURCE_ROOT_BINDINGS.json');e=obj(D/'EXPECTED_SOURCE_OBJECTS.json')
 for row in b['root_adoptions']:need(pin(row['original']['path'],row['original'])==pin(row['literal_copy']['path'],row['literal_copy']),'root adoption literal copy')
 for row in b['whole_literal_copies']:need(pin(row['original']['path'],row['original'])==pin(row['literal_copy']['path'],row['literal_copy']),'whole unmodified literal source copy')
 for ns in b['complete_original_namespaces']:
  f,d=extent(Path(ns['path']));need(f==ns['files'] and d==ns['directories'],'complete source/editorial files+directories')
  for r in ns['whole_file_bindings']:pin(r['path'],r)
 for rec in e['records']:
  rid=rec['record_id'];c=obj(D/'inputs'/rid/'editorial/publication.json')
  typed(rec['whole_original_publication_typed_object'],c)
  for key,name in [('whole_original_scholarly_typed_object','SCHOLARLY_METADATA.json'),('whole_original_rights_typed_object','RIGHTS_AND_IDENTITY.json'),('whole_original_public_sections','public-sections.json')]:typed(rec[key],obj(D/'inputs'/rid/'editorial'/name))
  main=pin(rec['complete_unchanged_expected_MAIN']['path'],rec['complete_unchanged_expected_MAIN'])
  need(main==read(D/'inputs'/rid/'editorial/PUBLIC_MAIN.html') and main.startswith(b'<main id="main">') and b'<iframe' in main and b'#view=FitH' in main,'complete expected MAIN no transform')
  native=obj(D/'inputs'/rid/'sources/record.response.body');typed(rec['original_native_API_file_array'],native['files'])
  need(rec['full_printed_abstract']==c['abstract'] and rec['full_native_deposit_description_HTML']==native['metadata']['description'],'whole distinct abstract/description')
  need(rec['MAIN_allowed_transforms']==[],'no MAIN transformations permitted')
 if not sys.argv[1:]:
  sb=read(D/'INITIAL_SEAL.json');s=json.loads(sb);mb=read(D/'INITIAL_MANIFEST.json');need(sha(mb)==s['MANIFEST_SHA256'],'same initial manifest buffer')
  m=json.loads(mb);names=[]
  for row in m['files']:
   p=PurePosixPath(row['path']);need(str(p)==row['path'] and not p.is_absolute() and '..' not in p.parts,'exact own path');pin(D/str(p),row);names.append(row['path'])
  f,d=extent(D);need(f==sorted(names+['INITIAL_MANIFEST.json','INITIAL_SEAL.json']) and d==m['directories'],'complete initial own file/directory extent')
  need(m['exact_root_terminal_exclusions']==['INITIAL_MANIFEST.json','INITIAL_SEAL.json'] and m['future_subtree_exclusions']==[],'exact root terminals only')
 print(json.dumps({'status':'PASS_INDEPENDENT_SOURCE_ROOT_ONLY_INITIAL_CUSTODY','mode':'preseal' if sys.argv[1:] else 'sealed-initial','checks':N,'typed_objects_or_scalars':TYPED,'source_editorial_namespace_files':[len(n['files']) for n in b['complete_original_namespaces']],'whole_original_files':len(b['whole_distinct_original_bindings']),'complete_MAINs_unchanged':True,'new_writer_website_real_git_baseline_or_scientific_campaign_inspected_or_executed':False,'publication_authority':False},sort_keys=True))
if __name__=='__main__':main()
