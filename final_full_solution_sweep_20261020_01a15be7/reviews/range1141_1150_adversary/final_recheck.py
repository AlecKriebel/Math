"""Final GET-only service and captured-payload preservation check."""
from capture import *
from publications import get

def require(ok,msg):
    if not ok:raise ValueError(msg)
out={'checkpoint':CHECKPOINT,'at_start':now(),'prs':[],'publications':[]}
for n in range(1141,1151):
    before=json.loads((PRIVATE/f'pr{n}/live_initial.json').read_text())
    raw=api(f'pulls/{n}');save(PRIVATE/f'pr{n}/live_final.json',raw);after=json.loads(raw)
    fields=['body','state','merged','merged_at','title','draft']
    require(all(before.get(k)==after.get(k) for k in fields),'pr-fields')
    require(before['head']['sha']==after['head']['sha'] and before['base']['sha']==after['base']['sha'],'pr-head-base')
    cap=json.loads((PRIVATE/f'pr{n}/capture_receipt.json').read_text())
    files=json.loads(api(f'pulls/{n}/files?per_page=100'))
    save(PRIVATE/f'pr{n}/live_files_final.json',json.dumps(files,indent=2).encode())
    require(sorted(f['filename'] for f in files)==sorted(cap['changed_paths']),'pr-paths')
    for f in cap['payloads']:
        data=(HERE/f['path']).read_bytes();require(len(data)==f['bytes'] and sha(data)==f['sha256'],'captured-head-preservation')
    out['prs'].append({'pr':n,'head':after['head']['sha'],'base':after['base']['sha'],'body_sha256':sha((after['body'] or '').encode()),'state':after['state'],'merged':after['merged'],'files':len(files),'head_base_body_status_paths_unchanged':True})
for n,record in [(1141,23443301),(1150,23444050)]:
    before=json.loads((PRIVATE/f'publication{n}/record_initial.json').read_text())
    raw,_,_=get(f'https://zenodo.org/api/records/{record}');save(PRIVATE/f'publication{n}/record_final.json',raw);after=json.loads(raw)
    for k in ['doi','metadata','submitted','state','status','files']:require(before[k]==after[k],'provider-'+k)
    hashes=[]
    for f in after['files']:
        data,_,code=get(f['links']['self']);old=(PRIVATE/f'publication{n}'/f['key']).read_bytes()
        require(code==200 and data==old,'provider-payload-preservation')
        hashes.append({'name':f['key'],'bytes':len(data),'sha256':sha(data),'md5':hashlib.md5(data).hexdigest()})
    _,dest,status=get('https://doi.org/'+after['doi'])
    require(status==200 and dest.rstrip('/')==f'https://zenodo.org/records/{record}','doi-destination')
    out['publications'].append({'pr':n,'record':record,'published':after['submitted'] and after['status']=='published' and after['state']=='done','native_metadata_and_files_unchanged':True,'doi_destination':dest,'all_payloads':hashes})
sid='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
raw=subprocess.check_output(['gws','sheets','+read','--spreadsheet',sid,'--range',"'Math Puzzles'!A:AQ"])
save(PRIVATE/'gws_final.json',raw)
meta=subprocess.check_output(['gws','sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':sid,'fields':'spreadsheetId,sheets.properties'})])
save(PRIVATE/'gws_metadata_final.json',meta)
require(any(s['properties']['sheetId']==1254632077 and s['properties']['title']=='Math Puzzles' for s in json.loads(meta)['sheets']),'sheet-gid-title')
initial=json.loads((PRIVATE/'gws_initial.json').read_text());final=json.loads(raw)
require(initial==final,'gws-full-response-preservation')
out['gws']={'spreadsheet':sid,'gid':1254632077,'range':final['range'],'full_initial_final_response_equal':True,'rows':len(final['values']),'columns':final['values'][0],'unique_publication_rows':[163,165]}
for f in json.loads((PRIVATE/'checkpoint_receipts.json').read_text()):
    data=(HERE/f['path']).read_bytes();require(len(data)==f['bytes'] and sha(data)==f['sha256'],'checkpoint-capture-preservation')
for f in json.loads((PRIVATE/'release_binding_captures.json').read_text()):
    data=(HERE/f['path']).read_bytes();require(len(data)==f['bytes'] and sha(data)==f['sha256'],'immutable-release-capture-preservation')
out['at_end']=now();out['captured_checkpoint_and_release_bytes_preserved']=True
(HERE/'FINAL_RECHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':True,'at_end':out['at_end'],'prs':10,'provider_payloads':4,'ledger_rows':len(final['values'])}))
