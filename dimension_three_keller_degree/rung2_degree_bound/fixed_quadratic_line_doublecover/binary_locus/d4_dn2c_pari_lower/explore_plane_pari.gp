\\ Clean-room PARI/GP probe of one transverse D4-DN-2C contact plane.
\\ This script uses only the frozen contact atlas, reconstructs the full
\\ weighted determinant, and retains all nonpivot lower variables.

p='p; q='q; r='r; w='w;
coords=[p,q,r];

jacmat(H)=matrix(3,3,i,j,deriv(H[i],coords[j]));
c3(f,ip,iq,ir)=polcoeff(polcoeff(polcoeff(f,ir,r),iq,q),ip,p);
check_zero(value,message)=
{
  if(value!=0,
    print(Str("FAIL: ",message,"; residual = ",value));
    quit(1)
  )
};
check_true(value,message)=
{
  if(!value,
    print(Str("FAIL: ",message));
    quit(1)
  )
};

\\ Work over Q(eta), eta^2=-2.
ee='ee;
et=Mod(ee,ee^2+2);
k='k; s='s;

\\ Homogeneous lower coefficients.
u0='u0; u1='u1; u2='u2; u3='u3;
v0='v0; v1='v1; v2='v2; v3='v3;
t0='t0; t1='t1; t2='t2;
a0='a0; a1='a1; a2='a2; a3='a3; a4='a4; a5='a5;
b0='b0; b1='b1; b2='b2; b3='b3; b4='b4; b5='b5;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4; l5='l5;
l6='l6; l7='l7; l8='l8;

U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=t0*p^2+t1*p*q+t2*q^2;
A=a0*p^2+a1*p*q+a2*p*r+a3*q^2+a4*q*r+a5*r^2;
B=b0*p^2+b1*p*q+b2*p*r+b3*q^2+b4*q*r+b5*r^2;
L=[l0,l1,l2;l3,l4,l5;l6,l7,l8];

h=(p+q)^2;
P=h*p^2;
Q=h*q^2;
R=h*(p-2*q);
H4=[P,Q,0]~;

\\ Plus plane from the frozen atlas.  The minus plane is its eta-conjugate.
aa=k;
yy=s;
bb=-3*s/2;
xx=(-(4+2*et)*k+(3-3*et)*s)/9;
U1=(xx+4*aa/3)*p^2+(yy+2*xx+4*(aa+bb)/3)*p*q+(2*yy+4*bb/3)*q^2;
V1=xx*p*q+yy*q^2;
T1=aa*p+bb*q;

H3=[U0+r*U1,V0+r*V1,R]~;
H2=[A,B,T0+r*T1]~;
D=matdet(L+w*jacmat(H2)+w^2*jacmat(H3)+w^3*jacmat(H4));
check_zero(polcoeff(D,9,w),"E9");
check_zero(polcoeff(D,8,w),"E8");
check_zero(polcoeff(D,7,w),"E7 on plus plane");

E6=polcoeff(D,6,w);
E5=polcoeff(D,5,w);
E4=polcoeff(D,4,w);

