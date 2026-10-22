#!/usr/bin/env python3
"""Independent package inventory, original-object check and actual OS-denied replay."""
from pathlib import Path,PurePosixPath
import os,sys,subprocess,zipfile,hashlib,json,re,datetime,shutil
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
REPO=AUDIT.parents[2]
CACHE=HERE/'.cache'
CACHE.mkdir(exist_ok=True)
(CACHE/'tmp').mkdir(exist_ok=True)
ENV=dict(os.environ,TMPDIR=str(CACHE/'tmp'),PYTHONDONTWRITEBYTECODE='1')
PUB=AUDIT/'publication'
sha=lambda b:hashlib.sha256(b).hexdigest()
def dump(n,x): (HERE/n).write_text(json.dumps(x,indent=2)+'\n')
def safe(n):
    assert isinstance(n,str) and n and '\\' not in n and ':' not in n
    p=PurePosixPath(n)
    assert not p.is_absolute() and '..' not in p.parts and p.as_posix()==n
    return p

def main():
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    baseline={str(p.relative_to(AUDIT)):sha(p.read_bytes()) for p in AUDIT.rglob('*') if p.is_file() and 'package_preflight02' not in p.relative_to(AUDIT).parts and '.cache' not in p.relative_to(AUDIT).parts and '__pycache__' not in p.relative_to(AUDIT).parts and 'qa' not in p.relative_to(AUDIT).parts}
    dump('FROZEN_INPUT_BASELINE.json',baseline)
    arch=zipfile.ZipFile(PUB/'verification_package.zip')
    infos=arch.infolist(); names=[i.filename for i in infos]
    assert len(names)==len(set(names))==93
    assert all(n.startswith('weighted_centers_verification/') for n in names)
    payload={n.split('/',1)[1]:arch.read(n) for n in names}
    for i in infos:
        p=safe(i.filename)
        assert not any(x in p.parts for x in ('.cache','sources','scratch','qa','.secrets','__pycache__','.git'))
        assert '.private' not in i.filename
        assert i.date_time==(2026,10,15,0,0,0)
        assert i.external_attr>>16==0o100644 and not i.is_dir()
        assert i.compress_type==zipfile.ZIP_DEFLATED
    manifest=json.loads(payload['MANIFEST.json'])
    assert payload['MANIFEST.json']==(PUB/'PACKAGE_MANIFEST.json').read_bytes()
    assert set(manifest['files'])==set(payload)-{'MANIFEST.json'}
    for n,rec in manifest['files'].items():
        safe(n); b=payload[n]
        assert {'bytes':len(b),'sha256':sha(b)}==rec
        if n.startswith(('reviews/','original/','root_reproduction/')): origin=AUDIT/n
        elif n=='metadata.json': origin=PUB/'zenodo-deposit.json'
        elif (PUB/n).is_file(): origin=PUB/n
        else: origin=AUDIT/n
        assert b==origin.read_bytes(),n
    seals=json.loads(payload['SEALS.json'])
    assert seals==manifest['nested_seals'] and len(seals)==len(set(seals))==6
    nested=[]
    for n in seals:
        seen=set()
        for line in payload[n].decode().splitlines():
            m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line); assert m
            digest,rel=m.groups(); p=(safe(n).parent/safe(rel)).as_posix()
            assert p not in seen and p!=n;seen.add(p)
            assert p in payload and sha(payload[p])==digest
            nested.append({'seal':n,'path':p,'sha256':digest})
    assert len(nested)==54
    snapshot=json.loads(payload['ORIGINAL_SNAPSHOT.json'])
    originals=[]
    assert snapshot['head']=='417ca52e83cf06b07c388d89c756cfd86473d5b0'
    for rec in snapshot['files']:
        p=safe(rec['path']).as_posix();b=payload['original/'+p]
        git=subprocess.run(['git','show',snapshot['head']+':'+p],cwd=REPO,capture_output=True,check=True).stdout
        assert b==git==(AUDIT/'original'/p).read_bytes()
        assert len(b)==rec['size'] and sha(b)==rec['sha256']
        originals.append({'path':p,'sha256':sha(b),'bytes':len(b),'git_object_equal':True})
    assert len(originals)==16 and {'original/'+r['path'] for r in originals}=={n for n in payload if n.startswith('original/')}
    dump('INTEGRITY_RESULTS.json',{'status':'PASS','timestamp_utc':started,'archive_sha256':sha((PUB/'verification_package.zip').read_bytes()),'members':len(names),'outer_payloads':len(manifest['files']),'all_payload_bytes_equal_checkout':True,'six_ordinary_sha_manifests':seals,'nested_entries':nested,'originals':originals,'zip_paths_regular_and_safe':True,'third_party_or_account_material':'None found in full explicit inventory','manifest_payload_exact':True})
    extract=CACHE/'clean_replay'
    if extract.exists(): shutil.rmtree(extract)
    extract.mkdir()
    arch.extractall(extract)
    extracted=extract/'weighted_centers_verification'
    before={str(p.relative_to(extracted)):sha(p.read_bytes()) for p in extracted.rglob('*') if p.is_file()}
    profile='(version 1)(allow default)(deny network*)'
    # Show that this OS policy actually prevents AF_INET sockets in this process.
    probe=subprocess.run(['/usr/bin/sandbox-exec','-p',profile,sys.executable,'-c','import socket; socket.create_connection(("127.0.0.1",9),timeout=1)'],env=ENV,capture_output=True,text=True)
    assert probe.returncode!=0 and 'Operation not permitted' in probe.stderr,probe.stderr
    proc=subprocess.run(['/usr/bin/sandbox-exec','-p',profile,sys.executable,str(extracted/'run_all.py')],cwd=extracted,env=ENV,capture_output=True,text=True)
    (HERE/'OFFLINE_REPLAY.stdout.txt').write_text(proc.stdout)
    (HERE/'OFFLINE_REPLAY.stderr.txt').write_text(proc.stderr)
    assert proc.returncode==0,proc.stderr
    lines=[json.loads(x) for x in proc.stdout.splitlines()]
    assert len(lines)==6 and all(x['status']=='PASS' for x in lines)
    assert lines[-1]['replayed_jobs']==5 and lines[-1]['frozen_payloads_unchanged']
    for x in lines[:-1]:
        assert x['ignored_clock_fields']==(['started_at_utc','completed_at_utc','elapsed_seconds'] if x['job']=='reviews/oracle01/controls.py' else [])
    after={str(p.relative_to(extracted)):sha(p.read_bytes()) for p in extracted.rglob('*') if p.is_file()}
    assert before==after
    dump('OFFLINE_REPLAY_RESULTS.json',{'status':'PASS','network_probe_denied':True,'network_probe_stderr':probe.stderr,'os_profile':profile,'all_five_actual_jobs':True,'results':lines,'returncode':proc.returncode,'stderr_empty':not proc.stderr,'immutable_extraction':before==after,'ended_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    print(json.dumps({'integrity':'PASS','offline_replay':'PASS','jobs':5,'nested':54,'originals':16}),flush=True)
if __name__=='__main__':main()
