"""Assemble publication inventory, checks, and bounded native Sheets batches."""
import argparse, collections, csv, json, re
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--partial',action='store_true');args=parser.parse_args()
def read(path): return json.loads((HERE/path).read_text())
corpus=read('sources/corpus_records.json')
papers=[r for r in corpus['records'] if r['classification']=='paper']
reviews={};review_files={}
for filename in ['older_a.json','older_b.json','recent_a.json','recent_b.json','followons.json']:
    p=HERE/'reviews'/filename
    if not p.exists(): continue
    for a in json.loads(p.read_text()):
        rid=int(a['record_id'])
        if rid in reviews: raise ValueError(f'Duplicate review {rid}')
        reviews[rid]=a;review_files[rid]=filename
missing=sorted(set(r['id'] for r in papers)-set(reviews))
if missing and not args.partial: raise ValueError(f'Missing {len(missing)} assessments: {missing}')
allowed={'Strong submission candidate','Specialist submission candidate','Technical note or merge','Hold for dependency or proof review','Superseded edition','Withdrawn or invalid main claim'}
for rid,a in reviews.items():
    for key in ['impact','added_contribution']:
        if not isinstance(a[key],(int,float)) or not 0<=a[key]<=10: raise ValueError((rid,key,a[key]))
    if a['publication_recommendation'] not in allowed: raise ValueError((rid,a['publication_recommendation']))

headers=['Index','Paper title','Field','Conditional impact /10','Added contribution /10','Journal assessment','In plain English','Why this impact','Publication rationale / gap','What is surprising','Claim boundaries','DOI','Zenodo record','Publication date','Version','Edition / availability','Related editions','Authors','Review basis','Dependency / novelty limits','Next step','Manuscript files','Zenodo record ID','Scientific work group','Assessed on','Manuscript SHA-256']
rows=[];entries=[]
for r in papers:
    rid=r['id'];a=reviews.get(rid)
    if a is None: continue
    duplicate=rid==21699069
    superseded=not r['is_latest_paper_version']
    edition='Presentation copy of 21699161' if duplicate else ('Earlier edition; latest '+str(max(r['all_paper_version_ids'])) if superseded else 'Latest standalone Zenodo manuscript')
    recommendation='Superseded edition' if duplicate or superseded else a['publication_recommendation']
    related=[f'https://zenodo.org/records/{x}' for x in r['all_paper_version_ids'] if x!=rid]
    if rid in (21699069,21699161): related.append('https://zenodo.org/records/'+str(21699161 if rid==21699069 else 21699069))
    work='Z-'+r['concept_id'] if rid not in (21699069,21699161) else 'Bell-setting-minimum'
    dependency=a.get('dependencies') or a.get('exact_gap') or 'No fresh exhaustive novelty or dependency-proof audit performed.'
    rationale=a['impact_reason']+(' Added contribution: '+a['added_contribution_reason'] if a.get('added_contribution_reason') else '')
    row=[0,r['title'],a['field'],a['impact'],a['added_contribution'],recommendation,a['lay_summary'],rationale,a['publication_reason'],a['surprise_reason'],a['claim_boundary'],'https://doi.org/'+r['doi'],r['record_url'],r['publication_date'],r['version'] or 'Not supplied',edition,'; '.join(related),'; '.join(x['name'] for x in r['metadata']['creators']),a['review_basis'],dependency,a['next_step'],'; '.join(x['filename'] for x in r['sources']),rid,work,'2026-10-24','; '.join(x['filename']+': '+x['sha256'] for x in r['sources'])]
    rows.append(row);entries.append(dict(record_id=rid,work_group=work,edition=edition,recommendation=recommendation,record=r['record_url'],**{k:v for k,v in a.items() if k not in ['record_id']}))

