\\ Independent PARI/GP replay of the full kappa=16/3 lower solve.

p='p; q='q; r='r; z='z;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};
hc(f,degree,index)=polcoeff(subst(f,q,1),degree-index,p);

aa='aa; bb='bb; kk='kk; mm='mm; nn='nn; la='la;
u0='u0; u1='u1; u2='u2; u3='u3;
v0='v0; v1='v1; v2='v2; v3='v3;
tt0='tt0; tt1='tt1; tt2='tt2;
x0='x0; x1='x1; x2='x2; x3='x3; x4='x4; x5='x5;
y0='y0; y1='y1; y2='y2; y3='y3; y4='y4; y5='y5;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4;
l5='l5; l6='l6; l7='l7; l8='l8;

h=(p+q)*(3*p+q);
R=(p+q)*(aa*p^2+2*bb*p*q+bb*q^2);
Nu=4*p+q;
Nv=-3*q;
Nt=aa-bb;
W=mm*p+nn*q;
S=kk*r^2/2+W*r;
U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=tt0*p^2+tt1*p*q+tt2*q^2;
A0=x0*p^2+x1*p*q+x2*q^2;
B0=y0*p^2+y1*p*q+y2*q^2;
H4=[h*p^2,h*q^2,0]~;
H3=[U0+Nu*S,V0+Nv*S,R]~;
H2=[A0+r*(x3*p+x4*q)+x5*r^2,B0+r*(y3*p+y4*q)+y5*r^2,T0+Nt*S]~;
L0=[l0,l1,l2;l3,l4,l5;l6,l7,l8];
D=matdet(L0+z*jacmat(H2)+z^2*jacmat(H3)+z^3*jacmat(H4));
E8=polcoeff(D,8,z);
E7=polcoeff(D,7,z);
E6=polcoeff(D,6,z);
E5=polcoeff(D,5,z);
check_zero(E8,"E8");
check_zero(E7,"E7");
expected=6*kk^2*(p+q)*(2*aa*p*q+aa*q^2+3*bb*p^2+4*bb*p*q+2*bb*q^2);
check_zero(polcoeff(E6,3,r)-expected,"E6 r^3");
print("PASS PARI full E8/E7 and E6 r^3");

E6r=polcoeff(subst(E6,kk,0),1,r);
check_zero(hc(E6r,5,0)+12*bb*(-3*mm^2+4*y5),"E6 r p^5");
check_zero(hc(E6r,5,5)-12*nn^2*(aa+2*bb),"E6 r q^5");
special=substvec(E6r,[aa,y5],[-2*bb,3*mm^2/4]);
check_zero(hc(special,5,4)-3*bb*(-3*mm^2+4*x5),"special E6 coefficient");
check_zero(hc(special,5,3)-3*bb*(-21*mm^2+12*nn^2+28*x5),"special E6 second coefficient");
print("PASS PARI E6 r endpoint mutations");

E6high=substvec(E6,[kk,mm,nn,x5,y5],[0,0,0,0,0]);
E6done=substvec(E6high,[x3,x4,y3,y4,l8],[4*la,la,0,-3*la,(aa-bb)*la]);
check_zero(E6done,"complete E6 kernel");

E5high=substvec(E5,[kk,mm,nn,x5,y5,x3,x4,y3,y4,l8],[0,0,0,0,0,4*la,la,0,-3*la,(aa-bb)*la]);
E5zero=subst(E5high,la,0);
Mzero=matrix(6,2,i,j,if(j==1,polcoeff(hc(E5zero,5,i-1),1,l2),polcoeff(hc(E5zero,5,i-1),1,l5)));
check_zero(matdet(vecextract(Mzero,[1,2],[1,2]))+432*aa*bb,"lambda zero first rank minor");
check_zero(matdet(vecextract(Mzero,[4,5],[1,2]))+144*bb*(aa+2*bb),"lambda zero second rank minor");
print("PASS PARI complete E6 kernel and lambda-zero rank guards");

print("ALL PARI KAPPA=16/3 DELTA=2 EXCLUSION CHECKS PASSED");
