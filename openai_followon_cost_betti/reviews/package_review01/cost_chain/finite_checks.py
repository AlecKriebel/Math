"""Independent finite falsification checks; none certifies an infinite theorem."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json


def reduce_word(word):
    answer=[]
    for x in word:
        if answer and answer[-1]==-x:
            answer.pop()
        else:
            answer.append(x)
    return answer


face_count=0
for length in range(3,11):
    for face in product((0,1), repeat=length):  # 0=outer, 1=inner
        weight=Fraction(0)
        for i,inner in enumerate(face):
            if inner:
                neighbors=face[i-1]+face[(i+1)%length]
                weight+=(Fraction(1),Fraction(1,2),Fraction(1,3))[neighbors]
        assert weight <= length-2, (face,weight)
        face_count+=1

# For cyclically neighboring distinct indices the overlap word cannot be empty.
overlap_count=0
for i,k,l,j in product(range(13),repeat=4):
    if i==k or k==l or l==j or j==i:
        continue
    word=[x for x in (i,-k,l,-j) if x]
    assert reduce_word(word), (i,k,l,j)
    overlap_count+=1

saturation_count=0
for A in (Fraction(i,4) for i in range(4,40001)):
    s=A.numerator//A.denominator
    assert s>=1
    assert 2*A+90*s<96*s, (A,s)
    assert 2*A+90*(s-1)<=92*A
    saturation_count+=1

left=2*3**97*96**4
right=2**183
assert left<right
assert 2**61>200
certificate={
    'scope':'Finite arithmetic and finite combinatorial falsification checks only; not a formal certificate of cost, planar topology, graph surgery, or the infinite model sequence.',
    'checks':{'face_weight_binary_walks_lengths_3_to_10':face_count,
              'overlap_words_indices_0_to_12':overlap_count,
              'saturation_boundary_quarter_steps_A_1_to_10000':saturation_count},
    'exact_parameter':{'alpha':'1/2305843009213693952',
                       'eta':'1/230584300921369395200',
                       'twice_K_integer_upper_bound':str(left),
                       'alpha_inverse_cube':str(right),
                       'strict_positive_margin':str(right-left)},
    'all_checks_pass':True,
}
if __name__=='__main__':
    Path(__file__).with_name('finite_checks.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps(certificate,indent=2))
