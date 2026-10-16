"""Read-only live provenance checks; no external source content is redistributed."""
from pathlib import Path
from datetime import datetime,timezone
import urllib.request,hashlib,json
OUT=Path(__file__).resolve().parent
CASE=OUT.parent.parent
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical review'}),timeout=30) as r:
        return r.read()
result={'UTC':datetime.now(timezone.utc).isoformat(),'records':[],'file_matches':[]}
record_bytes=fetch('https://zenodo.org/api/records/23267641')
record=json.loads(record_bytes)
m=record['metadata']
result['records'].append({'url':'https://zenodo.org/api/records/23267641','sha256':hashlib.sha256(record_bytes).hexdigest(),
 'created':record.get('created'),'updated':record.get('updated'),'state':record.get('state'),'submitted':record.get('submitted'),
 'metadata':{k:m.get(k) for k in ['title','creators','doi','publication_date','version','access_right']}})
registry_bytes=fetch('https://api.datacite.org/dois/10.5281/zenodo.23267641')
registry=json.loads(registry_bytes)['data']['attributes']
result['records'].append({'url':'https://api.datacite.org/dois/10.5281/zenodo.23267641','sha256':hashlib.sha256(registry_bytes).hexdigest(),
 'summary':{k:registry.get(k) for k in ['created','registered','published','state','doi','version','publicationYear','dates','titles']}})
pr_bytes=fetch('https://api.github.com/repos/AlecKriebel/Math/pulls/152')
pr=json.loads(pr_bytes)
result['records'].append({'url':'https://api.github.com/repos/AlecKriebel/Math/pulls/152','sha256':hashlib.sha256(pr_bytes).hexdigest(),
 'created':pr['created_at'],'head':pr['head']['sha'],'title':pr['title'],'merged':pr['merged'],'state':pr['state']})
website={'AMR-049-paper.pdf':'https://eulersolve.org/papers/amr-049/paper.pdf',
         'AMR-049-source.zip':'https://eulersolve.org/papers/amr-049/source.zip',
         'AMR-049-verification-report.md':'https://eulersolve.org/papers/amr-049/verification_report.md'}
for f in record['files']:
    url=f['links']['self']
    item={'name':f['key'],'declared_size':f['size'],'declared_checksum':f['checksum'],'deposit_url':url}
    try:
        b=fetch(url)
        item.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),md5=hashlib.md5(b).hexdigest())
        item['matches_record']=len(b)==f['size'] and 'md5:'+hashlib.md5(b).hexdigest()==f['checksum']
        if f['key']=='AMR-049-paper.pdf':
            item['matches_private_cached_pdf']=b==(CASE/'priority_exact_history/private_source_cache/ferudun2026.pdf').read_bytes()
    except Exception as e:item['deposit_read_error']=str(e)
    try:
        b=fetch(website[f['key']])
        item['website_bytes']=len(b);item['website_md5']=hashlib.md5(b).hexdigest();item['website_sha256']=hashlib.sha256(b).hexdigest()
        item['website_matches_record']=len(b)==f['size'] and 'md5:'+hashlib.md5(b).hexdigest()==f['checksum']
    except Exception as e:item['website_read_error']=str(e)
    result['file_matches'].append(item)
# Verify frozen original theorem bytes at their exact GitHub head; never change refs.
original='https://raw.githubusercontent.com/AlecKriebel/Math/99ef28d28bf380658400886d1f8c2120a5096d97/unsolved_math_prioritization/attempts/5000006/CANDIDATE.md'
raw=fetch(original)
local=CASE/'original_submission/files/unsolved_math_prioritization/attempts/5000006/CANDIDATE.md'
result['original_head']={'url':original,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'matches_frozen':raw==local.read_bytes()}
(OUT/'live_source_control.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
