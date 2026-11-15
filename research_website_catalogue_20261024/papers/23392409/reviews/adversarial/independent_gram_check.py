"""Independent centered-polynomial/Gram certificate, derived before native code.

Eighth roots use three integer-isqrt stages on a binary grid, with final eighth-
power inclusion checks. No native imports, expected-data reads, network or writes.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
import json


def need(ok, why):
    if not ok: raise ValueError(why)


@dataclass(frozen=True)
class I:
    lo: Q
    hi: Q
    def __init__(self, lo, hi=None):
        object.__setattr__(self, 'lo', Q(lo));object.__setattr__(self, 'hi', Q(lo if hi is None else hi));need(self.lo<=self.hi,'ordered rational interval')
    def __add__(self, other):
        o=iv(other);return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self, other):return self+-iv(other)
    def __rsub__(self, other):return iv(other)+-self
    def __mul__(self, other):
        o=iv(other);v=[a*b for a in (self.lo,self.hi) for b in (o.lo,o.hi)];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self, other):
        o=iv(other);need(o.lo>0 or o.hi<0,'nonzero interval denominator');return self*I(1/o.hi,1/o.lo)
    def __rtruediv__(self, other):return iv(other)/self
    def sq(self):
        low=0 if self.lo<=0<=self.hi else min(self.lo*self.lo,self.hi*self.hi);return I(low,max(self.lo*self.lo,self.hi*self.hi))
    def pow(self, n):
        need(type(n) is int and n>=0,'nonnegative integral power')
        if n==0:return I(1)
        if n%2:return self*self.sq().pow((n-1)//2)
        return self.sq().pow(n//2)
    def sign(self):
        if self.lo>0:return 1
        if self.hi<0:return -1
        return 0
    def data(self):return {'lo':str(self.lo),'hi':str(self.hi),'strict_sign':self.sign()}


def iv(value):return value if isinstance(value,I) else I(value)
def vadd(a,b):return tuple(x+y for x,y in zip(a,b))
def vsub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(c,a):return tuple(c*x for x in a)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),I(0))
def norm2(a):return sum((iv(x).sq() for x in a),I(0))
def norm16(a):return norm2(a).pow(8)
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def orient(a,b,c):return det(vsub(b,a),vsub(c,a))
def J(a):return (-a[1],a[0])
def point(x,y):return (I(x),I(y))


SCALE=1<<256
def sqrt_point(q):
    q=Q(q);need(q>=0,'nonnegative square-root argument');k=isqrt(q.numerator*SCALE*SCALE//q.denominator)
    lo=Q(k,SCALE);hi=lo if lo*lo==q else Q(k+1,SCALE)
    need(lo>=0 and lo*lo<=q<=hi*hi,'integer-isqrt outward proof');return I(lo,hi)


def root8(q):
    q=iv(q);need(q.lo>=0,'nonnegative eighth-root domain');r=q
    for _ in range(3):r=I(sqrt_point(r.lo).lo,sqrt_point(r.hi).hi)
    need(r.lo>=0 and r.lo**8<=q.lo and r.hi**8>=q.hi,'independent final eighth-power inclusion');return r


def centered_poly(r,h):
    r=Q(r);h=Q(h);V=r*r+h*h+Q(1,4)
    return 16*V**7*r+112*V**5*r**3+112*V**3*r**5+16*V*r**7


def isolate_boundary(q,h,ell):
    q2=sum(x*x for x in q);need(q2>0 and h!=0 and ell>0,'actual boundary nondegenerate positive parameters')
    factor=q2**8
    def f(r):return factor*centered_poly(r,h)-ell
    lo,hi=Q(0),Q(4);need(f(lo)<0<f(hi),'independent centered r bracket')
    for _ in range(160):
        mid=(lo+hi)/2;value=f(mid)
        if value==0:lo=hi=mid;break
        if value<0:lo=mid
        else:hi=mid
    need((lo==hi and f(lo)==0) or f(lo)<0<f(hi),'strict isolating endpoints')
    return I(Q(1,2)-hi,Q(1,2)-lo),{'r':I(lo,hi).data(),'polynomial_at_lo':str(f(lo)),'polynomial_at_hi':str(f(hi)),'bisections':160}


def gram(B,C):
    a=norm2(B);b=dot(B,C);c=norm2(C);D=a*c-b.sq();need(D.lo>0,'strict positive Gram determinant');return a,b,c,D


def residual(s,B,C,L,M):
    a,b,c,D=gram(B,C);u=root8(s);v=root8(iv(s)+L);w=root8(iv(s)+M);r1=a+u-v;r2=c+u-w
    return (c*r1.sq()-2*b*r1*r2+a*r2.sq()-4*D*u)/(4*D)


def center_box(s,B,C,L,M):
    a,b,c,D=gram(B,C);db=scale(1/D,vsub(scale(c,B),scale(b,C)));dc=scale(1/D,vsub(scale(a,C),scale(b,B)))
    base=scale(Q(1,2),vadd(scale(a,db),scale(c,dc)));U=scale(Q(1,2),vadd(db,dc))
    return vsub(vsub(vadd(base,scale(root8(s),U)),scale(root8(iv(s)+L)/2,db)),scale(root8(iv(s)+M)/2,dc))


def refine(lo,hi,B,C,L,M):
    lo,hi=Q(lo),Q(hi);sl=residual(lo,B,C,L,M).sign();sh=residual(hi,B,C,L,M).sign();need(sl*sh==-1,'strict opposite initial signs')
    for _ in range(80):
        mid=(lo+hi)/2;sm=residual(mid,B,C,L,M).sign();need(sm!=0,'ambiguous midpoint sign; never forced')
        if sm==sl:lo=mid
        else:hi=mid
    need(residual(lo,B,C,L,M).sign()==sl and residual(hi,B,C,L,M).sign()==sh,'retained opposite signs')
    return I(lo,hi)


def strict_inside(value,lo,hi,why):
    need(Q(lo)<value.lo<=value.hi<Q(hi),why)


def run():
    # Arithmetic/domain controls are independent of target sign values.
    for q in [Q(0),Q(1),Q(2),Q(1,10**40),Q(10**16),Q(27,1250),Q(9,10000)]:root8(q)
    need((I(-3,-2)*I(-5,-4)).data()==I(8,15).data(),'signed interval multiplication');need(I(-2,3).sq().data()==I(0,9).data(),'zero-crossing square')
    negatives=[]
    def rejected(name,fn):
        try:fn()
        except ValueError as exc:negatives.append({'case':name,'rejected':True,'reason':str(exc)})
        else:raise ValueError('unrejected independent false control '+name)
    rejected('negative_radical_domain',lambda:root8(I(-1)))
    rejected('denominator_crossing_zero',lambda:I(1)/I(-1,1))
    rejected('reversed_interval',lambda:I(2,1))
    rejected('collinear_focus_Gram',lambda:gram(point(1,0),point(2,0)))
    b,c,d,lam=Q(2073,10000),Q(4719,10000),Q(64,10000),Q(27,1250)
    A=point(0,0);B=point(b,0);C=point(c,d)
    table=[(Q(9,10000),'0.38','0.39'),(Q(11,10000),'-0.28','-0.27'),(Q(13,10000),'0.51','0.52'),(Q(1,2),'-0.91','-0.90'),(Q(1),'9','10'),(Q(10**16),'-4.766','-4.765')]
    signs=[]
    for s,lo,hi in table:
        r=residual(s,B,C,lam,1);strict_inside(r,lo,hi,'independent Gram endpoint sign range '+str(s));signs.append({'s':str(s),'residual':r.data()})
    need([x['residual']['strict_sign'] for x in signs]==[1,-1,1,-1,1,-1],'six strict alternating signs')
    x0=b/2;y0=(c*c+d*d-b*c)/(2*d);need(x0*x0+y0*y0==Q(39007985196121,409600000000),'exact limiting norm identity')
    tail=I(x0-lam/(16*b*10**14),x0).sq()+I(y0-Q(1,16*d*10**14),y0+(c/b)*lam/(16*d*10**14)).sq()-100
    strict_inside(tail,'-4.766','-4.765','analytic cancellation-free tail bound')
    t1,r1=isolate_boundary((c,d),Q(10),Q(1));t3,r3=isolate_boundary((b,Q(0)),Q(1),lam);t5,r5=isolate_boundary((c-b,d),Q(-10),1-lam)
    A1=vadd(scale(t1,C),scale(10,J(C)));A3=vadd(scale(t3,B),J(B));CB=vsub(C,B);A5=vadd(vadd(B,scale(t5,CB)),scale(-10,J(CB)))
    boundary=[A1,A,A3,B,A5,C]
    published_boxes=[(A1,('0.17194','0.17196'),('4.72219','4.72221')),(A3,('-0.55229','-0.55227'),None),(A5,('0.40359','0.40361'),('-2.64281','-2.64279'))]
    for P,x,y in published_boxes:
        strict_inside(P[0],*x,'boundary x range')
        if y:strict_inside(P[1],*y,'boundary y range')
    need(A3[1].lo==A3[1].hi==b,'exact A3 height')
    pairs=list(combinations(range(6),2));triples=[]
    for i,j in pairs:need(norm2(vsub(boundary[i],boundary[j])).lo>0,'all six vertices distinct')
    for i,j,k in combinations(range(6),3):
        value=orient(boundary[i],boundary[j],boundary[k]);need(value.sign()!=0,'all20 boundary triples noncollinear');triples.append({'indices':[i+1,j+1,k+1],'area2':value.data()})
    even=orient(A,B,C);need(even.lo==even.hi==Q('0.00132672'),'exact even determinant');odd=orient(A1,A3,A5);strict_inside(odd,'6.37','6.39','odd determinant')
    crossings=[orient(A1,A,A3),orient(A1,A,B),orient(A3,B,A1),orient(A3,B,A)]
    need([x.sign() for x in crossings]==[-1,1,1,-1],'strict interior boundary crossing')
    rejected('noncrossing_embedding_claim',lambda:need(crossings[0].sign()*crossings[1].sign()!=-1,'fixed boundary has strict crossing'))
    L=norm16(vsub(B,A5))-norm16(vsub(B,A3));M=norm16(A1)-norm16(A3);need(L.lo>0 and M.lo>0,'fixed incoming shifts positive')
    BP=vsub(A5,A3);CP=vsub(A1,A3);incoming=[]
    for s,lo,hi in [(Q(1,100),'0.00037','0.00038'),(Q(11,1000),'-0.00081','-0.00080')]:
        r=residual(s,BP,CP,L,M);strict_inside(r,lo,hi,'incoming Gram sign');incoming.append({'s':str(s),'residual':r.data()})
    Z=vadd(A3,center_box(I(Q(1,100),Q(11,1000)),BP,CP,L,M));strict_inside(Z[0],'0.1677','0.1717','whole incoming x');strict_inside(Z[1],'-0.0036','-0.0026','whole incoming y')
    roots=[];centers=[]
    for left,right in zip(table,table[1:]):
        bracket=refine(left[0],right[0],B,C,lam,1);X=center_box(bracket,B,C,lam,1);need(X[0].hi<b/2,'all selected outgoing centers left of bisector');roots.append(bracket);centers.append(X)
    need(Z[0].lo>b/2,'incoming/outgoing center separation')
    for left,right in zip(centers,centers[1:]):need(left[0].hi<right[0].lo,'pairwise distinct outgoing x boxes')
    line_checks=[]
    for n,P in enumerate([Z]+centers):
        for i,j in pairs:
            area=orient(boundary[i],boundary[j],P);need(area.sign()!=0,'every selected center avoids all15 boundary-pair lines');line_checks.append({'center':'incoming' if n==0 else 'outgoing'+str(n),'pair':[i+1,j+1],'area2':area.data()})
    a,f,g=norm16(A1),norm16(A3),norm16(vsub(A5,B))
    # Exact linear coefficient identities, not interval-containment evidence.
    def add(*terms):return tuple(sum(x) for x in zip(*terms))
    def neg(x):return tuple(-v for v in x)
    E=[tuple(int(i==j) for i in range(7)) for j in range(7)]
    aa,ff,gg,ll,one,rr,qq=E;r_one=add(rr,aa,neg(ff));r_five=add(rr,gg,neg(ff),neg(ll));qB=add(qq,ll);qC=add(qq,one)
    equations=[(add(aa,rr),add(r_one,ff)),(add(ff,ll,r_five),add(rr,gg)),(add(gg,one,neg(ll),r_one),add(r_five,aa,one)),(add(ff,qB),add(qq,ff,ll)),(add(gg,qC),add(qB,gg,one,neg(ll))),(add(aa,one,qq),add(qC,aa))]
    need(all(left==right for left,right in equations),'all six face identities exactly cancel')
    rejected('wrong_third_face_constant',lambda:need(add(aa,neg(one),qq)==add(qC,aa),'wrong boundary edge fails exact coefficient identity'))
    for P in [A,B,C,A1,A3,A5]:need(norm2(vsub(Z,P)).lo>0,'incoming point distinct from boundary')
    return {'status':'PASS_INDEPENDENT_FIXED_CONSTRUCTION_CERTIFICATE','mechanisms':['centered positive boundary polynomial','binary triple-isqrt eighth-root enclosure','Gram-adjugate residual','exact cycle coefficient identities','strict oriented-area separation'],
        'binary_root_grid_bits':256,'boundary_bisections_each':160,'outgoing_bisections_each':80,'strict_G_endpoints':signs,'analytic_tail_G':tail.data(),
        'boundary_parameters':[r1,r3,r5],'boundary_boxes':[[x.data(),y.data()] for x,y in boundary],'all20_boundary_triples':triples,
        'strict_boundary_crossing_signs':[x.sign() for x in crossings],'incoming_L':L.data(),'incoming_M':M.data(),'incoming_endpoint_signs':incoming,'whole_incoming_box':[x.data() for x in Z],
        'five_disjoint_s_brackets':[x.data() for x in roots],'five_outgoing_boxes':[[x.data(),y.data()] for x,y in centers],'all90_center_pair_line_checks':line_checks,
        'all_six_exact_face_coefficient_identities':[[list(a),list(b)] for a,b in equations],'false_controls':negatives,'exact_total_center_count_claimed':False,'proper_embedding_claimed':False,
        'foreign_native_or_peer_science_imports':[],'source_programs_or_expected_certificates_read':False,'finite_validated_certificate_plus_universal_geometric_reduction':True}


if __name__=='__main__':print(json.dumps(run(),indent=2))
