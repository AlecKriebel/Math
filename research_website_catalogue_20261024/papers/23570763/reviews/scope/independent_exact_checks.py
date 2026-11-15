"""New independent finite checks via equality graphs of quadratic monomials.

Standard library only, no supplied-code imports, execution, network or writes.
These controls supplement the universal arguments; finite ranks are not used
as a proof for arbitrary widths or arbitrary fields.
"""
from itertools import combinations_with_replacement, permutations, product
import json

def mon(a, b):
 return tuple(sorted((a, b)))

def relations(n):
 rows = []
 for i in range(n):
  for j in range(i+1, n):
   rows.append((mon(i, j), None))
 for i in range(n):
  for j in range(i, n):
   rows.append((mon(n+i, n+j), None))
 for i in range(n):
  rows.append((mon(i, n+i), None))
  for j in range(n):
   for k in range(j+1, n):
    if i != j and i != k:
     rows.append((mon(i, n+j), mon(i, n+k)))
 return rows

class Quotient:
 def __init__(self, n, rows=None):
  self.n = n
  self.monomials = list(combinations_with_replacement(range(2*n), 2))
  self.parent = {m: m for m in self.monomials}
  self.parent[None] = None
  for a, b in relations(n) if rows is None else rows:
   aa, bb = self.find(a), self.find(b)
   if aa != bb:
    self.parent[aa] = bb
  dead = self.find(None)
  self.roots = set(self.find(m) for m in self.monomials) - {dead}
  candidates = [mon(i, i) for i in range(n)]
  if n >= 2:
   candidates += [mon(i, n+(1 if i == 0 else 0)) for i in range(n)]
  self.basis = [self.find(m) for m in candidates]
  self.basis_index = {m: i for i, m in enumerate(self.basis)}
  self.dead = dead
 def find(self, m):
  while self.parent[m] != m:
   m = self.parent[m]
  return m
 def multiplication(self, coefficients):
  out = [[0]*(2*self.n) for _ in self.basis]
  for col in range(2*self.n):
   for i, c in enumerate(coefficients):
    r = self.find(mon(i, col))
    if r != self.dead:
     out[self.basis_index[r]][col] += c
  return out
 def dimension(self):
  return len(self.roots)

def rank_mod(matrix, p):
 a = [[x % p for x in row] for row in matrix]
 r = 0
 for c in range(len(a[0])):
  i = next((i for i in range(r, len(a)) if a[i][c]), None)
  if i is None:
   continue
  a[r], a[i] = a[i], a[r]
  inv = pow(a[r][c], p-2, p)
  a[r] = [x*inv % p for x in a[r]]
  for i in range(r+1, len(a)):
   v = a[i][c]
   a[i] = [(x-v*y) % p for x, y in zip(a[i], a[r])]
  r += 1
  if r == len(a):
   break
 return r

def determinant(matrix):
 a = [row[:] for row in matrix]
 n = len(a)
 sign = 1
 prev = 1
 for k in range(n-1):
  pivot = next((i for i in range(k, n) if a[i][k]), None)
  if pivot is None:
   return 0
  if pivot != k:
   a[k], a[pivot] = a[pivot], a[k]
   sign = -sign
  value = a[k][k]
  for i in range(k+1, n):
   for j in range(k+1, n):
    numerator = a[i][j]*value-a[i][k]*a[k][j]
    if numerator % prev:
     raise ValueError('nonexact Bareiss division')
    a[i][j] = numerator // prev
   a[i][k] = 0
  prev = value
 return sign*a[-1][-1]

def image_monomial(m, injection, source_width, target_width):
 return tuple(sorted(injection[v] if v < source_width else target_width+injection[v-source_width] for v in m))

