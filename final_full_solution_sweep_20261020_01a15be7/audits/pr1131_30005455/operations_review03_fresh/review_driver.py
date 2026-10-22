#!/usr/bin/env python3
"""Fresh reviewer: stdlib-only input verification, read-only checker and fixtures.
This driver never launches a provider process or reads real tokens. It must run
under -I -S. All output is confined to this review folder. Raw fixture bodies are
private; public reports contain only counts, hashes and synthetic test values.
"""
import argparse, contextlib, copy, datetime, hashlib, http.client, io, json, os
from pathlib import Path
import socket, subprocess, sys, tarfile, types, urllib.request

HERE=Path(__file__).resolve().parent
OPS=HERE.parent/'operations'
AUDIT=OPS.parent
REPO=OPS.parents[3]
OPS_SHA='69cb677847d73ffcfe8c3dc710978e62da1bbfc3f69e1b7944d7f5411183cea7'
BOOT_SHA='6bde66dd5ad378b8c1164fee8013e5b524255f76d1f8b5f0b5f58003802ebde0'
ATTEMPTS=[]
def need(v,m):
    if not v:raise RuntimeError(m)
def blocked(*a,**k):
    ATTEMPTS.append('blocked external entry point');raise RuntimeError('Fresh reviewer forbids external calls')
socket.socket=blocked;socket.create_connection=blocked;socket.getaddrinfo=blocked
http.client.HTTPConnection=blocked;http.client.HTTPSConnection=blocked
urllib.request.urlopen=blocked;urllib.request.OpenerDirector.open=blocked
subprocess.run=blocked;subprocess.Popen=blocked;subprocess.call=blocked
subprocess.check_call=blocked;subprocess.check_output=blocked
os.system=blocked;os.popen=blocked;os.spawnv=blocked;os.spawnve=blocked
os.execv=blocked;os.execve=blocked
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':sha(b)}
def dump(p,v):
    need(HERE in p.resolve().parents,'Output outside reviewer folder')
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def strict(b):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'Duplicate key');d[k]=v
        return d
    return json.loads(b,object_pairs_hook=pairs)
@contextlib.contextmanager
def patch(*changes):
    old=[]
    try:
        for obj,key,value in changes:old.append((obj,key,getattr(obj,key)));setattr(obj,key,value)
        yield
    finally:
        for obj,key,value in reversed(old):setattr(obj,key,value)
def rejected(fn):
    try:fn()
    except Exception as e:return {'type':type(e).__name__,'message':str(e)}
    raise RuntimeError('Injected fault was accepted')
def load(ops=OPS):
    b=(ops/'bootstrap.py').read_bytes();need(sha(b)==BOOT_SHA,'External bootstrap mismatch')
    ns={'__name__':'fresh_review_bootstrap','__file__':str(ops/'bootstrap.py')}
    exec(compile(b,str(ops/'bootstrap.py'),'exec'),ns)
    return ns['load_verified'](ops,OPS_SHA,BOOT_SHA)[0]
def verify():
    started=stamp();loader=load();c=loader('ops_common')
    c.zenodo.token_for=blocked
    check=loader('check_package');pkg=c.package();_,changes=c.proposal()
    preparation=check.verify_preparation()
    output={'at':stamp(),'started':started,'target_manifest':pin((OPS/'OPERATIONS_MANIFEST.json').read_bytes()),'bootstrap':pin((OPS/'bootstrap.py').read_bytes()),'source_only_checker_preparation':preparation,'source_payloads':len(pkg['source']),'flat_kit':len(pkg['flat']),'proposed_files':len(changes),'external_attempts':ATTEMPTS,'original_runtime_files':[p.name for p in (OPS/'runtime').glob('*')]}
    dump(HERE/'INPUT_VALIDATION.json',output)
    print(json.dumps(output,indent=2))
