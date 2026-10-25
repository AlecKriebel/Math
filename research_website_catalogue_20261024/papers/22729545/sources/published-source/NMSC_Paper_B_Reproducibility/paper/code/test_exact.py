from __future__ import annotations

import json
import copy
from fractions import Fraction
from pathlib import Path
import unittest

import sympy as sp

from nmsc_l2_exact import (
    CORE_REATTACH_SIGNATURES,
    OLD_PRINCIPAL_QUOTIENT_MOVES,
    REPAIRED_PRINCIPAL_QUOTIENT_MOVES,
    FanContinuationResponse,
    UnaryRoutingFan,
    anchored_route_separator_matrix,
    anchored_tagged_merger_masses,
    attachment_certificate_summary, biunary_kernel,
    biunary_kernel_from_route_enumeration,
    biunary_rate_word_chamber_density,
    biunary_rate_word_kernel,
    behaviorally_realizable_unary_fans,
    bridge_rank_one_matrix,
    build_preexposure_unary_fan,
    build_preexposure_strong_cycle_fixture,
    build_exposure_decorated_raw_carrier,
    build_stc_rank_one_nonbridge_fixture,
    build_repaired_core,
    canonical_reattach_signature,
    canonical_reachable_observable_response,
    decorated_word_signature,
    direct_routing_weights,
    enumerate_minimal_repairs,
    enumerate_exposure_decorated_core_regression,
    enumerate_exposure_loss_certificates,
    equal_arm_routing_survival,
    exposure_loss_observable_cells,
    exposure_loss_joint_bundle_matches,
    exposure_loss_record_matches_observation,
    exact_first_hit_composed_response,
    exponential_curvature,
    extend_fan_across_actual_exposure,
    fan_slide_equivalent,
    fan_slide_quotient_signature,
    exposure_decorated_isomorphic,
    exposure_decorated_signature,
    fixed_cut_det,
    fixed_cut_expected_det,
    fixed_cut_row,
    is_rooted_binary_fixture,
    is_level_one_fixture,
    is_local_tree_child,
    is_local_strong_tree_child,
    is_safe_preexposure_unary_fan,
    kingman_pair_survival,
    load_cores,
    log_hazard_numerator,
    marginal_routing_weights,
    nested_fan_first_hit_transport,
    normalize_exposure_decorated_carrier,
    pair_moments,
    pair_survival, potential_lowest_reticulations,
    preexposure_complete_local_kernel,
    preexposure_unary_fan_certificate,
    private_side_support_start,
    q1_q7_retention_certificate,
    q1_q7_unary_fan_signature,
    rank_one_nonbridge_certificate,
    recover_two_atom_rates,
    recover_two_exponential_total_law,
    repair_is_minimal,
    repair_satisfies_domain,
    routing_weights,
    scalar_separated_fan_continuation,
    sampling_initialization,
    side_free_cycle_domain_certificate,
    staggered_balance_certificate,
    survival_semigroup_defect,
    temporal_gluing_consistent,
    terminal_rate_exposed,
    triangle_forward,
    triangle_reverse,
    validate_stored_exposure_loss_record,
)

BASE = Path(__file__).resolve().parents[1]
CORES = load_cores(BASE / 'data' / 'NMSC_TOPOLOGY_IMPORT.json')


class ObservableMinorTests(unittest.TestCase):
    def test_symbolic_fixed_cut_identity(self):
        g, l, D, d, u1, u2 = sp.symbols('g l D d u1 u2', positive=True)
        self.assertEqual(sp.simplify(fixed_cut_det(g,l,D,d,u1,u2)-fixed_cut_expected_det(g,l,D,d,u1,u2)), 0)

    def test_equal_hazard_gamma_half_positive(self):
        val = fixed_cut_det(sp.Rational(1,2), 2, 3, sp.Rational(1,5), sp.Rational(1,10), sp.Rational(1,4))
        self.assertTrue(val.is_positive)

    def test_rows_share_two_columns(self):
        r1 = fixed_cut_row(sp.Rational(2,5), 3, 2, sp.Rational(1,7), sp.Rational(1,10))
        r2 = fixed_cut_row(sp.Rational(2,5), 3, 2, sp.Rational(1,7), sp.Rational(1,5))
        self.assertEqual(r1.shape, (1,2)); self.assertEqual(r2.shape, (1,2))
        self.assertNotEqual(sp.simplify(sp.Matrix.vstack(r1,r2).det()), 0)


    def test_actual_row_wronskian_nonzero(self):
        u=sp.symbols('u', positive=True)
        row=fixed_cut_row(sp.Rational(2,5),3,2,sp.Rational(1,7),u)
        w=sp.simplify(row[0]*sp.diff(row[1],u)-row[1]*sp.diff(row[0],u))
        self.assertNotEqual(w,0)
        self.assertTrue(w.subs(u,sp.Rational(1,5)).is_positive)

    def test_nearby_row_minor_has_wronskian_derivative(self):
        u,e=sp.symbols('u e', positive=True)
        r0=fixed_cut_row(sp.Rational(2,5),3,2,sp.Rational(1,7),u)
        re=fixed_cut_row(sp.Rational(2,5),3,2,sp.Rational(1,7),u+e)
        det=sp.Matrix.vstack(r0,re).det()
        derivative=sp.simplify(sp.diff(det,e).subs(e,0))
        w=sp.simplify(r0[0]*sp.diff(r0[1],u)-r0[1]*sp.diff(r0[0],u))
        self.assertEqual(sp.simplify(derivative-w),0)

    def test_genuine_bridge_outer_product_rank_one(self):
        m = bridge_rank_one_matrix([Fraction(2,3), Fraction(5,7)], [Fraction(3,5), Fraction(4,9)])
        self.assertEqual(m.det(), 0)
        self.assertEqual(m.rank(), 1)

    def test_nonbridge_actual_rank_two(self):
        m = sp.Matrix.vstack(
            fixed_cut_row(sp.Rational(1,3),2,2,sp.Rational(1,4),sp.Rational(1,10)),
            fixed_cut_row(sp.Rational(1,3),2,2,sp.Rational(1,4),sp.Rational(3,10)),
        )
        self.assertEqual(m.rank(), 2)


