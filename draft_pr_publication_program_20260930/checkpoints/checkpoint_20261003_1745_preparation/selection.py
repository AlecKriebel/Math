"""Explicit proposed scope; final ROOT confirmation still required."""
FAMILIES = [
    ('audits/pr48_2961/post_push_foreign_epoch_preparation_v5', 'SOURCE_MANIFEST.json', '7d6c549ddd7a3d65a0f329e4d1e550a2b91a9c51b09fb1a7291d8e25e0920fda', 'ROOT_SOURCE_closed', 31203, 31334),
    ('audits/pr48_2961/corrective_source_adversary_v3', 'SELF_MANIFEST.json', '563dd629787b0d7012544ae0a47b7c1832896c8001c043dadf9a908e60e17d32', 'ROOT_closed_adverse_M3_not_PASS', 3854, 4081),
    ('audits/pr48_2961/corrective_source_adversary_v4', 'SELF_MANIFEST.json', '86c38790af5d66aade5b5ebc09683b78eb31871d4e42b16687c5e2721e4f4911', 'ROOT_closed_adverse_M4_not_PASS', 19625, 19768),
    ('audits/pr48_2961/corrective_source_adversary_v5', 'SELF_MANIFEST.json', '1ae1a446fcb55a8311f27700bb75ff5f2ee93a4ee491063cf404dd186944531d', 'ROOT_closed_SOURCE_review_not_actual_recovery', 39656, 40354),
    ('audits/pr57_30003354/current_preparation_family', 'SOURCE.json', 'c3ee841ff4dbab43087cac0c3eaad9f5f529acc98d90f4c5f2b8f8cd432d92cd', 'ROOT_outside_custody_record', 83631, 83877),
    ('audits/pr57_30003354/priority_audit_family', 'SELF_MANIFEST.json', '7aa4582fe5ab7b0a6b55625803f1ff6bc6fe202d8e1ae903d5166fad76e8749e', 'ROOT_closed_bounded_priority_SOURCE', 51099, 51812),
    ('audits/pr57_30003354/preprint_round1_adversary', 'SOURCE.json', '625f54bc42154de9854975b0571dd90167628e141948aac92bd0b34e3e1a1708', 'ROOT_outside_clean_first_review_adjudication', None, None),
    ('audits/pr57_30003354/preprint_round2_wholepackage_adversary', 'SOURCE.json', '623731c5ed2dc7fb91e53ca884692ced7ec322a442bc639051e1dc246fd97238', 'ROOT_outside_final_review_custody', 38221, 38458),
    ('audits/pr57_30003354/publication_package_v1', None, None, 'ROOT_final_package_ready_unpublished', None, None),
    ('audits/pr58_30002298/original_preparation_family', 'SELF_MANIFEST.json', '0e4acfd46cd15d110a420f1846a061ae21aa0b3ad771b7cb77e0dc916ff05298', 'ROOT_SOURCE_closed', 85818, 86040),
    ('audits/pr58_30002298/current_preparation_family', 'SOURCE.json', 'a463f3aa4fbf31b083c25bea1e1f28e2c0879e5533e248a836a09e7026aa116c', 'ROOT_outside_custody_record', 20782, 21000),
    ('audits/pr58_30002298/tangent_cone_geometry_adversary_family', 'SOURCE.json', '8ae2e5e61e06a7d92e1d2e1ab14274a08f9941b72e322b132ebea15d0af680e0', 'ROOT_outside_custody_record', 71790, 71794),
    ('audits/pr58_30002298/transform_cancellation_adversary_family', 'SELF_MANIFEST.json', '32be519d9443c53c04f76221e599da339210b26ffe1cc086583f1d39988bbd6f', 'ROOT_SOURCE_closed', 54422, 54425),
    ('audits/pr59_10300025/original_preparation_family', 'ROOT_MANIFEST.json', 'e3c0c68005b4ff86b933e9d42fd7d5310b1d927d8800e12516805d5cdaf06150', 'ROOT_SOURCE_closed', 8132, 8244),
    ('audits/pr59_10300025/current_preparation_family', 'ROOT_MANIFEST.json', 'adce6cf14ecfe1df3e5ed2622f67c6c4175dab0484dfbd3f7893b2f951e6e012', 'ROOT_SOURCE_closed', 35902, 36020),
    ('audits/pr59_10300025/countable_conjugacy_adversary_family', 'ROOT_MANIFEST.json', 'b5182b62259b2bfcb841e0777d524adbbf48df4f9275fa9b0984dc4547a5754e', 'ROOT_SOURCE_closed', 8353, 8464),
    ('audits/pr59_10300025/exhaustion_conjugacy_adversary_family', 'INDEX.json', 'ef1412adc29abbe37232d06f82a3ad974ce9b8e87fdac9ed0dc1dae71743401e', 'ROOT_SELF_binds_fixed_INDEX', 8576, 8717),
    ('audits/pr60_10300054/original_preparation_family', 'SOURCE.json', '3d80022cfc9436d03aa5d7874644d6f010d6d87e967d7a14539fbef4d895c3ad', 'completed_SOURCE_ROOT_custody_pending', None, None),
    ('audits/pr60_10300054/differential_form_transgression_adversary_family', 'INDEX.json', 'd3791c897e105f81f956b4258b5ba70ba1ba2bbdd00b8bc594ec1ae405d1cf95', 'completed_SOURCE_ROOT_custody_pending', None, None),
    ('audits/pr60_10300054/global_geometry_transport_adversary_family', 'INDEX.json', '7edfb6fcb271466d3a659535b1bfc207f9f8fd6a79041a2fdf5e8b2af2d35aab', 'completed_SOURCE_ROOT_custody_pending', None, None),
]
ROOT_FILES = [
    'audits/pr48_2961/install_ROOT_epoch_v5_sources.py',
    'audits/pr48_2961/author_post_push_foreign_epoch_v5.py',
    'audits/pr48_2961/execute_post_push_foreign_epoch_phase_v5.py',
    'audits/pr48_2961/run_post_push_foreign_epoch_phase_v5.py',
    'audits/pr48_2961/inspect_complete_actual_post_epoch_v5.py',
    'audits/pr48_2961/ROOT_POST_EPOCH_V5_INSPECTION_PRELAUNCH_SOURCE.py',
    'audits/pr48_2961/capture_root_command.py',
    'audits/pr57_30003354/ROOT_CURRENT_PREPARATION_CLOSE_20261003.json',
    'audits/pr57_30003354/ROOT_CURRENT_PREPARATION_PROGRESS_20261003.json',
    'audits/pr57_30003354/ROOT_PREPRINT_ROUND1_ADJUDICATION_20261003.json',
    'audits/pr57_30003354/ROOT_PRIORITY_ADJUDICATION_20261003.json',
    'audits/pr57_30003354/record_ROOT_final_package_20261003.py',
    'audits/pr57_30003354/ROOT_FINAL_PREPRINT_PACKAGE_ADJUDICATION_20261003.json',
    'audits/pr57_30003354/ROOT_PREPRINT_ROUND2_ADJUDICATION_20261003.json',
    'audits/pr57_30003354/ROOT_PREPRINT_ROUND2_READBACK_20261003.json',
    'audits/pr58_30002298/ROOT_CURRENT_PREPARATION_CLOSE_20261003.json',
    'audits/pr58_30002298/ROOT_SCIENTIFIC_ADJUDICATION_20261003.json',
    'audits/pr58_30002298/ROOT_TANGENT_FAMILY_CLOSE.json',
    'audits/pr58_30002298/ROOT_TANGENT_FAMILY_READBACK.json',
    'audits/pr59_10300025/record_ROOT_science_20261003.py',
    'audits/pr59_10300025/ROOT_SCIENTIFIC_ADJUDICATION_20261003.json',
]
# Completed actual ROOT operations, including the genuine failed storage attempt.
CAP_PIDS = [3854,4081,19625,19768,31203,31334,39656,40354,
            83163,83631,83877,35334,4654,5157,12500,13265,13374,13605,20441,38221,38458,
            20671,20782,21000,85818,86040,71790,71794,54422,54425,
            8132,8244,8353,8464,8576,8717,10500,35902,36020,
            42224,90500,92507,94033,43793,17208,29791,32233,32363,
            51099,51812,40952,41530]
