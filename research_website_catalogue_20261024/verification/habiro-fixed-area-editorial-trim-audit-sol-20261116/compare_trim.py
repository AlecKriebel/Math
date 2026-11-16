#!/usr/bin/env python3
"""One fixed stdout-only comparison of two exact editorial deletions."""
from pathlib import Path
import hashlib
import json
import re

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R = P/'verification/root-habiro-fixed-area-editorial-trim-20261116'


def pin(data):
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest()}


def fixed(path, size, digest):
    data = path.read_bytes()
    assert pin(data) == {'bytes': size, 'SHA256': digest}, str(path)
    return data


def contracted(row):
    return fixed(P/row['path'], row['bytes'], row['SHA256'])


def block(data, expression):
    matches = re.findall(expression, data)
    assert len(matches) == 1
    return matches[0]


def main():
    final = json.loads(fixed(R/'FINAL.json', 942, '4c8196d2a28a672535df9e33a2f3ba789c9d0cb8ff8b1106ea6f62a4125f2a54'))
    manifest = json.loads(fixed(R/'MANIFEST.json', 1523, '6311cea8f92a798c0719b61716e53ba92f0c8d3c0b36ea10fb63d4e123191754'))
    contract = json.loads(fixed(R/'CONTRACT.json', 4522, 'c4421e8bfe6689986068e8006fd3318d99930824f090ce33e03cb5e6889b2cc4'))
    assert {q.name for q in R.iterdir()} == {x['path'] for x in manifest['payload_files']}|{'MANIFEST.json', 'FINAL.json'}
    assert not any(q.is_dir() or q.is_symlink() for q in R.iterdir())
    assert len(list(R.iterdir())) == final['actual_files'] == 10
    for row in manifest['payload_files']:
        fixed(R/row['path'], row['bytes'], row['SHA256'])
    assert pin(contracted(final['only_change_patch'])) == {'bytes': 7378, 'SHA256': 'a9f8d9c13e00de9b4135af38a727ad2b1bc40ffe22f5002055fd3555bb11c105'}
    source_pins = {23425412: (179564, 'b138a4f3e1cda8c195d2a6453121ef9ad144f7f838d79a6cfca9c973f7b001be'),
                   23443039: (156820, '3b005228f30f5ee7015e4d5919c3f4fea0423d47d90832e496be5ae89ed0e376')}
    rows = []
    for row in contract['records']:
        rid = row['record_id']
        old = contracted(row['old_private_page'])
        new = contracted(row['corrected_private_page'])
        removed = contracted(row['removed_section'])
        assert old.count(removed) == 1 and new == old.replace(removed, b'', 1)
        assert removed.count(b'<section ') == 1 and b'Original Zenodo description' in removed
        assert b'id="native-description"' not in new and b'Original Zenodo description' not in new
        main_expression = rb'<main id="main">[\s\S]*?</main>'
        old_main = block(old, main_expression)
        new_main = block(new, main_expression)
        assert pin(old_main) == row['old_MAIN']
        assert new_main == contracted(row['corrected_MAIN']) == old_main.replace(removed, b'', 1)
        abstract_expression = rb'<section id="original-abstract"[\s\S]*?</section>'
        abstract = block(old, abstract_expression)
        assert abstract == block(new, abstract_expression)
        paragraphs = re.findall(rb'<p(?:\s[^>]*)?>[\s\S]*?</p>', abstract)
        assert len(paragraphs) == (1 if rid == 23425412 else 3)
        if rid == 23443039:
            assert b'(z' in abstract and '<sup>−2</sup>'.encode() in abstract
            assert 'e<sup>−1</sup>'.encode() in abstract and b'R&gt;1' in abstract
        old_head = block(old, rb'<head>[\s\S]*?</head>')
        new_head = block(new, rb'<head>[\s\S]*?</head>')
        assert old_head == new_head
        ld = json.loads(block(new_head, rb'<script type="application/ld\+json">\s*([\s\S]*?)\s*</script>'))
        assert 'abstract' not in ld  # Explicit remaining public-assembly requirement.
        size, digest = source_pins[rid]
        source = json.loads(fixed(P/'papers'/str(rid)/'sources/ACQUIRED.json', size, digest))
        native_description = source['records'][0]['description_whole_field']['original_value']
        removed_description = block(removed, rb'<div id="native-description">([\s\S]*?)</div>').decode()
        assert removed_description == native_description
        rows.append({'record_id': rid, 'old_private_page': pin(old), 'corrected_private_page': pin(new),
                     'corrected_MAIN': pin(new_main), 'exact_removed_section': pin(removed),
                     'only_exact_section_removed_every_other_byte_equal': True,
                     'full_original_abstract_HTML': abstract.decode(), 'abstract_paragraph_count': len(paragraphs),
                     'full_abstract_bytes_unchanged': True, 'private_head_bytes_unchanged': True,
                     'source_ACQUIRED_metadata_bytes_unchanged': {'bytes': size, 'SHA256': digest},
                     'complete_native_Description_retained_in_source': True,
                     'full_ScholarlyArticle_abstract_still_required_in_public_wrapper': True})
    print(json.dumps({'status': 'PASS_EXACT_TWO_SECTION_TRIM', 'correction_files': 10,
                      'correction_child_directories': 0, 'rows': rows,
                      'scope': 'Informed editorial data audit only; no new science, native/project/old helper, render/browser/network or external mutation.',
                      'production_authority': False}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
