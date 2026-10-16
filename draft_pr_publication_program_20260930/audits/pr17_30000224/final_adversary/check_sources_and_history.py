#!/usr/bin/env python3
"""Verify source bytes, version receipts and precise historical/current separation."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import subprocess

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=BASE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
ledger=read(BASE/'primary_scope_family/source_ledger.json')
sources=[]
for entry in ledger['sources']:
    if entry.get('status')!='ok':continue
    key=entry['key']
    candidates=[p for p in (BASE/'primary_scope_family/tmp').glob(key+'.*') if p.suffix=='.pdf']
    if not candidates: candidates=[p for p in (BASE/'primary_scope_family/tmp').glob(key+'.*') if p.suffix=='.json']
    if not candidates: continue
    p=candidates[0]
    assert sha(p)==entry['sha256'] and p.stat().st_size==entry['bytes'],key
    sources.append({'key':key,'url':entry['url'],'path':str(p.relative_to(ROOT)),
                    'sha256':sha(p),'bytes':p.stat().st_size,'ledger_bytes_identical':True})
algebra=read(BASE/'algebra_family/evidence/primary_source_receipts.json')
for entry in algebra['records']:
    if entry.get('status')!='retrieved':continue
    p=BASE/'algebra_family'/entry['pdf']
    txt=BASE/'algebra_family'/entry['text']
    assert sha(p)==entry['pdf_sha256'] and sha(txt)==entry['text_sha256']

locations=[
 ('OWR19/2005','primary_scope_family/tmp/owr19_2005.pdf','1116 / PDF44','exact map and arbitrary ideal; i>=3 visually confirmed'),
 ('Singh-Walther v2','primary_scope_family/tmp/singh_walther_v2.pdf','PDF8, Example3.5 and Question3.6','exact unrestricted scope; i>=3 visually confirmed'),
 ('MSS v3','primary_scope_family/tmp/ma_schwede_shimomoto_v3_export.pdf','PDF14,16,17; Props4.4/4.9, Cor4.10','seminormality necessity, full criterion proofs, nonpositive degree boundary'),
 ('Boix-Eghbali v2','primary_scope_family/tmp/boix_eghbali_v2.pdf','PDF4-6,18-19; Notation2.1/2.6, Remark5.7, Thm5.8','full relevant conditional theorem and proof; linkage premises not unconditional'),
 ('Hassanzadeh v2','primary_scope_family/tmp/hassanzadeh_v2.pdf','PDF2-3,21-23; Thm1.2/3.16, Def3.18, actual Cor3.19','full relevant theorem proofs checked; actual p22 SD hypothesis differs from p3 summary'),
 ('Eisenbud-Sturmfels','primary_scope_family/tmp/eisenbud_sturmfels_published.pdf','PDF11-14; Thm2.1 and Cor2.2','algebraically closed statement handled by own arbitrary-K group-algebra proof'),
 ('Eisenbud-Van de Ven','primary_scope_family/tmp/eisenbud_van_de_ven_published.pdf','printed453 and463','classical quartic N=O(7)^2; explicit frame provides field-uniform proof'),
 ('Stacks reflexivity','geometry_family/tmp/primary_sources/stacks_reflexive.html','Tag0AVB','complete equivalence and proof inspected'),
 ('Stacks field change','geometry_family/tmp/primary_sources/stacks_field_cm.html','Tag045P','locally finite-type permits arbitrary field extension')]
loci=[{'source':name,'path':path,'sha256':sha(BASE/path),'locus':loc,'checked':finding} for name,path,loc,finding in locations]
crossref=read(BASE/'primary_scope_family/tmp/hassanzadeh_crossref.json')['message']
assert crossref['DOI']=='10.1112/jlms.70108'
assert crossref['volume']=='111' and crossref['issue']=='3' and crossref['article-number']=='e70108'
assert crossref['published-online']['date-parts']==[[2025,3,6]]

snap=read(BASE/'snapshot_manifest.json')
old=BASE/'source_snapshot/PARTIAL_RESULTS.md'
cur=BASE/'reviewed_candidate/PARTIAL_RESULTS.md'
delta=subprocess.run(['diff','-u',str(old),str(cur)],capture_output=True,text=True)
(HERE/'tmp/current_vs_original.diff').write_text(delta.stdout)
assert delta.returncode==1
changed=[name for name in sorted(p.name for p in (BASE/'source_snapshot').iterdir()) if (BASE/'reviewed_candidate'/name).read_bytes()!=(BASE/'source_snapshot'/name).read_bytes()]
assert changed==['PARTIAL_RESULTS.md','README.md','RESEARCH_LOG.md','SOURCES.md','status.json']
summary=read(BASE/'reviewed_candidate/review_summary.json')
assert summary['reviewed_sha256']==sha(old)
assert summary['review_sha256']==sha(BASE/'source_snapshot/REVIEW.md')==sha(BASE/'reviewed_candidate/REVIEW.md')
assert (BASE/'reviewed_candidate/turns.jsonl').read_bytes()==(BASE/'source_snapshot/turns.jsonl').read_bytes()

out={'checked_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'source_ledger_cache_matches':sources,
     'all_algebra_primary_receipt_pdf_and_text_hashes_match':True,'inspected_primary_loci':loci,
     'independent_metadata_recheck_urls':['https://arxiv.org/abs/1605.02755v3','https://arxiv.org/abs/1806.04405v2','https://arxiv.org/abs/2409.05705v2','https://ems.press/journals/owr/articles/824'],
     'versions_confirmed':{'MSS':'v3,2017-04-14','Boix-Eghbali':'v2,2021-06-12 corrected prior mistakes','Hassanzadeh':'v2,2025-02-12; manuscript2025-02-13','OWR':'report2005,publication2006-03-31'},
     'published_Hassanzadeh_metadata':{k:crossref[k] for k in ['DOI','volume','issue','article-number','published-online']},
     'published_Hassanzadeh_complete_text_checked':False,'publisher_access_limit':'prior independent PDF/XML routes403; fresh web DOI open returned internal error; no full version-of-record comparison claimed',
     'current_candidate_changed_from_original_files':changed,'historical_review_hash_and_original_review_summary_preserved':True,
     'historical_review_transferred_to_current_hash':False,'current_vs_original_diff_sha256':sha(HERE/'tmp/current_vs_original.diff'),
     'bounded_source_audit_only':True,'worldwide_openness_or_novelty_certified':False,
     'scope':'Source theorem-to-application audit, not a search for a new residual construction or exclusion'}
(HERE/'SOURCE_HISTORY_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'source_loci':len(loci),'ledger_sources_verified':len(sources),'candidate_changed_files':changed,'historical_review_transferred':False},indent=2))