class RoutingTests(unittest.TestCase):
    def test_weights_sum_one_m1_to_m4(self):
        g=Fraction(2,5)
        for m in range(1,5):
            with self.subTest(m=m):
                self.assertEqual(sum(routing_weights(m,g).values()), 1)

    def test_marginal_identity_all_subsets_m4(self):
        g=Fraction(3,7)
        for selected in [(0,), (2,), (0,1), (1,3), (0,2,3), (0,1,2,3)]:
            with self.subTest(selected=selected):
                self.assertEqual(marginal_routing_weights(4,selected,g), direct_routing_weights(len(selected),g))

    def test_mixed_assignments_positive_gamma_half(self):
        w=routing_weights(4,Fraction(1,2))
        self.assertTrue(all(v>0 for v in w.values()))
        self.assertEqual(len(w),16)

    def test_deleted_assignments_sum_out(self):
        self.assertEqual(marginal_routing_weights(3,(0,2),Fraction(1,4)), direct_routing_weights(2,Fraction(1,4)))

    def test_pair_survival_at_zero(self):
        u=sp.symbols('u')
        self.assertEqual(sp.simplify(pair_survival(sp.Rational(2,5),2,5,u).subs(u,0)),1)

    def test_two_atom_prony_exact(self):
        m=pair_moments(Fraction(1,3),Fraction(2),Fraction(5),4)
        self.assertEqual(recover_two_atom_rates(m),(Fraction(2),Fraction(5)))

    def test_equal_rate_pair_coefficient_identifies_gamma_pair(self):
        g=Fraction(2,7)
        c=g*g+(1-g)*(1-g)
        self.assertEqual(1-c,2*g*(1-g))

    def test_early_coalescence_marginal_still_bernoulli(self):
        # Any factor depending only on selected assignment survives summing deleted assignments.
        g=Fraction(2,5); full=routing_weights(3,g)
        factor={(0,):Fraction(3,7),(1,):Fraction(5,11)}
        lhs={}
        for bits,w in full.items():
            key=(bits[0],)
            lhs[key]=lhs.get(key,Fraction(0))+w*factor[key]
        rhs={k:v*factor[k] for k,v in direct_routing_weights(1,g).items()}
        self.assertEqual(lhs,rhs)


class TriangleTests(unittest.TestCase):
    def test_biunary_closed_form_matches_route_enumeration(self):
        closed = biunary_kernel(sp.Rational(2,5), 3, 4)
        enumerated = biunary_kernel_from_route_enumeration(sp.Rational(2,5), 3, 4)
        self.assertEqual(closed, enumerated)
        self.assertEqual(closed[0, 0] + closed[0, 1], 1)

    def test_biunary_piecewise_rate_word_contains_constant_case(self):
        gamma = sp.Rational(2, 5)
        self.assertEqual(
            biunary_rate_word_kernel(gamma, ((4, 3),)),
            biunary_kernel(gamma, 3, 4),
        )

    def test_biunary_piecewise_rate_word_density_integrates_to_kernel(self):
        gamma = sp.Rational(3, 7)
        word = ((sp.Rational(2, 5), 3), (sp.Rational(4, 9), 5))
        u = sp.symbols("u", nonnegative=True)
        merger_mass = sum(
            sp.integrate(
                biunary_rate_word_chamber_density(gamma, word, index, u),
                (u, 0, duration),
            )
            for index, (duration, _) in enumerate(word)
        )
        kernel = biunary_rate_word_kernel(gamma, word)
        self.assertEqual(sp.simplify(merger_mass - kernel[0, 1]), 0)
        self.assertEqual(sp.simplify(kernel[0, 0] + kernel[0, 1]), 1)

    def test_biunary_transfer_retains_rate_word_order_not_only_total_hazard(self):
        gamma = sp.Rational(3, 7)
        forward = ((1, 2), (1, 5))
        reversed_word = ((1, 5), (1, 2))
        self.assertEqual(
            biunary_rate_word_kernel(gamma, forward),
            biunary_rate_word_kernel(gamma, reversed_word),
        )
        self.assertNotEqual(
            biunary_rate_word_chamber_density(
                gamma, forward, 0, sp.Rational(1, 2)
            ),
            biunary_rate_word_chamber_density(
                gamma, reversed_word, 0, sp.Rational(1, 2)
            ),
        )

    def test_pair_exposed_not_single_exponential(self):
        u=sp.symbols('u', real=True)
        f=triangle_forward(sp.Rational(2,5),3,2,u)
        curv=sp.simplify(exponential_curvature(f,u))
        self.assertTrue(curv.subs(u,sp.Rational(1,7)).is_positive)

    def test_reverse_is_single_exponential(self):
        u=sp.symbols('u', real=True)
        g=triangle_reverse(sp.Rational(2,5),3,2,u)
        self.assertEqual(sp.simplify(exponential_curvature(g,u)),0)

    def test_gamma_half_pair_exposed(self):
        u=sp.symbols('u', real=True)
        f=triangle_forward(sp.Rational(1,2),2,1,u)
        self.assertNotEqual(sp.simplify(exponential_curvature(f,u)),0)


