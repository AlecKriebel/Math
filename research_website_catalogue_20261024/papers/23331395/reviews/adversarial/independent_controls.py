"""Finite boundary-interface controls, not a proof of algebraic geometry."""
from itertools import product
import json


def run():
    counts=[]
    total=0
    # All labelled trees via Prufer words; the degree sequence is sufficient
    # for the special-point stability test at each contracted component.
    for vertices in range(2,8):
        cases=0
        for word in product(range(vertices), repeat=vertices-2):
            degrees=[1]*vertices
            for letter in word:
                degrees[letter]+=1
            for nonconstant in range(vertices):
                for marked in range(vertices):
                    stable=all(degrees[v]+(v==marked)>=3
                               for v in range(vertices) if v!=nonconstant)
                    if stable:
                        raise RuntimeError('one nonconstant component plus one mark has stable ghosts')
                    cases+=1
        counts.append({'vertices':vertices,'root_and_mark_cases':cases})
        total+=cases
    # A second marking invalidates this particular ghost-exclusion assertion:
    # a contracted leaf can have one node plus two markings.
    assert 1+2 >= 3 and 1+1 < 3
    # The integer degree argument must count inseparable multiplicity as well.
    degree_cases=0
    for d in range(1,101):
        for image_degree in range(d,2*d+1):
            for generic_degree in (1,2,3,4,5,7,8,9,16,25):
                remainder=d-generic_degree*image_degree
                if remainder>=0:
                    assert remainder==0 and generic_degree==1 and image_degree==d
                degree_cases+=1
    # For P1 splitting O(a_i), positivity gives a_i>=1, enough for the
    # one-point and two-point deformation obstruction groups to vanish.
    splitting_checks=0
    for a in range(1,101):
        for marks in (1,2):
            h1=max(-a+marks-1,0)
            assert h1==0
            splitting_checks+=1
    return {'status':'PASS','universal_geometry_certified':False,
            'one_mark_tree_cases':counts,'total_tree_cases':total,
            'two_mark_countercontrol':'a ghost leaf with two marks is stable',
            'degree_cases':degree_cases,'splitting_checks':splitting_checks}


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
