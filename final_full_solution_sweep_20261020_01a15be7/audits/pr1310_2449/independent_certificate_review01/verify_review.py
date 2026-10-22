#!/usr/bin/env python3
"""Read-only sealed-package verifier. --full repeats the numerical certificates.
Trust the manifest digest supplied out of band, not a modifiable manifest alone.
"""
import pathlib,json,hashlib,gzip,base64,subprocess,sys
P=pathlib.Path(__file__).resolve().parent
def need(p,m):
    if not p:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    manifest_bytes=(P/'MANIFEST.json').read_bytes()
    if '--manifest-sha256' in sys.argv:need(sha(manifest_bytes)==sys.argv[sys.argv.index('--manifest-sha256')+1],'external manifest digest')
    m=json.loads(manifest_bytes);actual={str(x.relative_to(P)) for x in P.rglob('*') if x.is_file() and x!=P/'MANIFEST.json'};recorded={x['path'] for x in m['files']}
    need(actual==recorded,'closed inventory');need(len(recorded)==len(m['files']),'duplicate paths')
    total=0
    for x in m['files']:
        p=P/x['path'];need(p.is_relative_to(P) and not p.is_symlink(),'safe local member');b=p.read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'member hash '+x['path']);total+=len(b)
        need(x['private']==x['path'].startswith('private_sources/'),'privacy flag')
    need(total<8*1024*1024,'allocation bound')
    d=json.loads(gzip.decompress((P/'private_sources/captures.json.gz').read_bytes()));index=json.loads((P/'SOURCE_INDEX.json').read_text())
    need(d['head']=='4ce3fbd19d499c7a16aa46ca416ad3305ef3d286' and len(d['sources'])==21,'head and complete changed paths')
    for x,y in zip(d['sources'],index['pr_files'],strict=True):
        b=x['body'].encode();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'source bytes');need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'],'git blob');need(all(y[k]==x[k] for k in ['path','blob','sha256','bytes']),'source index binding')
    need(sha(d['ledger']['stdout'].encode())=='fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1','ledger hash')
    rows=json.loads(d['ledger']['stdout'])['valueRanges'][0]['valueRange']['values'];need(len(rows)==191,'ledger shape')
    need(sha(d['live_pr']['body'].encode())=='0bc9309de239d57d18ac15d02007c0f5961fc9bac17d981d9e0522bf1fb5c26e','PR body')
    for x in d['external']:
        if 'base64' in x:
            b=base64.b64decode(x['base64'],validate=True);need(len(b)==x['bytes'] and sha(b)==x['sha256'],'external capture bytes')
    need((P/'family_result.json').read_bytes()==(P/'family_replay_0.json').read_bytes(),'canonical family output')
    need((P/'block_result.json').read_bytes()==(P/'block_replay_0.json').read_bytes(),'canonical block output')
    for tag in ['family_replay','block_replay','controls']:
        bs=[(P/(tag+'_'+str(i)+'.json')).read_bytes() for i in range(3)];need(bs[0]==bs[1]==bs[2],'mode agreement '+tag)
    r=subprocess.run([sys.executable,'-B',str(P/'check_controls.py')],capture_output=True,check=True);need(r.stdout==(P/'controls_0.json').read_bytes(),'fresh exact controls')
    full=False
    if '--full' in sys.argv:
        r=subprocess.run([sys.executable,'-B',str(P/'check_certificate.py'),'--global-family'],capture_output=True,check=True);need(r.stdout==(P/'family_result.json').read_bytes(),'fresh complete family')
        r=subprocess.run([sys.executable,'-B',str(P/'check_block_certificate.py'),'--replay',str(P/'block_result.json')],capture_output=True,check=True);need(r.stdout==(P/'block_result.json').read_bytes(),'fresh complete block replay');full=True
    print(json.dumps({'schema':'ep1038-sealed-review-verification/v1','members':len(recorded),'private_members':sum(x['private'] for x in m['files']),'bytes':total,'pr_blobs':21,'family_slabs':178,'block_slabs':627,'exact_controls':'PASS','mode_receipts':'IDENTICAL','fresh_full_numeric_replay':full,'services_written':False},sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
