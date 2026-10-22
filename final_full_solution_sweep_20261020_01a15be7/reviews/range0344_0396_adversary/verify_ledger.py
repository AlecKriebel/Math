from pathlib import Path
import re,json,hashlib,datetime
E=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');O=E/'reviews/range0344_0396_adversary';P=E/'private/pr0344_0396_review'
f=P/'ledger_full_fresh.json';ledger=json.loads(f.read_text());values=ledger['values']
T={344:('30005649','OWR14297740021','23133607',20,'A counterexample to Takao'),356:('30001552','OWR4425007','23130727',17,'alternating antimorphic Fine'),359:('30001370','OWR4132003','23129302',15,'Common L1 basin boundaries'),364:('30004048','OWR16763022','23127646',16,'Non symmetry of biconstrained'),367:('11000151','AMR1090151','23124601',13,'Fixed generator positive factorizations')}
def norm(s):return re.sub('[^a-z0-9]','',s.lower())
checks=[];faults=[]
for pr,(pid,alias,record,row,title) in T.items():
 hits=[]
 for i,vals in enumerate(values,1):
  s=' '.join(vals);ns=norm(s);criteria=[]
  if re.search(r'(?<!\d)'+pid+r'(?!\d)',s):criteria.append('problem_id')
  if norm(alias) in ns:criteria.append('source_alias')
  if f'10.5281/zenodo.{record}' in s:criteria.append('exact_doi')
  if re.search(r'https://github\.com/AlecKriebel/Math/pull/'+str(pr)+r'(?!\d)',s):criteria.append('exact_pr')
  if norm(title) in ns:criteria.append('distinctive_paper_title')
  if criteria:hits.append({'row':i,'criteria':criteria,'row_sha256':hashlib.sha256(json.dumps(vals,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()})
 expected=values[row-1];meta=json.loads((P/f'pr{pr:04d}_public/record.json').read_text())['metadata']
 ok=len(hits)==1 and hits[0]['row']==row and set(hits[0]['criteria'])=={'problem_id','source_alias','exact_doi','exact_pr','distinctive_paper_title'} and norm(meta['title']) in norm(' '.join(expected))
 checks.append({'pr':pr,'problem_id':pid,'expected_row':row,'hits':hits,'unique_correct_row':ok,'doi_cell_exact':expected[2]==f'https://doi.org/10.5281/zenodo.{record}','record_title_in_row':norm(meta['title']) in norm(' '.join(expected))})
 if not ok:faults.append({'pr':pr,'ledger_identity_or_duplicate':hits})
missing=[]
for i,vals in enumerate(values,1):
 s=' '.join(vals)
 if re.search(r'(?<!\d)11000228(?!\d)',s) or 'amr1090228' in norm(s) or 'exceptionalstrata' in norm(s) or re.search(r'github\.com/AlecKriebel/Math/pull/363(?!\d)',s):missing.append(i)
result={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'requested_range':"'Math Puzzles'!A:AQ",'returned_range':ledger['range'],'complete_returned_row_count':len(values),'response_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'targets':checks,'pr363_lead_rows':missing,'faults':faults}
(O/'ledger_identity_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
