"""Independent absolute-coordinate replay of the author's 1D certificate.
No import of its generator, solver, or verifier; no game-search result is trusted.
Every length-six Angel word is replayed while retaining every actual announcement.
"""
import hashlib, itertools, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'pass1_survival/terminal_1d_horizon6_certificate.json'

def view(absolute_bombs, angel, remaining):
    rel = sorted({p - angel for p in absolute_bombs if abs(p - angel) <= remaining})
    ref = sorted(-x for x in rel)
    return (ref, -1) if ref < rel else (rel, 1)

def main():
    data = SOURCE.read_bytes()
    cert = json.loads(data)
    assert cert['dimension'] == 1 and cert['horizon'] == 6
    assert cert['moves'] == [-1, 0, 1] and cert['all_detonation_times'] == 6
    assert cert['first_bomb_relative_to_first_angel_position'] == 0
    states = cert['states']
    visited = set()
    examples = []
    count = 0
    for moves in itertools.product((-1, 0, 1), repeat=6):
        angel = moves[0]
        bombs = [angel]  # Round 1, after observing a_1, target (a_1, 6).
        key = cert['root']
        trace = [{'round': 1, 'angel': angel, 'bomb_position': angel, 'detonation': 6}]
        for n in range(2, 6):
            h = 7 - n
            coordinates, orientation = view(bombs, angel, h)
            row = states[key]
            visited.add(key)
            assert row['remaining_moves'] == h and row['bombs'] == coordinates
            responses = row['responses']
            assert sorted(r['angel_move'] for r in responses) == [-1, 0, 1]
            step = moves[n-1]
            response = next(r for r in responses if r['angel_move'] == orientation * step)
            angel += step
            q = response['devil_bomb_relative_to_new_position']
            assert type(q) is int
            actual = angel + orientation * q
            bombs.append(actual)
            key = response['next_state']
            projected, _ = view(bombs, angel, h-1)
            assert states[key]['remaining_moves'] == h-1
            assert states[key]['bombs'] == projected
            trace.append({'round': n, 'angel': angel, 'bomb_position': actual, 'detonation': 6})
        visited.add(key)
        leaf = states[key]
        assert leaf['remaining_moves'] == 1 and not leaf['responses']
        assert set((-1, 0, 1)).issubset(leaf['bombs'])
        angel += moves[5]
        assert angel in bombs  # Five prior, legal announcements; no round-6 attack.
        assert len(bombs) == 5
        trace.append({'round': 6, 'angel': angel, 'loss_from_previous_bomb': True})
        count += 1
        if moves in [(-1,)*6, (0,)*6, (1,)*6, (-1, 1, -1, 1, -1, 1)]:
            examples.append({'angel_moves': list(moves), 'trace': trace})
    assert count == 3**6 and visited == set(states)
    out = {
        'verified': True,
        'certificate_sha256': hashlib.sha256(data).hexdigest(),
        'certificate_bytes': len(data),
        'replayed_angel_words': count,
        'reachable_certificate_states': len(visited),
        'prior_announcements_per_play': 5,
        'terminal_time': 6,
        'method': 'Absolute-coordinate exhaustive replay, retaining all actual bombs; no imported search code.',
        'scope': 'One-dimensional king-step game; every bomb detonates at time 6. Not a two-dimensional loss.',
        'examples': examples,
    }
    (ROOT / 'independent_1d_replay.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'examples'}, indent=2))

if __name__ == '__main__':
    main()
