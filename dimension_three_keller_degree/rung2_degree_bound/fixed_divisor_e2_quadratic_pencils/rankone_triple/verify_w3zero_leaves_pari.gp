\\ Independent PARI/GP recomputation of the A != 0, w3 = 0 leaves.

die(msg) = { print(Str("FAIL: ",msg)); quit(1); };
check(flag,msg) = { if(!flag,die(msg)); };
checkeq(got,want,msg) =
{
  if(got!=want,die(Str(msg,": got ",got,", want ",want)));
};

xyz=[x,y,z];
jacvec(hh)=matrix(3,3,i,j,deriv(hh[i],xyz[j]));

weighted(U,V,W,H21,H22,LL) =
{
  my(H4=[x^4,x^2*(y^2+x*z),0]);
  my(H3=[U,V,x^3],H2=[H21,H22,W]);
  matdet(LL+t*jacvec(H2)+t^2*jacvec(H3)+t^3*jacvec(H4));
};

coeffxyz(f,i,j,k)=polcoeff(polcoeff(polcoeff(f,i,x),j,y),k,z);

check_top_e5(detpoly,label) =
{
  for(k=5,9,checkeq(polcoeff(detpoly,k,t),0,Str(label," E",k)));
};

print("PARI audit: C3-open w3=0 leaf");
A3=A3; c03=c03; c13=c13; c23=c23; c33=c33;
r3=r3; be3=be3; et3=et3; ga3=ga3;
a03=a03; b03=b03;
l03=l03; l33=l33; l43=l43; l53=l53; l63=l63;
d3=c03-c13;
u3=A3*x*(y^2+x*z);
v3=c03*x^2*z+c13*x*y^2+c23*x*y*z+c33*x*z^2;
h213=a03*x^2+A3*(c03-r3)*x*z+A3*(c13-r3)*y^2+ \
      A3*c23*y*z+A3*c33*z^2;
h223=b03*x^2+be3*x*y+(ga3+d3*r3+et3)*x*z+ga3*y^2+ \
      c23*r3*y*z+c33*r3*z^2;
L3=[l03,A3*be3,A3*et3;l33,l43,l53;l63,0,0];
wd3=weighted(u3,v3,0,h213,h223,L3);
check_top_e5(wd3,"C3-open");
E43=polcoeff(wd3,4,t);
S3=c13*r3-ga3-r3^2;
e03=coeffxyz(E43,4,0,0);
e13=coeffxyz(E43,3,1,0);
es3=coeffxyz(E43,2,1,1);
checkeq(e03,-3*A3*(l43-r3*be3),"C3-open [x^4]E4");
checkeq(e13,6*A3*(d3*S3+l53-r3*et3),"C3-open [x^3y]E4");
checkeq(es3,12*A3*c33*S3,"C3-open [x^2yz]E4");
cert3=l63*(2*c33*L3[1,2]*e13-d3*L3[1,2]*es3+ \
            4*c33*L3[1,3]*e03);
checkeq(12*A3*c33*matdet(L3),cert3,"C3-open determinant identity");
print("PASS C3-open leaf");

print("PARI audit: C2-open w3=0 leaf");
A2=A2; c02=c02; c12=c12; c22=c22;
r2=r2; be2=be2; et2=et2; ga2=ga2;
a02=a02; b02=b02;
l02=l02; l32=l32; l42=l42; l52=l52; l62=l62;
d2=c02-c12;
u2=A2*x*(y^2+x*z);
v2=c02*x^2*z+c12*x*y^2+c22*x*y*z;
h212=a02*x^2+A2*(c02-r2)*x*z+A2*(c12-r2)*y^2+ \
      A2*c22*y*z;
h222=b02*x^2+be2*x*y+(ga2+d2*r2+et2)*x*z+ga2*y^2+ \
      c22*r2*y*z;
L2=[l02,A2*be2,A2*et2;l32,l42,l52;l62,0,0];
wd2=weighted(u2,v2,0,h212,h222,L2);
check_top_e5(wd2,"C2-open");
E42=polcoeff(wd2,4,t);
S2=c12*r2-ga2-r2^2;
e02=coeffxyz(E42,4,0,0);
e12=coeffxyz(E42,3,1,0);
es2=coeffxyz(E42,3,0,1);
checkeq(e02,-3*A2*(l42-r2*be2),"C2-open [x^4]E4");
checkeq(e12,6*A2*(d2*S2+l52-r2*et2),"C2-open [x^3y]E4");
checkeq(es2,-3*A2*c22*S2,"C2-open [x^3z]E4");
cert2=l62*(c22*L2[1,2]*e12+2*d2*L2[1,2]*es2+ \
            2*c22*L2[1,3]*e02);
checkeq(6*A2*c22*matdet(L2),cert2,"C2-open determinant identity");
print("PASS C2-open leaf");

print("PARI audit: fully aligned w3=0 leaf, uniformly in D");
Aa=Aa; ca=ca; da=da; ro=ro; bea=bea; eaa=eaa; gaa=gaa;
a0a=a0a; b0a=b0a;
l0a=l0a; l3a=l3a; l4a=l4a; l5a=l5a; l6a=l6a;
ua=Aa*x*(y^2+x*z);
va=(ca+da)*x^2*z+ca*x*y^2;
h21a=a0a*x^2+Aa*(da+ro)*x*z+Aa*ro*y^2;
h22a=b0a*x^2+bea*x*y+(gaa-da*(ro-ca)+eaa)*x*z+gaa*y^2;
Laa=[l0a,Aa*bea,Aa*eaa;l3a,l4a,l5a;l6a,0,0];
wda=weighted(ua,va,0,h21a,h22a,Laa);
check_top_e5(wda,"aligned");
E4a=polcoeff(wda,4,t);
Sa=ca*ro-gaa-ro^2;
e0a=coeffxyz(E4a,4,0,0);
e1a=coeffxyz(E4a,3,1,0);
checkeq(e0a,-3*Aa*(l4a+(ro-ca)*bea),"aligned [x^4]E4");
checkeq(e1a,6*Aa*(l5a+(ro-ca)*eaa+da*Sa),"aligned [x^3y]E4");
checkeq(E4a,e0a*x^4+e1a*x^3*y,"aligned complete E4 support");

sol4a=subst(subst(wda,l4a,-(ro-ca)*bea), \
             l5a,-(ro-ca)*eaa-da*Sa);
E3a=polcoeff(sol4a,3,t);
e30a=coeffxyz(E3a,3,0,0);
e21a=coeffxyz(E3a,2,1,0);
checkeq(e30a,-3*Aa*bea*Sa,"aligned [x^3]E3");
checkeq(e21a,-6*Aa*(da*ro-eaa)*Sa,"aligned [x^2y]E3");
checkeq(E3a,e30a*x^3+e21a*x^2*y,"aligned complete E3 support");
detLa=subst(subst(matdet(Laa),l4a,-(ro-ca)*bea), \
             l5a,-(ro-ca)*eaa-da*Sa);
checkeq(3*detLa,da*l6a*e30a,"aligned determinant identity");
print("PASS aligned leaf");

print("all independent PARI w3=0 leaf certificates passed");
quit(0);
