from pathlib import Path
import importlib.util,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;PUB=HERE.parent.parents[1]/'publication'
spec=importlib.util.spec_from_file_location('publicscope',PUB/'check_public_downloads.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.ROOT=HERE.parent/'temp/public_metadata_scope';m.ROOT.mkdir(exist_ok=True)
build=json.loads((PUB/'BUILD_RECEIPT.json').read_text());expected=json.loads((PUB/'zenodo-deposit.json').read_text())
pub={'state':'published','id':999999,'doi':'10.0000/offline.fixture','title':expected['metadata']['title']}
for n,v in [('BUILD_RECEIPT.json',build),('PUBLICATION_RECEIPT.json',pub),('zenodo-deposit.json',expected)]:
 (m.ROOT/n).write_text(json.dumps(v))
actual={'id':pub['id'],'doi':pub['doi'],'metadata':{'title':pub['title'],'creators':[{'name':'Wrong creator'}],'license':{'id':'wrong-license'},'version':'wrong-version','publication_date':'1900-01-01','description':'AI disclosure removed'},'files':[]}
responses={}
for k in ['pdf','verification_zip']:
 item=build[k];url='https://offline.invalid/'+k;actual['files'].append({'key':item['path'],'links':{'self':url}});responses[url]=(PUB/item['path']).read_bytes()
responses['https://zenodo.org/api/records/'+str(pub['id'])]=json.dumps(actual).encode()
m.fetch=lambda url,limit:responses[url]
m.main()
result={'status':'CONFIRMED_SCOPE_LIMIT','external_calls':0,'all_expected_artifact_bytes_kept':True,'altered_metadata_fields_accepted':['creators','license','version','publication_date','description'],'identity_verified_is_correct_but_exact_metadata_is_not_checked':True,'script_sha256':__import__('hashlib').sha256((PUB/'check_public_downloads.py').read_bytes()).hexdigest()}
(HERE/'public_metadata_scope.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
