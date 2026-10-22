#!/usr/bin/env python3
"""Two new near-publication model probes; no provider/network/process access."""
import json,pathlib
P=pathlib.Path(__file__).resolve().parent;driver=P/'review_driver.py'
ns={'__file__':str(driver),'__name__':'fresh_review_driver'};exec(compile(driver.read_bytes(),str(driver),'exec'),ns)
mirror=P/'private/fixture/Math';ops=mirror/ns['OPS'].relative_to(ns['REPO']);loader=ns['load'](ops)
m={n:loader(n) for n in ['ops_common','collect_live','integrate_remote','native_policy','publish_and_ledger','full_controls']}
c=m['ops_common'];live=m['collect_live'];f=m['full_controls'];pub=m['publish_and_ledger']
c.zenodo.token_for=lambda *a:'OFFLINE_SENTINEL_NO_CREDENTIAL';c.zenodo.doi_status=lambda *a:{'status':'offline'}
out=[]
for position in ['ledger','account']:
    root=P/'private'/('near_publish_port_'+position);rt=root/'runtime';pr=root/'private';rt.mkdir(parents=True);pr.mkdir()
    for mod in m.values():
        if hasattr(mod,'RUNTIME'):mod.RUNTIME=rt
        if hasattr(mod,'PRIVATE'):mod.PRIVATE=pr
    c.zenodo.STATE_DIR=root/'.zenodo-state';w=f.World(ops,m)
    cl=ns['strict']((ops/'ROOT_OPERATIONAL_CLEARANCE.example.json').read_bytes());cl.update(operations_manifest_sha256=ns['OPS_SHA'],bootstrap_sha256=ns['BOOT_SHA'],publication_ready=True,unresolved_operational_findings=[],root_complete_reports_read_and_all_seals_verified=True,allowed_actions=['integrate','pr-description','ready','merge','stage','publish','ledger'],instructions='SYNTHETIC REVIEW FIXTURE ONLY')
    ns['dump'](rt/'ROOT_OPERATIONAL_CLEARANCE.json',cl);w.clearance_sha=ns['sha']((rt/'ROOT_OPERATIONAL_CLEARANCE.json').read_bytes())
    with w.installed():w.through_merge();pub.lifecycle(w.args('stage'))
    value='https://ordinary.invalid/?r=shortdoi.org:443/abc'
    if position=='ledger':w.rows.append(['Ordinary unrelated result','',value,''])
    else:
        record=next(r for r in w.accounts if r['id']!=23408971 and not any(live.semantic(t) for t in live.strings(live.projection(r))));record['metadata']['description']=value
    with w.installed():
        try:r=pub.lifecycle(w.args('publish'));accepted=True;error=None
        except Exception as e:accepted=False;error=str(e);r=None
    out.append({'position':position,'unresolved_alias':value,'publication_model_accepted':accepted,'model_publish_POSTs':w.native.calls.count('publish'),'verified_receipt_created':(pub.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists(),'error':error,'result':r})
    print(json.dumps(out[-1]),flush=True)
ns['need'](not ns['ATTEMPTS'] and not f.ATTEMPTS,'External entry point attempted')
receipt=ns['strict']((mirror.parent/'COPY_RECEIPT.json').read_bytes());ns['need'](all(ns['pin']((mirror/n).read_bytes())==p for n,p in receipt['files'].items()),'Copied input drift')
ns['dump'](P/'NEAR_PUBLICATION_PORTED_ALIAS_RESULTS.json',{'at':ns['stamp'](),'operations_sha256':ns['OPS_SHA'],'bootstrap_sha256':ns['BOOT_SHA'],'cases':out,'copied_inputs_unchanged':len(receipt['files']),'external_attempts':ns['ATTEMPTS']+f.ATTEMPTS,'real_external_mutations':0,'publication_ready':False})
