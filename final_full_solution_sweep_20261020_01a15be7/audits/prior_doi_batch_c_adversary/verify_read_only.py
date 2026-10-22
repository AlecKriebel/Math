#!/usr/bin/env python3
"""Rehash sealed evidence; optional live GET/read checks. Never mutates external state.
Run with python3 -B. No candidate-code loading; no credential output; no raw ledger output.
"""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,re,subprocess,urllib.request,urllib.error
A=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)

def read_json(p):return json.loads(p.read_text())
def cli(cmd):
    p=subprocess.run(cmd,capture_output=True,timeout=90)
    need(p.returncode==0,'Read command failed; inspect locally without exposing credentials')
    return json.loads(p.stdout)
def http(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'independent-publication-accounting/1.0'}),timeout=30) as r:return {'status':r.status,'final_url':r.url,'body':r.read()}
    except urllib.error.HTTPError as e:return {'status':e.code,'final_url':e.url,'body':e.read()}
    except Exception as e:return {'status':None,'error':type(e).__name__}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--live',action='store_true');args=parser.parse_args()
    manifest=read_json(A/'SEALED_MANIFEST.json');checks=0
    for z in manifest['files']:
        rel=Path(z['path']);need(not rel.is_absolute() and '..' not in rel.parts,'unsafe manifest path')
        p=A/rel;need(p.is_file() and not p.is_symlink(),'missing or linked sealed artifact: '+str(rel))
        data=p.read_bytes();need(len(data)==z['bytes'] and hashlib.sha256(data).hexdigest()==z['sha256'],'seal mismatch: '+str(rel));checks+=1
    decisions=read_json(A/'BATCH_C_ADVERSARIAL_DECISIONS.json')['items'];need(len(decisions)==12,'wrong item count')
    for x in decisions:
        c=x['proposed_four_cells'];need(len(c)==4 and all(isinstance(s,str) for s in c) and c[1]=='','row schema/B mismatch')
    pins=read_json(A/'PR_BINDINGS.json')['checks'];need(sum(len(x['complete_paths']) for x in pins)==188,'path inventory mismatch')
    out={'sealed_artifacts_checked':checks,'four_cell_rows_checked':12,'live_requested':args.live,'external_writes':False,'candidate_code_executed':False}
    if args.live:
        def pr_check(z):
            n=z['pr'];p=cli(['gh','api',f'repos/AlecKriebel/Math/pulls/{n}'])
            need(p['head']['sha']==z['head'] and p['base']['sha']==z['base'],'live head/base drift PR'+str(n))
            need(hashlib.sha256((p.get('body') or '').encode()).hexdigest()==z['body_sha256'],'live body drift PR'+str(n))
            q=cli(['gh','api',f"repos/AlecKriebel/Math/compare/{z['base']}...{z['head']}"])
            files=q.get('files',[]);need(len(files)<300,'possibly truncated comparison')
            actual={(f['filename'],f['sha'],f['status']) for f in files};expected={(f['path'],f['blob'],f['status']) for f in z['complete_paths']}
            need(actual==expected,'live complete path/blob/status drift PR'+str(n))
            return {'pr':n,'source_pins_match':True,'state':p['state'],'draft':p['draft'],'merged':p['merged'],'state_changed':p['state']!=z['state'] or p['merged']!=z['merged']}
        with concurrent.futures.ThreadPoolExecutor(3) as ex:out['live_pr_checks']=list(ex.map(pr_check,pins))
        book='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';gid=1254632077
        body={'dataFilters':[{'gridRange':{'sheetId':gid}}],'majorDimension':'ROWS','valueRenderOption':'FORMATTED_VALUE'}
        sheet=cli(['gws','sheets','spreadsheets','values','batchGetByDataFilter','--params',json.dumps({'spreadsheetId':book}),'--json',json.dumps(body)])
        ranges=sheet['valueRanges'];need(len(ranges)==1 and ranges[0]['dataFilters']==body['dataFilters'],'numeric grid binding drift')
        vals=ranges[0]['valueRange']['values'];need(vals[0]==['Original Problem','Solution Chat URL','DOI','Notes'],'ledger schema drift');need(max(map(len,vals))<=4,'ledger schema expanded; human semantic adoption needed')
        leads={}
        for x in decisions:
            needles=x['publication_aliases']+x['supporting_source_identifiers']+x['original_problem_ids']+[x['target'].split(' — ')[0]]
            leads[str(x['pr'])]=[i for i,row in enumerate(vals[1:],2) if any(k.casefold() in ' '.join(map(str,row)).casefold() for k in needles)]
        out['live_ledger']={'rows':len(vals),'range':ranges[0]['valueRange']['range'],'identifier_leads':leads,'semantic_recheck_required_before_any_write':True}
        def doi_check(x):
            r=http('https://doi.org/'+x['existing_doi']);return {'pr':x['pr'],'doi':x['existing_doi'],'status':r.get('status'),'final_url':r.get('final_url'),'error':r.get('error')}
        with concurrent.futures.ThreadPoolExecutor(4) as ex:out['live_doi_checks']=list(ex.map(doi_check,decisions))
        r=http('https://zenodo.org/api/records/23062843');need(r.get('status')==200,'live existing Zenodo record unavailable');z=json.loads(r['body']);meta=z['metadata'];out['live_1122']={'id':z['id'],'doi':z.get('doi',meta.get('doi')),'conceptdoi':z.get('conceptdoi'),'files':[{k:v for k,v in f.items() if k in ('key','size','checksum')} for f in z.get('files',[])],'note':'Inventory observation only; exact payload bytes were independently verified in the sealed evidence. Recheck them before an update.'}
    print(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