class PreExposureUnaryFanTests(unittest.TestCase):
    def setUp(self):
        self.certificate = preexposure_unary_fan_certificate(
            Fraction(1), Fraction(2)
        )

    def test_fixture_is_strict_binary_rooted_tree_child_strong_and_level_one(self):
        for graph in (
            self.certificate['left_graph'],
            self.certificate['right_graph'],
        ):
            with self.subTest(h=graph.nodes['X']['time']):
                self.assertTrue(is_rooted_binary_fixture(graph, root='R'))
                self.assertTrue(is_local_tree_child(graph))
                self.assertTrue(is_local_strong_tree_child(graph, source=None))
                self.assertTrue(is_level_one_fixture(graph))
                self.assertEqual(
                    [node for node, data in graph.nodes(data=True)
                     if data.get('role') == 'retic'],
                    ['X'],
                )

    def test_distinct_h_and_unary_rate_words_have_identical_complete_local_kernels(self):
        cert = self.certificate
        self.assertNotEqual(
            cert['left_graph'].nodes['X']['time'],
            cert['right_graph'].nodes['X']['time'],
        )
        self.assertNotEqual(
            cert['left_fan'].internal_unary_rates,
            cert['right_fan'].internal_unary_rates,
        )
        self.assertTrue(cert['complete_local_kernel_equal'])
        self.assertEqual(cert['left_kernel'], cert['right_kernel'])

    def test_private_side_density_support_starts_at_anchor_entry_not_h(self):
        fan = self.certificate['left_fan']
        kernel = self.certificate['left_kernel']
        u = sp.Symbol('u', positive=True)
        self.assertEqual(private_side_support_start(fan), Fraction(3))
        self.assertNotEqual(private_side_support_start(fan), fan.reticulation_time)
        self.assertEqual(
            kernel['marked_xz_density'],
            sp.Rational(2, 3) * sp.exp(-2 * u),
        )
        self.assertEqual(kernel['density_elapsed_support'], (Fraction(0), Fraction(2)))

    def test_complete_kernel_has_exact_survival_merge_and_arbitrary_continuation(self):
        left = self.certificate['left_kernel']
        right = self.certificate['right_kernel']
        expected = sp.Matrix([
            [sp.Rational(2, 3) + sp.exp(-4) / 3,
             sp.Rational(1, 3) * (1 - sp.exp(-4))],
            [0, 1],
        ])
        self.assertEqual(
            (left['state_kernel'] - expected).applyfunc(sp.simplify),
            sp.zeros(2),
        )
        self.assertEqual(sp.simplify(left['no_merger_to_S'] - expected[0, 0]), 0)
        self.assertEqual(sp.simplify(left['merged_before_S'] - expected[0, 1]), 0)
        self.assertEqual(
            left['arbitrary_upper_continuation'],
            right['arbitrary_upper_continuation'],
        )

    def test_old_q1_through_q7_retain_h_and_do_not_encode_collision(self):
        cert = self.certificate
        self.assertEqual(len(OLD_PRINCIPAL_QUOTIENT_MOVES), 7)
        self.assertFalse(cert['old_q1_q7_equal'])
        self.assertNotEqual(
            q1_q7_unary_fan_signature(cert['left_fan']),
            q1_q7_unary_fan_signature(cert['right_fan']),
        )
        for side in ('left_q1_q7', 'right_q1_q7'):
            retained = cert[side]
            self.assertEqual(tuple(move for move, _ in retained['retained_time_by_move']),
                             OLD_PRINCIPAL_QUOTIENT_MOVES)
            self.assertTrue(all(
                time == retained['retained_reticulation_time']
                for _, time in retained['retained_time_by_move']
            ))
            self.assertFalse(retained['whole_fan_is_two_terminal_corridor'])
            self.assertFalse(retained['single_upper_extension_is_safe'])

    def test_q8_forgets_only_h_and_internal_unary_words(self):
        cert = self.certificate
        self.assertEqual(len(REPAIRED_PRINCIPAL_QUOTIENT_MOVES), 8)
        self.assertTrue(cert['q8_fan_slide_equal'])
        self.assertTrue(fan_slide_equivalent(
            cert['left_fan'],
            cert['right_fan'],
            cert['left_continuation'],
            cert['right_continuation'],
        ))
        self.assertEqual(
            fan_slide_quotient_signature(cert['left_fan'], cert['left_continuation']),
            fan_slide_quotient_signature(cert['right_fan'], cert['right_continuation']),
        )

    def test_q8_preserves_route_dependent_typed_temporal_stopping_ports(self):
        fan = self.certificate['left_fan']
        continuation = scalar_separated_fan_continuation(fan)
        signature = fan_slide_quotient_signature(fan, continuation)
        self.assertEqual(signature[1], ('x', Fraction(0), 'one-block'))
        self.assertEqual(signature[2], (
            ('T', Fraction(3), 'first-exposure'),
            ('S', Fraction(5), 'first-exposure'),
        ))
        self.assertNotEqual(signature[2][0][1], signature[2][1][1])
        self.assertEqual(signature[3], (
            ('S@5:first-exposure', Fraction(2, 3)),
            ('T@3:first-exposure', Fraction(1, 3)),
        ))

    def test_q8_does_not_identify_changed_probability_or_frontier(self):
        rates = {'X-x': Fraction(5), 'T-X': Fraction(7), 'S-X': Fraction(11)}
        base = self.certificate['left_fan']
        changed_gamma = build_preexposure_unary_fan(
            Fraction(2), Fraction(2, 5), Fraction(3), Fraction(5), rates
        )
        changed_frontier = build_preexposure_unary_fan(
            Fraction(2), Fraction(1, 3), Fraction(4), Fraction(6), rates
        )
        self.assertFalse(fan_slide_equivalent(
            base,
            changed_gamma,
            scalar_separated_fan_continuation(base),
            scalar_separated_fan_continuation(changed_gamma),
        ))
        self.assertFalse(fan_slide_equivalent(
            base,
            changed_frontier,
            scalar_separated_fan_continuation(base),
            scalar_separated_fan_continuation(changed_frontier),
        ))

    def test_q8_uses_composed_response_not_raw_exit_weights(self):
        rates = {'X-x': Fraction(5), 'T-X': Fraction(7), 'S-X': Fraction(11)}
        left = self.certificate['left_fan']
        different_weights = build_preexposure_unary_fan(
            Fraction(2), Fraction(2, 5), Fraction(3), Fraction(5), rates
        )
        future_null = FanContinuationResponse(
            ('common-future', 'null-future'),
            (
                ('T', (Fraction(1), Fraction(0))),
                ('S', (Fraction(1), Fraction(0))),
            ),
        )
        self.assertNotEqual(
            tuple(port[3] for port in left.first_exposure_ports),
            tuple(port[3] for port in different_weights.first_exposure_ports),
        )
        self.assertEqual(
            canonical_reachable_observable_response(left, future_null),
            (('common-future', Fraction(1)),),
        )
        self.assertTrue(fan_slide_equivalent(
            left, different_weights, future_null, future_null
        ))

    def test_same_raw_weights_with_different_typed_continuation_are_not_equivalent(self):
        fan = self.certificate['left_fan']
        same_weights = self.certificate['right_fan']
        response_a = FanContinuationResponse(
            ('future-A',),
            (('T', (Fraction(1),)), ('S', (Fraction(1),))),
        )
        response_b = FanContinuationResponse(
            ('future-B',),
            (('T', (Fraction(1),)), ('S', (Fraction(1),))),
        )
        self.assertEqual(
            tuple(port[3] for port in fan.first_exposure_ports),
            tuple(port[3] for port in same_weights.first_exposure_ports),
        )
        self.assertFalse(fan_slide_equivalent(
            fan, same_weights, response_a, response_b
        ))

    def test_maximal_nested_fan_first_hit_composition_is_order_independent(self):
        outer = (sp.Rational(1, 3), sp.Rational(2, 3))
        inner = (sp.Rational(1, 4), sp.Rational(3, 4))
        flattened = nested_fan_first_hit_transport(outer, inner)
        self.assertEqual(
            flattened,
            (sp.Rational(1, 12), sp.Rational(1, 4), sp.Rational(2, 3)),
        )
        transition = sp.Matrix([
            [inner[0], inner[1], 0],
            [0, 0, 1],
        ])
        continuation = sp.Matrix([
            [1, 0],
            [0, 1],
            [1, 1],
        ])
        output_types = ('marked-A', 'marked-B')
        outer_then_inner = exact_first_hit_composed_response(
            outer, (transition,), continuation, output_types
        )
        flattened_once = exact_first_hit_composed_response(
            flattened, (), continuation, output_types
        )
        inner_then_outer = exact_first_hit_composed_response(
            outer, (), transition * continuation, output_types
        )
        self.assertEqual(outer_then_inner, flattened_once)
        self.assertEqual(flattened_once, inner_then_outer)

    def test_q8_rejects_extension_across_actual_two_block_exposure(self):
        extended = extend_fan_across_actual_exposure(self.certificate['left_fan'])
        self.assertEqual(extended.maximum_internal_occupancy, 2)
        self.assertEqual(extended.internal_sample_entries,
                         (('z', 'T', Fraction(3)),))
        self.assertFalse(is_safe_preexposure_unary_fan(extended))
        with self.assertRaises(ValueError):
            fan_slide_quotient_signature(
                extended,
                scalar_separated_fan_continuation(extended),
            )

    def test_q8_rejects_two_block_occupancy_even_without_side_entry_metadata(self):
        fan = self.certificate['left_fan']
        exposed = UnaryRoutingFan(
            fan.lower_boundary,
            fan.reticulation_time,
            fan.first_exposure_ports,
            fan.internal_unary_rates,
            2,
            (),
        )
        self.assertFalse(is_safe_preexposure_unary_fan(exposed))

    def test_q8_rejects_internal_sample_entry_even_with_unary_occupancy_flag(self):
        fan = self.certificate['left_fan']
        side_entry = UnaryRoutingFan(
            fan.lower_boundary,
            fan.reticulation_time,
            fan.first_exposure_ports,
            fan.internal_unary_rates,
            1,
            (('z', 'T', Fraction(3)),),
        )
        self.assertFalse(is_safe_preexposure_unary_fan(side_entry))

    def test_invalid_slide_past_first_exposure_is_rejected(self):
        rates = {'X-x': Fraction(5), 'T-X': Fraction(7), 'S-X': Fraction(11)}
        with self.assertRaises(ValueError):
            build_preexposure_unary_fan(
                Fraction(3), Fraction(1, 3), Fraction(3), Fraction(5), rates
            )


