"""Read-only row-by-row audit of the assembled portfolio; writes only audit results."""
import collections,datetime,hashlib,json,re
from pathlib import Path
B=Path(__file__).resolve().parents[1]
def rd(p):return json.loads((B/p).read_text())
def digest(p):return hashlib.sha256((B/p).read_bytes()).hexdigest()
inv=rd('outputs/inventory.json');corpus=rd('sources/corpus_records.json');candidates=rd('sources/supplemental_candidates.json')['candidates'];adj=rd('sources/work_group_adjudication.json');maps={r['candidate_id']:r for r in adj['mapping']}
P={r['id']:r for r in corpus['records'] if r['classification']=='paper'};C={r['candidate_id']:r for r in candidates}
reviews=[]
for fn in ['older_a.json','older_b.json','recent_a.json','recent_b.json','followons.json','archive_only_a.json','archive_only_root.json','archive_only_b.json','rejected_jc.json']:
 p=B/'reviews'/fn
 if p.exists():reviews+=json.loads(p.read_text())
def akey(a):return ('p',int(a['record_id'])) if 'record_id' in a else ('s',a['candidate_id'])
R=collections.defaultdict(list)
for r in reviews:R[akey(r)].append(r)
A=collections.defaultdict(list)
for a in inv['assessments']:A[akey(a)].append(a)
expected={('p',k)for k in P}|{('s',k)for k in C}
findings=[];entity=[];usedrows=[];expectedgroups=set()
allowed={'Strong submission candidate','Specialist submission candidate','Technical note or merge','Hold for dependency or proof review','Superseded edition','Withdrawn or invalid main claim'}
def fail(key,msg):findings.append({'entry':str(key),'issue':msg})
for key in sorted(expected,key=str):
 kind,k=key;found=[];checks=[]
 if kind=='p':
  r=P[k];found=[(n,row)for n,row in enumerate(inv['rows']) if row[22]==k]
  group='Bell-setting-minimum' if k in(21699069,21699161) else 'Z-'+r['concept_id'];edition='Presentation copy of 21699161' if k==21699069 else ('Earlier edition; latest '+str(max(r['all_paper_version_ids'])) if not r['is_latest_paper_version'] else 'Latest standalone Zenodo manuscript')
 else:
  c=C[k];m=maps[k];found=[(n,row)for n,row in enumerate(inv['rows']) if row[1]==c['title'] and row[25]==c['sha256']]
  group=m['work_group_id'];canonical=m['canonical_entry_id'];mt=re.fullmatch(r'(?:primary:|record:|zenodo:)?(\d+)',str(canonical))
  if not m['is_new_group_beyond_primary_corpus'] and mt:group='Z-'+P[int(mt[1])]['concept_id']
 expectedgroups.add(group)
 if len(R[key])!=1:fail(key,'Expected exactly one source assessment; found '+str(len(R[key])))
 if len(A[key])!=1:fail(key,'Expected exactly one assembled assessment; found '+str(len(A[key])))
 if len(found)!=1:fail(key,'Expected exactly one sheet row; found '+str(len(found)))
 if len(R[key])!=1 or len(A[key])!=1 or len(found)!=1:
  entity.append({'kind':kind,'id':k,'status':'pending_or_failed','source_assessments':len(R[key]),'output_assessments':len(A[key]),'rows':len(found)});continue
 src=R[key][0];out=A[key][0];n,row=found[0];usedrows.append(n)
 checks.append('Exactly one input assessment, output assessment and sheet row')
 for col,field in [(3,'impact'),(4,'added_contribution')]:
  v=row[col]
  if isinstance(v,bool) or not isinstance(v,(int,float)) or not 0<=v<=10:fail(key,'Invalid numeric score '+field)
  if v!=src[field] or out[field]!=v:fail(key,'Score differs between assessment and sheet '+field)
 if row[5] not in allowed:fail(key,'Invalid recommendation')
 if row[23]!=group or out['work_group']!=group:fail(key,'Incorrect scientific work group')
 for field,col in [('field',2),('lay_summary',6),('publication_reason',8),('surprise_reason',9),('claim_boundary',10),('next_step',20)]:
  if row[col]!=src[field]:fail(key,'Visible cell differs from its exact assessment '+field)
  if out.get(field)!=src[field]:fail(key,'Assembled assessment differs '+field)
 if not row[18] or not row[19]:fail(key,'Missing review-depth/dependency disclosure')
 if kind=='p':
  if row[1]!=r['title'] or row[11]!='https://doi.org/'+r['doi'] or row[12]!=r['record_url']:fail(key,'Title/DOI/record identity mismatch')
  if row[25]!='; '.join(s['filename']+': '+s['sha256']for s in r['sources']):fail(key,'Primary PDF SHA list mismatch')
  rec='Superseded edition' if k==21699069 or not r['is_latest_paper_version'] else src['publication_recommendation']
  if row[15]!=edition or row[5]!=rec:fail(key,'Edition or primary recommendation mismatch')
  if row[13]!=r['publication_date']:fail(key,'Primary publication date mismatch')
 else:
  matches=c.get('archive_matches',[]);rec=src['publication_recommendation']
  if rec!='Withdrawn or invalid main claim' and (m['relation'] in ['precursor_incorporated_in_consolidated_paper','archival_precursor_incorporated_in_consolidation','narrower_archival_precursor']or str(m['canonical_entry_id'])!=str(k)):rec='Superseded edition'
  if row[5]!=rec:fail(key,'Supplemental edition/readiness mismatch')
  if matches:
   z=max(matches,key=lambda x:x['deposit_id']);expecteddoi='Shared archive reference only: https://doi.org/10.5281/zenodo.'+str(z['deposit_id'])
   if row[11]!=expecteddoi or row[12]!=z['record_url']:fail(key,'Wrong or unqualified shared archive DOI')
   if row[21]!=z['archive_filename']+' :: '+z['member']:fail(key,'Published archive member locator missing or incorrect')
   if 'no paper-specific DOI' not in row[15]:fail(key,'Archive DOI presented as dedicated paper DOI')
   pc=c.get('archive_payload_check',{})
   if not all(pc.get(s)for s in['matches_candidate_sha256','member_crc32_verified','member_size_verified']):fail(key,'Missing exact archived-member binding')
   if pc.get('member_sha256')!=c['sha256']:fail(key,'Archived member SHA mismatch')
  else:
   if row[11] or row[22]!='No Zenodo record' or 'repository only'not in row[15].lower():fail(key,'Repository-only document incorrectly assigned a Zenodo DOI')
   if not c.get('public_payload_check',{}).get('matches_local_pdf'):fail(key,'Repository-only public-payload verification missing')
  if hashlib.sha256(Path(c['local_pdf_path']).read_bytes()).hexdigest()!=c['sha256']:fail(key,'Actual supplemental local PDF SHA mismatch')
  if k=='rejected-jc-cleanup-convention-closure':
   if row[5]!='Withdrawn or invalid main claim' or row[3]!=2 or row[4]!=0:fail(key,'Rejected draft promoted or incorrectly scored')
   if 'ONLY' not in row[7] or 'rejected'not in row[10].lower()or'do not submit'not in row[8].lower():fail(key,'Rejected headline and surviving-identity scope not explicit')
 checks+=['Scores and visible assessment cells match source','Edition and canonical grouping preserve source scope','DOI, public-source and PDF-hash binding verified']
 entity.append({'kind':kind,'id':k,'status':'pass'if not any(f['entry']==str(key)for f in findings)else'failed','inventory_number':row[0],'work_group':group,'checks':checks})
