#!/usr/bin/env python3
"""Verify this private audit and live read-only PR/source/ledger state. Never writes providers or files."""
import datetime
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
BOOK = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
SHEET = 1254632077

def need(test, reason):
    if not test:
        raise RuntimeError(reason)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def run(args):
    p = subprocess.run(args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
    need(p.returncode == 0, 'Read-only command failed: '+repr(args[:3])+': '+p.stderr.decode(errors='replace')[:1000])
    return p.stdout

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Independent scholarly verification/1.0'})
    with urllib.request.urlopen(req, timeout=45) as r:
        need(r.status == 200, 'Unexpected source HTTP status')
        return r.url, r.read()

manifest = json.loads((ROOT/'MANIFEST.json').read_text())
expected = {x['path'] for x in manifest['members']}
actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p != ROOT/'MANIFEST.json'}
need(actual == expected, 'Manifest closure changed: '+repr(sorted(actual ^ expected)))
for pin in manifest['members']:
    raw = (ROOT/pin['path']).read_bytes()
    need(len(raw)==pin['bytes'] and digest(raw)==pin['sha256'], 'Bad member: '+pin['path'])
b = json.loads((ROOT/'PR_BINDINGS.json').read_text())
pr = json.loads(run(['gh','api','repos/AlecKriebel/Math/pulls/1207']))
need(pr['head']['sha']==b['head'], 'PR head changed')
need(digest(pr['body'].encode())==b['body_sha256'], 'PR body changed')
need(pr['state']==b['state'] and pr['draft']==b['draft'] and pr['merged']==b['merged'], 'PR workflow status changed; reconcile before action')
files = json.loads(run(['gh','api','repos/AlecKriebel/Math/pulls/1207/files?per_page=100']))
need(len(files)==8, 'Complete file set changed')
need({(x['filename'],x['sha']) for x in files}=={(x['path'],x['git_blob']) for x in b['complete_files']}, 'Changed-file blob set changed')
need(not any(x['filename'].endswith('QUEUE.md') for x in files), 'Unexpected QUEUE change')
for pin in b['complete_files']:
    raw = run(['git','show',b['head']+':'+pin['path']])
    git_blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    need(git_blob==pin['git_blob'] and len(raw)==pin['bytes'] and digest(raw)==pin['sha256'], 'PR source changed: '+pin['path'])
    need(raw==(ROOT/'private_sources'/Path(pin['path']).name).read_bytes(), 'Captured source mismatch')
math = run([sys.executable,'-B',str(ROOT/'verify_math_bridges.py')])
need(math==(ROOT/'MATH_CHECK.stdout.json').read_bytes(), 'Independent mathematical check output changed')
source_results=[]
for name,url in [('pm2026','https://ems.press/content/serial-article-files/52275'),('arxiv_latest','https://arxiv.org/pdf/2310.17794')]:
    final,raw=get(url)
    need(raw==(ROOT/'private_sources'/f'{name}.pdf').read_bytes(), 'Primary PDF changed; re-review '+name)
    source_results.append({'name':name,'final_url':final,'bytes':len(raw),'sha256':digest(raw)})
final,absraw=get('https://arxiv.org/abs/2310.17794')
versions=re.findall(rb'<strong>\[v(\d+)\]</strong>',absraw)
need(versions==[b'1'],'arXiv history updated; inspect before action')
final,doi=get('https://doi.org/10.4171/PM/2155')
need(final=='https://ems.press/journals/pm/articles/14299324', 'DOI landing changed')
for token in [b'10.4171/pm/2155',b'Simone Marchesi',b'Elisa Palezzato',b'Michele Torielli',b'citation_firstpage',b'citation_lastpage']:
    need(token in doi, 'DOI identity token absent')
raw=run(['gws','sheets','spreadsheets','values','batchGetByDataFilter','--params',json.dumps({'spreadsheetId':BOOK}),'--json',json.dumps({'dataFilters':[{'gridRange':{'sheetId':SHEET}}],'majorDimension':'ROWS','valueRenderOption':'UNFORMATTED_VALUE'})])
ledger=json.loads(raw)
need(ledger['spreadsheetId']==BOOK and len(ledger['valueRanges'])==1,'Wrong workbook/selection')
vr=ledger['valueRanges'][0]
need(vr['dataFilters']==[{'gridRange':{'sheetId':SHEET}}],'Wrong numeric-sheet data filter')
rows=vr['valueRange']['values']
need(rows[0][:4]==['Original Problem','Solution Chat URL','DOI','Notes'],'Sheet schema changed')
exact=['30004602','owr-4990374-005','pm/2155','2310.17794','jacobian algebra of 3-dimensional hyperplane arrangements']
semantic=['marchesi','palezzato','torielli','jacobian','lefschetz']
exact_leads=[];semantic_leads=[]
for number,row in enumerate(rows,1):
    joined=' '.join(str(x) for x in row).lower()
    hit={'row':number,'doi':row[2] if len(row)>2 else '', 'matched_terms':[x for x in semantic if x in joined]}
    if any(x in joined for x in exact):
        exact_leads.append(number)
    if hit['matched_terms']:
        semantic_leads.append(hit)
print(json.dumps({'status':'PASS' if not exact_leads else 'RECONCILE_EXISTING_ROW_BEFORE_ACTION','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_members':len(expected),'fresh_pr':{'number':1207,'head':pr['head']['sha'],'base_now':pr['base']['sha'],'state':pr['state'],'draft':pr['draft'],'merged':pr['merged'],'file_count':len(files)},'fresh_primary_pdf_pins':source_results,'arxiv_latest_version':1,'exact_math_output_match':True,'fresh_ledger':{'numeric_sheet_id':SHEET,'populated_rows':len(rows),'response_bytes':len(raw),'response_sha256':digest(raw),'exact_target_publication_lead_rows':exact_leads,'semantic_leads':semantic_leads},'provider_mutations':False,'git_mutations':False,'source_author_code_executed':False},indent=2))
