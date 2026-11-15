"""Independent atomic dB raw-rate check for the admitted concentration family.

No supplied mathematical program is imported. Finite fractions check the
transcription; the limiting discrepancy is proved algebraically in ROOT_REVIEW.
"""
from fractions import Fraction as F
import json

def need(value, message):
    if not value:
        raise RuntimeError(message)

rows = []
r = F(3, 2)
for k in [2, 3, 5, 10, 100, 1000]:
    s, q, heavy = k**4, k**2, k
    light = s - heavy
    lam_h, lam_l = F(k**3), F(s, light)
    edge_h, edge_l = lam_h / s, lam_l / s
    blade_load = 2 * (F(heavy, s)*lam_h + F(light, s)*lam_l)
    need(blade_load == 4 and edge_h == F(1, k), 'Exact original conditions')
    need(q < s and lam_h < s and F(q)*edge_h == k, 'Separate smallness versus aggregate')
    need(F(heavy, s)*2*lam_h/blade_load == F(1, 2), 'Half predicted child incidence')
    # One mutant portal, all blade endpoints resident. Death rate of each
    # endpoint is one after the exact global n time change. Its partner has
    # weight one and is resident; one portal has mutant fitness r.
    raw_h = 2*heavy*r*edge_h / (1 + (q+r-1)*edge_h)
    raw_l = 2*light*r*edge_l / (1 + (q+r-1)*edge_l)
    need(raw_h == 2*r/(1+k+(r-1)/k), 'Heavy rate derived from atomic rule')
    need(raw_l == 2*r/(1+F(q+r-1, light)), 'Light rate derived from atomic rule')
    need(0 < raw_h < 2*r and 0 < raw_l < 2*r, 'Rate bounds')
    need(raw_h + raw_l != r*blade_load, 'Not the advertised dilute raw rate')
    rows.append({'k': k, 's': s, 'Q': q, 'B': str(blade_load),
                 'heavy_total_outer_degree': k,
                 'predicted_child_incidence_heavy': '1/2',
                 'actual_raw_dB_heavy': str(raw_h), 'actual_raw_dB_light': str(raw_l),
                 'actual_raw_dB_total': str(raw_h+raw_l),
                 'advertised_dilute_raw_rate': str(r*blade_load)})
need(F(rows[-1]['actual_raw_dB_total']) < F(301, 100), 'Large-k transcription near limit3')
print(json.dumps({'status': 'PASS_EXACT_RAW_RATE_COUNTERDIAGNOSTIC',
                  'actual_atomic_rate_limit': '2r = 3 at r=3/2',
                  'advertised_dilute_rate': 'rB = 4r = 6 at r=3/2',
                  'finite_fractions_are_infinite_limit_proof': False,
                  'source_program_imports_or_writes': False, 'rows': rows}, indent=2))
