#!/usr/bin/env python3
"""Independent known-target record/concept family lead falsification."""
import json,pathlib
P=pathlib.Path(__file__).resolve().parent;driver=P/'review_driver.py'
ns={'__file__':str(driver),'__name__':'fresh_review_driver'};exec(compile(driver.read_bytes(),str(driver),'exec'),ns)
mirror=P/'private/fixture/Math';ops=mirror/ns['OPS'].relative_to(ns['REPO']);loader=ns['load'](ops)
m={n:loader(n) for n in ['ops_common','collect_live','integrate_remote','native_policy','publish_and_ledger','full_controls']}
c=m['ops_common'];live=m['collect_live'];f=m['full_controls'];pub=m['publish_and_ledger']
c.zenodo.token_for=lambda *a:'OFFLINE_SENTINEL_NO_CREDENTIAL';c.zenodo.doi_status=lambda *a:{'status':'offline'}
out=[]
for kind in ['shared_concept','explicit_target_DOI','top_level_alias']:
    root=P/'private'/('knownfamily_final_'+kind);rt=root/'runtime';pr=root/'private';rt.mkdir(parents=True);pr.mkdir()
    for mod in m.values():
        if hasattr(mod,'RUNTIME'):mod.RUNTIME=rt
        if hasattr(mod,'PRIVATE'):mod.PRIVATE=pr
    c.zenodo.STATE_DIR=root/'.zenodo-state';w=f.World(ops,m)
    cl=ns['strict']((ops/'ROOT_OPERATIONAL_CLEARANCE.example.json').read_bytes());cl.update(operations_manifest_sha256=ns['OPS_SHA'],bootstrap_sha256=ns['BOOT_SHA'],publication_ready=True,unresolved_operational_findings=[],root_complete_reports_read_and_all_seals_verified=True,allowed_actions=['integrate','pr-description','ready','merge','stage','publish','ledger'],instructions='SYNTHETIC REVIEW FIXTURE ONLY')
    ns['dump'](rt/'ROOT_OPERATIONAL_CLEARANCE.json',cl);w.clearance_sha=ns['sha']((rt/'ROOT_OPERATIONAL_CLEARANCE.json').read_bytes())
    with w.installed():w.through_merge();pub.lifecycle(w.args('stage'))
    record=next(r for r in w.accounts if r['id']!=23408971 and not any(live.semantic(t) for t in live.strings(live.projection(r))))
    changed_id=record['id']
    if kind=='shared_concept':record['conceptrecid']='778';record['conceptdoi']='10.5281/zenodo.778'
    elif kind=='explicit_target_DOI':record['metadata']['references']=['https://doi.org/10.5281/zenodo.777']
    else:record['links']['review_pointer']='https://ordinary.invalid/?r=//shortdoi.org/abc'
    with w.installed():
        try:
            gate,records,rows=live.collect('before_publish',w.git.head,777,cleared=c.clearance(w.clearance_sha,ns['OPS_SHA']));accepted=True;error=None;leads=[e['id'] for e in gate['account_leads']];targetfamily=gate['family_ids']
        except Exception as e:accepted=False;error=str(e);leads=None;targetfamily=None
        if accepted:
            try:r=pub.lifecycle(w.args('publish'));publication_accepted=True;publication_error=None
            except Exception as e:publication_accepted=False;publication_error=str(e)
        else:publication_accepted=False;publication_error='prior read-only gate rejected'
    item={'kind':kind,'modified_unexempt_record_id':changed_id,'target_family_ids':targetfamily,'modified_record_family_ids':live.family_ids(record) if kind=='shared_concept' else None,'absence_gate_accepted':accepted,'account_leads':leads,'error':error,'publication_model_accepted':publication_accepted,'model_publish_POSTs':w.native.calls.count('publish'),'verified_receipt_created':(pub.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists(),'publication_error':publication_error}
    out.append(item);print(json.dumps(item),flush=True)
ns['need'](not ns['ATTEMPTS'] and not f.ATTEMPTS,'External entry point attempted')
receipt=ns['strict']((mirror.parent/'COPY_RECEIPT.json').read_bytes());ns['need'](all(ns['pin']((mirror/n).read_bytes())==p for n,p in receipt['files'].items()),'Copied input drift')
ns['dump'](P/'private/KNOWN_TARGET_FAMILY_RESULTS.json',{'at':ns['stamp'](),'operations_sha256':ns['OPS_SHA'],'bootstrap_sha256':ns['BOOT_SHA'],'cases':out,'copied_inputs_unchanged':len(receipt['files']),'external_attempts':ns['ATTEMPTS']+f.ATTEMPTS,'real_external_mutations':0,'publication_ready':False})
