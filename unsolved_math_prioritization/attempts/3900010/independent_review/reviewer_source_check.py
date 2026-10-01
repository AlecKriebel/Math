"""Hash binding and independent source-image/coordinate comparison.
Usage: python reviewer_source_check.py AUTHOR_ATTEMPT SOURCE_DIRECTORY
Reading images are not redistributed with the review.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys
from PIL import Image

author, sources = map(Path, sys.argv[1:3])
C = Counter()


def check(ok, label):
    assert ok, label
    C[label] += 1


manifest = json.loads((author/'FROZEN_MANIFEST.json').read_text())
for entry in manifest['files']:
    data = (author/entry['path']).read_bytes()
    check(len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256'],
          'frozen_author_file_hash_and_length')
source_manifest = json.loads((author/'source_manifest.json').read_text())
for entry in source_manifest['files']:
    data = (sources/entry['file']).read_bytes()
    check(len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256'],
          'primary_source_file_hash_and_length')

image = Image.open(sources/'tile02.gif').convert('RGB')
check(image.size == (79, 49), 'source_tile_image_dimensions')
for row in range(3):
    for column in range(6):
        expected = (255, 255, 255) if row == 0 or column < 4 else (204, 204, 204)
        check(image.getpixel((14+10*column, 14+10*row)) == expected,
              'source_cell_center_exact_6_4_4_shape')

P = [(x, y) for y, n in [(0, 4), (1, 4), (2, 6)] for x in range(n)]
maps = [lambda x, y: (x, y), lambda x, y: (2-y, x),
        lambda x, y: (5-x, 2-y), lambda x, y: (y, 5-x),
        lambda x, y: (5-x, y), lambda x, y: (2-y, 5-x),
        lambda x, y: (x, 2-y), lambda x, y: (y, x)]
witness = json.loads((author/'known_even_witness.json').read_text())
W, H = witness['width'], witness['height']
owner = {}
for i, tile in enumerate(witness['tiles']):
    for a, b in P:
        x, y = maps[tile['orientation']](a, b)
        cell = x+tile['x'], y+tile['y']
        check(cell not in owner, 'image_certificate_unique_cell_owner')
        owner[cell] = i
picture = Image.open(sources/'known66x84.gif').convert('RGB')
check(picture.size == (10*W+1, 10*H+1), 'source_witness_image_dimensions')
for y in range(H):
    for x in range(W):
        for dx, dy in [(1, 0), (0, 1)]:
            if x+dx >= W or y+dy >= H:
                continue
            boundary = owner[x, y] != owner[x+dx, y+dy]
            pixel = picture.getpixel((10*x+5+5*dx, 10*y+5+5*dy))
            check(pixel == ((0, 0, 0) if boundary else (255, 255, 255)),
                  'every_source_internal_edge_matches_coordinate_certificate')
ledger = [json.loads(line) for line in (author/'turn_ledger.jsonl').read_text().splitlines()]
turns = [event for event in ledger if event.get('event') == 'proof_attempt_turn']
check([event['turns_used'] for event in turns] == [1, 2, 3, 4, 5], 'five_substantive_author_turn_events')

print(json.dumps({'status': 'PASS', 'exact_assertions': sum(C.values()),
                  'families': dict(sorted(C.items())),
                  'author_manifest_sha256': hashlib.sha256((author/'FROZEN_MANIFEST.json').read_bytes()).hexdigest(),
                  'author_result_sha256': hashlib.sha256((author/'RESULT.md').read_bytes()).hexdigest(),
                  'source_reading_scope': 'Exact target image, credited even-tiling image and all supplied primary hashes checked. Complete 1997 and 2014 source texts were not supplied or asserted read.'},
                 indent=2, sort_keys=True))
