#!/usr/bin/env python3
"""Run an allowed reconciliation entry using externally pinned captured sources.

Run this file DIRECTLY with Python, never by importing a cached launcher module.
No local Python module is loaded through normal import or cached .pyc lookup.
"""
from pathlib import Path
import argparse,hashlib,json,re,sys,types
DEPENDENCIES=('metadata_rules','scope_sheet_evidence','expected_state')
ENTRIES=('collect_readbacks.py','analyze_readbacks.py','finalize_snapshot.py','preparation_controls.py','frozen_source_cache_controls.py')
class FrozenSourceError(RuntimeError):pass
class OfflineTransportError(RuntimeError):pass
def require(ok,message):
 if not ok:raise FrozenSourceError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def capture_sources(root,expected_freeze_sha256):
 root=Path(root)
 require(re.fullmatch('[0-9a-f]{64}',expected_freeze_sha256) is not None,'An externally pinned lowercase SHA-256 is required')
 freeze_path=root/'PREPARATION_FREEZE.json'
 require(freeze_path.is_file() and not freeze_path.is_symlink(),'Preparation freeze must be a regular file')
 freeze_bytes=freeze_path.read_bytes()
 require(sha(freeze_bytes)==expected_freeze_sha256,'Preparation freeze differs from the external SHA-256 pin')
 freeze=json.loads(freeze_bytes)
 pins={name:pin for name,pin in freeze['files'].items() if '/' not in name and name.endswith('.py')}
 actual={path.name for path in root.glob('*.py')}
 require(actual==set(pins),'Root Python source inventory differs from the pinned preparation freeze')
 require('run_frozen_sources.py' in pins and all(name+'.py' in pins for name in DEPENDENCIES),'Required frozen launcher/dependency sources are absent')
 captured={}
 for name,pin in sorted(pins.items()):
  path=root/name
  require(path.is_file() and not path.is_symlink(),'Frozen source must be a regular file: '+name)
  data=path.read_bytes()
  require(len(data)==pin['bytes'] and sha(data)==pin['sha256'],'Frozen source bytes differ: '+name)
  captured[name]=data
 return captured,{name:sha(data) for name,data in captured.items()}
def disable_transports():
 """Process-local preparation guard; deny sockets and child processes pre-dispatch."""
 blocked={'socket.__new__','socket.connect','socket.connect_ex','socket.getaddrinfo','socket.gethostbyname','subprocess.Popen','os.system','os.posix_spawn','os.posix_spawnp','os.exec','os.fork','pty.spawn'}
 def audit(event,args):
  if event in blocked:raise OfflineTransportError('Offline preparation forbids transport: '+event)
 sys.addaudithook(audit)
def run(root,freeze_sha256,entry,args=(),offline=False):
 root=Path(root).resolve()
 require(entry in ENTRIES,'Entry script is not allowed')
 require(not (offline and entry=='collect_readbacks.py' and '--collect' in args),'Offline preparation cannot dispatch collection')
 captured,pins=capture_sources(root,freeze_sha256)
 require(entry in captured,'Allowed entry is not present in the pinned source inventory')
 if offline:disable_transports()
 missing=object();names=(*DEPENDENCIES,'__main__');previous={name:sys.modules.get(name,missing) for name in names}
 old_argv=sys.argv;old_path=sys.path[:];old_dont_write=sys.dont_write_bytecode
 try:
  sys.dont_write_bytecode=True
  for name in DEPENDENCIES:
   module=types.ModuleType(name)
   module.__dict__.update({'__file__':str(root/(name+'.py')),'__package__':'','__cached__':None,'__frozen_source_sha256__':pins[name+'.py']})
   sys.modules[name]=module
   exec(compile(captured[name+'.py'],str(root/(name+'.py')),'exec',dont_inherit=True,optimize=sys.flags.optimize),module.__dict__)
  main=types.ModuleType('__main__')
  main.__dict__.update({'__file__':str(root/entry),'__package__':None,'__cached__':None,'__frozen_source_sha256__':pins[entry],'__frozen_sources__':pins,'__frozen_preparation_freeze_sha256__':freeze_sha256})
  sys.modules['__main__']=main;sys.argv=[str(root/entry),*args]
  exec(compile(captured[entry],str(root/entry),'exec',dont_inherit=True,optimize=sys.flags.optimize),main.__dict__)
  return 0
 finally:
  sys.argv=old_argv;sys.path[:]=old_path;sys.dont_write_bytecode=old_dont_write
  for name,old in previous.items():
   if old is missing:sys.modules.pop(name,None)
   else:sys.modules[name]=old
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--freeze-sha256',required=True,help='Exact preparation-freeze hash independently supplied by the reviewing parent')
 parser.add_argument('--offline',action='store_true',help='Deny sockets/child processes; mandatory for preparation controls and offline readiness checks')
 parser.add_argument('entry',choices=ENTRIES)
 parser.add_argument('entry_args',nargs=argparse.REMAINDER)
 args=parser.parse_args()
 try:return run(Path(__file__).resolve().parent,args.freeze_sha256,args.entry,args.entry_args,args.offline)
 except FrozenSourceError as exc:
  print('Frozen-source guard: '+str(exc),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
