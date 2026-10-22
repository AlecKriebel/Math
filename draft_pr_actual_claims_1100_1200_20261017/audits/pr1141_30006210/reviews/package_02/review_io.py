from pathlib import Path
import hashlib,json,datetime,sys
BASE=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1100_1200_20261017/audits/pr1141_30006210')
REVIEW=BASE/'reviews/package_02'
def pin(path,purpose):
 p=Path(path).resolve()
 if '/reviews/package_01/' in str(p):raise RuntimeError('Forbidden preceding whole-package review')
 d=p.read_bytes(); rec={'path':str(p),'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest(),'purpose':purpose,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 ledger=REVIEW/'READ_LEDGER.json'; rows=json.loads(ledger.read_text());rows.append(rec);ledger.write_text(json.dumps(rows,indent=2)+'\n');return d
if __name__=='__main__':
 p=Path(sys.argv[1]);p=p if p.is_absolute() else BASE/p
 data=pin(p,sys.argv[2] if len(sys.argv)>2 else 'semantic full read')
 if len(sys.argv)>3:
  lines=data.decode().splitlines(); a,b=map(int,sys.argv[3].split(':'));print('\n'.join(f'{i+1}: {s}' for i,s in enumerate(lines) if a<=i+1<=b))
 else:print(data.decode())
