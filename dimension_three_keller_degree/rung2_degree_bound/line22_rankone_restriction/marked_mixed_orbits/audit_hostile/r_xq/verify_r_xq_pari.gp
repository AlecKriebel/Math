\\ Independent exact hostile audit of the marked mixed orbit R=x*q.

die(msg) = { print(Str("FAIL: ",msg)); quit(1); };
check(flag,msg) = { if(!flag,die(msg)); };

xyz = [x,y,z];
p = x^2;
q = y^2+x*z;
P = p^2;
Q = q^2;
R = x*q;

jac3(f,g,h) =
{
  my(ff=[f,g,h]);
  matdet(matrix(3,3,i,j,deriv(ff[i],xyz[j])));
};

jacvec(hh) = matrix(3,3,i,j,deriv(hh[i],xyz[j]));

homexps(d) =
{
  my(L=List());
  forstep(i=d,0,-1,
    forstep(j=d-i,0,-1,
      listput(L,[i,j,d-i-j])
    )
  );
  Vec(L);
};

monoms(d) =
{
  my(E=homexps(d));
  vector(#E,i,x^E[i][1]*y^E[i][2]*z^E[i][3]);
};

coeffxyz(f,e) =
{
  polcoeff(polcoeff(polcoeff(f,e[1],x),e[2],y),e[3],z);
};

hcoeffs(f,d) =
{
  my(E=homexps(d));
  vector(#E,i,coeffxyz(f,E[i]));
};

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

is_affine_linear(f,d,vv) =
{
  my(cc=hcoeffs(f,d));
  for(i=1,#cc,
    my(rebuilt=zero_vars(cc[i],vv));
    for(j=1,#vv,rebuilt+=deriv(cc[i],vv[j])*vv[j]);
    if(cc[i]!=rebuilt,return(0));
  );
  1;
};

linear_system(f,d,vv) =
{
  my(cc=hcoeffs(f,d));
  my(M=matrix(#cc,#vv,i,j,deriv(cc[i],vv[j])));
  my(rhs=vector(#cc,i,-zero_vars(cc[i],vv))~);
  [M,rhs];
};

direction_column(direction) =
{
  concat(concat(hcoeffs(direction[1],3),hcoeffs(direction[2],3)),
         hcoeffs(direction[3],2))~;
};

print("PARI hostile R=xq audit: raw E7 kernel and gauge");

m3 = monoms(3);
m2 = monoms(2);
u = [u0,u1,u2,u3,u4,u5,u6,u7,u8,u9];
v = [v0,v1,v2,v3,v4,v5,v6,v7,v8,v9];
ww = [ww0,ww1,ww2,ww3,ww4,ww5];
rawvars = concat(concat(u,v),ww);
Uraw = sum(i=1,10,u[i]*m3[i]);
Vraw = sum(i=1,10,v[i]*m3[i]);
Wraw = sum(i=1,6,ww[i]*m2[i]);
check(jac3(P,Q,R)==0,"Jac(P,Q,R) is nonzero");
E7raw = jac3(P,Q,Wraw)+jac3(P,Vraw,R)+jac3(Uraw,Q,R);
check(is_affine_linear(E7raw,7,rawvars),"raw E7 is not linear in 26 unknowns");
sys7 = linear_system(E7raw,7,rawvars);
A7 = sys7[1];
b7 = sys7[2];
check(matsize(A7)==[36,26],"raw E7 matrix shape mismatch");
check(b7==vector(36)~,"raw E7 is not homogeneous");
check(matrank(A7)==18,"raw E7 rank is not 18");
rows7 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20];
cols7 = [2,3,5,6,7,8,9,10,12,13,15,16,17,18,19,20,25,26];
check(matdet(vecextract(A7,rows7,cols7))==-5343626510991360,"raw E7 fixed maximal minor mismatch");

translations = [[deriv(P,x),deriv(Q,x),deriv(R,x)],[deriv(P,y),deriv(Q,y),deriv(R,y)],[deriv(P,z),deriv(Q,z),deriv(R,z)]];
dirs = [[R,0,0],[0,R,0],translations[1],translations[2],translations[3],[0,x^3,0],[0,2*z*q,x*z],[0,-2*z*q,y^2]];
D7 = matrix(26,8,i,j,direction_column(dirs[j])[i]);
check(A7*D7==matrix(36,8),"a claimed raw E7 direction is not in the kernel");
check(matrank(D7)==8,"the eight raw E7 directions are dependent");
krows7 = [1,3,11,13,15,16,21,23];
check(matdet(vecextract(D7,krows7,vector(8,i,i)))==32,"raw kernel basis minor mismatch");
check(26-matrank(A7)==8,"raw E7 nullity is not eight");
normalcombo = vector(3,i,A*dirs[6][i]+w2*dirs[7][i]+w3*dirs[8][i]);
normaldisplay = [0,A*x^3+2*(w2-w3)*z*q,w2*x*z+w3*y^2];
check(normalcombo==normaldisplay,"three normal directions do not produce the displayed normal form");
print("PASS raw E7: rank 18/nullity 8 and complete five-gauge/three-normal basis");

print("PARI hostile R=xq audit: complete E6 solve");

d = w2-w3;
H3v = [0,A*x^3+2*d*z*q,R];
W2 = w2*x*z+w3*y^2;
a = [a0,a1,a2,a3,a4,a5];
b = [b0,b1,b2,b3,b4,b5];
ell = [l0,l1,l2,l3,l4,l5,l6,l7,l8];
H2v = [sum(i=1,6,a[i]*m2[i]),sum(i=1,6,b[i]*m2[i]),W2];
H4v = [P,Q,0];
Lmat = matrix(3,3,i,j,ell[3*(i-1)+j]);
weighted = matdet(Lmat+t*jacvec(H2v)+t^2*jacvec(H3v)+t^3*jacvec(H4v));
check(polcoeff(weighted,9,t)==0,"weighted determinant has nonzero E9");
check(polcoeff(weighted,8,t)==0,"weighted determinant has nonzero E8");
check(polcoeff(weighted,7,t)==0,"normal form has nonzero E7");

E6 = polcoeff(weighted,6,t);
vars6 = [a1,a2,a3,a4,a5,b1,b2,b3,b4,b5,l7,l8];
check(is_affine_linear(E6,6,vars6),"E6 is not affine linear in twelve claimed variables");
sys6 = linear_system(E6,6,vars6);
A6 = sys6[1];
b6 = sys6[2];
check(matsize(A6)==[28,12],"E6 matrix shape mismatch");
check(matrank(A6)==10,"E6 symbolic rank is not ten");
rows6 = [1,2,3,4,5,6,7,9,10,14];
cols6 = [1,2,4,5,6,7,9,10,11,12];
check(matdet(vecextract(A6,rows6,cols6))==-100663296,"E6 parameter-free maximal minor mismatch");

sol6 = [0,a3,a3,0,0,0,b3,b3,0,d^2,0,w3*d];
check(A6*sol6~==b6,"displayed E6 solution fails a coefficient equation");
ka6 = [0,1,1,0,0,0,0,0,0,0,0,0]~;
kb6 = [0,0,0,0,0,0,1,1,0,0,0,0]~;
check(A6*ka6==vector(28)~,"a3 is not a genuine E6 free direction");
check(A6*kb6==vector(28)~,"b3 is not a genuine E6 free direction");
check(matrank(matconcat([ka6,kb6]))==2,"E6 free directions are dependent");
check(12-matrank(A6)==2,"E6 nullity is not two");
check(subst_many(E6,vars6,sol6)==0,"full E6 converse substitution does not vanish");
print("PASS E6: constant rank ten and complete two-parameter affine solution");

print("PARI hostile R=xq audit: complete E5 solve and d=0 branch");

E5 = subst_many(polcoeff(weighted,5,t),vars6,sol6);
vars5 = [l1,l2,l4,l5];
check(is_affine_linear(E5,5,vars5),"E5 is not affine linear in four claimed variables");
sys5 = linear_system(E5,5,vars5);
A5 = sys5[1];
b5vec = sys5[2];
check(matsize(A5)==[21,4],"E5 matrix shape mismatch");
check(matrank(A5)==4,"E5 symbolic rank is not four");
rows5 = [1,2,6,9];
check(matdet(vecextract(A5,rows5,[1,2,3,4]))==256,"E5 parameter-free maximal minor mismatch");
sol5 = [0,a3*d,0,b3*d];
check(A5*sol5~==b5vec,"displayed E5 solution fails a coefficient equation");
check(subst_many(E5,vars5,sol5)==0,"full E5 converse substitution does not vanish");

\\ Recompute the resonant specialization d=0 directly, without cancellation.
A6d0 = subst(A6,w2,w3);
b6d0 = subst(b6,w2,w3);
sol6d0 = subst(sol6,w2,w3);
check(matrank(A6d0)==10,"E6 rank drops at d=0");
check(matdet(vecextract(A6d0,rows6,cols6))==-100663296,"E6 fixed minor changes at d=0");
check(A6d0*sol6d0~==b6d0,"specialized d=0 E6 solution fails");
check(subst(subst_many(E6,vars6,sol6),w2,w3)==0,"specialized d=0 E6 converse fails");

A5d0 = subst(A5,w2,w3);
b5d0 = subst(b5vec,w2,w3);
sol5d0 = subst(sol5,w2,w3);
check(matrank(A5d0)==4,"E5 rank drops at d=0");
check(matdet(vecextract(A5d0,rows5,[1,2,3,4]))==256,"E5 fixed minor changes at d=0");
check(sol5d0==[0,0,0,0],"d=0 does not specialize the E5 solution to zero");
check(A5d0*sol5d0~==b5d0,"specialized d=0 E5 solution fails");
check(subst(subst_many(E5,vars5,sol5),w2,w3)==0,"specialized d=0 E5 converse fails");
print("PASS d=0: both fixed ranks persist and the specialized converses vanish");

check(sol6[11]==0,"E6 does not force l32=0");
check(sol5[1]==0 && sol5[3]==0,"E5 does not force l12=l22=0");
check(subst_many(matdet(Lmat),[l1,l4,l7],[0,0,0])==0,"zero second column does not force det L=0");
check(matdet(Lmat)==l0*l4*l8-l0*l5*l7-l1*l3*l8+l1*l5*l6+l2*l3*l7-l2*l4*l6,"det L expansion mismatch");
print("PASS determinant exit: l12=l22=l32=0, including at d=0, so det(L)=0");
print("ALL HOSTILE PARI/GP R=xq AUDIT CHECKS PASSED");
quit(0);