def run():
 checks = []
 def need(ok, label):
  if not ok:
   raise ValueError(label)
  checks.append(label)
 rows = []
 for n in range(1, 9):
  q = Quotient(n)
  expected = 1 if n == 1 else 2*n
  need(q.dimension() == expected and set(q.basis) == q.roots and len(q.basis_index) == expected, 'integral equality components and explicit basis width' + str(n))
  if n == 1:
   need(q.multiplication([1, 0]) == [[1, 0]], 'initial width degree1-to2 is surjective')
   continue
  aa = list(range(1, n+1))
  bb = list(range(-n, 0))
  mat = q.multiplication(aa+bb)
  B = sum(bb)
  expected_matrix = [[0]*(2*n) for _ in range(2*n)]
  for i in range(n):
   expected_matrix[i][i] = aa[i]
   expected_matrix[n+i][i] = B-bb[i]
   for j in range(n):
    expected_matrix[n+i][n+j] = aa[i] if i != j else 0
  need(mat == expected_matrix, 'matrix independently built from quotient relations width' + str(n))
  prod_a2 = 1
  for v in aa:
   prod_a2 *= v*v
  need(determinant(mat) == (-1)**(n-1)*(n-1)*prod_a2, 'integer arbitrary-coefficient determinant width' + str(n))
  ell = [1]*n+[0]*n
  good_matrix = q.multiplication(ell)
  square = [sum(row[i] for i in range(n)) for row in good_matrix]
  need(square == [1]*n+[0]*n, 'actual linear-form square including characteristic2 width' + str(n))
  JminusI = [[int(i != j) for j in range(n)] for i in range(n)]
  need(determinant(JminusI) == (-1)**(n-1)*(n-1), 'integer all-ones-minus-identity determinant width' + str(n))
  for p in (2, 3, 5):
   rank = rank_mod(good_matrix, p)
   need((rank == 2*n) == ((n-1) % p != 0), 'prime-field explicit Lefschetz form width' + str(n) + ':p' + str(p))
   if (n-1) % p == 0:
    z = [0]*n+[1]*n
    for i in range(2*n):
     coefficient = [int(k == i) for k in range(2*n)]
     v = [sum(c*d for c, d in zip(row, z)) % p for row in q.multiplication(coefficient)]
     need(not any(v), 'all variable actions kill nonzero degree1 socle vector:' + str((n, p, i)))
   rows.append({'n': n, 'p': p, 'explicit_form_rank': rank, 'middle_dimension': 2*n})
 # Exhaustive pointed small coefficient spaces, rather than relying on one
 # invariant form to infer failure.
 profiles = []
 for n, p in [(2, 2), (2, 3), (3, 2)]:
  q = Quotient(n)
  successes = 0
  total = 0
  for coeff in product(range(p), repeat=2*n):
   full = rank_mod(q.multiplication(coeff), p) == 2*n
   want = (n-1) % p != 0 and all(v != 0 for v in coeff[:n])
   need(full == want, 'complete small coefficient profile:' + str((n, p, coeff)))
   successes += full
   total += 1
  profiles.append({'n': n, 'p': p, 'profiles': total, 'successful_middle_maps': successes})
 # Actual orbit-generation comparison of integral equality graphs at width4.
 n = 4
 image_rows = []
 cubics = set()
 for injection in permutations(range(n), 3):
  for u, v in relations(3):
   image_rows.append((image_monomial(u, injection, 3, n), None if v is None else image_monomial(v, injection, 3, n)))
  for m in combinations_with_replacement(range(6), 3):
   cubics.add(image_monomial(m, injection, 3, n))
 generated = Quotient(n, image_rows)
 full = Quotient(n)
 for u in full.monomials+[None]:
  for v in full.monomials+[None]:
   need((generated.find(u) == generated.find(v)) == (full.find(u) == full.find(v)), 'width3 orbit quadratic equality relation:' + str((u, v)))
 need(cubics == set(combinations_with_replacement(range(8), 3)), 'all cubic monomials generated including repeated variables')
 image2 = []
 for injection in permutations(range(3), 2):
  for u, v in relations(2):
   image2.append((image_monomial(u, injection, 2, 3), None if v is None else image_monomial(v, injection, 2, 3)))
 need(Quotient(3, image2).dimension() == 9 != Quotient(3).dimension(), 'negative control: width2 relations cannot replace width3 generation')
 need(rank_mod(Quotient(2).multiplication([1, 1, 0, 0]), 2) == 4, 'negative control: characteristic dividing n does not imply failure')
 need(rank_mod(Quotient(3).multiplication([1, 1, 1, 0, 0, 0]), 2) < 6, 'negative control: n-1, not n, controls failure')
 need(rank_mod(Quotient(2).multiplication([0, 0, 1, 1]), 2) < 4, 'negative control: failing one invariant form does not prove WLP failure')
 return {'independent_checks': len(checks), 'finite_profile_summary': profiles, 'explicit_forms_across_widths_and_primes': rows, 'quadratic_quotient_method': 'free integer monomial equality graph, independently constructed from displayed ideal generators', 'universal_proof_inferred_from_finite_checks': False, 'supplied_code_imports_or_execution': 0, 'network': 0, 'file_writes': 0}

if __name__ == '__main__':
 print(json.dumps(run(), indent=2))
