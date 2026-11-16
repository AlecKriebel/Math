#!/usr/bin/env python3
"""Default read-only original/copy/finite-namespace closure; no science replay.

Reads pinned original source, peer, root, core and prior custody inputs as well
as this owned packet. No project imports, network, subprocesses or writes.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import stat

E = Path(__file__).absolute().parent
INITIAL_SHA = '10fd0351a82db4b23b75d0eeb301cad2b58e018e30e4504a84d4a3503a4556db'
AUTHORING_SHA = '14662620c5119b64c48516ada7012fed08d0f7615bf9863f0abac59bef41bf86'
checks = 0
typed_nodes = 0
allowed = {}

def need(ok, why):
    global checks
    checks += 1
    if not ok:
        raise ValueError(why)

def pin(body):
    return {'bytes':len(body), 'SHA256':hashlib.sha256(body).hexdigest()}

def read(path):
    path = Path(path)
    need(path.is_absolute() and '..' not in path.parts, 'noncanonical input')
    need(path.is_relative_to(E) or str(path) in allowed, 'unbound original input')
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode), 'not ordinary file')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        held = os.fstat(fd)
        need((before.st_dev,before.st_ino) == (held.st_dev,held.st_ino), 'open identity')
        parts = []
        while True:
            part = os.read(fd,1048576)
            if not part:
                break
            parts.append(part)
        after = os.fstat(fd)
        need((held.st_size,held.st_mtime_ns,held.st_ctime_ns) == (after.st_size,after.st_mtime_ns,after.st_ctime_ns), 'file changed')
        final = path.lstat()
        need((final.st_dev,final.st_ino) == (held.st_dev,held.st_ino), 'pathname identity')
        body = b''.join(parts)
        need(len(body) == held.st_size, 'short read')
        if str(path) in allowed:
            need(pin(body) == allowed[str(path)], 'original whole-byte pin')
        return body
    finally:
        os.close(fd)

def obj(path):
    return json.loads(read(path))

def typed(a,b,p='$'):
    global typed_nodes
    typed_nodes += 1
    need(type(a) is type(b), 'type '+p)
    if type(a) is dict:
        need(list(a) == list(b), 'key/order '+p)
        for k in a:
            typed(a[k],b[k],p+'/'+k)
    elif type(a) is list:
        need(len(a) == len(b), 'length '+p)
        for i,(x,y) in enumerate(zip(a,b)):
            typed(x,y,p+'/'+str(i))
    else:
        need(a == b, 'literal '+p)

def scan(root,expected=None):
    need(stat.S_ISDIR(root.lstat().st_mode), 'not ordinary directory')
    allowed_files = None if expected is None else {r['path'] for r in expected['files']}
    allowed_dirs = None if expected is None else set(expected['directories'])
    files,dirs = [],[]
    def visit(path):
        before = path.lstat()
        with os.scandir(path) as it:
            entries = sorted(it,key=lambda x:x.name)
        for entry in entries:
            q = path/entry.name; rel = q.relative_to(root).as_posix(); mode = q.lstat().st_mode
            if stat.S_ISDIR(mode):
                need(allowed_dirs is None or rel in allowed_dirs, 'unlisted directory')
                dirs.append(rel); visit(q)
            elif stat.S_ISREG(mode):
                need(allowed_files is None or rel in allowed_files, 'unlisted file')
                files.append({'path':rel, **pin(read(q))})
            else:
                raise ValueError('symlink/FIFO/special '+rel)
        after = path.lstat()
        need((before.st_dev,before.st_ino,before.st_mtime_ns,before.st_ctime_ns) == (after.st_dev,after.st_ino,after.st_mtime_ns,after.st_ctime_ns), 'directory changed')
    visit(root)
    result = {'root':str(root),'files':sorted(files,key=lambda r:r['path']),'directories':sorted(dirs)}
    if expected is not None:
        typed(result,expected)
    return result

class Doc(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.attrs=[]; self.ids=[]; self.paragraphs={}; self.capture=None
    def handle_starttag(self,tag,attrs):
        d=dict(attrs); self.attrs.append((tag,d))
        if 'id' in d:
            self.ids.append(d['id'])
        if tag=='p' and d.get('id') in ('printed-abstract','native-description'):
            self.capture=d['id']; self.paragraphs[self.capture]=''
    def handle_endtag(self,tag):
        if tag=='p':
            self.capture=None
    def handle_data(self,data):
        if self.capture is not None:
            self.paragraphs[self.capture]+=data

def guard_main(body,initial):
    doc=Doc(); doc.feed(body); doc.close()
    need(doc.paragraphs['printed-abstract']==initial['full_printed_abstract_readable_math_transcription'],'entire printed abstract and mathematical notation')
    need(doc.paragraphs['native-description']==initial['entire_native_description_distinct_original_string'],'entire separate native description')
    required=[
        'it rejects every word whose length is not divisible by h²',
        'It accepts ε.', 'Nₕ = (3h³−h)/2 + 2 marked states',
        'ordinary epsilon-free 1NFA: Nₕ−1 states.',
        'h³ lower bound for ordinary one-way NFAs and for marked right-only sources',
        'not a cut-state lower bound for arbitrary two-way machines',
        'exact state count is sh²', 'positive finite acceptance',
        '2^(⌊(h−2)/31⌋) ≤ 4(sh²+2)²',
        '2^(⌊(h−2)/127⌋) ≤ 2(sh²+1)',
        'complement of Kₕ in all binary words', 'ε is absent from both complements',
        '2^(⌊(h−2)/127⌋) ≤ 2((s+1)h²+1)',
        '2^{Ω(h)} = 2^{Ω(Nₕ^(1/3))}', 'does not assert 2^{Ω(Nₕ)}',
        'self-reported, source-only context', 'October 2011 author preprint',
        'connectivity-chain ceiling is proved as Theorem 2',
        'Theorem 1 with its proof deferred', 'may rewrite cells',
        'adc7f1241b42e322a6451854ab7e4b4c146bf78a',
        'not an independent proof of the upstream exponential obstructions',
        'AI tools were used extensively', 'unrefereed preprint',
        'credit should reflect actual work', 'Creative Commons Attribution 4.0 International']
    for s in required:
        need(s in body,'copy loss '+s)
    need(len(doc.ids)==len(set(doc.ids)) and 'main' in doc.ids,'unique semantic IDs')
    frames=[d for t,d in doc.attrs if t=='iframe']
    need(len(frames)==1 and frames[0].get('src')=='paper.pdf#view=FitH' and bool(frames[0].get('title')),'titled FitH reader')
    need(body.index('<iframe')<body.index('<h2 id="abstract">'),'upfront reader')
    need(not re.search(r'mailto:|tel:|<form|<input|<button|<script|2026-11-15|57,795|398-byte|Theorem 2\.1',body,re.I),'no contact/internal dated counts/wrong locator')
    return doc

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--preseal',action='store_true',help='input/copy checks only, not final owned-namespace closure')
    args=ap.parse_args()
    ib=read(E/'INITIAL_SEAL.json'); need(pin(ib)['SHA256']==INITIAL_SHA,'immutable initial')
    initial_seal=json.loads(ib)
    for r in initial_seal['files']:
        need(pin(read(E/r['path']))=={k:r[k] for k in ['bytes','SHA256']},'initial payload unchanged')
    initial=obj(E/'INITIAL_EXPECTATIONS.json')
    ab=read(E/'AUTHORING_INPUTS_SEAL.json'); need(pin(ab)['SHA256']==AUTHORING_SHA,'authoring seal')
    authoring=json.loads(ab)
    for r in authoring['inputs']:
        need(pin(read(E/r['path']))=={k:r[k] for k in ['bytes','SHA256']},'whole authoring input')
    sb=read(E/'SOURCE_INPUTS.json')
    need(pin(sb)=={k:next(r for r in authoring['inputs'] if r['path']=='SOURCE_INPUTS.json')[k] for k in ['bytes','SHA256']},'same-buffer source input')
    source=json.loads(sb)
    for ns in source['complete_immutable_namespaces']:
        for r in ns['files']:
            allowed[str(Path(ns['root'])/r['path'])]={k:r[k] for k in ['bytes','SHA256']}
    for r in source['qualified_core17_plus_sole405b_sources']+[source['root_authority_binding']]:
        allowed[r['path']]={k:r[k] for k in ['bytes','SHA256']}
    for ns in source['complete_immutable_namespaces']:
        scan(Path(ns['root']),ns)
    for r in source['qualified_core17_plus_sole405b_sources']:
        read(Path(r['path']))
    authority=obj(Path(source['root_authority_binding']['path']))
    typed(authority,source['whole_root_authority'])
    ready=obj(E.parents[1]/'sources/SOURCE_READY.json')
    typed(ready,source['whole_original_SOURCE_READY']); typed(ready,authority['wholeOriginalSourceReady'])
    record=obj(Path(ready['whole_native_API_objects'][0]['path']))
    need('version' not in record['metadata'] and ready['native_version_whole_field']=={'present':False,'original_value':None},'native version absent not null-present')
    need(authority['nativeCurrentScienceDispositions']==106 and authority['nativeTrackerTransitionPending'] is True,'immutable historical native context')
    need(authority['fullEditorialCopyConfigCodeAdopted'] is False and authority['productionInstallationAuthorized'] is False,'separate adoption/install authority')
    cfg=obj(E/'EDITORIAL_CONFIG.json')
    typed(cfg['publication']['native_version_field'],ready['native_version_whole_field'])
    need(cfg['publication']['printed_version_present'] is False and cfg['publication']['printed_version'] is None,'printed version none')
    need(cfg['publication']['datePublished']=='2026-10-06' and cfg['publication']['native_created_separate']=='2026-10-07T04:34:37.920372+00:00','publication versus creation')
    for k in ['root_copy_adopted','production_install_authority','deployment_authority','native_tracker_mutation_authority','live_verified','browser_verified']:
        need(cfg['promotion'][k] is False,'private false '+k)
    for k in ['canonical_url','AA','follow_up']:
        need(cfg['promotion'][k] is None,'private null '+k)
    body=read(E/'PUBLIC_MAIN.html').decode(); doc=guard_main(body,initial)
    tex=read(Path(ready['controlling_TeX']['extracted_path'])).decode()
    raw_abstract=re.search(r'\\begin\{abstract\}\n(.*?)\\end\{abstract\}',tex,re.S).group(1)
    need(raw_abstract==initial['full_printed_abstract_original_TeX'],'whole original TeX abstract')
    need(doc.paragraphs['native-description']==record['metadata']['description'],'native description exact record value')
    need(doc.paragraphs['printed-abstract']!=doc.paragraphs['native-description'],'distinct original abstracts')
    negatives=0
    for old,new in [('2^{Ω(Nₕ^(1/3))}','2^{Ω(Nₕ)}'),
                    ('it rejects every word whose length is not divisible by h²','it accepts every word whose length is not divisible by h²'),
                    ('complement of Kₕ in all binary words','complement of Kₕ in well-formed binary words only'),
                    ('h³ lower bound for ordinary one-way NFAs and for marked right-only sources','h³ lower bound for arbitrary two-way NFAs')]:
        need(old in body,'actual mutation target')
        try:
            guard_main(body.replace(old,new),initial)
        except ValueError:
            negatives+=1
        else:
            raise ValueError('critical copy-loss mutation escaped')
    need(negatives==4,'four selected in-memory copy losses rejected')
    names=sorted(authoring['output_file_names'])
    need(sorted(p.name for p in (E/'candidate').iterdir())==names,'exact ten candidate leaves')
    need(sorted(p.name for p in (E/'optimized-candidate').iterdir())==names,'exact ten optimized leaves')
    for n in names:
        need(read(E/'candidate'/n)==read(E/'optimized-candidate'/n),'whole normal/optimized output')
    need(read(E/'candidate/PUBLIC_MAIN.html')==body.encode(),'zero MAIN transformation')
    page=read(E/'candidate/index.html').decode(); head=read(E/'candidate/PUBLIC_HEAD.html').decode()
    need(page.count(body)==1 and head in page,'complete actual head and MAIN in page')
    need('font-family:Arial,Helvetica,sans-serif' in page and 'background:#fff' in page and '@media(max-width:600px)' in page,'light responsive Arial style')
    need('noindex,nofollow,noarchive' in head and 'rel="canonical"' not in head,'private head without installed canonical')
    ld=obj(E/'candidate/SCHOLARLY_METADATA.json')
    inline=json.loads(head.split('<script type="application/ld+json">',1)[1].split('</script>',1)[0]); typed(ld,inline)
    need('version' not in ld and ld['abstract']==initial['full_printed_abstract_readable_math_transcription'] and ld['datePublished']=='2026-10-06','full scholarly abstract and absent version')
    need(ld['license']=='https://creativecommons.org/licenses/by/4.0/','broad authored rights')
    bib=read(E/'candidate/citation.bib').decode()
    need(not re.search(r'\bversion\s*=',bib,re.I) and 'day = {6}' in bib,'no invented Bib version/date')
    for asset,encoding in zip(ready['all_native_assets_in_original_order'],ld['encoding']):
        name=asset['original_api_file_object']['key']
        need(read(E/'candidate'/name)==read(Path(asset['path'])),'whole native asset unchanged')
        need(encoding['contentUrl'].endswith('/'+name),'native scholarly encoding order')
    need(len(ld['encoding'])==4 and ready['whole_regular_payload_occurrences']==28,'whole native asset/archive extent')
    for tag,d in doc.attrs:
        if tag=='a' and 'href' in d and not d['href'].startswith(('https://','#')):
            need(d['href'] in names,'local link target')
    for mode in ['normal','optimized']:
        receipt=obj(E/('RENDER-'+mode+'.stdout'))
        need(receipt['mode']==mode and receipt['assertions_enabled'] is (mode=='normal'),'actual distinct runtime stream')
        need(read(E/('RENDER-'+mode+'.stderr'))==b'','empty renderer stderr')
        for name,p in receipt['whole_buffers'].items():
            need(pin(read(E/receipt['directory']/name))==p,'whole output receipt pin')
    if not args.preseal:
        seal=obj(E/'FINAL_SEAL.json'); mb=read(E/'OWNED_MANIFEST.json')
        need(pin(mb)==seal['manifest'],'same-buffer final manifest')
        manifest=json.loads(mb); current=scan(E)
        terms={'OWNED_MANIFEST.json','FINAL_SEAL.json'}
        need(terms <= {r['path'] for r in current['files']},'exact own root terminals')
        current['files']=[r for r in current['files'] if r['path'] not in terms]
        typed(current['files'],manifest['files']); typed(current['directories'],manifest['directories'])
        need(manifest['exact_root_terminal_exclusions']==sorted(terms) and manifest['subtree_or_future_exclusions']==[],'no runtime/future carveouts')
        need(seal['publication_authority'] is False and seal['root_copy_adopted'] is False and seal['AA'] is None,'neutral final authority')
    print(json.dumps({'status':'PRIVATE_EDITORIAL_COPY_CUSTODY_PASSED','mode':'ordinary' if __debug__ else 'optimized-O',
        'strict_final_namespace':not args.preseal,'checks':checks,'typed_nodes':typed_nodes,
        'whole_paired_output_buffers':10,'native_assets_unchanged':4,'selected_copy_loss_rejections':negatives,
        'original_namespaces':[[len(ns['files']),len(ns['directories'])] for ns in source['complete_immutable_namespaces']],
        'scientific_execution':False,'publication_authority':False,'root_copy_adopted':False,'canonical_url':None,'AA':None},sort_keys=True))

if __name__=='__main__':
    main()
