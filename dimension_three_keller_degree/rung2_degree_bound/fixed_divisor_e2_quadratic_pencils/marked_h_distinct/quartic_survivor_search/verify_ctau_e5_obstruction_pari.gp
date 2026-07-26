\\ Independent PARI/GP reconstruction of the finite nonzero CTAU obstruction.

die(msg) = { print(Str("FAIL: ",msg)); quit(1); };
check(flag,msg) = { if(!flag,die(msg)); };
checkeq(got,want,msg) =
{
  if(got!=want,die(Str(msg,": got ",got,", want ",want)));
};

x='x; y='y; z='z; ww='ww; k='k;
A='A; B='B; T='T;
xyz=[x,y,z];

homexps(n) =
{
  my(out=List());
  forstep(i=n,0,-1,
    forstep(j=n-i,0,-1,listput(out,[i,j,n-i-j]))
  );
  Vec(out);
};

monoms(n) =
{
  my(exps=homexps(n));
  vector(#exps,i,x^exps[i][1]*y^exps[i][2]*z^exps[i][3]);
};

coeffxyz(f,e) =
{
  polcoeff(polcoeff(polcoeff(f,e[1],x),e[2],y),e[3],z);
};

checkhom(f,n,expected,label) =
{
  my(exps=homexps(n));
  for(i=1,#exps,
    my(got=coeffxyz(f,exps[i]), want=0);
    for(j=1,#expected,
      if(expected[j][1]==exps[i],want=expected[j][2])
    );
    checkeq(got,want,Str(label," exponent ",exps[i]));
  );
};

subst_many(f,vv,values) =
{
  my(g=f);
  check(#vv==#values,"subst_many length mismatch");
  for(i=1,#vv,g=subst(g,vv[i],values[i]));
  g;
};

jacvec(hh) = matrix(3,3,i,j,deriv(hh[i],xyz[j]));

m2=monoms(2);
aa=[a0,a1,a2,a3,a4,a5];
bb=[b0,b1,b2,b3,b4,b5];
ll=[l0,l1,l2,l3,l4,l5,l6,l7,l8];

h=x^2+y*z;
P=h^2;
Q=h*x^2;
R=x*(h+k*x^2);
H2=[sum(i=1,6,aa[i]*m2[i]),sum(i=1,6,bb[i]*m2[i]),T*x^2];
H3=[A*x^3,B*x^3,R];
H4=[P,Q,0];
L=matrix(3,3,i,j,ll[3*(i-1)+j]);
D=matdet(L+ww*jacvec(H2)+ww^2*jacvec(H3)+ww^3*jacvec(H4));

for(j=7,9,checkeq(polcoeff(D,j,ww),0,Str("top E",j)));

E6=polcoeff(D,6,ww);
expected6=[[[5,1,0],3*a1*k-a1-6*b1*k-2*b1+4*l7],[[5,0,1],-3*a2*k+a2+6*b2*k+2*b2-4*l8],[[4,2,0],2*(3*a3*k-a3-6*b3*k-2*b3)],[[4,0,2],-2*(3*a5*k-a5-6*b5*k-2*b5)],[[3,2,1],-a1-6*b1*k-4*b1+8*l7],[[3,1,2],a2+6*b2*k+4*b2-8*l8],[[2,3,1],-2*(a3+6*b3*k+4*b3)],[[2,1,3],2*(a5+6*b5*k+4*b5)],[[1,3,2],-2*(b1-2*l7)],[[1,2,3],2*(b2-2*l8)],[[0,4,2],-4*b3],[[0,2,4],4*b5]];
checkhom(E6,6,expected6,"E6");

ychain=subst_many(coeffxyz(E6,[5,1,0]),[b1,a1],[2*l7,-12*k*l7]);
zchain=subst_many(coeffxyz(E6,[5,0,1]),[b2,a2],[2*l8,-12*k*l8]);
checkeq(ychain,-36*k^2*l7,"E6 y saturation chain");
checkeq(zchain,36*k^2*l8,"E6 z saturation chain");

forced6=[a1,a2,a3,a5,b1,b2,b3,b5,l7,l8];
E5red=subst_many(polcoeff(D,5,ww),forced6,vector(#forced6));
expected5=[[[4,1,0],(3*k-1)*l1-(6*k+2)*l4],[[4,0,1],-(3*k-1)*l2+(6*k+2)*l5],[[2,2,1],-l1-(6*k+4)*l4],[[2,1,2],l2+(6*k+4)*l5],[[0,3,2],-2*l4],[[0,2,3],2*l5]];
checkhom(E5red,5,expected5,"reduced E5");

forced5=[l1,l2,l4,l5];
checkeq(subst_many(E5red,forced5,vector(#forced5)),0,"E5 vanishes after forced zeros");
checkeq(subst_many(subst_many(matdet(L),forced6,vector(#forced6)),forced5,vector(#forced5)),0,"forced linear part is singular");

q=9*k^2+6*k-1;
r=3*k-1;
checkeq(q/2-3*(k+1)*r/2,1,"E7 pivot-cover Bezout identity");
checkeq(polresultant(q,r,k),18,"E7 pivot-cover resultant");

print("CTAU_E5_PARI_PASS_91B027");
print("finite k != 0: independent determinant reconstruction forces det(L)=0");
quit;
