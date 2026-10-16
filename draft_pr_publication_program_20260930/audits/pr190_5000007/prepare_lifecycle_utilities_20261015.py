"""Prepare authorized lifecycle utilities without making external writes."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys,urllib.request
A=Path(__file__).resolve().parent;P=A.parent.parent;old=P/'audits/pr184_10300044'
if any((A/n).exists() for n in ['record_tracker.py']):raise RuntimeError('Historical generator retired: canonical outputs already exist; preserve independently repaired current scripts.')
s=(old/'record_tracker.py').read_text()
line=next(x for x in s.splitlines() if x.startswith(' row=['))
replacement=" row=[\"Fuchs Conjecture3.2 /5000007: bare-angle exclusion and parity-selected dodecahedral endpoint theorem\",'',z['doi_url'],\"A parity-selected endpoint theorem for the regular dodecahedron (PR190). Imported bare-angle exclusion is false by exactly two proper face diagonals per initial face/vertex; explicitly adopted parity-selected endpoint theorem proved. Classical AAH/Troubetzkoy symmetry and Ferudun current contemporaneous exact overlap credited. Original GitHub PR creation01Oct2026 and related DataCite DOIregistration09Oct documented with exact visibility/version/awareness limits; nofirstness, guaranteednovelty, current openness, authenticated author erratum or independence certification. Exact optimization-safe reproduction and pinned-coordinate norm inconsistency. Extensive AI; unrefereed; no conventional human peer review.\"]"
s=s.replace(line,replacement,1)
(A/'record_tracker.py').write_text(s)
D=A/'lifecycle_preflight_20261015';D.mkdir(exist_ok=False);rows=[]
calls=[
 ('append_schema',['/Users/alec/.nvm/versions/node/v22.16.0/bin/gws','schema','sheets.spreadsheets.values.append']),
 ('get_schema',['/Users/alec/.nvm/versions/node/v22.16.0/bin/gws','schema','sheets.spreadsheets.values.get']),
 ('sheet_tabs',['/Users/alec/.nvm/versions/node/v22.16.0/bin/gws','sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','fields':'spreadsheetId,sheets(properties(sheetId,title))'})]),
 ('sheet_header',['/Users/alec/.nvm/versions/node/v22.16.0/bin/gws','sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','range':"'Math Puzzles'!A1:D1",'valueRenderOption':'UNFORMATTED_VALUE'})])]
for label,argv in calls:
 start=datetime.datetime.now(datetime.UTC).isoformat();r=subprocess.run(argv,capture_output=True,timeout=90);end=datetime.datetime.now(datetime.UTC).isoformat();(D/(label+'.json')).write_bytes(r.stdout);(D/(label+'.stderr')).write_bytes(r.stderr)
 rec={'label':label,'start_UTC':start,'end_UTC':end,'argv':argv,'exit_code':r.returncode,'stdout_SHA256':hashlib.sha256(r.stdout).hexdigest(),'stderr_SHA256':hashlib.sha256(r.stderr).hexdigest(),'remote_mutations':0};rows.append(rec)
 if r.returncode:raise RuntimeError('Read-only preflight failed '+label+': '+r.stderr.decode(errors='replace')[:400])
tabs=json.loads((D/'sheet_tabs.json').read_bytes());matches=[x['properties'] for x in tabs['sheets'] if x['properties']['sheetId']==1254632077]
if len(matches)!=1 or matches[0]['title']!='Math Puzzles':raise RuntimeError('Intended tracker tab identity drift')
header=json.loads((D/'sheet_header.json').read_bytes())
(D/'ACTUAL_READONLY_RECEIPTS.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'read_only_calls':len(rows),'target_tab':matches[0],'header':header.get('values'),'remote_mutations':0,'lifecycle_utilities_prepared':['run_zenodo_step.py','record_tracker.py']}))

