"""Read-only target-stage and exact old-byte fence. Never renders or writes."""
from six_common import *
from six_source import load_bundles
from six_body_contract import check_page
from pathlib import Path
from html import escape as h
from datetime import date
import argparse,copy,subprocess,xml.etree.ElementTree as ET

def check_overlays(bundles,index,sitemap,build_date,old):
    """Pure overlay semantics against the authenticated saved base; no source replay."""
    checks={};test=lambda k,v:checks.__setitem__(k,bool(v))
    oldindex=(OWN/'baseline/research/index.html').read_bytes();oldmap=(OWN/'baseline/research/sitemap.xml').read_bytes()
    test('exact_saved_base_index',bind(OWN/'baseline/research/index.html')=={k:old['research/index.html'][k] for k in ['bytes','sha256']})
    test('exact_saved_base_sitemap',bind(OWN/'baseline/research/sitemap.xml')=={k:old['research/sitemap.xml'][k] for k in ['bytes','sha256']})
    text=index.decode();before=oldindex.decode();li=re.findall(r'<li>.*?</li>',text,re.S);oldli=re.findall(r'<li>.*?</li>',before,re.S)
    test('all_old72_visible_entries_byte_identical',len(li)==78 and len(oldli)==72 and li[:72]==oldli)
    add=[]
    for b in bundles:
        c=b['c'];dt=date.fromisoformat(c['publication_date']);day=f'{dt.day} {dt.strftime("%B %Y")}';kind='Unrefereed research note' if b['rid'] in {'23333046','23320818'} else 'Unrefereed preprint';doi='https://doi.org/'+c['doi']
        add.append('<li><a href="/research/'+c['slug']+'/">'+h(c['title'])+'</a><br><span class="entry-meta">'+day+' · '+kind+'</span><p>'+h(c['description'])+'</p><p><a href="/research/'+c['slug']+'/'+c['pdf_filename']+'">PDF</a> · <a href="'+doi+'">Zenodo</a></p></li>')
    test('exact_six_new_visible_entries',li[72:]==add)
    rx=r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)';om=re.search(rx,before,re.S);nm=re.search(rx,text,re.S)
    try:od=strict_json(om.group(2));nd=strict_json(nm.group(2))
    except (AttributeError,ValueError):od={};nd={}
    expected_json=copy.deepcopy(od)
    try:
        its=expected_json['mainEntity']['itemListElement']
        for b in bundles:
            c=b['c'];its.append({'@type':'ListItem','position':len(its)+1,'url':'https://aleckriebel.com/research/'+c['slug']+'/','name':c['title']})
        expected_json['mainEntity']['numberOfItems']=78
    except KeyError:expected_json=None
    test('exact_old_plus_six_ItemList_and78count',same(nd,expected_json))
    restored=text
    if om and nm:restored=restored[:nm.start(2)]+om.group(2)+restored[nm.end(2):]
    for entry in add:restored=restored.replace('      '+entry+'\n','',1)
    test('all_other_index_bytes_unchanged',restored==before)
    urls=['https://aleckriebel.com/research/'+b['c']['slug']+'/' for b in bundles]
    try:
        os=ET.fromstring(oldmap);ns=ET.fromstring(sitemap)
        locs=[x.text for x in ns.findall('{*}url/{*}loc')];olocs=[x.text for x in os.findall('{*}url/{*}loc')]
        test('exact_old73_plus_six_sitemap_locations',len(olocs)==73 and locs==olocs+urls and len(locs)==len(set(locs))==79)
    except ET.ParseError:test('exact_old73_plus_six_sitemap_locations',False)
    restored=sitemap.decode()
    for url in urls:restored=restored.replace('  <url><loc>'+url+'</loc><lastmod>'+build_date+'</lastmod></url>\n','',1)
    test('all_other_sitemap_bytes_unchanged',restored==oldmap.decode())
    return checks

