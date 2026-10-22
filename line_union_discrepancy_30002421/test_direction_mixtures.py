"""Exploratory floating-point diagnostics, not mathematical certificates.

An exactly evaluated maximum over admissible sampled cubes would be a lower
bound on the true supremum. These floating-point values are not certified lower
or upper bounds. This script does not certify cube containment, event ordering,
clipping, or numerical roundoff. It supplies no numerical counterexample.

Requires Python 3.12 and NumPy 2.3.5 for the recorded replay environment.
Writes DIRECTION_MIXTURE_EXPERIMENT.json beside this script, independently of cwd.
"""
import numpy as np, json, math
from pathlib import Path
rng=np.random.default_rng(182530002421)
base=np.array([math.sqrt(2),math.sqrt(3),1.])
dirs=[base,np.roll(base,1),np.roll(base,2)]

def full_chords(alpha,n):
    events=np.concatenate(([0.,float(n)],*[np.arange(1,math.ceil(n*a))/a for a in alpha]))
    events=np.unique(events[(events>=0)&(events<=n)]);events.sort()
    left,right=events[:-1],events[1:]
    cells=np.floor(((left+right)/2)[:,None]*alpha)
    starts=left[:,None]*alpha-cells
    lengths=(right-left)*np.linalg.norm(alpha)
    return starts,lengths,alpha/np.linalg.norm(alpha)

def frame(u):
    z=u/np.linalg.norm(u); e=np.array([0.,0.,1.])
    if abs(z@e)>.9:e=np.array([0.,1.,0.])
    x=np.cross(e,z);x/=np.linalg.norm(x);y=np.cross(z,x)
    return np.column_stack([x,y,z])

frames=[np.eye(3)]+[frame(a) for a in dirs]
for _ in range(24):
    q,_=np.linalg.qr(rng.normal(size=(3,3)))
    if np.linalg.det(q)<0:q[:,0]*=-1
    frames.append(q)

cubes=[]
for fi,U in enumerate(frames):
    smax=min(1/np.abs(U).sum(axis=1))
    for j in range(180 if fi<4 else 50):
        s=rng.uniform(.08,.98)*smax
        half=s/2*np.abs(U).sum(axis=1)
        center=rng.uniform(half,1-half)
        cubes.append((fi,U,center,s))

def cube_length(chord,U,c,s):
    p,lengths,v=chord
    y=(p-c)@U; d=v@U
    lo=np.zeros(len(p));hi=lengths.copy()
    for j in range(3):
        if abs(d[j])<1e-12:
            hi[np.abs(y[:,j])>s/2]=0
        else:
            t0=(-s/2-y[:,j])/d[j];t1=(s/2-y[:,j])/d[j]
            lo=np.maximum(lo,np.minimum(t0,t1));hi=np.minimum(hi,np.maximum(t0,t1))
    return np.maximum(hi-lo,0).sum()

results=[]
for n in [8,16,32,64,128,256]:
    chords=[full_chords(a,n) for a in dirs]
    max_single=(0,None);max_mix=(0,None)
    L1=n*math.sqrt(6);L3=3*L1
    # Length and clipping checks: discrepancies are diagnostic, not exact proofs.
    lengths=[float(ch[1].sum()) for ch in chords]
    max_piece=max(float(ch[1].max()) for ch in chords)
    for qi,(fi,U,c,s) in enumerate(cubes):
        ql=np.array([cube_length(ch,U,c,s) for ch in chords])
        e1=abs(ql[0]/L1-s**3);e3=abs(ql.sum()/L3-s**3)
        if e1>max_single[0]:max_single=(e1,qi)
        if e3>max_mix[0]:max_mix=(e3,qi)
    row={'n':n,'chord_counts':[len(ch[1]) for ch in chords], 'length_sums':lengths,'max_piece':max_piece,'cube_samples':len(cubes)}
    for label,(err,qi),L in [('single',max_single,L1),('three_direction',max_mix,L3)]:
        fi,U,c,s=cubes[qi]
        row[label]={'sample_max_discrepancy':float(err),'L':L,'L_times_sample_max':float(L*err),'ratio_to_logL_overL':float(L*err/math.log(L)),'frame_id':fi,'center':c.tolist(),'side':float(s),'frame':U.tolist()}
    results.append(row)
    print(n,row['single']['L_times_sample_max'],row['three_direction']['L_times_sample_max'],flush=True)
Path(__file__).resolve().with_name('DIRECTION_MIXTURE_EXPERIMENT.json').write_text(json.dumps({'seed':182530002421,'warning':'Exploratory floating-point diagnostics only. These values are not certified lower or upper bounds and are not a numerical counterexample.','results':results},indent=2)+'\n')
