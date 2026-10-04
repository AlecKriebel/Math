"""Independent finite controls. No finite output substitutes for a tail theorem."""
from fractions import Fraction
from itertools import product
import json

def next_marker(word, i, sentinel):
    for j in range(i, len(word)):
        if word[j] != 0:
            return word[j], j-i
    return sentinel, len(word)-i

def marker_control():
    cases = 0
    failures = []
    for word in product(range(3), repeat=8):
        for cut in range(8):
            original = [next_marker(word,i,1)[0] for i in range(cut+1)]
            splice = [next_marker(word[:cut+1],i,2)[0] for i in range(cut+1)]
            last = max([i for i in range(cut+1) if word[i]!=0],default=-1)
            expected = [i for i in range(last+1,cut+1) if original[i]!=splice[i]]
            actual = [i for i in range(cut+1) if original[i]!=splice[i]]
            if actual!=expected:
                failures.append({'word':word,'cut':cut,'actual':actual,'expected':expected})
            for i in range(cut+1):
                symbol,radius=next_marker(word,i,1)
                if i+radius<=cut and original[i]!=splice[i]:
                    failures.append({'word':word,'cut':cut,'i':i,'radius':radius})
            cases += 1
    return {'word_length':8,'alphabet':[0,1,2],'cases':cases,'failures':failures,
            'geometric_radius_mean_for_uniform_input':'1/2',
            'meaning':'Finite marker-code locality and eventual-agreement control only'}

def rotation_control():
    rows=[]
    for modulus,step,threshold in [(11,4,5),(17,6,8),(29,11,14)]:
        future=[tuple(int((u+n*step)%modulus<threshold) for n in range(modulus)) for u in range(modulus)]
        past=[tuple(int((u-n*step)%modulus<threshold) for n in range(modulus)) for u in range(modulus)]
        rows.append({'modulus':modulus,'step':step,'threshold':threshold,
                     'future_distinct':len(set(future)),'past_distinct':len(set(past)),
                     'phase_recovered_both':len(set(future))==modulus==len(set(past))})
    return {'rows':rows,'meaning':'Finite rational controls; irrational tail recovery is proved in baseline'}

def quotient_control():
    parameters=[(Fraction(1,4),0),(Fraction(1,4),1),(Fraction(1,2),0),(Fraction(1,2),1),(Fraction(3,4),0),(Fraction(3,4),1)]
    vectors=[]
    for p,v in parameters:
        vectors.append((p,v,tuple(p**sum(w)*(1-p)**(len(w)-sum(w)) for k in (1,2,3) for w in product((0,1),repeat=k))))
    distinct=len(set(z[2] for z in vectors))
    redundant_equal=all(vectors[2*j][2]==vectors[2*j+1][2] for j in range(3))
    ex=sum(p for p,v in parameters)/6
    exx=sum(p*p for p,v in parameters)/6
    return {'parameter_count':len(parameters),'observable_cylinder_quotient_count':distinct,
            'unused_latent_labels_indistinguishable':redundant_equal,
            'E_X0':str(ex),'E_X0_Xn_for_n_nonzero':str(exx),'covariance':str(exx-ex*ex),
            'meaning':'Exact finite mixture arithmetic and redundant-parameter negative control'}

def reset_control():
    rows=[]
    for q in [Fraction(1,2),Fraction(1,10),Fraction(1,100),Fraction(1,1000)]:
        rows.append({'q':str(q),'m':7,'no_reset':str((1-q)**6),
                     'block_coupling_error_bound':str(1-(1-q)**6),
                     'dependence_bound_n20':str((1-q)**20)})
    return {'rows':rows,'meaning':'Exact reset-coupling bounds; weak-limit obstruction is proved in baseline'}

result={'status':'PASS','finite_controls_only':True,'marker':marker_control(),
        'rotation':rotation_control(),'quotient':quotient_control(),'reset':reset_control()}
if result['marker']['failures'] or not all(r['phase_recovered_both'] for r in result['rotation']['rows']) or not result['quotient']['unused_latent_labels_indistinguishable'] or result['quotient']['observable_cylinder_quotient_count']!=3:
    result['status']='FAIL'
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['status']=='PASS' else 1)
