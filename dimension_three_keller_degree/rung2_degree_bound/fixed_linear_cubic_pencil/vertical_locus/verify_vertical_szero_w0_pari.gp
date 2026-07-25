\\ Independent PARI/GP expansion for VERTICAL_SZERO_W0_EXCLUSION.md.

checkzero(value,message) =
{
  if(value != 0,
    print(Str("FAIL: ",message));
    quit(1)
  );
};

checknonzero(value,message) =
{
  if(value == 0,
    print(Str("FAIL: ",message));
    quit(1)
  );
};

jac3(A,B,C) = matdet(matrix(3,3,i,j, \
  deriv([A,B,C][i],[x,y,z][j])));
c3(P,E) = polcoef(polcoef(polcoef(P,E[3],z),E[2],y),E[1],x);

x='x; y='y; z='z; tt='tt;
mu='mu; nu='nu; om='om; et='et;
alpha='alpha; beta='beta;
d0='d0; d1='d1; d2='d2; e0='e0; e1='e1;
a0='a0; a1='a1; a2='a2; a3='a3; a4='a4; a5='a5;
b0='b0; b1='b1; b2='b2; b3='b3; b4='b4; b5='b5;
v0='v0; v1='v1; v2='v2; v3='v3; v4='v4;
v5='v5; v6='v6; v7='v7; v8='v8; v9='v9;
L11='L11; L12='L12; L13='L13;
L21='L21; L22='L22; L23='L23;
L31='L31; L32='L32; L33='L33;

quadmons = [x^2,x*y,y^2,x*z,y*z,z^2];
cubmons = [x^3,x^2*y,x*y^2,y^3,x^2*z,x*y*z,y^2*z,x*z^2,y*z^2,z^3];
av = [a0,a1,a2,a3,a4];
ac = [a0,a1,a2,a3,a4,a5];
bc = [b0,b1,b2,b3,b4,b5];
vc = [v0,v1,v2,v3,v4,v5,v6,v7,v8,v9];

Araw = sum(i=1,6,ac[i]*quadmons[i]);
Braw = sum(i=1,6,bc[i]*quadmons[i]);
Vraw = sum(i=1,10,vc[i]*cubmons[i]);
Lraw = [L11,L12,L13;L21,L22,L23;L31,L32,L33];

ellform = mu*x+nu*y;
Wraw = z*(ellform+om*z);
Uraw = 4*z*Wraw/3;

qsf = x*y*(x-y)+z*(d0*x^2+d1*x*y+d2*y^2)+z^2*(e0*x+e1*y)+beta*z^3;
qdbl = x^2*y+z*(d0*x^2+d1*x*y+d2*y^2)+z^2*(e0*x+e1*y)+beta*z^3;
qA = x^3+y^2*z+alpha*x*z^2+beta*z^3;
qB = x^3+x*y*z+beta*z^3;
qC = x^3+y*z^2+beta*z^3;

weighteddet(q) =
{
  my(H0=[L11*x+L12*y+L13*z,L21*x+L22*y+L23*z,L31*x+L32*y+L33*z]);
  my(H1=[Araw,Braw,Wraw]);
  my(H2=[Uraw,Vraw,z^3]);
  my(H3=[z^4,z*q,0]);
  my(H=[H0,H1,H2,H3],answer=0);
  for(i=0,3,for(j=0,3,for(k=0,3, \
    answer += tt^(i+j+k)*jac3(H[i+1][1],H[j+1][2],H[k+1][3]))));
  return(answer)
};

e6sol(P) =
{
  my(R=P);
  R=subst(R,a0,2*mu^2/9);
  R=subst(R,a1,4*mu*nu/9);
  R=subst(R,a2,2*nu^2/9);
  R=subst(R,a3,4*mu*om/9+4*L31/3);
  R=subst(R,a4,4*nu*om/9+4*L32/3);
  R=subst(R,a5,et);
  return(R)
};

e6mut(P) =
{
  my(R=P);
  R=subst(R,a0,mu^2/9);
  R=subst(R,a1,4*mu*nu/9);
  R=subst(R,a2,2*nu^2/9);
  R=subst(R,a3,4*mu*om/9+4*L31/3);
  R=subst(R,a4,4*nu*om/9+4*L32/3);
  R=subst(R,a5,et);
  return(R)
};

