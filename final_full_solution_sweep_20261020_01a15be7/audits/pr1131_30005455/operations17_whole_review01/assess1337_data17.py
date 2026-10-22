"""Bounded private1337 serialization DATA assessment; no normalization widened."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
text=(ROOT/'data17.py').read_text()
marker="    # API-contract compatibility is tested independently of any live workbook."
insert="""    other=R.parent/'pr1337_30004534';action=other/'root_publication_action01'
    mpath=other/'publication_preparation_02/release/zenodo-deposit.json';read(mpath)
    md,up=c.zenodo.load_manifest(mpath)
    for e in up:read(e['path'])
    results=[]
    for tag,files,pub,names13 in [
      ('initial',['LEGACY_AFTER_CREATE','NATIVE_DRAFT_AFTER_CREATE','FINALIZED_AFTER_CREATE'],False,set()),
      ('PDF',['AFTER_PDF_LEGACY','AFTER_PDF_NATIVE','AFTER_PDF_FINALIZED'],False,{e['name']for e in up if e['name'].endswith('.pdf')}),
      ('ZIP',['BEFORE_PUBLISH01_LEGACY','BEFORE_PUBLISH01_NATIVE','BEFORE_PUBLISH01_FINALIZED'],False,{e['name']for e in up}),
      ('published',['AFTER_PUBLISH_LEGACY','AFTER_PUBLISH_NATIVE','AFTER_PUBLISH_FINALIZED_FILES'],True,{e['name']for e in up})]:
        l,n,f=[json.loads(read(action/(name+'.json')))for name in files]
        for role,v in [('legacy',l),('native',n),('file_collection',f)]:policy.validate_types(role,v)
        phase.prepare(l,n,f,l['id'],pub,md)
        try:old.validate_target(l,n,f,md,up,l['id'],pub,names13)
        except Exception as error:full={'accepted':False,'error':str(error)}
        else:full={'accepted':True}
        results.append({'phase':tag,'all_three_views_actual':True,'typed_schema_and_complete_phase_root_identity_alias_validation':'PASS','full_package_policy':full})
    envelope=json.loads(read(action/'PUBLIC_RECORD_VERIFIED_CAPTURE.json'));policy.validate_types('public',envelope)
    read(action/'ROOT_EXACT_DESCRIPTION_SERIALIZATION_ADOPTION.json')
    (ROOT/'private/ACTUAL1337_SERIALIZATION_ASSESSMENT.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_frozen':bool(EXPECTED),'results':results,'public_exact_recursive_schema':'PASS','full_public_metadata_projection_not_claimed':True,'known_root_record_specific_description_adoption_not_generalized':True,'all_input_pins':PINS,'actual_requests_or_mutations':0,'target1131_readiness_or_authority':False},sort_keys=True,indent=2)+'\\n')
"""
need=marker in text
if not need:raise RuntimeError('Assessment insertion')
text=text.replace(marker,insert+marker)
text=text.replace("private/DATA_RESULTS.json","private/ACTUAL1337_BASE_DATA_RESULTS.json")
exec(compile(text,str(ROOT/'data17.py')+'[1337-data-assessment]','exec',dont_inherit=True,optimize=0),{'__file__':str(ROOT/'data17.py'),'__name__':'data1337'})
print((ROOT/'private/ACTUAL1337_SERIALIZATION_ASSESSMENT.json').read_text()[:1800])
