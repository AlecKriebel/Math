\\ Independent hostile audit of the marked triple-companion orbit.

die(msg) = { print(Str("FAIL: ",msg)); quit(1); };
check(flag,msg) = { if(!flag,die(msg)); };

xyz = [x,y,z];
p = x^2;
q = y^2+x*z;
P = p^2;
Q = q^2;
R = x^3;

jac3(f,g,h) =
{
  my(ff=[f,g,h]);
  matdet(matrix(3,3,i,j,deriv(ff[i],xyz[j])));
};

jacvec(hh) = matrix(3,3,i,j,deriv(hh[i],xyz[j]));

homexps(n) =
{
  my(L=List());
  forstep(i=n,0,-1,
    forstep(j=n-i,0,-1,
      listput(L,[i,j,n-i-j])
    )
  );
  Vec(L);
};

monoms(n) =
{
  my(E=homexps(n));
  vector(#E,i,x^E[i][1]*y^E[i][2]*z^E[i][3]);
};

coeffxyz(f,e) =
{
  polcoeff(polcoeff(polcoeff(f,e[1],x),e[2],y),e[3],z);
};

hcoeffs(f,n) =
{
  my(E=homexps(n));
  vector(#E,i,coeffxyz(f,E[i]));
};

coefficient(f,monomial) =
{
  my(px=poldegree(monomial,x),py=poldegree(monomial,y),pz=poldegree(monomial,z));
  coeffxyz(f,[px,py,pz]);
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
  my(L=List());
  for(i=1,n,if(!setsearch(Set(indices),i),listput(L,i)));
  Vec(L);
};

complete_affine_solve(M,rhs,unknowns) =
{
  my(idx=matindexrank(M),rows=Vec(idx[1]),pivots=Vec(idx[2]));
  my(free=vector_complement(#unknowns,pivots));
  my(square=vecextract(M,rows,pivots));
  my(freepart=if(#free,vecextract(M,rows,free)*vector(#free,i,unknowns[free[i]])~,vector(#rows)~));
  my(pivotvalues=matsolve(square,vecextract(rhs,rows)-freepart));
  my(solution=unknowns~);
  for(i=1,#pivots,solution[pivots[i]]=pivotvalues[i]);
  check(M*solution==rhs,"complete_affine_solve produced a false solution");
  [solution,pivots,free];
};

has_associate(vv,target) =
{
  for(i=1,#vv,if(vv[i]==target || vv[i]==-target,return(1)));
  0;
};

lookup_solution(vv,ww,target) =
{
  for(i=1,#vv,if(vv[i]==target,return(ww[i])));
  die(Str("solution lookup failed for ",target));
};

chosen_minor(M) =
{
  my(idx=matindexrank(M));
  matdet(vecextract(M,Vec(idx[1]),Vec(idx[2])));
};

direction_column(direction) =
{
  concat(concat(hcoeffs(direction[1],3),hcoeffs(direction[2],3)),
         hcoeffs(direction[3],2))~;
};

weighted_determinant(U,V,W) =
{
  my(H2v=[sum(i=1,6,aall[i]*m2[i]),sum(i=1,6,ball[i]*m2[i]),W]);
  my(H3v=[U,V,R],H4v=[P,Q,0]);
  matdet(Lmat+t*jacvec(H2v)+t^2*jacvec(H3v)+t^3*jacvec(H4v));
};

print("PARI hostile marked-triple audit: raw E7 kernel and gauge");

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
check(is_affine_linear(E7raw,7,rawvars),"raw E7 is not linear");
sys7 = linear_system(E7raw,7,rawvars);
A7 = sys7[1];
b7 = sys7[2];
check(matsize(A7)==[36,26],"raw E7 matrix shape mismatch");
check(b7==vector(36)~,"raw E7 is not homogeneous");
check(matrank(A7)==8,"raw E7 rank is not eight");
rows7 = [3,5,6,8,9,10,12,14];
cols7 = [2,3,5,6,7,8,9,10];
check(matdet(vecextract(A7,rows7,cols7))==483729408,"raw E7 fixed maximal minor mismatch");

translations = [[deriv(P,x),deriv(Q,x),deriv(R,x)],[deriv(P,y),deriv(Q,y),deriv(R,y)],[deriv(P,z),deriv(Q,z),deriv(R,z)]];
dirs = [[x^3,0,0],[0,x^3,0],translations[1],translations[2],translations[3],[x*q,0,0],[4/3*x^2*y,0,x*y],[4/3*x^2*z,0,x*z],[-4/3*x^2*z,0,y^2],[4/3*x*y*z,0,y*z],[4/3*x*z^2,0,z^2],[0,x^2*y,0],[0,x^2*z,0],[0,x*y*z,0],[0,x*z^2,0],[0,y^2*z,0],[0,y*z^2,0],[0,z^3,0]];
D7 = matrix(26,18,i,j,direction_column(dirs[j])[i]);
check(A7*D7==matrix(36,18),"a claimed raw E7 direction is not in the kernel");
check(matrank(D7)==18,"the eighteen raw E7 directions are dependent");
krows7 = [1,2,3,4,5,6,11,12,13,14,15,16,17,18,19,20,21,23];
check(matdet(vecextract(D7,krows7,vector(18,i,i)))==-2048/27,"raw E7 kernel basis minor mismatch");
check(26-matrank(A7)==18,"raw E7 nullity is not eighteen");
normalcoeffs = [AA,w1,w2,w3,w4,w5,B1,B2,B3,B4,B5,B6,B7];
normalcombo = vector(3,i,sum(j=1,13,normalcoeffs[j]*dirs[j+5][i]));
normaldisplay = [AA*x*q+4/3*(w1*x^2*y+(w2-w3)*x^2*z+w4*x*y*z+w5*x*z^2),B1*x^2*y+B2*x^2*z+B3*x*y*z+B4*x*z^2+B5*y^2*z+B6*y*z^2+B7*z^3,w1*x*y+w2*x*z+w3*y^2+w4*y*z+w5*z^2];
check(normalcombo==normaldisplay,"thirteen normals do not give the displayed normal form");
print("PASS raw E7: rank 8/nullity 18 and complete five-gauge/thirteen-normal basis");

print("PARI hostile marked-triple audit: general E6 compatibility ideal");

aall = [a0,a1,a2,a3,a4,a5];
ball = [b0,b1,b2,b3,b4,b5];
ell = [l0,l1,l2,l3,l4,l5,l6,l7,l8];
Lmat = matrix(3,3,i,j,ell[3*(i-1)+j]);
alllower = concat(concat(aall,ball),ell);
Ugen = AA*x*q+4/3*(w1*x^2*y+(w2-w3)*x^2*z+w4*x*y*z+w5*x*z^2);
Vgen = B1*x^2*y+B2*x^2*z+B3*x*y*z+B4*x*z^2+B5*y^2*z+B6*y*z^2+B7*z^3;
Wgen = w1*x*y+w2*x*z+w3*y^2+w4*y*z+w5*z^2;
weightedgen = weighted_determinant(Ugen,Vgen,Wgen);
check(polcoeff(weightedgen,9,t)==0,"general weighted determinant has nonzero E9");
check(polcoeff(weightedgen,8,t)==0,"general weighted determinant has nonzero E8");
check(polcoeff(weightedgen,7,t)==0,"general normal form has nonzero E7");
E6gen = polcoeff(weightedgen,6,t);
vars6gen = concat(concat(aall,ball),[l7,l8]);
check(is_affine_linear(E6gen,6,vars6gen),"general E6 is not affine linear in fourteen lower variables");
sys6gen = linear_system(E6gen,6,vars6gen);
M6gen = sys6gen[1];
rhs6gen = sys6gen[2];
check(matsize(M6gen)==[28,14],"general E6 matrix shape mismatch");
check(matrank(M6gen)==4,"general E6 rank is not four");
check(matdet(vecextract(M6gen,[3,5,6,9],[2,3,5,6]))==10368,"general E6 fixed rank minor mismatch");
K6left = matker(M6gen~);
check(matsize(K6left)==[28,24],"general E6 left-kernel dimension mismatch");
pair6gen = vector(24,i,K6left[,i]~*rhs6gen);
check(has_associate(pair6gen,-32/3*w5^2),"E6 compatibility omits w5^2");
check(has_associate(pair6gen,-8/3*(3*AA*w5+2*w4^2)),"E6 compatibility omits 3*A*w5+2*w4^2");
check(has_associate(pair6gen,-4*AA*w4),"E6 compatibility omits A*w4");

pair6reduced = vector(24,i,subst(subst(pair6gen[i],w5,0),w4,0));
KK = 4*w3-3*AA;
dd = w2-w3;
check(pair6reduced[1]==-KK*B1,"reduced compatibility K*B1 mismatch");
check(pair6reduced[2]==2*KK*B2,"reduced compatibility K*B2 mismatch");
check(pair6reduced[3]==3*KK*B3,"reduced compatibility K*B3 mismatch");
check(pair6reduced[4]==-4*KK*(B4-B5),"reduced compatibility K*(B4-B5) mismatch");
check(pair6reduced[5]==3*(KK*B6+2*AA*w1),"first B6/A*w1 compatibility mismatch");
check(pair6reduced[7]==2*(-KK*B6+3*AA*w1),"second B6/A*w1 compatibility mismatch");
check(pair6reduced[8]==-4*AA*dd-6*KK*B7,"B7/A*d compatibility mismatch");
check(pair6reduced[12]==-4*AA*dd,"A*d compatibility mismatch");
for(i=1,24,if(!setsearch(Set([1,2,3,4,5,7,8,12]),i),check(pair6reduced[i]==0,"unexpected reduced E6 compatibility")));
check(pair6reduced[5]/3+pair6reduced[7]/2==5*AA*w1,"B6 equations do not imply A*w1");
check(pair6reduced[8]-pair6reduced[12]==-6*KK*B7,"B7 is not isolated after A*d");
print("PASS general E6: w4=w5=0 and exact division-free A/K compatibility ideal");

print("PARI hostile marked-triple audit: open K branch, A=0 leaf");

Ua0 = 4/3*(s1*x^2*y+delta*x^2*z);
Va0 = CC*z*q;
Wa0 = s1*x*y+(delta+wbar)*x*z+wbar*y^2;
weighteda0 = weighted_determinant(Ua0,Va0,Wa0);
E6a0 = polcoeff(weighteda0,6,t);
check(is_affine_linear(E6a0,6,alllower),"open A=0 E6 is not affine linear");
sys6a0 = linear_system(E6a0,6,alllower);
solve6a0 = complete_affine_solve(sys6a0[1],sys6a0[2],alllower);
sol6a0 = solve6a0[1];
free6a0 = vector(#solve6a0[3],i,alllower[solve6a0[3][i]]);
check(subst_many(E6a0,alllower,sol6a0)==0,"open A=0 full E6 converse fails");
E5a0 = subst_many(polcoeff(weighteda0,5,t),alllower,sol6a0);
check(is_affine_linear(E5a0,5,free6a0),"open A=0 E5 is not affine linear in E6-free variables");
sys5a0 = linear_system(E5a0,5,free6a0);
K5a0 = matker(sys5a0[1]~);
pair5a0 = vector(matsize(K5a0)[2],i,K5a0[,i]~*sys5a0[2]);
check(has_associate(pair5a0,-8/9*s1^3),"open A=0 E5 compatibility omits w1^3");
check(has_associate(pair5a0,16/9*delta^3),"open A=0 E5 compatibility omits d^3");
check(2*coefficient(E5a0,x^2*y^2*z)-coefficient(E5a0,x*y^4)==8/9*s1^3,"open A=0 division-free w1^3 row combination mismatch");
check(coefficient(E5a0,x*y*z^3)==-16/9*delta^3,"open A=0 division-free d^3 row mismatch");
print("PASS open K, A=0: fresh E6 solve and E5 cubes force w1=d=0 without division");

print("PARI hostile marked-triple audit: reduced open K branch");

Uopen = AA*x*q;
Vopen = CC*z*q;
Wopen = wbar*q;
weightedopen = weighted_determinant(Uopen,Vopen,Wopen);
E6open = polcoeff(weightedopen,6,t);
sys6open = linear_system(E6open,6,alllower);
solve6open = complete_affine_solve(sys6open[1],sys6open[2],alllower);
sol6open = solve6open[1];
free6open = vector(#solve6open[3],i,alllower[solve6open[3][i]]);
check(lookup_solution(alllower,sol6open,a1)==4/3*l7,"open E6 a1 formula mismatch");
check(lookup_solution(alllower,sol6open,a2)==a3+4/3*l8+AA*CC/2-2/3*CC*wbar,"open E6 a2 formula mismatch");
check(lookup_solution(alllower,sol6open,a4)==0 && lookup_solution(alllower,sol6open,a5)==0,"open E6 a4/a5 formula mismatch");
check(subst_many(E6open,alllower,sol6open)==0,"open full E6 converse fails");

E5open = subst_many(polcoeff(weightedopen,5,t),alllower,sol6open);
check(is_affine_linear(E5open,5,free6open),"open C!=0 E5 is not affine linear");
sys5open = linear_system(E5open,5,free6open);
solve5open = complete_affine_solve(sys5open[1],sys5open[2],free6open);
sol5open = solve5open[1];
free5open = vector(#solve5open[3],i,free6open[solve5open[3][i]]);
check(lookup_solution(free6open,sol5open,a3)==2*l2/CC,"open C!=0 E5 a3 formula mismatch");
check(lookup_solution(free6open,sol5open,b1)==0,"open C!=0 E5 b1 formula mismatch");
check(lookup_solution(free6open,sol5open,b2)==b3,"open C!=0 E5 b2 formula mismatch");
check(lookup_solution(free6open,sol5open,b4)==0,"open C!=0 E5 b4 formula mismatch");
check(lookup_solution(free6open,sol5open,b5)==CC^2/4,"open C!=0 E5 b5 formula mismatch");
check(lookup_solution(free6open,sol5open,l1)==0,"open C!=0 E5 l12 formula mismatch");
check(lookup_solution(free6open,sol5open,l7)==0,"open C!=0 E5 l32 formula mismatch");
check(lookup_solution(free6open,sol5open,l8)==CC*wbar/2,"open C!=0 E5 l33 formula mismatch");
check(subst_many(E5open,free6open,sol5open)==0,"open C!=0 full E5 converse fails");

E4open = subst_many(subst_many(polcoeff(weightedopen,4,t),alllower,sol6open),free6open,sol5open);
check(is_affine_linear(E4open,4,free5open),"open C!=0 E4 is not affine linear");
sys4open = linear_system(E4open,4,free5open);
solve4open = complete_affine_solve(sys4open[1],sys4open[2],free5open);
sol4open = solve4open[1];
free4open = vector(#solve4open[3],i,free5open[solve4open[3][i]]);
check(lookup_solution(free5open,sol4open,l4)==0,"open C!=0 E4 does not force l22=0");
check(subst_many(E4open,free5open,sol4open)==0,"open C!=0 full E4 converse fails");
detopen = subst_many(subst_many(subst_many(matdet(Lmat),alllower,sol6open),free6open,sol5open),free5open,sol4open);
check(detopen==0,"open C!=0 staged solve does not force det L=0");

\\ The generic pivot above contains A.  Rebuild A=0 rather than specializing it.
weightedopen_a0 = weighted_determinant(0,CC*z*q,wbar*q);
E6open_a0 = polcoeff(weightedopen_a0,6,t);
sys6open_a0 = linear_system(E6open_a0,6,alllower);
solve6open_a0 = complete_affine_solve(sys6open_a0[1],sys6open_a0[2],alllower);
sol6open_a0 = solve6open_a0[1];
free6open_a0 = vector(#solve6open_a0[3],i,alllower[solve6open_a0[3][i]]);
check(subst_many(E6open_a0,alllower,sol6open_a0)==0,"open A=0,C!=0 fresh E6 converse fails");
E5open_a0 = subst_many(polcoeff(weightedopen_a0,5,t),alllower,sol6open_a0);
sys5open_a0 = linear_system(E5open_a0,5,free6open_a0);
solve5open_a0 = complete_affine_solve(sys5open_a0[1],sys5open_a0[2],free6open_a0);
sol5open_a0 = solve5open_a0[1];
free5open_a0 = vector(#solve5open_a0[3],i,free6open_a0[solve5open_a0[3][i]]);
check(subst_many(E5open_a0,free6open_a0,sol5open_a0)==0,"open A=0,C!=0 fresh E5 converse fails");
E4open_a0 = subst_many(subst_many(polcoeff(weightedopen_a0,4,t),alllower,sol6open_a0),free6open_a0,sol5open_a0);
check(!is_affine_linear(E4open_a0,4,free5open_a0),"open A=0,C!=0 E4 rank-drop system unexpectedly affine linear");
check(coefficient(E4open_a0,y^3*z)==4/3*(2*l8-wbar*CC)^2,"open A=0,C!=0 l33 square mismatch");
E4open_a0_l8 = subst(E4open_a0,l8,wbar*CC/2);
check(coefficient(E4open_a0_l8,x^2*y*z)==-8/3*l7^2,"open A=0,C!=0 l32 square mismatch");
E4open_a0_l87 = subst(E4open_a0_l8,l7,0);
check(coefficient(E4open_a0_l87,x^4)==4*wbar*l4,"open A=0,C!=0 l22 row mismatch");
detopen_a0 = subst_many(subst_many(matdet(Lmat),alllower,sol6open_a0),free6open_a0,sol5open_a0);
check(subst_many(detopen_a0,[l8,l7,l4],[wbar*CC/2,0,0])==0,"open A=0,C!=0 square tree does not force det L=0");
print("PASS open K, C!=0: A!=0 solve and fresh A=0 E4 square tree both close");

\\ Rebuild C=0 literally; do not specialize the preceding 1/C solve.
weightedc0 = weighted_determinant(AA*x*q,0,wbar*q);
E6c0 = polcoeff(weightedc0,6,t);
sys6c0 = linear_system(E6c0,6,alllower);
solve6c0 = complete_affine_solve(sys6c0[1],sys6c0[2],alllower);
sol6c0 = solve6c0[1];
check(subst_many(E6c0,alllower,sol6c0)==0,"open C=0 full E6 converse fails");
E5c0 = subst_many(polcoeff(weightedc0,5,t),alllower,sol6c0);
Kopen = 4*wbar-3*AA;
check(coefficient(E5c0,x^5)==Kopen*b1,"open C=0 x^5 coefficient mismatch");
check(coefficient(E5c0,x^4*y)==-2*Kopen*(b2-b3),"open C=0 x^4*y coefficient mismatch");
check(coefficient(E5c0,x^4*z)==Kopen*b4+6*l1,"open C=0 x^4*z coefficient mismatch");
check(coefficient(E5c0,x^3*y^2)==-2*(Kopen*b4-3*l1),"open C=0 x^3*y^2 coefficient mismatch");
check(coefficient(E5c0,x^3*y*z)==-4*(Kopen*b5+3*l2),"open C=0 x^3*y*z coefficient mismatch");
check(coefficient(E5c0,x^2*y^3)==-12*l2,"open C=0 x^2*y^3 coefficient mismatch");
check(coefficient(E5c0,y^5)==4*AA*l8,"open C=0 y^5 coefficient mismatch");
check(coefficient(E5c0,x*y^4)==-2*AA*l7,"open C=0 x*y^4 coefficient mismatch");
c0basevars = [b1,b2,b4,b5,l1,l2];
c0basevals = [0,b3,0,0,0,0];
check(subst_many(E5c0,c0basevars,c0basevals)==-2*AA*l7*x^3*z^2-4*AA*l7*x^2*y^2*z-2*AA*l7*x*y^4+4*AA*l8*x^2*y*z^2+8*AA*l8*x*y^3*z+4*AA*l8*y^5,"open C=0 residual diagnostic mismatch");

\\ A!=0 forces l32=l33=0 directly at E5.
check(subst_many(E5c0,concat(c0basevars,[l7,l8]),concat(c0basevals,[0,0]))==0,"open C=0,A!=0 E5 converse fails");
check(subst_many(matdet(Lmat),[l1,l2,l7,l8],[0,0,0,0])==0,"open C=0,A!=0 determinant exit fails");

\\ A=0 must be handled before using the A*l32,A*l33 equations.
E5c0a0 = subst(E5c0,AA,0);
check(subst_many(E5c0a0,c0basevars,c0basevals)==0,"open C=A=0 E5 converse fails");
E4c0a0 = subst(subst_many(polcoeff(weightedc0,4,t),alllower,sol6c0),AA,0);
E4c0a0 = subst_many(E4c0a0,c0basevars,c0basevals);
check(coefficient(E4c0a0,y^3*z)==16/3*l8^2,"open C=A=0 l33 square mismatch");
check(coefficient(subst(E4c0a0,l8,0),x*y^3)==-8/3*l7^2,"open C=A=0 l32 square mismatch");
check(subst_many(matdet(Lmat),[l1,l2,l7,l8],[0,0,0,0])==0,"open C=A=0 determinant exit fails");
print("PASS open K, C=0: literal E5 split and A=0 E4 squares close every specialization");

print("PARI hostile marked-triple audit: resonant K=0, A!=0 branch");

weightedresgen = weighted_determinant(AA*x*q,Vgen,3/4*AA*q);
E6resgen = polcoeff(weightedresgen,6,t);
sys6resgen = linear_system(E6resgen,6,alllower);
solve6resgen = complete_affine_solve(sys6resgen[1],sys6resgen[2],alllower);
sol6resgen = solve6resgen[1];
free6resgen = vector(#solve6resgen[3],i,alllower[solve6resgen[3][i]]);
check(subst_many(E6resgen,alllower,sol6resgen)==0,"resonant general-V E6 converse fails");
E5resgen = subst_many(polcoeff(weightedresgen,5,t),alllower,sol6resgen);
sys5resgen = linear_system(E5resgen,5,free6resgen);
K5resgen = matker(sys5resgen[1]~);
pair5resgen = vector(matsize(K5resgen)[2],i,K5resgen[,i]~*sys5resgen[2]);
check(has_associate(pair5resgen,9/4*AA^2*B3),"resonant E5 compatibility omits B3");
check(has_associate(pair5resgen,-3*AA^2*(B4-B5)),"resonant E5 compatibility omits B4-B5");
check(has_associate(pair5resgen,3*AA^2*B6),"resonant E5 compatibility omits B6");
check(has_associate(pair5resgen,9/2*AA^2*B7),"resonant E5 compatibility omits B7");
check(coefficient(E5resgen,x^2*z^3)==3/4*AA^2*B6,"resonant direct B6 row mismatch");
check(coefficient(E5resgen,x*y*z^3)==-9/2*AA^2*B7,"resonant direct B7 row mismatch");
check(subst(coefficient(E5resgen,x^3*z^2)-coefficient(E5resgen,x*y^4),B6,0)==9/4*AA^2*B3,"resonant direct B3 row combination mismatch");
check(coefficient(E5resgen,x*y^3*z)-2*coefficient(E5resgen,y^5)==-3*AA^2*(B4-B5),"resonant direct B4-B5 row combination mismatch");
for(i=1,#pair5resgen,check(subst_many(pair5resgen[i],[B3,B4,B6,B7],[0,B5,0,0])==0,"unexpected resonant E5 compatibility survives V reduction"));
print("PASS resonant E5 compatibility: A!=0 reduces V exactly to B1*x^2*y+B2*x^2*z+C*z*q");

Vres = B1*x^2*y+B2*x^2*z+CC*z*q;
weightedres = weighted_determinant(AA*x*q,Vres,3/4*AA*q);
E6res = polcoeff(weightedres,6,t);
sys6res = linear_system(E6res,6,alllower);
solve6res = complete_affine_solve(sys6res[1],sys6res[2],alllower);
sol6res = solve6res[1];
free6res = vector(#solve6res[3],i,alllower[solve6res[3][i]]);
check(subst_many(E6res,alllower,sol6res)==0,"resonant reduced-V E6 converse fails");

E5res = subst_many(polcoeff(weightedres,5,t),alllower,sol6res);
sys5res = linear_system(E5res,5,free6res);
solve5res = complete_affine_solve(sys5res[1],sys5res[2],free6res);
sol5res = solve5res[1];
free5res = vector(#solve5res[3],i,free6res[solve5res[3][i]]);
check(subst_many(E5res,free6res,sol5res)==0,"resonant reduced-V E5 converse fails");

E4res = subst_many(subst_many(polcoeff(weightedres,4,t),alllower,sol6res),free6res,sol5res);
sys4res = linear_system(E4res,4,free5res);
solve4res = complete_affine_solve(sys4res[1],sys4res[2],free5res);
sol4res = solve4res[1];
free4res = vector(#solve4res[3],i,free5res[solve4res[3][i]]);
check(subst_many(E4res,free5res,sol4res)==0,"resonant reduced-V E4 converse fails");

staged_l1 = subst_many(subst_many(subst_many(l1,alllower,sol6res),free6res,sol5res),free5res,sol4res);
staged_l2 = subst_many(subst_many(subst_many(l2,alllower,sol6res),free6res,sol5res),free5res,sol4res);
staged_l7 = subst_many(subst_many(subst_many(l7,alllower,sol6res),free6res,sol5res),free5res,sol4res);
staged_l8 = subst_many(subst_many(subst_many(l8,alllower,sol6res),free6res,sol5res),free5res,sol4res);
staged_a0 = subst_many(subst_many(subst_many(a0,alllower,sol6res),free6res,sol5res),free5res,sol4res);
staged_b1 = subst_many(subst_many(subst_many(b1,alllower,sol6res),free6res,sol5res),free5res,sol4res);
staged_b2 = subst_many(subst_many(subst_many(b2,alllower,sol6res),free6res,sol5res),free5res,sol4res);
staged_b4 = subst_many(subst_many(subst_many(b4,alllower,sol6res),free6res,sol5res),free5res,sol4res);
staged_b5 = subst_many(subst_many(subst_many(b5,alllower,sol6res),free6res,sol5res),free5res,sol4res);
check(staged_l1==-AA^2*B1/8,"resonant l12 formula mismatch");
check(staged_l2==-AA^2*B2/8,"resonant l13 formula mismatch");
check(staged_l7==0,"resonant l32 formula mismatch");
check(staged_l8==3/8*AA*CC,"resonant l33 formula mismatch");
check(staged_a0==2/3*l6,"resonant a0 formula mismatch");
check(staged_b1==0 && staged_b2==b3 && staged_b4==0 && staged_b5==CC^2/4,"resonant lower b formulas mismatch");
check(matdet(vecextract(sys5res[1],[1,3,5,6,9],[2,10,11,16,17]))==-1728*AA^2*B1,"resonant B1-open E5 pivot mismatch");
check(matdet(vecextract(subst(sys5res[1],B1,0),[2,3,5,6,9],[2,10,11,16,17]))==3456*AA^2*B2,"resonant B1=0,B2-open E5 pivot mismatch");
check(matdet(vecextract(sys4res[1],[1,3,5,6,9],[1,3,4,6,7]))==243*AA^9*B1/64,"resonant B1-open E4 pivot mismatch");
check(matdet(vecextract(subst(sys4res[1],B1,0),[2,3,5,6,9],[1,3,4,6,7]))==-243*AA^9*B2/32,"resonant B1=0,B2-open E4 pivot mismatch");

E3res = subst_many(subst_many(subst_many(polcoeff(weightedres,3,t),alllower,sol6res),free6res,sol5res),free5res,sol4res);
check(is_affine_linear(E3res,3,free4res),"resonant E3 is not affine linear in staged free variables");
check(coefficient(E3res,x*y*z)-coefficient(E3res,y^3)==-3/8*AA^3*B2^2,"resonant direct B2^2 E3 row difference mismatch");
check(subst(coefficient(E3res,x^2*y),B2,0)==3/16*AA^3*B1^2,"resonant direct B1^2 E3 row mismatch");
print("PASS resonant nonzero-(B1,B2) stratum: two explicit pivots and literal E3 squares contradict it");

\\ Closed rank-drop stratum B1=B2=0, C=0: rebuild before solving.
weightedres_c0 = weighted_determinant(AA*x*q,0,3/4*AA*q);
E6res_c0 = polcoeff(weightedres_c0,6,t);
sys6res_c0 = linear_system(E6res_c0,6,alllower);
solve6res_c0 = complete_affine_solve(sys6res_c0[1],sys6res_c0[2],alllower);
sol6res_c0 = solve6res_c0[1];
free6res_c0 = vector(#solve6res_c0[3],i,alllower[solve6res_c0[3][i]]);
E5res_c0 = subst_many(polcoeff(weightedres_c0,5,t),alllower,sol6res_c0);
sys5res_c0 = linear_system(E5res_c0,5,free6res_c0);
check(matdet(vecextract(sys5res_c0[1],[3,5,6,9],[10,11,16,17]))==576*AA^2,"resonant C=0 fresh E5 pivot mismatch");
solve5res_c0 = complete_affine_solve(sys5res_c0[1],sys5res_c0[2],free6res_c0);
sol5res_c0 = solve5res_c0[1];
check(subst_many(E5res_c0,free6res_c0,sol5res_c0)==0,"resonant C=0 fresh E5 converse fails");
detres_c0 = subst_many(subst_many(matdet(Lmat),alllower,sol6res_c0),free6res_c0,sol5res_c0);
check(detres_c0==0,"resonant C=0 fresh determinant exit fails");

\\ Closed rank-drop stratum B1=B2=0, C!=0: l13 is genuinely free.
weightedres_exc = weighted_determinant(AA*x*q,CC*z*q,3/4*AA*q);
E6res_exc = polcoeff(weightedres_exc,6,t);
sys6res_exc = linear_system(E6res_exc,6,alllower);
solve6res_exc = complete_affine_solve(sys6res_exc[1],sys6res_exc[2],alllower);
sol6res_exc = solve6res_exc[1];
free6res_exc = vector(#solve6res_exc[3],i,alllower[solve6res_exc[3][i]]);
E5res_exc = subst_many(polcoeff(weightedres_exc,5,t),alllower,sol6res_exc);
sys5res_exc = linear_system(E5res_exc,5,free6res_exc);
check(matdet(vecextract(sys5res_exc[1],[3,5,6,9],[2,10,16,17]))==288*AA^2*CC,"resonant exceptional E5 pivot mismatch");
solve5res_exc = complete_affine_solve(sys5res_exc[1],sys5res_exc[2],free6res_exc);
sol5res_exc = solve5res_exc[1];
free5res_exc = vector(#solve5res_exc[3],i,free6res_exc[solve5res_exc[3][i]]);
check(subst_many(E5res_exc,free6res_exc,sol5res_exc)==0,"resonant exceptional E5 converse fails");
exc_a3 = subst_many(subst_many(a3,alllower,sol6res_exc),free6res_exc,sol5res_exc);
exc_l1 = subst_many(subst_many(l1,alllower,sol6res_exc),free6res_exc,sol5res_exc);
exc_l7 = subst_many(subst_many(l7,alllower,sol6res_exc),free6res_exc,sol5res_exc);
exc_l8 = subst_many(subst_many(l8,alllower,sol6res_exc),free6res_exc,sol5res_exc);
check(exc_a3==2*l2/CC && exc_l1==0 && exc_l7==0 && exc_l8==3/8*AA*CC,"resonant exceptional E5 parameterization mismatch");
E4res_exc = subst_many(subst_many(polcoeff(weightedres_exc,4,t),alllower,sol6res_exc),free6res_exc,sol5res_exc);
vars4res_exc = [b1,b2,b4,b5];
sys4res_exc = linear_system(E4res_exc,4,vars4res_exc);
check(matdet(vecextract(sys4res_exc[1],[3,6,7,9],[1,2,3,4]))==-81*AA^8/32,"resonant exceptional E4 pivot mismatch");
solve4res_exc = complete_affine_solve(sys4res_exc[1],sys4res_exc[2],vars4res_exc);
sol4res_exc = solve4res_exc[1];
check(sol4res_exc==[0,b3,0,CC^2/4]~,"resonant exceptional E4 solution mismatch");
check(subst_many(E4res_exc,vars4res_exc,sol4res_exc)==0,"resonant exceptional E4 converse fails");
E3res_exc = subst_many(E4res_exc*0+subst_many(subst_many(polcoeff(weightedres_exc,3,t),alllower,sol6res_exc),free6res_exc,sol5res_exc),vars4res_exc,sol4res_exc);
check(coefficient(E3res_exc,x^2*z)==3/4*AA^2*l4,"resonant exceptional E3 l22 coefficient mismatch");
detres_exc = subst_many(subst_many(subst_many(matdet(Lmat),alllower,sol6res_exc),free6res_exc,sol5res_exc),vars4res_exc,sol4res_exc);
check(subst(detres_exc,l4,0)==0,"resonant exceptional E3 determinant exit fails");
print("PASS K=0,A!=0: both rank-drop C leaves rebuilt; free l13 branch closes at literal E3");

print("PARI hostile marked-triple audit: resonant K=A=0 branch");

weightedzero_pre = weighted_determinant(4/3*(s1*x^2*y+s2*x^2*z),Vgen,s1*x*y+s2*x*z);
E6zero_pre = polcoeff(weightedzero_pre,6,t);
sys6zero_pre = linear_system(E6zero_pre,6,alllower);
solve6zero_pre = complete_affine_solve(sys6zero_pre[1],sys6zero_pre[2],alllower);
sol6zero_pre = solve6zero_pre[1];
free6zero_pre = vector(#solve6zero_pre[3],i,alllower[solve6zero_pre[3][i]]);
check(subst_many(E6zero_pre,alllower,sol6zero_pre)==0,"K=A=0 pre-specialization E6 converse fails");
E5zero_pre = subst_many(polcoeff(weightedzero_pre,5,t),alllower,sol6zero_pre);
sys5zero_pre = linear_system(E5zero_pre,5,free6zero_pre);
K5zero_pre = matker(sys5zero_pre[1]~);
pair5zero_pre = vector(matsize(K5zero_pre)[2],i,K5zero_pre[,i]~*sys5zero_pre[2]);
check(has_associate(pair5zero_pre,-8/9*s1^3),"K=A=0 E5 compatibility omits w1^3");
check(has_associate(pair5zero_pre,16/9*s2^3),"K=A=0 E5 compatibility omits w2^3");
check(2*coefficient(E5zero_pre,x^2*y^2*z)+3*coefficient(E5zero_pre,x*y^4)+8*coefficient(E5zero_pre,x^3*z^2)==40/9*s1^3,"K=A=0 division-free w1^3 row combination mismatch");
check(coefficient(E5zero_pre,x*y*z^3)==-16/9*s2^3,"K=A=0 division-free w2^3 row mismatch");

\\ Rebuild after w1=w2=0, leaving every coefficient of V arbitrary.
weightedzero = weighted_determinant(0,Vgen,0);
E6zero = polcoeff(weightedzero,6,t);
sys6zero = linear_system(E6zero,6,alllower);
solve6zero = complete_affine_solve(sys6zero[1],sys6zero[2],alllower);
sol6zero = solve6zero[1];
free6zero = vector(#solve6zero[3],i,alllower[solve6zero[3][i]]);
check(subst_many(E6zero,alllower,sol6zero)==0,"K=A=0 fresh E6 converse fails");
E5zero = subst_many(polcoeff(weightedzero,5,t),alllower,sol6zero);
check(coefficient(E5zero,x^5)==-3*B1*a3,"K=A=0 arbitrary-V B1*a3 row mismatch");
check(coefficient(E5zero,x^4*y)==6*B2*a3,"K=A=0 arbitrary-V B2*a3 row mismatch");
check(coefficient(E5zero,x^3*z^2)==-3*B6*a3,"K=A=0 arbitrary-V B6*a3 row mismatch");
check(coefficient(E5zero,x^2*y*z^2)==18*B7*a3,"K=A=0 arbitrary-V B7*a3 row mismatch");
check(coefficient(E5zero,x^3*y^2)-coefficient(E5zero,x^4*z)==9*B3*a3,"K=A=0 arbitrary-V B3*a3 row combination mismatch");
check(coefficient(E5zero,x^3*y*z)-coefficient(E5zero,x^2*y^3)==12*(B4-B5)*a3,"K=A=0 arbitrary-V B4-B5 row combination mismatch");

\\ Leaf a3=0: paired E5 rows force l12=l13=0 for arbitrary V.
E5zero_a3 = subst_many(E5zero,[a3,l1,l2],[0,0,0]);
check(E5zero_a3==0,"K=A=0,a3=0 E5 converse fails");
E4zero_a3 = subst_many(subst_many(polcoeff(weightedzero,4,t),alllower,sol6zero),[a3,l1,l2],[0,0,0]);
check(coefficient(E4zero_a3,y^3*z)==16/3*l8^2,"K=A=0,a3=0 E4 l33 square mismatch");
check(coefficient(subst(E4zero_a3,l8,0),x*y^3)==-8/3*l7^2,"K=A=0,a3=0 E4 l32 square mismatch");
check(subst_many(matdet(Lmat),[l1,l2,l7,l8],[0,0,0,0])==0,"K=A=0,a3=0 determinant exit fails");

\\ Leaf a3!=0: the literal products force V=C*z*q and l13=C*a3/2.
weightedzero_exc = weighted_determinant(0,CC*z*q,0);
E6zero_exc = polcoeff(weightedzero_exc,6,t);
sys6zero_exc = linear_system(E6zero_exc,6,alllower);
solve6zero_exc = complete_affine_solve(sys6zero_exc[1],sys6zero_exc[2],alllower);
sol6zero_exc = solve6zero_exc[1];
free6zero_exc = vector(#solve6zero_exc[3],i,alllower[solve6zero_exc[3][i]]);
E5zero_exc = subst_many(polcoeff(weightedzero_exc,5,t),alllower,sol6zero_exc);
sys5zero_exc = linear_system(E5zero_exc,5,free6zero_exc);
check(matdet(vecextract(sys5zero_exc[1],[3,5],[2,10]))==-36*CC,"K=A=0 exceptional E5 pivot mismatch");
check(subst_many(E5zero_exc,[l1,l2],[0,CC*a3/2])==0,"K=A=0 exceptional E5 converse fails");
E4zero_exc = subst_many(subst_many(polcoeff(weightedzero_exc,4,t),alllower,sol6zero_exc),[l1,l2],[0,CC*a3/2]);
check(coefficient(E4zero_exc,y^3*z)==16/3*l8^2,"K=A=0 exceptional E4 l33 square mismatch");
check(coefficient(subst(E4zero_exc,l8,0),x*y^3)==-8/3*l7^2,"K=A=0 exceptional E4 l32 square mismatch");
E4zero_exc00 = subst_many(E4zero_exc,[l7,l8],[0,0]);
vars4zero_exc = [b1,b2,b4,b5];
sys4zero_exc = linear_system(E4zero_exc00,4,vars4zero_exc);
check(matdet(vecextract(sys4zero_exc[1],[1,2,3,5],[1,2,3,4]))==648*a3^4,"K=A=0 exceptional E4 lower pivot mismatch");
solve4zero_exc = complete_affine_solve(sys4zero_exc[1],sys4zero_exc[2],vars4zero_exc);
sol4zero_exc = solve4zero_exc[1];
check(sol4zero_exc==[0,b3,0,CC^2/4]~,"K=A=0 exceptional E4 lower solution mismatch");
check(subst_many(E4zero_exc00,vars4zero_exc,sol4zero_exc)==0,"K=A=0 exceptional E4 converse fails");
E3zero_exc = subst_many(subst_many(subst_many(polcoeff(weightedzero_exc,3,t),alllower,sol6zero_exc),[l1,l2],[0,CC*a3/2]),vars4zero_exc,sol4zero_exc);
E3zero_exc = subst_many(E3zero_exc,[l7,l8],[0,0]);
check(coefficient(E3zero_exc,x^3)==-3*a3*l4,"K=A=0 exceptional E3 l22 coefficient mismatch");
detzero_exc = subst_many(subst_many(subst_many(matdet(Lmat),alllower,sol6zero_exc),[l1,l2],[0,CC*a3/2]),[l7,l8,l4],[0,0,0]);
check(detzero_exc==0,"K=A=0 exceptional determinant exit fails");

\\ C=0 in the exceptional shape has l13=0 before the square exit.
E5zero_v0 = subst_many(E5zero,[B1,B2,B3,B4,B5,B6,B7,l1,l2],[0,0,0,0,0,0,0,0,0]);
check(E5zero_v0==0,"K=A=0,V=0 E5 converse fails");
check(subst_many(matdet(Lmat),[l1,l2,l7,l8],[0,0,0,0])==0,"K=A=0,V=0 determinant exit fails");
print("PASS K=A=0: literal product ideal exhausts arbitrary V; exceptional V=C*z*q closes at E3");
print("ALL HOSTILE PARI/GP MARKED-TRIPLE AUDIT CHECKS PASSED");
quit(0);