def verify(stage_root,build_date,*,current_base=False,_bundles=None):
    require(date.fromisoformat(build_date).isoformat()==build_date,'explicit_stage_date')
    target=safe_output(stage_root);require(target.is_dir(),'existing_private_stage')
    bundles=load_bundles() if _bundles is None else _bundles
    seal=load(OWN/'INPUT_FREEZE_SEAL.json');baseline=load(OWN/'FRESH_BASELINE.json')
    require(bind(OWN/'FRESH_BASELINE.json')['sha256']==seal['baseline_sha256'],'fresh_baseline_seal')
    checks={};test=lambda k,v:checks.__setitem__(k,bool(v));old={x['path']:x for x in baseline['public_files']}
    expected={'research/index.html','research/sitemap.xml'}
    for b in bundles:
        c=b['c'];expected.update('research/'+c['slug']+'/'+n for n in ['index.html','citation.bib',c['pdf_filename'],c['supplement_filename']])
    actual={str(p.relative_to(target)) for p in target.rglob('*') if p.is_file()}
    test('exact_26_path_overlay_fence',actual==expected and len(actual)==26 and expected&set(old)=={'research/index.html','research/sitemap.xml'})
    test('no_stage_symlinks',not any(p.is_symlink() for p in target.rglob('*')))
    index=(target/'research/index.html').read_bytes();sitemap=(target/'research/sitemap.xml').read_bytes()
    records={}
    for b in bundles:
        c=b['c'];folder=target/'research'/c['slug'];files={x.name:x.read_bytes() for x in folder.iterdir() if x.is_file()}
        records[b['rid']]=check_page(b,files.get('index.html',b''),files,index_bytes=index,sitemap_bytes=sitemap,build_date=build_date)
    test('six_complete_body_contracts',all(all(x.values()) for x in records.values()))
    checks.update(check_overlays(bundles,index,sitemap,build_date,old))
    oldchecks={}
    for x in baseline['public_files']:
        if x['path'] not in {'research/index.html','research/sitemap.xml'}:
            oldchecks[x['path']]=bind(contained(PUBLIC,x['path']))=={k:x[k] for k in ['bytes','sha256']}
    test('all530_old_nonoverlay_public_bytes_preserved',len(oldchecks)==530 and all(oldchecks.values()))
    corechecks={x['path']:bind(contained(PROGRAMME,x['path']))=={k:x[k] for k in ['bytes','sha256']} for x in baseline['installed_core_files']}
    test('all18_installed_core_bytes_preserved',len(corechecks)==18 and all(corechecks.values()))
    test('installed_core_inventory_unchanged',{str(p) for p in [*PROGRAMME.joinpath('scripts').glob('*.py'),PROGRAMME/'verification/final-content-check.py']}==set(corechecks))
    test('conditional_public_union556',len(set(old)|actual)==556)
    # Every local article destination resolves in the overlay or unchanged base.
    from simple_dom import Document
    local=[]
    from urllib.parse import urlsplit,unquote
    for b in bundles:
        c=b['c'];rel='research/'+c['slug']+'/index.html';doc=Document((target/rel).read_text())
        for attrs,label in doc.anchors:
            u=urlsplit(attrs['href'])
            if u.scheme or u.netloc:continue
            path=unquote(u.path);dest=(Path(path.lstrip('/')) if path.startswith('/') else Path(rel).parent/path) if path else Path(rel)
            if path.endswith('/'):dest=dest/'index.html'
            dest=Path(str(dest));f=target/dest if (target/dest).is_file() else PUBLIC/dest
            ok=f.is_file()
            if ok and u.fragment:ok=('id="'+u.fragment+'"') in f.read_text()
            local.append(ok)
    test('all_actual_local_article_links_resolve',bool(local) and all(local))
    if current_base:
        present={str(x.relative_to(PUBLIC)) for x in PUBLIC.rglob('*') if x.is_file()}
        test('current_production_still_exact_old532_inventory',present==set(old))
        test('current_production_index_sitemap_unmodified',all(bind(PUBLIC/n)=={k:old[n][k] for k in ['bytes','sha256']} for n in ['research/index.html','research/sitemap.xml']))
        test('current_website_HEAD_preserved',subprocess.check_output(['git','rev-parse','HEAD'],cwd=WEBSITE,text=True).strip()==baseline['website_HEAD'])
    return {'status':'PASS' if all(checks.values()) else 'FAIL','stage':str(target),'build_date':build_date,'records':records,'checks':checks,
            'old_nonoverlay_public_files_checked':len(oldchecks),'installed_core_files_checked':len(corechecks),'local_links_checked':len(local),
            'conditional_counts':[556,78,79],'current_base_checked':current_base,'writes':0,'network':0}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--stage-root',required=True,type=Path);p.add_argument('--build-date',required=True);p.add_argument('--current-base',action='store_true');a=p.parse_args()
    r=verify(a.stage_root,a.build_date,current_base=a.current_base);print(json.dumps(r,ensure_ascii=False,sort_keys=True));raise SystemExit(0 if r['status']=='PASS' else 1)
