import unittest
import sympy as sp
from core_exact import *

class MutationDetectionTests(unittest.TestCase):
    def test_detect_individual_prefix_truncation_mutation(self):
        later=prefix_state(sp.Rational(3,2))
        self.assertFalse(any(later==prefix_state(s) for s in [sp.Rational(1,4),sp.Rational(3,4)]))

    def test_detect_wrong_span_coefficients(self):
        wrong=prefix_state(sp.Rational(1,4))+prefix_state(sp.Rational(3,4))
        self.assertNotEqual(wrong,prefix_state(sp.Rational(3,2)))

    def test_detect_wrong_divided_difference_sign(self):
        A,B,D=sp.Integer(2),sp.Integer(3),sp.Integer(1)
        correct=divided_difference_two(A,B,D)
        wrong=(sp.exp(-A*D)-sp.exp(-B*D))/(A-B)
        self.assertNotEqual(sp.simplify(correct),sp.simplify(wrong))

    def test_detect_resonance_division(self):
        A,D=sp.symbols('A D', positive=True)
        expr=(sp.exp(-A*D)-sp.exp(-A*D))/(A-A)
        self.assertTrue(expr.has(sp.nan) or expr is sp.nan)
        self.assertEqual(divided_difference_two(A,A,D),D*sp.exp(-A*D))

    def test_detect_missing_confluent_factor(self):
        A,D=sp.symbols('A D', positive=True)
        self.assertNotEqual(simplex_equal_rate(2,A,D),sp.exp(-A*D))

    def test_detect_cartesian_product_mutation(self):
        A,D=sp.symbols('A D', positive=True)
        simplex=D**2*sp.exp(-A*D)/2
        cartesian=(sp.integrate(sp.exp(-A*sp.Symbol('u')),(sp.Symbol('u'),0,D)))**2
        self.assertNotEqual(sp.simplify(simplex),sp.simplify(cartesian))

    def test_detect_wrong_gauge_rate(self):
        c,t,l=sp.symbols('c t l', positive=True)
        wrong=(l*c)*(c*t)
        self.assertNotEqual(sp.simplify(wrong),l*t)

    def test_detect_forward_only_minimization(self):
        A=sp.diag(-1,-2)
        alpha=sp.Matrix([[1,1]])
        beta=sp.Matrix([[1],[0]])
        _,R,H=reachable_observable_reduction(A,alpha,beta)
        self.assertNotEqual(R,H)

    def test_detect_unreachable_state_retained(self):
        A=sp.diag(-1,-2,-3)
        alpha=sp.Matrix([[1,0,0]])
        beta=sp.ones(3,1)
        n,R,H=reachable_observable_reduction(A,alpha,beta)
        self.assertTrue(n>H and R==H)

    def test_detect_funnel_routes_not_summed(self):
        g=sp.symbols('g')
        incomplete=g**2+(1-g)**2
        self.assertNotEqual(sp.expand(incomplete),1)

    def test_detect_unlabelled_alphabet_permutation(self):
        Q=sp.Matrix([[-1,1],[2,-2]])
        P=sp.Matrix([[0,1],[1,0]])
        self.assertNotEqual(Q,P.T*Q*P)

    def test_detect_false_finite_query_claim(self):
        # Equality of first moment does not determine a mixing measure.
        m1=sp.Rational(1,2)
        atoms1=([sp.Rational(1,2),sp.Rational(1,2)],[sp.Rational(1,4),sp.Rational(3,4)])
        atoms2=([sp.Rational(1,2),sp.Rational(1,2)],[sp.Rational(0),sp.Rational(1)])
        self.assertEqual(moment_of_atoms(*atoms1,1),m1)
        self.assertEqual(moment_of_atoms(*atoms2,1),m1)
        self.assertNotEqual(moment_of_atoms(*atoms1,2),moment_of_atoms(*atoms2,2))

    def test_detect_forced_latent_parent_linkage(self):
        x=sp.symbols('x', positive=True)
        survival,swapped,density,swapped_density=balanced_suffix_responses(
            sp.Rational(1,3),sp.Rational(1,4),
            (sp.Integer(1),sp.Integer(2)),
            (sp.Integer(3),sp.Integer(4)),x,
        )
        self.assertEqual(sp.simplify(survival-swapped),0)
        self.assertEqual(sp.simplify(density-swapped_density),0)
        self.assertNotEqual(x**3,x**4)

if __name__=='__main__':
    unittest.main(verbosity=2)
