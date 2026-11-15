"""Independent bounded rational polynomial checks, no project imports or writes.

These checks supplement a universal argument recorded separately; they do not
infer arbitrary-degree nonexistence from a degree cutoff or sampled failure.
"""
from fractions import Fraction
from itertools import permutations
import json

def add(a, b):
 out = dict(a)
 for e, c in b.items():
  out[e] = out.get(e, 0) + c
 return {e: c for e, c in out.items() if c}

def scale(p, c):
 return {e: c*v for e, v in p.items() if c*v}

def mul(a, b):
 out = {}
 for x, c in a.items():
  for y, d in b.items():
   e = tuple(i+j for i, j in zip(x, y))
   out[e] = out.get(e, 0) + c*d
 return {e: c for e, c in out.items() if c}

def power(p, k):
 out = {(0, 0, 0): 1}
 for _ in range(k):
  out = mul(out, p)
 return out

def sub(a, b):
 return add(a, scale(b, -1))

def evaluate(p, point):
 return sum(c*point[0]**e[0]*point[1]**e[1]*point[2]**e[2] for e, c in p.items())

def derivative(p, i):
 out = {}
 for e, c in p.items():
  if e[i]:
   q = list(e)
   q[i] -= 1
   out[tuple(q)] = c*e[i]
 return out

def axis(p):
 return {e[0]: c for e, c in p.items() if e[1:] == (0, 0)}

def rank_det(matrix):
 a = [[Fraction(v) for v in row] for row in matrix]
 rank = 0
 det = Fraction(1)
 for col in range(len(a[0])):
  pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
  if pivot is None:
   continue
  if pivot != rank:
   a[rank], a[pivot] = a[pivot], a[rank]
   det = -det
  v = a[rank][col]
  det *= v
  a[rank] = [x/v for x in a[rank]]
  for i in range(rank+1, len(a)):
   v = a[i][col]
   a[i] = [x-v*y for x, y in zip(a[i], a[rank])]
  rank += 1
  if rank == len(a):
   break
 return rank, det if len(a) == len(a[0]) and rank == len(a) else None

def run():
 checks = []
 def need(ok, label):
  if not ok:
   raise ValueError(label)
  checks.append(label)
 x, y, z = [{tuple(int(i == j) for i in range(3)): 1} for j in range(3)]
 variables = [x, y, z]
 R = {}
 for v in variables:
  R = add(R, power(v, 6))
 for i, j in permutations(range(3), 2):
  R = sub(R, mul(power(variables[i], 4), power(variables[j], 2)))
 R = add(R, scale(mul(mul(power(x, 2), power(y, 2)), power(z, 2)), 3))
 a, b, c = [power(v, 2) for v in variables]
 identity = add(mul(power(sub(a, b), 2), sub(add(a, b), c)), mul(c, mul(sub(a, c), sub(b, c))))
 need(R == identity, 'exact ordered-square Schur identity')
 gradient = [derivative(R, i) for i in range(3)]
 Z = [(1, s, t) for s in (-1, 1) for t in (-1, 1)]
 Z += [(1, s, 0) for s in (-1, 1)]
 Z += [(1, 0, t) for t in (-1, 1)]
 Z += [(0, 1, t) for t in (-1, 1)]
 need(len(set(Z)) == 10, 'ten distinct projective representatives')
 for point in Z:
  need(evaluate(R, point) == 0, 'zero:' + str(point))
  need(all(evaluate(g, point) == 0 for g in gradient), 'gradient zero:' + str(point))
 ranks = {}
 matrices = {}
 for degree in range(4):
  exponents = [(i, j, degree-i-j) for i in range(degree, -1, -1) for j in range(degree-i, -1, -1)]
  matrix = [[point[0]**i*point[1]**j*point[2]**k for i, j, k in exponents] for point in Z]
  rank, det = rank_det(matrix)
  need(rank == len(exponents), 'exact homogeneous evaluation injectivity degree' + str(degree))
  ranks[str(degree)] = {'columns': exponents, 'rank': rank, 'determinant': str(det) if det is not None else None}
  matrices[degree] = matrix
 for omitted in range(10):
  rank, _ = rank_det(matrices[3][:omitted] + matrices[3][omitted+1:])
  need(rank == 9, 'negative control: nine directions do not imply cubic injectivity:' + str(omitted))
 J = []
 K = []
 for i, j in [(0, 1), (0, 2), (1, 2)]:
  first = mul(variables[j], gradient[i])
  second = mul(variables[i], gradient[j])
  J.append(sub(first, second))
  K.extend([first, second])
 need(axis(R) == {6: 1}, 'axis exact sextic')
 need([axis(g) for g in gradient] == [{5: 6}, {}, {}], 'axis exact gradient')
 need(all(not axis(g) for g in J+K), 'axis lies in both exact ideal varieties')
 euler = {}
 for v, g in zip(variables, gradient):
  euler = add(euler, mul(v, g))
 need(euler == scale(R, 6), 'Euler identity prevents gradient-ideal conflation')
 q4 = mul(sub(a, b), sub(add(a, b), c))
 need(bool(q4) and all(evaluate(q4, point) == 0 for point in Z) and axis(q4) == {4: 1}, 'negative control: nonzero quartic vanishes on all ten lines and has fourth-degree axis restriction')
 need(all(evaluate({(0, 0, 0): 1}, point)**2 == 1 for point in Z), 'negative control: epsilon1 allows nonzero constant summands on zero lines')
 Q = add(add(power(sub({(0, 0, 0): 1}, mul(x, y)), 2), power(y, 2)), {(0, 0, 0): Fraction(-1, 2)})
 qx, qy = derivative(Q, 0), derivative(Q, 1)
 need(mul(y, qx) == scale(mul(power(y, 2), sub(mul(x, y), {(0, 0, 0): 1})), 2), 'exact product diagnostic first equation')
 need(mul(x, qy) == scale(mul(x, add(mul(x, sub(mul(x, y), {(0, 0, 0): 1})), y)), 2), 'exact product diagnostic second equation')
 need(evaluate(Q, (0, 0, 0)) == Fraction(1, 2) and evaluate(Q, (2, Fraction(1, 2), 0)) == Fraction(-1, 4), 'exact product diagnostic sign contrast')
 return {'independent_exact_checks': len(checks), 'labels': checks, 'ordered_Z': Z, 'evaluation_ranks_and_ordered_monomials': ranks, 'universal_claim_proved_by_finite_checks': False, 'source_programs_imported_or_executed': False, 'project_imports': 0, 'network': 0, 'file_writes': 0}

if __name__ == '__main__':
 print(json.dumps(run(), indent=2))
