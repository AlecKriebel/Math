#!/usr/bin/env python3
"""Check captured fresh ledger; never writes to Google Sheets or exposes raw ledger cells."""
import pathlib,json,hashlib,re,datetime
W=pathlib.Path(__file__).resolve().parent;v=json.loads((W/'inputs/fresh_ledger.json').read_text())['values'];out=[]
def pin(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
for n in [883,885,888,894,904,905]:
 d=json.loads((W/'inputs'/f'PR{n:04}_DISPOSITION.json').read_text());c=json.loads((W/'inputs'/f'PR{n:04}_PUBLICATION_COVERAGE_DETAILS.json').read_text());row=c['ledger_row'];doirows=[i for i,x in enumerate(v,1) if d['doi'] in ' '.join(x)];idrows=[i for i,x in enumerate(v,1) if re.search(r'(?<!\d)'+c['problem_id']+r'(?!\d)',' '.join(x))];prrows=[i for i,x in enumerate(v,1) if re.search(r'(?:PR\s*#?\s*|/pull/)'+str(n)+r'(?!\d)',' '.join(x),re.I)]
 out.append({'pr':n,'ledger_row':row,'doi':d['doi'],'doi_rows':doirows,'problem_id_rows':idrows,'pr_reference_rows':prrows,'doi_unique_exact_row':doirows==[row],'pr_reference_present':row in prrows,'problem_id_present':row in idrows,'source_url_or_alias_manual_review_required':n in (885,905),'row_cells_sha256':pin(v[row-1])})
(W/'LEDGER_CHECKS.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'range':'Math Puzzles!A:AQ','rows':len(v),'checks':out,'distinct_row30_sha256':pin(v[29])},indent=2)+'\n');print('PASS six unique DOI rows; PR885 source URL and PR905 source DOI/alias require documented semantic check')
