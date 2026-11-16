#!/usr/bin/env python3
"""Fixed eleven-page stdout-only copy audit. No project imports, programs or writes."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import hashlib
import json
import re
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
N = P/'verification/public-internal-narrative-trim-audit-sol-20261116'
R = P/'verification/public-internal-narrative-trim-stage-sol-20261116'
A = P/'verification/public-internal-narrative-audit-sol-20261116'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')

ADDITIONS = {
96: '<p>The <a href="focal_product_support.zip">support archive</a> also includes independent supplementary theta-series diagnostics. These floating-point checks are not validated numerical certification.</p>',
100: '<p>The <a href="outer-pedal-centroid-verification.zip">verification archive</a> includes exact symbolic and rational certificates and independent high-precision orbit controls. These checks supplement the written proof.</p>',
101: '<p>The <a href="cost-betti-source-and-verification.zip">supporting package</a> includes exact arithmetic and Fox-identity checks. These supplement the written proof.</p>',
104: '<p>The <a href="qss-self-duality-verification.zip">verification supplement</a> records the bounded source comparison and its access and version limitations.</p>',
105: '<p>The <a href="alternating-antimorphic-verification.zip">verification supplement</a> contains finite controls supporting the written proof and records the access and version gaps in the bounded source comparison.</p>',
106: '<p>The <a href="source-and-verification.zip">source package</a> includes an independent proof via positive definite bilinear slices and Cauchy–Schwarz, and a standard-library Python verifier with exact rational certificates. These finite checks supplement the analytic proof and do not formally verify the universal theorem.</p>'}
REMOVAL_TAGS = {
96: ('<details id="native-deposit-description">', '</details>'),
98: ('<details class="deposit-description">', '</details>'),
99: ('<section id="native-description">', '</section>'),
100: ('<details class="deposit-description">', '</details>'),
101: ('<section id="native-description">', '</section>'),
102: ('<section aria-labelledby="record-description">', '</section>'),
103: ('<h2>Original Zenodo record description</h2>\n<p id="record-description">', '</p>'),
104: ('<h2>Original Zenodo record description</h2>\n<div id="record-description">', '</div>'),
105: ('<h2>Original Zenodo record description</h2>\n<p id="record-description">', '</p>'),
106: ('<h2>Original Zenodo record description</h2>\n<div id="record-description">', '</div>'),
107: ('  <section aria-labelledby="description-heading">', '  </section>')}
ABSTRACTS = {96:[('section','abstract')],98:[('p','printed-abstract')],
99:[('section','printed-main-abstract'),('section','printed-companion-abstract')],
100:[('p','printed-abstract')],101:[('section','printed-abstract')],
102:[('p','printed-abstract')],103:[('p','original-abstract')],
104:[('p','original-abstract')],105:[('p','original-abstract')],
106:[('p','original-abstract')],107:[('section','original-abstract')]}

def fixed(path, row):
    assert not path.is_symlink(), str(path)
    data = path.read_bytes()
    assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['SHA256'], str(path)
    if 'mode' in row:
        assert stat.S_IMODE(path.stat().st_mode) == row['mode'], str(path)
    return data

def load(path):
    return json.loads(path.read_bytes())

def one(text, pattern):
    hits = re.findall(pattern, text)
    assert len(hits) == 1, pattern
    return hits[0]

class Tags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.hrefs, self.srcs, self.downloads, self.labels = [], [], [], [], []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'id' in d: self.ids.append(d['id'])
        if 'href' in d: self.hrefs.append(d['href'])
        if 'src' in d: self.srcs.append(d['src'])
        if 'download' in d: self.downloads.append((tag,d.get('href'),d['download']))
        self.labels.extend(d.get('aria-labelledby','').split())

def main():
    intake = json.loads(fixed(N/'INTAKE.json', {'bytes':19668,'SHA256':'6e8d385b04ae382bad5b76338c1174c755e2d016d6aa430263302e8b3b113072'}))
    final = json.loads(fixed(R/'FINAL.json', {'bytes':2712,'SHA256':'e7c56051bdf1e6ae7d999723940364633e52f287928ae1fc59a823bafb0d4685'}))
    manifest = json.loads(fixed(R/'MANIFEST.json', {'bytes':4627,'SHA256':'da77c17f4fe4f3e7c51fedf4432aa470245b1347178fc33cbd255135562345f2'}))
    assert {str(q.relative_to(R)) for q in R.rglob('*') if q.is_file()} == {x['path'] for x in manifest['files']}|{'FINAL.json','MANIFEST.json'}
    assert sorted(str(q.relative_to(R)) for q in R.rglob('*') if q.is_dir()) == manifest['directories']
    assert len(manifest['files'])+2 == 19 and len(manifest['directories']) == 14
    assert not any(q.is_symlink() for q in R.rglob('*'))
    for row in manifest['files']: fixed(R/row['path'],row)
    oldfinal = json.loads(fixed(A/'FINAL.json', final['source_audit_final']))
    for name in ('REPORT.md','CANDIDATES.json','ARTICLE_INVENTORY.json'):
        row = next(x for x in oldfinal['payload'] if x['path']==name)
        fixed(A/name,row)
    frozen = {x['position']:x for x in load(A/'ARTICLE_INVENTORY.json')['articles']}
    recommendations = {x['position']:x for x in load(A/'CANDIDATES.json')['candidate_descriptions']}
    guards = load(R/'SOURCE_GUARDS.json')['sources']
    edits = load(R/'EDITS.json')['records']
    assert len(edits) == len(guards) == len(intake['article_sources']) == 11
    assert {x['position'] for x in edits} == set(REMOVAL_TAGS) == set(recommendations)
    candidate_files = sorted(str(q.relative_to(R)) for q in (R/'candidate').rglob('*') if q.is_file())
    assert candidate_files == sorted(x['candidate_path'] for x in edits)
    results = []
    removed_id_count = 0
    for entry in edits:
        pos = entry['position']; source = entry['source']
        guard = next(x for x in guards if x['position']==pos)
        assert source == guard == next(x for x in intake['article_sources'] if x['position']==pos)
        assert all(source[k] == frozen[pos][k] for k in ('position','path','url','bytes','SHA256'))
        old_bytes = fixed(Path(source['path']),source)
        old = old_bytes.decode('utf-8')
        relative = str(Path(source['path']).relative_to(W))
        assert entry['candidate_path'] == 'candidate/'+relative
        new_bytes = (R/entry['candidate_path']).read_bytes(); new = new_bytes.decode('utf-8')
        changed = old
        kinds = []
        for operation in entry['operations']:
            kind = operation['kind']; before = operation['old']; after = operation['new']
            assert changed.count(before) == 1
            if kind == 'remove-duplicate-native-description':
                start,end = REMOVAL_TAGS[pos]
                assert before.startswith(start) and before.endswith(end) and after == ''
            elif kind == 'retain-unique-support-or-access-limit':
                assert pos in ADDITIONS and after == ADDITIONS[pos]+'\n'+before
            elif kind == 'condense-archival-caption':
                assert pos == 107
                assert before == 'Its statements about reviews pending as of that date are part of the deposited edition.'
                assert after == 'Its pending-review wording belongs to that archived edition.'
            else:
                raise AssertionError(kind)
            kinds.append(kind)
            changed = changed.replace(before,after,1)
        expected_kinds = ['remove-duplicate-native-description']
        if pos in ADDITIONS: expected_kinds += ['retain-unique-support-or-access-limit']
        if pos == 107: expected_kinds += ['condense-archival-caption']
        assert kinds == expected_kinds and changed.encode('utf-8') == new_bytes
        assert one(old,r'<head>[\s\S]*?</head>') == one(new,r'<head>[\s\S]*?</head>')
        for tag,ident in ABSTRACTS[pos]:
            pattern = '<'+tag+' id="'+ident+r'"[^>]*>[\s\S]*?</'+tag+'>'
            assert one(old,pattern) == one(new,pattern)
        a = Tags(); a.feed(old); b = Tags(); b.feed(new)
        assert len(b.ids) == len(set(b.ids)) and set(b.ids) <= set(a.ids)
        assert set(a.hrefs) == set(b.hrefs) and a.srcs == b.srcs and a.downloads == b.downloads
        assert set(b.labels) <= set(b.ids)
        removed = sorted(set(a.ids)-set(b.ids)); removed_id_count += len(removed)
        for href in a.hrefs:
            if href.startswith('#'): assert href[1:] not in removed
        for href in b.hrefs:
            target = urlsplit(href)
            if not target.path and not target.netloc and target.fragment:
                assert target.fragment in b.ids
        assert 'Original Zenodo description' not in new and 'Original Zenodo deposit description' not in new and 'Zenodo record description' not in new
        if pos == 107:
            assert 'Version 1.0 preparation candidate, 14 October 2026 UTC.' in new
            assert 'pending-review wording belongs to that archived edition' in new
            assert 'deposit was created on 17 October 2026 UTC' in new
        results.append({'position':pos,'path':relative,'source':{'bytes':len(old_bytes),'SHA256':hashlib.sha256(old_bytes).hexdigest()},'draft':{'bytes':len(new_bytes),'SHA256':hashlib.sha256(new_bytes).hexdigest()},'operations':kinds,'removed_ids':removed,'heads_full_abstracts_downloads_srcs_and_href_target_set_unchanged':True,'all_other_bytes_exact':True})
    assert removed_id_count == 13
    assert len(intake['linked_asset_initial_pins']) == 42
    for relative,row in intake['linked_asset_initial_pins'].items():
        assert Path(row['path']) == W/relative
        fixed(W/relative,row)
    assert final['publication_authority'] is False and final['deployment'] is False
    print(json.dumps({'status':'PASS_INDEPENDENT_ELEVEN_PAGE_COPY_FIDELITY','writer_packet_files':19,'writer_child_directories':14,'candidate_HTML_files':11,'description_removals':11,'support_or_access_relocations':6,'archival_caption_condensations':1,'removed_description_ids':removed_id_count,'current_article_sources_match_frozen_guards':True,'linked_non_HTML_assets_unchanged_since_own_intake':42,'whole_heads_full_printed_abstracts_downloads_and_asset_links_preserved':True,'all_remaining_bytes_outside_documented_edits_exact':True,'records':results,'whole_site_HEAD_index_lease_applied':False,'scientific_review_native_browser_render_network_Git_Sheet_mutations':False,'publication_authority':False},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
