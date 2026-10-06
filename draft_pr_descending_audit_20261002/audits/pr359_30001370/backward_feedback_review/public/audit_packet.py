#!/usr/bin/env python3
"""Independent frozen disk/Git/API binding and complete manifest-schema audit.

Only read-only Git/GitHub actions. Full native streams stay in private/bindings.
"""
from pathlib import Path
from datetime import datetime, timezone
import base64
import difflib
import hashlib
import json
import os
import stat
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/Users/alec/Documents/Math')
SNAPSHOT = ROOT.parent/'snapshot'
FOLDER = 'problems/30001370_basin_boundaries'
PACKET = SNAPSHOT/FOLDER
H = '6be98eac0ba508368218179ecf80020c037dbece'
B = 'efd29c05204703acca9a0860812f54b94fae54b1'
AUTHOR = 'be4730c4f09b4fe5cc82bbedb8cb154894124dfd'
CAPTURE = ROOT/'private'/'bindings'
CAPTURE.mkdir(parents=True, exist_ok=True)
records = []

def utc():
    return datetime.now(timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def capture(label, command):
    start = utc()
    result = subprocess.run(command, cwd=REPO, capture_output=True,
                            env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    end = utc()
    (CAPTURE/(label+'.stdout')).write_bytes(result.stdout)
    (CAPTURE/(label+'.stderr')).write_bytes(result.stderr)
    record = dict(label=label,command=command,start_utc=start,end_utc=end,
                  exit_code=result.returncode,stdout_bytes=len(result.stdout),
                  stderr_bytes=len(result.stderr),stdout_sha256=sha(result.stdout),
                  stderr_sha256=sha(result.stderr))
    (CAPTURE/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
    records.append(record)
    if result.returncode:
        raise RuntimeError(f'Native failure preserved: {label}, exit {result.returncode}')
    return result.stdout

def no_duplicates(pairs):
    output = {}
    for k,v in pairs:
        if k in output:
            raise ValueError('duplicate JSON key: '+k)
        output[k]=v
    return output

def parse(data):
    return json.loads(data,object_pairs_hook=no_duplicates)

def schema(value):
    if isinstance(value,dict):
        return {'object':{k:schema(v) for k,v in sorted(value.items())}}
    if isinstance(value,list):
        all_shapes = {json.dumps(schema(v),sort_keys=True) for v in value}
        return {'array_element_schemas':[json.loads(s) for s in sorted(all_shapes)]}
    if value is None:
        return 'null'
    if isinstance(value,bool):
        return 'boolean'
    if isinstance(value,int):
        return 'integer'
    if isinstance(value,float):
        return 'number'
    return 'string'

def file_identity(p):
    data=p.read_bytes()
    return {'bytes':len(data),'sha256':sha(data),'git_blob_sha':hashlib.sha1(
        ('blob '+str(len(data))+'\0').encode()+data).hexdigest(),
        'disk_mode':oct(stat.S_IMODE(p.stat().st_mode))}

receipt = {'created_utc':utc(),'head':H,'base':B,'author':AUTHOR}
try:
    receipt['branch_before']=capture('branch_before',['git','branch','--show-current']).decode().strip()
    capture('frozen_head_commit',['git','show','--no-patch','--format=fuller',H])
    capture('frozen_base_commit',['git','show','--no-patch','--format=fuller',B])
    capture('scope_diff',['git','diff','--name-status',B,H,'--',FOLDER,'unsolved_math_prioritization/QUEUE.md'])
    tree_data=capture('frozen_tree',['git','ls-tree','-r',H,'--',FOLDER,'unsolved_math_prioritization/QUEUE.md'])
    tree={}
    for line in tree_data.decode().splitlines():
        info,path=line.split('\t',1)
        mode,kind,blob=info.split()
        tree[path]={'git_mode':mode,'git_kind':kind,'git_blob_sha':blob}
    capture('api_frozen_head',['gh','api',f'repos/AlecKriebel/Math/commits/{H}'])
    remote={}
    for label,directory in [('api_packet_listing',FOLDER),('api_review_listing',FOLDER+'/review')]:
        data=parse(capture(label,['gh','api',f'repos/AlecKriebel/Math/contents/{directory}?ref={H}']))
        for item in data:
            if item['type']=='file':
                remote[item['path']]={'sha':item['sha'],'size':item['size'],'type':item['type']}
    queue_path='unsolved_math_prioritization/QUEUE.md'
    q=parse(capture('api_queue',['gh','api',f'repos/AlecKriebel/Math/contents/{queue_path}?ref={H}']))
    remote[queue_path]={'sha':q['sha'],'size':q['size'],'type':q['type']}
    disk={str(p.relative_to(SNAPSHOT)):p for p in PACKET.rglob('*') if p.is_file()}
    disk[queue_path]=SNAPSHOT/queue_path
    assert set(disk)==set(tree)==set(remote)
    identities=[]
    for index,(path,p) in enumerate(sorted(disk.items())):
        assert not p.is_symlink()
        local=p.read_bytes()
        git=capture('git_file_'+str(index).zfill(3),['git','show',H+':'+path])
        api=parse(capture('api_blob_'+str(index).zfill(3),['gh','api',f'repos/AlecKriebel/Math/git/blobs/{remote[path]["sha"]}']))
        assert api['encoding']=='base64'
        api_bytes=base64.b64decode(api['content'],validate=False)
        identity=file_identity(p)
        assert local==git==api_bytes
        assert identity['bytes']==remote[path]['size']==api['size']
        assert identity['git_blob_sha']==tree[path]['git_blob_sha']==remote[path]['sha']==api['sha']
        assert tree[path]['git_kind']=='blob' and tree[path]['git_mode'] in ('100644','100755')
        assert bool(p.stat().st_mode & stat.S_IXUSR)==(tree[path]['git_mode']=='100755')
        identities.append({'path':path,**identity,**tree[path],'git_api_disk_full_bytes_identical':True})
    receipt['file_identities']=identities
    receipt['all_files_count']=len(identities)
    manifests=[]
    for p in sorted(PACKET.rglob('*MANIFEST.json')):
        m=parse(p.read_bytes())
        entries=[]
        seen=set()
        for row in m['files']:
            name=row.get('path',row.get('name'))
            assert name not in seen
            seen.add(name)
            rel=Path(name)
            assert not rel.is_absolute() and '..' not in rel.parts
            assert type(row['bytes']) is int and row['bytes']>=0
            assert len(row['sha256'])==64 and set(row['sha256'])<=set('0123456789abcdef')
            target=p.parent/rel
            if p.name=='SOURCE_MANIFEST.json':
                target=ROOT/'private'/'candidate_source_aliases'/name
            if target.exists():
                raw=target.read_bytes()
                valid=len(raw)==row['bytes'] and sha(raw)==row['sha256']
                assert valid
                entries.append({'path':name,'actual':file_identity(target),'valid':True})
            else:
                entries.append({'path':name,'valid':None,'reason':'source bytes unavailable; not asserted verified'})
        chain=[]
        for key,name,base in [('previous_manifest_sha256','TURN_1_MANIFEST.json' if p.name=='TURN_2_MANIFEST.json' else 'TURN_2_MANIFEST.json',PACKET),
                              ('author_manifest_sha256','FINAL_AUTHOR_MANIFEST.json',PACKET)]:
            if key in m:
                actual=sha((base/name).read_bytes())
                assert actual==m[key]
                chain.append({'field':key,'target':name,'sha256':actual,'valid':True})
        manifests.append({'path':str(p.relative_to(PACKET)),'complete_schema':schema(m),
                          'entries':entries,'entry_count':len(entries),'chain_bindings':chain})
    receipt['nested_manifests']=manifests
    # Whole old bytes, not merely a count or hash: compare every entry in the
    # old author API listing against the frozen head and the old Git blob.
    old=parse(capture('api_author_listing',['gh','api',f'repos/AlecKriebel/Math/contents/{FOLDER}?ref={AUTHOR}']))
    old_comparisons=[]
    for i,row in enumerate(old):
        if row['type']!='file':
            continue
        old_bytes=capture('git_author_file_'+str(i).zfill(3),['git','show',AUTHOR+':'+row['path']])
        current=(SNAPSHOT/row['path']).read_bytes()
        assert old_bytes==current
        assert row['sha']==hashlib.sha1(('blob '+str(len(old_bytes))+'\0').encode()+old_bytes).hexdigest()
        old_comparisons.append({'path':row['path'],'old_bytes':len(old_bytes),
                                'full_old_bytes_equal_frozen_head':True,'sha256':sha(old_bytes),
                                'old_git_api_blob_sha':row['sha']})
    receipt['old_author_full_byte_comparisons']=old_comparisons
    old_queue=capture('git_base_queue',['git','show',B+':'+queue_path])
    new_queue=(SNAPSHOT/queue_path).read_bytes()
    diff=''.join(difflib.unified_diff(old_queue.decode().splitlines(True),new_queue.decode().splitlines(True),fromfile=B,tofile=H))
    (CAPTURE/'queue_full_byte_difference.diff').write_text(diff)
    relevant=lambda raw:[{'line':i+1,'text':line} for i,line in enumerate(raw.decode().splitlines()) if '30001370' in line]
    receipt['queue']={'base_rows':relevant(old_queue),'head_rows':relevant(new_queue),
                      'base_bytes':len(old_queue),'head_bytes':len(new_queue),
                      'complete_diff_path':'private/bindings/queue_full_byte_difference.diff'}
    receipt['branch_after']=capture('branch_after',['git','branch','--show-current']).decode().strip()
    assert receipt['branch_before']==receipt['branch_after']=='main'
    receipt['status']='PASS_READ_ONLY_BINDING'
except Exception as error:
    receipt['status']='FAIL_PRESERVED'
    receipt['failure']=str(error)
    raise
finally:
    receipt['native_commands']=records
    receipt['finished_utc']=utc()
    receipt['scope']='Custody, manifest schemas and preserved full byte comparisons only; not proof or novelty certification.'
    (ROOT/'public'/'PACKET_CUSTODY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'files':receipt.get('all_files_count'),
                  'manifest_entries':sum(m['entry_count'] for m in receipt.get('nested_manifests',[])),
                  'whole_native_commands':len(records)},indent=2))