# Supplemental author manuscripts are independently bound to archive members or
# canonical public repository files. Their distinct work groups are adjudicated.
supp=HERE/'sources/supplemental_candidates.json'
supp_missing=[]
if supp.exists():
    candidates=json.loads(supp.read_text())['candidates']
    mappings={x['candidate_id']:x for x in read('sources/work_group_adjudication.json')['mapping']}
    sr={}
    for name in ['archive_only_a.json','archive_only_root.json','archive_only_b.json','rejected_jc.json']:
        p=HERE/'reviews'/name
        if p.exists():
            for a in json.loads(p.read_text()):
                if a['candidate_id'] in sr:raise ValueError('Duplicate supplemental review')
                sr[a['candidate_id']]=a
    for c in candidates:
        key=c['candidate_id'];a=sr.get(key)
        if a is None:supp_missing.append(key);continue
        m=mappings[key]
        for score in ['impact','added_contribution']:
            if not isinstance(a[score],(int,float)) or not 0<=a[score]<=10:raise ValueError((key,score))
        if a['publication_recommendation'] not in allowed:raise ValueError((key,'recommendation'))
        matches=c.get('archive_matches',[])
        rec= max(matches,key=lambda x:x['deposit_id']) if matches else None
        refs='; '.join(str(x) for x in sorted({x['deposit_id'] for x in matches}))
        doi=('Shared archive reference only: https://doi.org/10.5281/zenodo.'+str(rec['deposit_id'])) if rec else ''
        url=rec['record_url'] if rec else c.get('public_pdf_url',c.get('public_repository_url',''))
        availability='Embedded in Zenodo archive; no paper-specific DOI' if rec else 'Public repository only; no Zenodo match'
        availability+='; '+m['relation'].replace('_',' ')
        canonical=m['canonical_entry_id']
        relation=m['reason']+' Canonical entry: '+str(canonical)
        if c.get('public_pdf_url'):relation+='; PDF: '+c['public_pdf_url']
        recommendation=a['publication_recommendation']
        if recommendation!='Withdrawn or invalid main claim' and (m['relation'] in ['precursor_incorporated_in_consolidated_paper','archival_precursor_incorporated_in_consolidation','narrower_archival_precursor'] or str(canonical)!=str(key)):
            recommendation='Superseded edition'
        work=m['work_group_id']
        # Existing-primary aliases use exactly the primary concept work ID.
        mt=re.fullmatch(r'(?:primary:|record:|zenodo:)?(\d+)',str(canonical))
        if not m['is_new_group_beyond_primary_corpus'] and mt:
            cr=next(x for x in papers if x['id']==int(mt[1]));work='Z-'+cr['concept_id']
        text=Path(c['text_path']).read_text()[:2500]
        months='January February March April May June July August September October November December'.split()
        date_match=re.search(r'\b(\d{1,2})\s+('+'|'.join(months)+r')\s+(2026)\b',text)
        date2=re.search(r'\b('+'|'.join(months)+r')\s+(\d{1,2}),?\s+(2026)\b',text)
        pubdate=(date_match.group(0) if date_match else date2.group(0) if date2 else '2026; see manuscript for edition date')
        version_match=re.search(r'(?i)\bversion\s+(\d+(?:\.\d+){0,3})',text)
        version=version_match.group(1) if version_match else 'Repository / archive edition'
        provenance='Local manuscript SHA-256 verified against public PDF' if c.get('public_payload_check') else 'Published ZIP member CRC32, exact size and extracted SHA-256 verified'
        provenance+='; entire large ZIP MD5 not recomputed' if rec and not rec.get('whole_archive_hash_verified') else ''
        reason=a['impact_reason']+(' Added contribution: '+a['added_contribution_reason'] if a.get('added_contribution_reason') else '')
        manuscript_locator=(rec['archive_filename']+' :: '+rec['member']) if rec else c.get('public_pdf_url',Path(c['local_pdf_path']).name)
        row=[0,c['title'],a['field'],a['impact'],a['added_contribution'],recommendation,a['lay_summary'],reason,a['publication_reason'],a['surprise_reason'],a['claim_boundary'],doi,url,pubdate,version,availability,relation,'Kriebel, Alec',a['review_basis']+' '+provenance,a.get('dependencies') or a['exact_gap'],a['next_step'],manuscript_locator,'Archive IDs: '+refs if refs else 'No Zenodo record',work,'2026-10-24',c['sha256']]
        rows.append(row);entries.append(dict(**a,work_group=work,edition=availability,recommendation=recommendation,provenance=provenance,source_url=url))
if supp_missing and not args.partial:raise ValueError(f'Missing supplemental assessments: {supp_missing}')

