"""Independent exact scalar replay of the consecutive-gap profile failure.
Uses trinomial coefficient counts and products of previous divisors;
imports no code from the proposed certificate implementation.
"""
from fractions import Fraction
from math import factorial
from pathlib import Path
import hashlib, json

def trinomial(m, x):
    total = 0
    for minus in range(m+1):
        plus = minus + x
        zero = m-minus-plus
        if plus >= 0 and zero >= 0:
            total += factorial(m)//(factorial(minus)*factorial(plus)*factorial(zero))
    return total

def maximal_three_sum(m):
    a = {x: trinomial(m, x) for x in range(-m, m+1)}
    return max(sum(a.get(x,0) for x in range(left,left+3))
               for left in range(-m-2,m+1))

def main():
    divisors=[]
    records=[]
    for step in range(1,101):
        n=len(divisors)
        choices=[]
        product=Fraction(1)
        for age in range(n+1):
            if age:
                product *= divisors[n-age]
            m=maximal_three_sum(age)
            choices.append(Fraction(m*m,9)/product)
        profile=max(choices)
        divisor=9*(1-profile)
        records.append({'step':step,'c3':str(profile),'divisor':str(divisor),
                        'maximizing_ages':[i for i,v in enumerate(choices) if v==profile],
                        'positive':divisor>0})
        if divisor<=0:
            break
        divisors.append(divisor)
    if len(records)!=27 or any(not x['positive'] for x in records[:-1]) or records[-1]['positive']:
        raise RuntimeError('Expected first nonpositive divisor at step27')
    out={'verified':True,'first_nonpositive_step':27,
         'method':'Independent trinomial coefficient / trailing-divisor product recurrence',
         'scope':'Failure of this uniform sufficient recursion only; not a losing game',
         'records':records}
    path=Path(__file__).with_name('independent_profile_recursion_replay.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'verified':True,'first_nonpositive_step':27,
                      'last_divisor_approx':float(divisor),
                      'replay_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':
    main()
