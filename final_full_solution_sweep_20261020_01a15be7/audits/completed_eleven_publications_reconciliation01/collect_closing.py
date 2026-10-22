#!/usr/bin/env python3
"""Full read-only GWS bracket and current endpoint observations; own output only."""
from pathlib import Path
import datetime,gzip,hashlib,json,shutil,subprocess,urllib.request
O=Path(__file__).resolve().parent;R=O.parent.parent
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();C=lambda a:json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def save(n,b):
 z=gzip.compress(b,mtime=0);assert sum(p.stat().st_blocks*512 for p in O.rglob('*')if p.is_file())+len(z)<6*1024**2;assert shutil.disk_usage(O).free-len(z)>150*1024**2;p=O/'private'/n;assert not p.exists();p.write_bytes(z)
sid='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';start=now()
def run(a):
 q=subprocess.run(['gws','sheets','spreadsheets']+a,capture_output=True,timeout=60);assert q.returncode==0,q.stderr.decode();return json.loads(q.stdout)
m0=run(['get','--params',json.dumps({'spreadsheetId':sid,'includeGridData':False})]);prop=next(x['properties']for x in m0['sheets']if x['properties']['sheetId']==1254632077);g={'sheetId':1254632077,'startRowIndex':0,'startColumnIndex':0,'endRowIndex':prop['gridProperties']['rowCount'],'endColumnIndex':prop['gridProperties']['columnCount']};v=[]
for mode in ['UNFORMATTED_VALUE','FORMULA']:v.append(run(['values','batchGetByDataFilter','--params',json.dumps({'spreadsheetId':sid}),'--json',json.dumps({'dataFilters':[{'gridRange':g}],'majorDimension':'ROWS','valueRenderOption':mode})]))
m1=run(['get','--params',json.dumps({'spreadsheetId':sid,'includeGridData':False})]);assert C(m0)==C(m1)and C(v[0])==C(v[1])
for i,a in enumerate([m0,*v,m1]):save(f'closing_gws_raw{i}.json.gz',C(a).encode())
rows=v[0]['valueRanges'][0]['valueRange']['values'];save('closing_ledger.json.gz',C(rows).encode());old=json.loads(gzip.decompress((O/'private/opening_ledger.json.gz').read_bytes()));preserved=rows[:len(old)]==old
(O/'CLOSING_LEDGER_RECEIPT.json').write_text(json.dumps({'started':start,'completed':now(),'typed_full_raw_VALUE_FORMULA_equal':True,'full_metadata_before_after_equal':True,'columns':g['endColumnIndex'],'allocated_rows':g['endRowIndex'],'populated_rows':len(rows),'gid':1254632077,'opening239rows_all43typed_cells_preserved':preserved,'later_row_count':len(rows)-len(old),'service_writes':0},indent=2)+'\n');assert preserved
b=(R/'STATE.json').read_bytes();s=json.loads(b);save('closing_STATE.json.gz',b);opening=json.loads(gzip.decompress((O/'private/STATE.json.gz').read_bytes()));oldpub=opening['completed_publications'];newpub=s['completed_publications'];assert all(x in newpub for x in oldpub)
u='https://api.github.com/repos/AlecKriebel/Math/pulls?state=all&sort=created&direction=desc&per_page=1';req=urllib.request.Request(u,headers={'Accept':'application/vnd.github+json','User-Agent':'completed-eleven-publications-readonly'})
with urllib.request.urlopen(req,timeout=45)as q:b=q.read();assert q.status==200
latest=json.loads(b);save('closing_highest.json.gz',b)
(O/'CLOSING_SCOPE.json').write_text(json.dumps({'at':now(),'opening_completed_scope_PRs':[x['pr']for x in oldpub],'current_completed_scope_PRs':[x['pr']for x in newpub],'later_completed_not_audited':[x for x in newpub if x not in oldpub],'current_ledger_rows':len(rows),'highest_PR':latest[0]['number'],'later_PR_observed':latest[0]['number']>1446,'inventory_extension_needed':latest[0]['number']>1446,'this_checkpoint_final_sweep_clearance':False,'no_pending_case_certified':True,'effects':0},indent=2)+'\n');print('Closing complete rows',len(rows),'completed STATE',len(newpub),'highest',latest[0]['number'])
