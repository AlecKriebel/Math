\\ Independent exact PARI/GP check of the companion-moduli scope failure.

die(msg) = { print(Str("FAIL: ",msg)); quit(1); };
checkeq(got,want,msg) =
{
  if(got!=want,die(Str(msg,": got ",got,", want ",want)));
};

x='x; y='y; z='z; a='a; b='b; lam='lam; mu='mu;
vars=[x,y,z];

jacvec(hh) = matrix(3,3,i,j,deriv(hh[i],vars[j]));
jac3(f,g,h) = matdet(jacvec([f,g,h]));
conicmat(q) = matrix(3,3,i,j,deriv(deriv(q,vars[i]),vars[j])/2);
qrank(q) = matrank(conicmat(q));
subst3(f,X,Y,Z) = subst(subst(subst(f,x,X),y,Y),z,Z);

s=x^2;
rt=y*z;
ro=y^2+x*z;

checkeq(matdet(conicmat(a*s+b*rt)),-a*b^2/4,"rank-two discriminant");
checkeq(matdet(conicmat(a*s+b*ro)),-b^3/4,"rank-one discriminant");

checkeq(subst3(s,lam*x,y,z),lam^2*s,"rank-two scaling on s");
checkeq(subst3(rt,lam*x,y,z),rt,"rank-two scaling on r");
checkeq(subst3(ro,x,y,z+mu*x),ro+mu*s,"rank-one affine shear");
checkeq(subst3(ro,lam*x,y,z/lam),ro,"rank-one scaling on r");
checkeq(subst3(s,lam*x,y,z/lam),lam^2*s,"rank-one scaling on s");

checkeq(jac3(rt^2,rt*s,x*(a*rt+b*s)),0,"RT reducible full top line");
checkeq(jac3((s+rt)^2,(s+rt)*s,x*(a*(s+rt)+b*s)),0, \
  "RT smooth full top line");
checkeq(jac3(ro^2,ro*s,x*(a*ro+b*s)),0,"RO smooth full top line");

checkeq([qrank(s),qrank(rt),qrank(s+rt)],[1,2,3], \
  "RT reducible endpoint/mixed ranks");
checkeq(jac3(rt^2,rt*s,x*(s+rt)),0, \
  "RT reducible mixed top witness");
checkeq(jac3((s+rt)^2,(s+rt)*s,x*rt),0, \
  "RT smooth third-rank top witness");

print("PASS PARI companion moduli: endpoint exhaustion is false");
quit;
