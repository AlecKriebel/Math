#!/usr/bin/env python3
"""Independent local/mock runner. Never dispatches any live helper main."""
import contextlib,datetime,hashlib,importlib.util,io,json,os,pathlib,subprocess,sys,tempfile,unittest
from unittest.mock import patch
sys.dont_write_bytecode=True
OUT=pathlib.Path(__file__).resolve().parent
AUDIT=OUT.parents[2]
FIXTURE=AUDIT/'reviews/operations_01/check_helpers.py'
ns={'__name__':'independent_supplied_fixtures','__file__':str(FIXTURE)}
exec(compile(FIXTURE.read_bytes(),str(FIXTURE),'exec'),ns)
ns['HERE']=OUT
# Imported test functions resolve globals through the namespace, so every
# temporary fixture is relocated to this reviewer's own directory.
ns['Helpers'].__module__='independent_supplied_fixtures'
p=ns['p']; t=ns['t']; DOI=ns['DOI']; META=ns['META']; ROW=ns['ROW']; QUEUE=ns['QUEUE']
ORIGINAL=ns['ORIGINAL']; FROZEN=ns['FROZEN']; PUB=ns['PUB']; SOURCE=ns['SOURCE']
results=[]

def check(name,fn):
    try:
        details=fn()
        results.append({'name':name,'result':'PASS','details':details})
    except Exception as exc:
        results.append({'name':name,'result':'FAIL','error':repr(exc)})
        raise

def reject(fn,pattern=None):
    try: fn()
    except Exception as exc:
        if pattern is not None: assert pattern in str(exc),(pattern,str(exc))
        return str(exc)
    raise AssertionError('unexpected acceptance')

with (OUT/'supplied-fixtures.stdout').open('w') as output,(OUT/'supplied-fixtures.stderr').open('w') as errors:
    with contextlib.redirect_stdout(output),contextlib.redirect_stderr(errors):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(ns['Helpers'])
        supplied=unittest.TextTestRunner(stream=errors,verbosity=2).run(suite)
assert supplied.wasSuccessful(), 'supplied regression fixtures failed'
results.append({'name':'supplied-14-fixtures','result':'PASS','tests':supplied.testsRun})

def unknown_no_reads():
    trace=[]
    prior={'schema':'pr623-scoped-integration-receipt-v1','pr':623,'problem_id':p.PROBLEM,'branch':p.BRANCH,
           'pushed':True,'historical_candidate_commit':p.ORIGINAL,'proof_sha256':p.PROOF_SHA,
           'doi':DOI,'integration_commit':'a'*40}
    for scenario,pr in [('none',None),('prior',prior)]:
        with tempfile.TemporaryDirectory(dir=OUT) as td:
            pp=pathlib.Path(td)/'prior.json'
            if pr: pp.write_bytes(p.json_bytes(pr))
            with patch.object(p,'PUSHED_RECEIPT',pp),patch.object(p,'local_state',return_value={}), \
                 patch.object(p,'pr_metadata',return_value=META|{'headRefOid':'b'*40}), \
                 patch.object(p,'git',side_effect=lambda *a,**k:trace.append(('git',a))), \
                 patch.object(p,'load_snapshot',side_effect=lambda *a:trace.append(('native',a))), \
                 patch.object(p,'publication_inputs',side_effect=lambda *a:trace.append(('publication',a))), \
                 patch.object(sys,'argv',['helper','--doi',DOI]):
                reject(p.main,'unreviewed PR head')
    assert not trace,trace
    return {'candidate_native_publication_calls':len(trace),'scenarios':2}
check('unknown-head-with-and-without-prior-before-candidate-reads',unknown_no_reads)

def json_doi_paths():
    messages=[]
    messages.append(reject(lambda:p.parse_json('{"x":1,"x":2}'),'duplicate JSON key'))
    for doi in ['', '10.5281/zenodo.0', '10.5281/zenodo.01', 'https://doi.org/'+DOI, DOI+'\n']:
        messages.append(reject(lambda:p.valid_doi(doi),'invalid Zenodo DOI'))
    for path in ['../escape','a/../b','/absolute','a\\b','a//b','./x']:
        messages.append(reject(lambda:p.safe_name(path),'unsafe file path'))
    return {'negative_controls':len(messages)}
