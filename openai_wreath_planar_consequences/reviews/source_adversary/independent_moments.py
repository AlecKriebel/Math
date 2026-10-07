"""Independent diagnostic only; composite Simpson arithmetic is not a proof.

Implements the mathematical definitions in family090 fourier.tex directly.
Does not import any supplied implementation or previous research check.
"""
from pathlib import Path
import cmath, math, json, hashlib, datetime

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'target_b/sources/openai_090'
BETA = math.sqrt(3)/2
H = 2/5
P = [5, complex(-1,2*BETA),complex(1,2*BETA),-2,
     complex(-.5,BETA), complex(-1,-2*BETA),1]
T = [j/6 for j in range(7)]
ROWS = [[int(x) for x in line.split()] for line in
        (SRC/'verification/data/coefficients.tsv').read_text().splitlines()]

def direct_qd(n):
    a = n % 12
    others = [v for v in (0,1,3,4,7,9) if v != a]
    q = (math.pi/6)**2
    for v in others:
        q *= (2*math.sin(math.pi*(a-v)/12))**2
    d = math.pi/6 * sum(1/math.tan(math.pi*(a-v)/12) for v in others)
    return q,d

def measure_density(t,j,entries):
    result = 0j
    for n,c,d in entries:
        phase = cmath.exp(-1j*math.pi*t*n)
        l0 = sum(P[k]*cmath.exp(1j*math.pi*T[k]*n) for k in range(j,7))
        l1 = sum((T[k]-t)*P[k]*cmath.exp(1j*math.pi*T[k]*n) for k in range(j,7))
        result += phase * (-2*math.pi**2*c*l1 + 2j*math.pi*d*l0)
    return result

def moments(entries,C,m,ell,panels):
    sums = [0j,0j]
    for j in range(1,7):
        start,end = T[j-1],T[j]
        dt = (end-start)/panels
        for k in range(panels+1):
            t = start+k*dt
            density = measure_density(t,j,entries)
            lam = 1j/(BETA*(t+1j*H))
            z = -(4/3)/(t+1j*H)-1j*H
            weight = 1 if k in (0,panels) else (4 if k%2 else 2)
            sums[0] += weight*dt/3*density*(1j*math.pi*t)**ell*cmath.exp(1j*math.pi*t*m)
            sums[1] += weight*dt/3*density*lam*(1j*math.pi*z)**ell*cmath.exp(1j*math.pi*z*m)
    for j,t in enumerate(T):
        mass = C*P[j]*(1 if j==0 else 2)
        lam = 1j/(BETA*(t+1j*H))
        z = -(4/3)/(t+1j*H)-1j*H
        sums[0] += mass*(1j*math.pi*t)**ell*cmath.exp(1j*math.pi*t*m)
        sums[1] += mass*lam*(1j*math.pi*z)**ell*cmath.exp(1j*math.pi*z*m)
    return [v.real for v in sums]

def lists():
    one = [(0,1,.44)] + [(n,c/1e10,d/1e10) for n,c,d,_,_ in ROWS]
    two = [(0,0,-.368)] + [(n,c/1e10,d/1e10) for n,_,_,c,d in ROWS]
    return one,two

def run(panels):
    entries = lists()
    constants = [-.013,.017]
    results = {}
    for m in [0,1,3,4]:
        for ell in range(3):
            values = [moments(entries[i],constants[i],m,ell,panels) for i in range(2)]
            results[f'H1_{ell}_at_{m}'] = values[0][0]+values[1][1]
            results[f'H2_{ell}_at_{m}'] = values[1][0]+values[0][1]
    results['poisson_origin_required'] = 6*direct_qd(1)[0]*math.exp(-math.pi*H)
    results['curvature_required_lower'] = 2*(1-math.pi*H)*direct_qd(1)[0]
    results['curvature_actual_difference'] = results['H1_2_at_1']-results['H2_2_at_1']
    return results

if __name__ == '__main__':
    values = {str(n):run(n) for n in [32,64,128]}
    result = {
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'method':'Independent stdlib composite Simpson of manuscript folded measures',
        'coverage':'Diagnostic moments only; no certified quadrature or global sign proof',
        'implementation_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'coefficients_sha256':hashlib.sha256((SRC/'verification/data/coefficients.tsv').read_bytes()).hexdigest(),
        'runs':values,
    }
    destination = Path(__file__).with_name('independent_moments_receipt.json')
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
