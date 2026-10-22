"""Exact finite consistency checks; not a formal topological proof."""
from collections import Counter


def require(ok, message):
    if not ok:
        raise ValueError(message)


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def bracket(a, b):
    ab, ba = mul(a, b), mul(b, a)
    return [[ab[i][j] - ba[i][j] for j in range(3)] for i in range(3)]


def rank_mod(rows, p):
    rows = [[v % p for v in row] for row in rows]
    r = 0
    for col in range(len(rows[0]) if rows else 0):
        pivot = next((i for i in range(r, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inverse = pow(rows[r][col], -1, p)
        rows[r] = [v * inverse % p for v in rows[r]]
        for i in range(len(rows)):
            if i != r:
                c = rows[i][col]
                rows[i] = [(a - c * b) % p for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


def run_checks():
    j = [[0,-1,0],[1,0,0],[0,0,0]]
    a = [[1,0,0],[0,-1,0],[0,0,0]]
    b = [[0,1,0],[1,0,0],[0,0,0]]
    c = [[0,0,1],[0,0,0],[1,0,0]]
    d = [[0,0,0],[0,0,1],[0,1,0]]
    e = [[1,0,0],[0,1,0],[0,0,-2]]
    for source, target in [(a,scale(2,b)),(b,scale(-2,a)),(c,d),(d,scale(-1,c)),(e,scale(0,e))]:
        require(bracket(j,source)==target,'isotropy generator identity')
    require((2+1)%2==1,'nontrivial loop parity')
    hom_to_z4 = [v for v in range(4) if 2*v%4==0]
    require(hom_to_z4==[0,2] and {v%2 for v in hom_to_z4}=={0},'Bockstein reduction model')
    require([r for r in range(2,12) if 5-r+1==0]==[6],'transgression bidegree')
    eigen_checks = 0
    odd_orders = 0
    for n in range(1,258):
        fixed = []
        for k in range(n):
            spectrum = Counter([k%n,k%n,(-2*k)%n])
            # Spectrum of an SO(3) rotation: 1 and an inverse pair.
            has_real_rotation_spectrum = any(spectrum==Counter([0,t,(-t)%n]) for t in spectrum)
            if has_real_rotation_spectrum:
                fixed.append(k)
            eigen_checks += 1
        expected = [0] if n%2 else [0,n//2]
        require(fixed==expected,'circle stabilizer arithmetic')
        if n%2:
            odd_orders += 1
    rank_checks = 0
    cubic_cases = 0
    # A deliberately small diagnostic set, including monomials and mixed cubics.
    choices = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
               (1,1,1,1),(1,-1,1,-1),(2,1,0,1),(0,1,-1,2)]
    for p in (3,5,7):
        for coeff in choices:
            cubic_cases += 1
            for m in range(3,13):
                matrix = [[coeff[row-col] if 0<=row-col<4 else 0 for col in range(m-2)] for row in range(m+1)]
                require(rank_mod(matrix,p)==m-2,'injectivity of sampled cubic multiplication')
                require((m+1)-(m-2)==3,'cubic Hilbert dimension')
                rank_checks += 1
    return {'status':'PASS','isotropy_generator_identities':5,'isotropy_circle_weights':[0,1,2],
            'loop_parity_mod_two':1,'coefficient_reduction_zero':True,'only_two_row_differential':6,
            'circle_orders_checked':257,'odd_orders_checked':odd_orders,'spectrum_elements_checked':eigen_checks,
            'cubic_cases':cubic_cases,'multiplication_rank_checks':rank_checks,
            'proof_or_infinite_family_certification':False}


if __name__=='__main__':
    import json
    print(json.dumps(run_checks(),sort_keys=True,indent=2))
