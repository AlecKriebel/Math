#!/usr/bin/env python3
"""Independent symbolic controls. Requires SymPy; does not prove general descent."""
import json
import sympy as s


def require(value,message):
    if not value:raise RuntimeError(message)

def run():
    a,b,t,c,z,u=s.symbols('a b t c z u',nonzero=True)
    E=s.Matrix([[0,1],[0,0]]);F=E.T;H=s.diag(1,-1)
    X=s.Matrix([[0,a],[b,0]])
    checks=[]
    def equal(label,left,right):
        diff=left-right
        values=list(diff) if isinstance(diff,s.MatrixBase) else [diff]
        require(all(s.cancel(x)==0 for x in values),label)
        checks.append(label)
    bracket=lambda x,y:x*y-y*x
    equal('sl2_EF',bracket(E,F),H)
    equal('sl2_HE',bracket(H,E),2*E)
    equal('sl2_HF',bracket(H,F),-2*F)
    equal('normal_involution_E',H*E*H,-E)
    equal('normal_involution_F',H*F*H,-F)
    equal('normal_involution_H',H*H*H,H)
    equal('p_f_centralizer_equation',bracket(X,F),a*H)
    equal('p_e_centralizer_equation',bracket(X,E),-b*H)
    equal('PGL_effective_action',s.diag(t,1)*X*s.diag(1/t,1),s.Matrix([[0,t*a],[b/t,0]]))
    equal('SL_cover_action',s.diag(u,1/u)*X*s.diag(1/u,u),s.Matrix([[0,u**2*a],[b/u**2,0]]))
    equal('product_invariant',(t*a)*(b/t),a*b)
    equal('plus_product',t*c/t,c)
    equal('minus_product',c*t/t,c)
    equal('plus_inverse_coordinate_b',(a*b)/a,b)
    equal('minus_inverse_coordinate_a',(a*b)/b,a)
    equal('plus_inverse_then_chart_t',t,t)
    equal('minus_inverse_then_chart_t',1/(1/t),t)
    equal('generic_orbit_witness_first',z*1,z)
    equal('generic_orbit_witness_second',z/z,1)
    equal('overlap_slice_transition_first',c*1,c)
    equal('overlap_slice_transition_second',c/c,1)
    # These coordinates are free variables here, not assumed nonzero.
    r,v,w,x=s.symbols('r v w x')
    M=s.Matrix([[r,v],[w,x]])
    equal('SL2_commutator_formula',bracket(M,E),s.Matrix([[-w,r-x],[0,w]]))
    equal('SL2_centralizer_determinant',M.subs({w:0,x:r}).det(),r**2)
    equal('SL2_component_factorization',s.factor(r**2-1),(r-1)*(r+1))
    centralizers=[]
    for n in range(2,9):
        coefficients=s.symbols('d0:'+str(n))
        N=s.zeros(n)
        for i in range(n-1):N[i,i+1]=1
        C=sum((coefficients[i]*(N**i) for i in range(n)),s.zeros(n))
        equal('regular_nilpotent_commutation_n'+str(n),C*N-N*C,s.zeros(n))
        equal('regular_nilpotent_determinant_n'+str(n),C.det(),coefficients[0]**n)
        centralizers.append({'n':n,'determinant':'d0^'+str(n),'SL_component_count_in_characteristic_zero':n})
    negative=[]
    require(s.cancel((t*a)*(t*b)-a*b)!=0,'wrong weight escaped detection')
    negative.append('same-sign torus weights fail product invariance')
    require(s.cancel((u*a)*(b/u)-((u**2*a)*(b/u**2)))==0,'same product control')
    require(s.diag(u,1/u)*X*s.diag(1/u,u)!=s.Matrix([[0,u*a],[b/u,0]]),
            'SL2 weights incorrectly treated as effective coordinates')
    negative.append('SL2 weights are plus/minus two for diag(u,u^-1)')
    A=(s.Integer(1),s.Integer(0));B=(s.Integer(0),s.Integer(1))
    require(A!=B and A[0]*A[1]==B[0]*B[1],'axis collapse control')
    require(t*A[0]!=B[0] and (A[1]/t)!=B[1],'axes incorrectly conjugate by diagonal torus')
    negative.append('product map merges two distinct diagonal-torus orbits')
    require(B[0]==0 and A[1]==0,'single-chart omission control')
    negative.append('each single slice saturation omits the opposite punctured axis')
    require(s.expand((r-1)*(r+1))==r**2-1,'SL2 component control')
    negative.append('SL2 regular nilpotent centralizer has two components')
    return {'schema':1,'engine':'SymPy '+s.__version__,'coefficient_domain':'characteristic zero rational functions',
            'identities_passed':len(checks),'identity_names':checks,
            'negative_controls':negative,'negative_count':len(negative),
            'finite_matrix_controls':centralizers,
            'scope':'rank-one rational identities and n=2..8 regular-centralizer controls; geometric descent and general connectedness are established only by prose reasoning'}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