def fixture():
    loader=load();c=loader('ops_common');c.package();c.proposal()
    mirror=HERE/'private/fixture/Math';need(not mirror.exists(),'Fixture exists')
    inventory={}
    def cp(p):
        b=p.read_bytes();n=p.relative_to(REPO);target=mirror/n
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
        need(target.read_bytes()==b,'Copy readback');inventory[n.as_posix()]=pin(b)
    manifest=strict((OPS/'OPERATIONS_MANIFEST.json').read_bytes())
    for n in [*manifest['files'],'OPERATIONS_MANIFEST.json']:cp(OPS/n)
    cp(REPO/'zenodo_deposit_tool/zenodo.py')
    science=strict((AUDIT/'ROOT_SCIENTIFIC_CLEARANCE.json').read_bytes())
    for n in {'ROOT_SCIENTIFIC_CLEARANCE.json','PACKAGE_FREEZE_01.json','reviews/package01/FINAL_REVIEW_MANIFEST.json','reviews/package02/MANIFEST.json',*science['root_acceptance_pins']}:cp(AUDIT/n)
    source=strict((AUDIT/'publication/SOURCE_MANIFEST.json').read_bytes());freeze=strict((AUDIT/'PACKAGE_FREEZE_01.json').read_bytes())
    for n in set(source)|set(freeze['frozen_six'])|{'SOURCE_MANIFEST.json'}:cp(AUDIT/'publication'/n)
    for n in ['ledger.json','pr.json','gate.json',*[f'account_{k}_page_{i}.json' for k in 'ab' for i in range(1,10)]]:cp(OPS/'private/live_8e3a39143bb740ef9053274be751a820'/n)
    for n,p in strict((OPS/'NATIVE_SCHEMA_REFERENCE.json').read_bytes())['captures'].items():
        q=OPS/'private/repair_native_reference'/n;need(pin(q.read_bytes())=={k:p[k] for k in ['bytes','sha256']},'Native fixture pin');cp(q)
    receipt={'at':stamp(),'target_manifest':pin((OPS/'OPERATIONS_MANIFEST.json').read_bytes()),'bootstrap_sha256':BOOT_SHA,'mirror':str(mirror),'files':inventory,'no_credentials_copied':True,'external_reads':0,'external_mutations':0,'reviewer_created':True}
    dump(mirror.parent/'COPY_RECEIPT.json',receipt)
    print(json.dumps({'copied_inputs':len(inventory),'mirror':str(mirror)}))
