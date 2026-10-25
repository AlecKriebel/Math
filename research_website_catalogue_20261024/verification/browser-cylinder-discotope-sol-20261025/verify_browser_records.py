#!/usr/bin/env python3
"""Read-only future browser-evidence checks. No UI, network, old suite or source execution."""
from pathlib import Path
import hashlib,json,re,subprocess
E=Path(__file__).resolve().parent

def read(name):return json.loads((E/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(p,r):return p.is_file() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256']

def main():
    required=['live-binding.json','preservation-before.json','observations.json','events.json','downloads.json','screenshot-manifest.json','browser-cleanup.json']
    missing=[n for n in required if not (E/n).is_file()]
    if missing:
        print(json.dumps({'status':'PREPARED_NOT_LIVE','public_gate_claimed':False,'missing_actual_evidence':missing},indent=2));return 0
    issues=[];specs=read('expected-records.json')['records'];live=read('live-binding.json');baseline=read('preservation-before.json')
    if live.get('public_site_files')!=492 or not baseline.get('before_first_UI') or baseline.get('public_site_files')!=492:issues.append('fresh492_baseline')
    for r in baseline['files']:
        if not bound(Path(r['path']),r):issues.append('original:'+r['path'])
    obs=read('observations.json');section_checks=0
    for s in specs:
        for width in ['desktop','narrow']:
            found=[r for r in obs if r['record']==s['record'] and r['viewport']==width]
            if len(found)!=1:issues.append('observation:'+s['record']+':'+width);continue
            o=found[0]
            if o['url']!=s['url']:issues.append('observation_url:'+s['record'])
            if ' '.join(o['body'].split())!=' '.join(Path(s['public_copy']).read_text().split()):issues.append('complete_public_copy:'+s['record']+':'+width)
            for t in s['accepted_sections']:
                actual=next((r for r in o['sections'] if r['id']==t['id']),None);section_checks+=1
                if actual is None or any(actual.get(k)!=t[k] for k in ['id','heading','paragraphs','list_items']):issues.append('section:'+s['record']+':'+t['id'])
            if o['section_links']!=s['expected_section_links']:issues.append('links:'+s['record']+':'+width)
    events=read('events.json')
    for s in specs:
        for width in ['desktop','narrow']:
            for action,target in [('title-link-follow',s['url']),('Research-return','https://aleckriebel.com/research/')]:
                key=s['short']+'-'+width+'-'+action;rows=[r for r in events if r['step']==key]
                if len(rows)!=1 or rows[0]['url']!=target:issues.append('navigation:'+key);continue
                r=rows[0]
                if width=='narrow' and [r['width'],r['height']]!=[390,844]:issues.append('narrow_navigation:'+key)
                if action=='Research-return' and (r['count']!=62 or not all(any(a['title']==t['title'] and a['url']==t['url'] for a in r['entries']) for t in specs)):issues.append('index62:'+key)
        pdf=[r for r in events if r['step']==s['short']+'-full-window-PDF-link']
        if len(pdf)!=1 or pdf[0]['url']!=s['url']+s['pdf']:issues.append('PDF_link:'+s['record'])
    downloads=read('downloads.json')
    if len(downloads)!=4 or len({r['tab_id'] for r in downloads})!=4:issues.append('four_download_tabs')
    for r in downloads:
        s=next(t for t in specs if t['record']==r['record']);a=next(t for t in s['assets'] if t['kind']==r['kind'])
        for key in ['path','source_path','site_path']:
            if not bound(Path(r[key]),a):issues.append('download:'+r['record']+':'+r['kind']+':'+key)
    captures=read('screenshot-manifest.json')['captures']
    if len(captures)!=len({r['file'] for r in captures}):issues.append('duplicate_capture_path')
    for r in captures:
        if not bound(E/r['file'],r):issues.append('capture:'+r['file'])
        out=subprocess.check_output(['/usr/bin/sips','-g','pixelWidth','-g','pixelHeight',str(E/r['file'])],text=True)
        physical=[int(re.search(r'pixelWidth: (\d+)',out)[1]),int(re.search(r'pixelHeight: (\d+)',out)[1])]
        if physical!=[r['width'],r['height']]:issues.append('physical_dimension_binding:'+r['file'])
        if r['positive'] and r['viewport']=='narrow' and ([r['width'],r['height']]!=[390,844] or [r['metrics']['width'],r['metrics']['height']]!=[390,844]):issues.append('positive_narrow:'+r['file'])
    cleanup=read('browser-cleanup.json')
    if cleanup['remaining_own'] or not cleanup['all_original_ID_URL_preserved'] or not cleanup['viewport_reset']:issues.append('cleanup')
    result={'status':'RECORDED_BROWSER_CUSTODY_PASS' if not issues else 'FAIL','section_checks':section_checks,'actual_downloads':len(downloads),'issues':issues,'visual_and_scientific_authority':'Separate raw-frame visual report and root dispositions; no new mathematical or native-count claim'}
    print(json.dumps(result,indent=2));return bool(issues)

if __name__=='__main__':raise SystemExit(main())
