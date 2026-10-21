"""A small selected replay of physical controls, deliberately avoiding the old full sweep."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys, time

HERE = Path(__file__).resolve().parent
MATERIALS = HERE.parent / 'publication_package_v1/materials'
DEP = HERE.parent.parent / 'pr200_5100007/math_algebra_family_01/runtime_packages'
sys.path.insert(0, str(DEP))
spec = importlib.util.spec_from_file_location('portable_physical', MATERIALS/'verification/physical_phase_checks.py')
physical = importlib.util.module_from_spec(spec)
spec.loader.exec_module(physical)
mp = physical.mp

def need(c, message):
    if not c:
        raise RuntimeError(message)

def main():
    started = time.monotonic()
    records = []
    # Convex base case, star with sign change, nearly circular boundary,
    # a high-winding eccentric case, and the listed-length countercontrol.
    for a, N, winding, target in [('2',6,1,True), ('2',10,3,True),
                                  ('1.0001',14,5,True), ('5',22,9,True),
                                  ('2',6,2,False)]:
        record, (aa, bb, lam) = physical.case(a,N,winding,target)
        P, _, _ = physical.orbit(aa,bb,lam,N,mp.mpf('.173'))
        A = physical.shoelace(P)
        Ap, B0, _, _ = physical.derived(P,aa,bb,(0,0))
        need(A > 0 and Ap > 0, 'oriented original/outer positivity failed')
        for M in [(mp.mpf('.37'),mp.mpf('-.81')),(mp.mpf(17),mp.mpf(-23))]:
            ap, bm, _, _ = physical.derived(P,aa,bb,M)
            rap, rbm, _, _ = physical.derived(list(reversed(P)),aa,bb,M)
            need(abs(ap+rap)<mp.mpf('1e-65') and abs(bm+rbm)<mp.mpf('1e-65'), 'signed reversal failed')
        record['phase_173_original_A'] = physical.textnum(A)
        record['phase_173_A_Aprime'] = physical.textnum(A*Ap)
        if not target:
            need(max(map(mp.mpf,record['relative_phase_spread_by_M']))>mp.mpf('1e-10'), 'repeated-odd falsifier did not falsify')
        if N == 10:
            _, B1, _, _ = physical.derived(P,aa,bb,(1,0))
            quadratic = B1-B0
            need(B0>0 and quadratic<0,'star zero crossing premise failed')
            radius=mp.sqrt(-B0/quadratic)
            controls=[]
            for phase in map(mp.mpf,('.173','.719','1.37')):
                points, _, _ = physical.orbit(aa,bb,lam,N,phase)
                values=[physical.derived(points,aa,bb,(radius*f,0))[1] for f in map(mp.mpf,('.99','1','1.01'))]
                need(values[0]>0 and abs(values[1])<mp.mpf('1e-45') and values[2]<0,'star zero/negative boundary failed')
                controls.append({'phase':str(phase),'pedal_below_zero_above':list(map(physical.textnum,values))})
            record['zero_pedal_boundary']={'radius':physical.textnum(radius),'samples':controls}
        records.append(record)
    report={'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','optimization':sys.flags.optimize,
            'precision_digits':mp.mp.dps,'elapsed_seconds':round(time.monotonic()-started,3),
            'scope':'Four target physical cases and one excluded repeated-odd case; finite noninterval diagnostics, not all periods or a proof.',
            'records':records}
    (HERE/'SELECTED_PHYSICAL_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','target_cases':4,'excluded_repeated_odd_cases':1,'star_zero_negative_boundary':True,'elapsed_seconds':report['elapsed_seconds']},indent=2))

if __name__=='__main__':
    main()
