"""Apply source-bound subfield-importance scores to open QUEUE.md rows."""
import csv, hashlib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
SCORES = ROOT / 'impact_scorebook.json'
QUEUE = ROOT / 'QUEUE.md'
OPEN_STATUSES = {'queued', 'unsolved', 'in_progress', 'claimed_solved', 'preprint_published'}
ALL_STATUSES = OPEN_STATUSES | {'already_solved'}


def load_scores():
    book = json.loads(SCORES.read_text())
    if book.get('version') != 'subfield-importance-v1':
        raise ValueError('Unsupported scorebook version')
    return book['scores']


def apply():
    scores = load_scores()
    lines = QUEUE.read_text().splitlines()
    catalog = {row['id']: row for row in json.loads((ROOT / 'catalog.json').read_text())}
    row_status = {}
    header_index = next(i for i, line in enumerate(lines) if line.startswith('| Rank |'))
    if 'Impact (/10)' in lines[header_index]:
        raise ValueError('QUEUE.md already has the impact column')
    header = lines[header_index].split('|')
    ev_index = next(i for i, cell in enumerate(header) if cell.strip() == 'EV')
    header.insert(ev_index + 1, ' Impact (/10) ')
    lines[header_index] = '|'.join(header)
    sep = lines[header_index + 1].split('|')
    sep.insert(ev_index + 1, '---:')
    lines[header_index + 1] = '|'.join(sep)

    seen = set()
    for index, line in enumerate(lines):
        if not line.startswith('| ') or index in (header_index, header_index + 1):
            continue
        fields = line.split('|')
        if len(fields) < 9:
            continue
        key = fields[2].strip().split('/')[0].strip()
        status_matches = [i for i in range(1, len(fields)-1)
                          if fields[i].strip() in ALL_STATUSES
                          and re.fullmatch(r'(?:\d+\s*/\s*\d+|—)', fields[i+1].strip())]
        if not status_matches:
            continue  # non-table content or a non-problem table
        if len(status_matches) != 1:
            raise ValueError(f'Ambiguous status cell on queue line {index+1}')
        status_index = status_matches[0]
        if status_index < 4:
            raise ValueError(f'Cannot locate EV cell on queue line {index+1}')
        status = fields[status_index].strip()
        row_status[key] = status
        item = scores.get(key)
        if status == 'already_solved':
            value = '—'
        else:
            if item is None:
                raise ValueError(f'No subfield impact score for open queue ID {key}')
            if key != 'KOU-16.45':
                if key not in catalog or item['source_hash'] != catalog[key]['review_hash']:
                    raise ValueError(f'Subfield impact score is stale for source {key}')
            value = f"{item['score']:.1f}"
            seen.add(key)
        ev_index_for_row = status_index - 3
        fields.insert(ev_index_for_row + 1, f' {value} ')
        lines[index] = '|'.join(fields)

    expected = {key for key in scores if key != 'KOU-16.45' and row_status.get(key) != 'already_solved'}
    missing = expected - seen
    if missing:
        raise ValueError('Scorebook entries not represented in open queue: ' + ', '.join(sorted(missing)[:10]))
    QUEUE.write_text('\n'.join(lines) + '\n')
    print(f'Added the impact column to {len(seen)} open problems; already-solved rows are blank.')


if __name__ == '__main__':
    apply()
