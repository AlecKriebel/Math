#!/usr/bin/env python3
"""Offline exact-path/exclusion probes; temporary fixtures are never published."""
import importlib.util,json,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('builder',ROOT/'build_preprint_package.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
def require(ok,message):
    if not ok:raise RuntimeError(message)
records=[]
with tempfile.TemporaryDirectory(prefix='builder_guards_') as tmp:
    package=Path(tmp).resolve()/'package';package.mkdir();builder.PACKAGE=package
    (package/'ordinary').mkdir();(package/'ordinary/item.txt').write_text('valid authored test payload')
    for name in ['venv','.venv','private_sources','private_cases','mutation_fixtures','.secrets','.zenodo-state','__pycache__']:
        (package/name).mkdir();(package/name/'item.txt').write_text('generated private test fixture')
    require(builder.selected_path('ordinary/item.txt')==package/'ordinary/item.txt','Valid canonical payload rejected');records.append({'case':'valid_canonical','accepted':True})
    for name in ['venv/item.txt','.venv/item.txt','private_sources/item.txt','private_cases/item.txt','mutation_fixtures/item.txt','.secrets/item.txt','.zenodo-state/item.txt','__pycache__/item.txt','ordinary/item.pyc','ordinary//item.txt','ordinary/./item.txt','./ordinary/item.txt','ordinary/../ordinary/item.txt','../escape','/absolute','','a\\b','a\x00b','a\nb',True]:
        try:builder.selected_path(name)
        except RuntimeError as err:
            require(any(term in str(err) for term in ['Invalid selected','Noncanonical selected','Excluded selected']),'Unexpected incidental rejection');records.append({'case':repr(name),'intended_rejection':True})
        else:raise RuntimeError('Unsafe builder path accepted')
    (package/'link.txt').symlink_to('ordinary/item.txt');(package/'linked_dir').symlink_to('ordinary',target_is_directory=True)
    for name in ['link.txt','linked_dir/item.txt']:
        try:builder.selected_path(name)
        except RuntimeError as err:
            require('Symlink' in str(err),'Unexpected symlink rejection');records.append({'case':name,'intended_rejection':True})
        else:raise RuntimeError('Symlink accepted')
result={'all_passed':True,'exact_cases':len(records),'real_external_calls':0,'frozen_package_mutation':False,'cases':records}
print(json.dumps(result,indent=2,sort_keys=True))
