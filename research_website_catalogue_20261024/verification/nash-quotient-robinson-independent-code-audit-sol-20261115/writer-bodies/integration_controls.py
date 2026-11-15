"""Six new bounded memory-only integration falsifiers, current triplet only.

Imports only this stage's fully read renderer. Does not invoke a legacy,
scientific, native or external program; never writes files or uses a network.
"""
import copy
import json
import sys
sys.dont_write_bytecode = True
import render_stage as stage


def rejects(label, operation):
    try:
        operation()
    except ValueError as e:
        return {'fault': label, 'rejected': True, 'actual_exception': str(e)}
    raise RuntimeError('uncaught integration fault: ' + label)


def main():
    _, website, frozen = stage.read_manifests()
    rows = stage.rows_for(frozen)
    buffers = stage.render_buffers(frozen, website, rows)
    positive = stage.validate_buffers(buffers, frozen, website, rows)
    results = []
    robinson = rows[2]['main']
    results.append(rejects('actual125 iframe height850 changed to0',
                   lambda: stage.body_contract(robinson.replace('height="850"', 'height="0"', 1), '23333002')))
    results.append(rejects('hiding attribute inserted into substantive125 paragraph',
                   lambda: stage.body_contract(robinson.replace('<p class="math">', '<p class="math" hidden>', 1), '23333002')))
    cases = []
    bad = dict(buffers)
    pdf = 'research/' + rows[0]['config']['slug'] + '/assets/' + rows[0]['config']['pdf_filename']
    bad[pdf] = bad[pdf][:-1]
    cases.append(('complete original123PDF truncated by one byte', bad))
    bad = dict(buffers)
    nash = 'research/' + rows[0]['config']['slug'] + '/index.html'
    bad[nash] = bad[nash].replace(b'<td>D', b'<td>E', 1)
    stage.need(bad[nash] != buffers[nash], 'actual table-cell mutation applied')
    cases.append(('actual123 normalization table reference changed', bad))
    bad = dict(buffers)
    bad['research/index.html'] = bad['research/index.html'].replace(b'free-spanning-forest-degree', b'changed-unrelated-record', 1)
    cases.append(('one prior typed ItemList URL changed', bad))
    bad = dict(buffers)
    bad['research/sitemap.xml'] = bad['research/sitemap.xml'].replace(b'<lastmod>', b'<lastmodified>', 1)
    cases.append(('one old sitemap node tag changed', bad))
    for label, bad in cases:
        results.append(rejects(label, lambda bad=bad: stage.validate_buffers(bad, frozen, website, rows)))
    print(json.dumps({'positive_actual_overlay': positive, 'new_memory_only_faults': results,
                      'fault_count': len(results), 'scientific_native_legacy_campaigns': False,
                      'source_site_or_file_writes': False, 'subprocesses_or_network': False}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
