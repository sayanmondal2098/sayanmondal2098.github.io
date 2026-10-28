const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const code = fs.readFileSync('js/citations.js', 'utf8');

async function scenario({clipboardFails = false, legacyResult = true, fetchFails = false, missingLink = false} = {}) {
  let click;
  let copied;
  let removed = false;
  const timers = [];
  const status = {dataset: {}, classList: {add() {}, remove() {}}};
  const button = {
    textContent: 'Copy citation', dataset: {title: 'Example'}, disabled: false,
    setAttribute() {}, removeAttribute() {},
    closest: () => ({querySelector: () => missingLink ? null : {href: 'https://example.test/research/citations/example.bib'}}),
    addEventListener: (_, listener) => {click = listener;},
  };
  const textarea = {setAttribute() {}, style: {}, select() {}, remove() {removed = true;}};
  const context = {
    document: {
      getElementById: () => status,
      querySelectorAll: () => [button],
      createElement: () => textarea,
      body: {appendChild() {}},
      execCommand: () => legacyResult,
    },
    window: {isSecureContext: true, clearTimeout() {}, setTimeout(fn) {timers.push(fn);}},
    navigator: {clipboard: {async writeText(text) {if (clipboardFails) throw Error('Denied'); copied = text;}}},
    async fetch(url) {
      assert.equal(url, 'https://example.test/research/citations/example.bib');
      return {ok: !fetchFails, text: async () => '  @misc{example}  '};
    },
  };
  vm.runInNewContext(code, context);
  await click();
  assert.equal(button.disabled, true);
  const fails = fetchFails || missingLink || (clipboardFails && !legacyResult);
  assert.equal(button.textContent, fails ? 'Copy failed' : 'Copied ✓');
  assert.equal(status.dataset.type, fails ? 'error' : 'success');
  if (!fails && !clipboardFails) assert.equal(copied, '@misc{example}');
  if (clipboardFails && !fetchFails && !missingLink) assert.equal(removed, true);
  timers.forEach(fn => fn());
  assert.equal(button.disabled, false);
  assert.equal(button.textContent, 'Copy citation');
}

(async () => {
  await scenario();
  await scenario({clipboardFails: true});
  await scenario({clipboardFails: true, legacyResult: false});
  await scenario({fetchFails: true});
  await scenario({missingLink: true});
  console.log('PASS: citation copy, clipboard fallback, denied clipboard, failed fetch, missing link, and button recovery.');
})().catch(error => {console.error(error); process.exitCode = 1;});
