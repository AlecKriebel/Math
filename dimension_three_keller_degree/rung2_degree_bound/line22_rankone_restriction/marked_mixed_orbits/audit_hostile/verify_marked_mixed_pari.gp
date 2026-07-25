\\ Hostile independent exact audit of both marked-critical mixed orbits.

die(msg) = { print(Str("FAIL: ",msg)); quit(1); };
check(flag,msg) = { if(!flag,die(msg)); };

varsxyz=[x,y,z];
p=x^2; q=y^2+x*z; P=p^2; Q=q^2;

jac3(f,g,h) = {
  my(fs=[f,g,h]);
  matdet(matrix(3,3,i,j,deriv(fs[i],varsxyz[j])))
};

homexps(degree) = {
  my(out=List());
  forstep(i=degree,0,-1,
    forstep(j=degree-i,0,-1,
      listput(out,[i,j,degree-i-j])
    )
  );
  Vec(out)
};

monoms(degree) = {
  my(exps=homexps(degree));
  vector(#exps,i,x^exps[i][1]*y^exps[i][2]*z^exps[i][3])
};

coeffxyz(f,ex) =
  polcoeff(polcoeff(polcoeff(f,ex[1],x),ex[2],y),ex[3],z);

hcoeffs(f,degree) = {
  my(exps=homexps(degree));
  vector(#exps,i,coeffxyz(f,exps[i]))
};

zero_vars(f,vv) = {
  my(out=f);
  for(i=1,#vv,out=subst(out,vv[i],0));
  out
};

subst_many(f,vv,ww) = {
  my(out=f);
  check(#vv==#ww,"subst_many length mismatch");
  for(i=1,#vv,out=subst(out,vv[i],ww[i]));
  out
};

linear_system(f,degree,unknowns) = {
  my(coeffs=hcoeffs(f,degree));
  my(A=matrix(#coeffs,#unknowns,i,j,deriv(coeffs[i],unknowns[j])));
  my(b=vector(#coeffs,i,-zero_vars(coeffs[i],unknowns))~);
  [A,b]
};

is_affine_linear(f,degree,unknowns) = {
  my(coeffs=hcoeffs(f,degree));
  for(i=1,#coeffs,
    my(rebuilt=zero_vars(coeffs[i],unknowns));
    for(j=1,#unknowns,
      rebuilt+=deriv(coeffs[i],unknowns[j])*unknowns[j]
    );
    if(coeffs[i]!=rebuilt,return(0))
  );
  1
};

direction_column(direction) = \
  concat(concat(hcoeffs(direction[1],3),hcoeffs(direction[2],3)), \
    hcoeffs(direction[3],2))~;

m3=monoms(3); m2=monoms(2);
u=[u0,u1,u2,u3,u4,u5,u6,u7,u8,u9];
v=[v0,v1,v2,v3,v4,v5,v6,v7,v8,v9];
ww=[ww0,ww1,ww2,ww3,ww4,ww5];
Uraw=sum(i=1,10,u[i]*m3[i]);
Vraw=sum(i=1,10,v[i]*m3[i]);
Wraw=sum(i=1,6,ww[i]*m2[i]);
rawvars=concat(concat(u,v),ww);
rawrows=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20];
rawcols=[2,3,5,6,7,8,9,10,12,13,15,16,17,18,19,20,25,26];
kernelrows=[1,3,11,13,15,16,21,23];

raw_case(label,R,normals,normalweights,normaldisplay,kminor) = {
  my(E7=jac3(P,Q,Wraw)+jac3(P,Vraw,R)+jac3(Uraw,Q,R));
  check(jac3(P,Q,R)==0,Str(label,": E8 identity"));
  check(is_affine_linear(E7,7,rawvars),Str(label,": E7 raw linearity"));
  my(sys=linear_system(E7,7,rawvars),A=sys[1],b=sys[2]);
  check(matsize(A)==[36,26],Str(label,": E7 matrix shape"));
  check(b==vector(36)~,Str(label,": E7 homogeneous rhs"));
  check(matrank(A)==18,Str(label,": E7 rank"));
  check(matdet(vecextract(A,rawrows,rawcols))==-5343626510991360, \
    Str(label,": E7 fixed maximal minor"));

  my(tx=[deriv(P,x),deriv(Q,x),deriv(R,x)]);
  my(ty=[deriv(P,y),deriv(Q,y),deriv(R,y)]);
  my(tz=[deriv(P,z),deriv(Q,z),deriv(R,z)]);
  my(dirs=concat([[R,0,0],[0,R,0],tx,ty,tz],normals));
  my(K=matrix(26,8,i,j,direction_column(dirs[j])[i]));
  check(A*K==matrix(36,8),Str(label,": claimed E7 kernel directions"));
  check(matrank(K)==8,Str(label,": E7 kernel independence"));
  check(matdet(vecextract(K,kernelrows,[1..8]))==kminor, \
    Str(label,": E7 kernel minor"));
  check(26-matrank(A)==8,Str(label,": E7 nullity completeness"));

  my(normalcombo=vector(3,i, \
    sum(j=1,3,normalweights[j]*normals[j][i])));
  check(normalcombo==normaldisplay,Str(label,": gauge quotient normal form"));
  print(Str("PASS ",label, \
    " raw E7: complete five-gauge/three-normal kernel and exact quotient"));
};

Rother=x*q;
normalsother=[[0,x^3,0],[0,2*z*q,x*z],[0,-2*z*q,y^2]];
weightsother=[AA,w2,w3];
displayother=[0,AA*x^3+2*(w2-w3)*z*q,w2*x*z+w3*y^2];
raw_case("R=xq",Rother,normalsother,weightsother,displayother,32);

Rdistinct=x*(p-q);
normalsdistinct=[[0,0,p],[0,-2*z*q,x*z],[0,2*z*q,y^2]];
weightsdistinct=[w0,w2,w3];
displaydistinct=[0,2*(w3-w2)*z*q,w0*p+w2*x*z+w3*y^2];
raw_case("R=x(p-q)",Rdistinct,normalsdistinct,weightsdistinct, \
  displaydistinct,64);

a=[a0,a1,a2,a3,a4,a5];
b=[b0,b1,b2,b3,b4,b5];
ell=[l0,l1,l2,l3,l4,l5,l6,l7,l8];
Lmat=matrix(3,3,i,j,ell[3*(i-1)+j]);
H4v=[P,Q,0];
constrained=[a1,a2,a3,a4,a5,b1,b2,b3,b4,b5,l7,l8];
cols6=[1,2,4,5,6,7,9,10,11,12];
lastvars=[l1,l2,l4,l5];

jacvec(hh)=matrix(3,3,i,j,deriv(hh[i],varsxyz[j]));

lower_case(label,R,H3v,W2,sign,rows6,minor6,rows5,minor5) = {
  my(d=w2-w3);
  my(H2v=[ \
    sum(i=1,6,a[i]*m2[i]), \
    sum(i=1,6,b[i]*m2[i]), \
    W2]);
  my(weighted=matdet( \
    Lmat+t*jacvec(H2v)+t^2*jacvec(H3v)+t^3*jacvec(H4v)));
  check(polcoeff(weighted,9,t)==0,Str(label,": no E9"));
  check(polcoeff(weighted,8,t)==0,Str(label,": E8 vanishes"));
  check(polcoeff(weighted,7,t)==0,Str(label,": E7 normal form"));

  my(E6=polcoeff(weighted,6,t));
  check(is_affine_linear(E6,6,constrained),Str(label,": E6 linearity"));
  my(sys6=linear_system(E6,6,constrained));
  my(A6=sys6[1],b6=sys6[2]);
  check(matsize(A6)==[28,12],Str(label,": E6 matrix shape"));
  check(matrank(A6)==10,Str(label,": E6 rank"));
  check(matdet(vecextract(A6,rows6,cols6))==minor6, \
    Str(label,": E6 constant maximal minor"));
  check(matrank(subst(A6,w2,w3))==10, \
    Str(label,": E6 d=0 rank specialization"));

  my(sol6=[ \
    0,a3,a3,0,0, \
    0,b3,b3,0,d^2, \
    0,sign*w3*d]);
  check(A6*sol6~==b6,Str(label,": complete displayed E6 solution"));
  my(ka=[0,1,1,0,0,0,0,0,0,0,0,0]~);
  my(kb=[0,0,0,0,0,0,1,1,0,0,0,0]~);
  check(A6*ka==vector(28)~,Str(label,": E6 free a3 direction"));
  check(A6*kb==vector(28)~,Str(label,": E6 free b3 direction"));
  check(matrank(matconcat([ka,kb]))==2, \
    Str(label,": E6 free directions independent"));
  check(12-matrank(A6)==2,Str(label,": E6 kernel completeness"));
  check(subst_many(E6,constrained,sol6)==0,Str(label,": E6 converse"));
  check(subst(subst_many(E6,constrained,sol6),w2,w3)==0, \
    Str(label,": E6 d=0 converse"));

  my(E5=subst_many(polcoeff(weighted,5,t),constrained,sol6));
  check(is_affine_linear(E5,5,lastvars),Str(label,": E5 linearity"));
  my(sys5=linear_system(E5,5,lastvars));
  my(A5=sys5[1],b5=sys5[2]);
  check(matsize(A5)==[21,4],Str(label,": E5 matrix shape"));
  check(matrank(A5)==4,Str(label,": E5 rank"));
  check(matdet(vecextract(A5,rows5,[1..4]))==minor5, \
    Str(label,": E5 constant maximal minor"));
  check(matrank(subst(A5,w2,w3))==4, \
    Str(label,": E5 d=0 rank specialization"));

  my(sol5=[0,sign*a3*d,0,sign*b3*d]);
  check(A5*sol5~==b5,Str(label,": complete displayed E5 solution"));
  check(subst_many(E5,lastvars,sol5)==0,Str(label,": E5 converse"));
  check(subst(subst_many(E5,lastvars,sol5),w2,w3)==0, \
    Str(label,": E5 d=0 converse"));

  my(allvars=concat(constrained,lastvars));
  my(allsol=concat(sol6,sol5));
  check(subst_many(l1,allvars,allsol)==0,Str(label,": l12 exit"));
  check(subst_many(l4,allvars,allsol)==0,Str(label,": l22 exit"));
  check(subst_many(l7,allvars,allsol)==0,Str(label,": l32 exit"));
  check(subst_many(matdet(Lmat),allvars,allsol)==0, \
    Str(label,": det L zero-column exit"));
  print(Str("PASS ",label, \
    " E6/E5: complete constant-pivot converses, including d=0, and det L=0"));
};

H3other=[0,AA*x^3+2*(w2-w3)*z*q,Rother];
W2other=w2*x*z+w3*y^2;
lower_case("R=xq",Rother,H3other,W2other,1, \
  [1,2,3,4,5,6,7,9,10,14],-100663296, \
  [1,2,6,9],256);

H3distinct=[0,-2*(w2-w3)*z*q,Rdistinct];
W2distinct=w0*p+w2*x*z+w3*y^2;
lower_case("R=x(p-q)",Rdistinct,H3distinct,W2distinct,-1, \
  [1,2,3,4,5,6,7,8,9,12],2717908992, \
  [1,2,3,5],2304);

print("ALL HOSTILE PARI/GP MARKED-MIXED AUDIT CHECKS PASSED");
quit(0);
