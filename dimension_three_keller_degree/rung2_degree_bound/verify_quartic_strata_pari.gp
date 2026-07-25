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