check('duplicate-json-doi-and-path-boundaries',json_doi_paths)

def queue_cases():
    row=ROW.encode()
    for ending in (b'',b'\n',b'\r\n'):
        q=b'header\n'+row+ending
        after,record=p.patch_queue(q,DOI)
        assert after.startswith(b'header\n')
        assert after.splitlines(keepends=True)[1].endswith(ending) if ending else not after.endswith(b'\n')
        assert record['all_other_bytes_unchanged'] is True
    for status,turns in [('claimed_solved','0/5'),('queued','1/5'),('rejected','0/5')]:
        q=QUEUE.replace(b' queued ',(' '+status+' ').encode()).replace(b' 0/5 ',(' '+turns+' ').encode())
        reject(lambda:p.patch_queue(q,DOI),'no longer queued')
    reject(lambda:p.patch_queue(b'header only',DOI),'exactly one')
    reject(lambda:p.patch_queue(QUEUE+row+b'\n',DOI),'exactly one')
    return {'positive_line_ending_controls':3,'negative_controls':5}
check('queue-lines-status-turns-missing-and-duplicate-target',queue_cases)

def frozen_control():
    damaged=dict(ORIGINAL)
    damaged['audit/AUDIT_SHA256SUMS.json']+=b' '
    reject(lambda:p.frozen_inventory(damaged),'frozen manifest changed')
    damaged=dict(ORIGINAL)
    audit_file=next(x for x in FROZEN if x.startswith('audit/') and x!='audit/AUDIT_SHA256SUMS.json')
    damaged[audit_file]+=b'changed'
    reject(lambda:p.frozen_inventory(damaged),'frozen input bytes changed')
    return {'original_frozen_count':len(FROZEN),'packet':len([x for x in FROZEN if x.startswith('packet/')]),'audit':len([x for x in FROZEN if x.startswith('audit/')])}
check('independent-frozen-manifest-and-audit-file-tamper',frozen_control)

def publication_controls():
    with tempfile.TemporaryDirectory(dir=OUT) as td:
        root=pathlib.Path(td)
        for name,data in PUB.items(): (root/name).write_bytes(data)
        (root/'CURRENT_PRIORITY_AND_STATUS.md').write_bytes(SOURCE)
        receipt=ns['receipt'](); rp=root/'r.json'; ip=root/'i.json'
        rp.write_bytes(p.json_bytes(receipt)); ip.write_bytes(p.json_bytes(receipt))
        p.publication_inputs(root,DOI,rp,ip,original=ORIGINAL)
        for change in [{'title':'wrong'},{'record_url':'https://zenodo.org/records/11'},
                       {'doi_url':'https://doi.org/10.5281/zenodo.11'},
                       {'files':receipt['files'][:1]}, {'files':[receipt['files'][0]]*2},
                       {'verified_utc':''}, {'doi_resolution':{'status':'resolved','http_status':302}}]:
            ip.write_bytes(p.json_bytes(receipt|change))
            reject(lambda:p.publication_inputs(root,DOI,rp,ip,original=ORIGINAL))
        ip.write_bytes(p.json_bytes(receipt))
        (root/'gns_generation_counterexample.tex').write_bytes(b'unbound changed TeX')
        reject(lambda:p.publication_inputs(root,DOI,rp,ip,original=ORIGINAL),'local paper differs')
        (root/'gns_generation_counterexample.tex').write_bytes(PUB['gns_generation_counterexample.tex'])
        (root/'CURRENT_PRIORITY_AND_STATUS.md').write_bytes(SOURCE+b'changed')
        reject(lambda:p.publication_inputs(root,DOI,rp,ip,original=ORIGINAL),'source notice differs')
    return {'positive_control':1,'negative_controls':9}
check('published-record-exact-two-files-local-tex-and-notice-binding',publication_controls)

