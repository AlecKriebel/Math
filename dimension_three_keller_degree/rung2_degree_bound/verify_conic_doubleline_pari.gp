\\ Independent PARI/GP checks for the unique-double-line conic exclusion.

default(parisizemax, 512000000);
allocatemem(128000000);

assertzero(value, label) =
{
  if (value != 0, error(Str("FAIL: ", label, ": ", value)));
};

jacvec(vector) =
{
  return(
  [deriv(vector[1],x),deriv(vector[1],y),deriv(vector[1],z);
   deriv(vector[2],x),deriv(vector[2],y),deriv(vector[2],z);
   deriv(vector[3],x),deriv(vector[3],y),deriv(vector[3],z)]);
};

ver(first, second) =
{
  return([first^2,first*second,second^2]~);
};

detcoeff(linear, quadratic, cubic, quartic, degree) =
{
  my(value);
  value = matdet(linear+s*jacvec(quadratic)
                 +s^2*jacvec(cubic)+s^3*jacvec(quartic));
  return(polcoef(value,degree,s));
};

main() =
{
  conic1 =
  [1,0,0;
   0,0,-tt/2;
   0,-tt/2,0];
  conic2 =
  [1,0,-tt;
   0,-tt,0;
   -tt,0,0];
  assertzero(matdet(conic1)+tt^2/4, "pencil yz determinant");
  assertzero(matdet(conic2)-tt^3, "pencil Jordan determinant");

  p = x^2;
  ell = lx*x+ly*y+lz*z;
  emm = mxx*x+myy*y+mzz*z;
  ellbar = ly*y+lz*z;
  emmbar = myy*y+mzz*z;
  u = [u1,u2,u3]~;
  v = [v1,v2,v3]~;
  zero = matrix(3,3);

  for (which=1,2,
    if (which==1, q=y*z, q=y^2+2*x*z);
    quartic = ver(p,q);
    tangent =
      [2*p*ell,q*ell+p*emm,2*q*emm]~;
    exceptional =
      x*[aa0*q+bb0*p,0,gg0*q+dd0*p]~;
    cubic = tangent+exceptional;

    quadraticAlpha0 =
      ver(ell,emm)
      +x*[3*bb0*ellbar/2,-gg0*ellbar/4,
          3*dd0*ellbar/2+gg0*emmbar]~
      +u*p+v*q;
    assertzero(
      detcoeff(zero,quadraticAlpha0,subst(cubic,aa0,0),quartic,7),
      Str("degree 7 alpha zero, case ",which));

    cubicEll0 = subst(subst(subst(cubic,lx,0),ly,0),lz,0);
    quadraticEll0 =
      ver(0,emm)+x*[aa0*emmbar,0,gg0*emmbar]~+u*p+v*q;
    assertzero(
      detcoeff(zero,quadraticEll0,cubicEll0,quartic,7),
      Str("degree 7 ell zero, case ",which));

    forcedLinear =
      [a1,v1*myy,v1*mzz;
       a2,v2*myy,v2*mzz;
       a3,v3*myy,v3*mzz];
    assertzero(
      detcoeff(forcedLinear,quadraticEll0,cubicEll0,quartic,6),
      Str("degree 6 singular linear part, case ",which));
    assertzero(matdet(forcedLinear),
               Str("forced linear rank, case ",which));
  );

  q = y^2+2*x*z;
  ell = lambda*y;
  emm = kappa*z;
  quartic = ver(p,q);
  cubic =
    [2*p*ell,q*ell+p*emm,2*q*emm]~
    +x*[bb0*p,0,gg0*q+dd0*p]~;
  quadratic =
    ver(ell,emm)
    +x*[3*bb0*ell/2,-gg0*ell/4,
        3*dd0*ell/2+gg0*emm]~
    +u*p+v*q;
  residualLinear =
    [a1,lambda*u1,kappa*v1-3*bb0*lambda^2/4;
     a2,lambda*u2,kappa*v2+3*gg0*lambda^2/8;
     a3,lambda*u3-gg0^2*lambda/4,
        kappa*v3-3*dd0*lambda^2/4];
  assertzero(detcoeff(residualLinear,quadratic,cubic,quartic,6),
             "residual degree 6");
  degree5 = detcoeff(residualLinear,quadratic,cubic,quartic,5);
  assertzero(polcoef(polcoef(polcoef(degree5,3,z),0,y),2,x)
             -12*bb0*lambda^3, "degree 5 x2z3");
  assertzero(polcoef(polcoef(polcoef(degree5,0,z),4,y),1,x)
             -2*lambda*(-v1*gg0+2*a1), "degree 5 xy4");
  assertzero(polcoef(polcoef(polcoef(degree5,2,z),0,y),3,x)
             -2*lambda*(-4*v1*gg0+3*gg0*lambda^2+8*a1),
             "degree 5 x3z2");
  assertzero(polcoef(polcoef(polcoef(degree5,0,z),2,y),3,x)
             +4*lambda*(-v2*gg0+2*a2), "degree 5 x3y2");
  assertzero(polcoef(polcoef(polcoef(degree5,1,z),0,y),4,x)
             +lambda*(-8*v2*gg0-3*dd0*lambda^2+16*a2),
             "degree 5 x4z");

  mapG =
    [fa1*source+first^2+fu1*first+fv1*second,
     fa2*source+first*second+fu2*first+fv2*second,
     fa3*source+second^2+fu3*first+fv3*second]~;
  determinantG = matdet(
    [deriv(mapG[1],source),deriv(mapG[1],first),deriv(mapG[1],second);
     deriv(mapG[2],source),deriv(mapG[2],first),deriv(mapG[2],second);
     deriv(mapG[3],source),deriv(mapG[3],first),deriv(mapG[3],second)]);
  scaledG = subst(subst(determinantG,first,scale*first),
                  second,scale*second);
  assertzero(polcoef(scaledG,2,scale)
             -2*(fa1*second^2-2*fa2*first*second+fa3*first^2),
             "factorization top degree");

  print("PASS: independent PARI unique-double-line conic regressions");
};

main();
quit;
