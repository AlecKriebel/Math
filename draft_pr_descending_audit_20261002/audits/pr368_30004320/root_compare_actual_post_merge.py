"""Compare every post-merge stream and the entire independent/root receipts.

Runtime dates and owned run locations are explicitly validated. Complete
JSON streams are compared structurally (including every field); text streams
are compared in full. No mathematical or file-scope field is discarded.
"""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import gzip,hashlib,json,re

A=Path(__file__).resolve().parent
F=A/'clean_final_adversary/post_merge'
CASES=[F/'runs/clean_post_20261003_04',F/'private_runs/root_post_replay_01']
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
checks=[];events=[];pairs=[]
def ck(v,label):
    assert v,label
    checks.append({'check':label,'pass':True})
def load(p):return json.loads(p.read_bytes())
receipts=[load(d/'RECEIPT.json') for d in CASES]
inv=[load(d/'EVERY_SAVED_GZIP.json') for d in CASES]
epochs=[(datetime.fromisoformat(r['start_utc']),datetime.fromisoformat(r['end_utc'])) for r in receipts]
maps=[];ids=[];captures=[];raws=[];raw_norms=[];norm_rows=[]
for side,(d,j,i) in enumerate(zip(CASES,receipts,inv)):
    ck(j['status']=='PASS_ACTUAL_POST_MERGE_UNSOLVED5' and j['check_count']==9546==len(j['checks']) and all(r['pass'] for r in j['checks']),'entire successful9546 receipt '+str(side))
    ck(j['program_sha256']==sha((F/'audit_actual_post_merge.py').read_bytes()),'literal complete executed program '+str(side))
    ck(j['literal_merge']=={'commit':'2da0adc1c56dbb15e53be162489eb001cfa83e03','merged_at':'2026-10-03T14:12:44Z','ordered_parents':['4b1fe16ffa841df9cefffe9479b05bbf950e423b','e8a53a05b309bda2a7d60136d8fb5a4e21e313fd'],'tree':'902a46b4ec28f332f7ef0228d8e6bca3736a0031','body_sha256':'99128f750a529174a631fd97600e4809f18c1054c0ef115b57e5838b4dff64fc','original_head':'74617174ddfb3ea726cea343a4ba915613724bdc'},'literal actual accepted merge '+str(side))
    ref=j['EVERY_saved_gzip_inventory'];b=(d/ref['path']).read_bytes()
    ck(len(b)==ref['bytes'] and sha(b)==ref['sha256'],'whole inventory receipt binding '+str(side))
    rows={r['path']:r for r in i['all_files']}
    ck(len(rows)==1484==i['saved_gzip_streams'] and set(rows)=={p.relative_to(d).as_posix() for p in d.rglob('*.gz') if p.is_file()},'closed EVERY1484 gzip inventory '+str(side))
    maps.append(rows);data={}
    for p,r in rows.items():
        z=(d/p).read_bytes();b=gzip.decompress(z)
        ck(len(z)==r['gzip_bytes'] and sha(z)==r['gzip_sha256'] and len(b)==r['bytes'] and sha(b)==r['sha256'],'whole compressed/raw binding '+str(side)+'/'+p)
        data[p]=b
    raws.append(data)
    groups=defaultdict(list)
    for c in j['all_complete_command_captures']:
        a=datetime.fromisoformat(c['start_utc']);b=datetime.fromisoformat(c['end_utc'])
        ck(epochs[side][0]<=a<=b<=epochs[side][1],'full captured UTC interval '+str(side)+'/'+str(c['id']))
        command=[v.replace(str(d),'OWN_RUN') for v in c['command']]
        cwd=c['cwd'].replace(str(d),'OWN_RUN')
        key=canon([command,cwd]).decode();groups[key].append(c)
    captures.append(groups);ids.append({})
ck(captures[0].keys()==captures[1].keys(),'full command/cwd multiset keys')
bindings=[{},{}]
for key in sorted(captures[0]):
    left=sorted(captures[0][key],key=lambda c:c['id']);right=sorted(captures[1][key],key=lambda c:c['id'])
    ck(len(left)==len(right),'complete command occurrence count '+key)
    for occurrence,(x,y) in enumerate(zip(left,right)):
        name=sha(key.encode())+'_'+str(occurrence)
        for side,c in enumerate((x,y)):
            ids[side][c['id']]=name
            for channel in ('stdout','stderr'):
                r=c[channel]
                if 'path' in r:bindings[side][r['path']]=name+'/'+channel
for side in range(2):
    for p in maps[side]:
        if p not in bindings[side]:
            ck(p.startswith('program_streams/negative_'),'only actual negative extras '+p)
            bindings[side][p]=p
    ck(len(set(bindings[side].values()))==1484,'unique canonical full stream paths '+str(side))
