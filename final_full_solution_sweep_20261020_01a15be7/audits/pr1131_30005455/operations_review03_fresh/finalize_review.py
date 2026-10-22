#!/usr/bin/env python3
"""Read-only final validation and self-contained review/custody sealing."""
import contextlib,hashlib,io,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent;driver=HERE/'review_driver.py'
ns={'__file__':str(driver),'__name__':'fresh_review_driver'};exec(compile(driver.read_bytes(),str(driver),'exec'),ns)
OPS=ns['OPS'];AUDIT=ns['AUDIT'];REPO=ns['REPO'];pin=ns['pin'];sha=ns['sha'];need=ns['need'];stamp=ns['stamp'];dump=ns['dump'];strict=ns['strict']
load=ns['load']();c=load('ops_common');c.zenodo.token_for=ns['blocked'];check=load('check_package')
sys.argv=['check_package','--verify-preparation'];out=io.StringIO()
with contextlib.redirect_stdout(out):r=check.main()
need(r is None or r==0,'Final complete checker failed')
manifestbytes=(OPS/'OPERATIONS_MANIFEST.json').read_bytes();manifest=strict(manifestbytes)
public_pins={n:pin((OPS/n).read_bytes()) for n in manifest['files']};need(public_pins==manifest['files'],'Final public closure byte drift')
dependency=strict((OPS/'DEPENDENCY_PINS.json').read_bytes());need(all(pin((REPO/n).read_bytes())==p for n,p in dependency.items()),'Final shared dependency drift')
mirror=HERE/'private/fixture/Math';receipt=strict((mirror.parent/'COPY_RECEIPT.json').read_bytes())
need(all(pin((mirror/n).read_bytes())==p for n,p in receipt['files'].items()),'Final fixture drift')
need(not ns['ATTEMPTS'],'External entry point attempted')
validation={'at':stamp(),'complete_source_checker_main_return':r,'complete_source_checker_stdout':out.getvalue(),'operations_manifest':pin(manifestbytes),'all_public_operations_files':public_pins,'shared_dependency':dependency,'frozen_science_sha256':sha((AUDIT/'PACKAGE_FREEZE_01.json').read_bytes()),'scientific_clearance_sha256':sha((AUDIT/'ROOT_SCIENTIFIC_CLEARANCE.json').read_bytes()),'source_manifest_sha256':sha((AUDIT/'publication/SOURCE_MANIFEST.json').read_bytes()),'copied_inputs_unchanged':len(receipt['files']),'original_runtime_files':[p.name for p in (OPS/'runtime').glob('*')],'external_attempts':ns['ATTEMPTS'],'external_mutations':0,'publication_ready':False,'scientific_package_changed':False}
dump(HERE/'FINAL_INPUT_VALIDATION.json',validation)
private=HERE/'private';entries=[['private/','directory']];files=0;bytes_=0
for p in sorted(private.rglob('*'),key=lambda p:p.relative_to(HERE).as_posix()):
    need(not p.is_symlink(),'Private review symlink')
    n=p.relative_to(HERE).as_posix()
    if p.is_dir():entries.append([n,'directory'])
    else:
        need(p.is_file(),'Private review nonregular');b=p.read_bytes();entries.append([n,'file',pin(b)]);files+=1;bytes_+=len(b)
custody={'at':stamp(),'root':'private/','files':files,'directories':len(entries)-files,'logical_bytes':bytes_,'sorted_full_tree_sha256':sha(json.dumps(entries,ensure_ascii=False,separators=(',',':')).encode()),'contains_raw_original_account_and_ledger_copies':True,'contains_synthetic_clearances_and_intents':True,'credentials_copied':False,'publication_allowed':False,'must_remain_ignored':True}
dump(HERE/'PRIVATE_EVIDENCE_CUSTODY.json',custody)
log=HERE/'RESEARCH_LOG.md'
with log.open('a') as f:f.write('\n- '+stamp()+': Final complete checker main including preparation, manifest/row template and all scientific/proposal checks passed again; all original operation and shared-source pins and all131 reviewer fixture inputs remain exact. All26 archives independently verified. Three material omissions remain; operational clearance rejected. Review completion100%; overall research estimate79%. Public review seal and complete private byte/hash custody finalized. No external calls, messages or real mutations.\n')
sealed={}
for p in sorted(HERE.iterdir()):
    if p.name in {'MANIFEST.json','private','__pycache__'}:continue
    need(p.is_file() and not p.is_symlink(),'Unexpected public review file');sealed[p.name]=pin(p.read_bytes())
seal={'at':stamp(),'status':'REJECT_OPERATIONAL_CLEARANCE_MATERIAL_FINDINGS','operations_manifest_sha256':ns['OPS_SHA'],'bootstrap_sha256':ns['BOOT_SHA'],'files':sealed,'excluded':['MANIFEST.json','private/','__pycache__/'],'private_custody':custody,'material_findings':['F1_bare_resolver_port_scheme_confusion','F2_other_owned_record_same_target_concept_ignored','F3_raw_account_fields_discarded_before_identity_scan'],'review_completion_percent':100,'overall_research_completion_percent':79,'publication_ready':False,'zero_material_objection_requirement_met':False,'raw_private_evidence_publication_allowed':False,'external_mutations':0,'external_messages':0,'scientific_clearance_unchanged':True}
dump(HERE/'MANIFEST.json',seal)
print(json.dumps({'review_manifest':pin((HERE/'MANIFEST.json').read_bytes()),'report':pin((HERE/'REPORT.md').read_bytes()),'findings':pin((HERE/'FINDINGS.json').read_bytes()),'public_files':len(sealed),'private_files':files,'private_logical_bytes':bytes_,'material_findings':3,'publication_ready':False,'operations_unchanged':True},indent=2))
