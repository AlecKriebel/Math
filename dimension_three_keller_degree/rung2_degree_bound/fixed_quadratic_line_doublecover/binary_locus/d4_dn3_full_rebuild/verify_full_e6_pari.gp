\\ Independent PARI/GP replay of the D4-DN-3 full-lower E6 atlas.

p='p; q='q; r='r; ww='ww;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
jac2(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};
check_true(value,message)={if(!value,error(Str("FAIL: ",message)))};
coef3(f,ip,iq,ir)=polcoeff(polcoeff(polcoeff(f,ir,r),iq,q),ip,p);

h=(p+q)^2;
P=h*p^2;
Q=h*q^2;
R=(p+q)^3;
H4=[P,Q,0]~;
alpha=jac2(Q,R);
beta=-jac2(P,R);
gam=jac2(P,Q);
check_zero(alpha+6*q*(p+q)^4,"alpha");
check_zero(beta+6*p*(p+q)^4,"beta");
check_zero(gam-8*p*q*(p+q)^4,"gamma");

dd='dd; zet='zet; xx='xx; yy='yy; aaa='aaa; bbb='bbb;
U2=(4*zet-3*dd)*p/3;
V2=dd*q;
T2=zet;
U1=(4*aaa-3*xx)*p^2/3+(4*bbb-3*yy)*p*q/3;
V1=xx*p*q+yy*q^2;
T1=aaa*p+bbb*q;
check_zero(alpha*U2+beta*V2+gam*T2,"complete E7 r-linear block");
check_zero(alpha*U1+beta*V1+gam*T1,"complete E7 constant block");

H3c=[r*U1+r^2*U2,r*V1+r^2*V2,R]~;
H2c=[0,0,r*T1+r^2*T2]~;
Dc=matdet(ww*jacmat(H2c)+ww^2*jacmat(H3c)+ww^3*jacmat(H4));
E6r3=polcoeff(polcoeff(Dc,6,ww),3,r);
expectedr3=2*(-3*dd+4*zet)^2*q^3/3+2*(9*dd^2-16*dd*zet+8*zet^2)*p*q^2+2*(27*dd^2-24*dd*zet+8*zet^2)*p^2*q/3+6*dd^2*p^3;
check_zero(E6r3-expectedr3,"E6 r^3 forces r^2 contact zero");

\\ Number field for the two geometric planes.
rr='rr;
rt=Mod(rr,rr^2-2);
ss='ss; kk='kk;
cplus=(-4+2*rt)/3;
Uplus=(4*kk-3*(ss+cplus*kk))*p^2/3+(4*kk-3*ss)*p*q/3;
Vplus=(ss+cplus*kk)*p*q+ss*q^2;
Tplus=kk*(p+q);

\\ All eighteen lower variables, including all eleven binary coefficients.
u0='u0;u1='u1;u2='u2;u3='u3;
v0='v0;v1='v1;v2='v2;v3='v3;
t0='t0;t1='t1;t2='t2;
a0='a0;a1='a1;a2='a2;a3='a3;a4='a4;a5='a5;
b0='b0;b1='b1;b2='b2;b3='b3;b4='b4;b5='b5;
l0='l0;l1='l1;l2='l2;l3='l3;l4='l4;l5='l5;l6='l6;l7='l7;l8='l8;
U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=t0*p^2+t1*p*q+t2*q^2;
A=a0*p^2+a1*p*q+a2*p*r+a3*q^2+a4*q*r+a5*r^2;
B=b0*p^2+b1*p*q+b2*p*r+b3*q^2+b4*q*r+b5*r^2;
L0=[l0,l1,l2;l3,l4,l5;l6,l7,l8];
H3=[U0+r*Uplus,V0+r*Vplus,R]~;
H2=[A,B,T0+r*Tplus]~;
Dfull=matdet(L0+ww*jacmat(H2)+ww^2*jacmat(H3)+ww^3*jacmat(H4));
check_zero(polcoeff(Dfull,7,ww),"full E7");
E6=polcoeff(Dfull,6,ww);
low=[a2,a4,a5,b2,b4,b5,l8,u0,u1,u2,u3,v0,v1,v2,v3,t0,t1,t2];
zeros=vector(18);
exps=[[6,0,0],[5,1,0],[5,0,1],[4,2,0],[4,1,1],[3,3,0],[3,2,1],[2,4,0],[2,3,1],[1,5,0],[1,4,1],[0,6,0],[0,5,1]];
eq=vector(13,i,lift(coef3(E6,exps[i][1],exps[i][2],exps[i][3])));
M=matrix(13,18,i,j,Mod(polcoeff(eq[i],1,low[j]),rr^2-2));
rhs=matrix(13,1,i,j,Mod(-substvec(eq[i],low,zeros),rr^2-2));
Aug=matconcat([M,rhs]);

rows7=[1,2,3,4,5,6,8];
cols7=[1,2,3,4,6,8,9];
pivot7=matdet(vecextract(M,rows7,cols7));
check_zero(pivot7-373248*(7-5*rt)*kk^2,"k-nonzero seven-pivot");
check_true(matrank(M)==7,"generic full-lower rank seven");
check_true(matrank(Aug)==7,"generic full-lower consistency");

Minter=subst(M,kk,0);
rhsinter=subst(rhs,kk,0);
Auginter=matconcat([Minter,rhsinter]);
rows6=[1,2,3,4,5,6];
cols6=[1,2,3,4,6,8];
check_zero(matdet(vecextract(Minter,rows6,cols6))+279936*ss,"intersection six-pivot");
check_true(matrank(Minter)==6,"intersection rank six");
check_true(matrank(Auginter)==6,"intersection consistency");

Morigin=subst(Minter,ss,0);
rhsorigin=subst(rhsinter,ss,0);
Augorigin=matconcat([Morigin,rhsorigin]);
rows5=[1,2,3,4,5];
cols5=[1,2,3,4,6];
check_zero(matdet(vecextract(Morigin,rows5,cols5))-31104,"origin five-pivot");
check_true(matrank(Morigin)==5,"origin rank five");
check_true(matrank(Augorigin)==5,"origin consistency");

\\ The conjugate plane is obtained by the nontrivial field automorphism.
pivotminus=Mod(subst(lift(pivot7),rr,-rr),rr^2-2);
check_zero(pivotminus-373248*(7+5*rt)*kk^2,"conjugate plane pivot");

print("D4_DN3_PARI_FULL_18_LOWER_ATLAS_PASS");
quit(0);
