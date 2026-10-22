"""Independent bounded certificate checks: system patch and Fraction-only arithmetic.
This does not import any candidate checking implementation or claim a full proof.
"""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
from datetime import datetime, timezone
import argparse, hashlib, json, subprocess

p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True)
a=p.parse_args();source=a.source.resolve();out=Path(__file__).resolve().parent
scratch=out/'private_tmp'/'independent_certificates';scratch.mkdir(parents=True,exist_ok=True)
history=json.loads((source/'EDITION_HISTORY.json').read_text())
versions={'PROOF_CANDIDATE_v4.md':(source/'PROOF.md').read_bytes()}
patches=[('PROOF_CANDIDATE_v4.md','PROOF_CANDIDATE_v2.md','CITATION_CORRECTION.patch'),
         ('PROOF_CANDIDATE_v2.md','PROOF_CANDIDATE.md','NUMERICAL_CORRECTION_v1_to_v2.patch'),
         ('PROOF_CANDIDATE_v4.md','PROOF_CANDIDATE_v3.md','POLYSTABILITY_CITATION_v3_to_v4.patch')]
patch_runs=[]
for direction in ['reverse','forward']:
    for newer,older,patch in patches:
        fr,to=(newer,older) if direction=='reverse' else (older,newer)
        src=scratch/('input_'+str(len(patch_runs)));dest=scratch/('output_'+str(len(patch_runs)))
        src.write_bytes(versions[fr])
        cmd=['/usr/bin/patch','-s','-f','-F','0']+(['-R'] if direction=='reverse' else [])+['-o',str(dest),str(src),str(source/'corrections'/patch)]
        r=subprocess.run(cmd,cwd=scratch,capture_output=True,text=True,timeout=30)
        data=dest.read_bytes() if dest.exists() else b''
        expected=next(e for e in history['editions'] if e['file']==to)
        actual=hashlib.sha256(data).hexdigest()
        good=r.returncode==0 and len(data)==expected['bytes'] and actual==expected['sha256']
        patch_runs.append({'direction':direction,'patch':patch,'from':fr,'to':to,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr.replace(str(scratch),'<PRIVATE_TMP>'),'bytes':len(data),'sha256':actual,'matches_recorded_hash_and_size':good})
        if not good:raise RuntimeError('Independent system patch failed: '+json.dumps(patch_runs[-1]))
        versions[to]=data

# Integrate polynomial pieces directly in rational arithmetic.
A=[(-1,0,[4,4,1]),(0,2,[4,-4,1])];B=[(-1,1,[2,1])]
def integral_poly(pieces,k,sign=1):
    return sum((F(sign*c, k+d+1)*(F(u)**(k+d+1)-F(l)**(k+d+1))
                for l,u,cs in pieces for d,c in enumerate(cs)),F(0))
def abs_first_moment(pieces):
    parts=[]
    for l,u,cs in pieces:
        if l<0:parts.append(integral_poly([(l,min(u,0),cs)],1,-1))
        if u>0:parts.append(integral_poly([(max(l,0),u,cs)],1))
    return sum(parts,F(0))

certificate=json.loads((source/'audits/reviewer_b/INDEPENDENT_CHECK_RESULTS.json').read_text())
numerical=[]
for name,pieces,radius,want_mass,want_first,want_l1 in [('a',A,2,F(5),F(5,12),F(9,4)),('b',B,1,F(4),F(2,3),F(2))]:
    mass=integral_poly(pieces,0);first=integral_poly(pieces,1);l1=abs_first_moment(pieces)
    if (mass,first,l1)!=(want_mass,want_first,want_l1):raise RuntimeError('Independent integral mismatch')
    c=certificate['positive_root_brackets'][name]
    for side in ['left','right']:
        t=F(c['lo' if side=='left' else 'hi']);N=32
        if not 0<t*radius<1:raise RuntimeError('Taylor radius hypothesis failed')
        center=sum(((-t)**k/F(factorial(k))*integral_poly(pieces,k+1) for k in range(N+1)),F(0))
        err=3*l1*(t*radius)**(N+1)/factorial(N+1)
        bounds=[center-err,center+err]
        recorded=[F(x) for x in c[side+'_moment_bounds']]
        match=bounds==recorded
        sign_ok=bounds[0]>0 if side=='left' else bounds[1]<0
        if not match or not sign_ok:raise RuntimeError('Fraction certificate mismatch')
        numerical.append({'density':name,'side':side,'degree':N,'mass':str(mass),'first_moment':str(first),'exact_L1':str(l1),'t':str(t),'radius_condition':True,'exact_fractions_match_frozen_certificate':match,'required_strict_sign':sign_ok,'bound_width':str(bounds[1]-bounds[0]),'floating_point_used':False})

# Elementary exact proof of exp(1)<3 used by the rational Taylor remainder:
# for k>=2, k!>=2^(k-1), strict for k>=3, so sum_{k>=2}1/k!<1.
result={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'system_patch_version':subprocess.run(['/usr/bin/patch','--version'],capture_output=True,text=True,check=True).stdout.strip(),'system_patch_runs':patch_runs,'fraction_only_endpoint_checks':numerical,'exp_one_bound':'For k>=2, k!>=2^(k-1), strict for k>=3. Thus exp(1)=2+sum_{k>=2}1/k!<2+sum_{k>=2}2^(-(k-1))=3.','scope':'Four finite exact endpoint certificates and six exact zero-fuzz edition transforms. No all-ratios, geometry, global minimization, or novelty inference.'}
(out/'INDEPENDENT_CERTIFICATE_RECEIPTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'system_patch_successes':sum(e['matches_recorded_hash_and_size'] for e in patch_runs),'fraction_endpoint_successes':len(numerical),'floating_point_used':False},indent=2))