commonzero(P) =
{
  my(R=P);
  R=subst(R,mu,0);
  R=subst(R,nu,0);
  R=subst(R,L11,4*om*L31/9);
  R=subst(R,L12,4*om*L32/9);
  return(R)
};

bbranch(P) =
{
  my(R=P);
  R=subst(R,nu,0);
  R=subst(R,L32,-mu^2/9);
  R=subst(R,L31,mu*om/3);
  R=subst(R,L12,-4*mu^2*om/81);
  R=subst(R,L11,mu*(-12*L33+18*et-4*om^2)/27);
  return(R)
};

cbranch(P) =
{
  my(R=P);
  R=subst(R,nu,0);
  R=subst(R,L32,0);
  R=subst(R,L31,mu*om/3);
  R=subst(R,L12,4*mu^3/81);
  R=subst(R,L11,mu*(-12*L33+18*et-4*om^2)/27);
  return(R)
};

pivotdet(E,mons) =
  matdet(matrix(5,5,i,j,deriv(c3(E,mons[i]),av[j])));

Dsf = weighteddet(qsf);
Ddbl = weighteddet(qdbl);
DA = weighteddet(qA);
DB = weighteddet(qB);
DC = weighteddet(qC);

checkzero(polcoef(Dsf,8,tt),"squarefree E8");
checkzero(polcoef(Dsf,7,tt),"squarefree E7");
checkzero(e6sol(polcoef(Dsf,6,tt)),"squarefree E6 solution");
checknonzero(e6mut(polcoef(Dsf,6,tt)),"squarefree E6 mutation");
checkzero(polcoef(Ddbl,8,tt),"double E8");
checkzero(polcoef(Ddbl,7,tt),"double E7");
checkzero(e6sol(polcoef(Ddbl,6,tt)),"double E6 solution");
checknonzero(e6mut(polcoef(Ddbl,6,tt)),"double E6 mutation");
checkzero(polcoef(DA,8,tt),"triple A E8");
checkzero(polcoef(DA,7,tt),"triple A E7");
checkzero(e6sol(polcoef(DA,6,tt)),"triple A E6 solution");
checknonzero(e6mut(polcoef(DA,6,tt)),"triple A E6 mutation");
checkzero(polcoef(DB,8,tt),"triple B E8");
checkzero(polcoef(DB,7,tt),"triple B E7");
checkzero(e6sol(polcoef(DB,6,tt)),"triple B E6 solution");
checknonzero(e6mut(polcoef(DB,6,tt)),"triple B E6 mutation");
checkzero(polcoef(DC,8,tt),"triple C E8");
checkzero(polcoef(DC,7,tt),"triple C E7");
checkzero(e6sol(polcoef(DC,6,tt)),"triple C E6 solution");
checknonzero(e6mut(polcoef(DC,6,tt)),"triple C E6 mutation");

monsSF = [[3,0,3],[2,1,3],[2,0,4],[1,2,3],[1,1,4]];
monsA = [[3,0,3],[2,1,3],[2,0,4],[1,1,4],[0,1,5]];
monsB = [[3,0,3],[2,1,3],[2,0,4],[1,0,5],[0,1,5]];
monsC = [[3,0,3],[2,1,3],[2,0,4],[1,0,5],[0,0,6]];
checkzero(pivotdet(polcoef(Dsf,6,tt),monsSF)-3888,"squarefree E6 pivot");
checkzero(pivotdet(polcoef(Ddbl,6,tt),monsSF)-3888,"double E6 pivot");
checkzero(pivotdet(polcoef(DA,6,tt),monsA)+104976,"triple A E6 pivot");
checkzero(pivotdet(polcoef(DB,6,tt),monsB)+8748,"triple B E6 pivot");
checkzero(pivotdet(polcoef(DC,6,tt),monsC)+26244,"triple C E6 pivot");

