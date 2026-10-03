import json
from hessian_certificate import compute
checks=0
def check(x):
 global checks
 assert x;checks+=1
certificate=compute(check);certificate['assertions']=checks
expected=json.load(open('TURN_4_CERTIFICATE.json'));assert json.loads(json.dumps(certificate))==expected
print(json.dumps(dict(assertions=checks+1,exact_hessian_dimension=128,gauge_kernel_dimension=63,physical_positive_dimension=65,fourier_modes=64,coefficient_field='Q(sqrt2,sqrt3), with integer-certified radical intervals',scope='Exact computer-assisted strict local minimum modulo gauge on8x8 only; global and arbitrary-size optimality remain unresolved.'),indent=2,sort_keys=True))
