#!/usr/bin/env python3
"""Attempted one-color extension; exact original and failed-extension certificates."""
import json
from rooted_verify import verify

def main():
    src=json.load(open('witness_c112_m43.json'));md=src['model'];n=md['n'];mat=[[0]*n for _ in range(n)]
    for i,j,col in md['edges']:mat[i][j]=mat[j][i]=col
    original={'c':112,'m':43,'spokes':md['spokes'],'edges':mat}
    r=verify(original,True);assert r['is_counterexample'];assert '42' in r['spectrum_witnesses']
    newmat=[row+[0] for row in mat]+[[0]*(n+1)]
    extended={'c':113,'m':43,'spokes':md['spokes']+[112],'edges':newmat}
    s=verify(extended,True);assert not s['is_counterexample'];assert s['observed_spectrum']==sorted(set(r['observed_spectrum'])|{x+1 for x in r['observed_spectrum']})
    out={'original':{'c':112,'m':43,'verified_avoids':True,'subsets_checked':r['subsets_checked'],'input_sha256':r['input_sha256'],'42_color_witness':r['spectrum_witnesses']['42']},'extension':{'c':113,'m':43,'verified_avoids':False,'subsets_checked':s['subsets_checked'],'input_sha256':s['input_sha256'],'43_color_witness':s['spectrum_witnesses']['43']}}
    open('rooted_c112_m43.json','w').write(json.dumps(original,indent=2)+'\n');open('failed_extension_c113_m43.json','w').write(json.dumps(extended,indent=2)+'\n')
    open('extension_failure_checks.json','w').write(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
