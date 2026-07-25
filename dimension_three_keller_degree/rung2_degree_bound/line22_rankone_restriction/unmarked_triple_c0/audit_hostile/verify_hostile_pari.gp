\\ Hostile independent exact audit of the unmarked triple-companion c=0 orbit.
\\ This script deliberately reconstructs the coefficient systems in PARI/GP.

die(msg) = { print(Str("FAIL: ", msg)); quit(1); };
check(flag, msg) = { if(!flag, die(msg)); };

varsxyz = [x, y, z];
p = x^2;
q = y^2 + x*z;
P = (p-q)^2;
Q = (p+q)^2;
R = x^3;

jac3(f,g,h) =
{
  my(fs=[f,g,h]);
  matdet(matrix(3,3,i,j,deriv(fs[i],varsxyz[j])));
};

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

zero_vars(f, vv) =
{
  my(g=f);
  for(i=1,#vv,g=subst(g,vv[i],0));
  g;
};

subst_many(f, vv, ww) =
{
  my(g=f);
  check(#vv==#ww, "subst_many length mismatch");
  for(i=1,#vv,g=subst(g,vv[i],ww[i]));
  g;
};

linear_system(f,d,unknowns) =
{
  my(c=hcoeffs(f,d));
  my(A=matrix(#c,#unknowns,i,j,deriv(c[i],unknowns[j])));
  my(b=vector(#c,i,-zero_vars(c[i],unknowns))~);
  [A,b];
};

is_affine_linear(f,d,unknowns) =
{
  my(c=hcoeffs(f,d));
  for(i=1,#c,
    my(rebuilt=zero_vars(c[i],unknowns));
    for(j=1,#unknowns,rebuilt+=deriv(c[i],unknowns[j])*unknowns[j]);
    if(c[i]!=rebuilt,return(0));
  );
  1;
};

direction_column(direction) =
{
  concat(concat(hcoeffs(direction[1],3),hcoeffs(direction[2],3)),
         hcoeffs(direction[3],2))~;
};

print("PARI hostile audit: raw E7 reconstruction");

u = [u0,u1,u2,u3,u4,u5,u6,u7,u8,u9];
v = [v0,v1,v2,v3,v4,v5,v6,v7,v8,v9];
ww = [ww0,ww1,ww2,ww3,ww4,ww5];
m3 = monoms(3);
m2 = monoms(2);
Uraw = sum(i=1,10,u[i]*m3[i]);
Vraw = sum(i=1,10,v[i]*m3[i]);
Wraw = sum(i=1,6,ww[i]*m2[i]);
rawvars = concat(concat(u,v),ww);
E7raw = jac3(P,Q,Wraw)+jac3(P,Vraw,R)+jac3(Uraw,Q,R);
check(is_affine_linear(E7raw,7,rawvars),"raw E7 is not linear in its 26 unknowns");
sys7 = linear_system(E7raw,7,rawvars);
A7 = sys7[1];
b7 = sys7[2];

check(matsize(A7)==[36,26],"raw E7 matrix shape");
check(b7==vector(36)~,"raw E7 is homogeneous");
check(matrank(A7)==16,"raw E7 rank is not 16");
rows7 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,18];
cols7 = [2,3,5,6,7,8,9,10,12,13,15,16,19,20,25,26];
check(matdet(vecextract(A7,rows7,cols7))==3194799993706229268480,"fixed raw E7 maximal minor mismatch");

dirs = [[x^3,0,0],[0,x^3,0],[deriv(P,y),deriv(Q,y),deriv(R,y)],[deriv(P,z),deriv(Q,z),deriv(R,z)],[deriv(P,x),deriv(Q,x),deriv(R,x)],[-z*(p-q),z*(p+q),0],[0,0,p],[8/3*y*(p-q),0,x*y],[8/3*z*(p-q),0,x*z],[-8/3*z*(p-q),0,y^2]];
D7 = matrix(26,10,i,j,direction_column(dirs[j])[i]);
check(A7*D7==matrix(36,10),"one of ten claimed E7 directions is not in kernel");
check(matrank(D7)==10,"ten claimed E7 directions are dependent");
krows7 = [1,2,3,4,11,12,13,14,21,23];
check(matdet(vecextract(D7,krows7,vector(10,i,i)))==-4096/9,"kernel-direction minor mismatch");
check(26-matrank(A7)==10,"raw E7 nullity is not ten");
normalcombo = vector(3,i,S*dirs[6][i]+w0*dirs[7][i]+w1*dirs[8][i]+w2*dirs[9][i]+w3*dirs[10][i]);
normaldisplay = [(p-q)*(8/3*w1*y+(-S+8/3*(w2-w3))*z),S*z*(p+q),w0*p+w1*x*y+w2*x*z+w3*y^2];
check(normalcombo==normaldisplay,"five normal directions do not give the displayed gauge-fixed normal form");
print("PASS raw E7: rank 16, nullity 10, all ten directions exact and independent");

print("PARI hostile audit: degree-six compatibility");

U3 = (p-q)*(8/3*w1*y+(-S+8/3*(w2-w3))*z);
V3 = S*z*(p+q);
W2 = w0*p+w1*x*y+w2*x*z+w3*y^2;

a = [a0,a1,a2,a3,a4,a5];
b = [b0,b1,b2,b3,b4,b5];
ell = [l0,l1,l2,l3,l4,l5,l6,l7,l8];
H2v = [sum(i=1,6,a[i]*m2[i]),sum(i=1,6,b[i]*m2[i]),W2];
H3v = [U3,V3,R];
H4v = [P,Q,0];
Lmat = matrix(3,3,i,j,ell[3*(i-1)+j]);
jacvec(hh) = matrix(3,3,i,j,deriv(hh[i],varsxyz[j]));
weighted = matdet(Lmat+t*jacvec(H2v)+t^2*jacvec(H3v)+t^3*jacvec(H4v));
check(polcoeff(weighted,9,t)==0,"weighted determinant has nonzero E9");
check(polcoeff(weighted,8,t)==0,"weighted determinant has nonzero E8");
check(polcoeff(weighted,7,t)==0,"normal form does not satisfy E7");
E6 = polcoeff(weighted,6,t);
constrained6 = [a1,a2,a3,a4,a5,b1,b2,b3,b4,b5,l7,l8];
check(is_affine_linear(E6,6,constrained6),"E6 is not affine linear in its twelve claimed unknowns");
sys6 = linear_system(E6,6,constrained6);
A6 = sys6[1];
bvec6 = sys6[2];
check(matsize(A6)==[28,12],"E6 matrix shape");
check(matrank(A6)==10,"E6 generic rank is not 10");
rows6 = [1,2,3,4,5,6,7,8,9,12];
cols6 = [1,2,4,5,6,7,9,10,11,12];
check(matdet(vecextract(A6,rows6,cols6))==7925422620672,"fixed constant E6 rank minor mismatch");

K6left = matker(A6~);
check(matsize(K6left)==[28,18],"E6 left-kernel dimension is not 18");
pair6 = vector(18,i,K6left[,i]~*bvec6);
check(pair6[1]==16/3*w1*(w2-w3),"E6 mixed compatibility mismatch");
check(pair6[4]==-32/3*(w2-w3)^2,"E6 square compatibility mismatch");
check(K6left[,4]==concat(vector(13),concat([1],vector(14)))~,"E6 square compatibility unexpectedly uses a divided syzygy");
check(A6~*K6left[,4]==vector(12)~,"E6 square row is not a genuine left syzygy");
print("PASS E6 compatibility: a unit-row syzygy gives -32/3*(w2-w3)^2, so w2=w3 without division");

A6r = subst(A6,w3,w2);
b6r = subst(bvec6,w3,w2);
check(matrank(A6r)==10,"E6 rank changed after w3=w2");
sol6 = [0,a3-16/9*w1^2,a3,-4/3*S*w1,S^2/4,0,b3,b3,0,S^2/4,2/3*w1*(w0-w2),S*w2/2-w1^2/6];
check(A6r*sol6~==b6r,"displayed E6 solution does not solve all coefficient equations");
ka6 = [0,1,1,0,0,0,0,0,0,0,0,0]~;
kb6 = [0,0,0,0,0,0,1,1,0,0,0,0]~;
check(A6r*ka6==vector(28)~,"claimed free a3 direction is not in E6 kernel");
check(A6r*kb6==vector(28)~,"claimed free b3 direction is not in E6 kernel");
check(matrank(matconcat([ka6,kb6]))==2,"two E6 free directions are dependent");
check(12-matrank(A6r)==2,"E6 specialized nullity is not two");
E6sol = subst_many(subst(E6,w3,w2),constrained6,sol6);
check(E6sol==0,"direct E6 converse substitution did not vanish");
print("PASS E6 solve: constant rank 10 and the displayed two-parameter affine solution is complete");

print("PARI hostile audit: degree-five compatibility and determinant exit");
E5 = subst_many(subst(polcoeff(weighted,5,t),w3,w2),constrained6,sol6);
lower5 = [a0,a3,b0,b3,l1,l2,l4,l5,l6];
check(is_affine_linear(E5,5,lower5),"E5 is not affine linear in its nine claimed lower variables");
sys5 = linear_system(E5,5,lower5);
A5 = sys5[1];
bvec5 = sys5[2];
check(matsize(A5)==[21,9],"E5 matrix shape");
check(matrank(A5)==5,"E5 generic rank is not five");
K5left = matker(A5~);
check(matsize(K5left)==[21,16],"E5 left-kernel dimension is not 16");
pair5 = vector(16,i,K5left[,i]~*bvec5);
check(pair5[1]==8/9*w1^3,"E5 cubic compatibility mismatch");
syzygy5 = concat([0,0,-1,1],vector(17))~;
check(K5left[,1]==syzygy5,"E5 cubic compatibility unexpectedly uses a divided syzygy");
check(A5~*syzygy5==vector(9)~,"E5 cubic row difference is not a genuine left syzygy");
print("PASS E5 compatibility: the integer row difference (-row 3 + row 4) gives 8/9*w1^3, so w1=0");

E5r = subst(E5,w1,0);
expected5poly = 6*x^2*(S*a3*(x^2*y+x*y*z+y^3)+S*b3*(x^2*y-x*y*z-y^3)+l1*(x^3+x^2*z+x*y^2)-2*l2*(x^2*y+x*y*z+y^3)+l4*(x^3-x^2*z-x*y^2)-2*l5*(x^2*y-x*y*z-y^3));
check(E5r==expected5poly,"displayed residual E5 polynomial mismatch");
lastvars5 = [l1,l2,l4,l5];
lastsys5 = linear_system(E5r,5,lastvars5);
Alast5 = lastsys5[1];
blast5 = lastsys5[2];
check(matrank(Alast5)==4,"residual E5 four-variable system is not full rank");
rows5 = [1,2,3,5];
check(matdet(vecextract(Alast5,rows5,[1,2,3,4]))==20736,"residual E5 constant pivot minor mismatch");
sol5 = [0,S*a3/2,0,S*b3/2];
check(Alast5*sol5~==blast5,"displayed residual E5 solution does not solve all equations");
check(subst_many(E5r,lastvars5,sol5)==0,"direct residual E5 converse substitution did not vanish");

check(subst(sol6[11],w1,0)==0,"E6 formula does not force l32=0 after w1=0");
check(sol5[1]==0 && sol5[3]==0,"E5 solution does not force l12=l22=0");
detzero = subst_many(matdet(Lmat),[l1,l4,l7],[0,0,0]);
check(detzero==0,"zero second column does not annihilate det L");
check(matdet(Lmat)==l0*l4*l8-l0*l5*l7-l1*l3*l8+l1*l5*l6+l2*l3*l7-l2*l4*l6,"det L expansion mismatch");
print("PASS determinant exit: l12=l22=l32=0, so the second column of L vanishes and det(L)=0");
print("ALL HOSTILE PARI/GP c=0 AUDIT CHECKS PASSED");
quit(0);
