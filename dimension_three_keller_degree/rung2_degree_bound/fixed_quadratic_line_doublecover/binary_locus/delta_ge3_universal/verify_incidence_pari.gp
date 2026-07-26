\\ Independent PARI/GP replay for the universal binary delta>=3 atlas.
\\
\\ Unlike the SymPy release certificate, this script does not enumerate
\\ linear systems or take gcds of maximal minors.  It computes the three
\\ Jacobian forms directly and checks the exact homogeneous gcd of a
\\ representative of every orbit family in both affine charts P^1.

p = 'p;
q = 'q;

jac(f,g) = deriv(f,p)*deriv(g,q) - deriv(f,q)*deriv(g,p);

check_zero(value,message) =
{
  if(value != 0, error(Str("FAIL: ",message,"; residual = ",value)));
};

check_true(value,message) =
{
  if(!value, error(Str("FAIL: ",message)));
};

\\ A homogeneous common factor is primitive precisely when it is primitive
\\ in both dehomogenizations q=1 and p=1.  This detects a possible residual
\\ factor supported at infinity in either chart.
check_exact_gcd(h,R,expected,name) =
{
  my(P=h*p^2, Q=h*q^2, aa=jac(Q,R), bb=-jac(P,R),
     cc=jac(P,Q), af,bf,cf,ef,ai,bi,ci,ei,gf,gi);
  af=subst(aa,q,1); bf=subst(bb,q,1); cf=subst(cc,q,1);
  ef=subst(expected,q,1);
  ai=subst(aa,p,1); bi=subst(bb,p,1); ci=subst(cc,p,1);
  ei=subst(expected,p,1);
  gf=gcd(gcd(af,bf),cf);
  gi=gcd(gcd(ai,bi),ci);
  check_true(poldegree(gf,p)==poldegree(ef,p),
             Str(name," finite-chart gcd degree"));
  check_true(poldegree(gi,q)==poldegree(ei,q),
             Str(name," infinity-chart gcd degree"));
  check_zero(gf/pollead(gf,p)-ef/pollead(ef,p),
             Str(name," finite-chart expected divisor"));
  check_zero(gi/pollead(gi,q)-ei/pollead(ei,q),
             Str(name," infinity-chart expected divisor"));
};

\\ Rational representatives of every delta-three orbit family.
L = p+q;

check_exact_gcd(p^2,p^2*(p+q),p^3,"D3-BS-P3");
check_exact_gcd(p^2,p*(p^2+q^2),p^2*q,"D3-BS-P2Q");
check_exact_gcd(p*q,p^3,p^3,"D3-TB-P3");
check_exact_gcd(p*q,p^2*q,p^2*q,"D3-TB-P2Q");

check_exact_gcd(p*L,p^3,p^3,"D3-OB-P3");
check_exact_gcd(p*L,p^2*L,p^2*L,"D3-OB-P2L");
check_exact_gcd(p*L,p*L^2,p*L^2,"D3-OB-PL2");
check_exact_gcd(p*L,p^2*(4*p+3*q),p^2*q,"D3-OB-P2Q");
check_exact_gcd(p*L,p*L*(4*p-q),p*q*L,"D3-OB-PQL");
check_exact_gcd(p*L,L^2*(4*p-5*q),q*L^2,"D3-OB-QL2");

check_exact_gcd(L^2,L^2*p,L^3,"D3-DN-L3");
check_exact_gcd(L^2,L*(p*q/2+q^2),p*L^2,"D3-DN-PL2");
check_exact_gcd(L^2,2*p^3+3*p^2*q,p*q*L,"D3-DN-PQL");

