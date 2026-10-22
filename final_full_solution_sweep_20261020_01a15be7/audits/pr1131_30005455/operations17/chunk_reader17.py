"""Read the complete disjoint direct LZMA segment store."""
from pathlib import Path
from collections import OrderedDict
import json,gzip,lzma,hashlib,stat
ROOT=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
class Reader:
 def __init__(self):
  self.z=None;self.keys=set();self.map={};self.cache=OrderedDict();self.segments={}
  root=ROOT/'private/chunks17_segments';actual=set(root.iterdir());expected=set()
  for q in sorted(root.glob('*.index.json.gz')):
   need(not q.is_symlink(),'Segment index symlink');v=json.loads(gzip.decompress(q.read_bytes()));name=v['data_file']
   need(Path(name).name==name and name.endswith('.xz'),'Unsafe segment path');path=root/name;expected.update([q,path]);self.segments[name]=v
   offset=0
   for key,pin in v['chunks'].items():
    need(key not in self.keys and type(pin['offset'])is int and pin['offset']==offset and type(pin['bytes'])is int and 0<pin['bytes']<=16384,'Segment chunk order/identity')
    self.keys.add(key);self.map[key]=(name,pin);offset+=pin['bytes']
   need(offset==v['raw_bytes']and offset<=128*1024*1024,'Segment raw size/bounds')
  need(actual==expected,'Missing/unindexed segment files')
 def get(self,key):
  if key not in self.map:raise KeyError(key)
  name,pin=self.map[key]
  if name not in self.cache:
   v=self.segments[name];q=ROOT/'private/chunks17_segments'/name;need(not q.is_symlink(),'Segment data symlink');packed=q.read_bytes()
   need({'bytes':len(packed),'sha256':sha(packed)}==v['compressed_pin'],'Segment compressed bytes changed')
   b=lzma.decompress(packed,memlimit=256*1024*1024);need(len(b)==v['raw_bytes']and sha(b)==v['raw_sha256'],'Segment raw bytes changed')
   self.cache[name]=b
   while len(self.cache)>2:self.cache.popitem(last=False)
  b=self.cache[name];self.cache.move_to_end(name);return b[pin['offset']:pin['offset']+pin['bytes']]
 def close(self):self.cache.clear()