ck(set(bindings[0].values())==set(bindings[1].values()),'entire canonical1484 paired stream scope')

raw_lookup=[{sha(b):b for b in side.values()} for side in raws]
runtime_keys={'utc','start_utc','end_utc','start_utc','end_utc',
              'download_started_utc','download_finished_utc'}
id_prefixes=('unique captured command','actual captured command interval',
 'successful or explicitly unavailable local commit probe','full command inventory reference',
 'huge Git map explicit nonretention','complete API raw stays private')
def scalar(value,side,path):
    if not isinstance(value,str):return value
    s=value.replace(str(CASES[side]),'OWN_RUN')
    if 'private/raw_streams/' in s or 'program_streams/' in s:
        for old,new in sorted(bindings[side].items(),key=lambda x:-len(x[0])):
            if old in s:s=s.replace(old,new)
    for prefix in id_prefixes:
        match=re.match(re.escape(prefix)+r' (\d+)(.*)$',s)
        if match:
            number=int(match[1]);ck(number in ids[side],'literal capture id reference '+s)
            s=prefix+' '+ids[side][number]+match[2]
    return s
def normal(value,side,path=()):
    if isinstance(value,dict):
        if 'stderr_sha256' in value and 'stderr_bytes' in value and value['stderr_sha256'] in raw_lookup[side]:
            raw=raw_lookup[side][value['stderr_sha256']]
            ck(len(raw)==value['stderr_bytes'],'complete stream negative stderr binding '+str(path))
            nb=raw.replace(str(CASES[side]).encode(),b'OWN_RUN')
            value={**value,'stderr_bytes':len(nb),'stderr_sha256':sha(nb)}
        result={}
        for k,v in value.items():
            p=path+(k,)
            if k in runtime_keys and isinstance(v,str):
                t=datetime.fromisoformat(v)
                if epochs[side][0]<=t<=epochs[side][1]:
                    result[k]='VALIDATED_CURRENT_RUN_UTC';events.append({'side':side,'path':list(p),'utc':v});continue
            if k=='repo' and isinstance(v,dict):
                copy=dict(v)
                for name in ('open_issues','open_issues_count','size'):
                    if name in copy:
                        ck(type(copy[name]) is int and copy[name]>=0,'actual repo counter type '+str(p+(name,)))
                        copy[name]='VALIDATED_VOLATILE_REPO_COUNTER'
                if 'pushed_at' in copy:
                    t=datetime.fromisoformat(copy['pushed_at'].replace('Z','+00:00'))
                    ck(t<=epochs[side][1],'actual repo pushed_at is not future')
                    copy['pushed_at']='VALIDATED_REPO_PUSH_TIME'
                result[k]=normal(copy,side,p);continue
            result[k]=normal(v,side,p)
        return result
    if isinstance(value,list):return [normal(v,side,path+(i,)) for i,v in enumerate(value)]
    return scalar(value,side,path)
def normalized_stream(b,side):
    try:return canon(normal(json.loads(b),side))
    except (json.JSONDecodeError,UnicodeDecodeError):
        return b.replace(str(CASES[side]).encode(),b'OWN_RUN')
for side in range(2):
    raw_norms.append({});nr={}
    for p,r in maps[side].items():
        b=raws[side][p];nb=normalized_stream(b,side)
        raw_norms[side][sha(b)]=(b,nb)
        row={**r,'path':bindings[side][p],'bytes':len(nb),'sha256':sha(nb),
             'gzip_bytes':len(gzip.compress(nb,mtime=0)),'gzip_sha256':sha(gzip.compress(nb,mtime=0))}
        nr[p]=row
    norm_rows.append(nr)
left_by_name={v:k for k,v in bindings[0].items()};right_by_name={v:k for k,v in bindings[1].items()}
for name in sorted(left_by_name):
    p=left_by_name[name];q=right_by_name[name]
    a=raws[0][p];b=raws[1][q]
    ck(normalized_stream(a,0)==normalized_stream(b,1),'every full paired raw stream '+name)
    ck(norm_rows[0][p]==norm_rows[1][q],'every full canonical stream row '+name)
    pairs.append({'canonical_command_channel':name,'agent_path':p,'root_path':q,
                  'agent_raw_bytes':len(a),'root_raw_bytes':len(b),
                  'agent_raw_sha256':sha(a),'root_raw_sha256':sha(b),
                  'byte_equal':a==b,'complete_normalized_sha256':sha(normalized_stream(a,0))})
