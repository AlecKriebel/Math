"""Execute a renderer completely; capture writes in memory to conserve disk."""
from pathlib import Path
import contextlib,hashlib,io,json,sys
import pypdf
O=Path(__file__).resolve().parent;R=O.parents[1];LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
source=Path(sys.argv[1]);rid=sys.argv[2];V=O/'memory-render';files={};inputs={}
rb,rt,wb,wt,mkdir=Path.read_bytes,Path.read_text,Path.write_bytes,Path.write_text,Path.mkdir
def digest(b):return hashlib.sha256(b).hexdigest()
def original(p):
 b=rb(p);inputs[str(p.resolve())]={'bytes':len(b),'sha256':digest(b)};return b
for rel in ['research/index.html','research/sitemap.xml','research/research.css','robots.txt']:files[str(V/rel)]=original(LIVE/rel)
def read_bytes(p):return files[str(p)] if str(p) in files else original(p)
def read_text(p,*a,**kw):return read_bytes(p).decode(kw.get('encoding') or (a[0] if a else None) or 'utf-8')
def write_bytes(p,b):
 assert p.is_relative_to(V),p;files[str(p)]=b;return len(b)
def write_text(p,t,*a,**kw):return write_bytes(p,t.encode(kw.get('encoding') or (a[0] if a else None) or 'utf-8'))
def private_mkdir(p,*a,**kw):
 assert p.is_relative_to(V),p
real_reader=pypdf.PdfReader
def reader(p,*a,**kw):return real_reader(io.BytesIO(files[str(p)]),*a,**kw)
code=rt(source).replace('ROOT = Path(__file__).resolve().parents[1]','ROOT = Path('+repr(str(R))+')').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",'SITE = Path('+repr(str(V/'research'))+')')
Path.read_bytes=read_bytes;Path.read_text=read_text;Path.write_bytes=write_bytes;Path.write_text=write_text;Path.mkdir=private_mkdir;pypdf.PdfReader=reader
sys.argv=[str(source),rid]
with contextlib.redirect_stdout(io.StringIO()) as receipt:exec(compile(code,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
outputs={str(Path(path).relative_to(V)):{'bytes':len(b),'sha256':digest(b)} for path,b in sorted(files.items())}
print(json.dumps({'record_id':rid,'outputs':outputs,'original_read_bindings':inputs,'renderer_receipt':json.loads(receipt.getvalue()),'filesystem_output_writes':0}))
