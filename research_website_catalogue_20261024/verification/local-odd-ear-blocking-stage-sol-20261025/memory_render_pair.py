"""Two complete renderer executions, comparing their actual in-memory bytes.

Only hashes/counts are emitted. No old output tree, asset copy, or fixture is
written; each side starts from the same actual current public input bytes.
"""
from pathlib import Path
import contextlib,hashlib,io,json,sys
import pypdf
O=Path(__file__).resolve().parent;P=O.parents[1]
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public');V=O/'memory-render-not-created'
rid=sys.argv[1]
rb,rt,wb,wt,mkdir=Path.read_bytes,Path.read_text,Path.write_bytes,Path.write_text,Path.mkdir
real_reader=pypdf.PdfReader
def digest(b):return hashlib.sha256(b).hexdigest()
def execute(source):
 files={};inputs={}
 def original(p):
  b=rb(p);inputs[str(p.resolve())]={'bytes':len(b),'sha256':digest(b)};return b
 for rel in ['research/index.html','research/sitemap.xml','research/research.css','robots.txt']:files[str(V/rel)]=original(LIVE/rel)
 def read_bytes(p):return files[str(p)] if str(p) in files else original(p)
 def read_text(p,*a,**k):return read_bytes(p).decode(k.get('encoding') or (a[0] if a else None) or 'utf-8')
 def write_bytes(p,b):
  if not p.is_relative_to(V):raise RuntimeError('memory write outside virtual output:'+str(p))
  files[str(p)]=b;return len(b)
 def write_text(p,t,*a,**k):return write_bytes(p,t.encode(k.get('encoding') or (a[0] if a else None) or 'utf-8'))
 def private_mkdir(p,*a,**k):
  if not p.is_relative_to(V):raise RuntimeError('memory mkdir outside virtual output')
 def reader(p,*a,**k):return real_reader(io.BytesIO(files[str(p)]),*a,**k)
 code=rt(source)
 root='ROOT = Path(__file__).resolve().parents[1]';site="SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')"
 if code.count(root)!=1 or code.count(site)!=1:raise RuntimeError('unexpected renderer root declarations')
 code=code.replace(root,'ROOT = Path('+repr(str(P))+')').replace(site,'SITE = Path('+repr(str(V/'research'))+')')
 try:
  Path.read_bytes=read_bytes;Path.read_text=read_text;Path.write_bytes=write_bytes;Path.write_text=write_text;Path.mkdir=private_mkdir;pypdf.PdfReader=reader
  sys.argv=[str(source),rid]
  with contextlib.redirect_stdout(io.StringIO()) as receipt:exec(compile(code,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
  return files,inputs,json.loads(receipt.getvalue())
 finally:
  Path.read_bytes=rb;Path.read_text=rt;Path.write_bytes=wb;Path.write_text=wt;Path.mkdir=mkdir;pypdf.PdfReader=real_reader
a,ai,ar=execute(O/'inputs/render_page.py');b,bi,br=execute(O/'render_page.proposed.py')
equal=a==b;input_equal=ai==bi;receipt_equal=ar==br
result={'record_id':rid,'current_and_proposed_actual_output_bytes_equal':equal,'original_reads_equal':input_equal,'renderer_receipts_equal':receipt_equal,'complete_renderer_executions':2,'filesystem_output_writes':0,'outputs':{str(Path(k).relative_to(V)):{'bytes':len(v),'sha256':digest(v)} for k,v in sorted(a.items())},'original_read_bindings':ai,'current_renderer_receipt':ar,'proposed_renderer_receipt':br}
print(json.dumps(result));sys.exit(0 if equal and input_equal and receipt_equal and not V.exists() else 1)