class CoreCatalogTests(unittest.TestCase):
    def test_five_cores(self):
        self.assertEqual(set(CORES),{'cycle','theta0','theta1','theta2','theta3'})

    def test_twelve_repairs(self):
        self.assertEqual(sum(len(c.repairs) for c in CORES.values()),12)

    def test_every_repair_tree_child(self):
        for c in CORES.values():
            for repair in c.repairs:
                with self.subTest(core=c.name,repair=repair):
                    self.assertTrue(is_local_tree_child(build_repaired_core(c,repair)))

    def test_every_repair_satisfies_strong_local_criterion(self):
        for c in CORES.values():
            for repair in c.repairs:
                with self.subTest(core=c.name,repair=repair):
                    self.assertTrue(is_local_strong_tree_child(build_repaired_core(c,repair)))

    def test_every_repair_minimal(self):
        for c in CORES.values():
            for repair in c.repairs:
                with self.subTest(core=c.name,repair=repair):
                    self.assertTrue(repair_is_minimal(c,repair))

    def test_primitive_enumeration_recovers_exact_five_core_twelve_repair_catalog(self):
        derived = {
            name: enumerate_minimal_repairs(core)
            for name, core in CORES.items()
        }
        supplied = {name: core.repairs for name, core in CORES.items()}
        self.assertEqual(derived, supplied)
        self.assertEqual(sum(map(len, derived.values())), 12)

    def test_domain_requires_both_tree_child_and_strong_tail(self):
        core = CORES['theta0']
        graph = build_repaired_core(core, (2,))
        self.assertFalse(is_local_tree_child(graph))
        self.assertTrue(is_local_strong_tree_child(graph))
        self.assertFalse(repair_satisfies_domain(core, (2,)))

    def test_core_retic_counts(self):
        self.assertEqual(len(CORES['cycle'].retics),1)
        for name in ['theta0','theta1','theta2','theta3']:
            self.assertEqual(len(CORES[name].retics),2)

    def test_suppressed_parallel_segments_are_repaired(self):
        # cycle and theta1 have parallel topological arcs; every minimum repair subdivides at least one relevant arc.
        self.assertTrue(all(len(r)>=1 for r in CORES['cycle'].repairs))
        self.assertTrue(all(any(i in r for i in (3,4)) for r in CORES['theta1'].repairs))

    def test_reattachment_table_matches_all_repairs(self):
        rows=json.loads((BASE/'data'/'CORE_REATTACHMENT_TABLE.json').read_text())['rows']
        table={(r['core'],tuple(r['repair'])) for r in rows}
        catalog={(c.name,tuple(rep)) for c in CORES.values() for rep in c.repairs}
        self.assertEqual(table,catalog)

    def test_every_table_row_has_two_certificates(self):
        rows=json.loads((BASE/'data'/'CORE_REATTACHMENT_TABLE.json').read_text())['rows']
        self.assertTrue(all(len(r['parent_certificates'])==2 and r['child'] for r in rows))

    def test_every_potential_lowest_reticulation_has_child_and_side_support(self):
        for c in CORES.values():
            for repair in c.repairs:
                g=build_repaired_core(c,repair)
                for h in potential_lowest_reticulations(g):
                    rec=attachment_certificate_summary(g,h)
                    with self.subTest(core=c.name,repair=repair,h=h):
                        self.assertTrue(rec['child_leaves'])
                        self.assertEqual(len(rec['parents']),2)
                        # Strong repair supplies at least one sampled side certificate;
                        # the complementary parent is handled by private, nested, sibling, or split data.
                        self.assertTrue(any(rec['side_leaves'][p] for p in rec['parents']))


class ExposureDecoratedCoreRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = enumerate_exposure_decorated_core_regression(CORES)

    def test_behavior_derived_joint_catalog_and_homogeneous_labels(self):
        certificate = self.certificate
        self.assertEqual(certificate['repair_count'], 12)
        self.assertEqual(certificate['fixed_sample_count'], 6)
        self.assertEqual(certificate['structural_realizable_cone_count'], 18)
        self.assertEqual(certificate['joint_configuration_count'], 36)
        self.assertEqual(certificate['per_core_joint_configuration_counts'], {
            'cycle': 4, 'theta0': 4, 'theta1': 4, 'theta2': 16, 'theta3': 8,
        })
        self.assertEqual(certificate['simultaneous_both_hidden_configuration_count'], 6)
        self.assertEqual(certificate['fixed_label_configuration_count'], 36)
        self.assertEqual(certificate['raw_joint_carrier_count'], 72)
        self.assertEqual(len(certificate['rows']), 72)
        self.assertNotIn('exposure_mask_count', certificate)
        self.assertNotIn('fan_component_count', certificate)
        self.assertIn('fixed-(X,S,s)', certificate['coverage_scope'])
        self.assertEqual(certificate['relative_label_orbit_audit']['symmetric_group_order'], 720)
        self.assertEqual(
            certificate['relative_label_orbit_audit']['relative_label_placement_count'],
            36 * 720,
        )
        self.assertEqual(certificate['relative_label_orbit_audit']['failures'], ())
        self.assertEqual(
            certificate['normalizer_label_generator_audit']['adjacent_generator_count'],
            5,
        )
        self.assertEqual(
            certificate['normalizer_label_generator_audit']['generated_group_order'],
            720,
        )
        self.assertEqual(
            certificate['normalizer_label_generator_audit']['audit_count'],
            36 * 5,
        )
        self.assertEqual(certificate['normalizer_label_generator_audit']['failures'], ())
        for row in certificate['rows']:
            labels = sorted(dict(row['sample_attachment']).values())
            self.assertEqual(labels, [f'sample-{index}' for index in range(6)])
            self.assertNotIn('companion-sample', repr(row['sample_attachment']))

    def test_higher_theta0_and_theta1_retics_are_not_free_hidden_masks(self):
        for core_name in ('theta0', 'theta1'):
            core = CORES[core_name]
            for repair in core.repairs:
                graph = build_repaired_core(core, repair)
                accepted, rejected = behaviorally_realizable_unary_fans(graph)
                self.assertEqual(len(accepted), 1)
                self.assertEqual(accepted[0]['reticulation'], 'X')
                self.assertTrue(any(
                    record['reticulation'] == 'V'
                    and record['reason'] == 'lower-reticulation-before-candidate'
                    for record in rejected
                ))

    def test_routes_stop_before_second_routing_event_and_joint_fans_are_disjoint(self):
        certificate = self.certificate
        self.assertEqual(certificate['critical_route_rejections'], ())
        self.assertEqual(certificate['potential_counterexamples'], ())
        self.assertEqual(certificate['joint_compatibility_rejections'], ())
        self.assertEqual(certificate['maximum_simultaneous_hidden_fans'], 2)
        self.assertEqual(certificate['maximum_hidden_reticulations_per_fan'], 1)
        self.assertEqual(certificate['maximum_typed_outlets_per_fan'], 2)
        self.assertEqual(certificate['maximum_weight_separating_anchors_per_fan'], 1)
        self.assertEqual(certificate['maximum_typed_first_outlet_anchors_per_fan'], 2)
        self.assertEqual(certificate['maximum_future_null_dimension'], 0)

    def test_actual_immediate_delayed_topologies_collapse_only_casewise(self):
        by_case = {}
        for row in self.certificate['rows']:
            key = (
                row['core'], row['repair'], row['sample_attachment'],
                row['hidden_focal_samples'],
            )
            by_case.setdefault(key, []).append(row)
        self.assertEqual(len(by_case), self.certificate['fixed_label_configuration_count'])
        for rows in by_case.values():
            hidden_count = rows[0]['derived_hidden_count']
            self.assertEqual(len(rows), 2 ** hidden_count)
            self.assertEqual(len({row['normalized_code'] for row in rows}), 1)
            if hidden_count:
                self.assertGreater(len({row['raw_code'] for row in rows}), 1)
                self.assertGreater(len({row['raw_node_count'] for row in rows}), 1)
        self.assertGreater(self.certificate['q8_only_collision_pair_count'], 0)

    def test_signature_collisions_equal_independently_declared_q7_q8_orbits(self):
        certificate = self.certificate
        self.assertEqual(certificate['canonical_isomorphism_failures'], ())
        self.assertEqual(certificate['unacceptable_collisions'], ())
        self.assertEqual(certificate['unclassified_quotient_collisions'], ())
        self.assertEqual(certificate['unclassified_quotient_splits'], ())
        self.assertGreater(certificate['declared_primitive_orbit_count'], 0)
        self.assertGreater(certificate['declared_core_automorphism_group_count'], 0)
        self.assertGreater(certificate['declared_q8_carrier_group_count'], 0)
        self.assertEqual(
            certificate['normalized_signature_count'],
            len({row['normalized_code'] for row in certificate['rows']}),
        )
        self.assertEqual(
            certificate['raw_orbit_count'],
            len({row['raw_code'] for row in certificate['rows']}),
        )

    def test_physical_normalization_removes_all_unary_interiors_and_keeps_global_order(self):
        for row in self.certificate['rows']:
            self.assertEqual(
                sum(
                    data.get('role') == 'macro'
                    for _, data in row['normalized_graph'].nodes(data=True)
                ),
                row['derived_hidden_count'],
            )
            self.assertFalse(any(
                data.get('role') == 'unary'
                for _, data in row['normalized_graph'].nodes(data=True)
            ))
            for payload in row['response_macro_collection']:
                self.assertEqual(tuple(field[0] for field in payload), (
                    'lower-sampled-role',
                    'route-wise-first-positive-exposure-frontier',
                    'continuation-column-classes',
                    'composite-route-polynomial',
                ))
                self.assertIn('global-retained-strict-order', repr(payload))
                self.assertIn('frontier-incidence', repr(payload))
            colors = repr(tuple(
                data['observable_color']
                for _, data in row['normalized_graph'].nodes(data=True)
            ))
            self.assertNotIn('segment-', colors)
            self.assertNotIn('internal-name', colors)
            self.assertNotIn('exact-time', colors)
            self.assertNotIn("'X0'", colors)
            self.assertNotIn("'X1'", colors)

    def test_independent_primitive_record_and_full_macro_reinsertion_match(self):
        for row in self.certificate['rows']:
            self.assertEqual(row['normalized_code'], row['independent_expected_code'])
            self.assertEqual(
                row['reinserted_skeleton_code'],
                row['independent_expected_skeleton_code'],
            )
            self.assertTrue(row['expected_record_matches'])
            self.assertIsInstance(row['declared_primitive_orbit_id'], int)

    def test_q8_preserves_exact_typed_weights_and_changed_weights_separate(self):
        certificates = tuple(
            item
            for record in self.certificate['configuration_records']
            for item in record['q8_weight_certificates']
        )
        self.assertTrue(certificates)
        self.assertEqual(
            {item['gamma'] for item in certificates},
            {Fraction(1, 3), Fraction(1, 2)},
        )
        self.assertTrue(all(item['strictly_internal'] for item in certificates))
        self.assertTrue(all(
            item['actual_equals_independent_typed_response']
            for item in certificates
        ))
        self.assertTrue(all(
            item['different_nonexchange_weight_changes_response']
            for item in certificates
        ))
        self.assertTrue(all(
            item['fixed_typed_outlet_complement_changes_response']
            for item in certificates
        ))
        self.assertTrue(all(
            item['true_parent_presentation_relabel_preserves_response']
            for item in certificates
        ))
        non_symmetric = tuple(
            item for item in certificates if item['gamma'] != Fraction(1, 2)
        )
        self.assertTrue(non_symmetric)
        self.assertTrue(all(
            item['fixed_typed_outlet_complement_changes_response']
            for item in non_symmetric
        ))

    def test_every_elimination_certificate_has_positive_exclusive_interval(self):
        certificates = (
            certificate
            for record in self.certificate['configuration_records']
            for certificate in record['fan_certificates']
        )
        for certificate in certificates:
            self.assertEqual(certificate['status'], 'PASS')
            self.assertEqual(certificate['hidden_reticulation_count'], 1)
            self.assertEqual(certificate['typed_outlet_count'], 2)
            self.assertEqual(certificate['future_null_dimension'], 0)
            self.assertEqual(certificate['weight_separating_anchor_count'], 1)
            self.assertEqual(certificate['typed_first_outlet_anchor_count'], 2)
            self.assertEqual(
                certificate['typed_outlet_coverage_matrix'],
                ((1, 0), (0, 1)),
            )
            interval = certificate['exclusive_positive_length_interval']
            self.assertIsNotNone(interval)
            self.assertGreaterEqual(interval['strict_event_order_edge_count'], 1)
            self.assertEqual(
                certificate['outlet_by_cell_possibility_matrix'],
                ((1, 1), (0, 1)),
            )
            self.assertEqual(
                certificate['symbolic_determinant'],
                '1-exp(-lambda*delta)>0',
            )

    def test_theta0_two_three_types_z2_and_z3_separately(self):
        record = next(
            record for record in self.certificate['configuration_records']
            if record['core'] == 'theta0'
            and record['repair'] == (2, 3)
            and record['hidden_reticulations'] == ('X',)
        )
        certificate = record['fan_certificates'][0]
        attachment = dict(record['sample_attachment'])
        typed_labels = tuple(
            anchor[1]
            for anchor in certificate['selected_first_outlet_anchors']
        )
        self.assertEqual(set(typed_labels), {attachment['L2'], attachment['L3']})
        self.assertEqual(certificate['weight_separating_anchor_count'], 1)
        self.assertEqual(certificate['typed_first_outlet_anchor_count'], 2)
        self.assertEqual(
            certificate['typed_outlet_coverage_matrix'],
            ((1, 0), (0, 1)),
        )

    def test_exact_temporal_separation_and_both_incomparable_orders(self):
        certificate = self.certificate
        self.assertEqual(certificate['incomparable_order_case_count'], 24)
        self.assertEqual(certificate['incomparable_order_realization_count'], 48)
        for audit in certificate['incomparable_order_audits']:
            self.assertIn(audit['core'], {'theta2', 'theta3'})
            self.assertEqual(audit['variant_count'], 2)
            self.assertNotEqual(
                audit['variants'][0]['reticulation_order'],
                audit['variants'][1]['reticulation_order'],
            )
            self.assertTrue(all(
                variant['strict_temporal_separation']
                for variant in audit['variants']
            ))
        self.assertTrue(all(
            all(
                value for key, value in row['raw_validity'].items()
                if key != 'actual_unary_epoch_node_count'
            )
            for row in certificate['rows']
        ))


class ExposureLossStorageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = enumerate_exposure_loss_certificates(CORES)

    def test_exact_below_and_above_observable_cells(self):
        u = sp.symbols('u', nonnegative=True)
        p_x = sp.Rational(2, 5)
        q_v = sp.Rational(1, 3)
        p_tilde = p_x * sp.exp(-sp.Rational(7, 3))
        cells = exposure_loss_observable_cells(
            p_x, q_v, 5, sp.Rational(4, 3), p_tilde, 7, 11, u=u,
        )
        self.assertEqual(
            cells['first_merger_density'],
            p_x * 5 * sp.exp(-(sp.Rational(4, 3) + 5 * u)),
        )
        self.assertEqual(
            cells['below_survival'],
            1 - p_x + p_x * sp.exp(-(sp.Rational(4, 3) + 5 * u)),
        )
        expected_above = (
            1 - p_x
            + p_tilde * (
                2 * q_v * (1 - q_v)
                + q_v**2 * sp.exp(-7 * u)
                + (1 - q_v) ** 2 * sp.exp(-11 * u)
            )
        )
        self.assertEqual(sp.simplify(cells['above_survival'] - expected_above), 0)
        self.assertEqual(
            sp.simplify(
                cells['first_merger_density']
                + sp.diff(cells['below_survival'], u)
            ),
            0,
        )

    def test_all_four_minimum_repair_records(self):
        certificate = self.certificate
        self.assertEqual(certificate['repair_count'], 4)
        self.assertEqual(certificate['per_core_counts'], {'theta0': 2, 'theta1': 2})
        self.assertEqual(
            {(row['core'], row['repair']) for row in certificate['rows']},
            {
                ('theta0', (2, 3)), ('theta0', (3, 4)),
                ('theta1', (2, 3)), ('theta1', (2, 4)),
            },
        )
        self.assertTrue(certificate['all_zero_atom_breakpoints_positive'])
        self.assertTrue(certificate['all_total_law_prony_inversions_exact'])

    def test_unequal_equal_and_half_inheritance_boundaries(self):
        self.assertTrue(
            self.certificate['all_equal_and_q_half_boundaries_recovered']
        )
        for row in self.certificate['rows']:
            recovered = row['recovered_v_record']
            self.assertTrue(all(
                chamber['branch'] == 'unequal-rate'
                and chamber['hankel_determinant'] > 0
                for chamber in recovered['prony_chambers']
            ))
            self.assertEqual(
                tuple(
                    item['inheritance_pair']
                    for item in recovered['equal_rate_recoveries']
                ),
                (
                    (sp.Rational(1, 3), sp.Rational(2, 3)),
                    (sp.Rational(1, 2), sp.Rational(1, 2)),
                ),
            )
            self.assertTrue(all(
                item['branch'] == 'equal-rate'
                and item['hankel_determinant'] == 0
                for item in recovered['equal_rate_recoveries']
            ))

    def test_full_equal_first_chamber_and_q_half_lifts(self):
        certificate = self.certificate
        self.assertEqual(certificate['full_equal_first_chamber_count'], 8)
        self.assertEqual(certificate['full_equal_first_q_half_count'], 4)
        self.assertTrue(certificate['all_full_equal_first_chamber_records_exact'])
        self.assertEqual(
            {
                (row['core'], row['repair'])
                for row in certificate['equal_first_chamber_rows']
            },
            {
                ('theta0', (2, 3)), ('theta0', (3, 4)),
                ('theta1', (2, 3)), ('theta1', (2, 4)),
            },
        )
        for row in certificate['equal_first_chamber_rows']:
            self.assertEqual(row['first_prony_branch'], 'equal-rate')
            self.assertTrue(row['record_matches_total_observation'])
            self.assertTrue(row['independent_expected_record_match'])
            self.assertTrue(row['joint_reattachment_exact'])
            self.assertEqual(
                tuple(sorted(
                    value
                    for _, value in row['recovered_v_record'][
                        'typed_inheritance_assignment'
                    ]
                )),
                tuple(sorted(row['manifest']['q_assignment'])),
            )

    def test_swapped_physical_q_and_typed_x_corridor_weights(self):
        certificate = self.certificate
        self.assertTrue(certificate['swapped_physical_q_assignment_exact'])
        swapped = certificate['swapped_physical_q_row']
        self.assertEqual(
            swapped['manifest']['q_assignment'],
            (sp.Rational(2, 3), sp.Rational(1, 3)),
        )
        self.assertEqual(
            swapped['recovered_v_record']['typed_inheritance_assignment'],
            swapped['manifest']['typed_q_assignment'],
        )
        self.assertTrue(swapped['record_matches_total_observation'])
        self.assertTrue(swapped['independent_expected_record_match'])
        self.assertTrue(swapped['joint_reattachment_exact'])

        for row in (
            *certificate['rows'],
            *certificate['equal_first_chamber_rows'],
            swapped,
        ):
            x_weights = dict(row['stored_x_macro']['typed_weights'])
            case = row['manifest']['case']
            self.assertEqual(
                x_weights[case['x_child_outlet'][0]],
                row['manifest']['p_x'],
            )
            self.assertEqual(
                x_weights[case['x_bypass_outlet'][0]],
                1 - row['manifest']['p_x'],
            )

    def test_equal_child_epochs_are_q3_compressed(self):
        certificate = self.certificate
        self.assertEqual(certificate['equal_child_epoch_count'], 4)
        self.assertTrue(certificate['all_equal_child_epochs_q3_compressed'])
        for row in certificate['equal_child_epoch_rows']:
            child_word = row['recovered_v_record']['exposed_rate_words']['child']
            self.assertEqual(len(child_word), 1)
            self.assertEqual(child_word[0][0], sp.Rational(5, 6))
            self.assertEqual(
                len(row['recovered_v_record']['child_chamber_rates']),
                2,
            )
            self.assertTrue(row['record_matches_total_observation'])
            self.assertTrue(row['joint_reattachment_exact'])

    def test_full_child_and_parent_rate_words_are_recovered_and_stored(self):
        self.assertTrue(self.certificate['all_records_match_total_observations'])
        self.assertTrue(self.certificate['all_independent_expected_records_match'])
        for row in self.certificate['rows']:
            recovered = row['recovered_v_record']
            expected = row['expected_graph'].nodes['V']['exposed_rate_words']
            self.assertEqual(
                recovered['exposed_rate_words'],
                expected,
            )
            self.assertTrue(validate_stored_exposure_loss_record(recovered))
            self.assertTrue(row['record_matches_total_observation'])
            self.assertEqual(len(recovered['parent_incidences']), 2)

    def test_repair_side_typing_including_theta0_bypass_sibling(self):
        rows = {(row['core'], row['repair']): row for row in self.certificate['rows']}
        bypass = rows[('theta0', (2, 3))]
        self.assertEqual(bypass['typing_kind'], 'U-to-X-bypass-sibling-at-U')
        self.assertEqual(bypass['label_triple'], ('C_X', 'L3', 'L2'))
        self.assertEqual(
            rows[('theta0', (3, 4))]['typing_kind'],
            'nested-U-to-V-parent-arm',
        )
        self.assertEqual(
            rows[('theta1', (2, 3))]['label_triple'],
            ('C_X', 'L2', 'L3'),
        )
        self.assertEqual(
            rows[('theta1', (2, 4))]['label_triple'],
            ('C_X', 'L2', 'L4'),
        )
        self.assertTrue(all(
            row['independent_expected_record_match']
            for row in self.certificate['rows']
        ))

    def test_focal_restriction_turns_v_into_q8_and_keeps_anchors(self):
        self.assertTrue(self.certificate['all_restrictions_turn_v_into_q8'])
        self.assertTrue(self.certificate['all_v_exposure_witnesses_positive'])
        for row in self.certificate['rows']:
            self.assertTrue(row['v_exposed_independently_witnessed'])
            self.assertEqual(len(row['v_exposure_witness']['descendant_samples']), 2)
            self.assertGreater(row['v_exposure_witness']['positive_interval'], 0)
            self.assertTrue(row['residual_v_becomes_q8'])

    def test_joint_stored_v_then_x_reattachment_is_exact(self):
        self.assertTrue(self.certificate['all_joint_reattachments_exact'])
        for row in self.certificate['rows']:
            self.assertEqual(row['joint_reattachment_order'], (
                'restore-recovered-original-V',
                'reattach-stored-typed-X-macro',
            ))
            self.assertEqual(
                row['expected_graph'].number_of_nodes(),
                row['reconstructed_graph'].number_of_nodes(),
            )
            self.assertTrue(row['joint_reattachment_exact'])

    def test_newly_q8_residual_is_not_a_full_original_v_record(self):
        for row in self.certificate['rows']:
            incomplete = {
                'h_v': row['recovered_v_record']['h_v'],
                'inheritance_pair': row['recovered_v_record']['inheritance_pair'],
            }
            self.assertFalse(validate_stored_exposure_loss_record(incomplete))

    def test_total_law_prony_has_distinct_and_equal_rate_branches(self):
        u = sp.symbols('u', nonnegative=True)
        scale = sp.Rational(2, 7)
        total = (
            sp.Rational(3, 11)
            + scale * (
                sp.Rational(1, 9) * sp.exp(-3 * u)
                + sp.Rational(4, 9) * sp.exp(-5 * u)
            )
        )
        recovered = recover_two_exponential_total_law(total, scale, u)
        self.assertEqual(recovered['branch'], 'unequal-rate')
        self.assertEqual(recovered['components'], (
            (sp.Integer(3), sp.Rational(1, 9)),
            (sp.Integer(5), sp.Rational(4, 9)),
        ))
        self.assertGreater(recovered['hankel_determinant'], 0)
        equal = recover_two_exponential_total_law(
            sp.Rational(3, 11) + scale * sp.Rational(5, 9) * sp.exp(-7 * u),
            scale,
            u,
        )
        self.assertEqual(equal['branch'], 'equal-rate')
        self.assertEqual(equal['components'], ((sp.Integer(7), sp.Rational(5, 9)),))

    def test_every_recovered_field_is_semantically_consumed(self):
        for row in self.certificate['rows']:
            record = row['recovered_v_record']
            observation = row['observation']

            changed_h = copy.deepcopy(record)
            changed_h['h_v'] += 1
            self.assertFalse(exposure_loss_record_matches_observation(
                changed_h, observation,
            ))

            changed_q = copy.deepcopy(record)
            changed_q['inheritance_pair'] = (sp.Rational(1, 4), sp.Rational(3, 4))
            self.assertFalse(exposure_loss_record_matches_observation(
                changed_q, observation,
            ))

            changed_typed_q = copy.deepcopy(record)
            typed_q = list(changed_typed_q['typed_inheritance_assignment'])
            typed_q[0], typed_q[1] = (
                (typed_q[0][0], typed_q[1][1]),
                (typed_q[1][0], typed_q[0][1]),
            )
            changed_typed_q['typed_inheritance_assignment'] = tuple(typed_q)
            if typed_q[0][1] != typed_q[1][1]:
                self.assertFalse(exposure_loss_record_matches_observation(
                    changed_typed_q, observation,
                ))

            for word_key in ('child', 'parent_1', 'parent_2'):
                changed_word = copy.deepcopy(record)
                word = list(changed_word['exposed_rate_words'][word_key])
                word[0] = (word[0][0], word[0][1] + 1)
                changed_word['exposed_rate_words'][word_key] = tuple(word)
                self.assertFalse(exposure_loss_record_matches_observation(
                    changed_word, observation,
                ))

            for incidence_key in ('parent_incidences', 'child_incidence'):
                changed_incidence = copy.deepcopy(record)
                incidence = list(changed_incidence[incidence_key])
                incidence[0] = ('wrong-port', *incidence[0][1:])
                changed_incidence[incidence_key] = tuple(incidence)
                self.assertFalse(exposure_loss_record_matches_observation(
                    changed_incidence, observation,
                ))

            changed_x = copy.deepcopy(row['stored_x_macro'])
            incoming = list(changed_x['incoming'])
            incoming[0] = ('wrong-X-port', *incoming[0][1:])
            changed_x['incoming'] = tuple(incoming)
            self.assertFalse(exposure_loss_joint_bundle_matches(
                CORES[row['core']], row['manifest'], observation, record, changed_x,
            ))

            changed_labels = copy.deepcopy(record)
            changed_labels['repair_side_typing']['labels'] = (
                'wrong-focal', 'wrong-child', 'wrong-anchor',
            )
            self.assertFalse(exposure_loss_record_matches_observation(
                changed_labels, observation,
            ))

            changed_x_focal = copy.deepcopy(row['stored_x_macro'])
            changed_x_focal['focal'] = 'wrong-X-focal'
            self.assertFalse(exposure_loss_joint_bundle_matches(
                CORES[row['core']], row['manifest'], observation, record,
                changed_x_focal,
            ))

            changed_x_parents = copy.deepcopy(row['stored_x_macro'])
            changed_x_parents['parents'] = ('wrong-parent',)
            self.assertFalse(exposure_loss_joint_bundle_matches(
                CORES[row['core']], row['manifest'], observation, record,
                changed_x_parents,
            ))

            swapped_x = copy.deepcopy(row['stored_x_macro'])
            x_weights = list(swapped_x['typed_weights'])
            x_weights[0], x_weights[1] = (
                (x_weights[0][0], x_weights[1][1]),
                (x_weights[1][0], x_weights[0][1]),
            )
            swapped_x['typed_weights'] = tuple(x_weights)
            self.assertFalse(exposure_loss_joint_bundle_matches(
                CORES[row['core']], row['manifest'], observation, record, swapped_x,
            ))


