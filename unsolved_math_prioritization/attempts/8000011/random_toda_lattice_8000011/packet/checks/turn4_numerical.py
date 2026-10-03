import mpmath as m, json
m.mp.dps=45
C=m.sqrt(m.pi/8);B=C*(m.log(2)-m.euler)/2
rows=[];checks=0
for eps in [m.mpf(1),m.mpf('.1'),m.mpf('.01'),m.mpf('.001')]:
 f=lambda d:m.exp(-d*d/8)*m.acosh(d/(2*eps))*m.acos(2*eps/d)/(2*m.pi)
 val=m.quad(f,[2*eps,max(2*eps+1,m.mpf(4)),m.inf])
 rows.append({'epsilon':str(eps),'mean':str(val),'difference_from_two_term':str(val-C*m.log(1/eps)-B)})
for A in [m.mpf('.2'),m.mpf(1),m.mpf(3)]:
 d=m.mpf(4)
 direct=m.quad(lambda s:(A-s)/d/m.pi/m.cosh(s),[-A,0,A])
 analytic=2*A/(m.pi*d)*m.acos(1/m.cosh(A))
 assert abs(direct-analytic)<m.mpf('1e-40');checks+=1
assert m.acosh(4)<3;checks+=1
print(json.dumps({'diagnostic_checks':checks,'precision_digits':45,'C2':str(C),'B2':str(B),'rows':rows,'scope':'floating quadrature diagnostics, not exact proof certificates'},indent=2))