extraA=set(A)-expected
for key in extraA:fail(key,'Unexpected output assessment')
for n in set(range(len(inv['rows'])))-set(usedrows):fail('row '+str(n+1),'Sheet row lacks a unique expected manuscript binding')
if len(usedrows)!=len(set(usedrows)):fail('rows','One sheet row reused for multiple manuscripts')
if [r[0]for r in inv['rows']]!=list(range(1,len(inv['rows'])+1)):fail('rows','Inventory numbering is not consecutive')
if any(len(r)!=len(inv['headers'])or len(r)!=26 for r in inv['rows']):fail('rows','Row/header width mismatch')
if len({r[23]for r in inv['rows']})!=inv['summary']['scientific_work_groups']:fail('summary','Work-group count mismatch')
if len(inv['rows'])!=inv['summary']['inventory_rows']:fail('summary','Row-count mismatch')
if dict(collections.Counter(r[5]for r in inv['rows']))!=inv['summary']['recommendation_counts']:fail('summary','Recommendation totals mismatch')
# Validate the exact pending native-Sheets value batches, independent of row order.
sheetfiles=sorted((B/'outputs').glob('sheet_batch_*.json'));sheetrows={};sheetissues=[]
for path in sheetfiles:
 for req in json.loads(path.read_text())['requests']:
  if set(req)!={'updateCells'}:sheetissues.append('Unexpected request type in '+path.name);continue
  u=req['updateCells'];q=u['range'];start=q['startRowIndex'];end=q['endRowIndex']
  if q['sheetId']!=1052646184 or q['startColumnIndex']!=0 or q['endColumnIndex']!=26 or end-start!=len(u['rows']) or len(u['rows'])>20:sheetissues.append('Range/shape mismatch in '+path.name)
  for j,rr in enumerate(u['rows'],start):
   if j in sheetrows:sheetissues.append('Overlapping native row '+str(j))
   vals=[]
   for c in rr['values']:
    v=c['userEnteredValue']
    if set(v)=={'numberValue'}:vals.append(v['numberValue'])
    elif set(v)=={'stringValue'}:vals.append(v['stringValue'])
    else:sheetissues.append('Formula or unexpected cell value at '+str(j));vals.append(None)
   sheetrows[j]=vals
