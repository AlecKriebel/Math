"""Read-only live tracker preparation; never append before publication gates."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess

D=Path(__file__).resolve().parent
ID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';GID=1254632077
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
private=D/('private_tracker_preflight_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
private.mkdir(exist_ok=False);cli=shutil.which('gws');assert cli
receipts=[]
def run(label,argv):
    start=utc();r=subprocess.run(argv,cwd=D,capture_output=True,timeout=55)
    for name,b in [('stdout',r.stdout),('stderr',r.stderr)]:(private/(label+'.'+name)).write_bytes(b)
    rec=dict(argv=argv,cwd=str(D),started_utc=start,ended_utc=utc(),exit_code=r.returncode,stdout_bytes=len(r.stdout),stdout_sha256=sha(r.stdout),stderr_bytes=len(r.stderr),stderr_sha256=sha(r.stderr))
    (private/(label+'.json')).write_text(json.dumps(rec,indent=2)+'\n');receipts.append(rec)
    assert r.returncode==0,(label,r.stderr.decode(errors='replace'))
    return json.loads(r.stdout)
meta=run('metadata',[cli,'sheets','spreadsheets','get','--params',json.dumps(dict(spreadsheetId=ID),separators=(',',':'))])
sheet=next(x['properties'] for x in meta['sheets'] if x['properties']['sheetId']==GID)
assert sheet['title']=='Math Puzzles'
grid=sheet['gridProperties'];assert grid['columnCount']>=4
rows=run('values',[cli,'sheets','spreadsheets','values','get','--params',json.dumps(dict(spreadsheetId=ID,range="'Math Puzzles'!A1:D"+str(grid['rowCount'])),separators=(',',':'))])
values=rows.get('values',[]);assert values[0]==['Original Problem','Solution Chat URL','DOI','Notes']
title='Full 5-torsion of the regular-pentagon quintic pencil'
hits=[dict(physical_row=i+1,cells=x) for i,x in enumerate(values) if i and ('20000450' in '\n'.join(x) or title.lower() in '\n'.join(x).lower())]
record=dict(utc=utc(),status='PASS_READ_ONLY_LIVE_TRACKER_LAYOUT_AND_EXISTING_TARGET_SCAN',spreadsheet_id=ID,gid=GID,sheet_title=sheet['title'],grid_rows=grid['rowCount'],grid_columns=grid['columnCount'],headers=values[0],returned_rows=len(values),matching_problem_or_exact_title_rows=hits,native_read_receipts=receipts,private_raw_directory=str(private),current_writer_policy='Final writer must freshly reread layout, rows and actual published DOI immediately before its single append; this preflight is not write approval or a stale-row lock.',tracker_append_performed=False,publication_clearance=False)
out=D/'TRACKER_READ_ONLY_PREFLIGHT.json';assert not out.exists();out.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ['native_read_receipts','private_raw_directory','matching_problem_or_exact_title_rows']}|dict(matching_problem_or_exact_title_row_count=len(hits)),indent=2))