class ReattachmentTests(unittest.TestCase):
    def test_core_signatures_unique_except_declared_sibling_roles(self):
        vals={k:canonical_reattach_signature(*k) for k in CORE_REATTACH_SIGNATURES}
        reverse={}
        for k,v in vals.items(): reverse.setdefault(v,[]).append(k)
        # Child certificates keep X0/X1 distinct; all signatures are unique in the labelled record.
        self.assertTrue(all(len(keys)==1 for keys in reverse.values()))

    def test_theta0_theta2_roles_do_not_collide(self):
        self.assertNotEqual(canonical_reattach_signature('theta0','X'),canonical_reattach_signature('theta2','X0'))

    def test_theta3_parent_roles_distinguish_lowest(self):
        self.assertNotEqual(canonical_reattach_signature('theta3','X0'),canonical_reattach_signature('theta3','X1'))

    def test_word_extension_preserves_difference(self):
        a=canonical_reattach_signature('theta0','X')
        b=canonical_reattach_signature('theta1','X')
        words={2:[('A',Fraction(1,3)),('B',Fraction(2,3))]}
        self.assertNotEqual(decorated_word_signature(a,words),decorated_word_signature(b,words))

    def test_word_order_is_temporal(self):
        sig=canonical_reattach_signature('cycle','X')
        w1={0:[('B',Fraction(2,3)),('A',Fraction(1,3))]}
        w2={0:[('A',Fraction(1,3)),('B',Fraction(2,3))]}
        self.assertEqual(decorated_word_signature(sig,w1),decorated_word_signature(sig,w2))