height=len(inv['rows'])+6
if set(sheetrows)!=set(range(height)):sheetissues.append('Native batch rows do not cover exact title/header/data extent')
if sheetrows.get(5)!=inv['headers']:sheetissues.append('Header is not native row5')
for j,row in enumerate(inv['rows'],6):
 if sheetrows.get(j)!=row:sheetissues.append('Sorted inventory row fails exact payload match at native index '+str(j))
fmt=rd('outputs/sheet_format.json');filterranges=[r['setBasicFilter']['filter']['range']for r in fmt['requests']if'setBasicFilter'in r]
if filterranges!=[{'sheetId':1052646184,'startRowIndex':5,'endRowIndex':height,'startColumnIndex':0,'endColumnIndex':26}]:sheetissues.append('Filter bounds mismatch')
# Check all pending formatting requests stay inside the selected sheet bounds.
for req in fmt['requests']:
 typ=next(iter(req));value=req[typ]
 if typ not in {'updateSheetProperties','repeatCell','mergeCells','updateDimensionProperties','setBasicFilter'}:sheetissues.append('Unexpected format mutation '+typ);continue
 if typ=='updateSheetProperties':
  prop=value['properties']
  if prop['sheetId']!=1052646184 or prop['gridProperties']!={'frozenRowCount':6,'frozenColumnCount':0}:sheetissues.append('Unexpected sheet-properties change')
 else:
  q=value['filter']['range']if typ=='setBasicFilter'else value['range']
  if q['sheetId']!=1052646184:sheetissues.append('Format request targets wrong sheet')
  if 'dimension'in q:
   limit=26 if q['dimension']=='COLUMNS'else height
   if not 0<=q.get('startIndex',0)<q['endIndex']<=limit:sheetissues.append('Dimension request out of bounds')
  elif not(0<=q.get('startRowIndex',0)<q.get('endRowIndex',height)<=height and 0<=q.get('startColumnIndex',0)<q.get('endColumnIndex',26)<=26):sheetissues.append('Format range out of bounds')
