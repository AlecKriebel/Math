#!/usr/bin/env python3
"""Detailed actual fresh-writer case identities and stderr in both directions."""
import datetime,hashlib,json,os,subprocess,sys,tempfile,zipfile
from pathlib import Path
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pins(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file() and not p.is_symlink()}
def require(x,m):
 if not x:raise RuntimeError(m)
output=W/'PHYSICAL_WRITER_REGRESSION.json';require(not output.exists(),'Do not overwrite actual physical receipts');receipts=[]
with tempfile.TemporaryDirectory(prefix='case_alias01-physical-own-',dir=W) as temp:
 base=Path(temp).resolve()
 with zipfile.ZipFile(D/'verification_kit.zip') as z:z.extractall(base)
 kit=base/'verification_kit';alias=base/'VERIFICATION_KIT';before=pins(kit);require(alias.samefile(kit),'Host case alias unavailable')
 outside=base/'outside';outside.mkdir();outsidealias=base/'OUTSIDE';require(outsidealias.samefile(outside),'Host outside case alias unavailable')
 for optimized in [False,True]:
  prefix=[sys.executable,'-B','-I']+(['-O'] if optimized else [])
  for kind,scriptroot,target in [('root',kit,alias/'fresh.zip'),('nested',kit,alias/'originals'/'fresh.zip'),('absent-parent',kit,alias/'absent-parent'/'fresh.zip'),('traversal',kit,alias/'originals'/'..'/'fresh.zip'),('reverse-root',alias,kit/'fresh.zip'),('reverse-absent-parent',alias,kit/'absent-parent'/'fresh.zip')]:
   require(not target.exists(),'Regression requires fresh absent leaf');argv=prefix+[str(scriptroot/'build_archive.py'),'--output',str(target)];r=subprocess.run(argv,capture_output=True,text=True,env=dict(os.environ,TMPDIR=str(base)),timeout=120)
   record={'optimized':optimized,'kind':kind,'argv':argv,'actual_script_root':str(scriptroot),'actual_output':str(target),'script_root_samefile_as_kit':scriptroot.samefile(kit),'case_output_root_samefile_as_kit':alias.samefile(kit),'script_root_device_inode':[scriptroot.stat().st_dev,scriptroot.stat().st_ino],'kit_device_inode':[kit.stat().st_dev,kit.stat().st_ino],'destination_initially_absent':True,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'destination_absent_after':not target.exists(),'absent_parent_not_created':not (kit/'absent-parent').exists(),'all_preexisting_kit_bytes_unchanged':pins(kit)==before}
   receipts.append(record);require(r.returncode!=0 and 'archive must be outside' in r.stderr and record['destination_absent_after'] and record['absent_parent_not_created'] and record['all_preexisting_kit_bytes_unchanged'],'Physical case writer regression failed '+kind)
  target=outsidealias/('fresh-optimized.zip' if optimized else 'fresh-normal.zip');argv=prefix+[str(kit/'build_archive.py'),'--output',str(target)];r=subprocess.run(argv,capture_output=True,text=True,env=dict(os.environ,TMPDIR=str(base)),timeout=120)
  positive={'optimized':optimized,'kind':'fresh-case-varied-external-positive','argv':argv,'external_parent_samefile':outsidealias.samefile(outside),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'byte_identical_to_current_zip':target.exists() and target.read_bytes()==(D/'verification_kit.zip').read_bytes(),'all_preexisting_kit_bytes_unchanged':pins(kit)==before};receipts.append(positive);require(r.returncode==0 and positive['byte_identical_to_current_zip'] and positive['all_preexisting_kit_bytes_unchanged'],'Positive physical outside writer failed');target.unlink()
output.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','actual_commands':len(receipts),'negative_physical_case_commands':12,'positive_case_varied_external_commands':2,'all_preexisting_kit_bytes_unchanged':True,'receipts':receipts},indent=2)+'\n')
print(json.dumps({'status':'PASS','actual_commands':len(receipts),'output':str(output)}))
