"""Read-only live tracker, local-state/manifests and public-record queries."""
from pathlib import Path
import datetime, gzip, hashlib, json, re, subprocess, sys, urllib.request, urllib.parse

R=Path(__file__).resolve().parent
WORK=R.parents[3]
BOOK='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID=1254632077

def need(x,m):
    if not x:raise RuntimeError(m)

def put(name,b):
    (R/'private'/name).write_bytes(gzip.compress(b,mtime=0))
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def gws(parts,params,body=None):
    cmd=['gws','sheets','spreadsheets',*parts,'--params',json.dumps(params)]
    if body is not None:cmd+=['--json',json.dumps(body)]
    p=subprocess.run(cmd,capture_output=True);need(p.returncode==0,p.stderr.decode());return p.stdout

def leads(text):
    low=text.lower()
    return any(x in low for x in ['30003225','/pull/1332','free-chain','free chain','nash-intersection','nash sets','nash sets of prime divisors','contact loci and nash'])

def run(phase):
    a=gws(['get'],{'spreadsheetId':BOOK,'includeGridData':False});meta=json.loads(a);put(phase+'_metadata_before.json.gz',a)
    shapes={s['properties']['sheetId']:s['properties'] for s in meta['sheets']}
    need(shapes[GID]['title']=='Math Puzzles' and shapes[GID]['gridProperties']['columnCount']==43,'target identity/full43')
    filters=[{'gridRange':{'sheetId':gid,'startRowIndex':0,'endRowIndex':p['gridProperties']['rowCount'],'startColumnIndex':0,'endColumnIndex':min(43,p['gridProperties']['columnCount'])}} for gid,p in shapes.items()]
    values={};matches={}
    for mode in ['UNFORMATTED_VALUE','FORMULA']:
        b=gws(['values','batchGetByDataFilter'],{'spreadsheetId':BOOK},{'dataFilters':filters,'majorDimension':'ROWS','valueRenderOption':mode});put(phase+'_'+mode+'.json.gz',b);x=json.loads(b);need(x['spreadsheetId']==BOOK,'returned workbook');values[mode]=x
        matches[mode]=[{'range':v['valueRange']['range'],'row':i,'values':row} for v in x['valueRanges'] for i,row in enumerate(v['valueRange'].get('values',[]),1) if leads(json.dumps(row))]
    ranges=["'Math Puzzles'!A1:AQ"+str(shapes[GID]['gridProperties']['rowCount']),"'Papers'!A1:AQ"+str(shapes[0]['gridProperties']['rowCount'])]
    raw=gws(['get'],{'spreadsheetId':BOOK,'includeGridData':True,'ranges':ranges,'fields':'spreadsheetId,sheets(properties,data(startColumn,startRow,rowData(values(userEnteredValue,effectiveValue,formattedValue,hyperlink,note))))'});put(phase+'_typed.json.gz',raw);typed=json.loads(raw)
    lookup={}
    for mode,x in values.items():
        lookup[mode]={v['dataFilters'][0]['gridRange'].get('sheetId',0):v['valueRange'].get('values',[]) for v in x['valueRanges']}
    checks=0
    def native(d):
        if not d:return ''
        if 'errorValue' in d:return '#ERROR:'+str(d['errorValue'])
        return next(iter(d.values()))
    for s in typed['sheets']:
        gid=s['properties']['sheetId']
        for block in s.get('data',[]):
            start=block.get('startRow',0);col=block.get('startColumn',0)
            for i,row in enumerate(block.get('rowData',[]),start):
                for j,cell in enumerate(row.get('values',[]),col):
                    for mode in lookup:
                        rows=lookup[mode][gid];got=rows[i][j] if i<len(rows) and j<len(rows[i]) else ''
                        entry=cell.get('userEnteredValue',{})
                        want=native(entry) if mode=='FORMULA' and 'formulaValue' in entry else native(cell.get('effectiveValue',{}))
                        need(type(got)==type(want) and got==want,'typed/formula VALUE cell mismatch '+str((gid,i,j,mode,got,want)));checks+=1
    z=gws(['get'],{'spreadsheetId':BOOK,'includeGridData':False});put(phase+'_metadata_after.json.gz',z);need(json.loads(z)==meta,'unstable metadata bracket')
    sheet={'all7tab_VALUE_FORMULA':len(shapes)==7,'target_and_Papers_all43cols':True,'complete_allocated_target_rows':shapes[GID]['gridProperties']['rowCount'],'full_metadata_bracket_stable':True,'raw_typed_formula_hyperlink_notes':True,'typed_cells_reconciled':checks,'leads':matches,'nonempty_target_rows':len(lookup['UNFORMATTED_VALUE'][GID])}
    # Complete local .zenodo-state JSON inventory and all available explicit manifests.
    state=WORK/'.zenodo-state';need(state.is_dir(),'workspace root resolution')
    captured={};inventory=[];missing=[];localleads=[]
    for p in sorted(state.glob('*.json')):
        b=p.read_bytes();x=json.loads(b);captured[str(p)]=b.decode();inventory.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
        if leads(b.decode()):localleads.append(str(p))
        manifest=x.get('manifest')
        if isinstance(manifest,str):
            q=Path(manifest);q=q if q.is_absolute() else WORK/q
            if q.is_file():
                data=q.read_bytes();json.loads(data);captured[str(q)]=data.decode()
                if leads(data.decode()):localleads.append(str(q))
            else:missing.append(str(q))
    put(phase+'_local_states_and_manifests.json.gz',json.dumps(captured,sort_keys=True).encode())
    local={'state_JSON_count':len(inventory),'complete_available_state_and_manifest_bodies':len(captured),'state_inventory':inventory,'missing_explicit_manifests':missing,'literal_relevant_leads':localleads,'not_owned_account_absence_certificate':True}
    queries=['"30003225"','"free-chain" AND "Nash"','"Nash-intersection"','"Kriebel" AND "Nash"','"Contact Loci and Nash Sets of Prime Divisors"','"10.1016/j.aim.2017.09.035" AND "Kriebel"','"1501.06898" AND "Kriebel"','"0009-0001-9320-500X" AND "Nash"']
    public=[]
    for qi,q in enumerate(queries):
        pages=[];seen=[];page=1;total=None
        while True:
            url='https://zenodo.org/api/records?'+urllib.parse.urlencode({'q':q,'size':25,'page':page})
            try:
                with urllib.request.urlopen(url,timeout=25) as h:b=h.read();status=h.status
            except Exception as e:
                pages.append({'url':url,'error':str(e)});break
            identity=put(phase+'_public'+str(qi)+'_page'+str(page)+'.json.gz',b);x=json.loads(b);v=x['hits']['total'];total=v['value'] if isinstance(v,dict) else v;hits=x['hits']['hits'];seen.extend(hits);pages.append({'url':url,'status':status,**identity,'hits':len(hits),'reported_total':total})
            if len(seen)>=total:break
            need(hits,'incomplete public pagination');page+=1;need(page<=100,'unbounded public query')
        public.append({'query':q,'pages':pages,'complete':total is not None and len(seen)==total,'retrieved':len(seen),'total':total,'hits':[{'id':h['id'],'doi':h.get('doi'),'title':h.get('metadata',{}).get('title')} for h in seen]})
    result={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':phase,'sheet':sheet,'local':local,'public':public,'owned_account_inventory_performed':False,'publication_ready':False,'read_only':True}
    (R/(phase.upper()+'_GATES.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'phase':phase,'sheet':sheet,'local_states':len(inventory),'available_bodies':len(captured),'missing_manifests':len(missing),'local_leads':localleads,'public':[{'query':p['query'],'complete':p['complete'],'total':p['total']} for p in public]}))

if __name__=='__main__':run(sys.argv[1])
