"""Passive byte/topology/metadata custody only; no mathematical execution."""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib, json, os, stat, sys, zipfile

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S=P/'papers/23204176/sources'
A=P/'papers/23204176/reviews/adversarial-sol'
ADOPT=P/'verification/root-source190191-custody-adoption-20261117.json'
phase=sys.argv[1]
if phase not in ['before','after']:raise ValueError('Only before/after custody')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(root):
    rows=[]
    for p in [root]+sorted(root.rglob('*')):
        s=p.lstat();r={'path':str(p.relative_to(root)),'mode_octal':oct(stat.S_IMODE(s.st_mode))}
        if stat.S_ISREG(s.st_mode):
            b=p.read_bytes();r.update(kind='file',bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),md5=hashlib.md5(b).hexdigest())
        elif stat.S_ISDIR(s.st_mode):r.update(kind='directory',empty=not any(p.iterdir()))
        elif stat.S_ISLNK(s.st_mode):r.update(kind='symlink',target=os.readlink(p))
        else:r['kind']='other'
        rows.append(r)
    return rows
actual=inventory(S)
manifest=json.loads((S/'SOURCE_MANIFEST.json').read_text())
expected={r['path']:r for r in manifest['entries']}
observed={r['path']:r for r in actual if r['path'] not in manifest['excluded_control_files']}
diffs=[{'path':n,'expected':expected.get(n),'actual':observed.get(n)} for n in sorted(set(expected)|set(observed)) if expected.get(n)!=observed.get(n)]
pins={'SOURCE_FINAL.json':'f7bc05f4e7d56f0fbad45d77bdb4992d9fd92de8d976bdc5ff3b446f7dbfe9c8',
      'SOURCE_MANIFEST.json':'53be96c6f47deccccc173286d10bdf46b50df4f237c985f42f2da8a69d8c8ffb'}
pin_checks={n:sha(S/n)==v for n,v in pins.items()}
pin_checks['root_source_adoption']=sha(ADOPT)=='9ab699b60b7ac0a9be04db1211f144ccb6db852b573a71a18aa37bb2a4fa707b'
ziprows=[]
with zipfile.ZipFile(S/'zenodo-files/source-and-verification.zip') as z:
    for e in z.infolist():
        dest=S/'archives/01-source-and-verification.zip.extracted'/e.filename
        b=b'' if e.is_dir() else z.read(e)
        ziprows.append({'name':e.filename,'directory':e.is_dir(),'bytes':e.file_size,'mode_octal':oct(stat.S_IMODE(e.external_attr>>16)),
                        'sha256':None if e.is_dir() else hashlib.sha256(b).hexdigest(),
                        'extracted_bytes_match':dest.is_dir() if e.is_dir() else dest.is_file() and dest.read_bytes()==b})
report={'schema':'row191-adversarial-passive-custody-v1','UTC':datetime.now(timezone.utc).isoformat(),'phase':phase,'source_root':str(S),
        'actual_entries':actual,'manifest_payload_diffs':diffs,'control_pins':pins,'control_pin_matches':pin_checks,
        'counts':{'files':sum(r['kind']=='file' for r in actual),'child_directories':sum(r['kind']=='directory' for r in actual)-1,
                  'hidden_objects':sum(any(x.startswith('.') and x!='.' for x in Path(r['path']).parts) for r in actual),
                  'empty_directories':sum(r.get('empty',False) for r in actual)},
        'zip_members':ziprows,'zip_member_count':len(ziprows),'embedded_PDF_count':sum(r['name'].lower().endswith('.pdf') for r in ziprows),
        'all_byte_mode_topology_checks_pass':not diffs and all(pin_checks.values()) and all(r['extracted_bytes_match'] for r in ziprows),
        'scientific_code_executed':False,'packaged_support_semantically_read':False}
if phase=='after':
    before=json.loads((A/'SOURCE_GUARD_BEFORE.json').read_text())
    report['source_exactly_unchanged_from_before']=actual==before['actual_entries']
target=A/('SOURCE_GUARD_'+phase.upper()+'.json')
with target.open('x') as f:f.write(json.dumps(report,indent=2)+'\n')
if not report['all_byte_mode_topology_checks_pass']:raise AssertionError('Custody mismatch, see literal report')
if phase=='after' and not report['source_exactly_unchanged_from_before']:raise AssertionError('Source changed')
if phase=='before':
    class NativeHTML(HTMLParser):
        def __init__(self):super().__init__();self.skip=0;self.visible=[];self.meta=[];self.special=None;self.script=[];self.scripts=[]
        def handle_starttag(self,tag,attrs):
            attrs=dict(attrs)
            if tag=='meta':self.meta.append(attrs)
            if tag in ['script','style']:self.skip+=1
            if tag=='script' and attrs.get('type') in ['application/ld+json','application/json']:self.special=attrs;self.script=[]
        def handle_endtag(self,tag):
            if tag=='script' and self.special is not None:self.scripts.append({'attributes':self.special,'text':''.join(self.script)});self.special=None
            if tag in ['script','style']:self.skip-=1
        def handle_data(self,data):
            if self.special is not None:self.script.append(data)
            if not self.skip and data.strip():self.visible.append(data.strip())
    h=NativeHTML();h.feed((S/'native-metadata/record-page.html').read_text())
    with (A/'native-record-visible.txt').open('x') as f:f.write('\n'.join(h.visible)+'\n')
    with (A/'native-record-html-metadata.json').open('x') as f:f.write(json.dumps({'meta_tags':h.meta,'metadata_scripts':h.scripts},indent=2)+'\n')
print(json.dumps({'phase':phase,'UTC':report['UTC'],'counts':report['counts'],'zip_members':len(ziprows),'embedded_PDFs':report['embedded_PDF_count'],
                  'all_checks_pass':report['all_byte_mode_topology_checks_pass'],'source_unchanged':report.get('source_exactly_unchanged_from_before')}))
