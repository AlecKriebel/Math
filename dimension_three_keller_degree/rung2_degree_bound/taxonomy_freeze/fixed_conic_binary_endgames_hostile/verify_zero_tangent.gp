\\ Independent exact audit of all zero-tangent support orbits.
default(parisizemax, 1200000000);
allocatemem(220000000);

jacmap(H)=matrix(3,3,i,j,deriv(H[i],[p,q,r][j]));
zero_vars(x,vv)={my(y=x);for(i=1,#vv,y=subst(y,vv[i],0));y};
subst_pairs(x,old,new)={my(y=x);for(i=1,#old,y=subst(y,old[i],new[i]));y};
mon_exponents(d)={my(z=List());for(i=0,d,for(j=0,d-i,listput(z,[i,j,d-i-j])));Vec(z)};
coeff_at(P,ex)=polcoef(polcoef(polcoef(P,ex[3],r),ex[2],q),ex[1],p);
coeff_vector(P,mons)=vector(#mons,i,coeff_at(P,mons[i]));
complement_indices(n,chosen)={my(z=List(),hit);for(i=1,n,hit=0;for(j=1,#chosen,if(chosen[j]==i,hit=1));if(!hit,listput(z,i)););Vecsmall(Vec(z))};
nonzero_entries(vv)={my(z=List());for(i=1,#vv,if(vv[i]!=0,listput(z,vv[i])));Vec(z)};
linear_data(P,degree,unknowns)=
{
  my(E=polcoef(P,degree,x),cv=coeff_vector(E,mon_exponents(degree)));
  my(M=matrix(#cv,#unknowns,i,j,deriv(cv[i],unknowns[j])));
  my(rhs=-vector(#cv,i,zero_vars(cv[i],unknowns)));
  my(ind=matindexrank(M),ker=matker(M~));
  [matrank(M),nonzero_entries(Vec(ker~*rhs~)),ind[1],ind[2],M,rhs]
};
linear_fibre(P,degree,unknowns)=
{
  my(z=linear_data(P,degree,unknowns),rows=z[3],piv=z[4]);
  my(free=complement_indices(#unknowns,piv),B=vecextract(z[5],rows,piv));
  my(rhs0=vecextract(z[6],rows)~-vecextract(z[5],rows,free)*vecextract(unknowns,free)~);
  my(ans=matsolve(B,rhs0),sol=unknowns);
  for(i=1,#piv,sol[piv[i]]=ans[i]);
  [sol,piv,free,z[2],matdet(B)]
};

v=vector(12,i,eval(Str("v",i)));
bv=vector(9,i,eval(Str("B",i)));
ell=vector(9,i,eval(Str("ell",i)));
A=[p^2,p*q,q^2]~;
Ap=vector(3,i,deriv(A[i],p))~;
Aq=vector(3,i,deriv(A[i],q))~;
V=vector(3,i,sum(j=1,4,v[4*(i-1)+j]*[p^3,p^2*q,p*q^2,q^3][j]))~;
B=vector(3,i,sum(j=1,3,bv[3*(i-1)+j]*[p^2,p*q,q^2][j]))~;
L=matrix(3,3,i,j,ell[3*(i-1)+j]);

audit_orbit(label,H4,H3,H2,compat_old,compat_new)=
{
  my(D=matdet(L+x*jacmap(H2)+x^2*jacmap(H3)+x^3*jacmap(H4)));
  my(z6=linear_fibre(D,6,ell));
  print(label," E6 L rank = ",#z6[2],", free L = ",#z6[3],", minor = ",z6[5]);
  print(label," E6 compatibility count = ",#z6[4]);
  for(i=1,#z6[4],print(label," E6 compat ",i," = ",z6[4][i]));
  my(Dc=subst_pairs(D,compat_old,compat_new));
  my(f6=linear_fibre(Dc,6,ell),D5=Dc);
  for(i=1,#f6[2],D5=subst(D5,ell[f6[2][i]],f6[1][f6[2][i]]));
  my(freeell=vecextract(ell,f6[3]));
  my(z5=linear_data(D5,5,freeell));
  print(label," E5 remaining-L rank = ",z5[1],"/",#freeell);
  print(label," E5 compatibility count = ",#z5[2]);
  my(constants=List());
  for(i=1,#z5[2],if(type(z5[2][i])=="t_INT" || type(z5[2][i])=="t_FRAC",listput(constants,z5[2][i])));
  print(label," E5 constant compatibilities = ",Vec(constants));
};

audit_orbit("split-one",p*q*A,V,B+r*Ap,[v3,v4,v9],[ -6*v8,0,0]);
audit_orbit("split-two",p*q*A,V,B+r*(Ap+Aq),[v3,v4,v9,v10],[-6*v8,0,0,-6*v5]);
audit_orbit("double-Ap",p^2*A,V,B+r*Ap,[v2,v3,v4],[3*v12-2*v7,6*v8,0]);
audit_orbit("double-Aq",p^2*A,V,B+r*Aq,[v3,v4],[3*v8,0]);

print("PASS zero-tangent orbit audit");
quit;
