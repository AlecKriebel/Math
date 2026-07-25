\\ Independent PARI/GP checks for the fixed-divisor verticality principle.

x='x; y='y; z='z; s='s;
vars=[x,y,z];

gradmat(F)=matrix(3,3,i,j,deriv(F[i],vars[j]));
jac3(a,b,c)=matdet(gradmat([a,b,c]));
check(label,value)={
  if(value!=0,
    print(Str("FAIL ",label,": ",value));
    quit(1)
  );
  print(Str("  PASS ",label));
};

h=z^2;
p=x^2+y*z;
q=y^2+x*z;
P=h*p;
Q=h*q;

H4=[P,Q,0];
H3=[x^3+y^3,x^2*z+y*z^2,x^3+2*x*y*z+3*z^3];
H2=[x^2+y*z,y^2+x*z,z^2+x*y];
L=[x+y,y+z,z+x];
detseries=matdet(gradmat(L+s*H2+s^2*H3+s^3*H4));
check("weight-eight normal determinant", \
  polcoeff(detseries,8,s)-jac3(H4[1],H4[2],H3[3]));

\\ Reconstruct cubic normal kernels for one horizontal sample in each row.
mons3=[x^3,x^2*y,x^2*z,x*y^2,x*y*z,x*z^2,y^3,y^2*z,y*z^2,z^3];
mons8=vector(45);
k=1;
for(i=0,8,for(j=0,8-i,mons8[k]=x^i*y^j*z^(8-i-j);k++));
checkkernel(label,hh,pp,qq)={
  my(PP=hh*pp,QQ=hh*qq,M);
  M=matrix(45,10,i,j,
    polcoeff(
      polcoeff(
        polcoeff(jac3(PP,QQ,mons3[j]),poldegree(mons8[i],x),x),
        poldegree(subst(mons8[i],x,1),y),y),
      poldegree(subst(subst(mons8[i],x,1),y,1),z),z));
  if(matrank(M)!=10,
    print(Str("FAIL ",label," cubic kernel rank: ",matrank(M)));
    quit(1)
  );
  print(Str("  PASS ",label," cubic kernel rank 10"));
};

checkkernel("(e,a)=(1,3)",z,x^3+y*z^2,y^3+x*z^2);
checkkernel("(e,a)=(2,2)",z^2,x^2+y*z,y^2+x*z);
checkkernel("(e,a)=(3,1)",x^3+y*z^2,x,y);

\\ Vertical sharpness witness.
hv=z^2;
pv=z^2;
qv=x^2+y^2;
check("vertical cubic first integral", \
  jac3(hv*pv,hv*qv,z^3));

print("PASS: independent PARI/GP fixed-divisor verticality reconstruction");
quit
