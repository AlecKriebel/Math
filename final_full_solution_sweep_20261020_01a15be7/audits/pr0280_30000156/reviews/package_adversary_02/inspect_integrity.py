#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,re,zipfile
BASE=Path(__file__).resolve().parent
AUDIT=BASE.parents[1]
TREE=BASE/'archive/birational-cycle-verification'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def seal_check(manifest,root):
    m=json.loads(manifest.read_text());rows=[]
    for entry in m['files']:
        p=root/entry['path'];data=p.read_bytes()
        ok=len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
        if not ok:raise RuntimeError(str(p))
        rows.append({'path':entry['path'],'bytes':len(data),'sha256':digest(p),'pass':True})
    return {'manifest':str(manifest.relative_to(AUDIT)),'sha256':digest(manifest),'count':len(rows),'files':rows}

def main():
    result={'status':'PASS','seals':[]}
    for name,root in [('MANIFEST.json',TREE),('original/FROZEN_MANIFEST.json',TREE/'original'),
            ('original/independent_review/REVIEW_MANIFEST.json',TREE/'original/independent_review'),
            ('historical_reviews/arithmetic_falsification/OUTPUT_MANIFEST.json',TREE/'historical_reviews/arithmetic_falsification'),
            ('historical_reviews/source_quantifiers/ARTIFACT_MANIFEST.json',TREE/'historical_reviews/source_quantifiers')]:
        result['seals'].append(seal_check(TREE/name,root))
    snapshot=json.loads((TREE/'SOURCE_SNAPSHOT.json').read_text());original=[]
    for e in snapshot['files']:
        p=TREE/e['snapshot'];data=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if len(data)!=e['bytes'] or digest(p)!=e['sha256'] or blob!=e['git_blob']:raise RuntimeError(e)
        original.append({'snapshot':e['snapshot'],'pass_sha256_length_gitblob':True})
    result['original_files']=original
    result['seals'].append(seal_check(AUDIT/'reviews/package_adversary_01/AUTHORED_FILE_MANIFEST.json',AUDIT/'reviews/package_adversary_01'))
    result['seals'].append(seal_check(AUDIT/'publication_support/schema_integer_repair_20261021/REPAIR_OUTPUT_MANIFEST.json',AUDIT))
    result['seals'].append(seal_check(AUDIT/'preprint/prior_review_01_full/publication_support/PREPARATION_OUTPUT_MANIFEST.json',AUDIT/'preprint/prior_review_01_full'))
    old=AUDIT/'preprint/prior_review_01_full/preprint/publication'
    current=BASE/'bound'
    with zipfile.ZipFile(old/'fixed-birational-cycle-nonlimit-verification.zip') as a,zipfile.ZipFile(current/'fixed-birational-cycle-nonlimit-verification.zip') as b:
        if a.namelist()!=b.namelist():raise RuntimeError('Member list changed')
        changed=[n for n in a.namelist() if a.read(n)!=b.read(n)]
        if changed!=['birational-cycle-verification/MANIFEST.json','birational-cycle-verification/verify.py']:raise RuntimeError(changed)
        result['changed_archive_members']=changed;result['unchanged_archive_payloads']=63
        result['old_zip_sha256']=digest(old/'fixed-birational-cycle-nonlimit-verification.zip')
        result['old_schema_guard']=a.read('birational-cycle-verification/verify.py').decode().splitlines()[21:24]
        result['new_schema_guard']=b.read('birational-cycle-verification/verify.py').decode().splitlines()[21:25]
    result['outer_unchanged']={n:(old/n).read_bytes()==(current/n).read_bytes() for n in ['fixed-birational-cycle-nonlimit.pdf','fixed-birational-cycle-nonlimit.tex','zenodo-deposit.json','README.md']}
    if not all(result['outer_unchanged'].values()):raise RuntimeError('Unexpected outer change')
    if (TREE/'paper/main.tex').read_bytes()!=(current/'fixed-birational-cycle-nonlimit.tex').read_bytes():raise RuntimeError('TeX mismatch')
    result['tex_inside_outside_identical']=True
    current_releases=json.loads((current/'RELEASE_FILES.json').read_text())
    for entry in current_releases['files']:
        p=current/entry['path']
        if p.stat().st_size!=entry['bytes'] or digest(p)!=entry['sha256']:raise RuntimeError(entry)
    result['outer_five_binding_verified']=True
    # Complete content read/decode/JSON parse, with roles and narrowly targeted exposure screens.
    inventory=[];hits=[]
    expressions={'private_key':r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',
        'credential_assignment':r'(?i)(?:access_token|api_key|refresh_token|password)\s*[=:]\s*["\'][^"\']{12,}',
        'provider_ids':r'(?i)\b(?:zenodo_token|oauth_token|bearer\s+[a-z0-9_-]{20,})',
        'email':r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'}
    for p in sorted(TREE.rglob('*')):
        if not p.is_file():continue
        text=p.read_text(encoding='utf-8');record={'path':p.relative_to(TREE).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p),'utf8':True}
        if p.suffix=='.json':
            x=json.loads(text);record['json_type']=type(x).__name__;record['json_top_keys']=list(x) if isinstance(x,dict) else None
        for label,expression in expressions.items():
            if re.search(expression,text):hits.append({'path':record['path'],'pattern':label})
        inventory.append(record)
    result['archive_inventory']=inventory;result['screen_hits']=hits
    result['all_archive_members_utf8']=True
    return result

if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