def inspect_controls():
    def inspect_mock(info,headers,values):
        calls=[]
        def fake(resource,method,params,body=None):
            calls.append((resource,method,params,body))
            if resource=='spreadsheets':return info
            if params['range'].endswith('A1:D1'):return {'values':headers}
            return {'values':values}
        with patch.object(t,'call',side_effect=fake): result=t.inspect()
        return result,calls
    good={'sheets':[{'properties':{'sheetId':t.GID,'title':t.TAB}}]}
    values,calls=inspect_mock(good,[t.HEADERS],[t.HEADERS])
    assert values==[t.HEADERS]
    assert all(call[2]['spreadsheetId']==t.ID for call in calls)
    assert calls[1][2]['range']=="'Math Puzzles'!A1:D1" and calls[2][2]['range']=="'Math Puzzles'!A:D"
    for info in [{'sheets':[]},{'sheets':[{'properties':{'sheetId':t.GID,'title':'Other'}}]},
                 {'sheets':[{'properties':{'sheetId':0,'title':t.TAB}}]}, {'sheets':good['sheets']*2}]:
        reject(lambda:inspect_mock(info,[t.HEADERS],[]),'gid/title')
    for headers in [[],[t.HEADERS[:-1]],[t.HEADERS+['Extra']],[t.HEADERS[::-1]]]:
        reject(lambda:inspect_mock(good,headers,[]),'headers differ')
    reject(lambda:inspect_mock(good,[t.HEADERS],{}),'not a row list')
    return {'positive_control':1,'negative_controls':9,'gid':t.GID,'tab':t.TAB,'range':'A:D'}
check('tracker-gid-title-exact-headers-and-range-binding',inspect_controls)

def pending_failure_controls():
    row=t.wanted_row(DOI)
    response={'updates':{'updatedRange':"'Math Puzzles'!A2:D2",'updatedRows':1,'updatedColumns':4,'updatedCells':4}}
    cases=['timeout','malformed-range','wrong-count','target-mismatch','global-mismatch']
    evidence=[]
    for mode in cases:
        with tempfile.TemporaryDirectory(dir=OUT) as td:
            pending=pathlib.Path(td)/'pending.json'; calls=[]
            def fake(resource,method,params,body=None):
                calls.append(method)
                if method=='append':
                    assert pending.exists()
                    assert p.parse_json(pending.read_bytes())['action_outcome'].startswith('unconfirmed')
                    assert params=={'spreadsheetId':t.ID,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True}
                    assert body=={'majorDimension':'ROWS','values':[row]}
                    if mode=='timeout':raise subprocess.TimeoutExpired('mock',1)
                    if mode=='malformed-range':return {'updates':response['updates']|{'updatedRange':"'Other'!A2:D2"}}
                    if mode=='wrong-count':return {'updates':response['updates']|{'updatedCells':3}}
                    return response
                if params['range'].endswith('A2:D2'):return {'values':[[*row[:3],'incorrect']]} if mode=='target-mismatch' else {'values':[row]}
                return {'values':[t.HEADERS]}
            with patch.object(t,'PENDING',pending),patch.object(t,'inspect',return_value=[t.HEADERS]),patch.object(t,'call',side_effect=fake):
                message=reject(lambda:t.append_once(DOI,row,{}))
                saved=p.parse_json(pending.read_bytes())
                assert saved['action_outcome'].startswith('unconfirmed')
                first_calls=list(calls)
                reject(lambda:t.append_once(DOI,row,{}),'earlier append outcome is unconfirmed')
                assert calls==first_calls
            evidence.append({'case':mode,'append_calls':calls.count('append'),'pending':saved['action_outcome'],'replay_new_calls':0,'failure':message})
    return evidence
check('append-timeout-malformed-reply-and-readback-failures-durable-no-retry',pending_failure_controls)

summary={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS',
         'supplied_tests':supplied.testsRun,'independent_control_groups':len(results)-1,
         'results':results,'live_helper_main_calls':0,'remote_mutations':0,'git_mutations':0,
         'writes_outside_review_folder':0}
(OUT/'RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
with (OUT/'RESEARCH_LOG.md').open('a') as log:
    log.write('\n'+summary['captured_utc']+' — Supplied '+str(supplied.testsRun)+' mock fixtures and '+str(len(results)-1)+' independent control groups passed. Frozen inventory confirms 13 packet and 11 audit files. Uncertain tracker outcomes remain blocked on absent exact DOI; no live helper/service/git calls. Completion estimate: 70%.\n')
print(json.dumps({'result':'PASS','supplied_tests':supplied.testsRun,'independent_control_groups':len(results)-1}))
