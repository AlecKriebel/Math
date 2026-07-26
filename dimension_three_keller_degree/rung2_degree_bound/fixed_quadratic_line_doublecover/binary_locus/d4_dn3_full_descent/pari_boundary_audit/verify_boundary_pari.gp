\\ Clean-room PARI/GP verifier for the two boundary charts of D4-DN-3.
\\
\\ This script reconstructs the weighted Jacobian determinant directly from
\\ the normalized homogeneous pieces.  It does not load formulas or data from
\\ either SymPy implementation.

p='p; q='q; r='r; w='w; k='k;
coords=[p,q,r];

jacmat(H)=matrix(3,3,i,j,deriv(H[i],coords[j]));
c3(f,ip,iq,ir)=polcoeff(polcoeff(polcoeff(f,ir,r),iq,q),ip,p);
check_zero(value,message)={if(value!=0,print(Str("FAIL: ",message,"; residual = ",value));quit(1))};
check_true(value,message)={if(!value,print(Str("FAIL: ",message));quit(1))};
check_kden(expr,index)=
{
  my(deni=denominator(expr));
  check_true(deni==1 || poldegree(deni,k)>=0,
    Str("denominator is polynomial, entry ",index));
  for(j=1,#denom_guard_vars,
    check_zero(deriv(deni,denom_guard_vars[j]),
      Str("denominator uses a parameter other than k, entry ",index))
  );
  check_true(subst(deni,k,1)!=0,
    Str("denominator has nonzero scalar at k=1, entry ",index));
  check_zero(deni/subst(deni,k,1)-k^poldegree(deni,k),
    Str("denominator supported only on k=0, entry ",index));
};

\\ Homogeneous coefficient variables.
u0='u0; u1='u1; u2='u2; u3='u3;
v0='v0; v1='v1; v2='v2; v3='v3;
t0='t0; t1='t1; t2='t2;
a0='a0; a1='a1; a2='a2; a3='a3; a4='a4; a5='a5;
b0='b0; b1='b1; b2='b2; b3='b3; b4='b4; b5='b5;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4; l5='l5;
l6='l6; l7='l7; l8='l8;
denom_guard_vars=[p,q,r,w,u0,u1,u2,u3,v0,v1,v2,v3,t0,t1,t2,a0,a1,a2,a3,a4,a5,b0,b1,b2,b3,b4,b5,l0,l1,l2,l3,l4,l5,l6,l7,l8];

U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=t0*p^2+t1*p*q+t2*q^2;
A=a0*p^2+a1*p*q+a2*p*r+a3*q^2+a4*q*r+a5*r^2;
B=b0*p^2+b1*p*q+b2*p*r+b3*q^2+b4*q*r+b5*r^2;
L=[l0,l1,l2;l3,l4,l5;l6,l7,l8];

h=(p+q)^2;
P=h*p^2;
Q=h*q^2;
R=(p+q)^3;
H4=[P,Q,0]~;

\\ Build one weighted determinant from a chosen contact scale.
build_det(contact_scale)=
{
  my(U1=-contact_scale*p*(p+q));
  my(V1= contact_scale*q*(p+q));
  my(H3=[U0+r*U1,V0+r*V1,R]~);
  my(H2=[A,B,T0]~);
  matdet(L+w*jacmat(H2)+w^2*jacmat(H3)+w^3*jacmat(H4));
};

D=build_det(k);
check_zero(polcoeff(D,9,w),"E9 vanishes");
check_zero(polcoeff(D,8,w),"E8 vanishes");
check_zero(polcoeff(D,7,w),"E7 contact syzygy");
E6=polcoeff(D,6,w);
E5=polcoeff(D,5,w);
E4=polcoeff(D,4,w);

