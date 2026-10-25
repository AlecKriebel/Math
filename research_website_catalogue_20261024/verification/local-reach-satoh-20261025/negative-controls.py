"""Publication-pipeline controls only; frozen sources are never changed."""
from pathlib import Path
from copy import deepcopy
from io import BytesIO
import contextlib, hashlib, json, runpy, shutil, sys, tempfile, zipfile

R=Path(__file__).resolve().parents[2]
O=Path(__file__).resolve().parent
S=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
sys.path.insert(0,str(R/'scripts'))
from published_assets import PublishedAssets, normalized_receipt_view

checks={}
def test(name,value):
    checks[name]=bool(value)
    if not value:raise ValueError(name)
def rejected(name,operation):
    try:operation()
    except (ValueError,KeyError):checks[name]=True
    else:raise ValueError('Bad input accepted: '+name)

rawbytes=(R/'papers/23431676/sources/receipt.json').read_bytes()
raw=json.loads(rawbytes);saved=deepcopy(raw)
view=normalized_receipt_view(raw)
test('assets_original_objects_retained',view['files']==raw['assets'])
view['files'][0]['name']='VIEW_ONLY_MUTATION'
test('view_is_independent_and_original_bytes_unchanged',raw==saved and (R/'papers/23431676/sources/receipt.json').read_bytes()==rawbytes)
test('files_schema_unchanged',normalized_receipt_view({'files':[{'name':'a'}]})['files']==[{'name':'a'}])
test('equal_dual_schema_accepted',normalized_receipt_view({'files':[{'name':'a'}],'assets':[{'name':'a'}]})['files']==[{'name':'a'}])
for i,bad in enumerate((None,[],{}, {'assets':None},{'assets':['bad']},{'files':{},'assets':[]},{'files':[],'assets':[{'name':'a'}]})):
    rejected('malformed_receipt_'+str(i),lambda bad=bad:normalized_receipt_view(bad))

with tempfile.TemporaryDirectory(prefix='receipt-control-',dir=O) as td:
    p=Path(td);buf=BytesIO()
    with zipfile.ZipFile(buf,'w') as z:z.writestr('control.txt','verified archive')
    data=buf.getvalue();(p/'control.zip').write_bytes(data)
    receipt={'assets':[{'name':'control.zip','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}]}
    resolver=PublishedAssets(p,receipt)
    test('missing_kind_authenticated_zip',resolver.additional_asset_kind({'filename':'control.zip'})=='zip')
    rejected('explicit_invalid_kind',lambda:resolver.additional_asset_kind({'filename':'control.zip','kind':'exe'}))
    rejected('explicit_null_kind',lambda:resolver.additional_asset_kind({'filename':'control.zip','kind':None}))
    rejected('explicit_mismatching_kind',lambda:resolver.additional_asset_kind({'filename':'control.zip','kind':'pdf'}))
    rejected('unbound_missing_kind',lambda:resolver.additional_asset_kind({'filename':'unbound.zip'}))
    (p/'control.zip').write_bytes(data+b'changed')
    rejected('missing_kind_does_not_bypass_identity',lambda:resolver.additional_asset_kind({'filename':'control.zip'}))
    (p/'control.zip').write_bytes(data)
    conflicting=deepcopy(receipt);conflicting['assets'][0]['filename']='different.zip'
    rejected('conflicting_receipt_name_aliases',lambda:PublishedAssets(p,conflicting))
    duplicate=deepcopy(receipt);duplicate['assets'].append(deepcopy(duplicate['assets'][0]))
    rejected('duplicate_receipt_assets',lambda:PublishedAssets(p,duplicate))
    (p/'control.txt').write_bytes(b'supported explicit text only')
    text_receipt={'files':[{'name':'control.txt','sha256':hashlib.sha256((p/'control.txt').read_bytes()).hexdigest()}]}
    text_resolver=PublishedAssets(p,text_receipt)
    rejected('unknown_suffix_not_inferred',lambda:text_resolver.additional_asset_kind({'filename':'control.txt'}))
    test('existing_explicit_text_kind_retained',text_resolver.additional_asset_kind({'filename':'control.txt','kind':'text'})=='text')
    (p/'fake.zip').write_bytes(b'not an archive')
    fake=PublishedAssets(p,{'assets':[{'name':'fake.zip','sha256':hashlib.sha256(b'not an archive').hexdigest()}]})
    rejected('recognized_suffix_needs_zip_content',lambda:fake.additional_asset_kind({'filename':'fake.zip'}))

configs={rid:json.loads((R/'papers'/rid/'publication.json').read_text()) for rid in ('23431676','23387442')}
cases={
 'reach-abstract':('23431676','<section id="abstract"><h2>Abstract</h2><p>Ordinary','<section id="abstract"><h2>Abstract</h2><p>Altered','abstract'),
 'reach-scope':('23431676','For finite nonempty loopless strongly connected directed multigraphs,','For finite nonempty loopless strongly connected directed simple graphs,','scope_complete'),
 'satoh-abstract':('23387442','<section id="abstract"><h2>Abstract</h2><p>Let','<section id="abstract"><h2>Abstract</h2><p>Altered','abstract'),
 'satoh-scope':('23387442','For every n≥4, the automorphism','For every n≥3, the automorphism','scope_complete'),
 'reach-pdf':('23431676',None,None,'pdf_filename'),
 'satoh-pdf':('23387442',None,None,'pdf_filename'),
}
mutations=[]
with tempfile.TemporaryDirectory(prefix='page-controls-',dir=O) as td:
    site=Path(td)
    for entry in S.iterdir():
        if entry.name!='research':(site/entry.name).symlink_to(entry,target_is_directory=entry.is_dir())
    research=site/'research';research.mkdir()
    for entry in (S/'research').iterdir():
        if entry.name in {c['slug'] for c in configs.values()}:shutil.copytree(entry,research/entry.name)
        else:(research/entry.name).symlink_to(entry,target_is_directory=entry.is_dir())
    for name,(rid,old,new,expected_check) in cases.items():
        c=configs[rid];page=research/c['slug']/'index.html';pdf=page.parent/c['pdf_filename']
        original=page.read_bytes() if old else pdf.read_bytes()
        if old:
            text=original.decode();test(name+'_mutation_present',text.count(old)==1);page.write_text(text.replace(old,new))
        else:pdf.write_bytes(original+b'\nCONTROL: byte identity intentionally changed\n')
        stem='negative-'+name;previous_argv=sys.argv[:]
        sys.argv=[str(R/'verification/final-content-check.py'),rid,'--site',str(site),'--output-dir',str(O),'--output-stem',stem]
        with (O/(stem+'.stdout.json')).open('w') as out,contextlib.redirect_stdout(out):
            try:runpy.run_path(str(R/'verification/final-content-check.py'),run_name='__main__')
            except SystemExit as e:code=e.code
            else:code=0
        sys.argv=previous_argv
        result=json.loads((O/(stem+'.json')).read_text())
        test(name+'_rejected',code==1 and result['status']=='ISSUES_FOUND' and result['papers'][rid]['checks'][expected_check] is False)
        mutations.append({'case':name,'exit_code':code,'expected_failed_check':expected_check,'issues':result['issues']})
        if old:page.write_bytes(original)
        else:pdf.write_bytes(original)

result={'status':'PASS','checks':checks,'passed_checks':len(checks),'page_mutations':mutations,'frozen_receipt_sha256':hashlib.sha256(rawbytes).hexdigest(),'frozen_inputs_modified':False,'scope':'Pipeline failure detection only; no scientific review or mathematical helper replay.'}
(O/'negative-controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'page_mutations':len(mutations)}))
