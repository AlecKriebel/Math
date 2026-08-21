\\ Independent PARI/GP replay of the exact delta=2 HB regressions.

p = 'p;
q = 'q;

jac(f,g) = deriv(f,p)*deriv(g,q) - deriv(f,q)*deriv(g,p);

m2(h,R) =
{
  my(P=h*p^2, Q=h*q^2, A=jac(Q,R), B=-jac(P,R), cols);
  cols = [A,B];
  matrix(6,2,i,j,polcoeff(subst(cols[j],q,1),6-i,p));
};

m1(h,R) =
{
  my(P=h*p^2, Q=h*q^2, A=jac(Q,R), B=-jac(P,R),
     G=jac(P,Q), cols);
  cols = [A*p,A*q,B*p,B*q,G];
  matrix(7,5,i,j,polcoeff(subst(cols[j],q,1),7-i,p));
};

m0(h,R) =
{
  my(P=h*p^2, Q=h*q^2, A=jac(Q,R), B=-jac(P,R),
     G=jac(P,Q), cols);
  cols = [A*p^2,A*p*q,A*q^2,B*p^2,B*p*q,B*q^2,G*p,G*q];
  matrix(8,8,i,j,polcoeff(subst(cols[j],q,1),8-i,p));
};

check_zero(value,message) =
{
  if(value != 0, error(Str("FAIL: ",message,"; residual = ",value)));
};

check_rank_tuple(h,R,expected,message) =
{
  my(got=[matrank(m2(h,R)),matrank(m1(h,R)),matrank(m0(h,R))]);
  if(got != expected,
     error(Str("FAIL: ",message,"; rank tuple = ",got)));
};

\\ Mandatory rational kappa=16 regression.
h16 = p^2 + 4*p*q + q^2;
R16 = p^3 + 3*p^2*q + 6*p*q^2 + 2*q^3;
A16 = jac(h16*q^2,R16);
B16 = -jac(h16*p^2,R16);
G16 = jac(h16*p^2,h16*q^2);
check_zero(gcd(gcd(A16,B16),G16)-2*p*q,"kappa=16 gcd");
check_zero(polresultant(subst(h16,q,1),subst(R16,q,1),p)+18,"kappa=16 resultant");
check_rank_tuple(h16,R16,[2,4,6],"kappa=16 ranks");
check_zero(m1(h16,R16)*[-5,-1,1,5,3]~,"kappa=16 literal kernel");
print("PASS PARI kappa=16 gcd, resultant, ranks, and kernel");

\\ Mandatory rational doubled-root kappa=4 regression.
h4 = (p+q)^2;
R4 = 6*p^2*q + 15*p*q^2 + 10*q^3;
A4 = jac(h4*q^2,R4);
B4 = -jac(h4*p^2,R4);
G4 = jac(h4*p^2,h4*q^2);
check_zero(gcd(gcd(A4,B4),G4)^2-4*p^2*(p+q)^2,"kappa=4 gcd");
check_zero(polresultant(subst(h4,q,1),subst(R4,q,1),p)-1,"kappa=4 resultant");
check_rank_tuple(h4,R4,[2,4,6],"kappa=4 ranks");
check_zero(m1(h4,R4)*[-3,-2,0,1,3]~,"kappa=4 literal kernel");
print("PASS PARI kappa=4 gcd, resultant, ranks, and kernel");

\\ Algebraic kappa=16/3 regression over Q(sqrt(3)).  Polynomial
\\ coefficients must be lifted before coefficient extraction in PARI.
x = 'x;
modx = x^2-3;
tt = Mod(x,modx);
et = 4*tt/3;

alg_coeff(f,index) =
  Mod(polcoeff(subst(lift(f),q,1),index,p),modx);

alg_m2(h,R) =
{
  my(P=h*p^2, Q=h*q^2, A=jac(Q,R), B=-jac(P,R), cols);
  cols = [A,B];
  matrix(6,2,i,j,alg_coeff(cols[j],6-i));
};

