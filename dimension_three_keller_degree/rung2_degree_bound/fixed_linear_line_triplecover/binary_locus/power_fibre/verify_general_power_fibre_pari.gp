\\ Independent PARI/GP determinant replay for the fixed-linear binary
\\ power fibre.  This file does not import expressions from the SymPy suite.

default(parisizemax,512000000);
allocatemem(128000000);

checkzero(value,message) =
{
  if(value != 0,
    print(Str("FAIL: ",message));
    quit(1)
  );
};

checkeq(left,right,message) = checkzero(left-right,message);
checktrue(value,message) =
{
  if(!value,
    print(Str("FAIL: ",message));
    quit(1)
  );
};

substmany(f,vars,vals) =
{
  my(g=f);
  if(#vars != #vals,error("substmany length mismatch"));
  for(i=1,#vars,g=subst(g,vars[i],vals[i]));
  g;
};

jacmap(V) = matrix(3,3,i,j,deriv(V[i],[p,q,r][j]));
cf(f,ep,eq,er) = polcoef(polcoef(polcoef(f,er,r),eq,q),ep,p);
tdeg2(f,a,b) = poldegree(subst(subst(f,a,ww*a),b,ww*b),ww);

{
C3=d0*p^3+d1*p^2*q+q^3;
Dq=deriv(C3,q);

T0=c0*p^2+c1*p*q+c2*q^2;
U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
A0=x0*p^2+x1*p*q+x2*q^2;
B0=y0*p^2+y1*p*q+y2*q^2;

T=T0+r*(tp*p+tq*q)+tt*r^2;
U=U0+4/3*r*p*(tp*p+tq*q)+4/3*tt*p*r^2;
V=V0+r*(v4*p^2+v5*p*q+v6*q^2)
    +r^2*(v7*p+v8*q)+v9*r^3;
A=A0+r*(ap*p+aq*q)+aa*r^2;
B=B0+r*(bp*p+bq*q)+bb*r^2;

H2=[A,B,T];
H3=[U,V,p^3];
H4=[p^4,p*C3,0];
L=[l11,l12,l13;l21,l22,l23;l31,l32,l33];
weighted=matdet(L+zz*jacmap(H2)+zz^2*jacmap(H3)+zz^3*jacmap(H4));
E6=polcoef(weighted,6,zz);
E5=polcoef(weighted,5,zz);
E4=polcoef(weighted,4,zz);
E3=polcoef(weighted,3,zz);

checkzero(polcoef(weighted,8,zz),"E8 after the complete E7 parameterization");
checkzero(polcoef(weighted,7,zz),"E7 after the complete parameterization");
checkeq(polcoef(E6,3,r),8/3*p*tt^2*Dq,"universal E6 r^3");
checktrue(deriv(polcoef(E6,3,r),d1) != 0,
          "deleted d1 modulus mutation was not detected");

\\ v9 != 0.
v9topvars=[tt,tq,u1,u2,u3,aa];
v9topvals=[0,0,4*c1/3,4*c2/3,0,2*tp^2/9];
E6v9=substmany(E6,v9topvars,v9topvals);
bracket=-9*ap*p^2-9*aq*p*q-8*c0*p^2*tp+4*c1*p*q*tp
        +4*c2*q^2*tp+12*l33*p^2+9*p^2*tp*u0;
checkeq(polcoef(E6v9,0,r),p^2*Dq*bracket/3,"v9 E6 constant-r factor");

e6vars=[ap,aq];
e6vals=[(12*l33+tp*(9*u0-8*c0))/9,4*c1*tp/9];
E5v9=substmany(substmany(E5,v9topvars,v9topvals),e6vars,e6vals);
checkeq(cf(E5v9,0,3,2),-8*c2^2*v9,"v9 E5 q^3 r^2");
E5v9c2=subst(subst(E5v9,c2,0),u2,0);
checkeq(cf(E5v9c2,1,2,2),-4*tp^3/3,"v9 E5 p q^2 r^2");
checktrue(cf(E5v9c2,1,2,2) != 4*tp^3/3,
          "wrong-sign mutation at v9 E5 terminal");

v9zvars=[tt,tq,tp,aa,c2,u1,u2,u3,ap,aq,x1,x2];
v9zvals=[0,0,0,0,0,4*c1/3,0,0,4*l33/3,0,
         4*l32/3-c1*(8*c0-9*u0)/9,2*c1^2/9];
E5v9z=substmany(E5,v9zvars,v9zvals);
checkeq(polcoef(E5v9z,0,r),
        p^2*Dq*(-8*c0*l33*p+4*c1*l33*q-9*l13*p+9*l33*u0*p)/3,
        "v9 lower E5 factor");
E4v9z=substmany(E4,v9zvars,v9zvals);
checkeq(cf(E4v9z,0,2,2),4*c1^3*v9/3,"v9 E4 q^2 r^2");

v9lowvars=concat(v9zvars,[c1,l13,l12]);
v9lowvals=concat(v9zvals,[0,l33*(u0-8*c0/9),l32*(u0-8*c0/9)]);
E4v9low=substmany(E4,v9lowvars,v9lowvals);
checkeq(polcoef(E4v9low,1,r),4*l33^2*p*Dq/3,
        "v9 E4 r identity after the necessary l12 relation");
v9singvars=concat(v9lowvars,[l33,ap,l13]);
v9singvals=concat(v9lowvals,[0,0,0]);
E3v9sing=substmany(E3,v9singvars,v9singvals);
checkeq(cf(E3v9sing,0,1,2),-4*l32^2*v9,
        "v9 E3 terminal q r^2");

\\ v9=0 and ell=v7*p+v8*q != 0.
elltopvars=[tt,tq,v9,aa,u1,u2,u3];
elltopvals=[0,0,0,2*tp^2/9,4*c1/3,4*c2/3,0];
elle6vars=[ap,aq];
elle6vals=[(12*l33+tp*(9*u0-8*c0))/9,4*c1*tp/9];
E5ell=substmany(substmany(E5,elltopvars,elltopvals),
                elle6vars,elle6vals);
checkeq(cf(E5ell,1,2,2),-4*tp*(3*c2*v8+tp^2)/3,
        "ell E5 p q^2 r^2");

elltpvars=[tt,tq,tp,aa,v9,u1,u2,u3,ap,aq];
elltpvals=[0,0,0,0,0,4*c1/3,4*c2/3,0,4*l33/3,0];
E5elltp=substmany(E5,elltpvars,elltpvals);
K=(8*c0*c1-9*c1*u0-12*l32+9*x1)*p^3
 +(16*c0*c2-4*c1^2-18*c2*u0+18*x2)*p^2*q
 -12*c1*c2*p*q^2-8*c2^2*q^3;
checkeq(polcoef(E5elltp,1,r),2*(v7*p+v8*q)*K/3,
        "ell domain factor");

elle5vars=concat(elltpvars,[c2,u2,x1,x2]);
elle5vals=concat(elltpvals,[0,0,
  4*l32/3-c1*(8*c0-9*u0)/9,2*c1^2/9]);
E5elle5=substmany(E5,elle5vars,elle5vals);
checkeq(polcoef(E5elle5,0,r),
        p^2*Dq*(-8*c0*l33*p+4*c1*l33*q-9*l13*p+9*l33*u0*p)/3,
        "ell lower E5 factor");
E4elle5=substmany(E4,elle5vars,elle5vals);
checkeq(cf(E4elle5,0,3,1),8*c1^3*v8/9,
        "ell v8-open c1 obstruction");
checkeq(subst(cf(E4elle5,1,2,1),v8,0),
        4*(2*c1^3*v7+3*c1*l33*v6+9*l33^2)/9,
        "ell v7-open joint obstruction");

ellsingvars=concat(elle5vars,[c1,u1,x1,x2,l33,ap,l13,l12]);
ellsingvals=concat(elle5vals,[0,0,4*l32/3,0,0,0,0,
                              l32*(u0-8*c0/9)]);
E3ellsing=substmany(E3,ellsingvars,ellsingvals);
checkeq(cf(E3ellsing,0,2,1),-8*l32^2*v8/3,
        "ell v8-open E3 terminal");
checkeq(subst(cf(E3ellsing,1,1,1),v8,0),-8*l32^2*v7/3,
        "ell v7-open E3 terminal");

\\ Zero r^2 orbit.
zeroheadvars=[tt,v9,v7,v8];
zeroheadvals=[0,0,0,0];
E6zerohead=substmany(E6,zeroheadvars,zeroheadvals);
checkeq(polcoef(E6zerohead,1,r),
        -2*p*Dq*(9*aa*p^2-2*(tp*p+tq*q)^2)/3,
        "zero-orbit E6 r classification");
zerotopvars=concat(zeroheadvars,[tq,aa]);
zerotopvals=concat(zeroheadvals,[0,2*tp^2/9]);
E5zerotop=substmany(E5,zerotopvars,zerotopvals);
checkeq(polcoef(E5zerotop,2,r),-4*p*tp^3*Dq/9,
        "zero-orbit E5 r^2 obstruction");

zerovars=[tt,tq,tp,aa,v9,v7,v8];
zerovals=[0,0,0,0,0,0,0];
F=L*[p,q,r]~+[A,B,T]~+[U,V,p^3]~+[p^4,p*C3,0]~;
F0=substmany(F,zerovars,zerovals);
G=subst(F0[3],r,0);
checkzero(F0[3]-l33*r-G,"l33 coordinate identity");
rsub=(w-G)/l33;
plane1=l33^2*subst(F0[1],r,rsub);
plane2=l33^2*subst(F0[2],r,rsub);
checktrue(tdeg2(plane1,p,q)<=6 && tdeg2(plane2,p,q)<=6,
          "l33 plane degree exceeds six");

coordvars=concat(zerovars,[l33,c1,c2]);
coordvals=concat(zerovals,[0,0,0]);
Fc=substmany(F,coordvars,coordvals);
qsub=(w-p^3-c0*p^2-l31*p)/l32;
checkzero(subst(Fc[3],q,qsub)-w,"l32 coordinate identity");
coord1=l32^3*subst(Fc[1],q,qsub);
coord2=l32^3*subst(Fc[2],q,qsub);
checktrue(tdeg2(coord1,p,r)<=10 && tdeg2(coord2,p,r)<=10,
          "l32 plane degree exceeds ten");

print("PASS independent PARI fixed-linear power-fibre determinant replay");
print("PASS independent PARI plane degree ceilings 6 and 10");
}
quit;
