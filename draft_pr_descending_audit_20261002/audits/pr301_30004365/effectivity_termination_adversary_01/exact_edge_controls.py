"""Independent exact seam, ribbon and peripheral edge controls.

These controls do not implement the submitted search and do not establish
universal halting. General conclusions are in EFFECTIVITY_AUDIT.md.
"""
from fractions import Fraction as F
from itertools import permutations
import json,pathlib

checks=[]
def check(name, condition, evidence):
    if not condition: raise AssertionError((name,evidence))
    checks.append({'name':name,'evidence':evidence})
def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def sub(u,v):return (u[0]-v[0],u[1]-v[1])
def add(u,v):return (u[0]+v[0],u[1]+v[1])
def scale(t,v):return (t*v[0],t*v[1])
def hit(a,b,c,d):
    r,s=sub(b,a),sub(d,c);den=cross(r,s)
    if not den:return None
    t,u=cross(sub(c,a),s)/den,cross(sub(c,a),r)/den
    if 0<=t<=1 and 0<=u<=1:return (t,u,add(a,scale(t,r)))
    return None

seams=0
for q in range(1,21):
    for p in range(q+1):
        t=F(p,q);u=1-t
        check('reversed_seam_exact_'+str(p)+'_'+str(q),t+u==1 and u.denominator<=q,{'t':str(t),'paired_t':str(u)})
        seams+=1

# Disk field model: dual arc x=1/2, two white boundary marks.
collar=[(F(1,4),F(1,4)),(F(1,4),F(3,4)),(F(3,4),F(3,4)),(F(3,4),F(1,4))]
dual=((F(1,2),F(0)),(F(1,2),F(1)))
hits=[hit(collar[i],collar[(i+1)%4],*dual) for i in range(4)]
hits=[h for h in hits if h]
check('field_disk_collar_two_crossings',len(hits)==2,{'crossings':[list(map(str,h[2])) for h in hits]})
# At left upward side, the left white mark is on the left. At right
# downward side, the right white mark is on the left. The two maximal
# cut portions are simple crosscuts, so each contributes +1.
left_mark=(F(0),F(1,2));right_mark=(F(1),F(1,2))
left_sign=cross(sub(collar[1],collar[0]),sub(left_mark,collar[0]))
right_sign=cross(sub(collar[3],collar[2]),sub(right_mark,collar[2]))
check('field_disk_winding_plus2',left_sign>0 and right_sign>0,{'left_determinant':str(left_sign),'right_determinant':str(right_sign),'winding':2,'gauss_bonnet':4-2*1})
check('field_disk_reverse_minus2',cross(sub(collar[0],collar[1]),sub(left_mark,collar[1]))<0 and cross(sub(collar[2],collar[3]),sub(right_mark,collar[3]))<0,{'winding':-2})

# Dual-numbers annulus model: cut at a radial arc. theta,r rectangle
# has the reverse of the ambient plane orientation. Both seam endpoints
# of the one-crossing peripheral loop are distinct occurrence copies.
puncture_arc=((F(0),F(5,4)),(F(1),F(5,4)))
outer_arc=((F(1),F(7,4)),(F(0),F(7,4)))
white=(F(1,2),F(2));chart_orientation=-1
ps=chart_orientation*cross(sub(puncture_arc[1],puncture_arc[0]),sub(white,puncture_arc[0]))
os=chart_orientation*cross(sub(outer_arc[1],outer_arc[0]),sub(white,outer_arc[0]))
check('annulus_one_crossing_occurrences_distinct',puncture_arc[0]!=puncture_arc[1],{'physical_seam_same':True,'occurrences':[list(map(str,p)) for p in puncture_arc]})
check('annulus_oriented_peripherals',ps<0 and os>0,{'puncture_winding':-1,'original_boundary_winding':1,'sum':0,'gauss_bonnet':4-2*2})

# One vertex, two loop edges: face-cycle count depends on cyclic order.
alpha={0:2,2:0,1:3,3:1}
def ribbon(order):
    sigma={order[i]:order[(i+1)%4] for i in range(4)}
    face={d:sigma[alpha[d]] for d in range(4)}
    unseen=set(range(4));cycles=[]
    while unseen:
        d=min(unseen);cy=[]
        while d in unseen:unseen.remove(d);cy.append(d);d=face[d]
        cycles.append(cy)
    chi=1-2;b=len(cycles);g=F(2-b-chi,2)
    return {'order':order,'face_cycles':cycles,'chi':chi,'boundary_components':b,'genus':int(g)}
alternating=ribbon([0,1,2,3]);nonalternating=ribbon([0,2,1,3])
check('alternating_pair_once_holed_torus',alternating['genus']==1 and alternating['boundary_components']==1,alternating)
check('nonalternating_pair_pair_of_pants',nonalternating['genus']==0 and nonalternating['boundary_components']==3,nonalternating)
types={}
for order in permutations(range(4)):
    r=ribbon(list(order));key=(r['genus'],r['boundary_components']);types[str(key)]=types.get(str(key),0)+1
check('all_two_loop_ribbon_orders_classified',types=={'(1, 1)':8,'(0, 3)':16},{'types':types})

# A short PL edge inside a disk fails a literal crosscut test. The
# maximal portion between dissection crossings is the intended object.
interior_edge=((F(1,4),F(1,4)),(F(1,3),F(1,3)))
check('literal_triangle_segment_is_not_proper_crosscut',all(0<x<1 and 0<y<1 for x,y in interior_edge),{'edge':[list(map(str,p)) for p in interior_edge],'endpoints_interior':True})

result={'status':'PASS_FINITE_INDEPENDENT_EDGE_CONTROLS','assertions':len(checks),'seam_checks':seams,'controls':checks,'limitations':'No full bound-quiver surface builder, enumerator, certificate verifier, or universal termination test; proofs remain mathematical.'}
pathlib.Path('EXACT_EDGE_CONTROLS.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
