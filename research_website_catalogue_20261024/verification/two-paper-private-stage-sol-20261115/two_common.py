"""New two-target private-only constants and import-safe strict primitives."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,re
OWN=Path(__file__).resolve().parent
PROGRAMME=OWN.parents[1]
PUBLIC=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
IDS=('23385145','22983513')
SCIENCE={
'23385145':('root-clearance-23385145-20261115.json','7103359ae07eb8c6e6560c7c8626cd991cc0c69f222134e10bea642b50350331'),
'22983513':('root-clearance-22983513-20261115.json','048205b0aa267298ac034afa9fdf2c88973c05e68e6d0278e4accfcac2c0da57')}
EDITORIAL={
'23385145':('root-editorial-23385145-20261115.json','89d8f041c3dcd378080b800404910935c847405f00ca974d09c8805f720e3130'),
'22983513':('root-editorial-22983513-20261115.json','7f690a368ebcfee37c85d0eeffbfc70fe58d2eecd1e2acab17b4e174799d1499')}
def need(ok,label):
 if not ok:raise ValueError('two_stage:'+label)
def sha(data):return hashlib.sha256(data).hexdigest()
def bind(path):
 data=Path(path).read_bytes();return {'bytes':len(data),'sha256':sha(data)}
def strict_json(text):
 def pairs(rows):
  d={}
  for k,v in rows:need(k not in d,'duplicate_JSON_key:'+k);d[k]=v
  return d
 return json.loads(text,object_pairs_hook=pairs)
def load(path):return strict_json(Path(path).read_bytes())
def same(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def safe_name(name):
 need(type(name) is str and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*',name) is not None,'safe_native_basename');return name
def contained(root,path):
 root=Path(root).resolve();p=Path(path);p=p if p.is_absolute() else root/p
 need(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root),'contained_regular_input:'+str(path))
 need(all(not q.is_symlink() for q in p.parents if q.is_relative_to(root)),'no_input_symlink_parent');return p
def safe_output(path):
 p=Path(path).absolute();need(p.resolve().is_relative_to(OWN) and p.resolve()!=OWN,'new_private_folder_only')
 need(all(not q.is_symlink() for q in [p,*p.parents] if q.is_relative_to(OWN)),'no_private_output_symlink');return p
def root_authority(rid,table):
 name,wanted=table[rid];p=PROGRAMME/'verification'/name;need(bind(p)['sha256']==wanted,'exact_root_authority:'+rid+':'+name);return load(p)
