#!/usr/bin/env python3
"""Read-only PDF authentication and extraction; raw outputs stay private.
Usage: python -I -S -B authenticate_primary_inputs.py CASE REVIEW PDFTOTEXT
"""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,subprocess,sys,time
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def now():return datetime.now(timezone.utc).isoformat()
def main():
    A=Path(sys.argv[1]);R=Path(sys.argv[2]);receipts=json.loads((A/'PRIMARY_FETCH_RECEIPTS.json').read_bytes());out=[]
    for row in receipts['sources']:
        path=A/'private_sources'/row['name'];b=path.read_bytes();actual=pin(b)
        if actual!={k:row[k] for k in ['bytes','sha256']}:raise ValueError('PDF input pin '+row['name'])
        start=now();mono=time.monotonic_ns();p=subprocess.Popen([sys.argv[3],'-layout',str(path),'-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);launch=now();stdout,stderr=p.communicate(timeout=60)
        meta={'name':row['name'],'pdf':actual,'started_utc':start,'launched_utc':launch,'ended_utc':now(),'elapsed_monotonic_ns':time.monotonic_ns()-mono,'pid':p.pid,'returncode':p.returncode,'stdout':pin(stdout),'stderr':pin(stderr)}
        stem=R/'private_tmp'/('primary-'+path.stem)
        for suffix,raw in [('stdout.bin',stdout),('stderr.bin',stderr),('json',(json.dumps(meta,indent=2,sort_keys=True)+'\n').encode())]:
            with Path(str(stem)+'.'+suffix).open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        if p.returncode!=0 or stderr:raise ValueError('PDF extraction failed '+row['name'])
        supplied=(A/'private_sources'/(path.stem+'.txt')).read_bytes();meta['exact_supplied_text_match']=stdout==supplied;out.append(meta)
    priority=[]
    for row in json.loads((A/'PRIORITY_PARENT_FRESH_FETCH.json').read_bytes())['records']:
        if 'text_capture' not in row:continue
        b=gzip.decompress((A/row['text_capture']).read_bytes());actual=pin(b)
        if actual!={'bytes':row['text_bytes'],'sha256':row['text_sha256']}:raise ValueError('priority text pin')
        priority.append({'source':row['source'],'authenticated_text':actual,'source_url':row['url'],'fresh_pdf_pin_in_parent_receipt':{k:row[k] for k in ['bytes','sha256']},'scope':'Text independently rehashed and read; not a new binary retrieval'})
    result={'status':'PASS','primary_pdf_authentication_and_reextraction':out,'priority_text_authentication':priority,'raw_bodies_in_safe_output':False}
    (R/'PRIMARY_INPUT_CHECKS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
