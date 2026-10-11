import hashlib,json,lzma,os,pathlib,sys,datetime
R=pathlib.Path(__file__).resolve().parent;p=R/'private_sources/cen2024.pdf'
b=p.read_bytes();c=lzma.compress(b,preset=6)
record={'actual_pid':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_path':str(p),'original_bytes':len(b),'original_sha256':hashlib.sha256(b).hexdigest(),'compressed_bytes':len(c),'decompression_verified':lzma.decompress(c)==b,'format':'XZ byte-lossless complete primary PDF'}
assert record['decompression_verified']
other=sum(q.stat().st_size for q in R.rglob('*') if q.is_file() and q!=p)
if other+len(c)<34*1024*1024:
 q=p.with_suffix('.pdf.xz');q.write_bytes(c);assert hashlib.sha256(lzma.decompress(q.read_bytes())).hexdigest()==record['original_sha256'];record['compressed_path']=str(q);record['compressed_sha256']=hashlib.sha256(c).hexdigest();p.unlink();record['action']='original complete PDF replaced by byte-lossless XZ with complete decoded body pin'
else:record['action']='no disk mutation to source; XZ not small enough'
(R/'CEN_SOURCE_COMPACTION.json').write_text(json.dumps(record,indent=2)+'\n'); print(json.dumps(record))
