\\ Independent PARI/GP certificate for the abstract binary-quartic
\\ Hilbert--Burch and signed E6 lemma.
\\
\\ This file deliberately does not import or translate the SymPy verifier.
\\ Set AUDIT_MUTATION to one of the modes exercised by the strict wrapper
\\ to check that the corresponding guard fails closed.

p='p; q='q; r='r; z='z; ss='ss;

mutation=getenv("AUDIT_MUTATION");
if(mutation==0,mutation="strict");

fail(message)={
  print(Str("FAIL [",mutation,"]: ",message));
  quit(1);
};
check(condition,message)=if(!condition,fail(message));
checkzero(value,message)=check(value==0,message);
checkequal(value,expected,message)=checkzero(value-expected,message);

jac(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);

adj2(M)=matrix(2,2,i,j,if(i==1 && j==1,M[2,2],if(i==1 && j==2,-M[1,2],if(i==2 && j==1,-M[2,1],M[1,1]))));

row2(a,b)=matrix(1,2,i,j,if(j==1,a,b));
cross3(a,b)=Col([a[2]*b[3]-a[3]*b[2],a[3]*b[1]-a[1]*b[3],a[1]*b[2]-a[2]*b[1]]);
dot3(a,b)=a[1]*b[1]+a[2]*b[2]+a[3]*b[3];
gradrow(f)=matrix(1,3,i,j,if(j==1,deriv(f,p),if(j==2,deriv(f,q),deriv(f,r))));
rowsdet(f,g,h)=matdet(matrix(3,3,i,j,if(i==1,gradrow(f)[1,j],if(i==2,gradrow(g)[1,j],gradrow(h)[1,j]))));
jacobian3(f,g,h)=matrix(3,3,i,j,if(i==1,gradrow(f)[1,j],if(i==2,gradrow(g)[1,j],gradrow(h)[1,j])));

homcf(f,n,i)=polcoef(polcoef(f,n-i,p),i,q);
homogeneous(f,n)=subst(subst(f,p,ss*p),q,ss*q)==ss^n*f;

