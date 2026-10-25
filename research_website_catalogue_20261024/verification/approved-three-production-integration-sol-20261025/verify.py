"""Fresh bounded integration checks; preserves every prior sealed QA output."""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import ast, datetime, hashlib, json, re, subprocess
import xml.etree.ElementTree as ET

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
D=P/'verification/local-bosonic-stage-sol-20261025'
E=Path(__file__).resolve().parent
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
IDS=['23306332','23203100','22089807']

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        while data:=stream.read(1048576):h.update(data)
    return h.hexdigest()

def save(name,value):
    target=E/name
    assert not target.exists(),target
    target.write_text(value if isinstance(value,str) else json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()

class Visible(HTMLParser):
    def __init__(self,h):
        super().__init__();self.body=False;self.parts=[];self.feed(h)
    def handle_starttag(self,t,a):
        if t=='body':self.body=True
        if self.body and t in ['p','h1','h2','li','br','section','header','footer']:self.parts.append('\n')
    def handle_endtag(self,t):
        if t=='body':self.body=False
        if self.body and t in ['p','h1','h2','li','section']:self.parts.append('\n')
    def handle_data(self,d):
        if self.body:self.parts.append(d)

baseline=json.loads((E/'premutation-custody.json').read_text())
actual={str(x.relative_to(S)):{'sha256':sha(x),'bytes':x.stat().st_size} for x in sorted((S/'public').rglob('*')) if x.is_file()}
before=baseline['site_baseline']
changed=[x for x in before if actual.get(x)!=before[x]]
added=sorted(set(actual)-set(before));removed=sorted(set(before)-set(actual))
assert sorted(changed)==['public/research/index.html','public/research/sitemap.xml'] and not removed
expected_added=[];files={};bodies={}
for rid in IDS:
    c=json.loads((P/'papers'/rid/'publication.json').read_text());folder=S/'public/research'/c['slug'];stage=D/'public/research'/c['slug']
    expected=['index.html','citation.bib',c['pdf_filename'],c['supplement_filename']]
    assert sorted(x.name for x in folder.iterdir())==sorted(expected)
    expected_added += [str((folder/x).relative_to(S)) for x in expected]
    files[rid]={x:{'actual':sha(folder/x),'accepted_stage':sha(stage/x),'bytes':(folder/x).stat().st_size} for x in expected}
    assert all(x['actual']==x['accepted_stage'] for x in files[rid].values()),rid
    h=(folder/'index.html').read_text();v=Visible(h)
    text='\n\n'.join(' '.join(x.split()) for x in ''.join(v.parts).split('\n') if x.strip())+'\n'
    assert text==(D/('public-copy-'+rid+'.txt')).read_text()
    save('public-copy-'+rid+'.txt',text)
    sections={sid:[unescape(x) for x in re.findall('<p>(.*?)</p>',segment,re.S)] for sid,segment in re.findall('<section id="([^"]+)">(.*?)</section>',h,re.S)}
    assert sections==json.loads((D/('public-sections-'+rid+'.json')).read_text())
    save('public-sections-'+rid+'.json',sections)
    bodies[rid]={'actual_body_sha256':sha(E/('public-copy-'+rid+'.txt')),'accepted_body_sha256':sha(D/('public-copy-'+rid+'.txt')),'all_sections_match':True}
assert added==sorted(expected_added) and len(added)==12
shared={relative:{'actual':sha(S/'public'/relative),'accepted_stage':sha(D/'public'/relative)} for relative in ['research/index.html','research/sitemap.xml','research/research.css','robots.txt']}
assert all(x['actual']==x['accepted_stage'] for x in shared.values())
index=(S/'public/research/index.html').read_text();old_index=(E/'before/site/public/research/index.html').read_text()
def itemlist(t):return json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',t,re.S).group(1))['mainEntity']
old_items=itemlist(old_index);items=itemlist(index)
assert old_items['numberOfItems']==47 and items['numberOfItems']==50
assert items['itemListElement'][:47]==old_items['itemListElement']
assert len({x['url'] for x in items['itemListElement']})==50
old_lis=re.findall(r'<li>.*?</li>',old_index,re.S);new_lis=re.findall(r'<li>.*?</li>',index,re.S)
assert len(old_lis)==47 and len(new_lis)==50 and new_lis[:47]==old_lis
def urls(path):return [x.text for x in ET.fromstring(path.read_text()).iter() if x.tag.endswith('loc')]
old_urls=urls(E/'before/site/public/research/sitemap.xml');new_urls=urls(S/'public/research/sitemap.xml')
assert len(old_urls)==48 and len(new_urls)==len(set(new_urls))==51 and new_urls[:48]==old_urls

# Rehash the entire accepted custody set, allowing exactly the four authorized
# already-existing production files. The new helper had no previous file.
manifest=json.loads((D/'stage-readiness-manifest.json').read_text())
allowed={str(P/'scripts/render_page.py'),str(P/'verification/final-content-check.py'),str(S/'public/research/index.html'),str(S/'public/research/sitemap.xml')}
input_changes=[];unexpected=[]
for name,binding in manifest['input_bindings'].items():
    path=Path(name)
    if not path.is_file() or path.stat().st_size!=binding['bytes'] or sha(path)!=binding['sha256']:
        input_changes.append(name)
        if name not in allowed:unexpected.append(name)
assert not unexpected and set(input_changes)==allowed,(unexpected,input_changes)
for name,binding in manifest['artifacts'].items():
    path=D/name
    assert path.is_file() and path.stat().st_size==binding['bytes'] and sha(path)==binding['sha256'],name
for relative,binding in baseline['proposal_bindings'].items():assert sha(P/relative)==binding['sha256']
evidence={'utc':now(),'status':'EXACT_ACCEPTED_STAGE_AND_PRESERVATION_PASS','original_public_file_count':len(before),'current_public_file_count':len(actual),'changed_existing_files':sorted(changed),'added_files':added,'removed_files':removed,'old_public_files_byte_identical':len(before)-len(changed),'old47_articles_and_all_assets_preserved':True,'CSS_and_robots_byte_identical':True,'old47_visible_and_structured_entries_preserved_in_order':True,'old48_sitemap_URLs_preserved_in_order':True,'index_entries':50,'sitemap_urls':51,'new_files':files,'visible_bodies':bodies,'shared_stage_comparison':shared,'input_bindings_rehashed':len(manifest['input_bindings']),'unchanged_input_bindings':len(manifest['input_bindings'])-len(input_changes),'authorized_changed_input_bindings':sorted(input_changes),'unexpected_changed_input_bindings':unexpected,'all_866_original_private_stage_outputs_preserved':True,'live_HTTP_browser_native_publication_PASS':False}
save('exact-output-and-preservation.json',evidence)

# One new complete target execution and one new complete legacy46 execution.
# The original pilot is the 47th existing article and has no TEX_PATHS mapping;
# its HTML and assets are covered by complete byte preservation above.
tree=ast.parse((P/'verification/final-content-check.py').read_text())
mapping=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TEX_PATHS' for t in n.targets))
legacy=[rid for rid in mapping if rid not in IDS]
assert len(legacy)==46 and len(mapping)==49
commands=[]
for stem,rids in [('target-three-production-check',IDS),('full-legacy46-production-check',legacy)]:
    assert not (E/(stem+'.json')).exists() and not (E/(stem+'.md')).exists()
    cmd=[PY,'-B',str(P/'verification/final-content-check.py'),*rids,'--site',str(S/'public'),'--output-dir',str(E),'--output-stem',stem]
    run=subprocess.run(cmd,cwd=P,capture_output=True,text=True)
    save(stem+'.stdout.json',run.stdout);save(stem+'.stderr.txt',run.stderr)
    report=json.loads((E/(stem+'.json')).read_text()) if (E/(stem+'.json')).exists() else None
    entry={'command':cmd,'returncode':run.returncode,'stderr_empty':not run.stderr,'report_status':report['status'] if report else None,'paper_count':len(report['papers']) if report else 0,'passing_checks':sum(sum(x['checks'].values()) for x in report['papers'].values()) if report else 0,'total_checks':sum(len(x['checks']) for x in report['papers'].values()) if report else 0,'issues':report['issues'] if report else ['missing report']}
    commands.append(entry)
    if run.returncode or run.stderr or not report or report['status']!='PASS':
        save('fresh-check-command-results.json',{'utc':now(),'status':'STOPPED_CHECK_ERROR','results':commands})
        raise SystemExit(1)
save('fresh-check-command-results.json',{'utc':now(),'status':'FRESH_TARGET_AND_LEGACY_CHECKS_PASS','results':commands})
save('final-site-manifest.json',actual)
print(json.dumps({'status':'LOCAL_INTEGRATION_CHECKS_PASS','changed_existing':len(changed),'new_files':len(added),'checks':[{'papers':x['paper_count'],'passed':x['passing_checks'],'total':x['total_checks']} for x in commands],'index':50,'sitemap':51,'no_live_pass_claimed':True}))
