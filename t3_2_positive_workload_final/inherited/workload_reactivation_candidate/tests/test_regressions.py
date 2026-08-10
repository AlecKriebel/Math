from current_target_regressions import exact_one_value,two_linkage_conditioned,honest_two_linkage
from counterexample_search import weighted_zero_detailed_balance,critical_queue

def test_conditional_activation_regressions():
    for n in (100,1000,10000):
        assert exact_one_value(n)>0
        assert two_linkage_conditioned(n)>0
        assert honest_two_linkage(n)<0

def test_weighted_zero_and_critical():
    assert all(weighted_zero_detailed_balance(h,l) for h in range(1,5) for l in range(5))
    assert critical_queue(1,1,2)=="critical_nonzero_variance"
