#!/usr/bin/env python3
"""Authenticate immutable GitHub tree/blob reads; never run original code."""
import base64, datetime, hashlib, json, os, pathlib, subprocess, sys

root = pathlib.Path(__file__).resolve().parent
science = 'unsolved_math_prioritization/attempts/10300025/'
head = 'bdee508c676c98cb96dbc1a2e5aef2fe9cd1c744'
source_sha = hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
utc = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
def read_api(label, endpoint):
    prefix=root/'receipts'/label
    if prefix.with_suffix('.stdout').exists():
        return json.loads(prefix.with_suffix('.stdout').read_bytes())
    started=utc()
    p=subprocess.Popen(['gh','api',endpoint],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate()
    rec={'operator':'SOURCE subagent /root/algebra_reproduction_audit','capture_pid':os.getpid(),
         'child_pid':p.pid,'started_utc':started,'ended_utc':utc(),'argv':['gh','api',endpoint],
         'returncode':p.returncode,'source_sha256':source_sha,
         'stdout':{'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},
         'stderr':{'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}}
    prefix.with_suffix('.stdout').write_bytes(out); prefix.with_suffix('.stderr').write_bytes(err)
    prefix.with_suffix('.json').write_text(json.dumps(rec,indent=2)+'\n')
    if p.returncode: raise RuntimeError(rec)
    return json.loads(out)
def tree(sha):
    t=read_api('tree_'+sha,'repos/AlecKriebel/Math/git/trees/'+sha)
    assert t['sha']==sha and not t['truncated']
    raw=b''.join((x['mode'].lstrip('0')+' '+x['path']).encode()+b'\0'+bytes.fromhex(x['sha'])
                 for x in sorted(t['tree'],key=lambda x:(x['path']+('/' if x['type']=='tree' else '')).encode()))
    assert hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==sha
    return t['tree']
commit=json.loads((root/'receipts/head_commit.stdout').read_bytes())
assert commit['sha']==head
nodes=tree(commit['tree']['sha'])
for dirname in science.rstrip('/').split('/'):
    matches=[x for x in nodes if x['path']==dirname and x['type']=='tree']
    assert len(matches)==1
    nodes=tree(matches[0]['sha'])
entries=[]
def walk(nodes,prefix=''):
    for x in nodes:
        p=prefix+x['path']
        if x['type']=='tree': walk(tree(x['sha']),p+'/')
        else:
            assert x['type']=='blob' and x['mode']=='100644'
            entries.append({'path':p,'git_sha1':x['sha'],'git_mode':x['mode'],'bytes':x['size']})
walk(nodes)
assert len(entries)==23
files=json.loads((root/'receipts/pr_files.stdout').read_bytes())
changed={x['filename'][len(science):]:x['sha'] for x in files if x['filename'].startswith(science)}
assert changed=={e['path']:e['git_sha1'] for e in entries}
phase=sys.argv[1]
literal={'source_record.json','KNOWN_RESULT.md','attempt.json','turns.json','prior_report.json','source_provenance.json'}
selected=[e for e in entries if (e['path'] in literal if phase=='literal' else e['path'] not in literal)]
for e in selected:
    d=read_api('blob_'+e['git_sha1'],'repos/AlecKriebel/Math/git/blobs/'+e['git_sha1'])
    assert d['sha']==e['git_sha1'] and d['encoding']=='base64'
    body=base64.b64decode(d['content']); assert len(body)==e['bytes']==d['size']
    assert hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==e['git_sha1']
    dest=root/'original'/e['path']; dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists(): assert dest.read_bytes()==body
    else: dest.write_bytes(body)
    e['sha256']=hashlib.sha256(body).hexdigest()
    print(json.dumps(e))
index=root/'SCIENCE_INDEX.json'
old=json.loads(index.read_text()) if index.exists() else {}
old.update({e['path']:e for e in selected})
index.write_text(json.dumps(old,indent=2,sort_keys=True)+'\n')
print(json.dumps({'operator':'SOURCE subagent','pid':os.getpid(),'utc':utc(),'phase':phase,
                  'selected_count':len(selected),'total_tree_bodies':len(entries),'no_checker_execution':True}))
