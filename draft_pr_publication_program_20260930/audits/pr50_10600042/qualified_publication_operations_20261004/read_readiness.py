"""Read operational prerequisites without changing any remote or native state."""
from pathlib import Path
import datetime as dt
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

if sys.flags.optimize or sys.argv[1:]:
    raise RuntimeError('No-argument nonoptimized invocation required')
own = Path(__file__).resolve().parent
repo = own.parents[3]
private = own/'private'
private.mkdir(exist_ok=True)
source = Path(__file__).read_bytes()
(private/'READINESS_PRELAUNCH_SOURCE.py').write_bytes(source)
commands=[]
def run(argv, name, allowed=(0,)):
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    child=subprocess.Popen(argv,cwd=repo,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    (private/(name+'.stdout')).write_bytes(out)
    (private/(name+'.stderr')).write_bytes(err)
    rec={'argv':argv,'started_utc':start,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
         'actual_pid':child.pid,'exit_code':child.returncode,
         'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),
         'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest()}
    commands.append(rec)
    (private/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
    if child.returncode not in allowed:
        raise RuntimeError('Readiness command failed: '+name+'; output retained privately')
    return out
def git(*args):
    return run(['git','--no-optional-locks',*args],'git-'+str(len(commands)))
branch=git('branch','--show-current').decode().strip()
head=git('rev-parse','HEAD').decode().strip()
index=git('diff','--cached','--name-only','-z')
spec=importlib.util.spec_from_file_location('operations_zenodo',repo/'zenodo_deposit_tool/zenodo.py')
z=importlib.util.module_from_spec(spec)
spec.loader.exec_module(z)
token_available=False
token_failure_kind=None
try:
    token=z.token_for('production')
    token_available=bool(token)
    del token
except z.DepositError:
    token_failure_kind='Token unavailable or malformed; private value never printed'
manifest=own.parent/'publication_package_v3/zenodo-deposit.json'
statefile,state=z.local_state(manifest,'production')
gws='/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'
version=run([gws,'--version'],'gws-version').decode().strip()
schemas={}
for name in ('sheets.spreadsheets.get','sheets.spreadsheets.values.get','sheets.spreadsheets.values.append'):
    out=run([gws,'schema',name],name.replace('.','-')+'-schema')
    schemas[name]={'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()}
sid='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
out=run([gws,'sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':sid,
             'fields':'spreadsheetId,sheets(properties(sheetId,title))'})],'gws-tab-read')
meta=json.loads(out)
assert meta['spreadsheetId']==sid
tabs=[x['properties'] for x in meta['sheets'] if x['properties']['sheetId']==1254632077]
assert len(tabs)==1
title=tabs[0]['title']
quoted="'"+title.replace("'","''")+"'"
out=run([gws,'sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':sid,
             'range':quoted+'!A1:D1','majorDimension':'ROWS','valueRenderOption':'UNFORMATTED_VALUE'})],'gws-header-read')
header=json.loads(out)
expected=['Original Problem','Solution Chat URL','DOI','Notes']
assert header['values']==[expected]
gh=run(['gh','pr','view','50','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,mergeable,mergeStateStatus,url'],'gh-pr50-read')
pr=json.loads(gh)
assert pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']=='7260315f8b8b193020c09d4ef6df9d943a3a13ff'
summary={'schema':'pr50-qualified-publication-operational-readiness/v1',
         'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),
         'source_sha256':hashlib.sha256(source).hexdigest(),'branch':branch,'dated_HEAD':head,
         'index_empty_at_readback':index==b'',
         'zenodo_token_locally_available':token_available,'zenodo_token_failure_kind':token_failure_kind,
         'zenodo_live_token_scopes_not_probed':True,'production_manifest_state_exists':state is not None,
         'production_state_id':state.get('id') if state else None,
         'gws_version':version,'gws_authenticated_metadata_and_header_reads_succeeded':True,
         'spreadsheet_id':sid,'sheet_id':1254632077,'resolved_tab':title,'actual_headers':expected,
         'schema_pins':schemas,'PR_current_readback':pr,
         'no_stage_publish_append_or_Git_mutation_performed':True,
         'pr50_priority_certification_conferred':False,'operational_audit_percent':80}
(own/'READINESS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
