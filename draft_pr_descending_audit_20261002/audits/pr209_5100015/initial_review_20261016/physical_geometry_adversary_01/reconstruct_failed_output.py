"""Recover the complete deterministic first-run output, verifying original hash.

This uses the unchanged original Cartesian numerical routines and the retained
original exact failure/checker hash. It writes a lossless gzip only if its full
uncompressed bytes match the SHA-256 recorded before compaction.
"""
from pathlib import Path
import gzip
import hashlib
import json
import runpy

root=Path(__file__).resolve().parent
f=runpy.run_path(str(root/'cartesian_check.py'))
mp=f['mp'];mp.mp.dps=60
old=json.loads((root/'FAILED_PROBE_01.json').read_text())
out={k:old[k] for k in ['checker_sha256','dps','numerics_certified','construction','exact']}
out['cases']=[]
cases=[('odd3',2,1,3,1),('odd5',2,1,5,1),('even6',2,1,6,1),
       ('odd_star5_2',2,1,5,2),('even_star10_3',2,1,10,3),
       ('odd_star7_3',3,1,7,3),('even14',2,1,14,1),
       ('boundary4',2,1,4,1),('boundary8',2,1,8,1),('boundary8star',2,1,8,3),
       ('near_circle',mp.mpf('1.000001'),1,5,2),('thin',10,1,7,1),('largeN',2,1,50,1)]
phases=[mp.mpf('0'),mp.mpf('.173'),mp.mpf('.631'),mp.mpf('1.17')]
strval=f['strval']
for name,a,b,N,winding in cases:
    a,b=mp.mpf(a),mp.mpf(b)
    lam=f['closure_caustic'](a,b,N,winding)
    products=[];rows=[]
    for phase in phases:
        vertices,angle,errors,minstep=f['trace'](a,b,lam,phase,N)
        A,B,g=f['geometry'](a,b,vertices);products.append(A*B)
        reversed_product=mp.fprod(f['geometry'](a,b,list(reversed(vertices)))[:2])
        repeated_product=mp.fprod(f['geometry'](a,b,vertices*3)[:2])
        primitive_dist=min(mp.sqrt(f['dot'](f['add'](vertices[i],f['mul'](-1,vertices[0])),f['add'](vertices[i],f['mul'](-1,vertices[0])))) for i in range(1,N))
        rows.append({'phase':strval(phase),'A_outer':strval(A),'B_pedal':strval(B),'product':strval(A*B),
                     'orbit_residuals':{k:strval(v) for k,v in errors.items()},
                     'geometry_residuals':{k:strval(v) for k,v in g.items()},
                     'minimum_forward_step':strval(minstep),'min_primitive_vertex_separation':strval(primitive_dist),
                     'reversal_product_error':strval(abs(reversed_product-A*B)),
                     'triple_repetition_scaling_error':strval(abs(repeated_product-9*A*B))})
    variation=max(products)-min(products)
    out['cases'].append({'name':name,'a':strval(a),'b':strval(b),'N':N,'winding':winding,
                         'lambda':strval(lam),'relative_product_spread':strval(variation/max(abs(x) for x in products)),
                         'phases':rows})
raw=(json.dumps(out,indent=2)+'\n').encode()
sha=hashlib.sha256(raw).hexdigest()
assert sha==old['original_full_output_sha256'],(sha,old['original_full_output_sha256'])
compressed=gzip.compress(raw,mtime=0)
assert gzip.decompress(compressed)==raw
target=root/'FAILED_PROBE_01_COMPLETE.json.gz'
target.write_bytes(compressed)
assert hashlib.sha256(gzip.decompress(target.read_bytes())).hexdigest()==sha
receipt={'status':'EXACT_BYTE_RECOVERY_PASS','original_full_output_sha256':sha,'original_uncompressed_bytes':len(raw),
         'gzip_sha256':hashlib.sha256(compressed).hexdigest(),'gzip_bytes':len(compressed),'gzip_mtime':0,
         'reconstructed_full_output_matches_precompaction_hash':True,'roundtrip_verified':True}
(root/'FAILED_PROBE_RECOVERY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
