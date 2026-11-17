"""One passive fact-audit read; never execute or import producer/source code."""
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import stat
import traceback

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
WRITER = PROJECT / 'verification/riesz-surface-editorial-sol-20261117'
SOURCE = PROJECT / 'papers/23202994/sources'
ORIGINAL = SOURCE / 'archives/01-source-and-verification.zip.extracted/publication/main.tex'
ROOT_REVIEW = PROJECT / 'papers/23202994/reviews/root-continuation-20261117/ROOT_REVIEW.md'
CLEARANCE = PROJECT / 'verification/root-clearance-23202994-20261117.json'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def enc(obj):
    return (json.dumps(obj, indent=2, ensure_ascii=False) + '\n').encode()
def put(name, obj):
    with (HERE / name).open('xb') as out:
        out.write(enc(obj))
def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'md5': hashlib.md5(data).hexdigest(), 'mode': oct(stat.S_IMODE(path.lstat().st_mode))}
def snapshot(root):
    entries = []
    for path in [root, *sorted(root.rglob('*'))]:
        st = path.lstat()
        name = '.' if path == root else path.relative_to(root).as_posix()
        kind = 'directory' if stat.S_ISDIR(st.st_mode) else 'file' if stat.S_ISREG(st.st_mode) else 'other'
        assert kind != 'other', (root, name, kind)
        row = {'path': name, 'kind': kind, 'mode': oct(stat.S_IMODE(st.st_mode)),
               'hidden': any(p.startswith('.') and p not in ('.', '..') for p in Path(name).parts)}
        if kind == 'file':
            row.update(pin(path)); row['empty'] = row['bytes'] == 0
        else:
            row['empty'] = not any(path.iterdir())
        entries.append(row)
    return {'root': str(root), 'files': sum(x['kind'] == 'file' for x in entries),
            'child_directories': sum(x['kind'] == 'directory' for x in entries)-1, 'entries': entries}
def normalized(text):
    return ' '.join(text.split())

class ReadHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.metas=[]; self.links=[]; self.iframes=[]; self.styles=[]
        self.script=None; self.script_data=[]; self.scripts=[]
        self.inbody=False; self.instyle=False; self.visible=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag == 'meta': self.metas.append(a)
        if tag in ('a','link','base'): self.links.append({'tag':tag, **a})
        if tag == 'iframe': self.iframes.append(a)
        if tag == 'body': self.inbody=True
        if tag == 'style': self.instyle=True; self.styles.append(a)
        if tag == 'script': self.script=a; self.script_data=[]
    def handle_endtag(self, tag):
        if tag == 'script' and self.script is not None:
            self.scripts.append({'attributes':self.script, 'text':''.join(self.script_data)})
            self.script=None
        if tag == 'style': self.instyle=False
        if tag == 'body': self.inbody=False
    def handle_data(self, text):
        if self.script is not None: self.script_data.append(text)
        elif self.inbody and not self.instyle: self.visible.append(text)

