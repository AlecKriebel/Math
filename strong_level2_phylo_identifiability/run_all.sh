#!/bin/sh
set -eu

./run_milestone1.sh
PYTHONPATH=src python3 src/verify_generator_atlas.py
PYTHONPATH=src .venv/bin/python src/verify_jc_four_network_class.py
PYTHONPATH=src python3 src/verify_jc_four_network_class_stdlib.py
PYTHONPATH=src .venv/bin/python src/verify_jc_psi_move.py
PYTHONPATH=src .venv/bin/python src/verify_jc_psi_lifting.py
PYTHONPATH=src python3 src/verify_jc_psi_lifting_stdlib.py
PYTHONPATH=src .venv/bin/python src/verify_jc_omega_move.py
PYTHONPATH=src python3 src/verify_jc_omega_move_stdlib.py
PYTHONPATH=src .venv/bin/python src/verify_jc_root_spanning_atlas.py
PYTHONPATH=src .venv/bin/python src/verify_jc_incoming_port_atlas.py
PYTHONPATH=src .venv/bin/python src/verify_jc_boundary_containments.py
PYTHONPATH=src .venv/bin/python src/verify_jc_cross_root_separation.py
PYTHONPATH=src .venv/bin/python src/verify_jc_three_outgoing_nonroot_atlas.py
PYTHONPATH=src python3 src/verify_theta_support_reduction.py
PYTHONPATH=src .venv/bin/python src/verify_jc_support_augmented_atlas.py
PYTHONPATH=src .venv/bin/python src/verify_jc_fully_labelled_support_atlas.py
PYTHONPATH=src .venv/bin/python src/verify_jc_cross_support_weak_atlas.py
PYTHONPATH=src .venv/bin/python src/verify_jc_cycle_cross_generator_atlas.py
PYTHONPATH=src .venv/bin/python src/verify_jc_cut_split_reconstruction.py
PYTHONPATH=src .venv/bin/python src/verify_jc_root_two_port_collapse.py
PYTHONPATH=src .venv/bin/python src/verify_group_based_root_two_port_collapse.py
PYTHONPATH=src .venv/bin/python src/verify_jc_root_three_port_saturation.py
PYTHONPATH=src .venv/bin/python src/verify_jc_root_three_port_tree_separation.py
PYTHONPATH=src .venv/bin/python src/verify_jc_root_four_port_cycle_theta_atlas.py
PYTHONPATH=src .venv/bin/python src/verify_jc_omega_chain.py
PYTHONPATH=src .venv/bin/python src/verify_omega_model_hierarchy.py
PYTHONPATH=src .venv/bin/python src/verify_jc_root_support_deck.py
PYTHONPATH=src .venv/bin/python src/verify_jc_projective_cut_locality.py
