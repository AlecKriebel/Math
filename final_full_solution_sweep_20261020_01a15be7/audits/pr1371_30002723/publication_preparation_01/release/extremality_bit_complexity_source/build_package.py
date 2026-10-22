"""Offline deterministic archives from this frozen scientific source; no service calls."""
import argparse,hashlib,json,stat,zipfile
from pathlib import Path
from reproduce import verify,need
P=Path(__file__).resolve().parent
STAMP=(2026,10,22,0,0,0)
def sha(b):return hashlib.sha256(b).hexdigest()
def archive(target,entries):
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,b in sorted(entries.items()):
   info=zipfile.ZipInfo(name,STAMP);info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b,compresslevel=9)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output).resolve();need(out!=P and P not in out.parents,'output must be outside source tree');out.mkdir(parents=True,exist_ok=True)
 m=json.loads((P/'PUBLIC_MANIFEST.json').read_text());data={str(p.relative_to(P)):p.read_bytes() for p in P.rglob('*') if p.is_file() and p!=P/'PUBLIC_MANIFEST.json'};verify(m['files'],data)
 data['PUBLIC_MANIFEST.json']=(P/'PUBLIC_MANIFEST.json').read_bytes();base='extremality-bit-complexity';pdf=out/(base+'.pdf');pdf.write_bytes((P/'paper.pdf').read_bytes());source=out/(base+'-source-and-verification.zip');archive(source,{'extremality_bit_complexity_source/'+n:b for n,b in data.items()})
 for name in ['zenodo-metadata.json','zenodo-deposit.json','UPLOAD_README.txt']:(out/name).write_bytes((P/name).read_bytes())
 names=[pdf.name,source.name,'zenodo-metadata.json','zenodo-deposit.json','UPLOAD_README.txt'];kit=out/(base+'-upload-kit.zip');archive(kit,{n:(out/n).read_bytes() for n in names})
 files=[out/n for n in names]+[kit]
 print(json.dumps({'status':'PASS','publication_performed':False,'network_used':False,'frozen_pdf_recompiled':False,'files':[{'name':f.name,'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files]},indent=2,sort_keys=True))
if __name__=='__main__':main()
