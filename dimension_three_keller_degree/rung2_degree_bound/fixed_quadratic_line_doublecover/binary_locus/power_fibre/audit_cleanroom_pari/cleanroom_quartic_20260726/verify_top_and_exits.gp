\\ Direct PARI/GP verification of the clean-room top identities and exits.
default(parisizemax, 800000000);

br(f,g,h)=
{
  my(M=matrix(3,3));
  M[1,1]=deriv(f,p); M[1,2]=deriv(f,q); M[1,3]=deriv(f,r);
  M[2,1]=deriv(g,p); M[2,2]=deriv(g,q); M[2,3]=deriv(g,r);
  M[3,1]=deriv(h,p); M[3,2]=deriv(h,q); M[3,3]=deriv(h,r);
  matdet(M);
};

Z=z20*p^2+z11*p*q+z02*q^2+z10*p*r+z01*q*r+z00*r^2;
A0=a30*p^3+a21*p^2*q+a12*p*q^2+a03*q^3;
G=g300*p^3+g210*p^2*q+g120*p*q^2+g030*q^3+g201*p^2*r+g111*p*q*r+g021*q^2*r+g102*p*r^2+g012*q*r^2+g003*r^3;
B=b300*p^3+b210*p^2*q+b120*p*q^2+b030*q^3+b201*p^2*r+b111*p*q*r+b021*q^2*r+b102*p*r^2+b012*q*r^2+b003*r^3;
X=x20*p^2+x11*p*q+x02*q^2+x10*p*r+x01*q*r+x00*r^2;
Y=y20*p^2+y11*p*q+y02*q^2+y10*p*r+y01*q*r+y00*r^2;
ell3=l3p*p+l3q*q+l3r*r;
P4=p^4;Q4=p^2*q^2;R3=p^3;

E7=br(P4,Q4,Z)+br(P4,B,R3)+br(G,Q4,R3);
RHS7=2*p^4*q*(4*p*deriv(Z,r)-3*deriv(G,r));
if(E7-RHS7!=0,error("E7 universal identity failed"));

A1=4/3*p*Z+A0;
E7c=br(P4,Q4,Z)+br(P4,B,R3)+br(A1,Q4,R3);
if(E7c!=0,error("E7 contact failed"));

E6=br(P4,Q4,ell3)+br(P4,B,Z)+br(P4,Y,R3)+br(A1,Q4,Z)+br(X,Q4,R3)+br(A1,B,R3);
RHS6=8*l3r*p^5*q-6*p^4*q*deriv(X,r)+3*p^2*deriv(A0,q)*deriv(B,r)+2*p*q*(p*deriv(A0,p)-q*deriv(A0,q))*deriv(Z,r)+8/3*p^2*q*Z*deriv(Z,r);
if(E6-RHS6!=0,error("E6 universal identity failed"));

\\ Explicit coordinate chart: f=(1+p)r+p^3+A p^2+p q.
h=p^2+(aa-1)*p+(1-aa);
f=(1+p)*r+p^3+aa*p^2+p*q;
PP=1+p;UU=r+q+h;WW=f-(aa-1);
if(WW-(PP*UU-q)!=0,error("explicit coordinate identity failed"));

\\ Canonical lambda-zero coordinate exits.
rank1=v+(p^3+aa*p^2+bb*p*u+cc*u^2+dd*p+u);
if(rank1-v-(p^3+aa*p^2+bb*p*u+cc*u^2+dd*p+u)!=0,error("rank-one exit failed"));
rank0i=v+p*u+p^3+aa*p^2+dd*p;
if(rank0i-v-p*u-p^3-aa*p^2-dd*p!=0,error("rank-zero independent exit failed"));
rank0c=u+p^3+aa*p^2+dd*p;
if(rank0c-u-p^3-aa*p^2-dd*p!=0,error("rank-zero constant exit failed"));

print("POWER_FIBRE_PARI_PASS");