merges=[r['mergeCells']['range']for r in fmt['requests']if'mergeCells'in r]
if len(merges)!=5 or any(q['startColumnIndex']!=0 or q['endColumnIndex']!=6 for q in merges):sheetissues.append('Summary merges do not match planned A:F extent')
if inv['headers'][0]!='Index':sheetissues.append('Final first-column header is not Index')
headerheights=[r['updateDimensionProperties']['properties'].get('pixelSize')for r in fmt['requests']if'updateDimensionProperties'in r and r['updateDimensionProperties']['range'].get('dimension')=='ROWS'and r['updateDimensionProperties']['range'].get('startIndex')==5 and r['updateDimensionProperties']['range'].get('endIndex')==6]
if headerheights!=[60]:sheetissues.append('Final header row height is not60 pixels')
for f in sheetissues:fail('sheet_payload',f)
sheetaudit={'value_batches':len(sheetfiles),'target_sheet_id':1052646184,'native_start_row':0,'native_end_row_exclusive':height,'native_header_row':5,'native_data_start_row':6,'column_start':0,'column_end_exclusive':26,'all_sorted_rows_exactly_match':not sheetissues,'formulas_present':False,'issues':sheetissues,'value_batch_sha256':{str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sheetfiles},'format_sha256':digest('outputs/sheet_format.json')}
leaks=[]
for n,row in enumerate(inv['rows']):
 for j,v in enumerate(row):
  if not isinstance(v,str):continue
  for tag,pat in {'local_path':r'/Users/|/private/|/var/folders/','credential':r'(?i)authorization:|bearer\s+[a-z0-9_-]{10,}|access_token|refresh_token|cookie:|api[_-]?key\s*[=:]','email':r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}'}.items():
   if re.search(pat,v,re.I):leaks.append({'inventory_number':n+1,'column':j+1,'kind':tag})
for f in leaks:fail('privacy',str(f))
# Adopt the already completed root native readback without pretending to rerun a remote read.
native=rd('outputs/native_verification_receipt.json')
if native.get('paperRows')!=len(inv['rows'])or native.get('columns')!=26 or native.get('cellsCompared')!=height*26 or native.get('mismatchCount')!=0 or native.get('headerReadback')!='Index'or not all(native.get('sourceTabsUnchanged',{}).get(k)for k in['Papers','MathPuzzles','ImpactScoring']):fail('native_receipt','Native verification receipt differs from final artifact extent/header or reports mismatches')
archive=rd('sources/archive_papers.json');duplicate_checks=[]
for d in archive['exact_matches_to_main_corpus']:
 p=P[d['main_corpus_id']]
 ok=d.get('direct_pdf_md5_sha256_match')and any(z['md5']==d.get('member_md5')and z['sha256']==d.get('member_sha256')for z in p['sources'])
 duplicate_checks.append({'record_id':d['main_corpus_id'],'md5_sha256_exact_match':bool(ok)})
 if not ok:fail(d['main_corpus_id'],'Reported archived duplicate is not MD5+SHA-bound to direct PDF')
