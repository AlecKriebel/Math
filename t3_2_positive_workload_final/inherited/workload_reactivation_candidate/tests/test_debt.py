from fractions import Fraction
from aggregate_debt import certify,drift_bound,expected_hitting_trials,one_step_upper_bound
from debt_queue_foster import certify as queue_certify

def test_scalar_debt():
    c=certify(service_probability=Fraction(3,5),mean_arrival_bound=Fraction(1,5))
    assert drift_bound(debt=4,service_probability=c.service_probability,
                       mean_arrival_bound=c.mean_arrival_bound)==Fraction(-2,5)
    assert expected_hitting_trials(4,c)==10

def test_pathwise_reflection():
    for d in range(1,8):
        for s in range(4):
            for a in range(4):
                nxt=one_step_upper_bound(d,s,a)
                assert nxt-d <= -int(s>=1)+a

def test_queue_capacity():
    q=queue_certify(path_length=2,edge_probability_lower_bound=Fraction(1,2),
                    slower_to_carrier_ratio=Fraction(1,10000),
                    maximum_single_arrival=2,mean_trial_duration_bound=5)
    assert q.debt.drift_margin>0
