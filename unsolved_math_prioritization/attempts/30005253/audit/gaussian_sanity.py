#!/usr/bin/env python3
"""Optional direct Gaussian matrix checks. Requires NumPy; not a proof.
Run with OPENBLAS_NUM_THREADS=1 for stable low-overhead execution.
"""
import argparse
import json
from pathlib import Path
import numpy as np

def run():
    rng=np.random.default_rng(30005253)
    rows=[]
    maximum_identity_error=0.0
    for m,repetitions in ((8,800),(32,600),(128,400)):
        p=2*m; beta=np.zeros(p); beta[0]=2.0; t=2/3
        risks=[]; projections=[]; noises=[]; crosses=[]
        for _ in range(repetitions):
            X=rng.standard_normal((m,p)); eps=rng.standard_normal(m)
            W=X@X.T
            projected=X.T@np.linalg.solve(W,X@beta)
            eta=X.T@np.linalg.solve(W,eps)
            fitted=projected+eta
            risk=1+np.dot(t*fitted-beta,t*fitted-beta)
            A=np.dot(projected,projected); B=np.dot(eta,eta); C=np.dot(beta,eta)
            identity=1+np.dot(beta-projected,beta-projected)+(t-1)**2*A+t*t*B+2*t*(t-1)*C
            maximum_identity_error=max(maximum_identity_error,abs(risk-identity))
            assert abs(risk-identity)<1e-9
            risks.append(risk); projections.append(A); noises.append(B); crosses.append(C)
        rows.append({'m':m,'p':p,'repetitions':repetitions,
                     'risk_mean':float(np.mean(risks)),
                     'risk_mean_exact':11/3+4/(9*(m-1)),
                     'risk_std':float(np.std(risks,ddof=1)),
                     'risk_quantiles_05_50_95':np.quantile(risks,[.05,.5,.95]).tolist(),
                     'projection_mean':float(np.mean(projections)),
                     'projection_variance':float(np.var(projections,ddof=1)),
                     'projection_variance_exact':4/(m+1),
                     'noise_mean':float(np.mean(noises)),
                     'noise_mean_exact':m/(m-1),
                     'cross_second_moment':float(np.mean(np.square(crosses))),
                     'cross_second_moment_exact':2/(m-1)})
    return {'passed_deterministic_identities':True,'seed':30005253,'numpy':np.__version__,
            'monte_carlo_is_not_a_proof':True,'maximum_identity_error':maximum_identity_error,'rows':rows}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('gaussian_sanity.replay.json'))
    args=parser.parse_args()
    result=run()
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))
