from fractions import Fraction
import json
cases = []
for a, b, c, d in [(1, 0, 0, 1), (1, 1, 1, 2), (0, 1, -1, 3), (0, -1, 1, 3), (0, -1, 1, 0)]:
    if not a * d - b * c == 1:
        raise AssertionError('exact check failed')
    P = d * d - 2 * c * c
    case = {'gamma': [[a, b], [c, d]], 'P': P, 'included_positive_orientation': P > 0}
    if P > 0:
        mu = (b * d - 2 * a * c) % P
        if not (mu * mu - 2) % P == 0:
            raise AssertionError('exact check failed')
        case.update(m=P, mu=mu, x_mod_1=str(Fraction(mu, P)))
    cases.append(case)
if not [(x['m'], x['mu']) for x in cases if x['included_positive_orientation']] == [(1, 0), (2, 0), (7, 3), (7, 4)]:
    raise AssertionError('exact check failed')
with open('endpoint_decoder_results.json', 'w') as f:
    json.dump(cases, f, indent=2)
print(json.dumps(cases, indent=2))
