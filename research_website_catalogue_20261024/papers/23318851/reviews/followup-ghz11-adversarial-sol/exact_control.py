"""Independently written exact GHZ11 control; no imported research/support code."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import comb, prod
from pathlib import Path
import datetime, hashlib, json
if not __debug__:
    raise RuntimeError('Exact assertions must be enabled')
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23318851/reviews/followup-ghz11-adversarial-sol')
N=11
# The integer sparse tensor B has two entries 1; A=B/sqrt(2).
sparse_B={tuple([0]*N):1,tuple([1]*N):1}
norm_squared_A=F(sum(v*v for v in sparse_B.values()),2)
flattenings=[]
for mode in range(N):
    rows=[{},{}]
    for bits,value in sparse_B.items():
        column=bits[:mode]+bits[mode+1:]
        rows[bits[mode]][column]=value
    integer_gram=[[sum(v*rows[b].get(c,0) for c,v in rows[a].items()) for b in range(2)] for a in range(2)]
    gram=[[F(v,2) for v in row] for row in integer_gram]
    determinant=gram[0][0]*gram[1][1]-gram[0][1]*gram[1][0]
    flattenings.append(dict(mode=mode,unscaled_integer_gram=integer_gram,normalized_gram=[[str(v) for v in row] for row in gram],determinant=str(determinant),row_supports=[[''.join(map(str,c)) for c in row] for row in rows]))
    assert integer_gram==[[1,0],[0,1]] and determinant==F(1,4)
assert norm_squared_A==1 and len(flattenings)==N
d=[F(x['determinant']) for x in flattenings]
q1_factors=[sum(d[j] for j in range(N) if j!=i)-d[i] for i in range(N)]
q1=prod(q1_factors)
# Route A: enumerate ALL sign vectors and multiply the actual rational factors.
q2_raw=F(1,2)
signed_integer_product=1
histogram=Counter()
negative=zero=positive=0
trace=[]
for epsilon in product((-1,1),repeat=N):
    sign_sum=sum(epsilon)
    factor=sum(F(e,2) for e in epsilon)
    q2_raw*=factor
    signed_integer_product*=sign_sum
    histogram[sign_sum]+=1
    negative+=factor<0;zero+=factor==0;positive+=factor>0
    trace.append(''.join('+' if e==1 else '-' for e in epsilon)+'\t'+str(sign_sum)+'\t'+str(factor)+'\n')
trace_raw=('epsilon\tsigned_integer_sum\tactual_Q2_factor\n'+''.join(trace)).encode()
with (OWN/'RAW_SIGN_FACTORS.tsv').open('xb') as stream:stream.write(trace_raw)
assert len(trace)==2**N and negative==positive==1024 and zero==0
assert q2_raw==F(signed_integer_product,2**(2**N+1))
# Route B: independent binomial grouping, no reference to the enumeration histogram.
q2_binomial=F(1,2)
binomial_rows=[]
for k in range(N+1):
    multiplicity=comb(N,k)
    factor=F(N-2*k,2)
    q2_binomial*=factor**multiplicity
    binomial_rows.append(dict(number_of_negative_signs=k,signed_integer_sum=N-2*k,multiplicity=multiplicity,factor=str(factor)))
assert sum(x['multiplicity'] for x in binomial_rows)==2**N
assert dict(histogram)=={N-2*k:comb(N,k) for k in range(N+1)}
assert q2_raw==q2_binomial and q2_raw>q1>0

def factor_integer(value):
    assert value>0
    result={};p=2
    while p*p<=value:
        while value%p==0:
            result[p]=result.get(p,0)+1;value//=p
        p+=1
    if value>1:result[value]=result.get(value,0)+1
    return result

def binary_bracket(value):
    assert value>0
    b=value.numerator.bit_length()-value.denominator.bit_length()
    power=lambda exponent:F(2**exponent) if exponent>=0 else F(1,2**(-exponent))
    if value<power(b):b-=1
    assert power(b)<=value<power(b+1)
    return dict(lower_exponent=b,upper_exponent=b+1,strict_lower=value>power(b))
ratio=q2_raw/q1
q2_factorization=dict(numerator=factor_integer(q2_raw.numerator),denominator=factor_integer(q2_raw.denominator))
ratio_factorization=dict(numerator=factor_integer(ratio.numerator),denominator=factor_integer(ratio.denominator))
# Compare supplied hypothesis formulas only AFTER independent evaluations/factorizations.
assert q1==F(3**22,2**22)
assert q2_factorization==dict(numerator={3:704,5:330,7:110,11:2},denominator={2:2049})
assert ratio_factorization==dict(numerator={3:682,5:330,7:110,11:2},denominator={2:2027})
# A short integer-only strict certificate, separate from giant integer comparison.
assert 9>8 and 625>512 and 25>16 and 16807>16384 and 121>64
exact_ratio_numerator=9**341*625**82*25*16807**22*121
lower_numerator=8**341*512**82*16*16384**22*64
assert exact_ratio_numerator==ratio.numerator
assert lower_numerator==2**2079 and exact_ratio_numerator>lower_numerator
assert ratio>2**52
# Small-dimensional controls catch missing 1/2, parity and n=3 boundary conventions.
controls=[]
for n in (3,4,5,7,9):
    first=F(n-2,4)**n
    second=F(1,2)
    for epsilon in product((-1,1),repeat=n):second*=F(sum(epsilon),2)
    grouped=F(1,2)*prod(F(n-2*k,2)**comb(n,k) for k in range(n+1))
    assert second==grouped
    if n==3:assert first==F(1,64) and second==F(9,512) and first-second==F(-1,512)
    elif n==4:assert second==0 and first>second
    else:assert first>second
    controls.append(dict(n=n,Q1=str(first),Q2=str(second),Q1_minus_Q2_sign=(first>second)-(first<second)))
certificate=dict(schema='ghz11-independent-exact-falsification-certificate-v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),n=N,tensor='A=(e_0^tensor11+e_1^tensor11)/sqrt(2), real',squared_Frobenius_norm=str(norm_squared_A),flattenings=flattenings,determinants=[str(x) for x in d],Q1_factors=[str(x) for x in q1_factors],Q1=str(q1),Q2_raw_sign_product=str(q2_raw),Q2_independent_binomial_product=str(q2_binomial),Q2_factorization=q2_factorization,ratio_factorization=ratio_factorization,ratio=str(ratio),raw_sign_vector_count=len(trace),negative_factors=negative,zero_factors=zero,positive_factors=positive,raw_trace_SHA256=hashlib.sha256(trace_raw).hexdigest(),binomial_rows=binomial_rows,Q1_binary_bracket=binary_bracket(q1),Q2_binary_bracket=binary_bracket(q2_raw),ratio_binary_bracket=binary_bracket(ratio),short_strict_bound='Q2/Q1 > 2^(2079-2027) = 2^52 > 1',controls=controls,source_or_support_code_imported=False,floating_point_used=False,claimed_scope='Counterexample to universal necessary inclusion at n=11 under the printed definitions; no novelty/priority/publication claim and no scientific defect asserted in Alec Gram194 paper')
with (OWN/'EXACT_CERTIFICATE.json').open('x') as stream:json.dump(certificate,stream,indent=2);stream.write('\n')
print(json.dumps(dict(status='EXACT_GHZ11_FALSIFICATION_PASSED',n=N,unit_norm=norm_squared_A==1,all_eleven_determinants='1/4',Q1_factorization=dict(numerator={3:22},denominator={2:22}),Q2_factorization=q2_factorization,ratio_factorization=ratio_factorization,ratio_binary_bracket=certificate['ratio_binary_bracket'],raw_sign_vectors=len(trace),independent_routes_equal=True,short_bound='Q2/Q1 > 2^52',controls=controls)))
