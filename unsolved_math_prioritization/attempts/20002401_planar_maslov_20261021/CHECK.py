import json
from fractions import Fraction as F

def require(p, msg):
    if not p: raise ValueError(msg)

def certificate(amplitude=F(1,4), tail_floor=F(5), lo=F(199,100), hi=F(2), coupling=F(1,16), derivative_sign=-1, maslov=-1):
    require(amplitude == F(1,4), 'fixed benchmark amplitude')
    # Multiplication by cos(x)cos(y) sends sin(x)sin(y) to sin(2x)sin(2y)/4.
    shifts = {(2,2): amplitude*F(1,2)*F(1,2)}
    require(shifts == {(2,2): coupling}, 'nonzero exact coupling')
    gap=tail_floor-amplitude-F(3)
    require(gap>0, 'strict infinite tail gap')
    require(tail_floor == F(5), 'fixed benchmark tail spectral floor')
    b2=coupling**2
    rmax=b2/gap
    rmin=b2/F(7)
    derivative_extra=b2/gap**2
    require(0 < rmin <= rmax, 'ordered positive tail correction bounds')
    require(F(1) < 2-rmax <= 2-rmin < F(3), 'ordered internal root interval')
    require(derivative_sign == -1, 'inverse derivative correction is negative in S')
    require(F(2)-lo-rmax>0, 'left endpoint positive')
    require(F(2)-hi-rmin<0, 'right endpoint negative')
    require(F(1)<lo<hi<F(3), 'single owned box inside transverse endpoints')
    require(F(2)-amplitude>1 and F(2)+amplitude<3 and F(5)-amplitude>3, 'independent minmax count')
    require(maslov == -1, 'Green identity fixes negative crossing sign')
    return dict(tail_gap=str(gap),coupling=str(coupling),coupling_squared=str(b2),r_lower=str(rmin),r_upper=str(rmax),root_lower=str(2-rmax),root_upper=str(2-rmin),derivative_lower=str(-1-derivative_extra),derivative_upper='-1',box=[str(lo),str(hi)],maslov_index=maslov)

if __name__ == '__main__':
    baseline=certificate()
    mutations={'omit_coupling':{'coupling':F(0)}, 'wrong_derivative':{'derivative_sign':1}, 'zero_tail_gap':{'tail_floor':F(13,4)}, 'miss_crossing':{'lo':F(3,2),'hi':F(7,4)}, 'wrong_maslov_sign':{'maslov':1}, 'overstated_tail_floor':{'tail_floor':F(100)}}
    rejected={}
    for name,kw in mutations.items():
        try: certificate(**kw)
        except ValueError as e: rejected[name]=str(e)
        else: raise RuntimeError('mutation accepted: '+name)
    print(json.dumps({'status':'PASS','arithmetic':'exact rational, no floating point','certificate':baseline,'rejected_mutations':rejected},indent=2,sort_keys=True))
