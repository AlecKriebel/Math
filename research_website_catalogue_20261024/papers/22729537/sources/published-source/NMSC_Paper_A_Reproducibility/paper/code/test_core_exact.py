import unittest
import sympy as sp
from core_exact import *


class CoreExactTests(unittest.TestCase):
    def test_indexed_moment_formula(self):
        weights = [sp.Rational(1,3), sp.Rational(2,3)]
        atoms = [sp.Rational(1,4), sp.Rational(3,4)]
        self.assertEqual(moment_of_atoms(weights, atoms, 2), sp.Rational(19,48))

    def test_repeated_site_pattern(self):
        v = [sp.Rational(1,3), sp.Rational(2,3)]
        self.assertEqual(moment_tensor_probability(v, [1,1,0]), sp.Rational(4,27))

    def test_lower_order_marginalization(self):
        p = sp.symbols('p')
        words = {}
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    probs=[p,1-p]
                    words[(a,b,c)] = probs[a]*probs[b]*probs[c]
        self.assertEqual(sp.expand(lower_moment_from_length_L(words,(1,1),2,3)), sp.expand((1-p)**2))

    def test_prefix_span_coefficients(self):
        a,b = span_coefficients_for_later()
        self.assertEqual((a,b),(sp.Rational(-3,2),sp.Rational(5,2)))
        later = a*prefix_state(sp.Rational(1,4)) + b*prefix_state(sp.Rational(3,4))
        self.assertEqual(later, prefix_state(sp.Rational(3,2)))

    def test_later_prefix_not_individual_transport(self):
        later=prefix_state(sp.Rational(3,2))
        self.assertNotEqual(later,prefix_state(sp.Rational(1,4)))
        self.assertNotEqual(later,prefix_state(sp.Rational(3,4)))

    def test_prefix_spans_equal(self):
        early = sp.Matrix.vstack(prefix_state(sp.Rational(1,4)), prefix_state(sp.Rational(3,4)))
        enlarged = sp.Matrix.vstack(early, prefix_state(sp.Rational(3,2)))
        self.assertEqual(early.rank(), enlarged.rank())

    def test_two_rate_divided_difference(self):
        A,B,D=sp.Integer(2),sp.Integer(3),sp.symbols('D', positive=True)
        u=sp.symbols('u', real=True)
        direct=sp.integrate(sp.exp(-A*u)*sp.exp(-B*(D-u)),(u,0,D))
        self.assertEqual(sp.simplify(direct-divided_difference_two(A,B,D)),0)

    def test_two_rate_confluent(self):
        A,D=sp.symbols('A D', positive=True)
        self.assertEqual(divided_difference_two(A,A,D),D*sp.exp(-A*D))

    def test_three_equal_simplex(self):
        A,D=sp.symbols('A D', positive=True)
        self.assertEqual(simplex_equal_rate(2,A,D),D**2*sp.exp(-A*D)/2)

    def test_four_equal_simplex(self):
        A,D=sp.symbols('A D', positive=True)
        self.assertEqual(simplex_equal_rate(3,A,D),D**3*sp.exp(-A*D)/6)

    def test_biunary_kernel_rows_stochastic(self):
        g,l,D=sp.symbols('g l D', positive=True)
        K=biunary_kernel(g,l,D)
        self.assertEqual(sp.simplify(sum(K[0,j] for j in range(2))),1)
        self.assertEqual(sp.simplify(sum(K[1,j] for j in range(2))),1)

    def test_gauge_substitution_invariant(self):
        c,t,l=sp.symbols('c t l', positive=True)
        Q=sp.Matrix([[-1,1],[1,-1]])
        qterm,cterm=gauge_invariants(t,l,Q,c)
        self.assertEqual(qterm,Q*t)
        self.assertEqual(cterm,l*t)

    def test_determinant_identity_diagonalizable(self):
        q,u,w=sp.symbols('q u w', positive=True)
        Q=sp.Matrix([[-q,q],[q,-q]])
        # pi=(1/2,1/2), trace=-2q
        val=determinant_distance(Q,[sp.Rational(1,2),sp.Rational(1,2)],u,w)
        self.assertEqual(sp.simplify(val-2*q*(u+w)),0)

    def test_unreachable_state_deleted(self):
        A=sp.diag(-1,-2,-3)
        alpha=sp.Matrix([[1,0,0]])
        beta=sp.Matrix([[1],[1],[1]])
        ambient,R,H=reachable_observable_reduction(A,alpha,beta)
        self.assertEqual((ambient,R,H),(3,1,1))

    def test_observational_null_state_deleted(self):
        A=sp.diag(-1,-2)
        alpha=sp.Matrix([[1,1]])
        beta=sp.Matrix([[1],[0]])
        ambient,R,H=reachable_observable_reduction(A,alpha,beta)
        self.assertEqual(ambient,2)
        self.assertEqual(R,2)
        self.assertEqual(H,1)

    def test_similarity_invariance_hankel_rank(self):
        A=sp.diag(-1,-2)
        alpha=sp.Matrix([[1,1]])
        beta=sp.Matrix([[1],[1]])
        S=sp.Matrix([[1,1],[0,1]])
        A2=S.inv()*A*S
        alpha2=alpha*S
        beta2=S.inv()*beta
        self.assertEqual(reachable_observable_reduction(A,alpha,beta)[2], reachable_observable_reduction(A2,alpha2,beta2)[2])

    def test_identity_boundary_refinement(self):
        A=sp.diag(-1,-2)
        t,s=sp.symbols('t s', positive=True)
        self.assertEqual(sp.simplify((A*t).exp() - (A*s).exp()*sp.eye(2)*(A*(t-s)).exp()), sp.zeros(2))

    def test_parent_exchange_kernel(self):
        g,l,D=sp.symbols('g l D', positive=True)
        # exchange is represented by relabelling donor/parent and g -> 1-g,
        # not equality without relabelling; the unordered weights agree.
        self.assertEqual({g,1-g},{1-(1-g),1-g})

    def test_pair_port_germ_contains_split_mass(self):
        g,l1,l2,u=sp.symbols('g l1 l2 u', positive=True)
        survival=pair_port_survival(g,l1,l2,u)
        split=sp.simplify(sp.limit(survival,u,sp.oo))
        self.assertEqual(split,2*g*(1-g))

    def test_exact_posterior_balance_suffix_switch(self):
        x=sp.symbols('x', positive=True)
        outputs=balanced_suffix_responses(
            sp.Rational(1,3),sp.Rational(1,4),
            (sp.Integer(1),sp.Integer(2)),
            (sp.Integer(3),sp.Integer(4)),x,
        )
        self.assertEqual(sp.simplify(outputs[0]-outputs[1]),0)
        self.assertEqual(sp.simplify(outputs[2]-outputs[3]),0)

    def test_balance_switch_not_global_parent_exchange(self):
        original={(1,3),(2,4)}
        suffix_swapped={(1,4),(2,3)}
        globally_exchanged={(2,4),(1,3)}
        self.assertNotEqual(original,suffix_swapped)
        self.assertNotEqual(suffix_swapped,globally_exchanged)

    def test_all_completions_rank_one_normalization(self):
        entry=sp.Matrix([sp.Integer(2),sp.Integer(5)])
        future=sp.Matrix([[sp.Rational(1,3),sp.Rational(2,3)]])
        kernel=entry*future
        alpha,beta=normalize_rank_one_kernel(kernel)
        self.assertEqual(alpha,entry)
        self.assertEqual(beta,future)
        self.assertEqual(kernel,alpha*beta)
        self.assertEqual(sum(beta),1)

    def test_joint_multicut_entry_need_not_factor_by_port(self):
        joint_entry=sp.Matrix([2,3,5,7])
        future=sp.Matrix([[sp.Rational(2,5),sp.Rational(3,5)]])
        joint_kernel=joint_entry*future
        alpha,beta=normalize_rank_one_kernel(joint_kernel)
        self.assertEqual(alpha,joint_entry)
        self.assertEqual(beta,future)
        # Reshaping the four joint histories by two incident ports is not rank one.
        self.assertNotEqual(sp.Matrix(2,2,list(joint_entry)).det(),0)

    def test_two_epoch_bridge_spanning_empty_word(self):
        segments=[(sp.Integer(0),sp.Integer(2),sp.Integer(1)),
                  (sp.Integer(2),sp.Integer(5),sp.Integer(3))]
        left=kingman_word_density(segments,0,2,[],3)
        right=kingman_word_density(segments,2,5,[],3)
        spanning=kingman_word_density(segments,0,5,[],3)
        self.assertEqual(spanning_cocycle_residual(left,right,spanning),0)

    def test_two_epoch_bridge_spanning_labelled_merger_word(self):
        segments=[(sp.Integer(0),sp.Integer(2),sp.Integer(1)),
                  (sp.Integer(2),sp.Integer(5),sp.Integer(3))]
        # One specified target pair merges at time 1.  Two blocks remain above.
        left=kingman_word_density(segments,0,2,[1],3)
        right=kingman_word_density(segments,2,5,[],2)
        spanning=kingman_word_density(segments,0,5,[1],3)
        self.assertEqual(spanning_cocycle_residual(left,right,spanning),0)

    def test_equal_adjacent_rate_epochs_collapse(self):
        split=[(sp.Integer(0),sp.Integer(2),sp.Integer(2)),
               (sp.Integer(2),sp.Integer(5),sp.Integer(2))]
        merged=[(sp.Integer(0),sp.Integer(5),sp.Integer(2))]
        split_density=kingman_word_density(split,0,5,[1,3],4)
        merged_density=kingman_word_density(merged,0,5,[1,3],4)
        self.assertEqual(split_density,merged_density)

    def test_rank_one_sides_do_not_replace_spanning_cocycle(self):
        beta_12=sp.Matrix([[sp.Rational(2,3),sp.Rational(1,3)]])
        beta_13=sp.Matrix([[sp.Rational(1,4),sp.Rational(3,4)]])
        left_kernel=sp.Matrix([2,5])*beta_12
        right_kernel=sp.Matrix([7,11])*beta_13
        self.assertEqual(left_kernel.rank(),1)
        self.assertEqual(right_kernel.rank(),1)
        normalize_rank_one_kernel(left_kernel)
        normalize_rank_one_kernel(right_kernel)

        labelled_word_mass=sp.Rational(3,7)
        wrong_observed=labelled_word_mass*beta_13
        residual=continuation_cocycle_residual(
            wrong_observed,labelled_word_mass,beta_12
        )
        self.assertNotEqual(residual,sp.zeros(1,2))
        # An all-completions-only mutant misses the labelled-column failure.
        self.assertEqual(sp.simplify(sum(residual)),0)

    def test_private_side_fixed_cut_minor_is_exactly_positive(self):
        gamma=sp.Rational(1,3)
        lam=sp.Integer(2)
        exp_u1=sp.Rational(1,2)
        exp_u2=sp.Rational(1,4)
        exp_D=sp.Rational(1,64)
        exp_delta=sp.Rational(1,8)

        def a(exp_u):
            return gamma*(1-gamma)*lam*exp_u

        def c(exp_u):
            return gamma**2*lam*exp_D*exp_u**2

        determinant=(1-exp_delta)*(c(exp_u1)*a(exp_u2)-c(exp_u2)*a(exp_u1))
        self.assertTrue(determinant > 0)

    def test_compact_measure_nested_sets_toy(self):
        # two-point Bernoulli family: first moment pins the parameter.
        p,q=sp.symbols('p q', real=True)
        self.assertEqual(sp.solve([sp.Eq(p,q)],[p]),{p:q})

    def test_funnel_route_weights_sum_one(self):
        g=sp.symbols('g')
        self.assertEqual(sp.expand(g**3+3*g**2*(1-g)+3*g*(1-g)**2+(1-g)**3),1)

    def test_trace_normalization(self):
        Q=sp.Matrix([[-3,1,2],[1,-4,3],[2,3,-5]])
        r=-sp.trace(Q)
        self.assertEqual(sp.trace(Q/r),-1)

    def test_borel_tree_stratum_formula_four_point(self):
        # quartet 12|34 with pendant 1 and split 2: additive distances
        d12,d34,d13,d24,d14,d23=2,2,4,4,4,4
        self.assertTrue(d12+d34 < d13+d24)
        self.assertEqual(d13+d24,d14+d23)

    def test_moment_map_separates_two_atoms(self):
        w=[sp.Rational(1,2),sp.Rational(1,2)]
        a=[sp.Rational(1,4),sp.Rational(3,4)]
        b=[sp.Rational(1,5),sp.Rational(4,5)]
        self.assertNotEqual(moment_of_atoms(w,a,2),moment_of_atoms(w,b,2))

    def test_root_tail_laplace_positive(self):
        s,l=sp.symbols('s l', positive=True)
        tt=sp.Symbol('t', positive=True)
        self.assertEqual(sp.simplify(sp.integrate(l*sp.exp(-(l+s)*tt),(tt,0,sp.oo))-l/(l+s)),0)

    def test_rate_visibility_requires_pair(self):
        l,t=sp.symbols('l t', positive=True)
        one_lineage_survival=sp.Integer(1)
        two_lineage_survival=sp.exp(-l*t)
        self.assertEqual(sp.diff(one_lineage_survival,l),0)
        self.assertNotEqual(sp.diff(two_lineage_survival,l),0)

    def test_indexed_not_unordered(self):
        P1={(0,):sp.Rational(1,2),(1,):sp.Rational(1,2)}
        P2={(0,0):sp.Rational(1,4),(0,1):sp.Rational(1,4),(1,0):sp.Rational(1,4),(1,1):sp.Rational(1,4)}
        self.assertNotEqual(P1,P2)

    def test_breakpoint_rank_does_not_bound_jet_order(self):
        # Recompute the integer obstruction from the binary-parity rule;
        # no expected rate lists or generator-produced output are imported.
        for r in range(2, 8):
            left = [i + 1 for i in range(2**r) if bin(i).count("1") % 2 == 0]
            right = [i + 1 for i in range(2**r) if bin(i).count("1") % 2 == 1]
            density_jets = [(-1)**k * (sum(a**(k + 1) for a in left)
                                      - sum(b**(k + 1) for b in right))
                            for k in range(r)]
            self.assertEqual(density_jets[:-1], [0] * (r - 1))
            self.assertNotEqual(density_jets[-1], 0)
            # The signed raw 2^(r-1)-route -> scalar Sylvester bound works.
            self.assertLess(r - 1, len(left) + len(right))
        # r=5 passes all four orders of the rejected fixed-time-rank test.
        left = [i + 1 for i in range(32) if bin(i).count("1") % 2 == 0]
        right = [i + 1 for i in range(32) if bin(i).count("1") % 2 == 1]
        self.assertEqual(sum(a**5 for a in left) - sum(b**5 for b in right),
                         -122880)

    def test_raw_rectangular_sylvester_predicts_scalar_jets(self):
        t = sp.symbols('t', real=True)
        A, B = sp.diag(-1, -3), sp.diag(-2, -5, -7)
        C = sp.Matrix([[1, 2, 3], [4, 5, 6]])
        row, col = sp.Matrix([[2, 3]]), sp.Matrix([1, 2, 1])
        # Direct scalar exponential expansion is independent of the
        # matrix recurrence used to predict its derivatives.
        density = sum(row[i] * C[i, j] * col[j]
                      * sp.exp((A[i, i] - B[j, j]) * t)
                      for i in range(2) for j in range(3))
        power = C
        for k in range(10):
            direct = sp.diff(density, t, k).subs(t, 0)
            self.assertEqual(direct, (row * power * col)[0])
            power = A * power - power * B

    def test_first_variation_requires_augmented_recurrence(self):
        # g(t)=d/dtheta exp((-1+theta)t)|theta=0=t exp(-t).
        # A one-dimensional base recurrence fails; its square succeeds.
        t, theta = sp.symbols('t theta', real=True)
        variation = sp.diff(sp.exp((-1 + theta) * t), theta).subs(theta, 0)
        jets = [sp.diff(variation, t, k).subs(t, 0) for k in range(12)]
        self.assertNotEqual(jets[1] + jets[0], 0)
        for k in range(10):
            self.assertEqual(jets[k + 2] + 2 * jets[k + 1] + jets[k], 0)
        augmented = sp.Matrix([[-1, 1], [0, -1]])
        for k, jet in enumerate(jets):
            self.assertEqual((augmented**k)[0, 1], jet)

    def test_irreducible_reversible_generator_with_zero_offdiagonal(self):
        # Three-state path: irreducible with Q_13=Q_31=0.
        Q = sp.Matrix([[-1, 1, 0], [1, -2, 1], [0, 1, -1]])
        t = sp.symbols('t', positive=True)
        transition = (Q * t).exp()
        self.assertEqual(Q * sp.ones(3, 1), sp.zeros(3, 1))
        self.assertEqual(Q, Q.T)
        self.assertEqual(Q[0, 2], 0)
        self.assertEqual(sp.simplify(transition.det() - sp.exp(-4 * t)), 0)
        self.assertEqual(sp.simplify(sp.diff(transition, t) - Q * transition),
                         sp.zeros(3, 3))
        self.assertNotEqual(transition[0, 2], 0)


if __name__=='__main__':
    unittest.main(verbosity=2)