sr = 2;
Lr = p-sr*q;
Mr = sr*p-q;
hr = Lr*Mr;
R21 = Lr^2*Mr;
R2c = Lr^2*((3*sr^2-5)*p-4*sr*q);
R11c = Lr*Mr*(4*sr*p+(sr^2+1)*q);
R1c2 = Mr*(4*p^2*sr^3-12*p^2*sr-3*p*q*sr^4+10*p*q*sr^2-3*p*q-12*q^2*sr^3+4*q^2*sr);
check_exact_gcd(hr,R21,Lr^2*Mr,"D3-SF-21");
check_exact_gcd(hr,R2c,p*Lr^2,"D3-SF-2C");
check_exact_gcd(hr,R11c,q*Lr*Mr,"D3-SF-11C");
check_exact_gcd(hr,R1c2,p*q*Mr,"D3-SF-1C2");
print("PASS PARI all 17 delta-three orbit representatives");

\\ Rational representatives of the doubled-nonbranch delta-four families.
check_exact_gcd(L^2,L^3,L^4,"D4-DN-L4");
check_exact_gcd(L^2,L^2*(p-2*q),p*L^3,"D4-DN-PL3");
check_exact_gcd(L^2,L*(2*p^2+p*q+2*q^2),p*q*L^2,"D4-DN-PQL2");
print("PASS PARI three doubled-nonbranch delta-four representatives");

\\ The three squarefree delta-four orbits are checked over their exact
\\ number fields.  Each modulus is irreducible over Q.
x = 'x;

f21 = x^2+5;
s21 = Mod(x,f21);
l21 = p-s21*q;
m21 = s21*p-q;
h21 = l21*m21;
check_exact_gcd(h21,l21^2*m21,p*l21^2*m21,"D4-SF-21C");
check_zero((s21+1/s21)^2+16/5,"D4-SF-21C kappa");

f2c2 = 5*x^4-6*x^2+5;
s2c2 = Mod(x,f2c2);
l2c2 = p-s2c2*q;
m2c2 = s2c2*p-q;
h2c2 = l2c2*m2c2;
r2c2 = l2c2^2*((3*s2c2^2-5)*p-4*s2c2*q);
check_exact_gcd(h2c2,r2c2,p*q*l2c2^2,"D4-SF-2C2");
check_zero((s2c2+1/s2c2)^2-16/5,"D4-SF-2C2 kappa");

f11c2 = x^2-4*x+1;
s11c2 = Mod(x,f11c2);
l11c2 = p-s11c2*q;
m11c2 = s11c2*p-q;
h11c2 = l11c2*m11c2;
r11c2 = l11c2*m11c2*(p+q);
check_exact_gcd(h11c2,r11c2,p*q*l11c2*m11c2,"D4-SF-11C2");
check_zero((s11c2+1/s11c2)^2-16,"D4-SF-11C2 kappa");
print("PASS PARI three algebraic squarefree delta-four orbits");

\\ Direct boundary replays in the doubled-nonbranch chart.
check_exact_gcd(L^2,L^3,L^4,"D3-DN-L3 boundary A=B");
check_exact_gcd(L^2,L^2*(p-2*q),p*L^3,"D3-DN-PL2 boundary 2A+C=0");
check_exact_gcd(L^2,L*(2*p^2+p*q+2*q^2),p*q*L^2,"D3-DN-PL2 boundary A=C");
check_exact_gcd(L^2,L*(2*p^2+p*q+2*q^2),p*q*L^2,"D3-DN-PQL boundary A=B");
print("PASS PARI internal doubled-nonbranch boundary arrows");

\\ The unique dependent power fibre: beta vanishes and alpha,gamma have
\\ homogeneous gcd p^4*q.  This is deliberately separated from delta=4.
hp = p^2;
rp = p^3;
pp = hp*p^2;
qp = hp*q^2;
ap = jac(qp,rp);
bp = -jac(pp,rp);
gp = jac(pp,qp);
check_zero(bp,"PF-BS beta");
check_zero(ap+6*p^4*q,"PF-BS alpha");
check_zero(gp-8*p^5*q,"PF-BS gamma");
check_exact_gcd(hp,rp,p^4*q,"PF-BS homogeneous gcd");
print("PASS PARI unique dependent power-fibre representative");

print("DELTA_GE3_UNIVERSAL_PARI_PASS_17_6_1");
quit(0);
