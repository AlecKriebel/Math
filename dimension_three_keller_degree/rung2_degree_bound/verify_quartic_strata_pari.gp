\\ Independent PARI/GP checks for the quartic leading-stratum identities.

assertzero(x, label) =
{
  if (x != 0, error(Str("FAIL: ", label, ": ", x)));
};

asserttrue(x, label) =
{
  if (!x, error(Str("FAIL: ", label)));
};

cross3(u, v) =
{
  return([u[2]*v[3]-u[3]*v[2],
          u[3]*v[1]-u[1]*v[3],
          u[1]*v[2]-u[2]*v[1]]~);
};

coeff3(pol, i, j, k) =
{
  return(polcoef(polcoef(polcoef(pol,k,z),j,y),i,x));
};

jac2(first, second, firstvar, secondvar) =
{
  return(deriv(first,firstvar)*deriv(second,secondvar)
         -deriv(first,secondvar)*deriv(second,firstvar));
};

conicrank(pform, qform) =
{
  my(pgrad, qgrad, dgrad, normal, products, monoms, index, coeffmat);
  pgrad = [deriv(pform,x),deriv(pform,y),deriv(pform,z)]~;
  qgrad = [deriv(qform,x),deriv(qform,y),deriv(qform,z)]~;
  dgrad = cross3(pgrad,qgrad);
  normal = [qform^2,-2*pform*qform,pform^2]~;
  products = vector(9);
  index = 0;
  for (i=1,3,
    for (j=1,3,
      index++;
      products[index] = normal[i]*dgrad[j];
    );
  );
  monoms = List();
  for (i=0,6,
    for (j=0,6-i,
      for (k=0,6-i-j,
        listput(monoms,[i,j,k]);
      );
    );
  );
  coeffmat = matrix(#monoms,9,row,column,
    coeff3(products[column],
           monoms[row][1],monoms[row][2],monoms[row][3]));
  return(matrank(coeffmat));
};

