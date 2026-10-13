"""Small target-specific countercontrol: overwide T support is false.

Fox3 color propagation at a classical crossing is the bijection
(x,y)->(2x-y,x), with inverse (x,y)->(y,2y-x), over F3.
Closure colorings are fixed points. This is a diagnostic about an explicitly
invalid enlarged rule, not a proof of the Markov theorem or the valid schemes.
"""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
import json,os
H=Path(__file__).resolve().parent
def crossing(pair,sign):
    x,y=pair
    return ((2*x-y)%3,x) if sign==1 else (y,(2*y-x)%3)
def action(pair,word):
    for sign in word:pair=crossing(pair,sign)
    return pair
def colorings(word):return [list(x) for x in product(range(3),repeat=2) if action(x,word)==x]
def main():
    assert __debug__
    for pair in product(range(3),repeat=2):
        assert crossing(crossing(pair,1),-1)==pair
        assert crossing(crossing(pair,-1),1)==pair
    # An overwide prefix b=sigma1^2 at N=2 permits an invalid T enlargement.
    before=[1,1,1];after=[1,1,-1]
    assert len(colorings(before))==9 and len(colorings(after))==3
    # Valid T at N=2 forces an empty prefix: either terminal sign gives unknot.
    assert len(colorings([1]))==len(colorings([-1]))==3
    # Odd exponents have the same one-component permutation closure, despite
    # these different coloring counts, so that former finite check is too weak.
    assert len(before)%2==len(after)%2==1
    r={'schema':'pr50-support-countercontrol/v1','utc':datetime.now(timezone.utc).isoformat(),'actual_pid':os.getpid(),'status':'PASS_T_SUPPORT_IS_ESSENTIAL','invalid_generalization':{'N':2,'prefix_sigma1_exponent':2,'before_word_signs':before,'after_word_signs':after,'before_Fox3_closure_colorings':colorings(before),'after_Fox3_closure_colorings':colorings(after),'same_permutation_component_count':1,'actual_T_rejects_prefix_because_required_max_index_is_zero':True},'positive_actual_T_boundary_color_count':3,'target_proved_by_finite_control':False,'acceptance_approved':False}
    with (H/'SUPPORT_COUNTERCONTROL.json').open('x') as f:f.write(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'actual_pid':os.getpid(),'invalid_rule_color_counts':[9,3],'actual_rule_empty_prefix_color_counts':[3,3],'target_proved_by_finite_control':False},sort_keys=True))
if __name__=='__main__':main()
