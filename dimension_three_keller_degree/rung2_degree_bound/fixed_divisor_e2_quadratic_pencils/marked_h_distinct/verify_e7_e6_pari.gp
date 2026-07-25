\\ Independent exact PARI/GP reconstruction of the six marked-h-distinct
\\ E7 normal spaces, E6 compatibility systems, and through-E6 witnesses.

die(msg) = { print(Str("FAIL: ", msg)); quit(1); };
check(flag,msg) = { if(!flag,die(msg)); };
checkeq(got,want,msg) =
{
  if(got!=want,die(Str(msg, ": got ",got,", want ",want)));
};

x='x; y='y; z='z; t='t;
A='A; B='B; C='C; D='D; T='T; E='E; F='F; S='S;
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

hcoeffs(f,n) =
{
  my(exps=homexps(n));
  vector(#exps,i,coeffxyz(f,exps[i]));
};

jacvec(hh) = matrix(3,3,i,j,deriv(hh[i],xyz[j]));
jac3(f,g,h) = matdet(jacvec([f,g,h]));

zero_vars(f,vv) =
{
  my(g=f);
  for(i=1,#vv,g=subst(g,vv[i],0));
  g;
};

subst_many(f,vv,ww) =
{
  my(g=f);
  check(#vv==#ww,"subst_many length mismatch");
  for(i=1,#vv,g=subst(g,vv[i],ww[i]));
  g;
};

is_affine_linear(f,n,vv) =
{
  my(cc=hcoeffs(f,n));
  for(i=1,#cc,
    my(rebuilt=zero_vars(cc[i],vv));
    for(j=1,#vv,rebuilt+=deriv(cc[i],vv[j])*vv[j]);
    if(cc[i]!=rebuilt,return(0));
  );
  1;
};

linear_system(f,n,vv) =
{
  my(cc=hcoeffs(f,n));
  my(M=matrix(#cc,#vv,i,j,deriv(cc[i],vv[j])));
  my(rhs=vector(#cc,i,-zero_vars(cc[i],vv))~);
  [M,rhs];
};

vector_complement(n,indices) =
{
  my(out=List(),seen=Set(indices));
  for(i=1,n,if(!setsearch(seen,i),listput(out,i)));
  Vec(out);
};

pivot_solution(M,rhs,unknowns,rows,pivots) =
{
  my(free=vector_complement(#unknowns,pivots));
  my(square=vecextract(M,rows,pivots));
  my(freepart=if(#free,
    vecextract(M,rows,free)*vector(#free,i,unknowns[free[i]])~,
    vector(#rows)~));
  my(pivotvalues=matsolve(square,vecextract(rhs,rows)-freepart));
  my(sol=unknowns~);
  for(i=1,#pivots,sol[pivots[i]]=pivotvalues[i]);
  [sol,M*sol-rhs];
};

direction_column(direction) =
{
  concat(concat(hcoeffs(direction[1],3),hcoeffs(direction[2],3)),
         hcoeffs(direction[3],2))~;
};

is_rational_constant(v) =
{
  type(v)=="t_INT" || type(v)=="t_FRAC";
};

associate(a,b) =
{
  if(a==0 || b==0,return(a==0 && b==0));
  my(ratio=simplify(a/b));
  is_rational_constant(ratio) && a==ratio*b;
};

check_residual_generators(residual,targets,label) =
{
  my(seen=vector(#targets),nonzero=0);
  for(i=1,#residual,
    if(residual[i]!=0,
      nonzero++;
      my(hit=0);
      for(j=1,#targets,
        if(associate(residual[i],targets[j]),seen[j]=1;hit=1)
      );
      check(hit,Str(label,": unexpected residual ",residual[i]));
    )
  );
  check(nonzero>0,Str(label,": no compatibility residuals"));
  for(j=1,#targets,check(seen[j],Str(label,": missing target ",targets[j])));
};

m2=monoms(2);
m3=monoms(3);
aall=[a0,a1,a2,a3,a4,a5];
ball=[b0,b1,b2,b3,b4,b5];
ell=[l0,l1,l2,l3,l4,l5,l6,l7,l8];
alllower=concat(concat(aall,ball),ell);
Lmat=matrix(3,3,i,j,ell[3*(i-1)+j]);

weighted_determinant(P,Q,R,U,V,W) =
{
  my(H2=[sum(i=1,6,aall[i]*m2[i]),sum(i=1,6,ball[i]*m2[i]),W]);
  matdet(Lmat+t*jacvec(H2)+t^2*jacvec([U,V,R])
              +t^3*jacvec([P,Q,0]));
};

raw_case(label,h,R,U,V,W,pars,rank7,rows7,cols7,det7,krows,kdet) =
{
  my(P=h^2,Q=h*x^2);
  my(uu=[u0,u1,u2,u3,u4,u5,u6,u7,u8,u9]);
  my(vv=[v0,v1,v2,v3,v4,v5,v6,v7,v8,v9]);
  my(ww=[w0,w1,w2,w3,w4,w5]);
  my(rawvars=concat(concat(uu,vv),ww));
  my(U0=sum(i=1,10,uu[i]*m3[i]));
  my(V0=sum(i=1,10,vv[i]*m3[i]));
  my(W0=sum(i=1,6,ww[i]*m2[i]));
  my(E7=jac3(P,Q,W0)+jac3(P,V0,R)+jac3(U0,Q,R));
  check(is_affine_linear(E7,7,rawvars),Str(label,": raw E7 nonlinear"));
  my(sys=linear_system(E7,7,rawvars),M=sys[1],rhs=sys[2]);
  checkeq(matsize(M),[36,26],Str(label,": raw E7 shape"));
  checkeq(rhs,vector(36)~,Str(label,": raw E7 rhs"));
  checkeq(matrank(M),rank7,Str(label,": raw E7 rank"));
  checkeq(matdet(vecextract(M,rows7,cols7)),det7,
    Str(label,": raw E7 maximal minor"));

  my(trans=[[deriv(P,x),deriv(Q,x),deriv(R,x)],
            [deriv(P,y),deriv(Q,y),deriv(R,y)],
            [deriv(P,z),deriv(Q,z),deriv(R,z)]]);
  my(normals=vector(#pars,i,
    [deriv(U,pars[i]),deriv(V,pars[i]),deriv(W,pars[i])]));
  my(dirs=concat([[R,0,0],[0,R,0],trans[1],trans[2],trans[3]],normals));
  my(K=matrix(26,#dirs,i,j,direction_column(dirs[j])[i]));
  checkeq(M*K,matrix(36,#dirs),Str(label,": E7 directions not in kernel"));
  checkeq(#dirs,26-rank7,Str(label,": normal dimension"));
  checkeq(matrank(K),#dirs,Str(label,": legal basis rank"));
  checkeq(matdet(vecextract(K,krows,[1..#dirs])),kdet,
    Str(label,": legal basis constant minor"));
};

e6_case(label,h,R,U,V,W,pars,targets,rank6,rows6,cols6,det6,wantE5) =
{
  my(P=h^2,Q=h*x^2);
  my(weighted=weighted_determinant(P,Q,R,U,V,W));
  for(k=7,9,checkeq(polcoeff(weighted,k,t),0,Str(label,": E",k)));
  my(E6=polcoeff(weighted,6,t));
  check(is_affine_linear(E6,6,alllower),Str(label,": E6 nonlinear in lower data"));
  my(sys=linear_system(E6,6,alllower),M=sys[1],rhs=sys[2]);
  checkeq(matsize(M),[28,21],Str(label,": E6 shape"));
  checkeq(matrank(M),rank6,Str(label,": E6 rank"));
  checkeq(matdet(vecextract(M,rows6,cols6)),det6,
    Str(label,": E6 constant maximal minor"));
  my(solved=pivot_solution(M,rhs,alllower,rows6,cols6));
  check_residual_generators(solved[2],targets,Str(label,": E6"));

  my(loww=vector(21),parw=vector(#pars));
  loww[14]=1; loww[18]=1; loww[19]=1;
  my(witness=subst_many(subst_many(weighted,pars,parw),alllower,loww));
  checkeq(polcoeff(witness,0,t),1,Str(label,": witness det L"));
  for(k=6,9,checkeq(polcoeff(witness,k,t),0,Str(label,": witness E",k)));
  checkeq(polcoeff(witness,5,t),wantE5,Str(label,": sharp witness E5"));
  check(wantE5!=0,Str(label,": witness is not sharp"));
};

print("PARI exact reconstruction: marked-h-distinct E7/E6");

h1=y*z;
U1H=A*x^3-2*C*y^2*z-2*D*y*z^2;
V1H=B*x^3+C*x^2*y+D*x^2*z+2*E*x*y^2+2*F*x*z^2;
W1H=T*x^2+E*y^2+F*z^2;
U1S=A*x*y*z;
V1S=B*x*y*z+2*C*y^2*z/3+2*D*y*z^2/3;
W1S=C*x*y+D*x*z+T*y*z;

raw_case("RT-reducible/H",h1,x*y*z,U1H,V1H,W1H,[A,B,C,D,T,E,F], \
  14,[8,9,12,14,17,18,19,20,24,26,31,32,33,34], \
  [2,3,4,6,7,8,9,10,14,16,17,18,19,20],-82944, \
  [1,5,8,9,11,12,13,14,15,16,21,25],64);
e6_case("RT-reducible/H",h1,x*y*z,U1H,V1H,W1H,[A,B,C,D,T,E,F], \
  [A*C,A*D,A*E,A*F,C*E,D*F,E^2,F^2],8, \
  [8,9,12,14,18,19,24,26],[2,3,4,6,8,9,10,12],256, \
  -y^2*z*(x^2-2*z^2));

raw_case("RT-reducible/S",h1,x^3,U1S,V1S,W1S,[A,B,C,D,T], \
  16,[2,3,4,6,7,8,9,10,12,14,17,18,19,20,24,26], \
  [2,3,4,6,7,8,9,10,14,16,17,18,19,20,24,26],25389989167104, \
  [1,5,8,9,11,15,18,19,21,25],16/3);
e6_case("RT-reducible/S",h1,x^3,U1S,V1S,W1S,[A,B,C,D,T], \
  [C^2,D^2],10,[2,3,4,6,8,9,12,14,18,19], \
  [2,3,4,6,8,9,10,12,20,21],-26873856, \
  3*x^2*y*(x^2+2*z^2));

h2=x^2+y*z;
U2H=A*x^3-2*C*y*h2-2*D*z*h2;
V2H=B*x^3+C*x^2*y+D*x^2*z+2*E*x*y^2+2*F*x*z^2;
W2H=T*x^2+E*y^2+F*z^2;
U2S=A*x*y*z-4*C*y*h2/3-4*D*z*h2/3;
V2S=B*x*y*z+2*C*y^2*z/3+2*D*y*z^2/3;
W2S=C*x*y+D*x*z+T*y*z;

raw_case("RT-smooth/H",h2,x*h2,U2H,V2H,W2H,[A,B,C,D,T,E,F], \
  14,[2,3,4,6,7,8,9,10,12,14,17,18,19,20], \
  [2,3,4,6,7,8,9,10,14,16,17,18,19,20],-82944, \
  [1,2,3,5,11,12,13,14,15,16,21,25],64);
e6_case("RT-smooth/H",h2,x*h2,U2H,V2H,W2H,[A,B,C,D,T,E,F], \
  [A*C,A*D,A*E,A*F,C*E,D*F,E^2,F^2],8, \
  [2,3,4,6,8,9,12,14],[2,3,4,6,8,9,10,12],256, \
  -h2*(x^2*y-2*x^2*z-2*y*z^2));

raw_case("RT-smooth/S",h2,x^3,U2S,V2S,W2S,[A,B,C,D,T], \
  16,[2,3,4,6,7,8,9,10,12,14,17,18,19,20,24,26], \
  [2,3,4,6,7,8,9,10,14,16,17,18,19,20,24,26],25389989167104, \
  [1,2,3,5,11,12,13,15,21,25],16/3);
e6_case("RT-smooth/S",h2,x^3,U2S,V2S,W2S,[A,B,C,D,T], \
  [C^2,D^2],10,[2,3,4,6,8,9,12,14,18,19], \
  [2,3,4,6,8,9,10,12,20,21],-26873856, \
  3*x^2*(x^2*y+2*x^2*z+2*y*z^2));

h3=y^2+x*z;
U3H=A*x^3-2*C*y*h3-2*D*z*h3+2*T*z*h3;
V3H=B*x^3+C*x^2*y+(D+T)*x^2*z+2*E*x*y*z+2*F*x*z^2;
W3H=T*x*z+E*y*z+F*z^2;
U3S=2*A*z*h3;
V3S=A*x^2*z+B*x*h3+2*C*y*h3/3+2*D*z*h3/3;
W3S=C*x*y+S*h3+D*x*z;

raw_case("RO-smooth/H",h3,x*h3,U3H,V3H,W3H,[A,B,C,D,T,E,F], \
  14,[3,5,6,8,9,10,12,13,14,15,17,18,20,23], \
  [2,3,5,6,7,8,9,10,15,16,17,18,19,20],-13271040, \
  [1,3,5,6,11,12,13,14,15,16,21,23],-128);
e6_case("RO-smooth/H",h3,x*h3,U3H,V3H,W3H,[A,B,C,D,T,E,F], \
  [A*C,A*D,A*E,A*F,C*F+D*E,E*F,2*D*F-E^2,F^2],8, \
  [3,5,6,8,9,10,12,14],[2,3,5,6,8,9,11,12],3072, \
  -h3*(x^3-4*x*y*z-4*y^3));

raw_case("RO-smooth/S",h3,x^3,U3S,V3S,W3S,[A,B,C,D,S], \
  16,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,18], \
  [2,3,5,6,7,8,9,10,15,16,17,18,19,20,25,26],12187194800209920, \
  [1,3,5,6,11,13,15,16,21,23],64/3);
e6_case("RO-smooth/S",h3,x^3,U3S,V3S,W3S,[A,B,C,D,S], \
  [C*D,D^2],10,[1,2,3,4,5,6,7,8,9,12], \
  [2,3,5,6,8,9,11,12,20,21],1934917632, \
  3*x^2*(x^3+4*x*y*z+4*y^3));

print("PASS PARI: all six marked-h-distinct E7/E6 branches");
quit;
