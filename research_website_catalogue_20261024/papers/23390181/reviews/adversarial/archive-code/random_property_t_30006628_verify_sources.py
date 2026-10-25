#!/usr/bin/env python3
"""Verify supplied source bytes and the complete-record exact-ID canonical hash.
No network access; source contents are never printed. No assertions are used.
"""
import argparse,hashlib,json,pathlib,sys

def fail(msg): raise ValueError(msg)
def pin(path, expected):
 data=path.read_bytes()
 if len(data)!=expected['bytes']: fail('byte count mismatch: '+path.name)
 if hashlib.sha256(data).hexdigest()!=expected['sha256']: fail('SHA256 mismatch: '+path.name)
 return data

def main(a):
 manifest=json.loads((pathlib.Path(__file__).parent/'sources.json').read_text())
 if a.mutant=='source_hash':manifest['corpus']['problems']['sha256']='0'*64
 if a.mutant=='pair_hash':manifest['canonical_pair']['sha256']='0'*64
 corpus={name:json.loads(pin(pathlib.Path(getattr(a,name)),expected)) for name,expected in manifest['corpus'].items()}
 p=[x for x in corpus['problems'] if str(x.get('id'))==manifest['problem_id']]
 if len(p)!=1:fail('exact-ID record count differs from one')
 p=p[0];r=corpus['reports'].get(p['problem_number'],{})
 data=json.dumps([p,r],sort_keys=True).encode()
 pair=manifest['canonical_pair']
 if len(data)!=pair['bytes'] or hashlib.sha256(data).hexdigest()!=pair['sha256']:fail('complete-record pair hash mismatch')
 c=[x for x in corpus['catalog'] if str(x.get('id'))==manifest['problem_id']]
 if len(c)!=1 or c[0]['review_hash']!=pair['sha256']:fail('catalog pair pin mismatch')
 checked=0
 for source in manifest['primary_sources']:
  pin(pathlib.Path(a.pdf_dir)/source['filename'],source);checked+=1
 return {'status':'PASS','corpus_files':3,'primary_pdf_files':checked,'complete_record_pair_sha256':pair['sha256'],'report_record_empty':r=={},'formal_mathematical_verification':False}

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for x in ['catalog','problems','reports','pdf-dir']:p.add_argument('--'+x,required=True)
 p.add_argument('--mutant',choices=['source_hash','pair_hash'])
 try:print(json.dumps(main(p.parse_args()),sort_keys=True,indent=2))
 except (ValueError,OSError,KeyError) as e:print(json.dumps({'status':'REJECTED','reason':str(e)}));sys.exit(1)