def probes():
    mirror=HERE/'private/fixture/Math';ops=mirror/OPS.relative_to(REPO);loader=load(ops)
    names=['ops_common','collect_live','integrate_remote','native_policy','publish_and_ledger','full_controls']
    m={n:loader(n) for n in names};c=m['ops_common'];live=m['collect_live'];ir=m['integrate_remote'];pub=m['publish_and_ledger'];f=m['full_controls'];native=m['native_policy']
    c.zenodo.token_for=lambda *a:'OFFLINE_SENTINEL_NO_CREDENTIAL'
    c.zenodo.doi_status=lambda *a:{'status':'offline'}
    results=[];serial=0
    def record(name,fn):
        try:r=fn();results.append({'name':name,'status':'PASS','detail':r})
        except Exception as e:results.append({'name':name,'status':'FAIL','type':type(e).__name__,'message':str(e)})
        print(json.dumps({'completed':name,'status':results[-1]['status']}),flush=True)
    def world(label):
        nonlocal serial
        serial+=1;root=HERE/'private'/('case_'+str(serial)+'_'+label);rt=root/'runtime';pr=root/'private';rt.mkdir(parents=True);pr.mkdir()
        for mod in m.values():
            if hasattr(mod,'RUNTIME'):mod.RUNTIME=rt
            if hasattr(mod,'PRIVATE'):mod.PRIVATE=pr
        c.zenodo.STATE_DIR=root/'.zenodo-state'
        w=f.World(ops,m)
        clearance=strict((ops/'ROOT_OPERATIONAL_CLEARANCE.example.json').read_bytes())
        clearance.update(operations_manifest_sha256=OPS_SHA,bootstrap_sha256=BOOT_SHA,publication_ready=True,unresolved_operational_findings=[],root_complete_reports_read_and_all_seals_verified=True,allowed_actions=['integrate','pr-description','ready','merge','stage','publish','ledger'],instructions='SYNTHETIC OFFLINE REVIEW FIXTURE ONLY')
        dump(rt/'ROOT_OPERATIONAL_CLEARANCE.json',clearance);w.clearance_sha=sha((rt/'ROOT_OPERATIONAL_CLEARANCE.json').read_bytes());return w
    def gate(w,identifier=None):
        return live.collect('before_publish' if identifier else 'before_integration',w.git.head,identifier,cleared=c.clearance(w.clearance_sha,OPS_SHA))
    def semantic_other_projection():
        cases=[]
        for where in ['metadata_extra','files_extra','top_level_extra','links_extra']:
            w=world('projection_'+where)
            r=next(r for r in w.accounts if r['id']!=23408971 and not any(live.semantic(t) for t in live.strings(live.projection(r))))
            value='https://github.com/AlecKriebel/Math/pull/1131'
            if where=='metadata_extra':r['metadata']['reviewer_pointer']=value
            elif where=='files_extra':r['files'].append({'filename':'ordinary.txt','source_pointer':value})
            elif where=='top_level_extra':r['reviewer_pointer']=value
            else:r.setdefault('links',{})['reviewer_pointer']=value
            with w.installed():
                try:gate(w);accepted=True;error=None
                except Exception as e:accepted=False;error=str(e)
            cases.append({'position':where,'absence_accepted':accepted,'error':error})
        return cases
    record('independent_account_projection_surface_probe',semantic_other_projection)
    def resolver_cases():
        cases=['https://a.invalid/?r=//doi.org/abc','https://a.invalid/?r=https://a.invalid/?deep=//doi.org/abc','https://a.invalid/#first=one&second=//shortdoi.org/abc','https://a.invalid/?r=&#47;&#47;doi.org/abc','https://a.invalid/?r=%252F%252Fdoi.org%252Fabc','10/abc','10/abc?','<span>10/abc</span>','doi.org:443/abc','https://doi.org:444/10.5281/zenodo.777','https://doi.org@a.invalid/abc']
        for value in cases:rejected(lambda:live.identities(value))
        positives=['10.5281/zenodo.777','https://doi.org/10.5281/zenodo.777','https://a.invalid/10/2019/06','https://a.invalid/path//doi.org/abc','OWR 10/2025 p. 1 DOI 10.4171/OWR/2025/10']
        return {'rejected':cases,'positive':{s:sorted(live.identities(s)) for s in positives}}
    record('independent_deeper_nested_HTML_alias_and_positive_cases',resolver_cases)
    def exact_source():
        cases=['10.4171/OWR/2025/100','10.4171/OWR/2025/10suffix','10.4171/OWR/2025/10/extra','10.4171/OWR/2025/10.extra','α10.4171/OWR/2025/10','\u200d10.4171/OWR/2025/10','&#x200d;10.4171/OWR/2025/10']
        for value in cases:rejected(lambda:live.row_ids(['OWR 10/2025 pp. 1-2','',value,'']))
        need(live.row_ids(['OWR 10/2025 p. 1','','10.4171/OWR/2025/10',''])==set(),'Exact source context')
        rejected(lambda:live.row_ids(['OWR 10/2025 p. 1','','10.4171/OWR/2025/10','10/abc']))
        return {'source_suffix_and_prefix_confusables_rejected':cases,'exact_source_allowed':True,'separate_alias_blocks':True}
    record('independent_exact_source_attribution_bounded_not_substring',exact_source)
    def title_race():
        w=world('description')
        with w.installed():w.integrate()
        w.gate_hook=lambda *a,**k:w.git.pr.__setitem__('title','Concurrent independently injected title')
        with w.installed():e=rejected(lambda:ir.describe(w.args('pr-description')))
        need(not [x for x in w.git.writes if x['endpoint']=='pulls/1131'],'Title race PATCH')
        need(not (ir.RUNTIME/'PR_DESCRIPTION_VERIFIED.json').exists(),'Title race receipt')
        return e
    record('independent_title_drift_immediate_original_description_guard',title_race)
    def ledger_existing_aliases():
        outcomes=[]
        for alias in ['https://doi.org/10.5281/zenodo.777','https://zenodo.org/records/777','10.5281/zenodo.778','https://zenodo.org/records/778/versions','https://doi.org/10.5281/zenodo.%37%37%37']:
            w=world('existing_alias')
            with w.installed():w.through_merge();w.stage_publish()
            w.rows.append(['Unrelated label','',alias,''])
            with w.installed():e=rejected(lambda:pub.append_ledger(w.args('ledger')))
            need(w.appends==0,'Existing alias appended');outcomes.append({'alias':alias,'appends':0,'error':e})
        return outcomes
    record('independent_existing_record_concept_encoded_alias_ledger_collision',ledger_existing_aliases)
    def native_last_gate():
        outcomes=[]
        for kind in ['conceptdoi_none','conceptdoi_conflict','version','extra_metadata','wrong_doi','owner']:
            w=world('native_'+kind)
            with w.installed():w.through_merge();pub.lifecycle(w.args('stage'))
            calls=[0]
            def drift(*a,**k):
                if a[0]!='before_publish':return
                calls[0]+=1
                if calls[0]!=2:return
                def fault(l,n,fc):
                    if kind=='conceptdoi_none':l['conceptdoi']=None
                    elif kind=='conceptdoi_conflict':l['conceptdoi']='10.5281/zenodo.999'
                    elif kind=='version':n['versions']['index']=2
                    elif kind=='extra_metadata':n['metadata']['copyright']='new unreviewed field'
                    elif kind=='wrong_doi':l['doi']='10.5281/zenodo.999'
                    else:l['owner']=999;n['parent']['access']['owned_by']['user']='999'
                w.native.fault=fault
            w.gate_hook=drift
            with w.installed():e=rejected(lambda:pub.lifecycle(w.args('publish')))
            need(w.native.calls.count('publish')==0,'Late fault POST');outcomes.append({'fault':kind,'POSTs':0,'error':e})
        return outcomes
    record('independent_final_full_publish_gate_infrastructure_drift',native_last_gate)
    def no_clearance_writes():
        w=world('no_clearance');bad=w.args('stage');bad.clearance_sha256='0'*64
        with w.installed():e=rejected(lambda:pub.lifecycle(bad))
        need(not w.native.calls and not w.git.writes and w.appends==0,'Bad clearance wrote')
        return e
    record('independent_clearance_rejection_before_any_publication_provider_write',no_clearance_writes)
    def numeric_ledger():
        w=world('numeric_whole')
        with w.installed():w.through_merge();w.stage_publish();r=pub.append_ledger(w.args('ledger'))
        receipt=strict((pub.RUNTIME/'LEDGER_VERIFIED.json').read_bytes())
        intent=strict((pub.RUNTIME/'LEDGER_APPEND_INTENT.json').read_bytes())
        need(w.appends==1 and r['new_row'] and intent['values'][1]=='' and len(intent['values'])==4,'Numeric positive append')
        need(receipt['all_other_rows_preserved'] and receipt['numeric_readback_counts']=={'rows':1,'columns':4,'cells':4},'Numeric preserved counts')
        return {'appends':1,'native_numeric_gid':receipt['sheet_id'],'blank_B':True,'four_string_cells':True,'prior_rows_preserved':True,'readback_counts':receipt['numeric_readback_counts']}
    record('independent_complete_numeric_fourcell_positive_lifecycle',numeric_ledger)
    def read_response_unknown():
        cases=[]
        for kind in ['replies_missing','replies_wrong','nested_workbook','extra_response','formula_mask','prior_row_change']:
            w=world('response_'+kind)
            with w.installed():w.through_merge();w.stage_publish()
            if kind=='prior_row_change':w.append_mode='prior_row_drift'
            else:
                def fault(r):
                    if kind=='replies_missing':r.pop('replies')
                    elif kind=='replies_wrong':r['replies']=[{'unexpected':True}]
                    elif kind=='nested_workbook':r['updatedSpreadsheet']['spreadsheetId']='other'
                    elif kind=='extra_response':r['updatedCells']=4
                    else:w.formula_fault=True
                w.response_fault=fault
            with w.installed():e=rejected(lambda:pub.append_ledger(w.args('ledger')))
            need(w.appends==1 and not (pub.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Contradictory append confirmed')
            with w.installed():
                if kind in {'formula_mask','prior_row_change'}:second=rejected(lambda:pub.append_ledger(w.args('ledger')))
                else:
                    second=pub.append_ledger(w.args('ledger'))
                    need(second['new_row'] is False,'Read-only reconciliation did not identify exact existing row')
            need(w.appends==1,'Blind retry after inconsistent outcome')
            cases.append({'fault':kind,'appends':1,'verified':False,'first':e,'second':second})
        return cases
    record('independent_native_response_literal_readback_and_unknown_outcome',read_response_unknown)
    def exact_live_git():
        cases=[]
        for fault in ['stale_test_parent','live_main_moves','proof_conflict']:
            w=world('git_'+fault)
            with w.installed():
                if fault=='proof_conflict':
                    flat=w.git.flatten(w.git.commits[w.git.main]['tree']['sha']);flat[c.PROBLEM+'/PROOF.md']=b'concurrent proof';w.git.save_commit(w.git.main,flat,[w.git.parent]);e=rejected(w.integrate)
                    need(not w.git.writes,'Conflicting main wrote')
                else:
                    w.integrate();ir.describe(w.args('pr-description'));ir.mark_ready(w.args('ready'));before=len(w.git.writes)
                    if fault=='stale_test_parent':
                        real=w.git.test_merge
                        def stale():
                            h=real();w.git.commits[h]['parents'][0]['sha']='9'*40;return h
                        w.git.test_merge=stale
                    else:
                        def hook(*a,**k):
                            if a[0]=='before_merge':
                                w.git.save_commit('9'*40,w.git.flatten(w.git.commits[w.git.main]['tree']['sha']),[w.git.main]);w.git.main='9'*40
                        w.gate_hook=hook
                    with w.installed():e=rejected(lambda:ir.merge(w.args('merge')))
                    need(len(w.git.writes)==before,'Stale main/test merge wrote')
            cases.append({'case':fault,'error':e})
        return cases
    record('independent_git_exact_live_main_expectedhead_and_selected_conflict',exact_live_git)
    receipt=strict((mirror.parent/'COPY_RECEIPT.json').read_bytes());changed=[]
    for n,p in receipt['files'].items():
        if pin((mirror/n).read_bytes())!=p:changed.append(n)
    need(not changed,'Reviewer copied inputs changed')
    need(not ATTEMPTS and not f.ATTEMPTS,'A real external entry point was attempted')
    dump(HERE/'INDEPENDENT_RESULTS.json',{'at':stamp(),'mode':sys.flags.optimize,'operations_sha256':OPS_SHA,'bootstrap_sha256':BOOT_SHA,'results':results,'failures':[r for r in results if r['status']!='PASS'],'copied_inputs_unchanged':len(receipt['files']),'external_attempts':ATTEMPTS+f.ATTEMPTS,'external_mutations':0,'publication_ready':False,'note':'Service model reused from sealed preparer source; probe selection, assertions, inputs and verdict are independently authored. Projection probe is diagnostic and must be interpreted separately.'})
def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['verify','fixture','probes']);a=p.parse_args()
    {'verify':verify,'fixture':fixture,'probes':probes}[a.action]()
if __name__=='__main__':main()
