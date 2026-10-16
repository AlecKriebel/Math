#!/usr/bin/env python3
"""Explicit before maps and noncircular packaging; never installed in the kit."""
import collections, datetime, hashlib, json, os, zipfile
from pathlib import Path
W=Path(__file__).resolve().parent; A=W.parents[1]; D=A/'preprint_v1_0'; K=D/'verification_kit'
def obj(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):
    q=p.with_name(p.name+'.archive_wording01-new');q.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');os.replace(q,p)
def row(p,root,key='path'): return {key:p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
if (W/'PACKAGING_COMPLETE.json').exists(): raise RuntimeError('One-shot packaging already complete')
before=obj(W/'BEFORE_COPIES.json')['files'];byname={r['original_path']:r for r in before};hashes=collections.defaultdict(list)
for r in before:hashes[(r['bytes'],r['sha256'])].append(r)
res=[]
def walk(v,pointer,source):
    if isinstance(v,dict):
        if type(v.get('bytes')) is int and isinstance(v.get('sha256'),str):
            for b in hashes.get((v['bytes'],v['sha256']),[]):
                res.append({'source_inventory':source,'source_snapshot':byname[source]['source_snapshot'] if source in byname else source,
                  'json_pointer':pointer,'original_pin':v,'changed_current_path':b['original_path'],
                  'exact_local_before':b['source_snapshot'],
                  'delivered_before':None if b['original_path'].endswith('.zip') else 'archive_wording01_history/before/'+b['original_path'],
                  'disposition':'old_archive_local_only_not_newly_packed' if b['original_path'].endswith('.zip') else 'exact_delivered_before_bytes'})
        for k,x in v.items():walk(x,pointer+'/'+str(k).replace('~','~0').replace('/','~1'),source)
    elif isinstance(v,list):
        for i,x in enumerate(v):walk(x,pointer+'/'+str(i),source)
for r in obj(W/'IMMEDIATE_INPUT_PINS.json')['files']:
    n=r['path']
    if not n.endswith('.json'):continue
    p=A/(byname[n]['source_snapshot'] if n in byname else n)
    try:walk(obj(p),'',n)
    except (ValueError,UnicodeDecodeError):pass
dump(W/'INDIVIDUAL_CHANGED_OLD_PIN_RESOLUTIONS.json',{'scope':'Every preexisting structured size/SHA pin naming any of eight immediately changed bytes, resolved to exact before snapshots without rewriting a stale old pointer. Source snapshots explicitly identify changed source inventories.','references':res})
dump(K/'ARCHIVE_WORDING01_BEFORE_MAP.json',{'scope':'Exact before interface map. The old ZIP is local-only; all other before bytes are delivered. No historical row is rewritten.','files':[{**r,'delivered_before':None if r['original_path'].endswith('.zip') else 'archive_wording01_history/before/'+r['original_path'],'reason':'Old ZIP deliberately not newly packed; retained exact locally only.' if r['original_path'].endswith('.zip') else 'Exact immediate before bytes.'} for r in before]})
dump(K/'ARCHIVE_WORDING01_OLD_PIN_RESOLUTIONS.json',obj(W/'INDIVIDUAL_CHANGED_OLD_PIN_RESOLUTIONS.json'))
sources=obj(A/'reviews/package_03/SOURCE_READ_LEDGER.json')['sources']
dump(K/'ARCHIVE_WORDING01_SOURCE_BODY_OMISSIONS.json',{'scope':'Individually disclosed third-party primary bodies named by the newly selected authored source-interface ledger. Metadata is delivered; no third-party body or extraction is newly copied. These omissions do not alter the old 1434 omission rows.','files':[{'source':r['source'],'original_path':r['path'],'bytes':r['bytes'],'sha256':r['sha256'],'disposition':'omitted','reason':'Third-party primary body retained at its existing audit source path only; selected authored ledger preserves source version, hash, actual historical reading scope and access limits. This repair performs no fresh source reading or body copy.'} for r in sources]})
names=sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file())
allow=obj(K/'ALLOWLIST.json');allow['members']=names;dump(K/'ALLOWLIST.json',allow)
manifest=obj(K/'MANIFEST.json');manifest['files']=[row(K/n,K) for n in names if n!='MANIFEST.json'];dump(K/'MANIFEST.json',manifest)
temp=D/'verification_kit.zip.archive_wording01-new'
with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_STORED) as z:
    for n in names:
        i=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=0;i.flag_bits=0;z.writestr(i,(K/n).read_bytes())
os.replace(temp,D/'verification_kit.zip')
b=obj(D/'EXTERNAL_BINDING.json');b['as_of_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();b['scope']='External noncircular archive-wording successor binding. Three completed whole reviews, latest whole03 one P3; bounded wording correction pending ROOT adoption and NEW complete whole04. Historical checkpoint objects and verifier remain unchanged; no readiness or publication clearance.'
b['manifest_sha256']=sha(K/'MANIFEST.json');b['archive']=row(D/'verification_kit.zip',D,'filename');b['external_files']=[row(D/r['filename'],D,'filename') for r in b['external_files']]
b['current_archive_wording_status']=row(D/'CURRENT_ARCHIVE_WORDING_REPAIR01.json',D,'filename');dump(D/'EXTERNAL_BINDING.json',b)
dump(W/'PACKAGING_COMPLETE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'members':len(names),'manifest_payloads':len(names)-1,'new_individual_old_pin_resolutions':len(res),'new_individual_source_body_omissions':len(sources),'archive':b['archive'],'current_status_binding':b['current_archive_wording_status']})
print(json.dumps(obj(W/'PACKAGING_COMPLETE.json'),indent=2))