class SamplingAndGluingTests(unittest.TestCase):
    def test_multiple_samples_same_taxon_population(self):
        init=sampling_initialization({'a1':'A','a2':'A','b1':'B'})
        self.assertEqual(init['A'],('a1','a2'))
        self.assertEqual(set(init),{'A','B'})

    def test_terminal_rate_criterion(self):
        mp={'a1':'A','a2':'A','b1':'B'}
        self.assertTrue(terminal_rate_exposed(mp,'A'))
        self.assertFalse(terminal_rate_exposed(mp,'B'))

    def test_temporal_gluing_consistent(self):
        self.assertTrue(temporal_gluing_consistent([{'bridgeAB':Fraction(3,2)},{'bridgeAB':Fraction(3,2),'h':Fraction(1)}]))

    def test_temporal_gluing_rejects_compensation(self):
        self.assertFalse(temporal_gluing_consistent([{'bridgeAB':Fraction(3,2)},{'bridgeAB':Fraction(4,3)}]))


class AdversarialRepairRegressions(unittest.TestCase):
    def test_kingman_semigroup_and_log_hazard_are_exact(self):
        u, v, lam = sp.symbols('u v lam', positive=True)
        survival = kingman_pair_survival(lam, u)
        self.assertEqual(survival_semigroup_defect(survival, u, v), 0)
        self.assertEqual(log_hazard_numerator(survival, u), 0)

    def test_equal_arm_routing_mixture_is_not_a_kingman_semigroup(self):
        u, v, lam, gamma = sp.symbols('u v lam gamma', positive=True)
        survival = equal_arm_routing_survival(gamma, lam, u)
        split = 2 * gamma * (1 - gamma)
        same = gamma**2 + (1 - gamma)**2
        expected_defect = split * same * (1 - sp.exp(-lam*u)) * (1 - sp.exp(-lam*v))
        expected_curvature = split * same * lam**2 * sp.exp(-lam*u)
        self.assertEqual(
            sp.simplify(survival_semigroup_defect(survival, u, v) - expected_defect),
            0,
        )
        self.assertEqual(
            sp.simplify(log_hazard_numerator(survival, u) - expected_curvature),
            0,
        )

    def test_old_rank_one_bridge_predicate_has_valid_stc_false_positive(self):
        cert = rank_one_nonbridge_certificate()
        graph = cert['graph']
        self.assertTrue(is_rooted_binary_fixture(graph))
        self.assertTrue(is_local_tree_child(graph))
        self.assertTrue(is_local_strong_tree_child(graph, source=None))
        self.assertTrue(cert['no_cross_merger_strictly_before_port'])
        self.assertTrue(cert['all_old_kernels_rank_one'])
        self.assertFalse(cert['retic_arm_is_graph_bridge'])

    def test_rank_one_false_positive_is_rejected_by_local_semigroup_germ(self):
        u, v, lam = sp.symbols('u v lam', positive=True)
        routed = equal_arm_routing_survival(sp.Rational(1,2), lam, u)
        defect = survival_semigroup_defect(routed, u, v)
        self.assertEqual(
            sp.simplify(
                defect
                - sp.Rational(1,4)
                * (1-sp.exp(-lam*u))
                * (1-sp.exp(-lam*v))
            ),
            0,
        )
        self.assertNotEqual(defect, 0)

    def test_staggered_balance_switch_is_exact_and_temporally_separated(self):
        cert = staggered_balance_certificate()
        self.assertEqual(cert['weight_1'], Fraction(1,4608))
        self.assertEqual(cert['weight_2'], Fraction(1,4608))
        self.assertEqual(cert['split_mass'], Fraction(4,9))
        self.assertEqual(cert['one_block_route_mass'], 1)
        self.assertEqual(len(set(cert['events'])), 4)
        self.assertTrue(all(
            chamber['survival_difference'] == 0
            and chamber['density_difference'] == 0
            for chamber in cert['chambers']
        ))
        self.assertFalse(cert['identity_or_global_exchange'])

    def test_unrepaired_side_free_cycle_fails_both_domain_predicates(self):
        cert = side_free_cycle_domain_certificate()
        self.assertFalse(cert['tree_child'])
        self.assertFalse(cert['strong_tail'])
        self.assertFalse(cert['combined_domain'])
        self.assertEqual(cert['minimal_repairs'], ((0,), (1,)))

    def test_anchor_tag_breaks_suffix_exchange_exactly(self):
        cert = anchored_tagged_merger_masses()
        self.assertEqual(cert['suffix_a_interval_mass'], Fraction(15,128))
        self.assertEqual(cert['suffix_b_interval_mass'], Fraction(14,128))
        self.assertEqual(cert['untagged_n'], cert['untagged_prime'])
        self.assertEqual(
            cert['tagged_difference'],
            Fraction(1,4608) * Fraction(1,128) * Fraction(63,64),
        )
        self.assertNotEqual(cert['tagged_n'], cert['tagged_prime'])

    def test_anchor_suffixes_separate_all_four_two_block_route_states(self):
        matrix = anchored_route_separator_matrix()
        self.assertTrue(matrix.det().is_positive)
        self.assertEqual(matrix.rank(), 4)


if __name__=='__main__':
    unittest.main(verbosity=2)
