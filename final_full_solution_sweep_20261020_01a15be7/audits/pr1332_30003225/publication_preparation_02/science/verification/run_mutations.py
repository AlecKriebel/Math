"""Active source-mutation diagnostics, with no filesystem or network writes."""
from pathlib import Path
import hashlib
import json


def run():
    source = Path(__file__).with_name('exact_checks.py').read_text()
    changes = [
        ('floor_for_ceiling', '(5+k-1)//k', '5//k'),
        ('only_zero_completion', 'parameters = list(product(range(2), repeat=5-k))', 'parameters = [tuple(0 for _ in range(5-k))]'),
        ('wrong_toric_chart', '[(3,5,1,2),(2,5,1,3)]', '[(3,4,1,2),(2,5,1,3)]'),
    ]
    results = []
    for name, old, new in changes:
        if source.count(old) != 1:
            raise RuntimeError('mutation anchor must occur exactly once: ' + name)
        bad = source.replace(old, new, 1)
        namespace = {'__name__':'mutation_' + name}
        try:
            exec(compile(bad, '<in-memory-exact-checks-'+name+'>', 'exec'), namespace)
            namespace['run']()
        except RuntimeError as error:
            results.append({'name':name,'status':'rejected','exception':'RuntimeError','diagnostic':str(error),'mutated_source_sha256':hashlib.sha256(bad.encode()).hexdigest()})
        else:
            raise RuntimeError('false source mutation passed: '+name)
    return {'status':'PASS','mutants':results,'scope':'Three distinct active source mutations. Interpreter repetitions are not distinct mathematical cases. No service actions or writes.'}


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