try:
    assert not (HERE / 'BEFORE.json').exists(), 'one audit only; do not retry'
    before = {'UTC':utc(), 'SOURCE':snapshot(SOURCE), 'WRITER':snapshot(WRITER)}
    put('BEFORE.json', before)
    assert (before['SOURCE']['files'], before['SOURCE']['child_directories']) == (39,15)
    assert (before['WRITER']['files'], before['WRITER']['child_directories']) == (28,1)
    protected = {
        WRITER/'FINAL.json':'4d48b3304f6e1de25e53092ef489f9bb5f02259e26ad4c751df4146e16b5ef4d',
        WRITER/'MANIFEST.json':'13164254fa6596772435ad817efacf99ab035bf418a07d601687f44846b50db6',
        WRITER/'article.html':'3685e7c43c42d45743a22ed8d05c3cb2277bca1922162549cb348d67c610380e',
        ROOT_REVIEW:'6ade63069c5793ba730d1526876e3de34b88e0540b3dcff385c5890c31dd467f',
        CLEARANCE:'6631b8b7c7a5452b6f1867400f6f2d3bec454b100daf8f5b8bd54f620cfeb843',
        SOURCE/'SOURCE_MANIFEST.json':'7a6854f7ebb1caf7a0f26c5cb6014872ee0ce93f03414c3f48d965ff13c9a976',
        SOURCE/'SOURCE_FINAL.json':'d90fbadc2f49aa86904695ce60c2042eef4e6850f70d3972b5f48fdb8913c27e',
    }
    protected_rows=[]
    for path, expected in protected.items():
        actual=pin(path)
        assert actual['sha256'] == expected, ('protected pin failure', str(path), actual, expected)
        protected_rows.append({'path':str(path), **actual})
    assert pin(ROOT_REVIEW)['bytes'] == 15870
    put('PROTECTED_PINS.json', protected_rows)
    final=json.loads((WRITER/'FINAL.json').read_text())
    manifest=json.loads((WRITER/'MANIFEST.json').read_text())
    actual_names={x['path'] for x in before['WRITER']['entries'] if x['kind']=='file'}
    payload_names={x['path'] for x in manifest['payload_files']}
    assert payload_names | {'MANIFEST.json','FINAL.json'} == actual_names
    for record in manifest['payload_files']:
        actual=pin(WRITER/record['path'])
        assert (actual['bytes'],actual['sha256'],actual['mode']) == (record['bytes'],record['SHA256'],record['mode']), record
    article=(WRITER/'article.html').read_text()
    main=(WRITER/'main.html').read_text()
    head=(WRITER/'head.html').read_text()
    model=json.loads((WRITER/'page-model.json').read_text())
    api=json.loads((SOURCE/'native-metadata/record-api.json').read_text())
    original=ORIGINAL.read_text()
    clearance=json.loads(CLEARANCE.read_text())
    reader=ReadHTML();reader.feed(article);reader.close()
    schemas=[json.loads(x['text']) for x in reader.scripts if x['attributes'].get('type')=='application/ld+json']
    abstract_tex=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',original,re.S).group(1)
    expected=normalized(abstract_tex)
    for a,b in [('$s>2$','s>2'),('$N^{1-s/2}$','N^(1−s/2)'),('Hardin--Saff','Hardin–Saff')]:
        expected=expected.replace(a,b)
    visible=normalized(''.join(reader.visible))
    dc=[x.get('content') for x in reader.metas if (x.get('name') or '').lower() in ('dcterms.abstract','dc.description')]
    abstract_source=json.loads((WRITER/'ABSTRACT_SOURCE.json').read_text())
    assets=[]
    for source_asset, prepared in zip(api['files'],model['native_asset_order']):
        native=SOURCE/'zenodo-files'/source_asset['key']
        copy=WRITER/prepared['local_path']
        a,b=pin(native),pin(copy)
        assert a==b, ('native asset mismatch',str(native),a,b)
        assert 'md5:'+a['md5']==source_asset['checksum']
        assets.append({'native_name':source_asset['key'],'native_order':len(assets)+1,
            'source_path':str(native),'prepared_path':str(copy),'identity':a,'native_metadata':source_asset})
    assert len(api['files'])==len(model['native_asset_order'])==len(assets)==2
    css=json.loads((WRITER/'COLLISION_AND_CSS.json').read_text())
    facts={'UTC':utc(),'protected_pins_match':True,'writer_manifest_complete_match':True,
        'native_metadata':api['metadata'],'native_created':api.get('created'),'native_updated':api.get('updated'),
        'clearance':clearance,'assets_in_original_order':assets,'expected_full_original_abstract':expected,
        'abstract_checks':{'source_tex_exact':abstract_source['native_abstract_tex']==abstract_tex,
            'model_exact':model['abstract']==expected,'abstract_txt_exact':(WRITER/'ABSTRACT.txt').read_text().strip()==expected,
            'visible_body_contains_full_abstract':expected in visible,'visible_body_full_abstract_occurrences':visible.count(expected),
            'DC_exact':expected in dc,'schema_exact':len(schemas)==1 and schemas[0].get('abstract')==expected},
        'article_metas':reader.metas,'article_links':reader.links,'article_iframes':reader.iframes,
        'script_attributes':[x['attributes'] for x in reader.scripts],'structured_data':schemas,
        'inline_style_elements':reader.styles,'visible_body_text':visible,
        'article_head_fragment_equals_saved_head':re.search(r'<head\b[^>]*>.*?</head>',article,re.S).group(0).strip()==head.strip(),
        'article_main_fragment_equals_saved_main':re.search(r'<main\b[^>]*>.*?</main>',article,re.S).group(0).strip()==main.strip(),
        'private_actual_fields':{k:model.get(k) for k in ['canonical_url','base_url','production_url','actual_publication_date','AA','publication_authority','robots']},
        'writer_stylesheet_guard_equal':css['stylesheet_before']==css['stylesheet_after'],
        'W_access_by_fact_audit':False,'new_scientific_runs':0,'producer_runs':0,'network_calls':0}
    put('DATA_FACTS.json',facts)
    with (HERE/'READING_PACKET.txt').open('x') as stream:
        for path in [WRITER/'article.html',WRITER/'head.html',WRITER/'main.html',WRITER/'main.template.html',
            WRITER/'page-model.json',WRITER/'citation.bib',WRITER/'ABSTRACT.txt',WRITER/'REPORT.md',
            ORIGINAL,SOURCE/'native-metadata/record-api.json',CLEARANCE,ROOT_REVIEW]:
            stream.write('\n===== '+str(path)+' =====\n'+path.read_text()+'\n')
    after={'UTC':utc(),'SOURCE':snapshot(SOURCE),'WRITER':snapshot(WRITER)}
    put('AFTER.json',after)
    assert before['SOURCE']==after['SOURCE'] and before['WRITER']==after['WRITER'], 'protected namespace changed'
    put('READ_ONCE_RECEIPT.json',{'UTC':utc(),'reader':pin(Path(__file__)),
        'complete_reader_personally_read_before_execution':True,'attempts':1,
        'source_exact':True,'writer_exact':True,'source_counts':[39,15],'writer_counts':[28,1],
        'scientific_runs':0,'producer_runs':0,'imports_of_project_code':0,'network':0,'W':0,
        'abstract_checks':facts['abstract_checks'],'manual_fact_verdict':'pending complete literal read'})
    print(json.dumps({'passive_read_complete':True,'source':[39,15],'writer':[28,1],
        'before_after_exact':True,'protected_pins_match':True,'abstract_checks':facts['abstract_checks']}))
except Exception:
    with (HERE/'LITERAL_FAILURE.txt').open('x') as stream:
        stream.write(utc()+'\n'+traceback.format_exc())
    raise
