import sys,json,time,subprocess
from pathlib import Path
from groups import *
from lattice_opt import load
BASE=Path(__file__).resolve().parents[1];DATA=BASE/'data'
examples={
 'C1':lambda:cyclic(1),'C6':lambda:cyclic(6),'Q8':quaternion,
 'Q8xC2':lambda:direct(quaternion(),cyclic(2)),
 'D8':lambda:dihedral(4),'S3':lambda:symmetric(3),'A4':lambda:alternating(4),
 'S4':lambda:symmetric(4),'A5':lambda:alternating(5),
 'UT4_2':lambda:unitriangular(4,2),
 'SL2_3':lambda:sl2(3),'SL2_5':lambda:sl2(5),
 'PSL2_7':lambda:sl2(7,True),'GL3_2':lambda:gl(3,2),
 'UT4_3':lambda:unitriangular(4,3),'S5':lambda:symmetric(5),
 'PSL2_11':lambda:sl2(11,True),'GL2_3':lambda:gl(2,3)
}
for name in sys.argv[1:]:
    print('START',name,flush=True);start=time.time()
    if not (DATA/f'{name}_table.txt').exists():save(name,examples[name](),DATA)
    if not (DATA/f'{name}_subgroups.json').exists():
        subprocess.run([str(BASE/'src/enumerate_subgroups'),str(DATA/f'{name}_table.txt'),str(DATA/f'{name}_subgroups.json')],check=True)
    L=load(name,DATA)
    out={'name':name,'order':L.n,'subgroups':len(L.subs),'normal_subgroups':len(L.normals),'meet_irreducibles':L.mi,'results':[]}
    for mode in ['arbitrary','normal','faithful']:
        r=L.optimize(mode,time_limit=90);out['results'].append(r)
        print(name,mode,r,flush=True)
        (DATA/f'{name}_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('TOTAL SECONDS',time.time()-start,flush=True)