\\ Full E6 system: all 28 degree-six coefficients, all 18 variables known
\\ to occur in this weighted block.
vars6=[a2,a4,a5,b2,b4,b5,l8,u0,u1,u2,u3,v0,v1,v2,v3,t0,t1,t2];
zero6=vector(#vars6);
exps6=List();
for(ip=0,6,for(iq=0,6-ip,listput(exps6,[ip,iq,6-ip-iq])));
exps6=Vec(exps6);
eq6=vector(#exps6,i,c3(E6,exps6[i][1],exps6[i][2],exps6[i][3]));
M6=matrix(#eq6,#vars6,i,j,polcoeff(eq6[i],1,vars6[j]));
rhs6=matrix(#eq6,1,i,j,-substvec(eq6[i],vars6,zero6));
Aug6=matconcat([M6,rhs6]);
for(i=1,#eq6,check_zero(eq6[i]-(M6*vars6~)[i]+rhs6[i,1],Str("punctured E6 linear reconstruction row ",i)));

\\ A fixed six-pivot valid exactly on the punctured chart k != 0.
rows6=[28,27,26,25,24,22];
cols6=[1,2,3,4,6,8];
pivot6=matdet(vecextract(M6,rows6,cols6));
check_zero(pivot6+279936*k,"punctured E6 pivot");
check_true(matrank(M6)==6,"punctured E6 coefficient rank six");
check_true(matrank(Aug6)==6,"punctured E6 augmented rank six");

freecols6=[5,7,9,10,11,12,13,14,15,16,17,18];
pivotvars6=vecextract(vars6,cols6);
freevars6=vecextract(vars6,freecols6);
rhsrows6=vector(#rows6,i,rhs6[rows6[i],1])~;
rhs_eff6=rhsrows6-vecextract(M6,rows6,freecols6)*freevars6~;
sol6=matsolve(vecextract(M6,rows6,cols6),rhs_eff6);
for(i=1,#eq6,check_zero(substvec(eq6[i],pivotvars6,Vec(sol6)),Str("punctured E6 residual row ",i)));
for(i=1,#sol6,check_kden(sol6[i],i));

E5_6=substvec(E5,pivotvars6,Vec(sol6));
E4_6=substvec(E4,pivotvars6,Vec(sol6));

\\ The r-linear E5 block is linear in the twelve E6-free variables.
exps51=vector(5,i,[i-1,4-(i-1),1]);
eq51=vector(5,i,c3(E5_6,exps51[i][1],exps51[i][2],1));
M51=matrix(5,#freevars6,i,j,polcoeff(eq51[i],1,freevars6[j]));
rhs51=matrix(5,1,i,j,-substvec(eq51[i],freevars6,vector(#freevars6)));
for(i=1,#eq51,check_zero(eq51[i]-(M51*freevars6~)[i]+rhs51[i,1],Str("E5 r-linear reconstruction row ",i)));
rows51=[1,2,3];
cols51=[1,2,10];
pivot51=matdet(vecextract(M51,rows51,cols51));
check_zero(pivot51-192*k^4,"punctured E5 r-linear pivot");
check_true(matrank(M51)==3,"punctured E5 r-linear rank three");
check_true(matrank(matconcat([M51,rhs51]))==3,"punctured E5 r-linear consistency");
freecols51=[3,4,5,6,7,8,9,11,12];
pivotvars51=vecextract(freevars6,cols51);
freevars51=vecextract(freevars6,freecols51);
rhsrows51=vector(#rows51,i,rhs51[rows51[i],1])~;
rhs_eff51=rhsrows51-vecextract(M51,rows51,freecols51)*freevars51~;
sol51=matsolve(vecextract(M51,rows51,cols51),rhs_eff51);
for(i=1,#eq51,check_zero(substvec(eq51[i],pivotvars51,Vec(sol51)),Str("punctured E5 r-linear residual row ",i)));
for(i=1,#sol51,check_kden(sol51[i],100+i));

E5_51=substvec(E5_6,pivotvars51,Vec(sol51));
E4_51=substvec(E4_6,pivotvars51,Vec(sol51));

\\ The binary E5 block is linear in the six binary quadratic coefficients
\\ of A,B and the four off-column entries of L listed below.
exps50=vector(6,i,[i-1,5-(i-1),0]);
eq50=vector(6,i,c3(E5_51,exps50[i][1],exps50[i][2],0));
vars50=[a0,a1,a3,b0,b1,b3,l2,l5,l6,l7];
M50=matrix(6,#vars50,i,j,polcoeff(eq50[i],1,vars50[j]));
rhs50=matrix(6,1,i,j,-substvec(eq50[i],vars50,vector(#vars50)));
for(i=1,#eq50,check_zero(eq50[i]-(M50*vars50~)[i]+rhs50[i,1],Str("E5 binary reconstruction row ",i)));
rows50=[1,2,3];
cols50=[1,2,4];
pivot50=matdet(vecextract(M50,rows50,cols50));
check_zero(pivot50-108*k^3,"punctured E5 binary pivot");
check_true(matrank(M50)==3,"punctured E5 binary coefficient rank three");
freecols50=[3,5,6,7,8,9,10];
pivotvars50=vecextract(vars50,cols50);
freevars50=vecextract(vars50,freecols50);
rhsrows50=vector(#rows50,i,rhs50[rows50[i],1])~;
rhs_eff50=rhsrows50-vecextract(M50,rows50,freecols50)*freevars50~;
sol50=matsolve(vecextract(M50,rows50,cols50),rhs_eff50);
res50=vector(#eq50,i,substvec(eq50[i],pivotvars50,Vec(sol50)));
for(i=1,#sol50,check_kden(sol50[i],200+i));

E4_50=substvec(E4_51,pivotvars50,Vec(sol50));
S=v0-v1+v2-v3;
Dlin=u1-2*u2+3*u3-v1+2*v2-3*v3;
check_zero(c3(E4_50,2,0,2)+9*k^3*S/4,"E4 p^2 r^2 explicitly forces S");
check_zero(c3(E4_50,1,1,2)+9*k^3*S/2,"E4 p q r^2 repeats S");
check_zero(c3(E4_50,0,2,2)+9*k^3*S/4,"E4 q^2 r^2 repeats S");

subSvars=[v0];
subSvals=[v1-v2+v3];
res50S=vector(#res50,i,substvec(res50[i],subSvars,subSvals));
ratios50=[0,0,0,3/4,3/2,3/4];
for(i=1,#res50S,check_zero(res50S[i]-ratios50[i]*k*Dlin^2,Str("complete E5 residual after S, row ",i)));

subDvars=[u1];
subDvals=[2*u2-3*u3+v1-2*v2+3*v3];
E4_SD=substvec(substvec(E4_50,subSvars,subSvals),subDvars,subDvals);

\\ The r-linear E4 block has a constant-rank two solve.
exps41=vector(4,i,[i-1,3-(i-1),1]);
eq41=vector(4,i,c3(E4_SD,exps41[i][1],exps41[i][2],1));
vars41=[b1,b3,l5,l6,l7];
M41=matrix(4,#vars41,i,j,polcoeff(eq41[i],1,vars41[j]));
rhs41=matrix(4,1,i,j,-substvec(eq41[i],vars41,vector(#vars41)));
for(i=1,#eq41,check_zero(eq41[i]-(M41*vars41~)[i]+rhs41[i,1],Str("E4 r-linear reconstruction row ",i)));
rows41=[1,2];
cols41=[1,4];
pivot41=matdet(vecextract(M41,rows41,cols41));
check_zero(pivot41-3*k^4,"punctured E4 r-linear pivot");
check_true(matrank(M41)==2,"punctured E4 r-linear rank two");
check_true(matrank(matconcat([M41,rhs41]))==2,"punctured E4 r-linear consistency");
freecols41=[2,3,5];
pivotvars41=vecextract(vars41,cols41);
freevars41=vecextract(vars41,freecols41);
rhsrows41=vector(#rows41,i,rhs41[rows41[i],1])~;
rhs_eff41=rhsrows41-vecextract(M41,rows41,freecols41)*freevars41~;
sol41=matsolve(vecextract(M41,rows41,cols41),rhs_eff41);
for(i=1,#eq41,check_zero(substvec(eq41[i],pivotvars41,Vec(sol41)),Str("E4 r-linear residual row ",i)));
for(i=1,#sol41,check_kden(sol41[i],300+i));

E4_41=substvec(E4_SD,pivotvars41,Vec(sol41));
exps40=vector(5,i,[i-1,4-(i-1),0]);
eq40=vector(5,i,c3(E4_41,exps40[i][1],exps40[i][2],0));
vars40=[l0,l1,l3,l4];
M40=matrix(5,#vars40,i,j,polcoeff(eq40[i],1,vars40[j]));
rhs40=matrix(5,1,i,j,-substvec(eq40[i],vars40,vector(#vars40)));
for(i=1,#eq40,check_zero(eq40[i]-(M40*vars40~)[i]+rhs40[i,1],Str("E4 binary reconstruction row ",i)));
rows40=[1,2];
cols40=[1,3];
pivot40=matdet(vecextract(M40,rows40,cols40));
check_zero(pivot40-9*k^2,"punctured E4 binary pivot");
check_true(matrank(M40)==2,"punctured E4 binary rank two");
check_true(matrank(matconcat([M40,rhs40]))==2,"punctured E4 binary consistency");
freecols40=[2,4];
pivotvars40=vecextract(vars40,cols40);
freevars40=vecextract(vars40,freecols40);
rhsrows40=vector(#rows40,i,rhs40[rows40[i],1])~;
rhs_eff40=rhsrows40-vecextract(M40,rows40,freecols40)*freevars40~;
sol40=matsolve(vecextract(M40,rows40,cols40),rhs_eff40);
for(i=1,#eq40,check_zero(substvec(eq40[i],pivotvars40,Vec(sol40)),Str("E4 binary residual row ",i)));
for(i=1,#sol40,check_kden(sol40[i],400+i));

E5_SD=substvec(substvec(substvec(E5_51,pivotvars50,Vec(sol50)),subSvars,subSvals),subDvars,subDvals);
check_zero(E5_SD,"complete E5 residual after S=D=0");
E4_final=substvec(E4_41,pivotvars40,Vec(sol40));
check_zero(E4_final,"complete E4 residual after both rank-two stages");

det_desc=matdet(L);
det_desc=substvec(det_desc,pivotvars6,Vec(sol6));
det_desc=substvec(det_desc,pivotvars51,Vec(sol51));
det_desc=substvec(det_desc,pivotvars50,Vec(sol50));
det_desc=substvec(det_desc,subSvars,subSvals);
det_desc=substvec(det_desc,subDvars,subDvals);
det_desc=substvec(det_desc,pivotvars41,Vec(sol41));
det_desc=substvec(det_desc,pivotvars40,Vec(sol40));
check_zero(det_desc,"punctured intersection forces determinant of L to zero");

print("D4_DN3_PARI_PUNCTURED_INTERSECTION_PASS_DETL_ZERO");

\\ -------------------------------------------------------------------------
\\ Origin chart.  Rebuild the determinant with zero contact rather than
\\ specializing any k-dependent solve.
\\ -------------------------------------------------------------------------

D0=build_det(0);
check_zero(polcoeff(D0,9,w),"origin E9 vanishes");
check_zero(polcoeff(D0,8,w),"origin E8 vanishes");
check_zero(polcoeff(D0,7,w),"origin E7 vanishes");
E60=polcoeff(D0,6,w);
E40=polcoeff(D0,4,w);

eq60=vector(#exps6,i,c3(E60,exps6[i][1],exps6[i][2],exps6[i][3]));
M60=matrix(#eq60,#vars6,i,j,polcoeff(eq60[i],1,vars6[j]));
rhs60=matrix(#eq60,1,i,j,-substvec(eq60[i],vars6,zero6));
Aug60=matconcat([M60,rhs60]);
for(i=1,#eq60,check_zero(eq60[i]-(M60*vars6~)[i]+rhs60[i,1],Str("origin E6 linear reconstruction row ",i)));
rows60=[28,27,26,25,24];
cols60=[1,2,3,4,6];
pivot60=matdet(vecextract(M60,rows60,cols60));
check_zero(pivot60-31104,"origin E6 pivot");
check_true(matrank(M60)==5,"origin E6 coefficient rank five");
check_true(matrank(Aug60)==5,"origin E6 augmented rank five");

freecols60=[5,7,8,9,10,11,12,13,14,15,16,17,18];
pivotvars60=vecextract(vars6,cols60);
freevars60=vecextract(vars6,freecols60);
rhsrows60=vector(#rows60,i,rhs60[rows60[i],1])~;
rhs_eff60=rhsrows60-vecextract(M60,rows60,freecols60)*freevars60~;
sol60=matsolve(vecextract(M60,rows60,cols60),rhs_eff60);
for(i=1,#eq60,check_zero(substvec(eq60[i],pivotvars60,Vec(sol60)),Str("origin E6 residual row ",i)));
for(i=1,#sol60,check_zero(denominator(sol60[i])-1,Str("origin E6 solve has no localization, entry ",i)));

E40done=substvec(E40,pivotvars60,Vec(sol60));
check_zero(c3(E40done,3,0,1)-3*b4^2,"origin E4 p^3 r square");
check_zero(c3(E40done,0,3,1)-(3*b4-4*l8)^2/3,"origin E4 q^3 r square");
for(i=1,#sol60,check_zero(substvec(sol60[i],[b4,l8],[0,0]),Str("origin E6 pivot collapses after the two squares, entry ",i)));

\\ Exact target-linear reduction after all nonlinear r-coefficients vanish.
A0=a0*p^2+a1*p*q+a3*q^2;
B0=b0*p^2+b1*p*q+b3*q^2;
Hbin=[A0+U0+P,B0+V0+Q,T0+R]~;
Fbin=L*[p,q,r]~+Hbin;
Jbin=jacmat(Hbin);
Mbin=L+Jbin;
detL=matdet(L);
adjL=[l4*l8-l5*l7,l2*l7-l1*l8,l1*l5-l2*l4;l5*l6-l3*l8,l0*l8-l2*l6,l2*l3-l0*l5;l3*l7-l4*l6,l1*l6-l0*l7,l0*l4-l1*l3];
check_zero(adjL*L-detL*matid(3),"adjugate target normalization");
Ftrans=adjL*Fbin;
check_zero(deriv(Ftrans[1],r),"first normalized coordinate is binary");
check_zero(deriv(Ftrans[2],r),"second normalized coordinate is binary");
check_zero(deriv(Ftrans[3],r)-detL,"third normalized coordinate has constant r slope");
Mtrans=adjL*Mbin;
check_zero(Mtrans[1,3],"normalized Jacobian top first r entry");
check_zero(Mtrans[2,3],"normalized Jacobian top second r entry");
check_zero(Mtrans[3,3]-detL,"normalized Jacobian bottom r entry");
planeDet=Mtrans[1,1]*Mtrans[2,2]-Mtrans[1,2]*Mtrans[2,1];
check_zero(planeDet-detL*matdet(Mbin),"exact plane Jacobian reduction identity");

print("D4_DN3_PARI_ORIGIN_PASS_BINARY_COLLAPSE_PLANE_REDUCTION");
print("D4_DN3_PARI_BOUNDARY_AUDIT_ALL_PASS");

quit(0);
