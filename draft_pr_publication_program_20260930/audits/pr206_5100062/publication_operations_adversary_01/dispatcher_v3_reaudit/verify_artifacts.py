"""Read-only source re-audit artifact verifier, never an operational entry point."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json,stat
ROOT=Path(__file__).resolve().parent

def need(ok,msg):
 if type(ok)is not bool or not ok:raise RuntimeError(msg)
def pin(p):
 raw=p.read_bytes();return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def safe(rel):
 need(type(rel)is str and rel and not Path(rel).is_absolute() and '..' not in Path(rel).parts,'unsafe relative path')
 p=ROOT/rel;need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'safe payload not regular normalized file');return p

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fixtures',action='store_true');args=ap.parse_args()
 seal=json.loads((ROOT/'SEAL.json').read_bytes());raw=(ROOT/'SAFE_MANIFEST.json').read_bytes();need(hashlib.sha256(raw).hexdigest()==seal['manifest_sha256'],'manifest pin changed');m=json.loads(raw)
 for x in m['files']:need(pin(safe(x['path']))=={k:x[k] for k in ('bytes','sha256')},'payload changed '+x['path'])
 need(len(m['files'])==seal['payload_file_count'] and sum(x['bytes'] for x in m['files'])==seal['payload_total_bytes'],'payload accounting')
 old=json.loads((ROOT/'PRESERVED_PRIOR_AUDIT_PINS.json').read_bytes())
 for n,w in old.items():need(pin(ROOT.parent/n)==w,'prior audit changed '+n)
 count=0
 if args.fixtures:
  index=json.loads((ROOT/'SYNTHETIC_FIXTURE_INDEX.json').read_bytes())
  for x in index['leaves']:
   q=ROOT/x['path'];mode=q.lstat().st_mode
   if x['kind']=='file':need(stat.S_ISREG(mode) and pin(safe(x['path']))=={k:x[k] for k in ('bytes','sha256')},'fixture file changed')
   elif x['kind']=='symlink':need(stat.S_ISLNK(mode) and str(q.readlink())==x['target'],'fixture symlink changed')
   elif x['kind']=='fifo':need(stat.S_ISFIFO(mode),'fixture FIFO changed')
   elif x['kind']=='directory':need(stat.S_ISDIR(mode),'fixture leaf directory changed')
   else:raise RuntimeError('unrecognized fixture kind')
   count+=1
 print(json.dumps({'status':'PASS','safe_payloads':len(m['files']),'fixture_leaves_checked':count,'prior_audit_unchanged':True,'source_reaudit_only':True,'actual_service_calls':0},sort_keys=True))
if __name__=='__main__':main()
