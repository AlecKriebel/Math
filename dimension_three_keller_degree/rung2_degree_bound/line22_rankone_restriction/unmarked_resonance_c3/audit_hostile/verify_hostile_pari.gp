\\ Hostile independent reconstruction of the unmarked c^2=9 resonance.
\\
\\ This intentionally rebuilds the determinant with a hand-written 3 by 3
\\ determinant, uses ascending monomial orders, and treats the E6
\\ compatibility equations as polynomial left-syzygies.

x='x; y='y; z='z; t='t;
p=x^2; q=y^2+x*z;
Pm=(p-q)^2; Pp=(p+q)^2;
R3=x*(p-3*q); Rm3=x*(p+3*q);

die(message) = { print(Str("FAIL: ",message)); quit(1); };
must(condition,message) = if(!condition,die(message));
mustzero(value,message) = must(value == 0,message);
mustequal(value,expected,message) = mustzero(value-expected,message);

detthree(M) = \
  M[1,1]*(M[2,2]*M[3,3]-M[2,3]*M[3,2]) \
 -M[1,2]*(M[2,1]*M[3,3]-M[2,3]*M[3,1]) \
 +M[1,3]*(M[2,1]*M[3,2]-M[2,2]*M[3,1]);
jmatrix(F) = matrix(3,3,i,j,deriv(F[i],[x,y,z][j]));
jacobian3(f,g,h) = detthree(jmatrix([f,g,h]));
weightedcoefficient(L,H2,H3,H4,k) = polcoef( \
  detthree(jmatrix(L+t*H2+t^2*H3+t^3*H4)),k,t);

coefficient(f,a,b,c) = polcoef(polcoef(polcoef(f,a,x),b,y),c,z);
coeffexp(f,e) = coefficient(f,e[1],e[2],e[3]);
monomial(e) = x^e[1]*y^e[2]*z^e[3];

\\ Deliberately opposite to the package's descending order.
ascendingexponents(d) = {
  my(out=List());
  for(i=0,d,
    for(j=0,d-i,
      listput(out,[i,j,d-i-j])
    )
  );
  Vec(out)
};

