"""Read-only network/local-primary reader; retain only authored provenance receipts.

Run with Python -B and PYTHONDONTWRITEBYTECODE=1. Full third-party bytes and
extracted text are not written. No Git subprocesses or write API calls.
"""
import datetime, hashlib, io, json, pathlib, sys, urllib.request
from pypdf import PdfReader

BASE = pathlib.Path(__file__).resolve().parent
RECEIPTS = BASE / 'PRIMARY_RECEIPTS.json'

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def read(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Independent-mathematical-primary-source-audit/1.0', 'Accept':'application/json,application/pdf,text/html;q=0.8'})
    started = now()
    with urllib.request.urlopen(req, timeout=25) as response:
        data = response.read()
        receipt = {'url':url,'access_started_utc':started,'access_finished_utc':now(), 'status':response.status,'final_url':response.url,'content_type':response.headers.get('Content-Type'),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    return data,receipt

def save(receipt):
    old=json.loads(RECEIPTS.read_text()) if RECEIPTS.exists() else []
    old.append(receipt)
    RECEIPTS.write_text(json.dumps(old, indent=2)+'\n')

kind, address = sys.argv[1:3]
try:
    if kind=='localpdf':
        data=pathlib.Path(address).read_bytes()
        receipt={'path':address,'access_finished_utc':now(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'source_reused_readonly':True}
    else:
        data, receipt = read(address)
    if kind=='record':
        item=json.loads(data)
        receipt['selected_primary_fields']={k:item.get(k) for k in ['id','doi','created','modified','updated','published','publication_date','conceptrecid','conceptdoi','metadata','files','links','is_published','pids'] if k in item}
        if 'metadata' in receipt['selected_primary_fields']:
            receipt['selected_primary_fields']['metadata']={k:item['metadata'].get(k) for k in ['title','doi','publication_date','creators','version','resource_type','relations'] if k in item['metadata']}
        receipt['selected_primary_fields'].pop('links',None)
        print(json.dumps(receipt,indent=2))
    elif kind=='github':
        item=json.loads(data)
        if isinstance(item, list):
            selected=[]
            for obj in item:
                selected.append({k:obj.get(k) for k in ['event','created_at','commit_id','sha','message','author','committer','url','node_id'] if k in obj})
        else:
            selected={k:item.get(k) for k in ['id','number','title','state','draft','created_at','updated_at','closed_at','merged_at','commits','changed_files','private','visibility','pushed_at','sha','commit','parents','html_url','head','base'] if k in item}
            for key in ['head','base']:
                if key in selected: selected[key]={k:selected[key].get(k) for k in ['sha','ref','label']}
        receipt['selected_primary_fields']=selected
        print(json.dumps(receipt,indent=2))
    elif kind=='datacite':
        item=json.loads(data)['data']['attributes']
        receipt['selected_primary_fields']={k:item.get(k) for k in ['doi','created','registered','published','updated','publicationYear','dates','version','url','titles','creators','state','relatedIdentifiers']}
        print(json.dumps(receipt,indent=2))
    elif kind in ('pdf','localpdf'):
        reader=PdfReader(io.BytesIO(data)); receipt['pages']=len(reader.pages)
        pages=list(range(1,len(reader.pages)+1)) if len(sys.argv)<4 else [int(x) for x in sys.argv[3].split(',')]
        receipt['pages_extracted_to_tool_output']=pages
        print(json.dumps(receipt,indent=2))
        for j in pages: print('\n--- PRIMARY PAGE '+str(j)+' ---\n'+reader.pages[j-1].extract_text())
    elif kind=='rawproof':
        local=pathlib.Path(sys.argv[3]).read_bytes()
        receipt['matches_frozen_local_bytes']=data==local
        receipt['local_sha256']=hashlib.sha256(local).hexdigest()
        print(json.dumps(receipt,indent=2))
    else: raise ValueError('unknown reader kind')
    save(receipt)
except Exception as exc:
    receipt={'url':address,'failed_utc':now(),'error_type':type(exc).__name__,'error':str(exc)}
    save(receipt); print(json.dumps(receipt,indent=2)); raise SystemExit(1)