def receipt_normal(v,side,path=()):
    if isinstance(v,dict):
        if 'gzip_sha256' in v and 'path' in v:
            ck(v==maps[side][v['path']],'whole nested stream record '+str(path))
            return norm_rows[side][v['path']]
        if set(v)=={'reference','bytes','sha256','scalar_leaves','complete_leaf_digest'}:
            if v['sha256'] in raw_norms[side]:
                b,nb=raw_norms[side][v['sha256']]
                ck(len(b)==v['bytes'],'whole original parsed JSON byte count '+v['reference'])
                obj=json.loads(b);leaves=[]
                def walk(x,p=()):
                    if isinstance(x,dict):
                        for k,y in sorted(x.items()):walk(y,p+(k,))
                    elif isinstance(x,list):
                        for i,y in enumerate(x):walk(y,p+(i,))
                    else:leaves.append([list(p),type(x).__name__,x])
                walk(obj)
                ck(len(leaves)==v['scalar_leaves'] and sha(canon(leaves))==v['complete_leaf_digest'],'every original parsed JSON scalar '+v['reference'])
                return {'reference':scalar(v['reference'],side,path),'complete_normalized_JSON_bytes':len(nb),'complete_normalized_JSON_sha256':sha(nb),'complete_scalar_count':len(leaves)}
            return normal(v,side,path)
        if 'stderr_sha256' in v and 'stderr_bytes' in v:
            raw,nb=raw_norms[side][v['stderr_sha256']]
            ck(len(raw)==v['stderr_bytes'],'every negative complete stderr byte binding '+str(path))
            v={**v,'stderr_bytes':len(nb),'stderr_sha256':sha(nb)}
        out={}
        for k,x in v.items():
            if k in {'id','capture_id'} and isinstance(x,int):
                ck(x in ids[side],'nested full capture id '+str(path+(k,)));out[k]=ids[side][x]
            elif k in runtime_keys:out[k]=normal({k:x},side,path)[k]
            else:out[k]=receipt_normal(x,side,path+(k,))
        return out
    if isinstance(v,list):return [receipt_normal(x,side,path+(i,)) for i,x in enumerate(v)]
    return scalar(v,side,path)
normalized=[]
for side,j in enumerate(receipts):
    out=receipt_normal(j,side)
    inventory=normal(inv[side],side)
    inventory['all_files']=sorted(norm_rows[side].values(),key=lambda r:r['path'])
    expected=receipts[side]['EVERY_saved_gzip_inventory']
    out['EVERY_saved_gzip_inventory']={**expected,'bytes':len(canon(inventory)),'sha256':sha(canon(inventory))}
    for name in ('checks','all_complete_JSON_parse_identity_records','all_complete_API_tree_chunks','all_complete_command_captures'):
        out[name]=sorted(out[name],key=lambda r:canon(r))
    normalized.append(out)
ck(normalized[0].keys()==normalized[1].keys(),'entire receipt key scope')
for key in normalized[0]:
    ck(normalized[0][key]==normalized[1][key],'every complete post receipt section '+key)
companions=[load(F/'COMPLETE_POST_EVIDENCE.json'),load(A/'root_post_complete_evidence.json')]
for side,c in enumerate(companions):
    ck(c['status']=='PASS_ALL_POST_MERGE_EVIDENCE' and c['full_semantic_checks']==9337==len(c['checks']) and all(r['pass'] for r in c['checks']),'whole evidence9337 '+str(side))
    t=datetime.fromisoformat(c['utc']);ck(epochs[side][1]<=t<=datetime.now(timezone.utc),'actual evidence companion after complete run '+str(side))
    c['utc']='VALIDATED_POSTRUN_VALIDATOR_UTC'
    c['checks']=sorted([normal(x,side) for x in c['checks']],key=lambda x:canon(x))
ck(companions[0]==companions[1],'every full companion semantic check and field')
manifest=load(F/'PUBLIC_MANIFEST.json')
ck(sha((F/'PUBLIC_MANIFEST.json').read_bytes())=='5d2c815afeac84953af1f156a62980e7b27a947a993e5e115b9e25164aedb0f9' and len(manifest['files'])==60,'literal closed sealed60 post packet')
for r in manifest['files']:
    b=(F/r['path']).read_bytes();ck(len(b)==r['bytes'] and sha(b)==r['sha256'],'entire sealed post artifact '+r['path'])
report={'status':'PASS_ALL_ACTUAL_POST_RECEIPTS_AND1484_STREAMS','utc':datetime.now(timezone.utc).isoformat(),
        'check_count':len(checks),'checks':checks,'complete_audit_checks_each':9546,
        'complete_evidence_checks_each':9337,'paired_complete_gzip_streams':1484,
        'pairs':pairs,'validated_runtime_dates':events,'all_receipt_sections_compared':list(normalized[0]),
        'accepted_status':'unsolved','original_problem_resolution_percent':0,'workflow_completion_percent':100}
(A/'root_actual_post_comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in {'checks','pairs','validated_runtime_dates','all_receipt_sections_compared'}},indent=2))