block(row,level)={
  my(a=row[1],b=row[2],c=row[3],cols,n);
  if(level==2,
    cols=[a,b]; n=5,
    if(level==1,
      cols=[a*p,a*q,b*p,b*q,c]; n=6,
      cols=[a*p^2,a*p*q,a*q^2,b*p^2,b*p*q,b*q^2,c*p,c*q];
      n=7
    )
  );
  matrix(n+1,#cols,i,j,homcf(cols[j],n,i-1))
};

\\ ----------------------------------------------------------------------
\\ 1. Reconstruct E8, E7, and E6 from an abstract weighted 3-by-3 matrix.
\\ ----------------------------------------------------------------------

d11='d11; d12='d12; d21='d21; d22='d22;
c11='c11; c12='c12; c21='c21; c22='c22;
a11='a11; a12='a12; a21='a21; a22='a22;
u1='u1; u2='u2; v1='v1; v2='v2;
w1='w1; w2='w2; t1='t1; t2='t2;
rho='rho; tau='tau; ell33='ell33;

D=matrix(2,2,i,j,if(i==1 && j==1,d11,if(i==1 && j==2,d12,if(i==2 && j==1,d21,d22))));
C=matrix(2,2,i,j,if(i==1 && j==1,c11,if(i==1 && j==2,c12,if(i==2 && j==1,c21,c22))));
A=matrix(2,2,i,j,if(i==1 && j==1,a11,if(i==1 && j==2,a12,if(i==2 && j==1,a21,a22))));

u=Col([u1,u2]); v=Col([v1,v2]);
w=row2(w1,w2); t=row2(t1,t2);

J4=matrix(3,3,i,j,if(i<=2 && j<=2,D[i,j],0));
J3rho=matrix(3,3,i,j,if(i<=2 && j<=2,C[i,j],if(i<=2 && j==3,u[i],if(i==3 && j<=2,w[1,j],if(i==3 && j==3,rho,0)))));
J3=matrix(3,3,i,j,if(i<=2 && j<=2,C[i,j],if(i<=2 && j==3,u[i],if(i==3 && j<=2,w[1,j],0))));
J2=matrix(3,3,i,j,if(i<=2 && j<=2,A[i,j],if(i<=2 && j==3,v[i],if(i==3 && j<=2,t[1,j],if(i==3 && j==3,tau,0)))));
L0=matrix(3,3,i,j,if(i==3 && j==3,ell33,0));

weighted_rho=matdet(L0+z*J2+z^2*J3rho+z^3*J4);
checkequal(polcoef(weighted_rho,8,z),matdet(D)*rho,"E8 is det(D) times the cubic normal derivative");

weighted=matdet(L0+z*J2+z^2*J3+z^3*J4);
actualE7=polcoef(weighted,7,z);
expectedE7=matdet(D)*tau-(w*adj2(D)*u)[1];
if(mutation=="e7_beta_sign",expectedE7=matdet(D)*tau+(w*adj2(D)*u)[1]);
if(mutation=="e7_gamma_sign",expectedE7=-matdet(D)*tau-(w*adj2(D)*u)[1]);
checkequal(actualE7,expectedE7,"signed E7 block identity");

actualE6=polcoef(weighted,6,z);
term0=matdet(D)*ell33;
term1=trace(adj2(C)*D)*tau;
term2=-(w*adj2(D)*v)[1];
term3=-(t*adj2(D)*u)[1];
term4=-(w*adj2(C)*u)[1];
if(mutation=="e6_wdv_sign",term2=-term2);
if(mutation=="e6_tdu_sign",term3=-term3);
if(mutation=="e6_curvature_sign",term4=-term4);
if(mutation=="e6_tau_sign",term1=-term1);
checkequal(actualE6,term0+term1+term2+term3+term4,"universal signed E6 block identity");

\\ Independently tie the block signs to alpha=J(Q,R), beta=-J(P,R).
P=p^4+2*p^3*q+3*p^2*q^2+5*p*q^3+7*q^4;
Q=2*p^4-p^3*q+4*p^2*q^2-3*p*q^3+q^4;
R=p^3-2*p^2*q+3*p*q^2+5*q^3;
Dact=matrix(2,2,i,j,if(i==1 && j==1,deriv(P,p),if(i==1 && j==2,deriv(P,q),if(i==2 && j==1,deriv(Q,p),deriv(Q,q)))));
wact=row2(deriv(R,p),deriv(R,q));
alpha=jac(Q,R); beta=-jac(P,R); gam=jac(P,Q);
check((-(wact*adj2(Dact)))==row2(alpha,beta),"alpha/beta orientation from the actual gradients");
checkequal(matdet(Dact),gam,"gamma orientation from the actual gradients");

\\ Check the determinant-sum version with honest homogeneous polynomials,
\\ independently of the abstract block placeholders.
Ua=p^3+2*p^2*q+3*p*q^2+5*q^3+r*(7*p^2+11*p*q+13*q^2)+r^2*(17*p+19*q)+23*r^3;
Va=2*p^3-p^2*q+4*p*q^2-3*q^3+r*(5*p^2-7*p*q+2*q^2)+r^2*(3*p-11*q)-13*r^3;
Aa=p^2+2*p*q+3*q^2+r*(5*p+7*q)+11*r^2;
Ba=2*p^2-p*q+4*q^2+r*(3*p-5*q)+7*r^2;
Ta=3*p^2+5*p*q-2*q^2+r*(7*p+q)-3*r^2;
H4a=jacobian3(P,Q,0);
H3a=jacobian3(Ua,Va,R);
H2a=jacobian3(Aa,Ba,Ta);
L0a=matrix(3,3,i,j,if(i==j,i+1,if(i+j==4,1,0)));
actual_poly_E6=polcoef(matdet(L0a+z*H2a+z^2*H3a+z^3*H4a),6,z);
det_sum_E6=alpha*deriv(Aa,r)+beta*deriv(Ba,r)+gam*L0a[3,3]+rowsdet(P,Va,Ta)+rowsdet(Ua,Q,Ta)+rowsdet(Ua,Va,R);
if(mutation=="e6_det_sum_sign",det_sum_E6-=2*rowsdet(Ua,Va,R));
checkequal(actual_poly_E6,det_sum_E6,"signed E6 determinant-sum identity");

\\ ----------------------------------------------------------------------
\\ 2. R=0 is outside the HB/power-fibre table.
\\ ----------------------------------------------------------------------

rzero=Col([0,0,gam]);
rzero_ranks=[matrank(block(rzero,2)),matrank(block(rzero,1)),matrank(block(rzero,0))];
rzero_expected=[0,1,2];
if(mutation=="rzero_in_table",rzero_expected=[0,1,3]);
check(rzero_ranks==rzero_expected,"R=0 ranks are (0,1,2), outside every nonexceptional row");
check(matrank(matrix(6,2,i,j,0))==0,"R=0 makes alpha and beta dependent");

\\ ----------------------------------------------------------------------
\\ 3. Six HB degree shapes, their tangent nullities, and the wedge factor.
\\ ----------------------------------------------------------------------

Ncolumn(k,which)={
  my(a=3-k,b=2-k);
  if(which==1,
    Col([p^a+q^a,p^a+2*q^a,p^b+3*q^b]),
    Col([p^a+4*q^a,2*p^a+q^a,3*p^b+2*q^b])
  )
};

auditpairs()={
  my(pairs=[[0,0],[1,0],[1,1],[2,0],[2,1],[2,2]]);
  my(seen_delta=vector(5,i,0));
  my(k1,k2,delta,d,N1,N2,reduced,gg,indep,e1,e2,gfac,M1,M2);
  my(wedge_expected,n2,n1,n0,ranks,expected);

  for(ii=1,#pairs,
    k1=pairs[ii][1]; k2=pairs[ii][2];
    delta=k1+k2; d=5-delta;
    check(d>=1,"constant independence forces d at least one");

    N1=Ncolumn(k1,1); N2=Ncolumn(k2,2);
    reduced=cross3(N1,N2);
    checkzero(dot3(reduced,N1),"first HB column is a syzygy");
    checkzero(dot3(reduced,N2),"second HB column is a syzygy");
    gg=gcd(gcd(reduced[1],reduced[2]),reduced[3]);
    check(poldegree(gg,p)<=0 && poldegree(gg,q)<=0,
      "reduced HB minors have gcd one");
    check(homogeneous(reduced[1],d) &&
          homogeneous(reduced[2],d) &&
          homogeneous(reduced[3],d+1),
      "HB minor degrees are (d,d,d+1)");
    indep=matrix(d+1,2,i,j,
      if(j==1,homcf(reduced[1],d,i-1),homcf(reduced[2],d,i-1)));
    check(matrank(indep)==2,
      "the first two reduced generators are constant-independent");

    e1=d+3-k1; e2=d+3-k2;
    check(e1+e2==3*d+1,"Hilbert--Burch degree sum");
    check(e1>=d+1 && e2>=d+1 && e1<=d+3 && e2<=d+3,
      "minimal syzygy degree window");

    gfac=p^k1*q^k2;
    M1=N1*p^k1; M2=N2*q^k2;
    wedge_expected=gfac*reduced;
    if(mutation=="wedge_drop_g" && delta==1,wedge_expected=reduced);
    check(cross3(M1,M2)==wedge_expected,
      "gradient-column wedge retains the removed gcd");

    n2=0;
    n1=(k1==2)+(k2==2);
    n0=(k1==1)+(k2==1)+2*((k1==2)+(k2==2));
    ranks=[matrank(block(gfac*reduced,2)),matrank(block(gfac*reduced,1)),
           matrank(block(gfac*reduced,0))];
    expected=[2-n2,5-n1,8-n0];
    if(mutation=="nullity_shift" && delta==3,expected[3]++);
    if(mutation=="delta0_kernel" && delta==0,expected[2]--);
    check(ranks==expected,Str("E7 tangent nullity for k=(",k1,",",k2,"); got ",ranks,", expected ",expected));
    seen_delta[delta+1]++;
  );
  check(seen_delta==[1,1,2,1,1],
    "all delta and both delta=2 HB shapes were exercised");
};
auditpairs();

\\ A fake delta=5 reduction makes alpha0,beta0 constants, so the
\\ constant-independence hypothesis must fail before HB height is invoked.
fake_indep=matrank(matrix(1,2,i,j,if(j==1,1,2)));
fake_expected=1;
if(mutation=="height_unit",fake_expected=2);
check(fake_indep==fake_expected,"delta=5 is rejected by constant dependence before the height-two step");

\\ ----------------------------------------------------------------------
\\ 4. Power-fibre implication and scalar normalization.
\\ ----------------------------------------------------------------------

Lp=2*(p+2*q);
Rpow=Lp^3;
Spow=Lp^4;
Qpow=p^4-p^3*q+2*p^2*q^2+3*p*q^3-q^4;
Ppow=Spow-2*Qpow;
apow=jac(Qpow,Rpow);
bpow=-jac(Ppow,Rpow);
gpow=jac(Ppow,Qpow);
check(apow!=0 && gpow!=0,"power-fibre witness is nondegenerate");
checkzero(bpow-2*apow,"alpha and beta are constant-dependent on a power fibre");
checkzero(jac(Ppow+2*Qpow,Rpow),"the dependent pencil member and R have zero Jacobian");

s0='s0; s1='s1; s2='s2; s3='s3; s4='s4;
r0='r0; r1='r1; r2='r2; r3='r3;
Sgen=s0*p^4+s1*p^3*q+s2*p^2*q^2+s3*p*q^3+s4*q^4;
Rgen=r0*p^3+r1*p^2*q+r2*p*q^2+r3*q^3;
Jgen=jac(Sgen,Rgen);
checkzero(3*Rgen*deriv(Sgen,p)-4*Sgen*deriv(Rgen,p)-q*Jgen,"Euler identity reducing the p derivative to J(S,R)");
checkzero(3*Rgen*deriv(Sgen,q)-4*Sgen*deriv(Rgen,q)+p*Jgen,"Euler identity reducing the q derivative to J(S,R)");

Rbad=Rpow+p^2*q;
power_bad=jac(Spow,Rbad);
if(mutation=="power_fibre",power_bad=0);
check(power_bad!=0,"a non-power perturbation leaves the power fibre");

\\ ----------------------------------------------------------------------
\\ 5. Delta=0 E6 injection and the plane-plus-shear shape.
\\ ----------------------------------------------------------------------

N10=Ncolumn(0,1); N20=Ncolumn(0,2);
row0=cross3(N10,N20);
check(matrank(block(row0,2))==2,"delta=0 r-linear E6 coefficients are killed injectively");
check(matrank(block(row0,1))==5,"delta=0 binary-linear E6 coefficients and L33 are killed injectively");

Y1='Y1; Y2='Y2; Y3='Y3;
G1=p+q^2; G2=q; G3=r+p*q;
pinv=Y1-Y2^2; qinv=Y2;
rinv=Y3-pinv*qinv;
if(mutation=="delta0_shear",rinv=Y3+pinv*qinv);
checkzero(subst(subst(subst(G1,p,pinv),q,qinv),r,rinv)-Y1,"plane-plus-shear inverse, first coordinate");
checkzero(subst(subst(subst(G2,p,pinv),q,qinv),r,rinv)-Y2,"plane-plus-shear inverse, second coordinate");
checkzero(subst(subst(subst(G3,p,pinv),q,qinv),r,rinv)-Y3,"plane-plus-shear inverse, third coordinate");

print("PASS independent E8/E7/E6 signs");
print("PASS R=0 separation");
print("PASS all six Hilbert--Burch/nullity shapes and wedge gcd");
print("PASS power-fibre implication guards");
print("PASS delta=0 injection and plane-shear shape");
print("ALL ABSTRACT HB/E6 HOSTILE PARI CHECKS PASSED");
quit;
