from fractions import Fraction
from chart_flow_gluing import ChartEdge,verify_flow_balance,terminal_components,common_workload
from global_green_closure import endpoint_balance,upward_rate_linear_bound

def test_chart_flow():
    E=(ChartEdge("a","b",Fraction(7)),ChartEdge("b","a",Fraction(7)))
    assert verify_flow_balance(("a","b"),E)=={"a":0,"b":0}
    assert terminal_components(("a","b"),E)==(("a","b"),)

def test_endpoint_and_nonexplosion_bound():
    assert endpoint_balance((2,1),((1,0,0),(-1,1,0)))==(Fraction(1,3),Fraction(1,3),0)
    assert upward_rate_linear_bound(((0,2,True),(1,3,True),(2,100,False)))==(2,3)
