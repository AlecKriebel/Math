#!/usr/bin/env python3
"""Read-only packet binding audit plus isolated execution; writes only this shard."""
from pathlib import Path
import argparse, hashlib, json, os, platform, shutil, subprocess, sys
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PACKET=ROOT/'corrected_packet'
def now(): return datetime.now(timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes()
    return {'path':str(p.relative_to(ROOT)), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
def save(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def check_manifest(path,base):
    m=json.loads(path.read_text()); rows=[]
    for e in m['files']:
        p=(base/e['path']).resolve()
        assert p.is_relative_to(base.resolve()), ('escaped path',p)
        a=pin(p)
        assert a['bytes']==e['bytes'] and a['sha256']==e['sha256'],(path,e,a)
        rows.append(a)
    assert len(rows)==len({x['path'] for x in rows}),('duplicate',path)
    return {'manifest':pin(path),'resolved_base':str(base),'entries':rows}

def bindings(stage):
    start=now(); initial=pin(PACKET/'PUBLICATION_MANIFEST.json')
    intake=json.loads((ROOT/'INTAKE.json').read_text()); originals=[]
    prefix=intake['native_source_prefix']
    for e in intake['original_source_files']:
        assert e['native_path'].startswith(prefix)
        p=PACKET/'original_submission'/e['native_path'][len(prefix):]
        a=pin(p)
        assert a['bytes']==e['bytes'] and a['sha256']==e['sha256'],(e,a)
        raw=p.read_bytes()
        sha1=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        assert sha1==e['native_blob'],(e['native_path'],sha1)
        a['native_blob']=sha1; originals.append(a)
    actual={str(p.relative_to(PACKET/'original_submission')) for p in (PACKET/'original_submission').rglob('*') if p.is_file()}
    expected={e['native_path'][len(prefix):] for e in intake['original_source_files']}
    assert actual==expected and len(actual)==20,(actual^expected,len(actual))
    current=[]
    for f in ('FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json'):
        z=check_manifest(PACKET/f,PACKET); current.append(z)
        entries={x['path'] for x in z['entries']}
        allfiles={str(p.relative_to(ROOT)) for p in PACKET.rglob('*') if p.is_file()}
        excluded={'corrected_packet/'+f}
        if f=='FROZEN_MANIFEST.json':excluded.add('corrected_packet/PUBLICATION_MANIFEST.json')
        assert entries==allfiles-excluded,(f,entries^(allfiles-excluded))
    archived=[]
    for f,base in [('FROZEN_MANIFEST.json',PACKET/'original_submission'),
                   ('PUBLICATION_MANIFEST.json',PACKET/'original_submission'),
                   ('independent_review/REVIEW_MANIFEST.json',PACKET/'original_submission/independent_review')]:
        archived.append(check_manifest(PACKET/'original_submission'/f,base))
    review=json.loads((PACKET/'original_submission/independent_review/REVIEW_MANIFEST.json').read_text())
    assert review['author_proof_sha256']==pin(PACKET/'original_submission/PROOF.md')['sha256']
    assert review['author_manifest_sha256']==pin(PACKET/'original_submission/FROZEN_MANIFEST.json')['sha256']
    historical_verification=json.loads((PACKET/'original_submission/independent_review/FROZEN_VERIFICATION.json').read_text())
    assert historical_verification['author_manifest_sha256']==pin(PACKET/'original_submission/FROZEN_MANIFEST.json')['sha256']
    for e in historical_verification['author']:
        assert pin(PACKET/'original_submission'/e['file'])['sha256']==e['sha256'],e
    new=(PACKET/'PROOF.md').read_bytes(); old=(PACKET/'original_submission/PROOF.md').read_bytes()
    def sections(b):return b[b.index(b'## 1. Exact process and notation'):]
    assert sections(new)==sections(old),'Mathematical sections changed'
    unchanged={}
    for f in ('stationary_law.py','verify_exact.py','exact_receipt.json'):
        assert (PACKET/f).read_bytes()==(PACKET/'original_submission'/f).read_bytes(),f
        unchanged[f]=pin(PACKET/f)
    src=[]
    for e in json.loads((PACKET/'source_manifest.json').read_text())['sources']:
        matches=list((ROOT/'root_priority/private_reading').glob(e['reading_filename']))+list((ROOT/'root_source_reading/private_reading').glob(e['reading_filename']))
        assert matches,('missing primary',e['reading_filename'])
        for p in matches:
            a=pin(p)
            assert a['bytes']==e['bytes'] and a['sha256']==e['sha256'],(e,a)
            src.append(a)
    oldsource=json.loads((PACKET/'original_submission/source_manifest.json').read_text())['sources']
    newsource=json.loads((PACKET/'source_manifest.json').read_text())['sources']
    assert newsource[:len(oldsource)]==oldsource,'six original source entries changed'
    for e in historical_verification['sources']:
        s=next(s for s in oldsource if s['reading_filename']==e['file'])
        assert s['sha256']==e['sha256'],e
    proposed=json.loads((ROOT/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_text())
    assert len(proposed['files'])==35 and proposed['all_files']==35
    for e in proposed['files']:
        a=pin(PACKET/e['path'])
        assert a['sha256']==e['sha256'] and a['bytes']==e['bytes'],('proposed',e,a)
    assert {e['path'] for e in proposed['files']}=={str(p.relative_to(PACKET)) for p in PACKET.rglob('*') if p.is_file()}
    assert pin(PACKET/'PUBLICATION_MANIFEST.json')==initial,'Packet changed during binding audit'
    obj={'status':'PASS','started_utc':start,'completed_utc':now(),'stage':stage,
         'intake':pin(ROOT/'INTAKE.json'),'original_input_count':len(originals),'originals':originals,
         'current_manifests':current,'historical_manifests':archived,
         'historical_FROZEN_VERIFICATION_author_and_source_hashes_valid':True,
         'root_proposed_packet_manifest':pin(ROOT/'PROPOSED_CURRENT_PACKET_MANIFEST.json'),
         'mathematical_sections_1_to_7_identical':True,
         'mathematical_sections_sha256':hashlib.sha256(sections(new)).hexdigest(),
         'unchanged':unchanged,'source_pins':src,
         'all_actual_packet_files':[pin(p) for p in sorted(PACKET.rglob('*')) if p.is_file()]}
    save(stage.upper()+'_PACKET_BINDINGS.json',obj)
    print(json.dumps({'stage':stage,'status':obj['status'],'originals':len(originals),'sources':len(src),'packet_files':len(obj['all_actual_packet_files'])}))

def replays():
    started=now(); dest=HERE/'isolated_replay'
    dest.mkdir(exist_ok=True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
    specs=[('current_author',PACKET,['stationary_law.py','verify_exact.py'],'verify_exact.py',PACKET/'exact_receipt.json'),
           ('archived_author',PACKET/'original_submission',['stationary_law.py','verify_exact.py'],'verify_exact.py',PACKET/'original_submission/exact_receipt.json'),
           ('archived_independent',PACKET/'original_submission/independent_review',['independent_checks.py'],'independent_checks.py',PACKET/'original_submission/independent_review/INDEPENDENT_CHECKS.json')]
    results=[]
    for label,source,files,entry,expected in specs:
        d=dest/label; d.mkdir(exist_ok=True)
        for f in files:shutil.copyfile(source/f,d/f)
        before={f:pin(source/f) for f in files}
        t0=now()
        r=subprocess.run([sys.executable,'-I','-B',entry],cwd=d,env=env,text=True,capture_output=True,timeout=180)
        # -I deliberately removes the script directory, so this source-importing
        # author program needs an isolated launcher that explicitly supplies it.
        if label.endswith('author') and r.returncode and 'ModuleNotFoundError' in r.stderr:
            launcher='import runpy,sys;sys.path.insert(0,\".\");runpy.run_path('+repr(entry)+',run_name=\"__main__\")'
            r=subprocess.run([sys.executable,'-I','-B','-c',launcher],cwd=d,env=env,text=True,capture_output=True,timeout=180)
        assert r.returncode==0,(label,r.returncode,r.stderr)
        assert not r.stderr,(label,r.stderr)
        actual=json.loads(r.stdout); ref=json.loads(expected.read_text())
        assert actual==ref,('COMPLETE RECEIPT MISMATCH',label)
        (HERE/(label.upper()+'_RECEIPT.json')).write_text(r.stdout)
        assert before=={f:pin(source/f) for f in files},('source mutation',label)
        results.append({'label':label,'started_utc':t0,'completed_utc':now(),'exit':r.returncode,
                        'inputs':list(before.values()),'receipt':pin(HERE/(label.upper()+'_RECEIPT.json')),
                        'expected_receipt':pin(expected),'complete_parsed_receipt_equal':True,
                        'complete_stdout_bytes_equal':r.stdout.encode()==expected.read_bytes()})
    assert json.loads((HERE/'CURRENT_AUTHOR_RECEIPT.json').read_text())==json.loads((HERE/'ARCHIVED_AUTHOR_RECEIPT.json').read_text())
    save('ISOLATED_REPLAY_RESULTS.json',{'status':'PASS','started_utc':started,'completed_utc':now(),
         'python':sys.version,'platform':platform.platform(),'runs':results,
         'scope':'Fresh local executions with copied source in separate directories; complete receipts compared, not status-only.'})
    print(json.dumps({'status':'PASS','runs':len(results),'whole_receipts_equal':True}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['bindings','replays']);p.add_argument('--stage',default='final');a=p.parse_args()
    bindings(a.stage) if a.mode=='bindings' else replays()