rows.sort(key=lambda r:(-r[3],-r[4],r[1].casefold(),str(r[22])))
for i,row in enumerate(rows,1):row[0]=i
assert all(len(r)==26 for r in rows)
work_count=len({r[23] for r in rows})
recommendations=collections.Counter(r[5] for r in rows)
summary={'status':'partial' if missing or supp_missing else 'complete_assessed_inventory','as_of':'2026-10-24','owned_account_records':len(corpus['records']),'primary_manuscript_records':len(papers),'primary_manuscripts_assessed':len(papers)-len(missing),'primary_pdfs':sum(len(r['sources']) for r in papers),'supplemental_manuscript_entries':len(rows)-(len(papers)-len(missing)),'inventory_rows':len(rows),'scientific_work_groups':work_count,'recommendation_counts':dict(recommendations),'missing_review_record_ids':missing,'missing_supplemental_assessments':supp_missing,'impact_definition':'Conditional importance assuming correctness and genuine novelty; neither correctness probability nor measured citations.','assessment_scope':'Manuscript triage; depth and limitations recorded per row. No complete new proof audit or exhaustive novelty search.'}
(HERE/'outputs/inventory.json').write_text(json.dumps({'summary':summary,'headers':headers,'rows':rows,'assessments':entries},ensure_ascii=False,indent=2)+'\n')
(HERE/'outputs/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
with (HERE/'outputs/inventory.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(headers);w.writerows(rows)
if missing or supp_missing:
    print(json.dumps(summary));raise SystemExit

grid=[['Complete paper inventory — Alec Kriebel']+['']*25,
      [f'{len(rows)} inventory rows | {work_count} scientific work groups | {len(papers)} standalone Zenodo manuscript records | reviewed 24 Oct 2026']+['']*25,
      ['Impact assumes correctness and genuine novelty. Added contribution credits prior inputs. Scores have about ±0.5–1 uncertainty.']+['']*25,
      ['Journal assessments are submission judgments, not acceptance or proof certificates. Review basis, exact limits, editions and source hashes appear in each row.']+['']*25,
      ['Most surprising: Free spanning-forest degree can decrease under squaring (7/10). Filter Journal assessment for submission priorities; withdrawn and superseded manuscripts remain explicit.']+['']*25,
      headers]+rows
sid=1052646184
def cell(v):
    return {'userEnteredValue':{'numberValue':v}} if isinstance(v,(int,float)) else {'userEnteredValue':{'stringValue':str(v)}}
for start in range(0,len(grid),20):
    sub=grid[start:start+20]
    payload={'requests':[{'updateCells':{'range':{'sheetId':sid,'startRowIndex':start,'endRowIndex':start+len(sub),'startColumnIndex':0,'endColumnIndex':26},'rows':[{'values':[cell(v) for v in row]} for row in sub],'fields':'userEnteredValue'}}]}
    (HERE/f'outputs/sheet_batch_{start//20:02d}.json').write_text(json.dumps(payload,ensure_ascii=False)+'\n')
height=len(grid)
fmt=[
 {'updateSheetProperties':{'properties':{'sheetId':sid,'gridProperties':{'frozenRowCount':6,'frozenColumnCount':0}},'fields':'gridProperties.frozenRowCount,gridProperties.frozenColumnCount'}},
 {'repeatCell':{'range':{'sheetId':sid,'startRowIndex':0,'endRowIndex':height,'startColumnIndex':0,'endColumnIndex':26},'cell':{'userEnteredFormat':{'wrapStrategy':'WRAP','verticalAlignment':'TOP','textFormat':{'fontFamily':'Arial','fontSize':10,'foregroundColor':{'red':0,'green':0,'blue':0}}}},'fields':'userEnteredFormat'}},
 {'mergeCells':{'range':{'sheetId':sid,'startRowIndex':0,'endRowIndex':1,'startColumnIndex':0,'endColumnIndex':6},'mergeType':'MERGE_ALL'}},
 *[{'mergeCells':{'range':{'sheetId':sid,'startRowIndex':i,'endRowIndex':i+1,'startColumnIndex':0,'endColumnIndex':6},'mergeType':'MERGE_ALL'}} for i in range(1,5)],
 {'repeatCell':{'range':{'sheetId':sid,'startRowIndex':0,'endRowIndex':1,'startColumnIndex':0,'endColumnIndex':6},'cell':{'userEnteredFormat':{'textFormat':{'bold':True,'fontSize':15}}},'fields':'userEnteredFormat.textFormat'}},
 {'repeatCell':{'range':{'sheetId':sid,'startRowIndex':5,'endRowIndex':6,'startColumnIndex':0,'endColumnIndex':26},'cell':{'userEnteredFormat':{'backgroundColor':{'red':0.9,'green':0.9,'blue':0.9},'textFormat':{'bold':True}}},'fields':'userEnteredFormat.backgroundColor,userEnteredFormat.textFormat'}},
 {'repeatCell':{'range':{'sheetId':sid,'startRowIndex':6,'endRowIndex':height,'startColumnIndex':3,'endColumnIndex':5},'cell':{'userEnteredFormat':{'numberFormat':{'type':'NUMBER','pattern':'0.0'},'horizontalAlignment':'CENTER'}},'fields':'userEnteredFormat.numberFormat,userEnteredFormat.horizontalAlignment'}},
 {'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'ROWS','startIndex':0,'endIndex':5},'properties':{'pixelSize':30},'fields':'pixelSize'}},
 {'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'ROWS','startIndex':5,'endIndex':6},'properties':{'pixelSize':60},'fields':'pixelSize'}},
 {'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'ROWS','startIndex':6,'endIndex':height},'properties':{'pixelSize':120},'fields':'pixelSize'}},
 {'setBasicFilter':{'filter':{'range':{'sheetId':sid,'startRowIndex':5,'endRowIndex':height,'startColumnIndex':0,'endColumnIndex':26}}}},
]
widths=[80,460,190,105,115,220,440,480,500,440,500,280,280,130,140,290,320,230,520,500,440,340,140,220,130,560]
fmt += [{'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'COLUMNS','startIndex':i,'endIndex':i+1},'properties':{'pixelSize':w},'fields':'pixelSize'}} for i,w in enumerate(widths)]
(HERE/'outputs/sheet_format.json').write_text(json.dumps({'requests':fmt})+'\n')
print(json.dumps(summary))
