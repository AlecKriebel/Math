"""Read-only verification of this bounded public-Git-docs legacy preflight.

Reads Git objects and the existing complete PDF extracts; does not extract PDFs,
contact a remote, update the Git index/refs, or write any file. Future publication
or local changes do not alter the historical before/after evidence.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, os, re, subprocess, unicodedata

O = Path(__file__).resolve().parent
P = O.parent.parent
R = P.parent
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1')

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def load(path):
    return json.loads(path.read_text())

def digest(data):
    return hashlib.sha256(data).hexdigest()

def binding(path):
    data = path.read_bytes()
    return dict(bytes=len(data), sha256=digest(data))

def git(*args):
    return subprocess.run(['git', *args], cwd=R, env=ENV, capture_output=True,
                          check=True, timeout=45).stdout

def normalize(text):
    text = unicodedata.normalize('NFKC', text).replace('\u00ad', '').replace('’', "'").replace('‘', "'")
    text = ''.join(c for c in unicodedata.normalize('NFKD',text) if not unicodedata.combining(c))
    text = re.sub(r'(?<=\w)-\s*\n\s*(?=\w)', '', text)
    text = re.sub('[‐‑‒–—−]', '-', text)
    return re.sub(r'\s+', ' ', text).casefold()

class Visible(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.skip += 1
        if tag in ['p', 'h1', 'h2', 'h3', 'li', 'div', 'section', 'br']:
            self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.skip -= 1
    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

def main():
    seal_path = O/'FINAL_SEAL.json'
    manifest_checked = False
    if seal_path.exists():
        seal = load(seal_path)
        manifest = load(O/'FINAL_MANIFEST.json')
        need(digest((O/'FINAL_MANIFEST.json').read_bytes()) == seal['manifest_sha256'],
             'Manifest is not sealed')
        actual = {str(p.relative_to(O)) for p in O.rglob('*') if p.is_file()
                  and p.name not in ['FINAL_MANIFEST.json', 'FINAL_SEAL.json']}
        need(actual == {x['path'] for x in manifest['files']}, 'Owned file inventory changed')
        for item in manifest['files']:
            need(binding(O/item['path']) == {k:item[k] for k in ['bytes','sha256']},
                 'Owned binding changed: '+item['path'])
        manifest_checked = True

    protected = load(O/'PROTECTED_INPUTS.json')['bindings']
    for path, expected in protected.items():
        need(binding(Path(path)) == expected, 'Protected original changed: '+path)
    old = P/'redirects/mtp2-preflight-sol-20261025'
    ban = old
    for folder in [old]:
        need(digest((folder/'FINAL_MANIFEST.json').read_bytes()) ==
             load(folder/'FINAL_SEAL.json')['manifest_sha256'], 'Prior seal changed')

    pin = load(O/'REMOTE_PIN.json')
    close = load(O/'REMOTE_CLOSING.json')
    need(pin['commit'] == close['commit'] == '83a46fd681e68ee1a3cab835d65053820703d77f',
         'Different historical remote pins')
    need(pin['docs_tree'] == close['docs_tree'] == '7a24ec1dcb73a5e06ba82ff9cccda54e73f9deec',
         'Different historical public docs trees')
    need((O/'remote-main.raw.txt').read_text() == pin['actual_output'] and
         (O/'remote-main-closing.raw.txt').read_text() == close['actual_output'], 'Advertisement mismatch')
    for kind, oid in [('commit',pin['commit']), ('tree',pin['root_tree']), ('tree',pin['docs_tree'])]:
        data = (O/('git-object-'+oid+'.raw')).read_bytes()
        need(hashlib.sha1((kind+' '+str(len(data))+'\0').encode()+data).hexdigest() == oid,
             'Historical Git object identity')
        need(data == git('cat-file',kind,oid), 'Actual historical Git object differs')
    listing = git('ls-tree','-r','-l','-z',pin['commit'],'--','docs')
    need(listing == (O/'docs-tree.raw.z').read_bytes(), 'Docs inventory differs')
    rows = load(O/'DOCS_OBJECT_BINDINGS.json')
    need(rows == load(ban/'DOCS_OBJECT_BINDINGS.json'), 'Prior complete inventory differs')
    decoded = []
    for item in listing.rstrip(b'\0').split(b'\0'):
        fields, path = item.split(b'\t',1)
        mode, kind, oid, size = fields.decode().split()
        decoded.append(dict(path=path.decode(),mode=mode,kind=kind,blob=oid,bytes=int(size)))
    need([{k:x[k] for k in ['path','mode','kind','blob','bytes']} for x in rows] == decoded,
         'Parsed tree does not match complete inventory')
    reused = load(O/'REUSED_EXTRACT_BINDINGS.json')
    pdfs = {x['public_path']:x for x in reused}
    need(len(rows) == 254 and len(pdfs) == 76 and sum(x['pages'] for x in reused) == 854,
         'Corpus coverage differs')
    for item in reused:
        need(binding(Path(item['path'])) == {k:item[k] for k in ['bytes','sha256']},
             'Reused extract changed: '+item['public_path'])

    targets = load(O/'TARGET_IDENTITIES.json')
    target_hashes = {h for x in targets.values() for h in x['source_asset_hashes']}
    for ident, item in targets.items():
        need(item['whole_original_source_ready'] == load(P/'papers'/ident/'sources/SOURCE_READY.json'), 'Whole target source identity')
    representatives = []
    hash_matches = []
    proc = subprocess.Popen(['git','cat-file','--batch'],cwd=R,env=ENV,
                            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    proc.stdin.write(('\n'.join(x['blob'] for x in rows)+'\n').encode())
    proc.stdin.close()
    for row in rows:
        need(proc.stdout.readline().decode().split() == [row['blob'],'blob',str(row['bytes'])],
             'Batch object header')
        data = proc.stdout.read(row['bytes'])
        need(proc.stdout.read(1) == b'\n', 'Batch object framing')
        need(digest(data) == row['sha256'] and
             hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest() == row['blob'],
             'Actual public blob differs: '+row['path'])
        if digest(data) in target_hashes:
            hash_matches.append(row['path'])
        if row['path'].lower().endswith('.pdf'):
            item = pdfs[row['path']]
            need(item['pdf_blob'] == row['blob'] and item['pdf_sha256'] == digest(data),
                 'PDF/extract source mismatch')
            representatives.append(dict(path=row['path'],kind='complete_reused_PDF_text',
                                        text=Path(item['path']).read_text()))
        else:
            try:
                text = data.decode('utf8')
            except UnicodeDecodeError:
                continue
            if '\0' in text:
                continue
            representatives.append(dict(path=row['path'],kind='raw_UTF8_blob',text=text))
            if row['path'].lower().endswith('.html'):
                parser = Visible()
                parser.feed(text)
                representatives.append(dict(path=row['path'],kind='decoded_visible_HTML',
                                            text=''.join(parser.parts)))
    need(proc.wait(timeout=30) == 0 and not proc.stderr.read(), 'Git batch failed')
    saved = load(O/'SEARCH_RESULTS.json')
    replay = []
    for item in representatives:
        text = normalize(item['text'])
        groups = {}
        for group, patterns in saved['queries'].items():
            hits = []
            for pattern in patterns:
                for match in re.finditer(pattern,text):
                    hits.append(dict(pattern=pattern,match=match.group(),
                                     context=text[max(0,match.start()-150):match.end()+250]))
            groups[group] = hits
        replay.append(dict(path=item['path'],kind=item['kind'],normalized_characters=len(text),groups=groups))
    need(replay == saved['representations'] and len(replay) == 260, 'Search replay differs')
    need(hash_matches == saved['exact_asset_hash_matches'] == [], 'Exact asset identity match')
    counts = {g:sum(bool(x['groups'][g]) for x in replay) for g in saved['queries']}
    need(counts == {'106_record_or_DOI':0,'106_exact_title':0,'106_distinctive_terms':0,'106_broad_context':2,
                    '107_record_or_DOI':0,'107_exact_title':0,'107_distinctive_terms':0,'107_broad_context':0},
         'Different search results')
    candidates = {x['path'] for x in replay if any(x['groups'].values())}
    exclusions = load(O/'EXCLUSIONS.json')['candidates']
    need(candidates == {x['path'] for x in exclusions} and len(candidates) == 2,
         'Missing candidate exclusion')
    need(all(x['identity_match_to_23124601'] is False and x['identity_match_to_23333046'] is False for x in exclusions), 'Unresolved positive candidate')
    controls = load(O/'QUERY_CONTROLS.json')
    need(len(controls['controls']) == 6 and all(x['pass_'] for x in controls['controls']),
         'Positive query controls failed')
    recalculated = []
    for ident, item in targets.items():
        text_entry = item['positive_control_full_reader_text']
        need(binding(Path(text_entry['path'])) == {k:text_entry[k] for k in ['bytes','sha256']},
             'Sealed comparison-reader text changed')
        recalculated.append(dict(name=ident+' actual complete title',
                                 pass_=normalize(item['whole_original_source_ready']['title']) in
                                 normalize(Path(text_entry['path']).read_text())))
    recalculated += [
        dict(name='known public positive-recurrence phrase',
             pass_=any('positive recurrence for single-linkage bimolecular' in normalize(x['text'])
                       for x in representatives)),
        dict(name='curly apostrophe and subscript',pass_=normalize('Wajnryb’s Artin A₅') == normalize("Wajnryb's Artin A5")),
        dict(name='accented versus ASCII devissage',pass_=normalize('dévissage') == normalize('devissage')),
        dict(name='soft hyphen/ligature/line wrap',pass_=normalize('ﬁxed non\u00adnegative\nwords') == normalize('fixed nonnegative words'))]
    need(recalculated == controls['controls'], 'Recomputed positive controls differ')
    before = load(O/'LOCAL_BEFORE.json')
    for name in ['LOCAL_CLOSING.json']:
        after = load(O/name)
        need({k:v for k,v in before.items() if k!='utc'} ==
             {k:v for k,v in after.items() if k!='utc'}, 'Historical preservation differs')
    need(load(O/'PRESERVATION_RESULT.json')['all_equal'], 'Preservation result failed')
    for item in load(O/'CHECKPOINT_CHAIN.json')['actual_read_only_deltas']:
        need(git('rev-parse',item['commit']+'^').decode().strip()==item['parent'],'Checkpoint ancestry')
        raw=git('diff','--no-renames','--name-only',item['parent'],item['commit'])
        need(raw==(O/('checkpoint-'+item['commit']+'-paths.raw.txt')).read_bytes(),'Checkpoint exact changed paths')
        need(len(raw.decode().splitlines())==item['changed_paths'] and
             all(p.startswith('research_website_catalogue_20261024/') for p in raw.decode().splitlines()),
             'Checkpoint programme-only changes')
        need(git('rev-parse',item['commit']+':docs').decode().strip()==pin['docs_tree'],'Checkpoint docs preservation')
    verdict = load(O/'VERDICT.json')
    need(set(verdict['records'])=={'23124601','23333046'} and
         all(x['status']=='NO_MATCH_FOUND_IN_EXACT_PINNED_PUBLIC_DOCS_CORPUS' for x in verdict['records'].values()),
         'Two literal bounded record verdicts')
    need(verdict['status'] == 'NO_MATCH_FOUND_IN_EXACT_PINNED_PUBLIC_DOCS_CORPUS' and
         verdict['redirect_authorized'] is False and verdict['live_verification_performed'] is False,
         'Bounded disposition changed')
    return dict(status='PASS',manifest_checked=manifest_checked,protected_files=len(protected),
                actual_public_blobs=len(rows),complete_reused_PDFs=len(pdfs),PDF_pages=854,
                replayed_representations=len(replay),positive_controls=6,candidate_exclusions=2,
                historical_preservation=True,PDF_extractions=0,network_actions=0,writes=0)

if __name__ == '__main__':
    print(json.dumps(main(),indent=2))
