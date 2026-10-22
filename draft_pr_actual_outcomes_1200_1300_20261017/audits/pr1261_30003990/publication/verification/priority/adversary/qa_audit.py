"""Consistency checks for this audit; not a proof of the universal theorem."""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
import hashlib,json

ROOT=Path(__file__).resolve().parent

def require(condition,message):
 if not condition:raise RuntimeError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

if __name__=='__main__':
 query=json.loads((ROOT/'QUERY_LEDGER.json').read_text())
 verdict=json.loads((ROOT/'VERDICT.json').read_text())
 inv=json.loads((ROOT/'SOURCE_INVENTORY.json').read_text())
 require(query['actual_calls']==len(query['calls'])==verdict['search_calls']==19,'search-call mismatch')
 require(sum(len(c['queries']) for c in query['calls'])==query['literal_queries']==verdict['literal_search_queries']==76,'query count mismatch')
 checked=0;pdfs=0
 for rec in inv['source_records']:
  if p:=rec.get('retained_payload'):
   f=ROOT/p['path'];data=f.read_bytes()
   require(len(data)==p['bytes'] and sha(f)==p['sha256'],'source byte mismatch '+str(f))
   require(data.startswith(b'%PDF')==p['is_pdf'],'signature mismatch '+str(f))
   checked+=1;pdfs+=p['is_pdf']
 require(pdfs==13,'valid PDF count mismatch')
 degree_cases=0
 for r in range(2,10001):
  m=r//2
  require(4*m<=2*r and 3*m>=r,'degree conversion failed')
  degree_cases+=1
 valley_cases=[]
 for k in range(1,17):
  t=Fraction(1,2**k);delta=t/16;eps=Fraction(1,2**(k*k))
  ratio=(1+eps)/eps
  require(ratio==1+2**(k*k),'doubling ratio algebra failed')
  require(t-2*delta > t/2+(t/2)/16,'expanded valley intersects next valley')
  valley_cases.append({'k':k,'doubling_ratio_exact':str(ratio)})
 input_records=[]
 for name in ['PROOF.md','AUDIT.md','SOURCE_VERIFICATION.json']:
  p=ROOT.parents[1]/'submitted'/name
  require(p.exists(),'missing reviewed input')
  input_records.append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)})
 for p in ROOT.glob('*.json'):json.loads(p.read_text())
 receipt={'checked_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','retained_source_payloads_checked':checked,'valid_pdf_payloads':pdfs,'degree_conversion_cases':degree_cases,'valley_ratio_algebra_cases':valley_cases,'reviewed_input_digests':input_records,'limits':'Consistency checks supplement the analytic derivation; no source-author code executed; no whole-work mathematical audit or priority certification.'}
 (ROOT/'QA_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({k:v for k,v in receipt.items() if k not in ['valley_ratio_algebra_cases','reviewed_input_digests']},indent=2))