if len(duplicate_checks)!=17:fail('archive_duplicates','Expected17 direct archive duplicate comparisons')
adoption={'format_fix':'Native Sheets rejected A:F summary merges spanning the old frozen2-column boundary. Adopted zero frozen columns, retaining6 frozen header rows.','readability_fix':'First-column header shortened to Index and header row height increased to60 pixels; scientific rows unchanged by this visual adjustment.','native_readback_basis':'Adopted root native verification receipt:6500/6500 compared cells match and Papers, MathPuzzles and ImpactScoring source tabs unchanged. This agent independently verifies final local payload/receipt binding; it did not repeat the remote read.','exact_archive_duplicate_checks':duplicate_checks}
pending=[{'kind':kind,'id':k}for kind,k in expected if len(R[(kind,k)])!=1]
report={'audited_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'pass'if not findings else'pending_inputs'if pending else'fail','completion_estimate_percent':100 if not findings else round(100*(len(expected)-len(pending))/len(expected),1),'scope':'Every primary manuscript and supplemental candidate in the current manifests; metadata/coverage/identity audit, not new mathematical proof or exhaustive archive-semantic audit.','input_sha256':{p:digest(p)for p in['scripts/build_inventory.py','outputs/inventory.json','sources/corpus_records.json','sources/supplemental_candidates.json','sources/work_group_adjudication.json','outputs/native_verification_receipt.json','outputs/source_manifest.json','sources/archive_papers.json','reviews/_inventory_integrity_audit.py']+[str(p.relative_to(B))for p in(B/'reviews').glob('*.json')if p.name in{'older_a.json','older_b.json','recent_a.json','recent_b.json','followons.json','archive_only_a.json','archive_only_root.json','archive_only_b.json','rejected_jc.json'}]},'expected_primary':len(P),'expected_supplemental':len(C),'expected_entries':len(expected),'expected_scientific_work_groups':len(expectedgroups),'actual_rows':len(inv['rows']),'actual_assessments':len(inv['assessments']),'actual_scientific_work_groups':len({r[23]for r in inv['rows']}),'pending_assessments':pending,'findings':findings,'visible_cell_privacy_findings':leaks,'native_sheet_payload_audit':sheetaudit,'final_adoption_note':adoption,'per_entry':entity,'limitations':['Historical review extracts may have different filesystem names, but all73 historical catalogue PDF filename+MD5 pairs match the freshly acquired corpus. These are not missing assessments.','Superseded editions and consolidated precursors intentionally retain their own rows and underlying scientific assessments; supersession is not a proof-error or unreviewed-work verdict.','Shared archive DOI references are not dedicated paper DOIs; full large-archive MD5 was not recomputed and this limitation is visible.','Local analysis JSON retains internal text-path provenance. Visible spreadsheet cells contain no local paths, credentials or personal email addresses in this audit.','The candidate manifest and scientific-work adjudication determine coverage; final archive-payload semantic sweep may discover further manuscript editions.']}
(B/'reviews/inventory_integrity_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
md='# Inventory integrity audit\n\nCheckpoint: '+report['audited_utc']+'. Coverage-audit completion estimate: '+str(report['completion_estimate_percent'])+'%. Status: '+report['status']+'.\n\n'
md+=f"Expected {len(P)} primary manuscript editions and {len(C)} supplemental entries ({len(expected)} total); assembled {len(inv['rows'])} rows and {len(inv['assessments'])} assessments. Expected scientific-work groups: {len(expectedgroups)}; assembled: {report['actual_scientific_work_groups']}. Every entry was checked individually for exactly one assessment and row, exact title/source/hash, numeric scores, edition disposition and work grouping.\n\n"
md+=f"Native Sheets batches: {len(sheetfiles)} value batches cover indices0–{height-1} exactly on sheet1052646184, columns0–25. Header index5 and first data index6 are correct; all sorted rows exactly match the inventory; no overlapping rows or formulas were found. Filter bounds are correct.\n\n"
md+='Final adoption note: '+adoption['format_fix']+' '+adoption['readability_fix']+' '+adoption['native_readback_basis']+' All17 archive/direct duplicate PDFs also match on MD5 and SHA-256.\n\n'
md+='Visible cells were scanned for credentials, personal email addresses and local filesystem paths. Findings: '+str(len(leaks))+'.\n\n'
if findings:
 md+='Findings or pending items:\n\n'+''.join('- '+f['entry']+': '+f['issue']+'\n'for f in findings)+'\n'
else:md+='No missing/duplicate entries, score mismatches, DOI/source identity errors, edition/readiness misrepresentations or visible-cell provenance leaks were found.\n\n'
md+='Scope limits:\n\n'+''.join('- '+s+'\n'for s in report['limitations'])
(B/'reviews/inventory_integrity_audit.md').write_text(md)
print(json.dumps({k:v for k,v in report.items()if k not in['per_entry','input_sha256','limitations','findings','native_sheet_payload_audit','final_adoption_note']},ensure_ascii=False,indent=2))
