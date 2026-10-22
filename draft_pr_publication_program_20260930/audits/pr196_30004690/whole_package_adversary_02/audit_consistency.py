"""Read-only nested custody, duplicate metadata and source-copy consistency checks."""
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parent
CASE=ROOT.parent
X=ROOT/'private'/'extracted'
def need(c,m):
    if not c: raise RuntimeError(m)
def read(p): return json.loads(p.read_bytes())
def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def match(p,v):
    need(pin(p)=={k:v[k] for k in ('bytes','sha256')},str(p))

def main():
    verified=0
    for family in ('contact_geometry_audit_01','legendre_regularity_audit_01','original_source_audit_01','priority_audit_01'):
        d=X/'audits'/family
        m=read(d/'HASH_MANIFEST.json')
        entries=m.get('files',m.get('entries'))
        if isinstance(entries,dict): entries=[dict(v,path=k) for k,v in entries.items()]
        for v in entries:
            match(d/v.get('path',v.get('file')),v); verified+=1
        allow=read(d/'SAFE_ALLOWLIST.json')
        names=next(allow[k] for k in ('safe_authored_files','files','safe_files','exact_safe_files') if k in allow)
        if family=='original_source_audit_01':
            add=read(d/'NORMALIZATION_ADDENDUM_MANIFEST.json')
            for v in add['entries']: match(d/v['path'],v);verified+=1
            need(pin(d/'HASH_MANIFEST.json')['sha256']==add['original_manifest_sha256'],'addendum original manifest')
            names=names+add['safe_files']
        need(set(names)=={p.name for p in d.iterdir()},'audit allowlist '+family)
    custody=read(X/'research'/'ORIGINAL_SUBMISSION_CUSTODY.json')
    need(custody['original_head']=='a229ac722a3b1733bcb590a5f796b4a52f68cc73','head literal')
    need(len(custody['files'])==19,'custody count')
    for name,v in custody['files'].items(): match(X/'original_submitted_head'/name,v);verified+=1
    orig=X/'original_submitted_head'
    for line in (orig/'SHA256SUMS').read_text().splitlines():
        h,n=line.split(None,1);need(pin(orig/n.strip())['sha256']==h,'original SHA256SUMS');verified+=1
    for name,h in read(orig/'CANDIDATE_REVIEW_MANIFEST.json')['files'].items():
        need(pin(orig/name)['sha256']==h,'candidate manifest '+name);verified+=1
    for name,h in read(orig/'independent_review'/'reviewed_hashes.json')['sha256'].items():
        need(pin(orig/name)['sha256']==h,'review manifest '+name);verified+=1
    for name in ('ROOT_THREE_FAMILY_AUTHENTICATION_01.json','ROOT_MATHEMATICAL_GATE_01.json'):
        gate=read(X/'research'/name)
        families=gate.get('three_new_families',gate.get('three_NEW_independent_audit_families'))
        for family,data in families.items():
            d=X/'audits'/family
            match(d/'HASH_MANIFEST.json',data['manifest']);verified+=1
            for n,v in data['safe_files'].items(): match(d/n,v);verified+=1
    gate=read(X/'research'/'ROOT_PRIORITY_GATE_01.json')
    match(X/'research'/'ROOT_MATHEMATICAL_GATE_01.json',gate['mathematical_gate']);verified+=1
    for n,v in gate['safe_priority_files'].items():match(X/'audits'/'priority_audit_01'/n,v);verified+=1
    source=read(X/'SOURCE_REFERENCES.json')
    older=read(X/'audits'/'priority_audit_01'/'SOURCE_ACCESS.json')
    differences=[]
    for new,old in zip(source['sources'],older['sources']):
        need(new['id']==old['id'],'source IDs order')
        for k in set(new)|set(old):
            if new.get(k)!=old.get(k): differences.append({'source':new['id'],'field':k,'current':new.get(k),'audit':old.get(k)})
        for field,kind in [('file','file'),('text','text')]:
            if field in new:
                basename=Path(new[field]).name
                paths=[CASE/'private_primary_sources'/basename,CASE/'priority_audit_01'/'private'/basename]
                p=next(p for p in paths if p.is_file())
                need(pin(p)=={'bytes':new[kind+'_bytes'],'sha256':new[kind+'_sha256']},'source copy '+basename);verified+=1
    need(source['access_gaps']==older['access_gaps'],'access gaps duplicated')
    q=read(X/'audits'/'priority_audit_01'/'QUERY_LOG.json')
    need(len(source['sources'])==18 and len(q['queries'])==64,'coverage counts')
    need([v['id'] for v in q['queries']]==['Q%03d'%i for i in range(1,65)],'query IDs')
    need(read(X/'PUBLICATION_METADATA.json')==read(CASE/'publication_package_v1'/'zenodo-deposit.json')['metadata'],'metadata exact duplication')
    need(read(ROOT/'private'/'replay-normal.json')==read(ROOT/'private'/'replay-optimized.json')==read(CASE/'publication_package_v1'/'verification_stdout.json'),'replays')
    result={'verdict':'PASS_NESTED_CONSISTENCY','pin_comparisons':verified,
            'source_entries':18,'discovery_query_entries':64,'original_custody_files_verified':19,
            'metadata_exact_match':True,'normal_and_optimized_wrapper_exact_match':True,
            'source_record_differences':differences,
            'historical_commit_authentication_scope':'Authenticated submitted bytes against fixed custody/manifests; did not query Git or any remote history.'}
    (ROOT/'CONSISTENCY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