E5sf=e6sol(polcoef(Dsf,5,tt));
E5dbl=e6sol(polcoef(Ddbl,5,tt));
E5A=e6sol(polcoef(DA,5,tt));
E5B=e6sol(polcoef(DB,5,tt));
E5C=e6sol(polcoef(DC,5,tt));

checkzero(c3(E5sf,[4,0,1])-4*mu^3/9,"squarefree mu cube");
checkzero(c3(E5sf,[0,4,1])-4*nu^3/9,"squarefree nu cube");
checkzero(c3(E5dbl,[4,0,1])-4*mu^3/9,"double mu cube");
checkzero(c3(E5dbl,[1,3,1])+8*nu^3/9,"double nu cube");
checkzero(c3(E5A,[2,2,1])+4*nu^3/3,"triple A nu cube");
checkzero(subst(c3(E5A,[2,1,2]),nu,0)-8*mu^3/9,"triple A mu cube");
checkzero(c3(E5B,[2,2,1])+4*nu^3/3,"triple B nu cube");
checkzero(c3(E5C,[2,2,1])+4*nu^3/3,"triple C nu cube");

checkzero(commonzero(E5sf),"squarefree common E5 converse");
checkzero(commonzero(E5dbl),"double common E5 converse");
checkzero(commonzero(E5A),"triple A common E5 converse");
checkzero(commonzero(E5B),"triple B common E5 converse");
checkzero(commonzero(E5C),"triple C common E5 converse");
checkzero(bbranch(E5B),"triple B E5 converse");
checkzero(cbranch(E5C),"triple C E5 converse");

E4sf=commonzero(e6sol(polcoef(Dsf,4,tt)));
E4dbl=commonzero(e6sol(polcoef(Ddbl,4,tt)));
E4A=commonzero(e6sol(polcoef(DA,4,tt)));
E4B0=commonzero(e6sol(polcoef(DB,4,tt)));
E4C0=commonzero(e6sol(polcoef(DC,4,tt)));

checkzero(c3(E4sf,[3,0,1])+4*L31^2/3,"squarefree first square");
checkzero(c3(E4sf,[0,3,1])+4*L32^2/3,"squarefree second square");
checkzero(c3(E4dbl,[3,0,1])+4*L31^2/3,"double first square");
checkzero(c3(E4dbl,[1,2,1])-8*L32^2/3,"double second square");
checkzero(c3(E4A,[2,1,1])-4*L32^2,"triple A first square");
checkzero(c3(E4A,[1,1,2])+8*L31^2/3,"triple A second square");
checkzero(c3(E4B0,[2,1,1])-4*L32^2,"triple B first square");
checkzero(subst(c3(E4B0,[2,0,2]),L32,0)+4*L31^2/3,"triple B second square");
checkzero(c3(E4C0,[2,1,1])-4*L32^2,"triple C first square");
checkzero(c3(E4C0,[1,0,3])+4*L31^2/3,"triple C second square");

Lcommon=commonzero(matdet(Lraw));
checkzero(subst(subst(Lcommon,L31,0),L32,0),"common branch det L");

E4B=bbranch(e6sol(polcoef(DB,4,tt)));
b400=c3(E4B,[4,0,0]);
b211=c3(E4B,[2,1,1]);
b022=c3(E4B,[0,2,2]);
checkzero(b400-4*mu^3*(mu+9*v1)/81,"triple B c400");
checkzero(b211+4*mu^3*(-mu+v1-6*v6)/27,"triple B c211");
checkzero(b022-4*mu^3*(mu+18*v6)/243,"triple B c022");
checkzero(81*b400+243*b211-729*b022-28*mu^4,"triple B E4 contradiction");

E4C=cbranch(e6sol(polcoef(DC,4,tt)));
c301=c3(E4C,[3,0,1]);
c013=c3(E4C,[0,1,3]);
checkzero(c301-4*mu^3*(-2*mu+9*v5)/81,"triple C c301");
checkzero(c013+4*mu^3*(-mu+v5)/27,"triple C c013");
checkzero(81*c301+243*c013-28*mu^4,"triple C E4 contradiction");

print("VERTICAL_SZERO_W0_PARI_PASS_C5E4A2");
quit;
