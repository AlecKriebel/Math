"""Publication replay controls; all guards remain active under python -O."""
import ast
import json
from pathlib import Path
import sympy as s
from branch_integrality import X, A, kernel, verify_witness, require
from audit_independent_model import linear_normal_form
from audit_division_free import division_free_dimension

x,y,z=X

def rejected(name, action, expected):
    try:
        action()
    except expected:
        return {'name':name,'rejected':True}
    raise RuntimeError('Invalid mutation was accepted: '+name)

def main():
    invalid=[
        ('empty',lambda:kernel([],1,2)),
        ('zero',lambda:kernel([0],1,2)),
        ('constant',lambda:kernel([1],1,2)),
        ('nonhomogeneous',lambda:kernel([x+1],1,2)),
        ('nonreduced',lambda:kernel([z*z],2,4)),
        ('duplicate',lambda:kernel([z,z],1,2)),
        ('shared_component',lambda:kernel([x*y,y*z],1,4)),
        ('zero_order',lambda:kernel([z],0,2)),
        ('negative_order',lambda:kernel([z],-1,2)),
        ('nonintegral_order',lambda:kernel([z],1.5,2)),
        ('nonintegral_twist',lambda:kernel([z],1,2.5)),
        ('zero_witness',lambda:verify_witness([z],1,2,0)),
        ('wrong_bidegree',lambda:verify_witness([z],1,2,z*A[0])),
        ('zero_incidence_class',lambda:verify_witness([z],1,3,sum(t*a for t,a in zip(X,A)))),
        ('wrong_branch_witness',lambda:verify_witness([z],1,2,A[2])),
        ('invalid_witness_order',lambda:verify_witness([z],0,2,A[0])),
    ]
    controls=[rejected(name,action,ValueError) for name,action in invalid]
    controls.append(rejected('false_require',lambda:require(False,'deliberate mutation'),AssertionError))
    if not verify_witness([z],1,2,A[0]):
        raise RuntimeError('Valid witness rejected')
    F=x*z-y*y-y*z-z*z
    if kernel([F],1,3)['dimension']!=3 or kernel([F],2,4)['dimension']!=1:
        raise RuntimeError('Transformed-conic regression')
    if division_free_dimension([F],1,3)!=3 or division_free_dimension([F],2,4)!=1:
        raise RuntimeError('Division-free transformed-conic regression')
    E1=x*y+x*z;E2=-x*y
    def normalize(E):
        return s.Poly.from_dict(linear_normal_form(E,F),X,domain=s.QQ).as_expr()
    if s.expand(normalize(E1)+normalize(E2)-normalize(E1+E2))!=0:
        raise RuntimeError('Independent normal form is not additive')
    if kernel([x*y*z],2,4)['dimension']!=kernel([x,y,z],2,4)['dimension']:
        raise RuntimeError('Split/product mismatch')
    files=sorted(p.name for p in Path(__file__).parent.glob('*.py'))
    for filename in files:
        if any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(Path(__file__).with_name(filename).read_text()))):
            raise RuntimeError('Optimization-removable assertion in '+filename)
    output={'negative_controls_count':len(controls),'negative_controls':controls,
            'valid_line_witness_accepted':True,'transformed_conic_dimensions':[3,1],
            'division_free_transformed_conic_dimensions':[3,1],
            'independent_normal_form_additivity':True,'split_product_agreement':True,
            'no_optimization_removable_asserts':files}
    Path(__file__).with_name('publication_controls_results.json').write_text(json.dumps(output,indent=2)+'\n')
    print('PASS: 17 rejection controls, valid witness, conic regression, additivity, split/product, explicit guards')

if __name__=='__main__':main()
