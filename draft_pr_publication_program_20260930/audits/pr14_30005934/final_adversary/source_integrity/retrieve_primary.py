#!/usr/bin/env python3
"""Fresh public primary retrieval; copyrighted source is kept only in ignored tmp."""
from pathlib import Path
from datetime import datetime,timezone
import urllib.request,json,hashlib,concurrent.futures,subprocess,zipfile,io
OUT=Path(__file__).resolve().parent; TMP=OUT/'tmp'; TMP.mkdir(exist_ok=True)
SOURCES={
 'prior_paper.md':'https://raw.githubusercontent.com/ipitchford/wishart-reachable-noise/73dd242a4450400e2f8f16b65929cb77fee76be1/paper.md',
 'prior_commit.json':'https://api.github.com/repos/ipitchford/wishart-reachable-noise/commits/73dd242a4450400e2f8f16b65929cb77fee76be1',
 'prior_paper_git_blob.json':'https://api.github.com/repos/ipitchford/wishart-reachable-noise/git/blobs/54ff9ccf53045aa22230e8f03c4127f54bb98902',
 'zenodo_record.json':'https://zenodo.org/api/records/22892681',
 'zenodo_versions.json':'https://zenodo.org/api/records/22892681/versions',
 'owr.pdf':'https://ems.press/content/serial-article-files/49484',
 'cck_final.pdf':'https://pure.uva.nl/ws/files/234720765/Infinite-dimensional_Wishart_processes.pdf',
 'gmm.pdf':'https://arxiv.org/pdf/1607.00206'}
def get(pair):
 name,url=pair; stamp=datetime.now(timezone.utc).isoformat()
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'independent-research-source-audit/1.0'})
  with urllib.request.urlopen(req,timeout=50) as r: data=r.read(); resolved=r.url; status=r.status
  (TMP/name).write_bytes(data)
  return {'name':name,'url':url,'resolved_url':resolved,'retrieved_utc':stamp,'status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'md5':hashlib.md5(data).hexdigest()}
 except Exception as e: return {'name':name,'url':url,'retrieved_utc':stamp,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool: receipts=list(pool.map(get,SOURCES.items()))
record=json.loads((TMP/'zenodo_record.json').read_text())
file_urls={x['key']:x['links']['self'] for x in record['files']}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: receipts.extend(pool.map(get,file_urls.items()))
checks=[]
for f in record['files']:
 b=(TMP/f['key']).read_bytes(); algo,value=f['checksum'].split(':'); calc=hashlib.new(algo,b).hexdigest()
 checks.append({'file':f['key'],'algorithm':algo,'advertised':value,'computed':calc,'pass':value==calc})
sha_checks=[]
for line in (TMP/'SHA256SUMS').read_text().splitlines():
 h,name=line.split(maxsplit=1); name=name.lstrip('*'); actual=hashlib.sha256((TMP/name).read_bytes()).hexdigest()
 sha_checks.append({'file':name,'advertised':h,'computed':actual,'pass':h==actual})
archive_checks=[]
raw=(TMP/'prior_paper.md').read_bytes(); pdf=(TMP/'wishart-reachable-noise-v0.1.0-candidate.pdf').read_bytes()
for f in record['files']:
 if f['key'].endswith('.zip'):
  with zipfile.ZipFile(TMP/f['key']) as z:
   for n in z.namelist():
    if n.endswith('/paper.md') or n=='paper.md' or n.endswith('/paper.pdf') or n=='paper.pdf':
     b=z.read(n); expected=raw if n.endswith('.md') else pdf
     archive_checks.append({'archive':f['key'],'member':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'pass':b==expected})
import base64
blob=json.loads((TMP/'prior_paper_git_blob.json').read_text()); blob_bytes=base64.b64decode(blob['content'])
commit=json.loads((TMP/'prior_commit.json').read_text())
versions=json.loads((TMP/'zenodo_versions.json').read_text())
commit_paper_blob=next(f['sha'] for f in commit['files'] if f['filename']=='paper.md')
meta={'doi':record.get('doi'),'record_id':record.get('id'),'created':record.get('created'),'updated':record.get('updated'),'publication_date':record['metadata'].get('publication_date'),'version':record['metadata'].get('version'),'title':record['metadata'].get('title'),'creators':record['metadata'].get('creators'),'git_commit':commit.get('sha'),'git_author_name':commit['commit']['author']['name'],'git_author_date':commit['commit']['author']['date'],'git_committer_name':commit['commit']['committer']['name'],'git_committer_date':commit['commit']['committer']['date'],'paper_git_blob':blob.get('sha'),'commit_paper_blob':commit_paper_blob,'paper_git_blob_matches_raw':blob_bytes==raw,'paper_git_object_sha1':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),'version_hits_total':versions.get('hits',{}).get('total'),'version_ids':[x.get('id') for x in versions.get('hits',{}).get('hits',[])]}
receipt={'generated_utc':datetime.now(timezone.utc).isoformat(),'sources':receipts,'archive_md5_checks':checks,'advertised_sha256_checks':sha_checks,'archive_identity_checks':archive_checks,'metadata':meta,'all_downloads_ok':all('error' not in r for r in receipts),'archive_identity_pass':all(x['pass'] for x in checks+sha_checks+archive_checks) and meta['paper_git_blob_matches_raw'] and meta['paper_git_object_sha1']==blob['sha']==commit_paper_blob and commit['sha']=='73dd242a4450400e2f8f16b65929cb77fee76be1' and record.get('doi')=='10.5281/zenodo.22892681'}
(OUT/'primary_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'generated_utc':receipt['generated_utc'],'metadata':meta,'all_downloads_ok':receipt['all_downloads_ok'],'archive_identity_pass':receipt['archive_identity_pass'],'download_count':len(receipts),'md5_count':len(checks),'advertised_sha256_count':len(sha_checks),'archive_member_count':len(archive_checks),'errors':[r for r in receipts if 'error' in r]},indent=2))
