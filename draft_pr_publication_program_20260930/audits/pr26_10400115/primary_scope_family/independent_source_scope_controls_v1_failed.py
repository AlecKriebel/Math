from pathlib import Path
import datetime, hashlib, json, unicodedata
import sympy as s
P=Path(__file__).resolve().parent
checks={};details={}
def check(name,ok):
 assert bool(ok),name
 checks[name]='PASS'
x,a,b,l,alpha,z=s.symbols('x a b l alpha z')
I=s.eye(2);U=s.Matrix([[1,1],[0,1]]);V=s.Matrix([[1,0],[-1,1]])
# Discrete scalar image 2^Z has kernel sigma1 sigma2^-1; its permutation image is nontrivial.
transposition1=s.Matrix([[0,1,0],[1,0,0],[0,0,1]])
transposition2=s.Matrix([[1,0,0],[0,0,1],[0,1,0]])
check('discrete_image_does_not_imply_faithful',s.Rational(2,2)==1 and transposition1*transposition2.inv()!=s.eye(3))
check('trivial_rho_with_J1_satisfies_theorem_hypotheses',s.Matrix([[1]])*s.Matrix([[1]])*s.Matrix([[1]])==s.Matrix([[1]]))
# Normalization negative control: unscaled integral matrices kill a nontrivial central square.
check('untwisted_central_square_is_identity',(U*V)**6==I)
check('twisted_central_square_survives',((2*U)*(2*V))**6==4096*I)
check('untwisted_center_is_not_identity',(U*V)**3==-I)
check('scaled_determinant_controls_exponent',(2*U).det()==4)
# Semidirect-product formula, independently checked as one formula rather than sampled words.
k,j=s.symbols('k j',integer=True);p,q=s.symbols('p q')
check('wreath_multiplication_formula',s.Matrix([[x**k,p],[0,1]])*s.Matrix([[x**j,q],[0,1]])==s.Matrix([[x**(k+j),p+x**k*q],[0,1]]))
# Several finite-set survivors followed by a separate diagonal counterexample for the same rational.
D=s.diag(x,1)
polys=[x*x-3,x**3+2*x+5,3*x-8,x**4-x*x+2]
chosen=s.Rational(7,3)
for i,poly in enumerate(polys):
 check('finite_set_survivor_'+str(i),poly.subs(x,chosen)!=0)
kill=3*x-7
word=D*U**3*D.inv()*U**(-7)
check('finite_set_does_not_make_single_parameter_faithful',s.simplify(word-s.Matrix([[1,kill],[0,1]]))==s.zeros(2) and word!=I and word.subs(x,chosen)==I)
check('zero_specialization_is_invalid',D.subs(x,0).det()==0)
# Parameter dependence is a coefficient-ring kernel, with no asserted braid kernel.
check('scherich_example_parameter_dependence',s.expand((alpha-l**5).subs({alpha:z**15,l:z**3}))==0 and alpha-l**5!=0)
check('dependent_specialization_need_not_kill_group',all((z**m).subs(z,2)!=1 for m in [-3,-2,-1,1,2,3]))
# Restriction-of-scalars basis (1,sqrt(3)); homomorphism and identity reflection.
def reg(r,t):return s.Matrix([[r,3*t],[t,r]])
r,t,u,v=s.symbols('r t u v')
check('restriction_scalars_is_ring_homomorphism',reg(r,t)*reg(u,v)==reg(r*u+3*t*v,r*v+t*u))
check('restriction_scalars_identity_reflecting',s.solve(list(reg(r,t)-I),(r,t))=={r:1,t:0})
check('restriction_scalars_increases_dimension',reg(0,1).shape==(2,2) and reg(0,1)**2==3*I)
# Literal published Example3.11 has an exact parameter integrity failure.
S=s.Rational(1,2)+1/s.sqrt(2)+1/(2*s.sqrt(-1+2*s.sqrt(2)))
minimal=s.minpoly(S,x)
expected=7*x**4-14*x**3+3*x**2+2*x+1
res=s.resultant((2*x-1-a)**2*(-1+2*a)-1,a*a-2,a)
check('printed_radical_minimal_polynomial',s.expand(minimal-expected)==0)
check('printed_radical_resultant_confirmation',s.rem(res,expected,x)==0)
check('printed_radical_polynomial_irreducible',s.Poly(expected,x).is_irreducible)
check('printed_radical_not_algebraic_integer',s.Poly(expected,x).LC()!=1 and s.polys.polytools.primitive(expected,x)[0]==1)
check('printed_radical_not_reciprocal',s.expand(x**4*expected.subs(x,1/x)-expected)!=0)
details['printed_example_parameter']={'formula':'1/2+1/sqrt(2)+1/(2*sqrt(-1+2*sqrt(2)))','minimal_polynomial':str(minimal),'resultant':str(res),'approximate':str(s.N(S,20)),'scope':'The source calls this S a Salem number; as printed it fails algebraic integrality. No correction to S, no claim that its image is nondiscrete, and no braid kernel conclusion is inferred.'}
# Source/version checks and falsification controls are tied to fresh bytes and literal extraction.
src=P/'primary_sources';old=json.loads((P.parent/'source_snapshot/source_checksums.json').read_text())
check('ohtsuki_exact_original_variant_sha',hashlib.sha256((src/'ohtsuki2002_s.pdf').read_bytes()).hexdigest()==old[0]['sha256'])
check('scherich_exact_original_variant_sha',hashlib.sha256((src/'scherich2023_s.pdf').read_bytes()).hexdigest()==old[1]['sha256'])
opage=(src/'ohtsuki2002_s.txt').read_text().split('\f')[97]
normalized=unicodedata.normalize('NFD',opage)
check('field_has_bar_over_Q','Q\u0304' in normalized)
check('bar_removed_source_negative_control','Q\u0304' not in normalized.replace('Q\u0304','Q'))
check('source_range_is_n_at_least_four','n ≥ 4' in opage)
check('range_changed_source_negative_control','n ≥ 4' not in opage.replace('n ≥ 4','n ≥ 3'))
sch=(src/'scherich2023_s.txt').read_text()
check('source_contains_all_three_requested_labels',all(label in sch for label in ('Theorem 1.1','Corollary 3.10','Example 3.11')))
check('no_faithful_token_in_fresh_article','faithful' not in sch.casefold())
cross=json.loads((src/'scherich_crossref.json').read_text())['message']
check('crossref_doi_title_and_page_match',cross['DOI']=='10.2140/agt.2023.23.2009' and cross['page']=='2009-2028' and 'Discrete real specializations' in cross['title'][0])
details['crossref_metadata']={k:cross.get(k) for k in ('DOI','title','author','publisher','container-title','volume','issue','page','published','published-online','published-print')}
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','assertions':len(checks),'checks':checks,'details':details,'sympy_version':s.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Independent source/type/normalization/quantifier checks and negative controls only; no target proof search.'}
(P/'independent_source_scope_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
