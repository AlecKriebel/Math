\\ Hostile, independent PARI exploration of complete binary endgame fibres.
\\ This file intentionally does not import or execute the legacy checkers.

default(parisizemax, 2000000000);
allocatemem(300000000);

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
  polcoef(polcoef(polcoef(P,ex[3],r),ex[2],q),ex[1],p);

coeff_vector(P, mons) = vector(#mons,i,coeff_at(P,mons[i]));

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

linear_data(P, degree, unknowns) =
{
  my(E=polcoef(P,degree,x), cv=coeff_vector(E,mon_exponents(degree)));
  my(M=matrix(#cv,#unknowns,i,j,deriv(cv[i],unknowns[j])));
  my(rhs=-vector(#cv,i,zero_vars(cv[i],unknowns)));
  my(ind=matindexrank(M), ker=matker(M~));
  [matrank(M),nonzero_entries(Vec(ker~*rhs~)),ind[1],ind[2],M,rhs]
};

linear_fibre(P, degree, unknowns) =
{
  my(z=linear_data(P,degree,unknowns));
  my(rows=z[3], piv=z[4], free=complement_indices(#unknowns,piv));
  my(B=vecextract(z[5],rows,piv));
  my(rhs0);
  if(#free==0,rhs0=vecextract(z[6],rows)~,rhs0=vecextract(z[6],rows)~-vecextract(z[5],rows,free)*vecextract(unknowns,free)~);
  my(ans=matsolve(B,rhs0), sol=unknowns);
  for(i=1,#piv,sol[piv[i]]=ans[i]);
  [sol,piv,free,z[2],matdet(B)]
};

v=vector(12,i,eval(Str("v",i)));
w=vector(18,i,eval(Str("w",i)));
ell=vector(9,i,eval(Str("ell",i)));
A=[p^2,p*q,q^2]~;
Ap=vector(3,i,deriv(A[i],p))~;
Aq=vector(3,i,deriv(A[i],q))~;
V=vector(3,i,sum(j=1,4,v[4*(i-1)+j]*[p^3,p^2*q,p*q^2,q^3][j]))~;
H2=vector(3,i,sum(j=1,6,w[6*(i-1)+j]*[p^2,p*q,q^2,p*r,q*r,r^2][j]))~;
L=matrix(3,3,i,j,ell[3*(i-1)+j]);

\\ Certified E7 split fibre, specialized to opposite weights a=1,d=-1.
split_H4=p*q*A;
split_H3=V+r*(p*Ap-q*Aq);
split_w4=             v2 + 2*v7 - 3*v12 + 2*w11;
split_w5=            -v3 + 6*v8;
split_w6=0;
split_w10= -3*v1/2 + v6 + v11/2 + w17/2;
split_w12=-2;
split_w16= -6*v5 + v10;
split_w18=0;
split_H2=subst_pairs(H2,[w4,w5,w6,w10,w12,w16,w18],[split_w4,split_w5,split_w6,split_w10,split_w12,split_w16,split_w18]);
split_H3=subst_pairs(split_H3,[v4,v9],[0,0]);
split_H2=subst_pairs(split_H2,[v4,v9],[0,0]);
split_D=matdet(L+x*jacmap(split_H2)+x^2*jacmap(split_H3)+x^3*jacmap(split_H4));
print("START opposite E6 from full E7 fibre");
opp6=linear_fibre(split_D,6,ell);
print("opposite E6 ell rank = ",#opp6[2]);
print("opposite E6 ell pivots = ",opp6[2]);
print("opposite E6 ell free = ",opp6[3]);
print("opposite E6 ell pivot determinant = ",opp6[5]);
print("opposite E6 nonzero compatibility count = ",#opp6[4]);
for(i=1,#opp6[4],print("opposite E6 compat ",i," = ",opp6[4][i]));

opp_old=[v3,v8,v5,v10,w3,w13,v2,v1];
opp_new=[0,0,0,0,0,0,6*v7-9*v12+4*w11,(2*v6-3*v11-2*w17)/3];
opp_Dc=subst_pairs(split_D,opp_old,opp_new);
opp6c=linear_fibre(opp_Dc,6,ell);
opp_D5=opp_Dc;
for(i=1,#opp6c[2],opp_D5=subst(opp_D5,ell[opp6c[2][i]],opp6c[1][opp6c[2][i]]));
opp_ell_free=vecextract(ell,opp6c[3]);
opp5=linear_data(opp_D5,5,opp_ell_free);
print("opposite E6 radical fibre dimension H3+H2 = 13");
print("opposite E5 remaining-ell rank = ",opp5[1]);
print("opposite E5 remaining-ell count = ",#opp_ell_free);
print("opposite E5 nonzero compatibility count = ",#opp5[2]);
for(i=1,min(4,#opp5[2]),print("opposite E5 compat ",i," = ",opp5[2][i]));

\\ Double-root semisimple tangent a=1,d=c=0, with full E7 fibre.
double_H4=p^2*A;
semi_H3=V+r*p*Ap;
semi_w4=3*v1/2-v6-v11/2+2*w11;
semi_w5=v2/2+v7-3*v12/2;
semi_w6=1;
semi_w10=3*v5/2-v10/4+w17/2;
semi_w12=0;
semi_w16=3*v9/2;
semi_w18=0;
semi_H3=subst_pairs(semi_H3,[v4,v3],[0,6*v8]);
semi_H2=subst_pairs(H2,[w4,w5,w6,w10,w12,w16,w18],[semi_w4,semi_w5,semi_w6,semi_w10,semi_w12,semi_w16,semi_w18]);
semi_H2=subst_pairs(semi_H2,[v4,v3],[0,6*v8]);
semi_D=matdet(L+x*jacmap(semi_H2)+x^2*jacmap(semi_H3)+x^3*jacmap(double_H4));
print("START semisimple E6 from full E7 fibre");
semi6=linear_fibre(semi_D,6,ell);
print("semisimple E6 ell rank = ",#semi6[2]);
print("semisimple E6 ell pivots = ",semi6[2]);
print("semisimple E6 ell free = ",semi6[3]);
print("semisimple E6 ell pivot determinant = ",semi6[5]);
print("semisimple E6 nonzero compatibility count = ",#semi6[4]);
for(i=1,#semi6[4],print("semisimple E6 compat ",i," = ",semi6[4][i]));
semi_old0=[v8,v9,v2,w3,v1,v5];
semi_new0=[0,0,2*v7-9*v12,v7^2-6*v7*v12,2*v6+5*v11/3-16*w11/3,v10/2-4*w17/3];
semi_c6=subst_pairs(semi6[4][6],semi_old0,semi_new0);
semi_w9=-subst(semi_c6,w9,0)/deriv(semi_c6,w9);
semi_old=concat(semi_old0,[w9]);
semi_new=concat(semi_new0,[semi_w9]);
semi_Dc=subst_pairs(semi_D,semi_old,semi_new);
semi6c=linear_fibre(semi_Dc,6,ell);
semi_D5=semi_Dc;
for(i=1,#semi6c[2],semi_D5=subst(semi_D5,ell[semi6c[2][i]],semi6c[1][semi6c[2][i]]));
semi_ell_free=vecextract(ell,semi6c[3]);
semi5=linear_fibre(semi_D5,5,semi_ell_free);
print("semisimple E6 radical fibre dimension H3+H2 = 14");
print("semisimple E5 remaining-ell rank = ",#semi5[2],"/",#semi_ell_free,", minor = ",semi5[5]);
print("semisimple E5 compatibility count = ",#semi5[4]);
for(i=1,#semi5[4],print("semisimple E5 compat ",i," = ",semi5[4][i]));
semi_Dc5=subst_pairs(semi_Dc,[v12,v11,w17,w15],[0,2*w11,0,w11^2]);
semi6f=linear_fibre(semi_Dc5,6,ell);
semi_Dafter6=semi_Dc5;
for(i=1,#semi6f[2],semi_Dafter6=subst(semi_Dafter6,ell[semi6f[2][i]],semi6f[1][semi6f[2][i]]));
semi_free6=vecextract(ell,semi6f[3]);
semi5f=linear_fibre(semi_Dafter6,5,semi_free6);
semi_Dafter5=semi_Dafter6;
for(i=1,#semi5f[2],semi_Dafter5=subst(semi_Dafter5,semi_free6[semi5f[2][i]],semi5f[1][semi5f[2][i]]));
semi_free5=vecextract(semi_free6,semi5f[3]);
semi4f=linear_fibre(semi_Dafter5,4,semi_free5);
print("semisimple E5 radical fibre dimension H3+H2 = 10");
print("semisimple E4 remaining-ell rank = ",#semi4f[2],"/",#semi_free5,", minor = ",semi4f[5]);
print("semisimple E4 compatibility count = ",#semi4f[4]);
semi_Lsol=L;
for(i=1,#semi6f[2],semi_Lsol=subst(semi_Lsol,ell[semi6f[2][i]],semi6f[1][semi6f[2][i]]));
for(i=1,#semi5f[2],semi_Lsol=subst(semi_Lsol,semi_free6[semi5f[2][i]],semi5f[1][semi5f[2][i]]));
for(i=1,#semi4f[2],semi_Lsol=subst(semi_Lsol,semi_free5[semi4f[2][i]],semi4f[1][semi4f[2][i]]));
print("semisimple solved det(L) = ",matdet(semi_Lsol));

\\ Double-root nilpotent tangent a=d=0,c=1, with full E7 fibre.
nil_H3=V+r*p*Aq;
nil_w4=v2-4*v7+3*v12+2*w11;
nil_w5=2*v3-6*v8;
nil_w6=0;
nil_w10=v6-v11+w17/2;
nil_w12=0;
nil_w16=v10;
nil_w18=1;
nil_H3=subst(nil_H3,v4,0);
nil_H2=subst_pairs(H2,[w4,w5,w6,w10,w12,w16,w18],[nil_w4,nil_w5,nil_w6,nil_w10,nil_w12,nil_w16,nil_w18]);
nil_H2=subst(nil_H2,v4,0);
nil_D=matdet(L+x*jacmap(nil_H2)+x^2*jacmap(nil_H3)+x^3*jacmap(double_H4));
print("START nilpotent E6 from full E7 fibre");
nil6=linear_fibre(nil_D,6,ell);
print("nilpotent E6 ell rank = ",#nil6[2]);
print("nilpotent E6 ell pivots = ",nil6[2]);
print("nilpotent E6 ell free = ",nil6[3]);
print("nilpotent E6 ell pivot determinant = ",nil6[5]);
print("nilpotent E6 nonzero compatibility count = ",#nil6[4]);
for(i=1,#nil6[4],print("nilpotent E6 compat ",i," = ",nil6[4][i]));
nil_old0=[v3,v8,v7,w17];
nil_new0=[0,0,3*v12/2+w11,v11];
nil_c4=subst_pairs(nil6[4][4],nil_old0,nil_new0);
nil_w3=-subst(nil_c4,w3,0)/deriv(nil_c4,w3);
nil_old=concat(nil_old0,[w3]);
nil_new=concat(nil_new0,[nil_w3]);
nil_Dc=subst_pairs(nil_D,nil_old,nil_new);
nil6c=linear_fibre(nil_Dc,6,ell);
nil_D5=nil_Dc;
for(i=1,#nil6c[2],nil_D5=subst(nil_D5,ell[nil6c[2][i]],nil6c[1][nil6c[2][i]]));
nil_ell_free=vecextract(ell,nil6c[3]);
nil5=linear_fibre(nil_D5,5,nil_ell_free);
print("nilpotent E6 radical fibre dimension H3+H2 = 17");
print("nilpotent E5 remaining-ell rank = ",#nil5[2],"/",#nil_ell_free,", minor = ",nil5[5]);
print("nilpotent E5 compatibility count = ",#nil5[4]);
for(i=1,#nil5[4],print("nilpotent E5 compat ",i," = ",nil5[4][i]));

\\ Nilpotent K != 0 component (K=w11).
nil_nonzero_D=subst_pairs(nil_Dc,[v12,v2,w9,w15,v1],[0,2*w11,w11*v11/2,v11^2/4,2*v6-v11]);
nilnz6=linear_fibre(nil_nonzero_D,6,ell);
nilnz_after6=nil_nonzero_D;
for(i=1,#nilnz6[2],nilnz_after6=subst(nilnz_after6,ell[nilnz6[2][i]],nilnz6[1][nilnz6[2][i]]));
nilnz_free6=vecextract(ell,nilnz6[3]);
nilnz5=linear_fibre(nilnz_after6,5,nilnz_free6);
nilnz_after5=nilnz_after6;
for(i=1,#nilnz5[2],nilnz_after5=subst(nilnz_after5,nilnz_free6[nilnz5[2][i]],nilnz5[1][nilnz5[2][i]]));
nilnz_free5=vecextract(nilnz_free6,nilnz5[3]);
nilnz4=linear_fibre(nilnz_after5,4,nilnz_free5);
nilnz_L=L;
for(i=1,#nilnz6[2],nilnz_L=subst(nilnz_L,ell[nilnz6[2][i]],nilnz6[1][nilnz6[2][i]]));
for(i=1,#nilnz5[2],nilnz_L=subst(nilnz_L,nilnz_free6[nilnz5[2][i]],nilnz5[1][nilnz5[2][i]]));
for(i=1,#nilnz4[2],nilnz_L=subst(nilnz_L,nilnz_free5[nilnz4[2][i]],nilnz4[1][nilnz4[2][i]]));
print("nilpotent K!=0 ranks E6/E5/E4 = ",#nilnz6[2],"/",#nilnz5[2],"/",#nilnz4[2]);
print("nilpotent K!=0 minors E6/E5/E4 = ",nilnz6[5],"/",nilnz5[5],"/",nilnz4[5]);
print("nilpotent K!=0 final compatibility count = ",#nilnz4[4]);
for(i=1,#nilnz4[4],print("nilpotent K!=0 E4 compat ",i," = ",nilnz4[4][i]));
nilnz_Dfinal=subst_pairs(nil_nonzero_D,[v5,v9],[v10/2,0]);
nilnz6f=linear_fibre(nilnz_Dfinal,6,ell);
nilnz_Df6=nilnz_Dfinal;
for(i=1,#nilnz6f[2],nilnz_Df6=subst(nilnz_Df6,ell[nilnz6f[2][i]],nilnz6f[1][nilnz6f[2][i]]));
nilnz_f6=vecextract(ell,nilnz6f[3]);
nilnz5f=linear_fibre(nilnz_Df6,5,nilnz_f6);
nilnz_Df5=nilnz_Df6;
for(i=1,#nilnz5f[2],nilnz_Df5=subst(nilnz_Df5,nilnz_f6[nilnz5f[2][i]],nilnz5f[1][nilnz5f[2][i]]));
nilnz_f5=vecextract(nilnz_f6,nilnz5f[3]);
nilnz4f=linear_fibre(nilnz_Df5,4,nilnz_f5);
nilnz_Lfinal=L;
for(i=1,#nilnz6f[2],nilnz_Lfinal=subst(nilnz_Lfinal,ell[nilnz6f[2][i]],nilnz6f[1][nilnz6f[2][i]]));
for(i=1,#nilnz5f[2],nilnz_Lfinal=subst(nilnz_Lfinal,nilnz_f6[nilnz5f[2][i]],nilnz5f[1][nilnz5f[2][i]]));
for(i=1,#nilnz4f[2],nilnz_Lfinal=subst(nilnz_Lfinal,nilnz_f5[nilnz4f[2][i]],nilnz4f[1][nilnz4f[2][i]]));
print("nilpotent K!=0 post-E4 compatibility count = ",#nilnz4f[4]);
print("nilpotent K!=0 final solved det(L) = ",matdet(nilnz_Lfinal));

\\ Nilpotent K = 0 component.
nil_zero_D=subst_pairs(nil_Dc,[v12,w11,w9,w15],[0,0,0,v11^2/4]);
nilz6=linear_fibre(nil_zero_D,6,ell);
nilz_after6=nil_zero_D;
for(i=1,#nilz6[2],nilz_after6=subst(nilz_after6,ell[nilz6[2][i]],nilz6[1][nilz6[2][i]]));
nilz_free6=vecextract(ell,nilz6[3]);
nilz5=linear_fibre(nilz_after6,5,nilz_free6);
nilz_L=L;
for(i=1,#nilz6[2],nilz_L=subst(nilz_L,ell[nilz6[2][i]],nilz6[1][nilz6[2][i]]));
for(i=1,#nilz5[2],nilz_L=subst(nilz_L,nilz_free6[nilz5[2][i]],nilz5[1][nilz5[2][i]]));
print("nilpotent K=0 ranks E6/E5 = ",#nilz6[2],"/",#nilz5[2]);
print("nilpotent K=0 minors E6/E5 = ",nilz6[5],"/",nilz5[5]);
print("nilpotent K=0 E5 compatibility count = ",#nilz5[4]);
if(nilz_L[1,2]!=v11*nilz_L[1,3]/2 || nilz_L[2,2]!=v11*nilz_L[2,3]/2 || nilz_L[3,2]!=v11*nilz_L[3,3]/2,error("nilpotent K=0 column relation failed"));
print("nilpotent K=0 column relation PASS");
print("nilpotent K=0 solved det(L) = ",matdet(nilz_L));

\\ Split-root scalar tangent a=d=1, with full E7 fibre.
ss_H3=V+2*r*A;
ss_w4=3*v2/2-3*v7+3*v12/2+2*w11;
ss_w5=3*v3/2-3*v8;
ss_w6=0;
ss_w10=-3*v1/4+3*v6/2-3*v11/4+w17/2;
ss_w12=0;
ss_w16=-3*v5+3*v10/2;
ss_w18=0;
ss_H3=subst_pairs(ss_H3,[v4,v9],[0,0]);
ss_H2=subst_pairs(H2,[w4,w5,w6,w10,w12,w16,w18],[ss_w4,ss_w5,ss_w6,ss_w10,ss_w12,ss_w16,ss_w18]);
ss_H2=subst_pairs(ss_H2,[v4,v9],[0,0]);
ss_D=matdet(L+x*jacmap(ss_H2)+x^2*jacmap(ss_H3)+x^3*jacmap(split_H4));
print("START split-scalar E6 from full E7 fibre");
ss6=linear_fibre(ss_D,6,ell);
print("split-scalar E6 ell rank = ",#ss6[2],", minor = ",ss6[5]);
print("split-scalar E6 compatibility count = ",#ss6[4]);
for(i=1,#ss6[4],print("split-scalar E6 compat ",i," = ",ss6[4][i]));
ss_old=[v8,v3,v2,w3,v1,v5,v10,w13];
ss_new=[0,0,2*v7-v12,0,2*v6-v11,0,0,0];
ss_Dc=subst_pairs(ss_D,ss_old,ss_new);
ss6c=linear_fibre(ss_Dc,6,ell);
ss_D5=ss_Dc;
for(i=1,#ss6c[2],ss_D5=subst(ss_D5,ell[ss6c[2][i]],ss6c[1][ss6c[2][i]]));
ss_free6=vecextract(ell,ss6c[3]);
ss5=linear_fibre(ss_D5,5,ss_free6);
print("split-scalar E6 fibre dimension H3+H2 = 13");
print("split-scalar E5 L rank = ",#ss5[2],"/",#ss_free6,", minor = ",ss5[5]);
print("split-scalar E5 compatibility count = ",#ss5[4]);
for(i=1,#ss5[4],print("split-scalar E5 compat ",i," = ",ss5[4][i]));
ss_w2=-subst(ss5[4][1],w2,0)/deriv(ss5[4][1],w2);
ss_w1=-subst(ss5[4][2],w1,0)/deriv(ss5[4][2],w1);
ss_w7=-subst(ss5[4][3],w7,0)/deriv(ss5[4][3],w7);
ss_Dc5=subst_pairs(ss_Dc,[w2,w1,w7],[ss_w2,ss_w1,ss_w7]);
ss6f=linear_fibre(ss_Dc5,6,ell);
ss_Df6=ss_Dc5;
for(i=1,#ss6f[2],ss_Df6=subst(ss_Df6,ell[ss6f[2][i]],ss6f[1][ss6f[2][i]]));
ss_f6=vecextract(ell,ss6f[3]);
ss5f=linear_fibre(ss_Df6,5,ss_f6);
ss_Df5=ss_Df6;
for(i=1,#ss5f[2],ss_Df5=subst(ss_Df5,ss_f6[ss5f[2][i]],ss5f[1][ss5f[2][i]]));
ss_f5=vecextract(ss_f6,ss5f[3]);
ss4=linear_data(ss_Df5,4,ss_f5);
print("split-scalar E5 fibre dimension H3+H2 = 10");
print("split-scalar E4 remaining-L rank = ",ss4[1],"/",#ss_f5);
print("split-scalar E4 compatibility count = ",#ss4[2]);
print("split-scalar E4 square cert 1 = ",ss4[2][1]);
print("split-scalar E4 square cert 2 = ",ss4[2][6]);
ss_X=v11-v6;
ss_Y=v12-v7;
ss_w11=2*(v7-v12);
ss_w17=4*(v11-v6);
ss_w9=v12*(v7-v12);
ss_w14=2*v6*ss_X-ss_X^2;
ss_w15=w8+v6*ss_Y+v7*ss_X+ss_X*ss_Y;
ss_E4raw=coeff_vector(polcoef(ss_Df5,4,x),mon_exponents(4));
ss_after_squares=nonzero_entries(subst_pairs(ss_E4raw,[w11,w17],[ss_w11,ss_w17]));
print("split-scalar E4 equations after two square conditions = ",#ss_after_squares);
for(i=1,min(3,#ss_after_squares),print("split-scalar E4 residual ",i," = ",ss_after_squares[i]));
ss_after_w9=nonzero_entries(subst(ss_after_squares,w9,ss_w9));
print("split-scalar E4 equations after B2 condition = ",#ss_after_w9);
for(i=1,#ss_after_w9,print("split-scalar E4 after-B2 ",i," = ",ss_after_w9[i]));
ss_after_w14=nonzero_entries(subst(ss_after_w9,w14,ss_w14));
print("split-scalar E4 equations after B0 condition = ",#ss_after_w14);
for(i=1,#ss_after_w14,print("split-scalar E4 after-B0 ",i," = ",ss_after_w14[i]));
ss_Dfinal=subst_pairs(ss_Df5,[w11,w17,w9,w14,w15],[ss_w11,ss_w17,ss_w9,ss_w14,ss_w15]);
print("split-scalar final E4 coefficient = ",polcoef(ss_Dfinal,4,x));
print("split-scalar final E3 coefficient = ",polcoef(ss_Dfinal,3,x));
print("split-scalar final free L entries = ",ss_f5);
ss_Q=w8*ss_Y+v6*ss_Y^2+ell5;
ss_R=-2*w8*ss_X-2*v6*ss_X*ss_Y+v7*ss_X^2+ss_X^2*ss_Y+ell8;
ss_P=v7*ss_X^2*ss_Y+ss_X^2*ss_Y^2+2*ss_X*ell5+ss_Y*ell8;
if(polcoef(ss_Dfinal,2,x)!=(ss_R*p-2*ss_Q*q)^2,error("split scalar E2 square mismatch"));
if(polcoef(ss_Dfinal,0,x)!=ss_P^2,error("split scalar det(L) square mismatch"));
if(ss_P!=2*ss_X*ss_Q+ss_Y*ss_R,error("split scalar ideal identity mismatch"));
print("split-scalar E2 square and det(L) ideal identity PASS");

\\ Double-root scalar tangent a=d=1,c=0, with full E7 fibre.
ds_H3=V+2*r*A;
ds_w4=3*v1/2-3*v6+3*v11/2+2*w11;
ds_w5=3*v2/2-3*v7+3*v12/2;
ds_w6=0;
ds_w10=3*v5/2-3*v10/4+w17/2;
ds_w12=0;
ds_w16=3*v9/2;
ds_w18=0;
ds_H3=subst_pairs(ds_H3,[v4,v3],[0,2*v8]);
ds_H2=subst_pairs(H2,[w4,w5,w6,w10,w12,w16,w18],[ds_w4,ds_w5,ds_w6,ds_w10,ds_w12,ds_w16,ds_w18]);
ds_H2=subst_pairs(ds_H2,[v4,v3],[0,2*v8]);
ds_D=matdet(L+x*jacmap(ds_H2)+x^2*jacmap(ds_H3)+x^3*jacmap(double_H4));
print("START double-scalar E6 from full E7 fibre");
ds6=linear_fibre(ds_D,6,ell);
print("double-scalar E6 ell rank = ",#ds6[2],", minor = ",ds6[5]);
print("double-scalar E6 compatibility count = ",#ds6[4]);
for(i=1,#ds6[4],print("double-scalar E6 compat ",i," = ",ds6[4][i]));
ds_old0=[v8,v2,w3,v1,v5,v9];
ds_new0=[0,2*v7-v12,3*(v7-v12)^2,2*v6-v11,v10/2,0];
ds_c6=subst_pairs(ds6[4][6],ds_old0,ds_new0);
ds_w2=-subst(ds_c6,w2,0)/deriv(ds_c6,w2);
ds_old=concat(ds_old0,[w2]);
ds_new=concat(ds_new0,[ds_w2]);
ds_Dc=subst_pairs(ds_D,ds_old,ds_new);
ds6c=linear_fibre(ds_Dc,6,ell);
ds_D5=ds_Dc;
for(i=1,#ds6c[2],ds_D5=subst(ds_D5,ell[ds6c[2][i]],ds6c[1][ds6c[2][i]]));
ds_free6=vecextract(ell,ds6c[3]);
ds5=linear_fibre(ds_D5,5,ds_free6);
print("double-scalar E6 fibre dimension H3+H2 = 14");
print("double-scalar E5 L rank = ",#ds5[2],"/",#ds_free6,", minor = ",ds5[5]);
print("double-scalar E5 compatibility count = ",#ds5[4]);
for(i=1,#ds5[4],print("double-scalar E5 compat ",i," = ",ds5[4][i]));
ds_c5=subst_pairs(ds5[4],[v7],[v12]);
ds_w1=-subst(ds_c5[5],w1,0)/deriv(ds_c5[5],w1);
ds_w7=-subst(ds_c5[6],w7,0)/deriv(ds_c5[6],w7);
ds_w13=-subst(ds_c5[7],w13,0)/deriv(ds_c5[7],w13);
ds_Dc5=subst_pairs(ds_Dc,[v7,w1,w7,w13],[v12,ds_w1,ds_w7,ds_w13]);
ds6f=linear_fibre(ds_Dc5,6,ell);
ds_Df6=ds_Dc5;
for(i=1,#ds6f[2],ds_Df6=subst(ds_Df6,ell[ds6f[2][i]],ds6f[1][ds6f[2][i]]));
ds_f6=vecextract(ell,ds6f[3]);
ds5f=linear_fibre(ds_Df6,5,ds_f6);
ds_Df5=ds_Df6;
for(i=1,#ds5f[2],ds_Df5=subst(ds_Df5,ds_f6[ds5f[2][i]],ds5f[1][ds5f[2][i]]));
ds_f5=vecextract(ds_f6,ds5f[3]);
ds4=linear_data(ds_Df5,4,ds_f5);
print("double-scalar E5 fibre dimension H3+H2 = 10");
print("double-scalar E4 remaining-L rank = ",ds4[1],"/",#ds_f5);
print("double-scalar E4 compatibility count = ",#ds4[2]);
print("double-scalar E4 square cert 1 = ",ds4[2][1]);
print("double-scalar E4 square cert 2 = ",ds4[2][6]);
ds_X=v11-v6;
ds_Z=v10;
ds_w11=-2*ds_X;
ds_w17=2*ds_Z;
ds_w9=-v12*ds_X;
ds_w14=v11*ds_Z;
ds_w15=w8+v6*ds_X+v12*ds_Z/2+ds_X^2;
ds_E4raw=coeff_vector(polcoef(ds_Df5,4,x),mon_exponents(4));
ds_after_squares=nonzero_entries(subst_pairs(ds_E4raw,[w11,w17],[ds_w11,ds_w17]));
print("double-scalar E4 equations after two square conditions = ",#ds_after_squares);
for(i=1,min(3,#ds_after_squares),print("double-scalar E4 residual ",i," = ",ds_after_squares[i]));
ds_after_b2=nonzero_entries(subst(ds_after_squares,w9,ds_w9));
print("double-scalar E4 equations after B2 condition = ",#ds_after_b2);
for(i=1,#ds_after_b2,print("double-scalar E4 after-B2 ",i," = ",ds_after_b2[i]));
ds_after_b0=nonzero_entries(subst(ds_after_b2,w14,ds_w14));
print("double-scalar E4 equations after B0 condition = ",#ds_after_b0);
for(i=1,#ds_after_b0,print("double-scalar E4 after-B0 ",i," = ",ds_after_b0[i]));
ds_Dfinal=subst_pairs(ds_Df5,[w11,w17,w9,w14,w15],[ds_w11,ds_w17,ds_w9,ds_w14,ds_w15]);
print("double-scalar final E4 coefficient = ",polcoef(ds_Dfinal,4,x));
print("double-scalar final E3 coefficient = ",polcoef(ds_Dfinal,3,x));
print("double-scalar final free L entries = ",ds_f5);
ds_Q=w8*ds_X+v6*ds_X^2+ds_X^3+ell5;
ds_R=-4*w8*ds_Z-4*v6*ds_X*ds_Z+v12*ds_Z^2-4*ds_X^2*ds_Z+4*ell8;
ds_P=v12*ds_X*ds_Z^2+4*ds_X*ell8+4*ds_Z*ell5;
if(polcoef(ds_Dfinal,2,x)!=(ds_R*p/4-2*ds_Q*q)^2,error("double scalar E2 square mismatch"));
if(polcoef(ds_Dfinal,0,x)!=ds_P^2/16,error("double scalar det(L) square mismatch"));
if(ds_P!=4*ds_Z*ds_Q+ds_X*ds_R,error("double scalar ideal identity mismatch"));
print("double-scalar E2 square and det(L) ideal identity PASS");

print("PASS hostile complete binary fixed-conic endgames");
quit;
