"""Normal/-O explicit-exception self-test plus exact-caustic reverse billiards."""
from pathlib import Path
import sys,subprocess,json
root=Path(__file__).resolve().parent
setup="import runpy;g=runpy.run_path("+repr(str(root/"independent_geometry.py"))+")\n"
body=r'''
mp=g['mp']
for A,B,L,N,expected in [(8,3,mp.mpf(24)/35,8,mp.mpf(3200)/3),(9,4,mp.mpf(36)/13,4,mp.mpf(144))]:
    a,b=mp.sqrt(A),mp.sqrt(B)
    for phase in g['PHASES']:
        forward,_=g['orbit'](a,b,L,phase,N,True)
        outer=g['intersections'](forward,a,b)
        reference=g['focal_logproduct'](outer,a,b,1)
        g['residual']('exact_caustic_product',reference-mp.log(expected))
        p=forward[0]
        ccw=g['initial_direction'](p,a,b,L)
        reflected=g['reflected'](ccw,p,a,b)
        d=(-reflected[0],-reflected[1])
        points=[p]
        for j in range(N):
            q=g['second_hit'](p,d,a,b)
            points.append(q)
            d=g['reflected'](d,q,a,b)
            p=q
        g['residual']('reverse_closure',g['norm'](g['sub'](points[-1],points[0]))/a)
        rout=g['intersections'](points,a,b)
        for focus in [-1,1]:
            g['residual']('reverse_both_foci_product',g['focal_logproduct'](rout,a,b,focus)-reference)
print('PASS explicit-exception geometry, both foci, axes/generic phases, forward/reverse')
'''
results={}
for mode,flags in [("normal",[]),("optimized",["-O"])]:
    good=subprocess.run([sys.executable,"-E","-B","-P"]+flags+["-c",setup+body],capture_output=True,text=True)
    bad=subprocess.run([sys.executable,"-E","-B","-P"]+flags+["-c",setup+"g['check']('DELIBERATE FALSE GUARD',False)"],capture_output=True,text=True)
    (root/("independent_guard_"+mode+"_stdout.txt")).write_text(good.stdout)
    (root/("independent_guard_"+mode+"_stderr.txt")).write_text(good.stderr)
    (root/("independent_guard_false_"+mode+"_stderr.txt")).write_text(bad.stderr)
    if good.returncode!=0 or bad.returncode==0:
        raise RuntimeError("independent guard test failed "+mode+": "+good.stderr)
    results[mode]={"geometric_replay_returncode":good.returncode,"deliberate_false_check_returncode":bad.returncode}
(root/"independent_guard_replay.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
