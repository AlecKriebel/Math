from fractions import Fraction
from physical_carrier_reactivation import PhaseEdge,ReturnCertificate,classify
from source_layer_hierarchy import EffectiveEdge,terminate_hierarchy

def test_closed_positive_forces_negative():
    E=(PhaseEdge("i","h",1),PhaseEdge("h","i",-1))
    C=(ReturnCertificate(0,(1,)),)
    out=classify(("i","h"),E,C)
    assert out[0].kind=="strict"

def test_zero_then_strict_layer():
    E=(EffectiveEdge(0,1,Fraction(0),0),EffectiveEdge(1,0,Fraction(0),0),
       EffectiveEdge(0,0,Fraction(-1),1),EffectiveEdge(1,1,Fraction(-1),1))
    out=terminate_hierarchy((0,1),E,1)
    assert [c.kind for c in out]==["zero","strict"] or set(c.kind for c in out)=={"zero","strict"}
