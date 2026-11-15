#!/usr/bin/env python3
"""Private localhost-only screenshots. No production/browser gate is set."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
import json
import shutil
import subprocess
import sys
import tempfile

P=Path(__file__).resolve().parent
CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
access=[]


class Local(SimpleHTTPRequestHandler):
    def log_message(self,format,*args):access.append({'message':format%args})


def main():
    final=sys.argv[1:]==['--final']
    if sys.argv[1:] not in ([],['--final']):raise ValueError('unknown preview arguments')
    target=P/('PRIVATE_PREVIEW_FINAL_RECEIPTS.json' if final else 'PRIVATE_PREVIEW_RECEIPTS.json')
    if target.exists():raise FileExistsError(str(target))
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Local,directory=str(P)))
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    base='http://127.0.0.1:'+str(server.server_port)+'/preview/index.html'
    specs=[('desktop-top',1440,1000,''),('mobile-top',390,844,''),
           ('desktop-reader',1440,1000,'#reader'),('mobile-materials',390,844,'#materials')]
    records=[]
    try:
        for name,width,height,anchor in specs:
            image=P/'preview'/(('final-' if final else '')+name+'.png')
            if image.exists():raise FileExistsError(str(image))
            profile=Path(tempfile.mkdtemp(prefix='chrome-',dir=P/'preview/cache'))
            cmd=[CHROME,'--headless=new','--disable-gpu','--no-first-run',
                 '--disable-background-networking','--disable-component-update','--disable-sync',
                 '--disable-default-apps','--disable-crash-reporter','--no-default-browser-check',
                 '--host-resolver-rules=MAP * 0.0.0.0, EXCLUDE localhost, EXCLUDE 127.0.0.1',
                 '--user-data-dir='+str(profile),'--disk-cache-dir='+str(profile/'disk'),
                 '--hide-scrollbars','--window-size='+str(width)+','+str(height),
                 '--virtual-time-budget=4000','--screenshot='+str(image),base+anchor]
            started=datetime.now(timezone.utc).isoformat()
            result=subprocess.run(cmd,cwd=P,capture_output=True,timeout=30)
            if result.returncode or not image.exists():raise RuntimeError(result.stderr.decode())
            records.append({'started_UTC':started,'completed_UTC':datetime.now(timezone.utc).isoformat(),
              'private_localhost_only':True,'command':cmd,'exit_code':result.returncode,
              'stdout':result.stdout.decode(),'stderr':result.stderr.decode(),
              'screenshot':str(image),'screenshot_SHA256':sha256(image.read_bytes()).hexdigest(),
              'HTML_SHA256':sha256((P/'preview/index.html').read_bytes()).hexdigest(),
              'window':[width,height],'anchor':anchor,'production_or_native_verification':False})
            shutil.rmtree(profile)
    finally:server.shutdown();server.server_close()
    target.write_text(json.dumps({'receipts':records,'actual_local_access_log':access,
       'all_production_browser_native_canonical_gates_remain_false':True,
       'temporary_profiles_removed':True},indent=2)+'\n')
    print(json.dumps({'private_screenshots':len(records),'local_requests':len(access),
                      'production_browser_gate':False,'native_service_gate':False},indent=2))


if __name__=='__main__':main()
