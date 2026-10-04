"""Implement and reject erroneous alternatives using independent exact artifacts."""
from pathlib import Path
from math import comb
from fractions import Fraction
import hashlib
import json
from independent_product_checks import closure, lattice_volume

HERE = Path(__file__).resolve().parent

def main():
    result_path = HERE / 'INDEPENDENT_RESULTS.json'
    data = json.loads(result_path.read_text())
    r = next(x for x in data['records'] if x['n'] == 2 and x['l'] == 2)
    n, l, q = r['n'], r['l'], [tuple(x) for x in r['q']]
    e = [(0, 0), (1, 0), (0, 1)]
    points = [a + b for a in q for b in e]
    facets = [tuple(x) for x in r['facets']]
    direct = r['projected_massive']
    all_faces = [[0] * len(q) for _ in direct]
    indicator = [[0] * len(q) for _ in direct]
    for face in closure(facets):
        k = len(face) - 1
        v = lattice_volume([points[i] for i in face])
        rows = {i // (l + 1) for i in face}
        cols = {i % (l + 1) for i in face}
        for i in face:
            all_faces[k][i // (l + 1)] += v
        if k == len(rows) + len(cols) - 2:
            for a in rows:
                indicator[k][a] += v
    omit_second_faces = [[sum(comb(k + 1, j + 1) * r['base_massive'][j][a]
                             for j in range(n + 1) if 0 <= k - j <= l)
                          for a in range(len(q))] for k in range(n + l + 1)]
    omit_centroid_ratio = [[sum(comb(l + 1, k - j + 1) * comb(k, j)
                                * r['base_massive'][j][a]
                                for j in range(n + 1) if 0 <= k - j <= l)
                           for a in range(len(q))] for k in range(n + l + 1)]
    omit_product_volume = [[sum(comb(l + 1, k - j + 1) * Fraction(k + 1, j + 1)
                                * r['base_massive'][j][a]
                                for j in range(n + 1) if 0 <= k - j <= l)
                           for a in range(len(q))] for k in range(n + l + 1)]
    cloud = {tuple(x) for x in data['unit_square_projection_cloud']}
    w = (0, 1, 0, 1)
    selected = (2, 0, 2, 0)
    weights = [sum(a * b for a, b in zip(w, x)) for x in cloud]
    rejects = {
        'count_all_internal_faces_as_massive': all_faces != direct,
        'replace_projecting_vertex_count_by_row_indicator': indicator != direct,
        'omit_second_factor_face_count': omit_second_faces != direct,
        'omit_centroid_ratio': omit_centroid_ratio != direct,
        'omit_binomial_product_volume': omit_product_volume != direct,
        'reverse_minimum_to_maximum_for_lower_hull': sum(a * b for a, b in zip(w, selected)) == min(weights) < max(weights),
        'projected_discriminant_vertices_all_extreme': (1, 1, 1, 1) in cloud and (1, 1, 1, 1) == tuple((a + b) // 2 for a, b in zip((2, 0, 2, 0), (0, 2, 0, 2))),
        'squared_Euclidean_length_as_normalized_lattice_length': lattice_volume([(0, 0), (1, 1)]) == 1 != 2,
    }
    assert all(rejects.values()), rejects
    output = {'status': 'PASS_IMPLEMENTED_NEGATIVE_ALTERNATIVES', 'rejected_alternatives': rejects,
              'independent_results_sha256': hashlib.sha256(result_path.read_bytes()).hexdigest(),
              'witness': {'q': q, 'facets': facets, 'correct_projected_massive': direct,
                          'all_faces_wrong': all_faces, 'row_indicator_wrong': indicator,
                          'omitted_second_faces_wrong': omit_second_faces,
                          'omitted_centroid_ratio_wrong': omit_centroid_ratio,
                          'omitted_product_volume_wrong': [[str(x) for x in row] for row in omit_product_volume]},
              'scope': 'Finite mutation witnesses, not universal coverage of every possible implementation error.'}
    (HERE / 'NEGATIVE_RESULTS.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'status': output['status'], 'implemented_alternatives_rejected': len(rejects)}, sort_keys=True))

if __name__ == '__main__':
    main()
