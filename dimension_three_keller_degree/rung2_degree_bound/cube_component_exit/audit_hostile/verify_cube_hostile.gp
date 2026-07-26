\\ Independent PARI/GP audit of the cube-leading coordinate theorem.
\\ No primary Python code or symbolic-polynomial class is imported.

default(parisizemax, 400000000);

FAULT_INVERSE = if(getenv("AUDIT_FAULT_INVERSE") == "1", 1, 0);

fail(msg) =
{
  print("FAIL ", msg);
  quit(1);
};

check0(value, msg) =
{
  if(value != 0, fail(Str(msg, ": residual = ", value)));
  print("PASS ", msg);
};

checkeq(left, right, msg) = check0(left-right,msg);
tdeg(f,vars) = poldegree(substvec(f,vars,vector(#vars,i,t*vars[i])),t);

main() =
{
  my(f2,det2,y2,z2,fx2,f1,x1,y1,z1,res1,h1,zinv,sgn,
     f0,delta,x0,y0,z0,Y0,Z0,h0,Zinv,yinv,zinv0,f00,yinv0,zinv1);

  \\ General normalized form:
  \\ x^3+a x^2+x(by+cz)+q(y,z)+dx+ey+gz.
  \\ Rank two transverse Hessian.
  f2=x^3+a*x^2+x*(b*y+c*z)
     +(h11*y^2+2*h12*y*z+h22*z^2)/2+d*x+e*y+g*z;
  det2=h11*h22-h12^2;
  y2=(h12*(c*x+g)-h22*(b*x+e))/det2;
  z2=(h12*(b*x+e)-h11*(c*x+g))/det2;
  check0(substvec(deriv(f2,y),[y,z],[y2,z2]),
         "rank two: transverse y equation");
  check0(substvec(deriv(f2,z),[y,z],[y2,z2]),
         "rank two: transverse z equation");
  fx2=substvec(deriv(f2,x),[y,z],[y2,z2]);
  checkeq(polcoeff(fx2,2,x),3,
          "rank two: residual critical equation has leading coefficient 3");

  \\ Rank one, with z spanning the transverse Hessian kernel.
  f1=x^3+a*x^2+x*(b*y+c*z)+y^2/2+d*x+e*y+g*z;
  x1=-g/c;
  y1=-(b*x1+e);
  z1=-(3*x1^2+2*a*x1+b*y1+d)/c;
  check0(substvec(deriv(f1,x),[x,y,z],[x1,y1,z1]),
         "rank one,c!=0: x critical equation");
  check0(substvec(deriv(f1,y),[x,y,z],[x1,y1,z1]),
         "rank one,c!=0: y critical equation");
  check0(substvec(deriv(f1,z),[x,y,z],[x1,y1,z1]),
         "rank one,c!=0: z critical equation");

  res1=subst(deriv(substvec(f1,[c,g],[0,0]),x),y,-(b*x+e));
  checkeq(polcoeff(res1,2,x),3,
          "rank one,c=g=0: residual critical equation is quadratic");

  \\ Thus a submersion on rank one has c=0,g!=0 and is triangular.
  h1=substvec(f1,[c,g,z],[0,0,0]);
  sgn=if(FAULT_INVERSE,1,-1);
  zinv=(w+sgn*h1)/g;
  checkeq(substvec(f1,[c,z],[0,zinv]),w,
          "rank one: explicit triangular inverse");
  checkeq(tdeg(zinv,[x,y,w]),3,
          "rank one: inverse degree is at most three");

  \\ Rank zero.  The two transverse derivatives are bx+e and cx+g.
  f0=x^3+a*x^2+d*x+(b*x+e)*y+(c*x+g)*z;
  delta=b*g-c*e;

  \\ Dependent affine pair, chart b!=0.
  x0=-e/b;
  y0=-(3*x0^2+2*a*x0+d)/b;
  check0(substvec(deriv(f0,x),[x,y,z],[x0,y0,0]),
         "rank zero,delta=0,b!=0: x critical equation");
  check0(substvec(deriv(f0,y),[x,y,z],[x0,y0,0]),
         "rank zero,delta=0,b!=0: y critical equation");
  check0(substvec(deriv(f0,z),[x,y,z,g],[x0,y0,0,c*e/b]),
         "rank zero,delta=0,b!=0: z critical equation");

  \\ Dependent affine pair, complementary chart b=0,c!=0; delta=0 gives e=0.
  x0=-g/c;
  z0=-(3*x0^2+2*a*x0+d)/c;
  check0(substvec(deriv(f0,x),[x,y,z,b,e],[x0,0,z0,0,0]),
         "rank zero,delta=0,b=0,c!=0: x critical equation");
  check0(substvec(deriv(f0,y),[x,y,z,b,e],[x0,0,z0,0,0]),
         "rank zero,delta=0,b=0,c!=0: y critical equation");
  check0(substvec(deriv(f0,z),[x,y,z,b,e],[x0,0,z0,0,0]),
         "rank zero,delta=0,b=0,c!=0: z critical equation");

  \\ Independent affine pair: Y=by+cz, Z=ey+gz, det=delta.
  h0=x^3+a*x^2+d*x;
  Zinv=w-h0-x*Y;
  yinv=(g*Y-c*Zinv)/delta;
  zinv0=(-e*Y+b*Zinv)/delta;
  checkeq(substvec(b*y+c*z,[y,z],[yinv,zinv0]),Y,
          "rank zero,delta!=0: inverse recovers Y");
  checkeq(substvec(e*y+g*z,[y,z],[yinv,zinv0]),Zinv,
          "rank zero,delta!=0: inverse recovers Z");
  checkeq(substvec(f0,[y,z],[yinv,zinv0]),w,
          "rank zero,delta!=0: coordinate inverse");
  checkeq(max(tdeg(yinv,[x,Y,w]),tdeg(zinv0,[x,Y,w])),3,
          "rank zero,delta!=0: inverse degree is at most three");

  \\ Constant affine pair: b=c=0 and at least one of e,g is nonzero.
  f00=substvec(f0,[b,c],[0,0]);
  yinv0=(w-h0-g*z)/e;
  checkeq(subst(f00,y,yinv0),w,
          "rank zero,b=c=0,e!=0: triangular inverse");
  zinv1=(w-h0)/g;
  checkeq(substvec(f00,[e,z],[0,zinv1]),w,
          "rank zero,b=c=e=0,g!=0: triangular inverse");

  checkeq(3*35,105,"degree transfer at d=35");
  if(!(3*35<108),fail("plane floor does not cover d=35"));
  if(3*36<108,fail("degree argument incorrectly covers d=36"));
  checkeq(3*33,99,"Moh fallback transfer at d=33");
  if(!(3*33<100),fail("Moh fallback does not cover d=33"));
  if(3*34<100,fail("Moh fallback incorrectly covers d=34"));

  print("CUBE_COMPONENT_HOSTILE_EXACT_PASS");
};

main();
