\\ Independent exact PARI/GP checks for the vertical cubic-pencil frontier.

x='x; y='y; z='z; t='t; T='T;
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

mons2=[z^2,y*z,y^2,x*z,x*y,x^2];
mons3=[z^3,y*z^2,y^2*z,y^3,x*z^2,x*y*z,x*y^2,x^2*z,x^2*y,x^3];
mons7=vector(36);
mons8=vector(45);
k=1;
for(i=0,7,for(j=0,7-i,mons7[k]=x^i*y^j*z^(7-i-j);k++));
k=1;
for(i=0,8,for(j=0,8-i,mons8[k]=x^i*y^j*z^(8-i-j);k++));

coeff3(poly,mon)={
  my(ix=poldegree(mon,x),iy=poldegree(subst(mon,x,1),y),iz=poldegree(subst(subst(mon,x,1),y,1),z));
  polcoeff(polcoeff(polcoeff(poly,ix,x),iy,y),iz,z)
};

kernelrank(p,q,d)={
  my(ms=if(d==2,mons2,mons3),outs=if(d==2,mons7,mons8),M);
  M=matrix(#outs,#ms,i,j,coeff3(jac3(z*p,z*q,ms[j]),outs[i]));
  [matrank(M),#ms-matrank(M)]
};

q=x^3+y^3;
plist=[z*x*y,z*(x*y+z^2),z*x^2,z*(x^2+z^2),z*(x^2+y*z),z^2*x,z^3];
expected2=[0,0,1,0,0,0,1];
expected3=[0,0,0,0,0,0,2];

for(i=1,#plist,{
  my(k2=kernelrank(plist[i],q,2),k3=kernelrank(plist[i],q,3));
  if(k2[2]!=expected2[i],
    print(Str("FAIL degree-two kernel ",i,": ",k2));
    quit(1)
  );
  if(k3[2]!=expected3[i],
    print(Str("FAIL degree-three kernel ",i,": ",k3));
    quit(1)
  );
  print(Str("  PASS representative ",i," kernels ",k2," / ",k3))
});

check("m1 square quadratic witness",jac3(z*(z*x^2),z*q,x*z));
check("m3 quadratic witness",jac3(z*z^3,z*q,z^2));
check("m3 vertical cubic witness",jac3(z*z^3,z*q,z^3));
check("m3 companion cubic witness",jac3(z*z^3,z*q,q));

H4=[z^4,z*q,0];
for(i=1,2,{
  my(normal=if(i==1,z^3,q),H3=[0,0,normal],series);
  series=matdet(matid(3)+T^2*gradmat(H3)+T^3*gradmat(H4));
  check(Str("survivor ",i," E8"),polcoeff(series,8,T));
  check(Str("survivor ",i," E7"),polcoeff(series,7,T));
  check(Str("survivor ",i," E6"),polcoeff(series,6,T));
  if(poldegree(series,T)>5,
    print(Str("FAIL survivor ",i," degree: ",poldegree(series,T)));
    quit(1)
  );
  if(series==1,
    print(Str("FAIL survivor ",i," accidentally Keller"));
    quit(1)
  );
  print(Str("  PASS survivor ",i," lower obstruction remains"))
});

expected=(1+3*T^2*z^2)*(1+3*T^3*y^2*z);
series=matdet(matid(3)+T^2*gradmat([0,0,z^3])+T^3*gradmat(H4));
check("factored vertical-companion determinant",series-expected);

H3=[q+4*z^3/3,0,z^3];
H2=[0,x*z,z^2];
series=matdet(matid(3)+T*gradmat(H2)+T^2*gradmat(H3)+T^3*gradmat(H4));
expected=(1+3*T^2*x^2)*(1+2*T*z+3*T^2*z^2);
check("E5-survivor determinant",series-expected);
check("E5-survivor E8",polcoeff(series,8,T));
check("E5-survivor E7",polcoeff(series,7,T));
check("E5-survivor E6",polcoeff(series,6,T));
check("E5-survivor E5",polcoeff(series,5,T));
check("E5-survivor nonzero E4",polcoeff(series,4,T)-9*x^2*z^2);

print("PASS: independent PARI/GP vertical cubic-pencil reconstruction");
quit
