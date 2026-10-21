#!/usr/bin/env python3
"""Read-only live ledger/public-record leads; root must decide result identity.

This tool never appends a row, publishes, changes a PR, or disposes a candidate.
"""
import argparse
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import urllib.request
import zipfile
from sweep_io import atomic_json

ROOT=Path(__file__).resolve().parent
SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'


def get(url):
    request=urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-publication-audit/1.0'})
    with urllib.request.urlopen(request,timeout=45) as response:
        return response.read(),{'status':response.status,'final_url':response.url}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('pr',type=int)
    parser.add_argument('--problem-id',action='append',default=[])
    parser.add_argument('--term',action='append',default=[])
    parser.add_argument('--record',type=int,action='append',default=[])
    parser.add_argument('--download',action='store_true')
    args=parser.parse_args()
    if args.pr<9:raise RuntimeError('Outside sweep scope')
    raw=ROOT/'raw'/f'pr{args.pr:04d}'
    if raw.is_symlink() or not raw.resolve().is_relative_to(ROOT):raise RuntimeError('Unsafe output')
    raw.mkdir(parents=True,exist_ok=True)
    params={'spreadsheetId':SHEET,'range':"'Math Puzzles'!A1:AQ1169",'valueRenderOption':'FORMATTED_VALUE'}
    value=json.loads(subprocess.run(['gws','sheets','spreadsheets','values','get','--params',json.dumps(params)],capture_output=True,text=True,check=True).stdout)
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    atomic_json(raw/'ledger_live.json',{'checked_at':now,'response':value})
    matches=[]
    for n,row in enumerate(value.get('values',[]),1):
        joined=' '.join(str(x) for x in row)
        reasons=[]
        if re.search(r'github\.com/AlecKriebel/Math/pull/'+str(args.pr)+r'(?!\d)',joined,re.I):reasons.append('exact_PR_reference')
        elif re.search(r'\bPR\s*#?'+str(args.pr)+r'(?!\d)',joined,re.I):reasons.append('exact_PR_label')
        for identifier in args.problem_id:
            if re.search(r'(?<!\d)'+re.escape(identifier)+r'(?!\d)',joined):reasons.append('problem_id:'+identifier)
        for term in args.term:
            if term.casefold() in joined.casefold():reasons.append('term:'+term)
        if reasons:matches.append({'row':n,'values':row,'reasons':reasons})
    records=set(args.record)
    for match in matches:
        for s in match['values']:
            records.update(int(v) for v in re.findall(r'10\.5281/zenodo\.(\d+)',str(s)))
    verification=[]
    for record in sorted(records):
        wire,_=get('https://zenodo.org/api/records/'+str(record))
        atomic_json(raw/f'zenodo_{record}.json',json.loads(wire))
        value_record=json.loads(wire)
        metadata=value_record.get('metadata',{})
        files=[]
        for item in value_record.get('files',[]):
            file={'name':item['key'],'size':item['size'],'checksum':item['checksum']}
            if args.download:
                if item['size']>100_000_000:raise RuntimeError('Large payload requires root storage decision')
                data,_=get(item['links']['self'])
                if len(data)!=item['size'] or item['checksum']!='md5:'+hashlib.md5(data).hexdigest():raise RuntimeError('Payload integrity mismatch')
                # Preserve by content hash; remote names cannot affect filesystem paths.
                digest=hashlib.sha256(data).hexdigest()
                (raw/f'payload_{digest}.bin').write_bytes(data)
                file.update(sha256=digest,download_verified=True)
                if item['key'].lower().endswith('.zip'):
                    with zipfile.ZipFile(io.BytesIO(data)) as archive:
                        if archive.testzip():raise RuntimeError('ZIP integrity error')
                        names=archive.namelist()
                    file.update(zip_crc_ok=True,members=names)
            files.append(file)
        _,resolution=get('https://doi.org/'+value_record['doi'])
        verification.append({'record':record,'doi':value_record['doi'],'title':metadata.get('title'),'description':metadata.get('description'),'creators':metadata.get('creators'),'publication_date':metadata.get('publication_date'),'published':value_record.get('state')=='done' and value_record.get('submitted') is True,'files':files,'doi_resolution':resolution})
    result={'pr':args.pr,'checked_at':now,'ledger_rows':len(value.get('values',[])),'matches':matches,'records':verification,'identity_verdict':'pending_root_scope_comparison; title/number leads alone do not authorize skip or new publication'}
    atomic_json(ROOT/f'PR{args.pr:04d}_PUBLICATION_LEADS.json',result)
    view={**result,'records':[{**{k:v for k,v in x.items() if k!='files'},
          'files':[{'name':f['name'],'bytes':f['size'],'download_verified':f.get('download_verified',False),
                    'zip_members':len(f.get('members',[])),
                    'source_present':any(n.endswith(('.tex','.md')) for n in f.get('members',[])),
                    'code_present':any(n.endswith(('.py','.sage','.ipynb','.jl')) for n in f.get('members',[]))}
                   for f in x['files']]} for x in result['records']]}
    print(json.dumps(view,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