alg_m1(h,R) =
{
  my(P=h*p^2, Q=h*q^2, A=jac(Q,R), B=-jac(P,R),
     G=jac(P,Q), cols);
  cols = [A*p,A*q,B*p,B*q,G];
  matrix(7,5,i,j,alg_coeff(cols[j],7-i));
};

alg_m0(h,R) =
{
  my(P=h*p^2, Q=h*q^2, A=jac(Q,R), B=-jac(P,R),
     G=jac(P,Q), cols);
  cols = [A*p^2,A*p*q,A*q^2,B*p^2,B*p*q,B*q^2,G*p,G*q];
  matrix(8,8,i,j,alg_coeff(cols[j],8-i));
};

ha = p^2 + et*p*q + q^2;
Ra = 8*p^2*q + 12*tt*p*q^2 + 12*q^3;
Aa = jac(ha*q^2,Ra);
Ba = -jac(ha*p^2,Ra);
Ga = jac(ha*p^2,ha*q^2);
ga = p*(p+tt*q);
check_zero(Aa-ga*(Aa/ga),"kappa=16/3 alpha divisibility");
check_zero(Ba-ga*(Ba/ga),"kappa=16/3 beta divisibility");
check_zero(Ga-ga*(Ga/ga),"kappa=16/3 gamma divisibility");
check_zero(gcd(gcd(lift(Aa/ga),lift(Ba/ga)),lift(Ga/ga))-8/3,"kappa=16/3 primitive reduced row");
if([matrank(alg_m2(ha,Ra)),matrank(alg_m1(ha,Ra)),matrank(alg_m0(ha,Ra))] != [2,4,6],error("FAIL: kappa=16/3 rank tuple"));
check_zero(alg_m1(ha,Ra)*[-et,-1,0,1,4]~,"kappa=16/3 literal kernel");
print("PASS PARI kappa=16/3 primitive row, ranks, and kernel");

\\ Symbolic replay of the two squarefree exceptional factors.
ss = 'ss;
aa = 'aa;
dd = 'dd;
LL = p-ss*q;
MM = ss*p-q;
hs = LL*MM;
Rtc = 4*ss*aa*p^3-3*(1+ss^2)*aa*p^2*q-3*(1+ss^2)*dd*p*q^2+4*ss*dd*q^3;
rootL = aa*ss^3-3*aa*ss-3*dd*ss^2+dd;
rootM = -3*aa*ss^2+aa+dd*ss^3-3*dd*ss;
expected = 648*(ss-1)^2*(ss+1)^2*(ss^2-4*ss+1)*(ss^2+4*ss+1)*rootM^2*rootL^2;
check_zero(matdet(vecextract(m1(hs,Rtc),[2,3,4,5,6],[1,2,3,4,5]))-expected,"two-contact squarefree determinant");

uu = 'uu;
Rrc = LL*(aa*p^2+(1-3*ss^2)*uu*p*q+4*ss*uu*q^2);
otherroot = aa+uu*ss^3+uu*ss;
chosenroot = -aa*ss+3*uu*ss^2-5*uu;
opposite = aa*ss^2-3*aa+12*uu*ss^3-4*uu*ss;
expected = 72*(ss-1)^2*(ss+1)^2*(ss^2-3)*otherroot^2*chosenroot*opposite;
check_zero(matdet(vecextract(m1(hs,Rrc),[1,2,3,4,5],[1,2,3,4,5]))-expected,"root-contact squarefree determinant");
print("PASS PARI squarefree exceptional determinant factors");

\\ Symbolic replay of the doubled-root exceptional coefficient.
av = 'av;
bv = 'bv;
dv = 'dv;
Rd = av*p^3+bv*p^2*q+(3*dv/2)*p*q^2+dv*q^3;
expected = 576*(3*av-2*bv)*(2*av-2*bv+dv)^2*(6*av-5*bv+3*dv);
check_zero(matdet(vecextract(m1((p+q)^2,Rd),[1,2,3,4,5],[1,2,3,4,5]))-expected,"doubled-root exceptional determinant");
print("PASS PARI doubled-root exceptional determinant factor");

print("ALL PARI DELTA=2 HILBERT--BURCH CHECKS PASSED");
