from pathlib import Path
import datetime,hashlib,json,sys
R=Path(__file__).resolve().parent;P=R/'INPUT_FREEZE.json';EXPECTED='1da81cb82f6f29348d25212a973fb342bb82489cc6d34aec47d5979fbeb25fd3'
def main():
 stage=sys.argv[1] if len(sys.argv)>1 else 'END';d=json.loads(P.read_text());A=Path(d['root']);entries=[];bad=[]
 anchor=hashlib.sha256(P.read_bytes()).hexdigest()
 if anchor!=EXPECTED:bad.append('INPUT_FREEZE anchor')
 for scope,items in [('internal',d['files']),('external_readonly',d['external_readonly_inputs'])]:
  for e in items:
   p=Path(e['path']);p=p if p.is_absolute() else A/p;b=p.read_bytes();sha=hashlib.sha256(b).hexdigest();ok=len(b)==e['bytes'] and sha==e['sha256'];entries.append({'scope':scope,'path':str(p),'bytes':len(b),'sha256':sha,'ok':ok})
   if not ok:bad.append(str(p))
 result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'anchor_sha256':anchor,'expected_anchor':EXPECTED,'internal_inputs':len(d['files']),'external_readonly_inputs':len(d['external_readonly_inputs']),'authenticated_count':len(entries),'entries':entries,'bad':bad,'status':'PASS' if not bad else 'FAIL'}
 (R/('AUTHENTICATION_'+stage+'.json')).write_text(json.dumps(result,indent=2)+'\n')
 if bad:raise RuntimeError('Inputs changed: '+repr(bad))
 print(json.dumps({'status':'PASS','authenticated':len(entries),'stage':stage}))
if __name__=='__main__':main()
