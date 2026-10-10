"""Supplementary exact arithmetic only; no imports, file access, or network."""
def require(condition, label):
    if not condition:
        raise SystemExit("FAILED: " + label)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def prime(n):
    if n < 2:
        return False
    t = 2
    while t*t <= n:
        if n % t == 0:
            return False
        t += 1
    return True

def valuation(n, p):
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v

def det3(m):
    a,b,c = m[0]
    d,e,f = m[1]
    g,h,i = m[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)

require(-4*(-4)**3-27 == 229, "arithmetic check 01")
require(prime(229), "arithmetic check 02")
require((1**3-4*1+1) != 0, "arithmetic check 03")
require(((-1)**3-4*(-1)+1) != 0, "arithmetic check 04")
modular_residue_checks = 0
for x in range(229):
    require((x**3-4*x+1-(x-29)**2*(x-171)) % 229 == 0, "arithmetic check 05")
    modular_residue_checks += 1
require((3*29**2-4) % 229 == 0, "arithmetic check 06")
require((3*171**2-4) % 229 != 0, "arithmetic check 07")
def reduce_mod_f(coeffs):
    a = coeffs + [0]*max(0, 3-len(coeffs))
    for j in range(len(a)-1, 2, -1):
        c = a[j]
        a[j] = 0
        a[j-2] += 4*c
        a[j-3] -= c
    return a[:3]
cols = [reduce_mod_f([0]*j + [-4,0,3]) for j in range(3)]
matrix = [[cols[j][i] for j in range(3)] for i in range(3)]
require(matrix == [[-4,-3,0],[0,8,-3],[3,0,8]], "arithmetic check 08")
require(det3(matrix) == -229, "arithmetic check 09")
require((-3)**3-4*(-3)+1 < 0 < (-2)**3-4*(-2)+1, "arithmetic check 10")
require(0**3-4*0+1 > 0 > 1**3-4*1+1, "arithmetic check 11")
require(1**3-4*1+1 < 0 < 2**3-4*2+1, "arithmetic check 12")

conductor_checks = 0
necessary_cases = 0
values = []
E = 1
for d in range(1,9):
    E = E*d//gcd(E,d)
    m = 2*E
    M = 2**(valuation(m,2)+2)
    for p in range(3,m+2,2):
        if prime(p) and m % (p-1) == 0:
            M *= p**(valuation(m,p)+1)
    values.append([d,E,M])
    for n in range(1,601):
        condition = all(pow(u,m,n) == (1 % n)
                        for u in range(1,n+1) if gcd(u,n) == 1)
        if condition:
            necessary_cases += 1
            require(M % n == 0, "arithmetic check 13")
        conductor_checks += 1
require(values[0][2] == 24, "arithmetic check 14")
require(values[1][2] == 240, "arithmetic check 15")
require(values[2][2] == 65520, "arithmetic check 16")
require(modular_residue_checks == 229, "modular coverage")
require(conductor_checks == 4800, "conductor coverage")
require(necessary_cases == 1030, "necessary-case coverage")
print('{"status":"passed","discriminant":229,"norm":-229,'
      '"modular_residue_checks":229,"conductor_cases":%d,'
      '"conductor_necessary_cases":%d,"d_range":[1,8],"n_range":[1,600]}'
      % (conductor_checks,necessary_cases))