low=[a2,a4,a5,b2,b4,b5,l8,u0,u1,u2,u3,v0,v1,v2,v3,t0,t1,t2];
zeros=vector(#low);
exps6=[[6,0,0],[5,1,0],[5,0,1],[4,2,0],[4,1,1],[3,3,0],[3,2,1],[2,4,0],[2,3,1],[1,5,0],[1,4,1],[0,6,0],[0,5,1]];
eq6=vector(#exps6,i,lift(c3(E6,exps6[i][1],exps6[i][2],exps6[i][3])));
M6=matrix(#eq6,#low,i,j,Mod(polcoeff(eq6[i],1,low[j]),ee^2+2));
rhs6=matrix(#eq6,1,i,j,Mod(-substvec(eq6[i],low,zeros),ee^2+2));
for(i=1,#eq6,{check_zero(eq6[i]-(M6*low~)[i]+rhs6[i,1],Str("E6 linear reconstruction row ",i))});

\\ Frozen plus-plane pivot: zero-based rows 0,1,2,3,4,5,7 and
\\ zero-based columns 0,1,2,3,5,7,8.
rows=[1,2,3,4,5,6,8];
pivcols=[1,2,3,4,6,8,9];
freecols=[5,7,10,11,12,13,14,15,16,17,18];
Mp=vecextract(M6,rows,pivcols);
Mf=vecextract(M6,rows,freecols);
bp=vector(#rows,i,rhs6[rows[i],1])~;
delta=2*k+3*s;
check_zero(matdet(Mp)-93312*(et-1)*delta^2,"frozen plus-plane pivot");
check_true(matrank(M6)==7,"E6 coefficient rank seven");
check_true(matrank(matconcat([M6,rhs6]))==7,"E6 augmented rank seven");

freevec=vector(#freecols,i,low[freecols[i]])~;
pivsol=matsolve(Mp,bp-Mf*freevec);
pivvars=vecextract(low,pivcols);
for(i=1,#eq6,{check_zero(substvec(eq6[i],pivvars,Vec(pivsol)),Str("complete E6 residual row ",i))});

E5s=substvec(E5,pivvars,Vec(pivsol));
E4s=substvec(E4,pivvars,Vec(pivsol));
alllower=[u0,u1,u2,u3,v0,v1,v2,v3,t0,t1,t2,a0,a1,a2,a3,a4,a5,b0,b1,b2,b3,b4,b5,l0,l1,l2,l3,l4,l5,l6,l7,l8];

print("DN2C_PLUS_E5_UNKNOWN_FREE_BEGIN");
c12=c3(E5s,1,2,2);
c21=c3(E5s,2,1,2);
c30=c3(E5s,3,0,2);
check_true(c12!=0 && c21!=0 && c30!=0,"three r^2 coefficients are nonzero");
for(j=1,#alllower,check_zero(deriv(c12,alllower[j]),Str("c12 lower-variable-free column ",j)));
for(j=1,#alllower,check_zero(deriv(c21,alllower[j]),Str("c21 lower-variable-free column ",j)));
for(j=1,#alllower,check_zero(deriv(c30,alllower[j]),Str("c30 lower-variable-free column ",j)));
print(Str("[1,2,2] ",lift(c12)));
print(Str("[2,1,2] ",lift(c21)));
print(Str("[3,0,2] ",lift(c30)));
print("DN2C_PLUS_E5_UNKNOWN_FREE_COUNT 3");

tt='tt;
g12=subst(subst(c12,k,1),s,tt);
g21=subst(subst(c21,k,1),s,tt);
g30=subst(subst(c30,k,1),s,tt);
gcommon=gcd(gcd(g12,g21),g30);
print(Str("DN2C_PLUS_E5_PROJECTIVE_GCD ",lift(gcommon)));
check_zero(gcommon-(tt/162+1/243),"plus-plane exact projective gcd");
check_zero(subst(c12,s,-2*k/3),"plus-plane c12 contains intersection factor");
check_zero(subst(c21,s,-2*k/3),"plus-plane c21 contains intersection factor");
check_zero(subst(c30,s,-2*k/3),"plus-plane c30 contains intersection factor");
check_true(subst(subst(c12,k,0),s,1)!=0,"plus-plane k=0 c12 nonzero");
check_true(subst(subst(c21,k,0),s,1)!=0,"plus-plane k=0 c21 nonzero");
check_true(subst(subst(c30,k,0),s,1)!=0,"plus-plane k=0 c30 nonzero");
g12m=Mod(subst(lift(g12),ee,-ee),ee^2+2);
g21m=Mod(subst(lift(g21),ee,-ee),ee^2+2);
g30m=Mod(subst(lift(g30),ee,-ee),ee^2+2);
gcommonm=gcd(gcd(g12m,g21m),g30m);
check_zero(gcommonm-(tt/162+1/243),"minus-plane conjugate projective gcd");
print(Str("DN2C_PLUS_E5_KZERO_VALUES ",lift(subst(subst(c12,k,0),s,1))," ",lift(subst(subst(c21,k,0),s,1))," ",lift(subst(subst(c30,k,0),s,1))));

\\ Print the two highest-r blocks compactly for pivot selection.
print("DN2C_PLUS_E5_R2_BEGIN");
for(ip=0,3,{iq=3-ip;value=c3(E5s,ip,iq,2);if(value!=0,print(Str("[",ip,",",iq,",2] ",lift(value))))});
print("DN2C_PLUS_E5_R1_BEGIN");
for(ip=0,4,{iq=4-ip;value=c3(E5s,ip,iq,1);if(value!=0,print(Str("[",ip,",",iq,",1] ",lift(value))))});

print("D4_DN2C_PLUS_PLANE_E5_PROBE_PASS");
print("D4_DN2C_TRANSVERSE_INTERIORS_E5_EXCLUDED");
quit(0);
