#!/usr/bin/env python3
"""Independent full-gate follow-up for the newly observed authority-port gap."""
import hashlib,json,pathlib,types
P=pathlib.Path(__file__).resolve().parent
driver=P/'review_driver.py';ns={'__file__':str(driver),'__name__':'fresh_review_driver'}
exec(compile(driver.read_bytes(),str(driver),'exec'),ns)
load=ns['load'];sha=ns['sha'];dump=ns['dump'];need=ns['need'];stamp=ns['stamp'];strict=ns['strict'];patch=ns['patch']
mirror=P/'private/fixture/Math';ops=mirror/ns['OPS'].relative_to(ns['REPO']);loader=load(ops)
m={n:loader(n) for n in ['ops_common','collect_live','integrate_remote','native_policy','publish_and_ledger','full_controls']}
c=m['ops_common'];live=m['collect_live'];f=m['full_controls'];pub=m['publish_and_ledger']
c.zenodo.token_for=lambda *a:'OFFLINE_SENTINEL_NO_CREDENTIAL';c.zenodo.doi_status=lambda *a:{'status':'offline'}
serial=0
def world(label):
    global serial
    serial+=1;root=P/'private'/('followup_'+str(serial)+'_'+label);rt=root/'runtime';pr=root/'private';rt.mkdir(parents=True);pr.mkdir()
    for mod in m.values():
        if hasattr(mod,'RUNTIME'):mod.RUNTIME=rt
        if hasattr(mod,'PRIVATE'):mod.PRIVATE=pr
    c.zenodo.STATE_DIR=root/'.zenodo-state';w=f.World(ops,m)
    cl=strict((ops/'ROOT_OPERATIONAL_CLEARANCE.example.json').read_bytes());cl.update(operations_manifest_sha256=ns['OPS_SHA'],bootstrap_sha256=ns['BOOT_SHA'],publication_ready=True,unresolved_operational_findings=[],root_complete_reports_read_and_all_seals_verified=True,allowed_actions=['integrate','pr-description','ready','merge','stage','publish','ledger'],instructions='SYNTHETIC REVIEW FIXTURE ONLY')
    dump(rt/'ROOT_OPERATIONAL_CLEARANCE.json',cl);w.clearance_sha=sha((rt/'ROOT_OPERATIONAL_CLEARANCE.json').read_bytes());return w
out=[]
values=['doi.org:443/abc','shortdoi.org:443/abc','doi.org.:443/abc','https://ordinary.invalid/?r=doi.org:443/abc','https://ordinary.invalid/#shortdoi.org:443/abc']
for where in ['ledger','account','local_state']:
    for value in values:
        w=world('ported_'+where);extra=[]
        if where=='ledger':w.rows.append(['Unrelated result','',value,''])
        elif where=='account':
            record=next(r for r in w.accounts if r['id']!=23408971 and not any(live.semantic(t) for t in live.strings(live.projection(r))));record['metadata']['description']=value
        else:
            state_repo=c.PRIVATE/'state_repo';(state_repo/'.zenodo-state').mkdir(parents=True);dump(state_repo/'.zenodo-state/alias.json',{'id':999001,'description':value});extra=[(live,'REPO',state_repo)]
        with w.installed(),patch(*extra):
            try:g,records,rows=live.collect('before_integration',c.ORIGINAL,cleared=c.clearance(w.clearance_sha,ns['OPS_SHA']));accepted=True;error=None
            except Exception as e:accepted=False;error=str(e)
        out.append({'surface':where,'value':value,'absence_gate_accepted':accepted,'error':error,'appends':w.appends,'native_provider_writes':len(w.native.calls),'git_provider_writes':len(w.git.writes)})
        print(json.dumps({'surface':where,'value':value,'accepted':accepted}),flush=True)
# An explicit protocol-relative form is recognized, showing that failure is
# specifically authority parsing of the no-scheme host:port family.
controls=[]
for value in ['//doi.org:443/abc','https://doi.org:443/abc','//shortdoi.org:443/abc','https://ordinary.invalid/?r=//doi.org:443/abc']:
    try:live.identities(value);accepted=True;error=None
    except Exception as e:accepted=False;error=str(e)
    need(not accepted,'Explicit counterpart not rejected');controls.append({'value':value,'accepted':False,'error':error})
need(not ns['ATTEMPTS'] and not f.ATTEMPTS,'External entry attempted')
receipt=strict((mirror.parent/'COPY_RECEIPT.json').read_bytes());need(all(ns['pin']((mirror/n).read_bytes())==p for n,p in receipt['files'].items()),'Copied input drift')
dump(P/'PORTED_AUTHORITY_FULL_GATE_RESULTS.json',{'at':stamp(),'operations_sha256':ns['OPS_SHA'],'bootstrap_sha256':ns['BOOT_SHA'],'cases':out,'explicit_counterparts':controls,'copied_inputs_unchanged':len(receipt['files']),'external_attempts':ns['ATTEMPTS']+f.ATTEMPTS,'external_mutations':0,'publication_ready':False})
