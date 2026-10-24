#!/usr/bin/env python3
"""Separate independent rank-six delta check, importing no author programs."""
import datetime
import hashlib
import json
from collections import deque
from pathlib import Path

review = Path(__file__).resolve().parent
root = review.parent
source = root / 'rank6_cocycle_certificate.json'
certificate = json.loads(source.read_text())


def check(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse(word):
    return [-letter for letter in reversed(word)]


epsilon = {(2, 1), (3, 1), (5, 2), (6, 2), (8, 3), (9, 3),
           (10, 3), (12, 3), (16, 4), (31, 4)}
permutations, backwards = [], []
for i in range(6):
    action = [(v ^ (1 << i)) + 64 * (s ^ int((v, i) in epsilon))
              for s in range(2) for v in range(64)]
    check(sorted(action) == list(range(128)), 'Invalid cover permutation')
    permutations.append(action)
    back = [None] * 128
    for start, end in enumerate(action):
        back[end] = start
    backwards.append(back)
check(certificate['permutations'] == permutations, 'Graph differs from explicit ten-entry epsilon data')
check((certificate['m'], certificate['fiber_cover_degree'],
       certificate['stable_letter_power'], certificate['index']) == (6, 128, 16, 2048),
      'Incorrect advertised parameters')


def walk(word, start=0, weights=None):
    position, value = start, 0
    for letter in word:
        check(type(letter) is int and 1 <= abs(letter) <= 6, 'Illegal letter')
        i = abs(letter) - 1
        if letter > 0:
            if weights is not None:
                value += weights.get((position, i), 0)
            position = permutations[i][position]
        else:
            position = backwards[i][position]
            if weights is not None:
                value -= weights.get((position, i), 0)
    return position, value


visited, queue = {0}, deque([0])
while queue:
    vertex = queue.popleft()
    for i in range(1, 7):
        end, _ = walk([i], vertex)
        if end not in visited:
            visited.add(end)
            queue.append(end)
check(len(visited) == 128, 'Disconnected cover')

# Iteratively substitute ai -> ai*a(i-1), not the inverse automorphism.
images = [[i] for i in range(1, 7)]
for _ in range(16):
    images = [[letter2 for letter in word
               for letter2 in ([letter] if letter == 1 else [letter, letter - 1])]
              for word in images]
endpoint_checks = 0
for vertex in range(128):
    for i in range(6):
        check(walk(images[i], vertex)[0] == permutations[i][vertex],
              'theta16 fails identity-vertex lift')
        endpoint_checks += 1

characters, cell_checks = {}, 0
for record in certificate['characters']:
    index = record['index']
    check(type(index) is int and index not in characters, 'Duplicate character index')
    weights = {}
    for key, value in record['positive_edge_weights'].items():
        coordinates = key.split(',')
        check(len(coordinates) == 2, 'Malformed edge key')
        edge = tuple(map(int, coordinates))
        check(0 <= edge[0] < 128 and 0 <= edge[1] < 6 and type(value) is int,
              'Nonintegral or out-of-range edge weight')
        weights[edge] = value
    beta = record['vertex_potentials']
    check(len(beta) == 128 and all(type(x) is int for x in beta), 'Bad integral potential')
    for vertex in range(128):
        for i in range(6):
            end, value = walk(images[i], vertex, weights)
            check(value - weights.get((vertex, i), 0) == beta[end] - beta[vertex],
                  f'Failed cell: character {index}, vertex {vertex}, generator {i+1}')
            cell_checks += 1
    characters[index] = weights
check(len(characters) == 6 and cell_checks == 4608, 'Incorrect character/cell count')

targets = []
check(len(certificate['targets']) == 6, 'Incorrect target count')
for i, record in enumerate(certificate['targets'], 1):
    check(record['label'] == f'a{i}' and record['word'] == [i], 'Target label/word mismatch')
    power, position = 0, 0
    while True:
        power += 1
        position, _ = walk([i], position)
        if position == 0:
            break
        check(power < 128, 'Invalid generator orbit')
    check(record['power_closing_in_fiber_cover'] == power, 'Incorrect first closed power')
    weights = characters[record['character_index']]
    end, value = walk([i] * power, weights=weights)
    check(end == 0 and value != 0, 'Target power not closed or invisible')
    check(record['visible'] is True and record['character_value'] == str(value),
          'Incorrect recorded target evaluation')
    end2, value2 = walk(images[i - 1] * power, weights=weights)
    check(end2 == 0 and value2 == value, 'Substituted target invariant evaluation fails')
    # Independent signed-path check: inverse target must contribute -value.
    end3, value3 = walk([-i] * power, weights=weights)
    check(end3 == 0 and value3 == -value, 'Inverse target sign evaluation fails')
    targets.append(dict(label=f'a{i}', power=power, character_index=record['character_index'],
                        value=value, inverse_value=value3))
check(targets[0]['value'] == 14 and targets[0]['power'] == 2, 'Central a1^2 visibility claim fails')

# The earlier rank-five review is checked read-only and is not refrozen here.
frozen = review / 'COCYCLE_AUDIT_HASHES.json'
check(sha(frozen) == 'c80308bce7db242fce1abfe6e6d02e0deb00dc23ef5533c46dde11ff0099eb87',
      'Earlier rank-five review manifest changed')
for entry in json.loads(frozen.read_text())['files']:
    check(sha(review / entry['file']) == entry['sha256'], 'Earlier rank-five artifact changed')

result = dict(status='PASS', timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              scope='Separate rank-six finite-cover visibility delta only',
              certificate_sha256=sha(source), certificate_bytes=source.stat().st_size,
              verifier_sha256=sha(Path(__file__)), graph_vertices=len(visited), index=2048,
              stable_letter_power=16, endpoint_checks=endpoint_checks,
              theta16_positive_word_lengths=[len(w) for w in images],
              integral_characters=len(characters), edge_cell_checks=cell_checks,
              signed_target_checks=12, substituted_target_checks=6, targets=targets,
              rank5_frozen_review_unchanged=True,
              limited_delta_review_completion_percent=100,
              retraction_onto_a1_squared_claimed=False)
output = review / 'RANK6_DELTA_RECEIPT.json'
output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
