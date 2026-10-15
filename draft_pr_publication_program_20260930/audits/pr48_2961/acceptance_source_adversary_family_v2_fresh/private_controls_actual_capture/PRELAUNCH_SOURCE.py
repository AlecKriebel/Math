"""Handwritten independent OS and scope models. Never loads executable production."""
import copy
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat

F = Path(__file__).absolute().parent
H = F.parent / 'acceptance_preparation_family_v2'
counts = {'assertions': 0}
negatives = []


def need(ok, message):
    counts['assertions'] += 1
    if not ok:
        raise ValueError(message)


def reject(label, operation):
    try:
        operation()
    except (ValueError, OSError):
        negatives.append(label)
    else:
        raise ValueError('Expected rejection missing: ' + label)


def typed_equal(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(typed_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(typed_equal(x, y) for x, y in zip(a, b))
    return a == b


def strict_parse(data):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, 'duplicate key')
            out[k] = v
        return out
    def finite(s):
        v = float(s)
        need(math.isfinite(v), 'nonfinite')
        return v
    def constant(s):
        raise ValueError('nonfinite ' + s)
    return json.loads(data, object_pairs_hook=pairs, parse_float=finite, parse_constant=constant)


def canonical(name):
    need(type(name) is str and name and '\\' not in name and '\x00' not in name, 'path type')
    p = PurePosixPath(name)
    need(not p.is_absolute() and p.as_posix() == name and name != '.'
         and not {'.', '..', '.git', '__pycache__'}.intersection(p.parts), 'path domain')
    return name


def independent_replace(path, body):
    """Separate descriptor-level mechanism, with a retained readable descriptor."""
    need(not path.is_symlink() and stat.S_ISREG(path.stat().st_mode), 'regular target')
    previous = stat.S_IMODE(path.stat().st_mode)
    temporary = path.with_suffix('.independent-stage')
    fd = os.open(temporary, os.O_EXCL | os.O_CREAT | os.O_RDWR, 0o666)
    try:
        for start in range(0, len(body), 23):
            block = body[start:start + 23]
            need(os.write(fd, block) == len(block), 'full block written')
        os.fchmod(fd, previous)
        os.fsync(fd)
        os.replace(temporary, path)
        after = stat.S_IMODE(path.stat().st_mode)
        need(after == previous, 'full mode preserved')
        os.lseek(fd, 0, os.SEEK_SET)
        need(os.read(fd, len(body) + 1) == body, 'entire published descriptor body')
        parentfd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(parentfd)
        finally:
            os.close(parentfd)
    finally:
        os.close(fd)
    return previous, after


def mode_domain(rows, expected_paths, current_modes, old_bodies, current_bodies, allowed):
    need(type(rows) is list and len(rows) == 13, 'thirteen rows')
    identities = [z['path'] for z in rows]
    need(len(set(identities)) == 13 and set(identities) == expected_paths, 'exact identities')
    for row in rows:
        mode = row['worktree_mode']
        need(type(mode) is int and 0 <= mode <= 0o7777, 'typed full mode')
        need(current_modes[row['path']] == mode, 'all thirteen modes including allowed bodies')
        if row['path'] not in allowed:
            need(old_bodies[row['path']] == current_bodies[row['path']], 'protected body')


def log_predicate(records, live, expected_names, note):
    need(type(records) is list and len(records) == 2, 'two logs only')
    for row, name in zip(records, expected_names):
        need(set(row) == {'path', 'prefix', 'before_mode', 'after_mode'}, 'exact log schema')
        need(row['path'] == name, 'owned log identity')
        body, mode = live[name]
        need(type(row['before_mode']) is int and type(row['after_mode']) is int,
             'exact mode types')
        need(0 <= row['before_mode'] <= 0o7777 and row['before_mode'] == row['after_mode'] == mode,
             'owned log fullmode')
        need(body == row['prefix'] + note, 'entire retained prefix plus exact note')


def exact_budget(raw, used, limit, expected):
    need(type(used) is int and type(limit) is int and used == 2 and limit == 5,
         'typed unchanged budget')
    need(type(raw) is bytes and raw == expected and raw.endswith(b'\n'), 'literal two-turn bytes')


def queue_model(before):
    lines = before.decode().splitlines(keepends=True)
    aliases = [s for s in lines if len(s.split('|')) == 14
               and s.split('|')[2].strip().startswith('30004403 / ')]
    need(not aliases, 'alias absent')
    rows = [s for s in lines if len(s.split('|')) == 14
            and s.split('|')[2].strip() == '2961 / KP-4.85']
    need(len(rows) == 1, 'unique primary')
    row = rows[0]
    cells = row.split('|')
    need(cells[8].strip() == 'queued' and cells[9].strip() == '0/5', 'queued baseline')
    out = cells[:]
    out[8], out[9], out[11] = ' unsolved ', ' 2/5 ', ' qualified subgroup partial only '
    result = before.replace(row.encode(), '|'.join(out).encode(), 1)
    need({i for i, (x, y) in enumerate(zip(cells, out)) if x != y} == {8, 9, 11}, 'named columns')
    need(cells[10] == out[10] and cells[12] == out[12], 'Chat and DOI preserved')
    need(result.replace('|'.join(out).encode(), row.encode(), 1) == before, 'entire inverse body')
    return result


def main():
    former_umask = os.umask(0o022)
    work = F / 'private_os_fixtures'
    work.mkdir(exist_ok=False)
    selected = [0o0000, 0o0001, 0o0010, 0o0100, 0o0200, 0o0400, 0o0600, 0o0644,
                0o0755, 0o0777, 0o1000, 0o2000, 0o4000, 0o1600, 0o2600, 0o4600,
                0o7644, 0o7777]
    models = []
    try:
        for i, mode in enumerate(selected):
            path = work / ('mode_%04o.bin' % mode)
            path.write_bytes(b'private original body\n')
            path.chmod(mode)
            need(stat.S_IMODE(path.stat().st_mode) == mode, 'actual initial mode')
            body = (('replacement boundary ' + str(i) + '\n') * 9).encode()
            before, after = independent_replace(path, body)
            models.append({'path': path.relative_to(F).as_posix(), 'before_mode': before,
                           'after_mode': after, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()})
            # Make the first-party retained evidence readable; modes above are actual model-epoch facts.
            path.chmod(0o644)
        old = work / 'old0600_loss.bin'
        old.write_bytes(b'old bytes\n')
        old.chmod(0o600)
        tmp = work / 'old0600_loss.stage'
        tmp.write_bytes(b'new bytes\n')
        os.replace(tmp, old)
        need(stat.S_IMODE(old.stat().st_mode) == 0o644, 'old0600 loss genuinely reproduced')
        occupied = work / 'occupied.bin'
        occupied.write_bytes(b'old unchanged\n')
        stage = occupied.with_suffix('.independent-stage')
        stage.write_bytes(b'retained failed stage\n')
        reject('occupied_temporary_is_not_silently_reused', lambda: independent_replace(occupied, b'invalid'))
        need(occupied.read_bytes() == b'old unchanged\n' and stage.read_bytes() == b'retained failed stage\n',
             'failure retains old body and temp')
    finally:
        os.umask(former_umask)
    paths = {'native' + str(i) for i in range(13)}
    rows = [{'path': 'native' + str(i), 'worktree_mode': 0o644} for i in range(13)]
    modes = {n: 0o644 for n in paths}
    bodies = {n: ('old ' + n).encode() for n in paths}
    allowed = {'native0', 'native1', 'native2', 'native3'}
    changed = dict(bodies)
    for n in allowed:
        changed[n] = b'authorized mutable body'
    mode_domain(rows, paths, modes, bodies, changed, allowed)
    for i, row in enumerate(rows):
        name = row['path']
        for bit in [1 << b for b in range(12)]:
            mutation = dict(modes)
            mutation[name] ^= bit
            reject('native%d_mode_bit_%04o' % (i, bit),
                   lambda mutation=mutation: mode_domain(rows, paths, mutation, bodies, changed, allowed))
    # Predicate boundary coverage for all4096 legal full modes, without claiming4096 filesystem writes.
    for mode in range(0o10000):
        single = copy.deepcopy(rows)
        single[0]['worktree_mode'] = mode
        variant = dict(modes)
        variant['native0'] = mode
        mode_domain(single, paths, variant, bodies, changed, allowed)
    for malformed in [True, False, 420.0, None, -1, 0o10000, '0644']:
        bad = copy.deepcopy(rows)
        bad[0]['worktree_mode'] = malformed
        reject('malformed_mode_' + repr(malformed), lambda bad=bad: mode_domain(bad, paths, modes, bodies, changed, allowed))
    reject('missing_thirteenth', lambda: mode_domain(rows[:-1], paths, modes, bodies, changed, allowed))
    repeated = rows[:-1] + [rows[0]]
    reject('duplicate_native_identity', lambda: mode_domain(repeated, paths, modes, bodies, changed, allowed))
    wrong = dict(changed)
    wrong['native12'] += b' changed'
    reject('immutable_native_body', lambda: mode_domain(rows, paths, modes, bodies, wrong, allowed))
    for literal in ['../escape', '/absolute', 'a//b', 'a/./b', 'a/../b', '.git/config', '__pycache__/x', 'a\\b']:
        reject('noncanonical_' + literal, lambda literal=literal: canonical(literal))
    for raw in ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":1e309}']:
        reject('invalid_JSON_' + raw, lambda raw=raw: strict_parse(raw))
    exact = {'flag': False, 'count': 2, 'metadata': None, 'values': [1, 2]}
    for key, value in [('flag', 0), ('count', True), ('metadata', {}), ('values', [1, 2, 3])]:
        mutant = copy.deepcopy(exact)
        mutant[key] = value
        need(not typed_equal(exact, mutant), 'typed schema mutant ' + key)
    ext = dict(exact)
    ext['approval'] = True
    need(not typed_equal(exact, ext), 'critical schema extension')
    owned_names = ['audit/ROOT_RESEARCH_LOG.md', 'program/RESEARCH_LOG.md']
    note = b'\nfixed actual-finalization note\n'
    logs = [{'path': n, 'prefix': ('prefix ' + n).encode(), 'before_mode': 0o600, 'after_mode': 0o600}
            for n in owned_names]
    live = {z['path']: (z['prefix'] + note, 0o600) for z in logs}
    log_predicate(logs, live, owned_names, note)
    wronglive = dict(live)
    wronglive[owned_names[0]] = (b'prefix rewritten' + note, 0o600)
    reject('owned_log_prefix_rewrite', lambda: log_predicate(logs, wronglive, owned_names, note))
    wronglive = dict(live)
    wronglive[owned_names[1]] = (live[owned_names[1]][0], 0o644)
    reject('owned_log_mode_loss', lambda: log_predicate(logs, wronglive, owned_names, note))
    reject('extra_owned_log', lambda: log_predicate(logs + [logs[0]], live, owned_names, note))
    reject('wrong_fixed_log_note', lambda: log_predicate(logs, live, owned_names, note + b'extra'))
    literal = b'{"turn":1}\n{"turn":2}\n'
    exact_budget(literal, 2, 5, literal)
    for label, raw, used, limit in [('empty', b'', 2, 5), ('invented', b'{"turn":2}\n', 2, 5),
                                   ('bool', literal, True, 5), ('wrong_used', literal, 3, 5),
                                   ('wrong_limit', literal, 2, 4)]:
        reject('budget_' + label, lambda raw=raw, used=used, limit=limit: exact_budget(raw, used, limit, literal))
    primary = '| 1 | 2961 / KP-4.85 | target | 1 | 9 | 8 | yes | queued | 0/5 | KEEP_CHAT | pending | KEEP_DOI |\n'
    other = '| 2 | 123 / OTHER | other | 2 | 8 | 7 | yes | unsolved | 5/5 | FOREIGN_CHAT | unchanged | FOREIGN_DOI |\n'
    queue = ('preamble and exact arbitrary bytes\n' + primary + other).encode()
    out = queue_model(queue)
    need(other.encode() in out and out.startswith(b'preamble and exact arbitrary bytes\n'), 'entire unrelated queue text')
    reject('duplicate_primary_queue', lambda: queue_model(queue + primary.encode()))
    alias = primary.replace('2961 / KP-4.85', '30004403 / OWR-17471-009')
    reject('invented_alias_queue', lambda: queue_model(queue + alias.encode()))
    native_paths = {'native/' + str(i) for i in range(13)}
    def foreign_scope(names):
        need(type(names) is list and names == sorted(set(names)), 'sorted unique foreign list')
        for n in names:
            canonical(n)
            need(n not in native_paths and n != 'program/RESEARCH_LOG.md'
                 and not n.startswith('audit/') and not n.startswith('canonical/'), 'owned excluded from foreign')
    foreign_scope(['program/sibling/RESEARCH_LOG.md'])
    for n in ['program/RESEARCH_LOG.md', 'audit/review.json', 'canonical/x', 'native/12']:
        reject('owned_foreign_' + n, lambda n=n: foreign_scope([n]))
    reject('foreign_unsorted', lambda: foreign_scope(['z', 'a']))
    # Literal SOURCE text comparison only, no compilation, import, or execution.
    operator_text = (H / 'capture_root_final_operation.py').read_text()
    match = re.search(r"assert script\.parent == A / '([^']+)' and script\.name == 'seal_final_evidence\.py'", operator_text)
    need(match is not None, 'literal operative parent predicate located')
    allowed_folder = match.group(1)
    actual_v2 = H / 'seal_final_evidence.py'
    need(actual_v2.parent.name == 'acceptance_preparation_family_v2', 'actual V2 source path')
    def operator_parent_predicate(candidate):
        need(candidate.parent == H.parent / allowed_folder and candidate.name == 'seal_final_evidence.py',
             'operator rejects supplied sealer parent')
    reject('M2_literal_operator_rejects_actual_V2_before_child_launch', lambda: operator_parent_predicate(actual_v2))
    operator_parent_predicate(H.parent / allowed_folder / 'seal_final_evidence.py')
    need(allowed_folder == 'acceptance_preparation_family', 'operator still accepts old V1 path')
    result = {'schema': 'pr48-v2-fresh-source-adversary-private-result/v1',
              'status': 'PASS_PRIVATE_MODE_AND_SCOPE_CONTROLS_WITH_M2_REPRODUCED',
              'utc': dt.datetime.now(dt.timezone.utc).isoformat(), **counts,
              'negative_controls_count': len(negatives), 'negative_controls': negatives,
              'OS_mode_cases': models, 'mode_cases_are_actual_epoch_not_current_fixture_modes': True,
              'predicate_full_modes_checked': 4096, 'filesystem_fullmode_sweep_claimed': False,
              'actual_model_umask': 0o022, 'old0600_loss_reproduced': True,
              'literal_operator_allowed_family': allowed_folder,
              'actual_V2_path_rejected_before_launch': True,
              'production_imported_compiled_executed': False,
              'future_acceptance_approved': False, 'root_approval_authored': False,
              'new_substantive_attempts': 0, 'audit_turns': 0}
    with (F / 'PRIVATE_RESULT.json').open('x') as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k not in {'negative_controls', 'OS_mode_cases'}}, sort_keys=True))


if __name__ == '__main__':
    main()
