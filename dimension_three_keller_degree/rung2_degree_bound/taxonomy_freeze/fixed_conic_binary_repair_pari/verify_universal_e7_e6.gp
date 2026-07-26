\\ Independent universal E7/E6 calculation for the binary fixed-conic row.
\\
\\ Method: exact coefficient matrices over Q and constant-pivot elimination.
\\ No rank decision or division depends on a parameter.

default(parisizemax, 1500000000);
allocatemem(256000000);

jacmap(H) = matrix(3,3,i,j,deriv(H[i],[p,q,r][j]));

zero_vars(x, vv) =
{
  my(y=x);
  for(i=1,#vv,y=subst(y,vv[i],0));
  y
};

subst_pairs(x, old, new) =
{
  my(y=x);
  for(i=1,#old,y=subst(y,old[i],new[i]));
  y
};

mon_exponents(d) =
{
  my(z=List());
  for(i=0,d,
    for(j=0,d-i,
      listput(z,[i,j,d-i-j])
    )
  );
  Vec(z)
};

coeff_at(P, ex) =
{
  polcoef(polcoef(polcoef(P,ex[3],r),ex[2],q),ex[1],p)
};

coeff_vector(P, mons) = vector(#mons,i,coeff_at(P,mons[i]));

map_coeff_vector(H, mons) =
{
  my(z=List());
  for(i=1,3,
    for(j=1,#mons,listput(z,coeff_at(H[i],mons[j])))
  );
  Vec(z)
};

complement_indices(n, chosen) =
{
  my(z=List(), hit);
  for(i=1,n,
    hit=0;
    for(j=1,#chosen,if(chosen[j]==i,hit=1));
    if(!hit,listput(z,i))
  );
  Vecsmall(Vec(z))
};

nonzero_entries(vv) =
{
  my(z=List());
  for(i=1,#vv,if(vv[i]!=0,listput(z,vv[i])));
  Vec(z)
};

\\ Return [rank, raw left-null compatibility vector, pivot rows, pivot cols].
e7_data(H4,H3,H2,w) =
{
  my(D=matdet(x*jacmap(H2)+x^2*jacmap(H3)+x^3*jacmap(H4)));
  my(E7=polcoef(D,7,x), mons=mon_exponents(7));
  my(cv=coeff_vector(E7,mons));
  my(Amat=matrix(#mons,#w,i,j,deriv(cv[i],w[j])));
  my(rhs=-vector(#mons,i,zero_vars(cv[i],w)));
  my(ind=matindexrank(Amat), ker=matker(Amat~));
  [matrank(Amat),nonzero_entries(Vec(ker~*rhs~)),ind[1],ind[2]]
};

\\ Given a consistent specialized E7, solve the complete affine fibre using
\\ the same constant pivots and retain every free H2 coefficient.
e7_fibre(H4,H3,H2,w) =
{
  my(D=matdet(x*jacmap(H2)+x^2*jacmap(H3)+x^3*jacmap(H4)));
  my(E7=polcoef(D,7,x), mons=mon_exponents(7));
  my(cv=coeff_vector(E7,mons));
  my(Amat=matrix(#mons,#w,i,j,deriv(cv[i],w[j])));
  my(rhs=-vector(#mons,i,zero_vars(cv[i],w)));
  my(ind=matindexrank(Amat), rows=ind[1], piv=ind[2]);
  my(free=complement_indices(#w,piv));
  my(B=vecextract(Amat,rows,piv));
  my(rhs0=vecextract(rhs,rows)~-vecextract(Amat,rows,free)*vecextract(w,free)~);
  my(ans=matsolve(B,rhs0), sol=w);
  for(i=1,#piv,sol[piv[i]]=ans[i]);
  [sol,piv,free,Amat,rhs]
};

v=vector(12,i,eval(Str("v",i)));
w=vector(18,i,eval(Str("w",i)));
ell=vector(9,i,eval(Str("ell",i)));
u=vector(30,i,eval(Str("u",i)));

A=[p^2,p*q,q^2]~;
Ap=vector(3,i,deriv(A[i],p))~;
Aq=vector(3,i,deriv(A[i],q))~;
V=vector(3,i,sum(j=1,4,v[4*(i-1)+j]*[p^3,p^2*q,p*q^2,q^3][j]))~;
H2=vector(3,i,sum(j=1,6,w[6*(i-1)+j]*[p^2,p*q,q^2,p*r,q*r,r^2][j]))~;
H3=V+r*((a*p+b*q)*Ap+(c*p+d*q)*Aq)+r^2/2*(e*Ap+f*Aq);
L=matrix(3,3,i,j,ell[3*(i-1)+j]);
if(#v!=12 || #w!=18 || #ell!=9,error("input coefficient count changed"));
print("CERT input dimensions V=12 H2=18 L=9");

print("START complete E8 cubic normal");
cubic_mons=mon_exponents(3);
H3full=vector(3,i,sum(j=1,#cubic_mons,u[10*(i-1)+j]*p^cubic_mons[j][1]*q^cubic_mons[j][2]*r^cubic_mons[j][3]))~;
normal_parameters=concat(v,[a,b,c,d,e,f]);
normal_coordinates=map_coeff_vector(H3,cubic_mons);
normal_matrix=matrix(30,18,i,j,deriv(normal_coordinates[i],normal_parameters[j]));
if(matrank(normal_matrix)!=18,error("E8 normal parameters are dependent"));

check_e8(H4case,label) =
{
  my(D8=matdet(x^2*jacmap(H3full)+x^3*jacmap(H4case)));
  my(E8=polcoef(D8,8,x), cm8=coeff_vector(E8,mon_exponents(8)));
  my(M8=matrix(#cm8,30,i,j,deriv(cm8[i],u[j])));
  my(normal_E8=polcoef(matdet(x^2*jacmap(H3)+x^3*jacmap(H4case)),8,x));
  print(label," E8 rank = ",matrank(M8),", kernel dimension = ",30-matrank(M8));
  if(matrank(M8)!=12,error("unexpected E8 rank"));
  if(normal_E8!=0,error("displayed E8 normal does not lie in kernel"));
};

check_e8(p*q*A,"split");
check_e8(p^2*A,"double");

print("START raw E7 compatibility");
split_raw=e7_data(p*q*A,H3,H2,w);
print("split E7 H2 rank = ",split_raw[1]);
print("split E7 pivot rows = ",split_raw[3]);
print("split E7 pivot cols = ",split_raw[4]);
print("split E7 nonzero compatibility count = ",#split_raw[2]);
for(i=1,#split_raw[2],print("split compat ",i," = ",split_raw[2][i]));

double_raw=e7_data(p^2*A,H3,H2,w);
print("double E7 H2 rank = ",double_raw[1]);
print("double E7 pivot rows = ",double_raw[3]);
print("double E7 pivot cols = ",double_raw[4]);
print("double E7 nonzero compatibility count = ",#double_raw[2]);
for(i=1,#double_raw[2],print("double compat ",i," = ",double_raw[2][i]));

print("START specialized consistent E7 fibres");
H3s=subst_pairs(H3,[b,c,e,f],[0,0,0,0]);
Fs=e7_fibre(p*q*A,H3s,H2,w);
print("split fibre pivot H2 indices = ",Fs[2]);
print("split fibre free H2 indices = ",Fs[3]);
split_pivot_det=matdet(vecextract(Fs[4],matindexrank(Fs[4])[1],Fs[2]));
print("split E7 constant pivot determinant = ",split_pivot_det);
if(split_pivot_det==0,error("split E7 pivot determinant vanished"));
for(i=1,#Fs[2],print("split w",Fs[2][i]," = ",Fs[1][Fs[2][i]]));
split_residual=nonzero_entries(Vec(Fs[4]*Fs[1]~-Fs[5]~));
print("split fibre residual E7 equations = ",split_residual);
split_radical=[(a-3*d)*v4,(3*a-d)*v9];
if(#split_residual!=2,error("unexpected split residual equation count"));
if(split_residual[1]!=3*split_radical[1],error("split residual generator 1 changed"));
if(split_residual[2]!=-3*split_radical[2],error("split residual generator 2 changed"));

H3d=subst_pairs(H3,[b,e,f],[0,0,0]);
Fd=e7_fibre(p^2*A,H3d,H2,w);
print("double fibre pivot H2 indices = ",Fd[2]);
print("double fibre free H2 indices = ",Fd[3]);
double_pivot_det=matdet(vecextract(Fd[4],matindexrank(Fd[4])[1],Fd[2]));
print("double E7 constant pivot determinant = ",double_pivot_det);
if(double_pivot_det==0,error("double E7 pivot determinant vanished"));
for(i=1,#Fd[2],print("double w",Fd[2][i]," = ",Fd[1][Fd[2][i]]));
double_residual=nonzero_entries(Vec(Fd[4]*Fd[1]~-Fd[5]~));
print("double fibre residual E7 equations = ",double_residual);
double_radical=[(a-2*d)*v4,(a-4*d)*v3-6*c*v4-6*(a-2*d)*v8];
if(#double_residual!=2,error("unexpected double residual equation count"));
if(double_residual[1]!=6*double_radical[1],error("double residual generator 1 changed"));
if(double_residual[2]!=2*double_radical[2],error("double residual generator 2 changed"));

print("START universal E6 r^2 checks");
Ds=matdet(L+x*jacmap(H2)+x^2*jacmap(H3s)+x^3*jacmap(p*q*A));
E6s=polcoef(Ds,6,x);
for(i=1,#Fs[2],E6s=subst(E6s,w[Fs[2][i]],Fs[1][Fs[2][i]]));
R2s=polcoef(E6s,2,r);
target_s=12*p^2*q^2*(a-d)^2*(a+d);
print("split universal R2 = ",factor(R2s));
if(R2s!=target_s,error("split universal E6 r^2 identity failed"));
print("CERT split E6 R2=12*p^2*q^2*(a-d)^2*(a+d)");

Dd=matdet(L+x*jacmap(H2)+x^2*jacmap(H3d)+x^3*jacmap(p^2*A));
E6d=polcoef(Dd,6,x);
for(i=1,#Fd[2],E6d=subst(E6d,w[Fd[2][i]],Fd[1][Fd[2][i]]));
R2d=polcoef(E6d,2,r);
target_d=24*d*p^2*(c*p+(d-a)*q)^2;
print("double universal R2 = ",factor(R2d));
if(R2d!=target_d,error("double universal E6 r^2 identity failed"));
print("CERT double E6 R2=24*d*p^2*(c*p+(d-a)*q)^2");

print("PASS universal E7 affine fibres and E6 r^2 identities");
quit;
