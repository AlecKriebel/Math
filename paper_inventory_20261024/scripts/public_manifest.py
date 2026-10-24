"""Publish public provenance only, excluding private tracker and account drafts."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
corpus=json.loads((HERE/'sources/corpus_records.json').read_text())
groups=json.loads((HERE/'sources/work_group_adjudication.json').read_text())
supp=json.loads((HERE/'sources/supplemental_candidates.json').read_text())['candidates']
primary=[]
for r in corpus['records']:
    if r['classification']!='paper':continue
    primary.append({'record_id':r['id'],'concept_id':r['concept_id'],'title':r['title'],'doi':r['doi'],'record_url':r['record_url'],'publication_date':r['publication_date'],'version':r['version'],'all_paper_version_ids':r['all_paper_version_ids'],'sources':[{k:s[k] for k in ['filename','bytes','pages','md5','sha256','origin']} for s in r['sources']]})
supplemental=[{k:c[k] for k in ['candidate_id','title','sha256','bytes','archive_matches','public_pdf_url','publication_status'] if k in c} for c in supp]
out={'scope':'All published author manuscripts plus individually identifiable historical archive/repository manuscripts; historical byte-level editions and nonpaper artifacts accounted for separately.','as_of':'2026-10-24','primary_manuscripts':primary,'supplemental_manuscripts':supplemental,'scientific_work_group_adjudication':groups,'public_author_identity_reconciliation':json.loads((HERE/'sources/corpus_public_author_search.json').read_text())['summary'],'independent_archive_coverage':json.loads((HERE/'reviews/archive_coverage_independent.json').read_text()),'direct_archive_copy_verification':'All 17 archive/direct duplicate PDF payloads separately downloaded and verified by MD5 and SHA-256.','integrity_limit':'Large ZIP central directories and downloaded member CRC32/size/SHA256 were verified; whole-ZIP advertised MD5 was not independently recomputed. Primary manuscript published MD5 and sizes matched exactly.','privacy':'Private tracker snapshots, unpublished account draft metadata, credentials and extracted source texts are omitted.'}
(HERE/'outputs/source_manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'primary_records':len(primary),'supplemental_entries':len(supplemental),'archive_payloads':groups['archive_pdf_payload_audit']['unique_payloads']}))
