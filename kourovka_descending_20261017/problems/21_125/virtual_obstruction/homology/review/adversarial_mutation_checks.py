#!/usr/bin/env python3
"""Check that synthetic corruptions are rejected, without altering inputs."""
import copy
import datetime
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

review = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('independent_audit', review / 'independent_cocycle_audit.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
original_path = review.parent / 'rank5_cocycle_certificate.json'
original = json.loads(original_path.read_text())


def char63(data):
    return next(c for c in data['characters'] if c['index'] == 63)


def corrupt_graph(data):
    data['permutations'][0][0], data['permutations'][0][1] = data['permutations'][0][1], data['permutations'][0][0]


def corrupt_weight(data):
    char63(data)['positive_edge_weights']['1,0'] += 1


def corrupt_potential(data):
    char63(data)['vertex_potentials'][16] += 1


def corrupt_signed_word(data):
    data['targets'][5]['word'][0] *= -1


def corrupt_power(data):
    data['targets'][1]['power_closing_in_fiber_cover'] = 2


def corrupt_value(data):
    data['targets'][0]['character_value'] = '2'


def corrupt_character_assignment(data):
    data['targets'][0]['character_index'] = 62


def corrupt_integrality(data):
    char63(data)['positive_edge_weights']['1,0'] = 1.0


mutations = [corrupt_graph, corrupt_weight, corrupt_potential, corrupt_signed_word,
             corrupt_power, corrupt_value, corrupt_character_assignment, corrupt_integrality]
receipt = []
with tempfile.TemporaryDirectory(prefix='synthetic_mutation_', dir=review) as temporary:
    for mutate in mutations:
        data = copy.deepcopy(original)
        mutate(data)
        path = Path(temporary) / (mutate.__name__ + '.json')
        path.write_text(json.dumps(data))
        try:
            module.audit(path, check_manifest=False)
        except ValueError as error:
            receipt.append(dict(mutation=mutate.__name__, rejected=True, reason=str(error)))
        else:
            raise RuntimeError('Synthetic corruption passed: ' + mutate.__name__)
result = dict(status='PASS', timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              verifier_sha256=hashlib.sha256((review / 'independent_cocycle_audit.py').read_bytes()).hexdigest(),
              synthetic_mutations=len(receipt), checks=receipt)
(review / 'adversarial_mutation_receipt.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
