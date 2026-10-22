"""Additional exact-source corrupt-evidence and actual sealed-review compatibility controls."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,traceback
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('repair_probes_01',HERE/'probes_01.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
p.RUNS=HERE/'probe_runs_02';p.SNAP=HERE/'source_snapshot_02'
p.SOURCE={n:(HERE.parent/n).read_bytes() for n in p.NAMES}
RESULTS=[]
def test(label,fn):
    try:r={'label':label,'status':'PASS','detail':fn()}
    except Exception as e:r={'label':label,'status':'FAIL','error':repr(e),'traceback':traceback.format_exc()}
    RESULTS.append(r);p.dump(HERE/'PROBE_RESULTS_02.json',RESULTS);print(json.dumps(r),flush=True)
def tampered_readbacks():
    out={}
    for kind in ['target_readback','after_scan','append_attempt']:
        f=p.Fixture('corrupt_'+kind);f.publish();t=f.append()
        if kind=='append_attempt':
            path=f.pub/'private_transport/tracker/APPEND_ATTEMPT.json';r=json.loads(path.read_text());r['publication_receipt_sha256']='0'*64;p.dump(path,r);t['append_attempt_sha256']=p.sha(path.read_bytes())
        else:
            path=f.c/t['evidence'][kind]['path'];r=json.loads(path.read_text())
            if kind=='target_readback':r['response']['values'][0][3]='Altered fourth cell'
            else:r['response']['values'].append(t['values'])
            p.dump(path,r);t['evidence'][kind]=p.pin(path,f.c)
        p.dump(f.pub/'TRACKER_VERIFIED_APPEND.json',t)
        out[kind]=p.reject(lambda:f.rb.tracker(f.r,f.pub,f.ctx));f.trace()
    return out
def retained_public_bytes():
    f=p.Fixture('corrupt_download');z=f.publish();raw=f.c/z['additional_actual_public_file_downloads'][0]['payload']['path'];raw.write_bytes(b'corrupted')
    z['additional_actual_public_file_downloads'][0]['payload']=p.pin(raw,f.c);p.dump(f.pub/'ZENODO_VERIFIED_PUBLICATION.json',z)
    return p.reject(lambda:f.rb.publication(f.r,f.pub,f.ctx))
def live_conflict():
    f=p.Fixture('live_conflict');z=f.publish();t=f.append();before=f.rb.digest(f.pub/'TRACKER_VERIFIED_APPEND.json');f.sheet.append(t['values'][:])
    err=p.reject(lambda:f.module('append_verified_tracker.py').verify_tracker_live(f.r,f.pub,f.ctx,z))
    assert f.appends==1 and before==f.rb.digest(f.pub/'TRACKER_VERIFIED_APPEND.json')
    f.trace();return {'error':err,'actual_stub_appends':1,'immutable_receipt_unchanged':True}
def wrong_live_doi():
    f=p.Fixture('wrong_live_doi');z=f.publish();before=f.rb.digest(f.pub/'ZENODO_VERIFIED_PUBLICATION.json');real=f.v
    def wrong(*a,**k):
        v=real(*a,**k);v['doi_resolution']['resolved_url']='https://zenodo.org/records/99999';return v
    f.v=wrong
    err=p.reject(lambda:f.module('verify_published_readonly.py').verify_publication_live(f.r,f.pub,f.ctx))
    assert before==f.rb.digest(f.pub/'ZENODO_VERIFIED_PUBLICATION.json')
    f.trace();return {'error':err,'immutable_receipt_unchanged':True}
def stale_reviewed_helpers():
    f=p.Fixture('stale_reviewed_helpers');path=f.pub/'publish_preprint.py';path.write_bytes(path.read_bytes()+b'\n# Changed after review\n')
    f.clear['release_helpers']=[p.pin(f.pub/n,f.pub) for n in p.NAMES];f.save_clear()
    return p.reject(lambda:f.rb.context(f.r))
def missing_readback():
    f=p.Fixture('missing_readback');f.publish();t=f.append();(f.c/t['evidence']['after_scan']['path']).unlink()
    return p.reject(lambda:f.rb.tracker(f.r,f.pub,f.ctx))
def helper_finding():
    f=p.Fixture('helper_finding');entry=f.clear['release_helper_reviews'][0];path=f.c/entry['resolution']['path'];r=json.loads(path.read_text());r['resolved_findings']=[];p.dump(path,r);entry['resolution']=p.pin(path,f.c);f.save_clear()
    return p.reject(lambda:f.rb.context(f.r))
def actual_sealed_compatibility():
    case=HERE.parent.parent;rb=p.Fixture('actual_review_parser').rb
    base=HERE/'actual_review_compatibility_01';base.mkdir()
    # The first actual scientific seal, additive supplement and actual root repair are read only.
    first=case/'whole_package_adversary_01'
    entry={'assessment':p.pin(first/'ASSESSMENT.json',case),'authored_manifest':p.pin(first/'AUTHORED_MANIFEST.json',case),
        'supplements':[p.pin(first/'AUTHORED_MANIFEST_SUPPLEMENT_REPORT_CORRECTION.json',case)],
        'resolution':p.pin(case/'initial_review_20261016/ROOT_REVIEW01_RESOLUTION.json',case)}
    core=rb.current_core(case/'preprint');folder=base/'synthetic_final_whole';folder.mkdir()
    frozen=datetime.now(timezone.utc).isoformat();p.dump(folder/'FROZEN_BYTES.json',{'frozen_utc':frozen,'core':[dict(path=n,**v) for n,v in core.items()]})
    (folder/'REPORT.md').write_text('SYNTHETIC compatibility fixture, not a review or clearance.\n')
    a={'schema':'pr209-whole-package-assessment-v1','review_id':'synthetic_compatibility_whole02','review_completed':True,
       'frozen_utc':frozen,'completed_utc':datetime.now(timezone.utc).isoformat(),'frozen_bindings':core,'verdict':'PASS',
       'mandatory_findings':[],'optional_findings':[],'evidence':{'report':p.pin(folder/'REPORT.md',folder),'freeze':p.pin(folder/'FROZEN_BYTES.json',folder)}}
    p.dump(folder/'ASSESSMENT.json',a);p.dump(folder/'AUTHORED_MANIFEST.json',{'files':[p.pin(x,folder) for x in sorted(folder.iterdir()) if x.is_file()]})
    second={'assessment':p.pin(folder/'ASSESSMENT.json',case),'authored_manifest':p.pin(folder/'AUTHORED_MANIFEST.json',case),'supplements':[]}
    whole=rb.review_chain(case,[entry,second],'whole-package',core)
    # The first actual source seal is checked against every retained payload; final evidence below is synthetic.
    first=case/'release_helpers_adversary_01';a=json.loads((first/'ASSESSMENT.json').read_text())
    entry={'assessment':p.pin(first/'ASSESSMENT.json',case),'authored_manifest':p.pin(first/'AUTHORED_MANIFEST.json',case),'supplements':[],
           'source_freeze':p.pin(first/'FROZEN_SOURCES.json',case)}
    helpers=[p.pin(HERE.parent/n,HERE.parent) for n in p.NAMES]
    resolution={'review_id':a['reviewer'],'utc':datetime.now(timezone.utc).isoformat(),
        'review_assessment_sha256':entry['assessment']['sha256'],'review_manifest_sha256':entry['authored_manifest']['sha256'],
        'resolved_findings':[{'id':f['id'],'status':'resolved'} for f in a['mandatory_findings']+a['optional_findings']],
        'unresolved_mandatory_findings':[],'unresolved_optional_findings':[],'source_bindings':helpers,
        'role':'SYNTHETIC parser fixture only; no actual finding closure'}
    p.dump(base/'SYNTHETIC_HELPER_RESOLUTION.json',resolution);entry['resolution']=p.pin(base/'SYNTHETIC_HELPER_RESOLUTION.json',case)
    folder=base/'synthetic_final_helper';folder.mkdir()
    for n in p.NAMES:(folder/n).write_bytes((HERE.parent/n).read_bytes())
    p.dump(folder/'FROZEN_SOURCES.json',{'frozen_utc':datetime.now(timezone.utc).isoformat(),'rows':helpers})
    (folder/'REPORT.md').write_text('SYNTHETIC compatibility fixture, not a source review.\n')
    a={'schema':'pr209-release-helper-assessment-v1','reviewer':'synthetic_compatibility_helper02','completed_utc':datetime.now(timezone.utc).isoformat(),
        'frozen_sources':helpers,'mandatory_findings':[],'optional_findings':[],'verdict':'PASS'}
    p.dump(folder/'ASSESSMENT.json',a);p.dump(folder/'AUTHORED_MANIFEST.json',{'files':[p.pin(x,folder) for x in sorted(folder.iterdir()) if x.is_file()]})
    second={'assessment':p.pin(folder/'ASSESSMENT.json',case),'authored_manifest':p.pin(folder/'AUTHORED_MANIFEST.json',case),'supplements':[],'source_freeze':p.pin(folder/'FROZEN_SOURCES.json',case)}
    helper=rb.review_chain(case,[entry,second],'release-helper',helpers)
    return {'actual_first_scientific_review_payloads_and_additive_supplement_validated':True,
        'actual_first_helper_review_all_payloads_validated':True,'synthetic_next_whole_count_and_clean':whole,
        'synthetic_next_helper_count_and_clean':helper,'no_real_clearance_or_findings_closed':True}
if __name__=='__main__':
    p.SNAP.mkdir()
    for n,raw in p.SOURCE.items():(p.SNAP/n).write_bytes(raw)
    p.dump(HERE/'EXACT_SOURCE_INPUTS_02.json',{'utc':datetime.now(timezone.utc).isoformat(),'case_completion_percent':55,'files':[p.pin(p.SNAP/n,HERE) for n in p.NAMES]})
    for label,fn in [('tampered_readbacks',tampered_readbacks),('retained_public_bytes',retained_public_bytes),
        ('live_conflict',live_conflict),('wrong_live_doi',wrong_live_doi),('stale_reviewed_helpers',stale_reviewed_helpers),
        ('missing_readback',missing_readback),('helper_finding',helper_finding),('actual_sealed_compatibility',actual_sealed_compatibility)]:
        test(label,fn)
    raise SystemExit(0 if all(r['status']=='PASS' for r in RESULTS) else 1)
