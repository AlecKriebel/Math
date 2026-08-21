\\ Independent PARI/GP replay of the full kappa=16 lower solve.

p='p; q='q; r='r; z='z;
vars=[p,q,r];

jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};
hc(f,degree,index)=polcoeff(subst(f,q,1),degree-index,p);

aa='aa; dd='dd; kk='kk; mm='mm; nn='nn; la='la;
u0='u0; u1='u1; u2='u2; u3='u3;
v0='v0; v1='v1; v2='v2; v3='v3;
tt0='tt0; tt1='tt1; tt2='tt2;
x0='x0; x1='x1; x2='x2; x3='x3; x4='x4; x5='x5;
y0='y0; y1='y1; y2='y2; y3='y3; y4='y4; y5='y5;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4;
l5='l5; l6='l6; l7='l7; l8='l8;

h=p^2+4*p*q+q^2;
R=aa*p^3+3*aa*p^2*q+3*dd*p*q^2+dd*q^3;
Nu=5*p+q;
Nv=-p-5*q;
Nt=3*(aa-dd);
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
E4=polcoeff(D,4,z);

check_zero(E8,"E8");
check_zero(E7,"E7");
C=(aa+2*dd)*(p^3+3*p^2*q)+(2*aa+dd)*(3*p*q^2+q^3);
check_zero(polcoeff(E6,3,r)-12*kk^2*C,"E6 r^3");
print("PASS PARI full E8/E7 and E6 r^3");

E6k=subst(E6,kk,0);
E6r=polcoeff(E6k,1,r);
check_zero(hc(E6r,5,0)-24*mm^2*(aa+2*dd),"E6 r p^5");
check_zero(hc(E6r,5,5)-24*nn^2*(2*aa+dd),"E6 r q^5");

E6high=substvec(E6,[kk,mm,nn,x5,y5],[0,0,0,0,0]);
E6sol=substvec(E6high,[x3,x4,y3,y4,l8],[5*la,la,-la,-5*la,3*(aa-dd)*la]);
check_zero(E6sol,"complete E6 kernel");
print("PASS PARI E6 endpoints and complete kernel");

E5high=substvec(E5,[kk,mm,nn,x5,y5,x3,x4,y3,y4,l8],[0,0,0,0,0,5*la,la,-la,-5*la,3*(aa-dd)*la]);
E5zero=subst(E5high,la,0);
Mzero=matrix(6,2,i,j,if(j==1,polcoeff(hc(E5zero,5,i-1),1,l2),polcoeff(hc(E5zero,5,i-1),1,l5)));
check_zero(matdet(vecextract(Mzero,[2,3],[1,2]))+288*aa*(aa+2*dd),"lambda zero first rank minor");
check_zero(matdet(vecextract(Mzero,[4,5],[1,2]))+288*dd*(2*aa+dd),"lambda zero second rank minor");
print("PASS PARI lambda-zero rank guards");

\\ Remaining a=d branch.  Substitute the exact E5 solution.
L2sol=la*(-3*u0/10+11*u1/10-7*u2/2+15*u3/2);
L5sol=la*(3*u0/2-u1/2+11*u2/2-33*u3/2+v1-3*v3);
V0sol=-u0/5+u1/15+v1/3;
V2sol=-5*u2+15*u3+3*v3;
commonvars=[dd,l2,l5,tt0,tt1,v0,v2];
commonvals=[aa,L2sol,L5sol,tt2,2*tt2,V0sol,V2sol];
E5done=substvec(E5high,commonvars,commonvals);
check_zero(E5done,"a=d complete E5 solve");
E4high=substvec(E4,[kk,mm,nn,x5,y5,x3,x4,y3,y4,l8],[0,0,0,0,0,5*la,la,-la,-5*la,3*(aa-dd)*la]);
E4done=substvec(E4high,commonvars,commonvals);
check_zero(polcoeff(E4done,1,r)-72*aa*la^2*(p+q)^3,"decisive E4 r coefficient");
print("PASS PARI a=d E5 solve and E4 contradiction");

print("ALL PARI KAPPA=16 DELTA=2 EXCLUSION CHECKS PASSED");
