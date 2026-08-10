from fractions import Fraction
from one_active_debt import coefficients_for_channel,verify_bimolecular_sign,service_token_vector,PolynomialEdge,quadratic_drift_bound
from one_active_poisson import poisson,corrected_variance

def test_exact_polynomial_rates():
    assert coefficients_for_channel((2,0,0),Fraction(3),7,8)==(Fraction(3),0,0)
    assert coefficients_for_channel((1,1,0),Fraction(2),4,0)==(0,Fraction(8),0)
    assert coefficients_for_channel((0,1,1),Fraction(5),3,2)==(0,0,Fraction(30))

def test_signs_and_token():
    verify_bimolecular_sign((2,0,0),(1,1,0),True)
    verify_bimolecular_sign((1,0,1),(0,0,1),False)
    kind,w=service_token_vector(((0,0,0),(1,1,0)))
    assert kind=="invariant" and w==(1,-1,0)

def test_poisson_and_critical_variance():
    P=((Fraction(1,2),Fraction(1,2)),(Fraction(1,3),Fraction(2,3)))
    pi,mean,h=poisson(P,(Fraction(-1),Fraction(0)))
    assert mean<0
    Q=((0,1),(1,0));edge=((0,1),(-1,0))
    assert corrected_variance(Q,edge,(0,0))==1
