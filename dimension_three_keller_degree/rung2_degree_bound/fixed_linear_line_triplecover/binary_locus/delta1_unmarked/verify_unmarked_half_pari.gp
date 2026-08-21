\\ Independent PARI/GP replay of the unmarked a3=1/2 contact family.

default(parisizemax,512000000);
allocatemem(128000000);

checkzero(value,message) =
{
  if(value != 0,
    print(Str("FAIL: ",message));
    quit(1)
  );
};
checktrue(value,message) =
{
  if(!value,
    print(Str("FAIL: ",message));
    quit(1)
  );
};
jac2(f,g) = deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
jac3(f,g,h) = matdet([deriv(f,p),deriv(f,q),deriv(f,r);deriv(g,p),deriv(g,q),deriv(g,r);deriv(h,p),deriv(h,q),deriv(h,r)]);
jacmap(V) = matrix(3,3,i,j,deriv(V[i],[p,q,r][j]));

{
A3=p*q^2+q^3/2;
B3=p^3+p^2*q-q^3/8;
P=p*A3;
Q=p*B3;
R=p^3+3*p^2*q/4+(4*z+1/8)*p*q^2+z*q^3;

alpha=jac2(Q,R);
beta=-jac2(P,R);
gam=jac2(P,Q);
checkzero(gam/q+p^2*(2*p+q)^2*(4*p+q)/2,
          "gamma exact-open factor");

Nu=(deriv(P,q)-deriv(P,p)/4)/q;
Nv=(deriv(Q,q)-deriv(Q,p)/4)/q;
Nt=(deriv(R,q)-deriv(R,p)/4)/q;
checkzero(alpha*Nu+beta*Nv+gam*Nt,"directional tangent syzygy");
curvature=jac3(P,r*Nv,r*Nt)
         +jac3(r*Nu,Q,r*Nt)
         +jac3(r*Nu,r*Nv,R);
K=polcoef(curvature,1,r);
checkzero(K-alpha/2+5*beta/32,"signed contact identity");
checktrue(K-alpha/2-5*beta/32 != 0,
          "contact wrong-sign mutation was not detected");

U0=u1*p^2*q+(3*u1/4+4*u3)*p*q^2+u3*q^3;
V0=-3*u1*p^2*q/8+(-u1/4+4*v3)*p*q^2+v3*q^3;
T0=(64*z-1)*u1*p*q/16;
U=U0+r*Nu;
V=V0+r*Nv;
T=T0+r*Nt;

x0=8*(-l13-2*u1*u3+2*x2);
x1=(-16*l13+u1^2-16*u1*u3+32*x2)/4;
y0=(-128*l23-u1^2-256*u1*v3+256*y2)/16;
y1=(-128*l23-3*u1^2-128*u1*v3+256*y2)/32;
A=x0*p^2+x1*p*q+x2*q^2+r*((u1/2+8*u3)*p+(-u1/8+2*u3)*q)-r^2/4;
B=y0*p^2+y1*p*q+y2*q^2+r*((-u1/8+8*v3)*p+(3*u1/64+2*v3)*q)+5*r^2/64;

l31=(64*l32+(64*z-1)*u1^2)/16;
l33=-(64*z-1)*u1/32;
L=[l11,l12,l13;l21,l22,l23;l31,l32,l33];
H2=[A,B,T];
H3=[U,V,R];
H4=[P,Q,0];
weighted=matdet(L+zz*jacmap(H2)+zz^2*jacmap(H3)+zz^3*jacmap(H4));

checkzero(polcoef(weighted,8,zz),"weighted E8");
checkzero(polcoef(weighted,7,zz),"weighted E7");
checkzero(polcoef(weighted,6,zz),"weighted E6");
checkzero(polcoef(weighted,5,zz),"weighted E5");

Az=(2048*z+112)*(p^4+p^3*q)+(576*z+30)*p^2*q^2+(32*z+1)*p*q^3-24*z*q^4;
Bz=384*(p^4+p^3*q)+(-512*z+104)*p^2*q^2+(-256*z+4)*p*q^3-96*z*q^4;
M1=l11-4*l12+2*u1*l13;
M2=l21-4*l22+2*u1*l23;
checkzero(polcoef(weighted,4,zz)-(Az*M1+Bz*M2)/256,
          "weighted E4 covariant collapse");
checkzero((32*z+1)*(-96*z)-(-24*z)*(-256*z+4)+9216*z^2,
          "E4 independence minor");

kernel=[1,-4,2*u1]~;
checkzero((L*kernel)[1]-M1,"first kernel covariant");
checkzero((L*kernel)[2]-M2,"second kernel covariant");
checkzero((L*kernel)[3],"third kernel identity");
checktrue(kernel[1] != 0,"kernel nonzero mutation");

print("PASS independent PARI unmarked half-family lower replay");
}
quit;
