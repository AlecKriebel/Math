\\ Independent hostile PARI/GP audit of the two fixed-divisor e=2
\\ mixed-companion exclusions.

die(msg) = { print(Str("FAIL: ", msg)); quit(1); };
check(flag,msg) = { if(!flag,die(msg)); };
checkeq(got,want,msg) = { if(got!=want,die(Str(msg, ": got ",got,", want ",want))); };

xyz = [x,y,z];

homexps(n) =
{
  my(out=List());
  forstep(i=n,0,-1,
    forstep(j=n-i,0,-1,
      listput(out,[i,j,n-i-j])
    )
  );
  Vec(out);
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

coeffmon(f,m) =
{
  coeffxyz(f,[poldegree(m,x),poldegree(m,y),poldegree(m,z)]);
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
  my(L=List(),S=Set(indices));
  for(i=1,n,if(!setsearch(S,i),listput(L,i)));
  Vec(L);
};

lookup_solution(vv,ww,target) =
{
  for(i=1,#vv,if(vv[i]==target,return(ww[i])));
  die(Str("solution lookup failed for ",target));
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
  [sol,pivots,free,M*sol-rhs];
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

cleared_left_data(M,rhs) =
{
  my(N=matker(M~),pairs=List(),vectors=List());
  for(j=1,matsize(N)[2],
    my(den=1,v,pair);
    for(i=1,matsize(N)[1],den*=denominator(N[i,j]));
    v=den*N[,j];
    for(i=1,#v,checkeq(denominator(v[i]),1,
      Str("cleared left vector ",j," is not polynomial")));
    checkeq(M~*v,vector(matsize(M)[2])~,
      Str("cleared left vector ",j," is not a syzygy"));
    pair=v~*rhs;
    listput(vectors,v);
    listput(pairs,pair);
  );
  [Vec(vectors),Vec(pairs)];
};

weighted_determinant(P,Q,R,U,V,W) =
{
  my(H2=[sum(i=1,6,aall[i]*m2[i]),sum(i=1,6,ball[i]*m2[i]),W]);
  my(H3=[U,V,R],H4=[P,Q,0]);
  matdet(Lmat+t*jacvec(H2)+t^2*jacvec(H3)+t^3*jacvec(H4));
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

raw_case(label,p,q,R,normals,rows,cols,wantdet,krows,wantkdet,display) =
{
  my(P=p^2,Q=p*q);
  my(uu=[u0,u1,u2,u3,u4,u5,u6,u7,u8,u9]);
  my(vv=[v0,v1,v2,v3,v4,v5,v6,v7,v8,v9]);
  my(ww=[ww0,ww1,ww2,ww3,ww4,ww5]);
  my(rawvars=concat(concat(uu,vv),ww));
  my(U=sum(i=1,10,uu[i]*m3[i]));
  my(V=sum(i=1,10,vv[i]*m3[i]));
  my(W=sum(i=1,6,ww[i]*m2[i]));
  my(E7=jac3(P,Q,W)+jac3(P,V,R)+jac3(U,Q,R));
  checkeq(jac3(P,Q,R),0,Str(label,": top E8 identity"));
  check(is_affine_linear(E7,7,rawvars),Str(label,": raw E7 nonlinear"));
  my(sys=linear_system(E7,7,rawvars),M=sys[1],rhs=sys[2]);
  checkeq(matsize(M),[36,26],Str(label,": raw shape"));
  checkeq(rhs,vector(36)~,Str(label,": raw inhomogeneous"));
  checkeq(matrank(M),14,Str(label,": raw rank"));
  checkeq(matdet(vecextract(M,rows,cols)),wantdet,
    Str(label,": raw maximal minor"));
  my(trans=[[deriv(P,x),deriv(Q,x),deriv(R,x)],
            [deriv(P,y),deriv(Q,y),deriv(R,y)],
            [deriv(P,z),deriv(Q,z),deriv(R,z)]]);
  my(dirs=concat([[R,0,0],[0,R,0],trans[1],trans[2],trans[3]],normals));
  my(K=matrix(26,12,i,j,direction_column(dirs[j])[i]));
  checkeq(M*K,matrix(36,12),Str(label,": claimed kernel directions"));
  checkeq(matrank(K),12,Str(label,": kernel direction independence"));
  checkeq(matdet(vecextract(K,krows,[1..12])),wantkdet,
    Str(label,": kernel independence minor"));
  checkeq(26-matrank(M),12,Str(label,": raw nullity"));
  my(pars=if(label=="rank-two",[AA,CC,DD,w0,w3,w4,w5],
                              [CC,DD,w0,w2,w3,w4,w5]));
  my(combo=vector(3,i,sum(j=1,7,pars[j]*normals[j][i])));
  checkeq(combo,display,Str(label,": normal display reconstruction"));
};

print("PARI hostile audit: raw E7 completeness and legal gauges");

raw_case("rank-two",x^2,y*z,x*y*z, \
  [[0,x^3,0],[4*x^2*y,y^2*z,0],[4*x^2*z,y*z^2,0], \
   [0,0,x^2],[0,x*y^2,y^2],[0,0,y*z],[0,x*z^2,z^2]], \
  [2,3,4,6,7,8,9,10,12,14,17,18,19,20], \
  [2,3,4,6,7,8,9,10,12,13,14,16,17,20], \
  -5308416, \
  [1,2,3,5,11,12,13,14,15,16,21,25],64, \
  [4*CC*x^2*y+4*DD*x^2*z, \
   AA*x^3+CC*y^2*z+DD*y*z^2+w3*x*y^2+w5*x*z^2, \
   w0*x^2+w3*y^2+w4*y*z+w5*z^2]);

raw_case("rank-one",x^2,y^2+x*z,x*(y^2+x*z), \
  [[4*x^2*y,y*(y^2+x*z),0],[4*x^2*z,z*(y^2+x*z),0], \
   [0,0,x^2],[0,x^2*z,x*z],[0,-x^2*z,y^2], \
   [0,x*y*z,y*z],[0,x*z^2,z^2]], \
  [1,2,3,4,5,6,7,8,9,10,11,12,14,16], \
  [2,3,5,6,7,8,9,10,12,13,15,16,19,20], \
  -849346560, \
  [1,2,3,4,11,12,13,14,15,16,21,23],-128, \
  [4*CC*x^2*y+4*DD*x^2*z, \
   CC*y*(y^2+x*z)+DD*z*(y^2+x*z)+(w2-w3)*x^2*z+ \
      w4*x*y*z+w5*x*z^2, \
   w0*x^2+w2*x*z+w3*y^2+w4*y*z+w5*z^2]);

print("PASS raw E7: both rank 14/nullity 12 with complete five-gauge complements");

print("PARI hostile audit: global E6 compatibility");

rtP=x^4; rtQ=x^2*y*z; rtR=x*y*z;
rtU=4*CC*x^2*y+4*DD*x^2*z;
rtV=AA*x^3+CC*y^2*z+DD*y*z^2+w3*x*y^2+w5*x*z^2;
rtW=w0*x^2+w3*y^2+w4*y*z+w5*z^2;
rtweighted=weighted_determinant(rtP,rtQ,rtR,rtU,rtV,rtW);
for(k=7,9,checkeq(polcoeff(rtweighted,k,t),0,Str("rank-two E",k)));
rtE6=polcoeff(rtweighted,6,t);
check(is_affine_linear(rtE6,6,alllower),"rank-two E6 nonlinear in lower data");
rtsys6=linear_system(rtE6,6,alllower);
rtM6=rtsys6[1]; rtrhs6=rtsys6[2];
rtrows6=[2,3,4,6,8,9,12,14];
rtcols6=[2,3,4,6,8,9,10,12];
checkeq(matrank(rtM6),8,"rank-two E6 rank");
checkeq(matdet(vecextract(rtM6,rtrows6,rtcols6)),4096, \
  "rank-two E6 constant maximal minor");
rtsolve6=pivot_solution(rtM6,rtrhs6,alllower,rtrows6,rtcols6);
check_residual_generators(rtsolve6[4],[CC*w3,DD*w5],"rank-two E6");

roP=x^4; roQ=x^2*(y^2+x*z); roR=x*(y^2+x*z);
roU=4*CC*x^2*y+4*DD*x^2*z;
roV=CC*y*(y^2+x*z)+DD*z*(y^2+x*z)+(w2-w3)*x^2*z+ \
    w4*x*y*z+w5*x*z^2;
roW=w0*x^2+w2*x*z+w3*y^2+w4*y*z+w5*z^2;
roweighted=weighted_determinant(roP,roQ,roR,roU,roV,roW);
for(k=7,9,checkeq(polcoeff(roweighted,k,t),0,Str("rank-one E",k)));
roE6=polcoeff(roweighted,6,t);
check(is_affine_linear(roE6,6,alllower),"rank-one E6 nonlinear in lower data");
rosys6=linear_system(roE6,6,alllower);
roM6=rosys6[1]; rorhs6=rosys6[2];
rorows6=[1,2,3,4,5,6,7,9];
rocols6=[2,3,5,6,8,9,11,12];
checkeq(matrank(roM6),8,"rank-one E6 rank");
checkeq(matdet(vecextract(roM6,rorows6,rocols6)),49152, \
  "rank-one E6 constant maximal minor");
rosolve6=pivot_solution(roM6,rorhs6,alllower,rorows6,rocols6);
check_residual_generators(rosolve6[4],[DD*w5,CC*w5+DD*w4],"rank-one E6");

print("PASS global E6: constant pivots and specialization-safe residual generators");

print("PARI hostile audit: rank-two branch tree");

rt_c_weighted=weighted_determinant(rtP,rtQ,rtR, \
  4*CC*x^2*y, \
  AA*x^3+CC*y^2*z+w5*x*z^2, \
  w0*x^2+w4*y*z+w5*z^2);
rt_c_E6=polcoeff(rt_c_weighted,6,t);
rt_c_sys6=linear_system(rt_c_E6,6,alllower);
rt_c_solve6=pivot_solution(rt_c_sys6[1],rt_c_sys6[2],alllower,rtrows6,rtcols6);
checkeq(rt_c_solve6[4],vector(28)~,"rank-two C-only E6 residual");
rt_c_E5=subst_many(polcoeff(rt_c_weighted,5,t),alllower,rt_c_solve6[1]);
rt_c_free=vector(#rt_c_solve6[3],i,alllower[rt_c_solve6[3][i]]);
check(is_affine_linear(rt_c_E5,5,rt_c_free),"rank-two C-only E5 nonlinear");
rt_c_sys5=linear_system(rt_c_E5,5,rt_c_free);
rt_c_left=cleared_left_data(rt_c_sys5[1],rt_c_sys5[2]);
rt_c_found=0;
for(i=1,#rt_c_left[2],if(associate(rt_c_left[2][i],CC^3),rt_c_found=1));
check(rt_c_found,"rank-two C-only E5 lacks polynomial C^3 syzygy");

rt_cd_weighted=weighted_determinant(rtP,rtQ,rtR, \
  4*CC*x^2*y+4*DD*x^2*z, \
  AA*x^3+CC*y^2*z+DD*y*z^2, \
  w0*x^2+w4*y*z);
rt_cd_E6=polcoeff(rt_cd_weighted,6,t);
rt_cd_sys6=linear_system(rt_cd_E6,6,alllower);
rt_cd_solve6=pivot_solution(rt_cd_sys6[1],rt_cd_sys6[2],alllower,rtrows6,rtcols6);
checkeq(rt_cd_solve6[4],vector(28)~,"rank-two C,D E6 residual");
rt_cd_E5=subst_many(polcoeff(rt_cd_weighted,5,t),alllower,rt_cd_solve6[1]);
rt_cd_free=vector(#rt_cd_solve6[3],i,alllower[rt_cd_solve6[3][i]]);
check(is_affine_linear(rt_cd_E5,5,rt_cd_free),"rank-two C,D E5 nonlinear");
rt_cd_sys5=linear_system(rt_cd_E5,5,rt_cd_free);
rt_cd_left=cleared_left_data(rt_cd_sys5[1],rt_cd_sys5[2]);
rt_cd_found=0;
for(i=1,#rt_cd_left[2],if(associate(rt_cd_left[2][i],CC^3),rt_cd_found=1));
check(rt_cd_found,"rank-two C,D E5 lacks polynomial C^3 syzygy");

swap_yz(f)={my(aux='auxswap,g);g=subst(f,y,aux);g=subst(g,z,y);subst(g,aux,z)};
checkeq(swap_yz(x^2),x^2,"rank-two symmetry p");
checkeq(swap_yz(y*z),y*z,"rank-two symmetry q");
checkeq(swap_yz(x*y*z),x*y*z,"rank-two symmetry R");
checkeq(swap_yz([4*x^2*y,y^2*z,y^2]), \
  [4*x^2*z,y*z^2,z^2],"rank-two C/D normal symmetry");

rt_z_weighted=weighted_determinant(rtP,rtQ,rtR,0, \
  AA*x^3+w3*x*y^2+w5*x*z^2, \
  w0*x^2+w3*y^2+w4*y*z+w5*z^2);
rt_z_E6=polcoeff(rt_z_weighted,6,t);
rt_z_vars=[a1,a2,a3,a5,b1,b2,b3,b5];
rt_z_vals=[0,0,0,0,l7,l8,-w3*w4,-w4*w5];
checkeq(matdet(vecextract(linear_system(rt_z_E6,6,alllower)[1], \
  rtrows6,rtcols6)),4096,"rank-two zero-normal E6 constant pivot");
checkeq(subst_many(rt_z_E6,rt_z_vars,rt_z_vals),0, \
  "rank-two zero-normal complete E6 solution");
rt_z_E5=subst_many(polcoeff(rt_z_weighted,5,t),rt_z_vars,rt_z_vals);
checkeq(coeffmon(rt_z_E5,x^4*y),4*(l4+w4*l7), \
  "rank-two zero-normal E5 x4y");
checkeq(coeffmon(rt_z_E5,x^4*z),-4*(l5+w4*l8), \
  "rank-two zero-normal E5 x4z");
checkeq(coeffmon(rt_z_E5,x^2*y^2*z),-l1, \
  "rank-two zero-normal E5 x2y2z");
checkeq(coeffmon(rt_z_E5,x^2*y*z^2),l2, \
  "rank-two zero-normal E5 x2yz2");
rt_z_det=subst_many(matdet(Lmat),[l1,l2,l4,l5], \
  [0,0,-w4*l7,-w4*l8]);
checkeq(rt_z_det,0,"rank-two zero-normal determinant exit");

print("PASS rank-two: nonzero normals have cube obstructions; closed branch has literal determinant exit");

print("PARI hostile audit: rank-one nonzero-normal branches");

ro_d_weighted=weighted_determinant(roP,roQ,roR, \
  4*CC*x^2*y+4*DD*x^2*z, \
  CC*y*(y^2+x*z)+DD*z*(y^2+x*z)+(w2-w3)*x^2*z, \
  w0*x^2+w2*x*z+w3*y^2);
ro_d_E6=polcoeff(ro_d_weighted,6,t);
ro_d_sys6=linear_system(ro_d_E6,6,alllower);
ro_d_solve6=pivot_solution(ro_d_sys6[1],ro_d_sys6[2],alllower,rorows6,rocols6);
checkeq(ro_d_solve6[4],vector(28)~,"rank-one D-branch E6 residual");
ro_d_E5=subst_many(polcoeff(ro_d_weighted,5,t),alllower,ro_d_solve6[1]);
ro_d_free=vector(#ro_d_solve6[3],i,alllower[ro_d_solve6[3][i]]);
check(is_affine_linear(ro_d_E5,5,ro_d_free),"rank-one D-branch E5 nonlinear");
ro_d_sys5=linear_system(ro_d_E5,5,ro_d_free);
ro_d_left=cleared_left_data(ro_d_sys5[1],ro_d_sys5[2]);
ro_d_found=0;
for(i=1,#ro_d_left[2],if(associate(ro_d_left[2][i],DD^3),ro_d_found=1));
check(ro_d_found,"rank-one D-branch lacks polynomial D^3 syzygy");

ro_c_weighted=weighted_determinant(roP,roQ,roR, \
  4*CC*x^2*y, \
  CC*y*(y^2+x*z)+(w2-w3)*x^2*z+w4*x*y*z, \
  w0*x^2+w2*x*z+w3*y^2+w4*y*z);
ro_c_E6=polcoeff(ro_c_weighted,6,t);
ro_c_sys6=linear_system(ro_c_E6,6,alllower);
ro_c_solve6=pivot_solution(ro_c_sys6[1],ro_c_sys6[2],alllower,rorows6,rocols6);
checkeq(ro_c_solve6[4],vector(28)~,"rank-one C-branch E6 residual");
ro_c_E5=subst_many(polcoeff(ro_c_weighted,5,t),alllower,ro_c_solve6[1]);
ro_c_free=vector(#ro_c_solve6[3],i,alllower[ro_c_solve6[3][i]]);
check(is_affine_linear(ro_c_E5,5,ro_c_free),"rank-one C-branch E5 nonlinear");
ro_c_sys5=linear_system(ro_c_E5,5,ro_c_free);
ro_c_left=cleared_left_data(ro_c_sys5[1],ro_c_sys5[2]);
fpoly=CC^3+2*CC^2*w4-2*CC*w4^2+w4^3;
gpoly=(CC+2*w4)*(w4^2-3*CC^2);
ro_c_found_f=0; ro_c_found_g=0;
for(i=1,#ro_c_left[2], \
  my(scaledpair=simplify((CC-w4)*ro_c_left[2][i])); \
  if(associate(scaledpair,CC*fpoly), \
    my(vf=ro_c_left[1][i]*(CC-w4)); \
    vf=vector(#vf,j,simplify(vf[j]))~; \
    checkeq(ro_c_sys5[1]~*vf,vector(#ro_c_free)~, \
      "rank-one C*f cross-multiplied left syzygy"); \
    check(associate(vf~*ro_c_sys5[2],CC*fpoly), \
      "rank-one C*f cross-multiplied pair"); \
    checkeq(subst(ro_c_sys5[1],w4,CC)~*subst(vf,w4,CC), \
      vector(#ro_c_free)~,"rank-one C*f syzygy at w4=C"); \
    check(associate(subst(vf,w4,CC)~*subst(ro_c_sys5[2],w4,CC),CC^4), \
      "rank-one C*f pair at w4=C"); \
    ro_c_found_f=1 \
  ); \
  if(associate(scaledpair,CC*gpoly), \
    my(vg=ro_c_left[1][i]*(CC-w4)); \
    vg=vector(#vg,j,simplify(vg[j]))~; \
    checkeq(ro_c_sys5[1]~*vg,vector(#ro_c_free)~, \
      "rank-one C*g cross-multiplied left syzygy"); \
    check(associate(vg~*ro_c_sys5[2],CC*gpoly), \
      "rank-one C*g cross-multiplied pair"); \
    checkeq(subst(ro_c_sys5[1],w4,CC)~*subst(vg,w4,CC), \
      vector(#ro_c_free)~,"rank-one C*g syzygy at w4=C"); \
    check(associate(subst(vg,w4,CC)~*subst(ro_c_sys5[2],w4,CC),CC^4), \
      "rank-one C*g pair at w4=C"); \
    ro_c_found_g=1 \
  ) \
);
check(ro_c_found_f,"rank-one C-branch lacks cross-multiplied C*f syzygy");
check(ro_c_found_g,"rank-one C-branch lacks cross-multiplied C*g syzygy");
checkeq(polresultant(fpoly,gpoly,w4),-250*CC^9, \
  "rank-one C-branch resultant");
checkeq(subst(fpoly,w4,CC),2*CC^3, \
  "rank-one C-branch f at w4=C");
checkeq(subst(gpoly,w4,CC),-6*CC^3, \
  "rank-one C-branch g at w4=C");
checkeq(subst(CC*fpoly,w4,CC),2*CC^4, \
  "rank-one cross-multiplied C*f at w4=C");
checkeq(subst(CC*gpoly,w4,CC),-6*CC^4, \
  "rank-one cross-multiplied C*g at w4=C");

print("PASS rank-one nonzero normals: D^3 and division-free C*f,C*g obstructions, including w4=C");

print("PARI hostile audit: rank-one zero-normal specialization tree");

ro_z_weighted=weighted_determinant(roP,roQ,roR,0, \
  (w2-w3)*x^2*z+w4*x*y*z+w5*x*z^2, \
  w0*x^2+w2*x*z+w3*y^2+w4*y*z+w5*z^2);

zero_branch_data(subvars,subvals,label) =
{
  my(weighted=subst_many(ro_z_weighted,subvars,subvals));
  my(E6=polcoeff(weighted,6,t));
  my(sys6=linear_system(E6,6,alllower));
  checkeq(matrank(sys6[1]),8,Str(label,": rebuilt E6 rank"));
  checkeq(matdet(vecextract(sys6[1],rorows6,rocols6)),49152, \
    Str(label,": rebuilt E6 constant pivot"));
  my(solve6=pivot_solution(sys6[1],sys6[2],alllower,rorows6,rocols6));
  checkeq(solve6[4],vector(28)~,Str(label,": rebuilt E6 residual"));
  my(free=vector(#solve6[3],i,alllower[solve6[3][i]]));
  my(E5=subst_many(polcoeff(weighted,5,t),alllower,solve6[1]));
  check(is_affine_linear(E5,5,free),Str(label,": E5 nonlinear"));
  my(sys5=linear_system(E5,5,free));
  [weighted,solve6,free,E5,sys5];
};

check_open_zero_solution(data,rows,cols,wantdet,label) =
{
  my(free=data[3],E5=data[4],sys5=data[5]);
  checkeq(matrank(sys5[1]),6,Str(label,": E5 rank"));
  checkeq(matdet(vecextract(sys5[1],rows,cols)),wantdet, \
    Str(label,": E5 chart minor"));
  my(sol5=pivot_solution(sys5[1],sys5[2],free,rows,cols));
  checkeq(sol5[4],vector(21)~,Str(label,": complete E5 residual"));
  checkeq(lookup_solution(free,sol5[1],a3),0,Str(label,": a3"));
  checkeq(lookup_solution(free,sol5[1],b3),-w3^2,Str(label,": b3"));
  checkeq(lookup_solution(free,sol5[1],l1),0,Str(label,": l12"));
  checkeq(lookup_solution(free,sol5[1],l2),0,Str(label,": l13"));
  checkeq(lookup_solution(free,sol5[1],l4),-w3*l7,Str(label,": l22"));
  checkeq(lookup_solution(free,sol5[1],l5),-w3*l8,Str(label,": l23"));
  checkeq(subst_many(E5,free,sol5[1]),0,Str(label,": direct E5 converse"));
  checkeq(subst_many(matdet(Lmat),free,sol5[1]),0,Str(label,": determinant"));
};

ro_z_open=zero_branch_data([],[],"rank-one w4 chart");
check_open_zero_solution(ro_z_open,[1,2,3,4,5,6],[2,4,6,7,9,10], \
  768*w4^2,"rank-one w4 chart");

ro_z_w5=zero_branch_data([w4],[0],"rank-one w5 chart");
check_open_zero_solution(ro_z_w5,[1,2,3,5,7,9],[2,4,6,7,9,10], \
  -4096*w5^2,"rank-one w5 chart");

ro_z_d0=zero_branch_data([w4,w5,w2],[0,0,w3],"rank-one d=0 chart");
ro_z_d0_free=ro_z_d0[3]; ro_z_d0_E5=ro_z_d0[4]; ro_z_d0_sys5=ro_z_d0[5];
checkeq(matrank(ro_z_d0_sys5[1]),4,"rank-one d=0 E5 rank");
checkeq(matdet(vecextract(ro_z_d0_sys5[1],[1,2,3,5],[6,7,9,10])),64, \
  "rank-one d=0 constant E5 pivot");
ro_z_d0_sol5=pivot_solution(ro_z_d0_sys5[1],ro_z_d0_sys5[2], \
  ro_z_d0_free,[1,2,3,5],[6,7,9,10]);
checkeq(ro_z_d0_sol5[4],vector(21)~,"rank-one d=0 complete E5 residual");
checkeq(lookup_solution(ro_z_d0_free,ro_z_d0_sol5[1],l1),0, \
  "rank-one d=0 l12");
checkeq(lookup_solution(ro_z_d0_free,ro_z_d0_sol5[1],l2),0, \
  "rank-one d=0 l13");
checkeq(lookup_solution(ro_z_d0_free,ro_z_d0_sol5[1],l4),-w3*l7, \
  "rank-one d=0 l22");
checkeq(lookup_solution(ro_z_d0_free,ro_z_d0_sol5[1],l5),-w3*l8, \
  "rank-one d=0 l23");
checkeq(subst_many(ro_z_d0_E5,ro_z_d0_free,ro_z_d0_sol5[1]),0, \
  "rank-one d=0 direct E5 converse");
checkeq(subst_many(matdet(Lmat),ro_z_d0_free,ro_z_d0_sol5[1]),0, \
  "rank-one d=0 determinant");

ro_z_d=zero_branch_data([w4,w5],[0,0],"rank-one d!=0 chart");
ro_z_d_free=ro_z_d[3]; ro_z_d_E5=ro_z_d[4]; ro_z_d_sys5=ro_z_d[5];
dpar=w2-w3;
checkeq(matrank(ro_z_d_sys5[1]),4,"rank-one d!=0 E5 generic rank");
checkeq(matdet(vecextract(ro_z_d_sys5[1],[1,2,3,5],[2,4,6,9])), \
  -64*dpar^2,"rank-one d!=0 E5 chart minor");
ro_z_d_sol5=pivot_solution(ro_z_d_sys5[1],ro_z_d_sys5[2], \
  ro_z_d_free,[1,2,3,5],[2,4,6,9]);
checkeq(ro_z_d_sol5[4],vector(21)~,"rank-one d!=0 complete E5 residual");
checkeq(lookup_solution(ro_z_d_free,ro_z_d_sol5[1],l1),0, \
  "rank-one d!=0 l12");
checkeq(lookup_solution(ro_z_d_free,ro_z_d_sol5[1],l4),-w3*l7, \
  "rank-one d!=0 l22");
checkeq(subst_many(ro_z_d_E5,ro_z_d_free,ro_z_d_sol5[1]),0, \
  "rank-one d!=0 direct E5 converse");
ro_z_d_E4=subst_many(polcoeff(ro_z_d[1],4,t),alllower,ro_z_d[2][1]);
ro_z_d_E4=subst_many(ro_z_d_E4,ro_z_d_free,ro_z_d_sol5[1]);
ro_z_d_M=l5+w3*l8;
ro_z_d_cx4=coeffmon(ro_z_d_E4,x^4);
ro_z_d_cx3z=coeffmon(ro_z_d_E4,x^3*z);
checkeq(ro_z_d_cx4,-4*l7*ro_z_d_M/dpar, \
  "rank-one d!=0 E4 x4 product");
checkeq(ro_z_d_cx3z,l2*l7/dpar, \
  "rank-one d!=0 E4 x3z product");
ro_z_d_det=subst_many(matdet(Lmat),ro_z_d_free,ro_z_d_sol5[1]);
checkeq(ro_z_d_det,-l7*(l0*ro_z_d_M-l2*(l3+w3*l6)), \
  "rank-one d!=0 determinant formula");
checkeq(ro_z_d_det, \
  dpar*l0*ro_z_d_cx4/4+dpar*(l3+w3*l6)*ro_z_d_cx3z, \
  "rank-one d!=0 determinant is an E4 coefficient combination");

print("PASS rank-one zero normals: w4, w5, d=0, and d!=0 charts are exhaustive and force det(L)=0");

print("ALL HOSTILE PARI/GP FIXED-DIVISOR e=2 MIXED-ORBIT CHECKS PASSED");
quit;