form(c,e) = sum(i=1,#c,c[i]*monomial(e[i]));
substituteall(value,vars,vals) = {
  my(out=value);
  for(i=1,#vars,out=subst(out,vars[i],vals[i]));
  out
};
coefficientvector(f,e) = vector(#e,i,coeffexp(f,e[i]));

\\ Rows are equations, columns are the listed variables.  The returned
\\ constant column c gives M*v+c=0.  Linearity is checked literally.
linearsystem(E,degree,vars) = {
  my(ex=ascendingexponents(degree), M, c, value, reconstructed);
  M=matrix(#ex,#vars,i,j,deriv(coeffexp(E,ex[i]),vars[j]));
  c=vector(#ex,i,substituteall( \
      coeffexp(E,ex[i]),vars,vector(#vars,j,0)))~;
  for(i=1,#ex,
    value=coeffexp(E,ex[i]);
    reconstructed=c[i]+sum(j=1,#vars,M[i,j]*vars[j]);
    mustzero(value-reconstructed, \
      Str("nonlinear lower system at degree ",degree,", row ",i))
  );
  [M,c]
};

\\ Independently clear every rational-function denominator in a computed
\\ left kernel.  The proof below does not use these vectors: it uses sparse
\\ integral syzygies.  This is a hostile check that the exploratory
\\ denominator-clearing step did not manufacture or lose a component.
auditclearedleftkernel(M,c,label) = {
  my(N=matker(M~), den, v, pairing);
  for(j=1,matsize(N)[2],
    den=1;
    for(i=1,matsize(N)[1],den*=denominator(N[i,j]));
    v=den*N[,j];
    for(i=1,#v,
      mustequal(denominator(v[i]),1, \
        Str(label,": uncleared left-kernel denominator ",j,"/",i))
    );
    mustzero(M~*v,Str(label,": cleared vector is not a left syzygy ",j));
    pairing=v~*c;
    mustequal(denominator(pairing),1, \
      Str(label,": cleared pairing still has a denominator ",j))
  );
  1
};

e2=ascendingexponents(2);
e3=ascendingexponents(3);
e6=ascendingexponents(6);
e7=ascendingexponents(7);

\\ -----------------------------------------------------------------------
\\ The c=+3 raw orbit, its complete E7 kernel, and the legal gauge.
\\ -----------------------------------------------------------------------

wc=vector(6,i,eval(Str("aw",i)));
vc=vector(10,i,eval(Str("av",i)));
uc=vector(10,i,eval(Str("au",i)));
Wraw=form(wc,e2); Vraw=form(vc,e3); Uraw=form(uc,e3);
rawvars=concat(concat(wc,vc),uc);

E7=jacobian3(Pm,Pp,Wraw)+jacobian3(Pm,Vraw,R3) \
   +jacobian3(Uraw,Pp,R3);
M7=matrix(#e7,#rawvars,i,j,deriv(coeffexp(E7,e7[i]),rawvars[j]));

mustzero(jacobian3(Pm,Pp,R3),"E8 top identity");
delta(h)=2*y*deriv(h,z)-x*deriv(h,y);
compact=2*(8*x*(p-q)*(p+q)*delta(Wraw) \
  +3*(p+q)*(q-3*p)*delta(Uraw) \
  +3*(p-q)*(p+q)*delta(Vraw));
mustzero(E7-compact,"raw E7 compact identity");
mustequal(matrank(M7),14,"raw E7 rank");

translationx=[deriv(Pm,x),deriv(Pp,x),deriv(R3,x)];
translationy=[deriv(Pm,y),deriv(Pp,y),deriv(R3,y)];
gauge=[translationy,[0,R3,0],translationx,[R3,0,0]];
quotient=[ \
  [x*q,0,0],[0,x*q,0], \
  [y*(p-q),y*(3*p-q),0], \
  [z*(p-q),z*(3*p-q),0], \
  [0,0,p], \
  [0,8*x^2*z,3*y^2], \
  [0,-8*x*y*z,3*y*z], \
  [0,-8*x*z^2,3*z^2]];
directions=concat(gauge,quotient);

\\ The column order is W,V,U, unlike the primary certificate.
directioncolumn(D)=concat( \
  concat(coefficientvector(D[3],e2),coefficientvector(D[2],e3)), \
  coefficientvector(D[1],e3))~;
K=matrix(26,12,i,j,directioncolumn(directions[j])[i]);
mustzero(M7*K,"twelve proposed E7 kernel directions");
mustequal(matrank(K),12,"E7 kernel direction independence");
mustequal(matsize(M7)[2]-matrank(M7),12,"E7 nullity");

\\ Coordinates: [xz]W, [x^3]V, [xy]W, [x^3]U.
G=matrix(4,4,i,j, \
  if(i==1,coefficient(gauge[j][3],1,0,1), \
    if(i==2,coefficient(gauge[j][2],3,0,0), \
      if(i==3,coefficient(gauge[j][3],1,1,0), \
        coefficient(gauge[j][1],3,0,0)))));
must(matdet(G)!=0,"legal four-direction gauge determinant");

\\ -----------------------------------------------------------------------
\\ Rebuild E6 from the complete normal form.
\\ -----------------------------------------------------------------------

AA='AA; BB='BB; CC='CC; DD='DD;
ee='ee; ff='ff; gg='gg; ww='ww;
u0='u0; uq='uq; du1='du1; du2='du2; du3='du3; du4='du4;
v0='v0; vq='vq; dv1='dv1; dv2='dv2; dv3='dv3; dv4='dv4;
l11='l11; l12='l12; l13='l13;
l21='l21; l22='l22; l23='l23;
l31='l31; l32='l32; l33='l33;

U3=AA*x*q+CC*y*(p-q)+DD*z*(p-q);
V3=BB*x*q+CC*y*(3*p-q)+DD*z*(3*p-q) \
  +8*ee*x^2*z-8*ff*x*y*z-8*gg*x*z^2;
W2=ww*p+3*ee*y^2+3*ff*y*z+3*gg*z^2;
U2=u0*p+uq*q+du1*x*y+du2*x*z+du3*y*z+du4*z^2;
V2=v0*p+vq*q+dv1*x*y+dv2*x*z+dv3*y*z+dv4*z^2;
H4=[Pm,Pp,0]; H3=[U3,V3,R3]; H2=[U2,V2,W2];
L=[l11*x+l12*y+l13*z, \
   l21*x+l22*y+l23*z, \
   l31*x+l32*y+l33*z];
Lmatrix=[l11,l12,l13;l21,l22,l23;l31,l32,l33];
lower=[u0,uq,du1,du2,du3,du4, \
       v0,vq,dv1,dv2,dv3,dv4,l32,l33];

E6=weightedcoefficient(L,H2,H3,H4,6);
mustzero(weightedcoefficient(L,H2,H3,H4,8),"normal-form E8");
mustzero(weightedcoefficient(L,H2,H3,H4,7),"normal-form E7");

S0=linearsystem(E6,6,lower);
mustequal(matrank(S0[1]),8,"E6 generic coefficient rank");
mustequal(matrank(concat(S0[1],S0[2])),9, \
  "E6 generic augmented rank");
auditclearedleftkernel(S0[1],S0[2],"E6/generic");
\\ This single row is an integral left syzygy: no localization.
mustequal(coefficient(E6,1,1,4),192*gg^2, \
  "E6 division-free g square");

E6g=subst(E6,gg,0);
S1=linearsystem(E6g,6,lower);
mustequal(matrank(S1[1]),8,"E6 rank after g=0");
mustequal(matrank(concat(S1[1],S1[2])),9, \
  "E6 augmented rank before f=0");
auditclearedleftkernel(S1[1],S1[2],"E6/g=0");
mustequal(-coefficient(E6g,2,1,3)+coefficient(E6g,0,5,1), \
  144*ff^2,"E6 division-free f square");

E6gf=substituteall(E6,[gg,ff],[0,0]);
S2=linearsystem(E6gf,6,lower);
mustequal(matrank(S2[1]),8,"E6 rank after g=f=0");
mustequal(matrank(concat(S2[1],S2[2])),9, \
  "E6 augmented rank before D=-2e");
auditclearedleftkernel(S2[1],S2[2],"E6/g=f=0");
mustequal( \
  coefficient(E6gf,4,1,1)-coefficient(E6gf,3,3,0) \
  -2*coefficient(E6gf,3,1,2)+coefficient(E6gf,2,3,1) \
  +coefficient(E6gf,2,1,3), \
  -48*(DD+2*ee)^2,"E6 division-free D+2e square");

E6gfd=substituteall(E6,[gg,ff,DD],[0,0,-2*ee]);
S3=linearsystem(E6gfd,6,lower);
mustequal(matrank(S3[1]),8,"E6 rank after D=-2e");
mustequal(matrank(concat(S3[1],S3[2])),9, \
  "E6 augmented rank before C=0");
auditclearedleftkernel(S3[1],S3[2],"E6/g=f=0,D=-2e");
mustequal( \
  coefficient(E6gfd,5,1,0)-coefficient(E6gfd,3,3,0) \
  -coefficient(E6gfd,3,1,2)+coefficient(E6gfd,2,3,1), \
  24*CC^2,"E6 division-free C square");

E6final=substituteall(E6,[gg,ff,DD,CC],[0,0,-2*ee,0]);
S4=linearsystem(E6final,6,lower);
mustequal(matrank(S4[1]),8,"surviving E6 rank");
mustequal(matrank(concat(S4[1],S4[2])),8, \
  "surviving E6 consistency");
auditclearedleftkernel(S4[1],S4[2],"E6/survivor");

\\ A constant eight-by-eight pivot proves that no parameter specialization
\\ lowers the rank.  Rows are selected by monomial, not package row number.
dependent=[du1,du2,du3,du4,dv1,dv2,dv3,dv4];
pivotmonomials=[[6,0,0],[5,1,0],[5,0,1],[4,2,0], \
                [4,1,1],[4,0,2],[3,3,0],[3,1,2]];
M6pivot=matrix(8,8,i,j, \
  deriv(coeffexp(E6final,pivotmonomials[i]),dependent[j]));
mustequal(matdet(M6pivot),5159780352, \
  "surviving E6 parameter-free pivot");
e6pivotdet(value)=matdet(matrix(8,8,i,j, \
  deriv(coeffexp(value,pivotmonomials[i]),dependent[j])));
mustequal(e6pivotdet(E6),5159780352,"E6 generic constant pivot");
mustequal(e6pivotdet(E6g),5159780352,"E6 g=0 constant pivot");
mustequal(e6pivotdet(E6gf),5159780352,"E6 g=f=0 constant pivot");
mustequal(e6pivotdet(E6gfd),5159780352, \
  "E6 D=-2e constant pivot");

lowercandidate=[u0,uq,0,AA*ee,0,ee^2, \
  v0,vq,-8/3*l32,BB*ee+8*ee^2-8/3*l33,0,ee^2,l32,l33];
mustzero(substituteall(E6final,lower,lowercandidate), \
  "complete surviving E6 solution");

\\ -----------------------------------------------------------------------
\\ Reconstruct the only E5 rank drop and all of its specializations.
\\ -----------------------------------------------------------------------

U3s=AA*x*q-2*ee*z*(p-q);
V3s=BB*x*q+2*ee*z*(p+q);
W2s=ww*p+3*ee*y^2;
U2s=u0*p+uq*q+AA*ee*x*z+ee^2*z^2;
V2s=v0*p+vq*q-8/3*l32*x*y \
  +(BB*ee+8*ee^2-8/3*l33)*x*z+ee^2*z^2;
H3s=[U3s,V3s,R3]; H2s=[U2s,V2s,W2s];
E5=weightedcoefficient(L,H2s,H3s,H4,5);

f1=coefficient(E5,5,0,0);
f2=coefficient(E5,4,0,1);
f3=coefficient(E5,3,0,2);
columnvariables=[l12,l22,l32];
Mcolumn=matrix(3,3,i,j,deriv([f1,f2,f3][i],columnvariables[j]));
resonance=-6*AA+3*BB+48*ee+16*ww;
mustequal(matdet(Mcolumn),-96*resonance, \
  "E5 resonance determinant");
\\ A constant 2 by 2 minor makes the rank exactly two on resonance.
mustequal(matdet(vecextract(Mcolumn,[1,2],[1,2])),72, \
  "E5 resonance rank-two floor");

\\ Off resonance the homogeneous three-by-three system kills column two.
mustzero(substituteall(matdet(Lmatrix), \
  [l12,l22,l32],[0,0,0]), \
  "zero second column forces det L=0");
\\ On resonance, the l32=0 subbranch has two literal numeric pivots.
mustequal(subst(f2,l32,0),12*l12, \
  "E5 resonant l32=0 first numeric pivot");
mustequal(substituteall(f3,[l32,l12],[0,0]),6*l22, \
  "E5 resonant l32=l12=0 second numeric pivot");

BBres=2*AA-16*ee-16/3*ww;
E5res=subst(E5,BB,BBres);
e5vars=[l12,l13,l22,l23];
S5=linearsystem(E5res,5,e5vars);
mustequal(matrank(S5[1]),4,"full resonant E5 rank");
pivot5=[[5,0,0],[4,1,0],[4,0,1],[3,1,1]];
M5pivot=matrix(4,4,i,j, \
  deriv(coeffexp(E5res,pivot5[i]),e5vars[j]));
mustequal(matdet(M5pivot),20736, \
  "full resonant E5 parameter-free pivot");

l12s=-AA*l32/2;
l22s=(-15*AA+96*ee+32*ww)*l32/18;
l13s=AA*(3*ee^2-l33)/2+ee*uq;
l23s=(15*AA-96*ee-32*ww)*(3*ee^2-l33)/18+ee*vq;
e5candidate=[l12s,l13s,l22s,l23s];
mustzero(substituteall(E5res,e5vars,e5candidate), \
  "complete resonant E5 solution");
\\ All denominators are constants; no parameter divisor has been cleared.
mustequal(vector(#e5candidate,i,denominator(e5candidate[i])), \
  [1,1,1,1],"resonant E5 solution has no parameter denominators");

\\ -----------------------------------------------------------------------
\\ Literal E4 exit on the only determinant-compatible branch.
\\ -----------------------------------------------------------------------

E4=weightedcoefficient(L,H2s,H3s,H4,4);
E4res=substituteall(E4,[BB,l12,l13,l22,l23], \
  [BBres,l12s,l13s,l22s,l23s]);
mustequal(coefficient(E4res,2,0,2), \
  16/3*l32*(3*ee^2-l33),"E4 first literal pivot");
E4last=subst(E4res,l33,3*ee^2);
mustequal(coefficient(E4last,3,1,0),16/3*l32^2, \
  "E4 final literal pivot");

\\ -----------------------------------------------------------------------
\\ Exact c=+3 <-> c=-3 orbit equivalence over C.
\\ -----------------------------------------------------------------------

ii=I;
T(value)=substituteall(value,[x,y,z],[x,ii*y,-z]);
mustzero(T(p)-p,"sign symmetry fixes p");
mustzero(T(q)+q,"sign symmetry negates q");
mustzero(T(Pm)-Pp,"sign symmetry swaps first quartic");
mustzero(T(Pp)-Pm,"sign symmetry swaps second quartic");
mustzero(T(R3)-Rm3,"sign symmetry sends c=+3 to c=-3");
mustzero(T(Rm3)-R3,"sign symmetry sends c=-3 to c=+3");
Tmatrix=[1,0,0;0,ii,0;0,0,-1];
targetswap=[0,1,0;1,0,0;0,0,1];
mustequal(matdet(Tmatrix),-ii,"source symmetry determinant");
mustequal(matdet(targetswap),-1,"target swap determinant");
mustequal(matdet(Tmatrix)*matdet(targetswap),ii, \
  "nonzero Keller-determinant scaling");
mustzero(jacobian3(Pm,Pp,Rm3),"c=-3 E8 identity");

print("ALL HOSTILE UNMARKED c^2=9 PARI AUDIT CHECKS PASSED");
quit;
