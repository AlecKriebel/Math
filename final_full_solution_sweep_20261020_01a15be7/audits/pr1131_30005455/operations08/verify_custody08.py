"""Read-only exact container + source artifact reconstruction, one member at a time."""
from pathlib import Path
import json,gzip,zipfile,hashlib,io,os,stat,datetime,tempfile,argparse
ROOT=Path(__file__).resolve().parent
ns={'__file__':str(ROOT/'compact_archives08.py'),'__name__':'custody_reader'}
exec(compile((ROOT/'compact_archives08.py').read_bytes(),str(ROOT/'compact_archives08.py'),'exec'),ns)
sha=ns['sha']
def need(x,m):
 if not x:raise RuntimeError(m)
def verify(scratch=None):
 if scratch is None:
  need(not (ROOT/'MANIFEST.json').exists(),'Sealed input requires an explicit outside scratch folder')
  scratch=ROOT/'private'
 else:
  scratch=Path(scratch).resolve();need(scratch!=ROOT and ROOT not in scratch.parents,'Review scratch must be outside sealed input')
 need(scratch.is_dir() and not scratch.is_symlink(),'Scratch directory must already exist')
 stats={'archives':0,'physical_files':0,'physical_bytes':0,'virtual_capture_paths':0,'virtual_unique_bodies_across_archives':set(),'exact_original_zip_reconstruction':True,'physical_mode_nsmtime_readback':True,'original_container_mode_nsmtime_readback':True,'retired_case_root_directory_metadata_captured':False}
 with zipfile.ZipFile(ROOT/'private/chunks08.zip') as source:
  for key in source.namelist():need(sha(source.read(key))==key,'Chunk bytes changed')
  with tempfile.TemporaryDirectory(prefix='reconstruct_',dir=scratch) as temp:
   output=Path(temp)/'single_member'
   for receipt in sorted((ROOT/'private').glob('case_archives*/*.custody.json.gz')):
    index=json.loads(gzip.decompress(receipt.read_bytes()));stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as reconstructed:
     reconstructed.comment=bytes.fromhex(index['comment'])
     for e in index['entries']:
      body=b''.join(source.read(k) for k in e['chunks']);need(len(body)==e['bytes'] and sha(body)==e['sha256'],'Container member changed')
      reconstructed.writestr(ns['zi'](e['zipinfo']),body,compresslevel=9)
    raw=stream.getvalue();need(len(raw)==index['original_bytes'] and sha(raw)==index['original_sha256'],'Exact original ZIP not reconstructible')
    output.write_bytes(raw);os.chmod(output,index['mode']);os.utime(output,ns=(index['mtime_ns'],index['mtime_ns']));metadata=output.stat()
    need(sha(output.read_bytes())==index['original_sha256'] and stat.S_IMODE(metadata.st_mode)==index['mode'] and metadata.st_mtime_ns==index['mtime_ns'],'Exact container physical metadata reconstruction failed');output.unlink()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
     v=json.loads(z.read('INDEX.json'));physical=v['files'];directories=v['directories'];virtual=v['virtual_paths']
     need(set(z.namelist())=={'INDEX.json'}|{'physical/'+n for n in physical}|{'virtual/'+k for k in set(virtual.values())},'Archive closure changed')
     for rel,pin in physical.items():
      need(not Path(rel).is_absolute() and '..' not in Path(rel).parts,'Unsafe physical path')
      parent=Path(rel).parent
      while parent.as_posix()!='.':need(parent.as_posix() in directories,'Parent directory missing');parent=parent.parent
      body=z.read('physical/'+rel);need(len(body)==pin['bytes'] and sha(body)==pin['sha256'],'Physical bytes changed')
      output.write_bytes(body);os.chmod(output,pin['mode']);os.utime(output,ns=(pin['mtime_ns'],pin['mtime_ns']));s=output.stat()
      need(sha(output.read_bytes())==pin['sha256'] and stat.S_IMODE(s.st_mode)==pin['mode'] and s.st_mtime_ns==pin['mtime_ns'],'Physical reconstruction mismatch')
      output.unlink();stats['physical_files']+=1;stats['physical_bytes']+=len(body)
     for k,size in v['virtual_bytes'].items():body=z.read('virtual/'+k);need(sha(body)==k and len(body)==size,'Virtual exact bytes changed');stats['virtual_unique_bodies_across_archives'].add(k)
     stats['virtual_capture_paths']+=len(virtual)
    stats['archives']+=1
 stats['virtual_unique_bodies_across_archives']=len(stats['virtual_unique_bodies_across_archives']);stats['at']=datetime.datetime.now(datetime.timezone.utc).isoformat();stats['verifier_sha256']=sha(Path(__file__).read_bytes());stats['temporary_storage_outside_sealed_input']=scratch!=ROOT/'private';return stats
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--scratch');args=parser.parse_args();print(json.dumps(verify(args.scratch),indent=2))
