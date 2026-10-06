#!/usr/bin/env python3
"""Normal/optimized/relocated and independent adversarial witness controls."""
import copy
import itertools
import json
import pathlib
import runpy
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def invoke(script, path=None, optimized=False, cwd='/'):
    cmd = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(script)]
    if path is not None:
        cmd.append(str(path))
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def independent_enumeration():
    # Separate letter-based implementation. No call to witness_check.analyze.
    states = [p for p in itertools.permutations('aAbB') if p.index('a') < p.index('A')
              and p.index('b') < p.index('B')]
    reverse = lambda p: tuple(x.swapcase() for x in p[::-1])
    neighbors = {}
    for p in states:
        neighbors[p] = []
        for i in range(3):
            q = list(p); q[i], q[i + 1] = q[i + 1], q[i]
            if tuple(q) in states:
                neighbors[p].append(tuple(q))
    def walks(p, depth):
        if depth == 0:
            yield [p]
        else:
            for q in neighbors[p]:
                for tail in walks(q, depth - 1):
                    yield [p] + tail
    counts = {'primitive_eight_term_words': 0, 'switch_once_words': 0,
              'weak_words_violating_switch_once': 0, 'no_separating_switch_words': 0}
    witness = [tuple(t) for t in ['abAB', 'abBA', 'abAB', 'abBA', 'baBA', 'abBA', 'baBA', 'abBA']]
    found = False
    for start in states:
        for half in walks(start, 4):
            if half[-1] != reverse(start):
                continue
            word = half[:-1] + [reverse(p) for p in half[:-1]]
            if any(all(word[i] == word[(i + d) % 8] for i in range(8)) for d in (1, 2, 4)):
                continue
            switches = [tuple(b[j] for j in range(4) if a[j] != b[j])
                        for a, b in zip(word, word[1:] + word[:1])]
            counts['primitive_eight_term_words'] += 1
            if len(set(switches)) == 8:
                counts['switch_once_words'] += 1
            else:
                counts['weak_words_violating_switch_once'] += 1
            if all(a.islower() == b.islower() for a, b in switches):
                counts['no_separating_switch_words'] += 1
            found = found or word == witness
    require(found, 'Independent graph enumeration missed the witness')
    require(counts['weak_words_violating_switch_once'] > 0, 'No axiom gap found')
    return {'result': 'PASS', 'witness_found': found, 'rooted_words_not_isomorphism_classes': True, **counts}


def main():
    base = json.loads((ROOT / 'WITNESS.json').read_text())
    script = ROOT / 'witness_check.py'
    tests = []
    for opt in (False, True):
        mode = 'optimized' if opt else 'normal'
        require(invoke(script, optimized=opt).returncode == 0, mode + ' baseline')
        tests.append(mode + ':baseline')
        with tempfile.TemporaryDirectory(prefix='double-permutation-audit-') as tmp:
            moved = pathlib.Path(tmp) / 'moved with spaces'; moved.mkdir()
            shutil.copy2(script, moved / script.name)
            shutil.copy2(ROOT / 'WITNESS.json', moved / 'WITNESS.json')
            require(invoke(moved / script.name, optimized=opt).returncode == 0, 'Relocation')
            tests.append(mode + ':relocated-default-path')
            cases = []
            def changed(name, operation):
                data = copy.deepcopy(base); operation(data); cases.append((name, json.dumps(data), False))
            changed('boolean-schema', lambda d: d.update(schema=True))
            changed('boolean-n', lambda d: d.update(n=True))
            changed('missing-field', lambda d: d.pop('schema'))
            changed('unexpected-field', lambda d: d.update(unexpected=1))
            changed('period-truncated', lambda d: d['sequence'].pop())
            changed('wrong-term-size', lambda d: d['sequence'][0].pop())
            changed('boolean-symbol', lambda d: d['sequence'][0].__setitem__(0, True))
            changed('duplicate-symbol', lambda d: d['sequence'][0].__setitem__(1, 1))
            changed('endpoint-order', lambda d: d['sequence'].__setitem__(0, [-1, 2, 1, -2]))
            changed('broken-half-reversal', lambda d: d['sequence'].__setitem__(4, [1, 2, -1, -2]))
            stutter = [base['sequence'][0]] * 4 + [base['sequence'][4]] * 4
            changed('stutter', lambda d: d.update(sequence=stutter))
            # Half-symmetric length-eight word with nonadjacent transitions.
            invalid = [[1, -1, 2, -2], [2, -2, 1, -1]] * 4
            changed('nonadjacent-transition', lambda d: d.update(sequence=invalid))
            changed('short-fundamental-period', lambda d: d.update(sequence=[base['sequence'][1]] * 8))
            good = [[1,-1,2,-2], [1,2,-1,-2], [2,1,-1,-2], [2,1,-2,-1],
                    [2,-2,1,-1], [2,1,-2,-1], [2,1,-1,-2], [1,2,-1,-2]]
            changed('switch-once-is-not-gap', lambda d: d.update(sequence=good))
            cases += [('duplicate-json-key', '{"schema":1,"schema":1,"n":2,"sequence":[]}', False),
                      ('nonfinite-json', json.dumps(base)[:-1] + ',"x":NaN}', False),
                      ('malformed-json', '{', False), ('null-root', 'null', False)]
            for name, raw, expected in cases:
                path = moved / 'input.json'; path.write_text(raw)
                result = invoke(moved / script.name, path, opt)
                require(result.returncode != 0 and result.stderr.startswith('FAIL:'), 'Accepted ' + name)
                tests.append(mode + ':' + name)
            # Relabeling and reversal cannot repair an omitted switch type.
            for name, seq in [('cyclic-shift', base['sequence'][1:] + base['sequence'][:1]),
                              ('reverse-time', list(reversed(base['sequence'])))]:
                path = moved / 'input.json'; path.write_text(json.dumps(dict(base, sequence=seq)))
                require(invoke(moved / script.name, path, opt).returncode == 0, name)
                tests.append(mode + ':' + name)
    api = runpy.run_path(str(script), run_name='witness_check_test_import')
    good_result = api['analyze']({'schema': 1, 'n': 2, 'sequence': good})
    require(good_result['switch_once_condition'] and good_result['separating_switch_count'] == 4,
            'Positive switch-once control failed')
    print(json.dumps({'result': 'PASS', 'cli_control_count': len(tests), 'checks': tests,
                      'positive_switch_once_control': 'PASS',
                      'independent_letter_graph_enumeration': independent_enumeration(),
                      'scope': 'Finite witness/code controls; no representation theorem reproof.'}, indent=2))


if __name__ == '__main__':
    main()
