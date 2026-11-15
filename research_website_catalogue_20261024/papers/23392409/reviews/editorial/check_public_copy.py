"""Bounded editorial checks, with eight optional memory-only loss controls."""
import copy
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import sys


def require(test, label):
    if not test:
        raise ValueError(label)


def scope_check(p):
    result = ' '.join(p['result'])
    proof = ' '.join(p['why_it_works'])
    limits = ' '.join(p['limitations'])
    require('Six fixed distinct algebraic points' in result, 'fixed algebraic boundary lost')
    require('incoming center Z' in result and 'at least five distinct outgoing centers' in result,
            'incoming-plus-lower-bound count lost')
    require('α = 16' in result and 'both alternating triples noncollinear' in result,
            'exponent or nondegeneracy lost')
    require(all(x in result for x in ['A₁A₂A₃Z', 'A₃A₄A₅Z', 'A₅A₆A₁Z',
                                     'A₂A₃A₄X', 'A₄A₅A₆X', 'A₆A₁A₂X']),
            'ordered face coverage lost')
    require('fixed boundary crosses' in limits and 'cannot yield a proper embedding' in limits,
            'crossing category lost')
    require('exact total' in limits and 'universal maximum' in limits and 'α < 1' in limits
            and 'joint intersection transversality' in limits and 'historical firstness' in limits,
            'scope exclusions lost')
    require('individually smooth' in proof and 'A₃ lies on one curve' in proof,
            'distinct individual-curve argument lost')
    require(p['version_field_present'] is False and p['version'] is None
            and p['printed_version_field_present'] is False and p['printed_version'] is None,
            'absent versions invented or flattened')
    require(p['publication_date'] == '2026-10-15'
            and p['native_record_created'] == '2026-10-15T10:30:58.597543+00:00'
            and p['native_record_updated'] == '2026-10-15T10:30:58.922225+00:00',
            'original date replaced by record or review timestamp')
    require(p['additional_assets'] == [{'filename': 'five_centers.tex',
                                      'label': 'Original standalone TeX source'}],
            'standalone TeX download lost')
    require(p['license'] == 'CC BY 4.0' and p['authored_package_license'] == 'CC BY 4.0'
            and p['code_license'] is None and 'MIT' not in p['rights_notice'],
            'authored rights changed')
    require('used extensively' in p['ai_disclosure'] and 'unrefereed' in p['ai_disclosure']
            and 'has not received conventional human peer review' in p['ai_disclosure'],
            'AI or review status lost')
    require(p['follow_up'] is None and p['canonical_url'] is None and p['AA'] is None,
            'unapproved followup or live identity asserted')


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.links = []
        self.scripts = []
        self.canonicals = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta' and 'name' in a:
            self.meta[a['name']] = a.get('content')
        if tag == 'a':
            self.links.append(a.get('href'))
        if tag == 'script':
            self.scripts.append(a)
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonicals.append(a)


def main():
    require(sys.argv[1:] in [[], ['--loss-controls']], 'unsupported arguments')
    e = Path(__file__).resolve().parent
    p = json.loads((e / 'publication.json').read_bytes())
    scope_check(p)
    main_html = (e / 'PUBLIC_MAIN.html').read_text()
    page = (e / 'candidate/index.html').read_text()
    require(main_html in page, 'whole public main missing from candidate')
    for key in ['plain_language', 'result', 'why_it_works', 'limitations', 'background']:
        for text in p[key]:
            require(html.escape(text) in main_html, 'public paragraph lost: ' + key)
    for key in ['abstract', 'collaboration', 'ai_disclosure', 'reader_intro', 'rights_notice']:
        require(html.escape(p[key]) in main_html, 'public scalar prose lost: ' + key)
    scan = Scan()
    scan.feed(page)
    require(scan.meta['robots'] == 'noindex,nofollow,noarchive' and not scan.canonicals,
            'private noindex or unset canonical lost')
    require(scan.meta['citation_title'] == p['title'] and scan.meta['citation_author'] == 'Alec Kriebel'
            and scan.meta['citation_publication_date'] == '2026/10/15'
            and scan.meta['citation_doi'] == '10.5281/zenodo.23392409', 'scholarly identity lost')
    require(all(x in scan.links for x in ['five_centers.pdf', 'five_centers.tex',
                                         'verification-package.zip', 'citation.bib',
                                         'https://doi.org/10.5281/zenodo.23392409',
                                         'https://orcid.org/0009-0001-9320-500X']),
            'required reader or source link lost')
    require(scan.scripts == [{'type': 'application/ld+json'}], 'unexpected executable or remote script')
    require('font-family:Arial,Helvetica,sans-serif' in page and 'background:#fff' in page,
            'plain white Arial candidate lost')
    for token in ['root-clearance', 'ROOT_REVIEW', '17472', '17,472', '1939', '1393',
                  '2026-11-15', 'audit_evidence', 'mailto:', 'PASS_FULL_ORIGINAL']:
        require(token not in page, 'private review/bookkeeping/contact item leaked: ' + token)
    bib = (e / 'citation.bib').read_text()
    require('version =' not in bib.lower() and '2026' in bib and '23392409' in bib,
            'BibTeX invented version or lost identity')
    scholarly = json.loads((e / 'SCHOLARLY_METADATA.json').read_bytes())
    require('version' not in scholarly and scholarly['datePublished'] == '2026-10-15'
            and scholarly['identifier'] == p['doi'], 'JSON-LD version or date error')
    count = 0
    if sys.argv[1:] == ['--loss-controls']:
        cases = []
        q = copy.deepcopy(p); q['result'][0] = q['result'][0].replace('at least five', 'exactly five'); cases.append(q)
        q = copy.deepcopy(p); q['result'][0] = q['result'][0].replace('incoming center Z', 'a point'); cases.append(q)
        q = copy.deepcopy(p); q['limitations'][0] = 'Proper embedding.'; cases.append(q)
        q = copy.deepcopy(p); q['result'][1] = q['result'][1].replace('A₅A₆A₁Z', 'A₅A₁A₆Z'); cases.append(q)
        q = copy.deepcopy(p); q['version_field_present'] = True; q['version'] = '1.0'; cases.append(q)
        q = copy.deepcopy(p); q['publication_date'] = '2026-11-15'; cases.append(q)
        q = copy.deepcopy(p); q['additional_assets'] = []; cases.append(q)
        q = copy.deepcopy(p); q['license'] = 'MIT'; cases.append(q)
        for q in cases:
            try:
                scope_check(q)
            except ValueError:
                count += 1
            else:
                raise ValueError('a semantic-loss control was not detected')
        require(count == 8, 'loss-control count')
    print(json.dumps({'status': 'PASS', 'mode': 'bounded editorial copy checks',
                      'memory_only_loss_controls_detected': count,
                      'scientific_execution': False, 'writes_network_subprocess': False}))


if __name__ == '__main__':
    main()
