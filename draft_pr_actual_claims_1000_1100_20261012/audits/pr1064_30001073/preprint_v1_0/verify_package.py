#!/usr/bin/env python3
"""Strict explicit-guard verifier usable in a clean support archive extraction."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,re,stat,zipfile
ROOT=Path(__file__).resolve().parent
FIXED_TIME=(2026,10,14,0,0,0)
def require(c,m):
 if not c:raise ValueError(m)
def sha(data):return hashlib.sha256(data).hexdigest()
def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def safe(name):
 require(isinstance(name,str) and name and '\\' not in name and '\x00' not in name,'unsafe member name')
 p=PurePosixPath(name)
 require(not p.is_absolute() and '..' not in p.parts and '.' not in p.parts and str(p)==name,'unsafe relative path '+name)
 return name

def check():
 allow=load('SUPPORT_ALLOWLIST.json')['members'];require(allow==sorted(set(allow)),'allowlist must be sorted and unique')
 for name in allow:safe(name)
 require('SUPPORT_MANIFEST.json' in allow,'manifest missing from allowlist')
 manifest=load('SUPPORT_MANIFEST.json');records=manifest['entries']
 require([r['path'] for r in records]==[x for x in allow if x!='SUPPORT_MANIFEST.json'],'manifest exact coverage failed')
 for record in records:
  name=safe(record['path']);p=ROOT/name
  require(p.is_file() and not p.is_symlink(),'missing/symlink member '+name)
  data=p.read_bytes();require(len(data)==record['bytes'] and sha(data)==record['sha256'],'hash mismatch '+name)
  if name!='paper.pdf':data.decode('utf-8')
 require((ROOT/'paper.pdf').read_bytes().startswith(b'%PDF-'),'paper PDF signature missing')
 excluded=set(load('EXCLUSION_LEDGER.json')['local_package_files'])
 for p in ROOT.rglob('*'):
  if not p.is_file():continue
  name=p.relative_to(ROOT).as_posix()
  if name.startswith('tmp/'):continue
  require(name in allow or name in excluded,'unmanifested file '+name)
 copies=load('COPY_MAP.json')['copies']
 for c in copies:
  require(c['package_path'] in allow,'copy not distributed')
  data=(ROOT/c['package_path']).read_bytes()
  require(sha(data)==c['sha256'] and len(data)==c['bytes'],'copy map mismatch')
 require(sum(c['source_path'].startswith('submitted/') for c in copies)==9,'original nine-copy coverage failed')
 require(load('SAFE_INPUT_PINS.json')['records']==copies,'selected input pins mismatch')
 meta=load('metadata.json');require(load('publication/release_metadata.json')['metadata']==meta and load('publication/zenodo.json')['metadata']==meta,'normalized metadata differ')
 status=load('STATUS.json')
 require(status['publication_ready'] is False and status['issues_updated'] is False,'pending preparation gate altered')
 require(status['whole_package_reviews_completed']==0 and status['whole_package_reviews_required']>=2,'new review gate altered')
 require(status['novelty']=='UNKNOWN' and status['historical_priority']=='UNKNOWN','novelty boundary altered')
 require(load('support/CHECKS.json')['pass'] is True,'authored diagnostic record not passed')
 return allow

def check_archive(path,allow):
 require(path.is_file(),'archive missing')
 with zipfile.ZipFile(path) as z:
  infos=z.infolist();require([i.filename for i in infos]==allow,'archive exact member set/order failed')
  for info in infos:
   safe(info.filename)
   require(info.date_time==FIXED_TIME and info.create_system==3 and info.external_attr==(0o100644<<16),'archive timestamp/mode failed')
   require(info.compress_type==zipfile.ZIP_DEFLATED,'unexpected compression')
   require(not (info.flag_bits&1),'encrypted member rejected')
   require(z.read(info)==(ROOT/info.filename).read_bytes(),'archive bytes mismatch '+info.filename)

def check_binding(path,archive,required):
 if not path.exists():
  require(not required,'required deposit binding absent')
  return 'absent (permitted for clean extraction)'
 binding=json.loads(path.read_text(encoding='utf-8'))
 require(set(binding)=={'schema_version','paper_pdf','support_archive'},'binding fields differ')
 require(binding['schema_version']==1,'binding schema unsupported')
 for key,file in [('paper_pdf',ROOT/'paper.pdf'),('support_archive',archive)]:
  require(file is not None and file.is_file(),'present binding requires both deliverables')
  r=binding[key];require(r['path']==('paper.pdf' if key=='paper_pdf' else 'support.zip'),'binding names differ')
  data=file.read_bytes();require(r['bytes']==len(data) and r['sha256']==sha(data),'deposit binding mismatch '+key)
 return 'present and valid'

def main():
 p=argparse.ArgumentParser();p.add_argument('--archive');p.add_argument('--deposit-binding');p.add_argument('--require-deposit-binding',action='store_true');args=p.parse_args()
 allow=check()
 archive=Path(args.archive).resolve() if args.archive else (ROOT/'support.zip' if (ROOT/'support.zip').exists() else None)
 if archive is not None:check_archive(archive,allow)
 binding=Path(args.deposit_binding).resolve() if args.deposit_binding else ROOT/'publication/DEPOSIT_BINDING.json'
 result=check_binding(binding,archive,args.require_deposit_binding)
 print(json.dumps({'pass':True,'members':len(allow),'archive_checked':archive is not None,'deposit_binding':result},indent=2))
if __name__=='__main__':main()
