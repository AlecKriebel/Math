#!/opt/homebrew/bin/python3.11
"""Repeat the most ill-conditioned/limiting physical computations at 130 digits."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json
import independent_check as fresh

D=Path(__file__).resolve().parent
base=json.loads((D/'NUMERICAL_GEOMETRY_RESULTS.json').read_text())
specs=[('0.999999',31,15,'precision_probe'),('0.00000001',11,5,'precision_probe'),
       ('0.75',101,1,'precision_probe'),('0.75',101,50,'precision_probe')]
out=fresh.numeric_checks(130,specs)
comparisons=[]
for row in out['records']:
    old=next(r for r in base['records'] if (r['k'],r['N'],r['tau'])==(row['k'],row['N'],row['tau']))
    # Stored 24-significant-digit phase products must agree on precision increase.
    agrees=all(a['product']==b['product'] and a['Bplus']==b['Bplus'] and a['Bminus']==b['Bminus']
               for a,b in zip(old['phases'],row['phases']))
    assert agrees
    comparisons.append({'k':row['k'],'N':row['N'],'tau':row['tau'],
                        'all_24_digit_phase_areas_and_products_agree':agrees,
                        'old_relative_product_variation':old['relative_product_variation'],
                        'new_relative_product_variation':row['relative_product_variation']})
out['precision_comparisons']=comparisons
(D/'PRECISION_PROBE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print('All 24-significant-digit phase areas/products stable at 130 digits.')
