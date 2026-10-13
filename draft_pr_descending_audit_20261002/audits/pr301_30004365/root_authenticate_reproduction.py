"""Read full original intake and actual finite-reproduction custody, without mutation."""
from pathlib import Path
from datetime import datetime, timezone
import base64, gzip, hashlib, json, os, stat, sys
A=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v: raise RuntimeError(m)
def pin(p):
    p=Path(p);b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def match(p,w):
    d=pin(p);need(d['bytes']==w['bytes'] and d['sha256']==w['sha256'],'complete pinned body')
    if 'mode' in w:need(d['mode']==w['mode'],'pinned mode')
    return d
def capture(q):
    record=json.loads((q/'execution.json').read_bytes())
    need(record['exit_code']==0 and record['parent_reaped'] and record['actual_PID']>0,'actual completed native execution')
    streams={}
    for label,item in record['streams'].items():
        match(item['stored']['path'],item['stored'])
        b=gzip.decompress(Path(item['stored']['path']).read_bytes())
        need(len(b)==item['logical_bytes'] and sha(b)==item['logical_sha256'],'complete logical stream')
        streams[label]=b
    need(not streams['stderr'],'no successful-run stderr')
    request=json.loads((q/'request.json').read_bytes())
    if 'request' in record:match(q/'request.json',record['request'])
    for name in ['source','original_source','expected','recorder','interpreter','interpreter_binary']:
        if name in request:match(request[name]['path'],request[name])
    src=gzip.decompress((q/'source.gz').read_bytes())
    need(len(src)==request['source']['bytes'] and sha(src)==request['source']['sha256'],'exact full prelaunch source')
    if (q/'recorder.gz').exists():need(gzip.decompress((q/'recorder.gz').read_bytes())==Path(request['recorder']['path']).read_bytes(),'exact recorder')
    if 'read_only' in request:need(request['read_only'] and request['argv'][1]=='api','read-only intake')
    else:need(request['argv'][1:3]==['-E','-B'],'assertions enabled and no ambient optimization')
    return dict(execution=pin(q/'execution.json'),actual_PID=record['actual_PID'],argv=request['argv']),streams['stdout']
def main():
    need(not sys.flags.optimize,'unoptimized validator')
    manifest=json.loads((A/'snapshot_manifest.json').read_bytes());original=[]
    for row in manifest['files']:
        p=Path(row['snapshot']['path']);d=match(p,row['snapshot']);b=p.read_bytes()
        need(hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==row['git_blob_sha'] and row['git_mode']=='100644','original Git blob/mode')
        original.append(d)
    need(len(original)==18 and manifest['head']=='125d90fa3f5a4f90b813fec7a7c0f1918914d885' and manifest['original_submitted_status']=='claimed_solved','original eligibility')
    snapshots=[];responses=[]
    for q in sorted((A/'snapshot_actual_api').iterdir()):
        r,b=capture(q);snapshots.append(r);responses.append(json.loads(b))
    need(len(responses)==22 and responses[0]['head']['sha']==manifest['head']==responses[-1]['head']['sha'],'full intake final head')
    need(responses[0]['state']==responses[-1]['state']=='open' and responses[0]['draft'] and responses[-1]['draft'],'original draft still open at intake')
    changed={r['filename']:r for r in responses[1]};tree={r['path']:r for r in responses[2]['tree']}
    need(set(changed)=={r['path'] for r in manifest['files']},'full exact changed domain')
    for row,response in zip(manifest['files'],responses[3:21]):
        body=base64.b64decode(response['content']);need(body==Path(row['snapshot']['path']).read_bytes(),'native blob full body')
        need(row['git_blob_sha']==response['sha']==tree[row['path']]['sha']==changed[row['path']]['sha'],'four-way Git identity')
    replays=[]
    for parent in [A/'reproduction',A/'root_family_reproduction']:
        for q in sorted(parent.iterdir()):
            r,b=capture(q);request=json.loads((q/'request.json').read_bytes())
            if 'expected' in request:
                need(json.loads((q/Path(request['expected']['path']).name).read_bytes())==json.loads(Path(request['expected']['path']).read_bytes()),'complete independent generated output')
            else:
                original_relative='review/INDEPENDENT_CONTROLS.json' if q.name.endswith('verify_independent') else 'verification.json'
                need(json.loads(b)==json.loads((A/'snapshot/problems/30004365_gentle_derived_invariant'/original_relative).read_bytes()),'original exact full output')
            replays.append(r)
    need(len(replays)==7,'four original plus three fresh root controls')
    package=A/'snapshot/problems/30004365_gentle_derived_invariant'
    scoped=[]
    for filename,prefix in [('PUBLIC_MANIFEST.json',package),('review/REVIEW_MANIFEST.json',package/'review')]:
        for row in json.loads((package/filename).read_bytes())['files']:
            scoped.append(match(prefix/row['path'],row))
    out=dict(status='PASS_ROOT_AUTHENTICATES_FULL_ORIGINAL_AND_SEVEN_ACTUAL_FINITE_REPLAYS',UTC=datetime.now(timezone.utc).isoformat(),
             actual_recorder_PID=os.getpid(),source=pin(__file__),original_head=manifest['head'],snapshot_manifest=pin(A/'snapshot_manifest.json'),
             original_files=original,actual_read_only_API_captures=snapshots,actual_root_replays=replays,public_and_review_manifest_bodies=scoped,
             omitted_historical_source_record_upstream_PDF_images_not_authenticated_by_this_scope=True,
             no_full_algorithm_implementation_no_universal_computational_proof=True,mathematical_acceptance=False,priority_acceptance=False)
    f=A/'ROOT_FULL_ORIGINAL_AND_REPRODUCTION_CUSTODY.json';f.write_text(json.dumps(out,indent=2)+'\n');f.chmod(0o444)
    print(json.dumps(dict(status=out['status'],API_captures=len(snapshots),root_replays=len(replays),result=pin(f)),indent=2))
if __name__=='__main__':main()