EXTRA_DIRECTORIES = ['audits/pr48_2961/root_finalize_foreign_epoch_v5_readonly']
STORAGE_FILES = ['V3PLAN.md','V3_INPUT_PINS.json','compress_completed_v3.py',
                 'inventory_v3.operator.json','inventory_v3.stderr.bin','inventory_v3.stdout.json','inventory_v3_readonly.py']
STORAGE_OPERATIONS = ['pr33-catalog_y9mcjtwx','pr38-catalog_tmzxwlwx','pr38-problems_vxxmjqtw',
                      'pr38-results_6zj6xzgu','pr39-catalog_ct96nvj5','pr39-catalog_n_atp_92',
                      'pr39-problems_shrso_sn','pr39-results_q5gv9gc_','pr41-typed_el7lkarz']
FORMAL_INVENTORY = '37/180'
ROOT_LOG_MARKER_SUFFIX = ('research evidence only; prepared formal inventory37/180 (20.5556%); '
                         'PR48 merged/pushed, V5 actual author41530 failed before epoch/native/final roles, recovery bookkeeping pending; '
                         'PR57 final package ROOT-ready, unpublished; PR58 already_solved0/5; '
                         'PR59 already_solved1/5; PR60 original unsolved1/5, SOURCE custody pending; '
                         'no native acceptance, DOI or tracker transition by this checkpoint.')
