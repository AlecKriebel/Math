// Pure WHATWG URL + location.replace mock. No network, DOM navigation or writes.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const html=fs.readFileSync(new URL('./candidate/docs/papers/gromov-unitary-lipschitz/index.html',import.meta.url),'utf8');
const script=html.match(/<script>\s*([\s\S]*?)\s*<\/script>/)[1];
const OLD='https://aleckriebel.github.io/Math/papers/gromov-unitary-lipschitz/';
const BASE='https://aleckriebel.com/research/lipschitz-nonincreasing-unitary-deformation/';
const samples=[
 ['',BASE],
 ['#result',BASE+'#result'],
 ['?utm_source=legacy#result',BASE+'?utm_source=legacy#result'],
 ['?a=1&a=2&q=a%2Bb+space#result',BASE+'?a=1&a=2&q=a%2Bb+space#result'],
 ['?next=https%3A%2F%2Fevil.example%2F#result',BASE+'?next=https%3A%2F%2Fevil.example%2F#result'],
 ['?q=%23result#r%C3%A9sultat',BASE+'?q=%23result#r%C3%A9sultat'],
 ['?x=1#//evil.example/path',BASE+'?x=1#//evil.example/path'],
 ['?#',BASE],
];
function evaluate(source,suffix) {
 const original=new URL(OLD+suffix);const calls=[];
 vm.runInNewContext(source,{URL,window:{location:{search:original.search,hash:original.hash,replace(value){calls.push(value);}}}},{timeout:1000});
 assert.equal(calls.length,1,'one replace call');
 const result=new URL(calls[0]);assert.equal(result.origin,'https://aleckriebel.com');assert.equal(result.pathname,'/research/lipschitz-nonincreasing-unitary-deformation/');
 return calls[0];
}
const positives=samples.map(([suffix,wanted])=>{const actual=evaluate(script,suffix);assert.equal(actual,wanted);return {suffix,expected:wanted,actual};});
const mutants=[
 ['query discarded',script.replace('target.search = window.location.search;','')],
 ['fragment discarded',script.replace('target.hash = window.location.hash;','')],
 ['destination changed',script.replace(BASE,'https://example.org/unrelated/')],
];
const rejected=[];
for (const [name,source] of mutants) {
 assert.notEqual(source,script);let failed=false;
 try {for (const [suffix,wanted] of samples)assert.equal(evaluate(source,suffix),wanted);} catch {failed=true;}
 assert.ok(failed,name+' must be detected');rejected.push(name);
}
console.log(JSON.stringify({status:'PASS_PURE_REDIRECT_URL_PARSER_CONTROLS',node:process.version,positive_cases:positives,changed_script_controls_rejected:rejected,actual_browser_navigation:false,network_requests:0,files_written:0,no_Javascript_fallback:'Clean canonical destination via static meta refresh and visible link; no claim of preserving query without JavaScript.'},null,2));
