from pathlib import Path
import json, hashlib, datetime
HERE=Path(__file__).resolve().parent
pins=json.loads((HERE/'REVIEWED_HASHES.json').read_text())
for row in pins['files']:
 data=Path(row['path']).read_bytes()
 assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
sourcepaths=[
('RGK final DOI 10.1007/s40598-021-00174-y','/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/tmp/pdfs/reznik-published.pdf','https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf','Printed pages 343, 346; Table 4 k307 and complete Section 3.4; page 346 rendered'),
('Bialy-Tabachnikov','/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/tmp/pdfs/bialy-tabachnikov.pdf','https://doi.org/10.1007/s40879-020-00428-7','Theorem 4.1 and proof; Theorem 4.3 symmetry paragraph'),
('Schwartz-Tabachnikov','/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/priority_billiards_adversary_01/tmp/pdfs/schwartz-tabachnikov-2016.pdf','https://arxiv.org/abs/1607.04766','Lemma 2.1, Theorem 1 and surrounding signed moment/locus scope')]
sources=[]
for title,path,url,scope in sourcepaths:
 data=Path(path).read_bytes()
 sources.append({'title':title,'private_local_path':path,'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'inspected_scope':scope})
rec={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'bounded source-credit consistency, not a new priority search','sources':sources,'web_read_receipts':[
{'url':'https://doi.org/10.1007/s40598-021-00174-y','result':'web resolver unavailable; final journal-hosted original read successfully'},
{'url':'https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf','result':'web original PDF read, DOI/title/pages/target match'},
{'url':'https://arxiv.org/abs/2004.12497v11','result':'web original metadata read; title/authors/version/journal DOI match'}],
'finding':'Original k307 credited correctly; signed quotient and even/all-M historical observation match source. BT arithmetic vertex mean is distinguished from area centroid. ST signed locus work is credited without being used as a covering proof. Bounded reports do not certify firstness.',
'reviewed_candidate_unchanged':True}
(HERE/'SOURCE_AND_FINAL_INTEGRITY_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
