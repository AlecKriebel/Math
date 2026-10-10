#!/usr/bin/env python3
"""Adversarial filesystem controls, without modifying the original packet."""
import argparse, json, os, shutil, socket, tempfile
from pathlib import Path
import verify_publication as v

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--expected-manifest',required=True);args=ap.parse_args()
 count=v.integrity(v.ROOT,args.expected_manifest);results=[]
 cases=['changed','missing','extra_file','extra_directory','extra_nested_directory','dangling_symlink','file_symlink','directory_symlink','listed_file_symlink','fifo','socket','wrong_trusted_digest','manifest_tamper','zip_tamper']
 for name in cases:
  with tempfile.TemporaryDirectory(prefix='operadic-negative-') as td:
   root=Path(td)/'packet';shutil.copytree(v.ROOT,root);extra=root/'extra';digest=args.expected_manifest;s=None
   if name=='changed':(root/'README.md').write_bytes(b'changed')
   elif name=='missing':(root/'README.md').unlink()
   elif name=='extra_file':extra.write_bytes(b'extra')
   elif name=='extra_directory':extra.mkdir()
   elif name=='extra_nested_directory':(root/'audit/extra').mkdir()
   elif name=='dangling_symlink':extra.symlink_to('missing')
   elif name=='file_symlink':extra.symlink_to('README.md')
   elif name=='directory_symlink':extra.symlink_to('audit')
   elif name=='listed_file_symlink':(root/'README.md').unlink();(root/'README.md').symlink_to('audit/README.md')
   elif name=='fifo':os.mkfifo(extra)
   elif name=='socket':
    try:s=socket.socket(socket.AF_UNIX);s.bind(str(extra))
    except PermissionError:
     if s is not None:s.close()
     results.append({'case':name,'status':'NOT_RUN_ENVIRONMENT_DENIED'});continue
   elif name=='wrong_trusted_digest':digest='0'*64
   elif name=='manifest_tamper':(root/'PUBLICATION_MANIFEST.json').write_bytes(b'{}')
   elif name=='zip_tamper':(root/'OPERADIC_CENTER_30006031_AUTHOR_PACKET.zip').write_bytes(b'bad zip')
   rejected=False
   try:v.integrity(root,digest)
   except (ValueError,FileNotFoundError,RuntimeError):rejected=True
   finally:
    if s is not None:s.close()
   v.need(rejected,'negative control '+name);results.append({'case':name,'rejected':True})
 print(json.dumps({'status':'PASS','packet_files':count,'negative_controls':results,'author_bug_scope':'Covered separately by mandatory audit author-replay regression.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
