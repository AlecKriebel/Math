#!/usr/bin/env python3
"""Reject changed packet payloads using the retained original manifest anchor."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path

root=Path(__file__).resolve().parent
anchor=hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()
results=[]
for name in ['proof_payload','diagnostic_driver','result_payload','missing_file','extra_file','extra_directory','manifest_payload']:
    with tempfile.TemporaryDirectory(prefix='octa-packet-mutation-') as td:
        target=Path(td)/'packet';shutil.copytree(root,target)
        if name=='proof_payload':
            p=target/'MATHEMATICAL_NOTE.md';p.write_bytes(p.read_bytes()+b'\nChanged claim.\n')
        elif name=='diagnostic_driver':
            p=target/'check_exact.py';p.write_bytes(p.read_bytes().replace(b'Q(1,6)',b'Q(1,5)',1))
        elif name=='result_payload':
            p=target/'CHECK_RESULTS.json';p.write_bytes(p.read_bytes().replace(b'884',b'883',1))
        elif name=='missing_file':(target/'SOURCES.md').unlink()
        elif name=='extra_file':(target/'UNEXPECTED.txt').write_text('unexpected payload')
        elif name=='extra_directory':(target/'UNEXPECTED').mkdir()
        elif name=='manifest_payload':
            p=target/'MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
        for options in ([],['-O']):
            p=subprocess.run([sys.executable]+options+[str(target/'verify_packet.py'),'--manifest-sha256',anchor],capture_output=True)
            if p.returncode==0:raise RuntimeError('Mutation incorrectly accepted: '+name)
            results.append({'mutation':name,'optimized':bool(options),'rejected':True})
print(json.dumps({'result':'PASS_PACKET_MUTATION_CONTROLS','rejections':len(results),'tests':results},sort_keys=True,indent=2))
