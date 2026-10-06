#!/usr/bin/env python3
"""Replay adversarial controls against each accepted packet's trusted checker."""
import hashlib,json,pathlib,shutil,subprocess,sys,tempfile,zipfile
HERE=pathlib.Path(__file__).resolve().parent

def require(x,m):
    if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def build(root,mp,zp,m):
    with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(root.iterdir()):z.writestr(f.name,f.read_bytes())
    for e in m['files']:
        b=(root/e['path']).read_bytes();e['bytes']=len(b);e['sha256']=sha(b)
    b=zp.read_bytes();m['zip']['bytes']=len(b);m['zip']['sha256']=sha(b);mp.write_text(json.dumps(m))
def run(root=HERE):
    results=[]
    variants=[('original','AUTHOR_SAFE_FREEZE.zip','AUTHOR_EXTERNAL_MANIFEST.json'),('clarified','CLARIFIED_SAFE.zip','CLARIFIED_EXTERNAL_MANIFEST.json')]
    for label,zn,mn in variants:
        with tempfile.TemporaryDirectory(prefix='torus-integrity-') as td:
            td=pathlib.Path(td);clean=td/'clean';clean.mkdir()
            with zipfile.ZipFile(root/zn) as z:z.extractall(clean)
            trusted=clean/'verify_packet.py'
            for case in ['changed_proof','extra_file','missing_file','symlink','rebound_solved_status','duplicate_manifest_key','duplicate_zip_entry','zip_traversal_entry','changed_zip_bytes','wrong_member_digest','rebound_source_pin','rebound_pair_hash']:
                d=td/case;d.mkdir();packet=d/'packet';shutil.copytree(clean,packet);mp=d/'manifest.json';zp=d/'packet.zip';mp.write_bytes((root/mn).read_bytes());zp.write_bytes((root/zn).read_bytes());m=json.loads(mp.read_text())
                if case=='changed_proof':(packet/'PROOF.md').write_bytes((packet/'PROOF.md').read_bytes()+b'\n')
                elif case=='extra_file':(packet/'extra.txt').write_text('adversarial fixture')
                elif case=='missing_file':(packet/'README.md').unlink()
                elif case=='symlink':(packet/'README.md').unlink();(packet/'README.md').symlink_to(clean/'README.md')
                elif case=='rebound_solved_status':
                    f=packet/'status.json';s=json.loads(f.read_text());s['full_problem_solved']=True;f.write_text(json.dumps(s));build(packet,mp,zp,m)
                elif case=='duplicate_manifest_key':mp.write_text(mp.read_text().replace('"schema":','"schema": "authored-packet-v1", "schema":',1))
                elif case in ['duplicate_zip_entry','zip_traversal_entry']:
                    import warnings
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore')
                        with zipfile.ZipFile(zp,'a') as z:z.writestr('PROOF.md' if case=='duplicate_zip_entry' else '../outside.txt',b'fixture')
                    b=zp.read_bytes();m['zip']['bytes']=len(b);m['zip']['sha256']=sha(b);mp.write_text(json.dumps(m))
                elif case=='changed_zip_bytes':zp.write_bytes(zp.read_bytes()+b'fixture')
                elif case=='wrong_member_digest':m['files'][0]['sha256']='0'*64;mp.write_text(json.dumps(m))
                elif case=='rebound_source_pin':
                    f=packet/'sources.json';s=json.loads(f.read_text());s['sources'][0]['sha256']='0'*64;f.write_text(json.dumps(s));build(packet,mp,zp,m)
                elif case=='rebound_pair_hash':
                    f=packet/'verification_metadata.json';s=json.loads(f.read_text());s['complete_record_report_pair_sha256']='0'*64;f.write_text(json.dumps(s));build(packet,mp,zp,m)
                for optimized in (False,True):
                    cmd=[sys.executable]+(['-O'] if optimized else [])+[str(trusted),str(packet),str(mp),str(zp)]
                    r=subprocess.run(cmd,capture_output=True,timeout=45,cwd=td)
                    require(r.returncode!=0 and b'"result": "fail"' in r.stderr,label+' accepted '+case)
                    results.append({'packet':label,'case':case,'optimized':optimized,'result':'rejected','reason':json.loads(r.stderr)['error']})
    return {'result':'pass','case_families':12,'cli_rejections':len(results),'original_required_controls':10,'clarified_required_controls':10,'results':results}
if __name__=='__main__':
    try:print(json.dumps(run(),sort_keys=True))
    except Exception as e:print(json.dumps({'result':'fail','error':str(e)}),file=sys.stderr);sys.exit(1)
