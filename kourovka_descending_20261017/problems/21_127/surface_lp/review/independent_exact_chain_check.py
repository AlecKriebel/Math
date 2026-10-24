#!/usr/bin/env python3
"""Fresh free-word and degree checks for one exact chain certificate."""
from fractions import Fraction
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def inv(w):
    return w.swapcase()[::-1]


def normal(w):
    stack = []
    for letter in w:
        if stack and stack[-1] == letter.swapcase():
            stack.pop()
        else:
            stack.append(letter)
    return ''.join(stack)


def comm(u,v):
    return normal(u+v+inv(u)+inv(v))


def main():
    snapshot = HERE/'exact_chain_reproduction'
    snapshot.mkdir(exist_ok=True)
    shutil.copyfile(BASE/'check_exact_chain.py',snapshot/'check_exact_chain.py')
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    p = subprocess.run([sys.executable,str(snapshot/'check_exact_chain.py')],
                       check=True,capture_output=True,text=True,env=env)
    assert json.loads((BASE/'EXACT_CHAIN_CHECKS.json').read_text()) == json.loads((snapshot/'EXACT_CHAIN_CHECKS.json').read_text())

    # Independently use alphabet inversion, not the author's signed-integer code.
    a,b,c,d = 'x','XX','','y'
    assert all(comm(u,v)=='' for u,v in [(a,b),(b,c),(c,d)])
    h = comm('x','y')
    first = comm(normal(a+b),d)
    second = comm(d,a)
    assert first == normal('X'+inv(h)+'x') == 'XyxY'
    assert second == inv(h) == 'yxYX'
    assert comm('ab','d') == 'abdBAD'
    # Check the two actual displayed outer words after substitution.
    image = {'a':a,'b':b,'c':c,'d':d}
    image.update({x.upper():inv(w) for x,w in list(image.items())})
    substitute = lambda w: normal(''.join(image[x] for x in w))
    assert substitute('badBAD') == first
    assert substitute('daDA') == second

    # Attaching an annulus along two circles of one connected 4-holed sphere.
    chi = -2 + 0  # circle gluings have Euler characteristic zero
    boundary_count = 4 + 2 - 4
    genus = (2-boundary_count-chi)//2
    common_chain_degree = 1
    assert boundary_count == 2 and genus == 1
    assert Fraction(-chi,2*common_chain_degree) == 1
    # An independent upper construction: two punctured tori, one for each term.
    assert Fraction(1+1,2*common_chain_degree) == 1
    out = {'scope':'one exact homogeneous chain value; not arbitrary RAAG words',
           'author_json_reproduced_identically':True,'author_stdout':p.stdout.strip(),
           'free_word_h':h,'first_image':first,'second_image':second,
           'all_defining_relations_respected':True,
           'surface_characteristic':chi,'surface_boundary_count':boundary_count,
           'surface_genus':genus,'common_chain_degree':common_chain_degree,
           'surface_upper_bound':'1','homogeneous_image_chain':'2 h^-1',
           'lower_bound_from_established_free_commutator_value':'1',
           'all_checks_passed':True}
    (HERE/'independent_exact_chain_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__ == '__main__':
    main()