main() =
{
  lm =
  [l11,l12,l13;
   l21,l22,l23;
   l31,l32,l33];
  am =
  [ap,aq,ar;
   bp,bq,br;
   wp,wq,wr];
  bm =
  [up,uq,ur;
   vp,vq,vr;
   rp,rq,rr];
  cm =
  [pp,pq,0;
   qp,qq,0;
   0,0,0];

  cc = pp*qq-pq*qp;
  aa = qp*rq-qq*rp;
  bb = pp*rq-pq*rp;
  determinant = matdet(lm+t*am+t^2*bm+t^3*cm);
  assertzero(polcoef(determinant,8,t)-cc*rr, "line (1,4) degree 8");

  bm7 =
  [up,uq,ur;
   vp,vq,vr;
   rp,rq,0];
  determinant7 = matdet(lm+t*am+t^2*bm7+t^3*cm);
  assertzero(polcoef(determinant7,7,t)-(cc*wr+aa*ur-bb*vr),
             "line (1,4) degree 7");
  curvature6 =
    matdet([pp,pq,0;vp,vq,vr;wp,wq,wr])
    +matdet([up,uq,ur;qp,qq,0;wp,wq,wr])
    +matdet([up,uq,ur;vp,vq,vr;rp,rq,0]);
  assertzero(polcoef(determinant7,6,t)
             -(cc*l33+aa*ar-bb*br+curvature6),
             "line (1,4) full degree 6");

  bm6 =
  [up,uq,0;
   vp,vq,0;
   rp,rq,0];
  am6 =
  [ap,aq,ar;
   bp,bq,br;
   wp,wq,0];
  determinant6 = matdet(lm+t*am6+t^2*bm6+t^3*cm);
  assertzero(polcoef(determinant6,6,t)-(cc*l33+aa*ar-bb*br),
             "line (1,4) degree 6");

  curveL =
  [cl0,cl1,cl2;
   cl3,cl4,cl5;
   cl6,cl7,cl8];
  curveA =
  [ca0,ca1,ca2;
   ca3,ca4,ca5;
   ca6,ca7,ca8];
  curveB =
  [cb0,cb1,cb2;
   cb3,cb4,cb5;
   cb6,cb7,cb8];
  curveC =
  [cc0,cc1,0;
   cc2,cc3,0;
   cc4,cc5,0];
  curveNormal = cross3(curveC[,1],curveC[,2]);
  curveDet = matdet(curveL+u*curveA+u^2*curveB+u^3*curveC);
  assertzero(polcoef(curveDet,8,u)-curveNormal~*curveB[,3],
             "rational quartic curve degree 8");
  curveB0 =
  [cb0,cb1,0;
   cb3,cb4,0;
   cb6,cb7,0];
  curveDet7 = matdet(curveL+u*curveA+u^2*curveB0+u^3*curveC);
  assertzero(polcoef(curveDet7,7,u)-curveNormal~*curveA[,3],
             "rational quartic curve degree 7");
  curveParam = [cp^4,cp*cq^3,cq^4]~;
  curveDelta = cross3(
    [deriv(curveParam[1],cp),deriv(curveParam[2],cp),
     deriv(curveParam[3],cp)]~,
    [deriv(curveParam[1],cq),deriv(curveParam[2],cq),
     deriv(curveParam[3],cq)]~
  );
  curveReduced = curveDelta/(4*cq^2);
  assertzero(curveReduced~*[0,3*cp,4*cq]~,
             "ramified quartic-curve sharpness");

  ramP1 = hp^4+hp^2*hq^2+hp*hq^3+hq^4;
  ramQ1 = hp^2*hq^2+hp*hq^3+2*hq^4;
  ramR1 = hp^3+2*hp*hq^2+3*hq^3;
  rama1 = jac2(ramQ1,ramR1,hp,hq);
  ramb1 = jac2(ramP1,ramR1,hp,hq);
  ramc1 = jac2(ramP1,ramQ1,hp,hq);
  asserttrue(poldegree(gcd(gcd(rama1,ramb1),ramc1),hq)==1,
             "ramification delta 1");
  assertzero(rama1*(2*hp^2+3*hp*hq+4*hq^2)
             -ramb1*(2*hp^2+3*hp*hq+8*hq^2)
             +ramc1*(4*hp+9*hq), "ramification syzygy delta 1");

  ramP2a = hp^4+hp^2*hq^2+2*hq^4;
  ramQ2a = 2*hp^4+3*hp^2*hq^2+hq^4;
  ramR2a = hp^3+hq^3;
  rama2a = jac2(ramQ2a,ramR2a,hp,hq);
  ramb2a = jac2(ramP2a,ramR2a,hp,hq);
  ramc2a = jac2(ramP2a,ramQ2a,hp,hq);
  ramg2a = gcd(gcd(rama2a,ramb2a),ramc2a);
  asserttrue(poldegree(ramg2a,hp)+poldegree(ramg2a,hq)==2,
             "ramification delta 2 split");
  assertzero(rama2a*(4*hp^2+2*hq^2)
             -ramb2a*(8*hp^2+6*hq^2)+ramc2a*3*hp,
             "ramification syzygy delta 2 split, first");
  assertzero(rama2a*(2*hp^2+8*hq^2)
             -ramb2a*(6*hp^2+4*hq^2)+ramc2a*3*hq,
             "ramification syzygy delta 2 split, second");

  ramP2b = hp^4+hp*hq^3+hq^4;
  ramQ2b = hp*hq^3+2*hq^4;
  ramR2b = hp^3+hq^3;
  rama2b = jac2(ramQ2b,ramR2b,hp,hq);
  ramb2b = jac2(ramP2b,ramR2b,hp,hq);
  ramc2b = jac2(ramP2b,ramQ2b,hp,hq);
  asserttrue(poldegree(gcd(gcd(rama2b,ramb2b),ramc2b),hq)==2,
             "ramification delta 2 tangent");
  assertzero(rama2b*(3*hp+4*hq)-ramb2b*(3*hp+8*hq)+3*ramc2b,
             "ramification syzygy delta 2 tangent");

  ramP3 = hp^4+4*hp^2*hq^2+4*hp*hq^3+2*hq^4;
  ramQ3 = hq^4;
  ramR3 = hp^3+3*hp*hq^2+3*hq^3;
  rama3 = jac2(ramQ3,ramR3,hp,hq);
  ramb3 = jac2(ramP3,ramR3,hp,hq);
  ramc3 = jac2(ramP3,ramQ3,hp,hq);
  asserttrue(poldegree(gcd(gcd(rama3,ramb3),ramc3),hq)==3,
             "ramification delta 3");
  assertzero(rama3*(52*hp+40*hq)-ramb3*(-8*hp+12*hq)+39*ramc3,
             "ramification syzygy delta 3, first");
  assertzero(rama3*(-hq*(5*hp+hq))-ramb3*(hp^2+hq^2),
             "ramification syzygy delta 3, second");

  ramP4 = hp^4+2*hq^4;
  ramQ4 = hq^4;
  ramR4 = hp^3+hq^3;
  rama4 = jac2(ramQ4,ramR4,hp,hq);
  ramb4 = jac2(ramP4,ramR4,hp,hq);
  ramc4 = jac2(ramP4,ramQ4,hp,hq);
  ramg4 = gcd(gcd(rama4,ramb4),ramc4);
  asserttrue(poldegree(ramg4,hp)+poldegree(ramg4,hq)==4,
             "ramification delta 4");
  assertzero(rama4*(-hp+2*hq)-ramb4*hq,
             "ramification syzygy delta 4, first");
  assertzero(4*hp*rama4+3*ramc4,
             "ramification syzygy delta 4, second");

  sharpP = hp^4+hp^2*hq^2+hq^4;
  sharpQ = hp^2*hq^2+2*hq^4;
  sharpR = hp^3+2*hp*hq^2;
  sharpN1 = 2*hp^2+4*hq^2;
  sharpN2 = 2*hp^2+8*hq^2;
  sharpN3 = 4*hp;
  sharpL =
  [0,0,1;
   0,1,0;
   1,0,0];
  sharpH2 =
  [0,0,8*hr;
   0,0,16*hr;
   4*hr,0,4*hp];
  sharpH3 =
  [deriv(hr*sharpN1,hp),deriv(hr*sharpN1,hq),sharpN1;
   deriv(hr*sharpN2,hp),deriv(hr*sharpN2,hq),sharpN2;
   deriv(sharpR,hp),deriv(sharpR,hq),0];
  sharpH4 =
  [deriv(sharpP,hp),deriv(sharpP,hq),0;
   deriv(sharpQ,hp),deriv(sharpQ,hq),0;
   0,0,0];
  sharpDet = matdet(sharpL+hs*sharpH2+hs^2*sharpH3+hs^3*sharpH4);
  assertzero(polcoef(sharpDet,8,hs), "sharpness degree 8");
  assertzero(polcoef(sharpDet,7,hs), "sharpness degree 7");
  assertzero(polcoef(sharpDet,6,hs), "sharpness degree 6");
  assertzero(polcoef(sharpDet,5,hs)
             +2*hq*(hp^2+2*hq^2)*(3*hp^2+4*hq^2),
             "sharpness degree 5");

  pv = [p1,p2,p3]~;
  qv = [q1,q2,q3]~;
  dv = [p2*q3-p3*q2,p3*q1-p1*q3,p1*q2-p2*q1]~;
  nv = [q^2,-2*p*q,p^2]~;
  cv =
  [2*p*p1,2*p*p2,2*p*p3;
   q*p1+p*q1,q*p2+p*q2,q*p3+p*q3;
   2*q*q1,2*q*q2,2*q*q3];
  assertzero(matadjoint(cv)-2*dv*nv~, "conic adjugate");

  tangent = [2*p*ell,q*ell+p*emm,2*q*emm]~;
  assertzero(nv~*tangent, "conic tangent syzygy");
  thetav = q*ell-p*emm;
  versmall = [ell^2,ell*emm,emm^2]~;
  assertzero(nv~*versmall-thetav^2, "conic degree-seven square");

  ellv = [ell1,ell2,ell3]~;
  emmv = [emm1,emm2,emm3]~;
  hvals = [h1,h2,h3]~;
  h1v = [h11,h12,h13]~;
  h2v = [h21,h22,h23]~;
  h3v = [h31,h32,h33]~;
  ah =
  [h11,h12,h13;
   h21,h22,h23;
   h31,h32,h33];
  bh =
  [2*ell*p1+2*p*ell1,2*ell*p2+2*p*ell2,2*ell*p3+2*p*ell3;
   ell*q1+q*ell1+emm*p1+p*emm1,
     ell*q2+q*ell2+emm*p2+p*emm2,
     ell*q3+q*ell3+emm*p3+p*emm3;
   2*emm*q1+2*q*emm1,2*emm*q2+2*q*emm2,2*emm*q3+2*q*emm3];
  conicdet = matdet(scale*ah+scale^2*bh+scale^3*cv);
  n1grad = 2*q*qv;
  n2grad = -2*(q*pv+p*qv);
  n3grad = 2*p*pv;
  gradndoth = h1*n1grad+q^2*h1v
             +h2*n2grad-2*p*q*h2v
             +h3*n3grad+p^2*h3v;
  gradtheta = ell*qv+q*ellv-emm*pv-p*emmv;
  expected7 = 2*dv~*(gradndoth-2*thetav*gradtheta);
  assertzero(polcoef(conicdet,7,scale)-expected7,
             "conic full degree 7");

  ag =
  [ag11,ag12,ag13;
   ag21,ag22,ag23;
   ag31,ag32,ag33];
  bg1 = [bg11,bg12,bg13]~;
  bg2 = [bg21,bg22,bg23]~;
  kg1 = [kg11,kg12,kg13]~;
  kg2 = [kg21,kg22,kg23]~;
  updated = ag+bg1*kg1~+bg2*kg2~;
  ranktwo = matdet(ag)
            +kg1~*matadjoint(ag)*bg1
            +kg2~*matadjoint(ag)*bg2
            +cross3(bg1,bg2)~*ag*cross3(kg1,kg2);
  assertzero(matdet(updated)-ranktwo, "rank-two determinant formula");

  asserttrue(conicrank(y^2+2*z^2,x^2+y^2+z^2)==9,
             "conic degree 6, three eigenvalues");
  asserttrue(conicrank(y^2+z^2,2*x*y+z^2)==9,
             "conic degree 6, two-by-two block");
  asserttrue(conicrank(2*y*z,2*x*z+y^2)==9,
             "conic degree 6, three-by-three block");

  p0 = x^2;
  q0 = y*z;
  r0 = x^3;
  d0 =
  [deriv(p0,y)*deriv(q0,z)-deriv(p0,z)*deriv(q0,y),
   deriv(p0,z)*deriv(q0,x)-deriv(p0,x)*deriv(q0,z),
   deriv(p0,x)*deriv(q0,y)-deriv(p0,y)*deriv(q0,x)];
  assertzero(d0[1]*deriv(r0,x)+d0[2]*deriv(r0,y)+d0[3]*deriv(r0,z),
             "double-line sharpness");

  ptest = s^4+t0^4;
  qtest = s^3*t0+2*s*t0^3;
  rtest = s^3+s*t0^2+t0^3;
  ja = deriv(qtest,s)*deriv(rtest,t0)-deriv(qtest,t0)*deriv(rtest,s);
  jb = deriv(ptest,s)*deriv(rtest,t0)-deriv(ptest,t0)*deriv(rtest,s);
  jc = deriv(ptest,s)*deriv(qtest,t0)-deriv(ptest,t0)*deriv(qtest,s);
  asserttrue(gcd(gcd(ja,jb),jc)==1, "gcd-one ramification example");

  triangular =
  [1,0,0;
   0,1,0;
   gx,gy,beta];
  assertzero(matdet(triangular)-beta, "quadratic coordinate Jacobian");

  print("PASS: independent PARI quartic leading-stratum regressions");
};

main();
quit;
