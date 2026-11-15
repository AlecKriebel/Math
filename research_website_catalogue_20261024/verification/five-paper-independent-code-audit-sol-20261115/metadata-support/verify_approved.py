#!/usr/bin/env python3
"""New read-only approved-input metadata checker; never reads target stage.

This is not a scientific/content verifier. It only hashes protected files and
compares the literal approved metadata objects with their current originals.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

BASE=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=Path(__file__).resolve().parent
AUTHORITY_SHA256='4af1b271c9f678899b17504dc2b6678fba2ae11f0a6609da719a543dcc73b4f4'


def strict(a,b):
    if type(a) is not type(b):
        return False
    if isinstance(a,dict):
        return list(a)==list(b) and all(strict(a[k],b[k]) for k in a)
    if isinstance(a,list):
        return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate():
    checks=[];rejections=[]
    def check(value,name):
        if not value:raise RuntimeError(name)
        checks.append(name)
    approved=load(OWN/'APPROVED_METADATA.json')
    guard=load(OWN/'INPUT_MANIFEST.json')
    for item in guard['files']:
        f=Path(item['path'])
        check(f.is_file() and f.stat().st_size==item['bytes'] and sha(f)==item['sha256'],
              'Immutable source/approved file: '+str(f.relative_to(BASE)))
    authority_file=Path(approved['authority_path'])
    check(sha(authority_file)==AUTHORITY_SHA256==approved['authority_sha256'],
          'Assigned five-record adoption authority hash')
    check(strict(load(authority_file),approved['whole_literal_root_adoption_original']),
          'Whole exact root adoption object')
    check([r['record_id'] for r in approved['records']]
          ==['23441890','23174283','23430498','23149775','23331080'],
          'Exactly the approved five records;118 excluded')
    asset_count=0;verdict_count=0;transport_count=0
    for record in approved['records']:
        rid=record['record_id'];q=BASE/'papers'/rid;source=q/'sources'
        ready=load(Path(record['source_ready_path']))
        check(sha(Path(record['source_ready_path']))==record['source_ready_sha256']
              and strict(ready,record['whole_literal_source_ready_original']),rid+' whole original SOURCE_READY')
        for config in record['approved_configuration_objects']:
            b=config['approved_binding_original'];f=BASE/b['path']
            check(f.stat().st_size==b['bytes'] and sha(f)==b['sha256']
                  and strict(load(f),config['whole_literal_original_object']),
                  rid+' whole frozen approved configuration '+f.name)
        rootfile=Path(record['root_science_authority_path'])
        check(sha(rootfile)==record['root_science_authority_sha256']
              and strict(load(rootfile),record['whole_literal_root_science_authority_original']),rid+' whole root scientific authority')
        raw_record=Path(ready['native_record_body_path']) if 'native_record_body_path' in ready else source/'record.raw.json'
        version_file=source/('versions.page-001.raw.json' if 'native_record_body_path' in ready else 'versions.raw.json')
        for field,f in [('whole_literal_native_record_original',raw_record),
                        ('whole_literal_native_latest_original',source/'latest.raw.json'),
                        ('whole_literal_native_versions_original',version_file)]:
            check(strict(load(f),record[field]),rid+' whole native object '+f.name)
        if record['whole_literal_native_files_original'] is not None:
            check(strict(load(source/'files.raw.json'),record['whole_literal_native_files_original']),rid+' whole file-list object')
        native=record['whole_literal_native_record_original'];versions=record['whole_literal_native_versions_original']
        check(native['metadata']['version']==record['API_version']
              and native['metadata']['publication_date']==record['original_publication_date']
              and native['created']==record['created_original']
              and native['updated']==record['updated_original'],rid+' exact date/version/created/updated')
        check(type(native['swh']) is dict and native['swh']=={}
              and versions['hits']['hits'][0]['swh'] is None,rid+' empty-object versus null preserved')
        transports=record['whole_literal_transport_objects_original']
        if rid in ['23441890','23174283']:
            for w in transports:
                f=Path(w['path'])
                check(sha(f)==w['sha256'] and strict(load(f),w['original']),rid+' complete mixed transport '+f.name)
        elif rid=='23430498':
            for w in transports:
                check(strict(load(source/w['filename']),w['whole_original_object']),rid+' complete mixed transport '+w['filename'])
        elif rid=='23149775':
            for w in transports:
                f=Path(w['original_source_path'])
                check(sha(f)==w['sha256'] and strict(load(f),w['original_object']),rid+' complete mixed transport '+f.name)
        else:
            check(strict(load(Path(ready['actual_transport_receipt_path'])),transports),rid+' actual five api-receipts objects')
        transport_count+=len(transports)
        for w in record['whole_three_literal_scientific_verdicts']:
            f=Path(w['path'])
            check(sha(f)==w['sha256'] and strict(load(f),w['whole_literal_original_object']),rid+' full scientific literal verdict '+w['lane'])
            verdict_count+=1
        for asset,raw in zip(record['approved_assets'],native['files']):
            f=Path(asset['actual_native_path']);descriptor=asset['original_native_asset_descriptor']
            check(f.stat().st_size==asset['bytes']==raw['size'] and sha(f)==asset['sha256']
                  and hashlib.md5(f.read_bytes()).hexdigest()==raw['checksum'].split(':')[1]
                  and strict(descriptor['original_api_file_object'],raw),rid+' complete native asset '+raw['key'])
            asset_count+=1
        check([x['key'] for x in native['files']]==record['native_asset_order'],rid+' original asset order')
        code=record['approved_code_license_policy']['explicit_approved_code_license']
        expected={'23441890':'CC BY 4.0','23174283':None,'23430498':'CC BY 4.0','23149775':'MIT','23331080':None}[rid]
        check(code==expected and type(code) is type(expected),rid+' exact approved code-license field')
    override_file=Path(approved['Dlab_exact_one_href_override_path'])
    override=approved['whole_literal_Dlab_override_original']
    check(sha(override_file)==approved['Dlab_exact_one_href_override_sha256']
          and strict(load(override_file),override),'Exact separately adopted one-href override')
    check(override['old_href']=='https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-1.pdf'
          and override['new_href']=='https://kourovkanotebookorg.wordpress.com/'
          and override['scientific_sentence_delta'] is None,'Only approved Dlab hyperlink target changes')
    for name,a,b in [
        ('bool/int coercion',True,1),('empty-object/null coercion',{},None),
        ('empty-list/null coercion',[],None),('header-list/dictionary coercion',[['a','b']],{'a':'b'}),
        ('array ordering',[1,2],[2,1]),('dictionary key ordering',{'a':1,'b':2},{'b':2,'a':1})
    ]:
        if strict(a,b):raise RuntimeError('Type/order control survived: '+name)
        rejections.append(name)
    return {'status':'PASS_APPROVED_METADATA_BINDINGS_STAGE_UNREAD',
            'protected_files':len(guard['files']),'checks':len(checks),
            'approved_records':5,'whole_scientific_verdicts':verdict_count,
            'whole_native_transport_objects':transport_count,'complete_original_assets':asset_count,
            'small_type_order_controls_rejected':len(rejections),'controls':rejections,
            'target_stage_read':False,'record118_excluded':True,
            'network_browser_scientific_or_old_content_programs':False,
            'writes':False,'public_integration_authority':False}


if __name__=='__main__':
    print(json.dumps(validate(),indent=2))
