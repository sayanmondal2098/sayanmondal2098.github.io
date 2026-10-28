"""Validate the static portfolio's local links and research coverage (stdlib only)."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'sayanmondal2098.github.io'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.links = []
        self.citations = []
        self.downloads = []
        self.canonical = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])
        if 'data-copy-citation' in attrs:
            self.citations.append(attrs['data-copy-citation'])
        if tag == 'a' and 'download' in attrs and attrs.get('href', '').endswith('.bib'):
            self.downloads.append(attrs['href'])
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')


def check():
    files = [ROOT / 'index.html', *sorted((ROOT / 'pages').glob('*.html')),
             *sorted((ROOT / 'research').glob('*.html'))]
    pages = {}
    errors = []
    for path in files:
        page = Page(path)
        content = path.read_text(encoding='utf-8')
        page.feed(content)
        pages[path.resolve()] = page
        if len(page.ids) != len(set(page.ids)):
            errors.append(f'{path.relative_to(ROOT)}: duplicate HTML IDs')
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.S):
            try:
                json.loads(block)
            except ValueError as error:
                errors.append(f'{path.relative_to(ROOT)}: invalid structured data: {error}')

    links = 0
    for path, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                if url.hostname != ORIGIN:
                    continue
            target = ((ROOT if url.path.startswith('/') else path.parent)
                      / unquote(url.path).lstrip('/')).resolve() if url.path else path
            if target.is_dir():
                target /= 'index.html'
            links += 1
            label = f'{path.relative_to(ROOT)}: {href}'
            if not target.is_file():
                errors.append(f'{label} -> missing file')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{label} -> missing fragment')

    archive = pages[(ROOT / 'research/index.html').resolve()]
    if len(archive.citations) != len(set(archive.citations)):
        errors.append('research/index.html: duplicate publication citation keys')
    cited_files = set()
    for key in archive.citations:
        path = (ROOT / f'research/{key}.html').resolve()
        page = pages.get(path)
        if not page:
            errors.append(f'{key}: no dedicated research page')
            continue
        if key not in archive.ids:
            errors.append(f'{key}: no stable archive anchor')
        if f'{key}.html' not in archive.links:
            errors.append(f'{key}: archive does not link to research page')
        if page.citations != [key] or len(set(page.downloads)) != 1:
            errors.append(f'{key}: expected one matching copy action and BibTeX download')
        cited_files.update(page.downloads)
        expected = f'https://{ORIGIN}/research/{key}.html'
        if page.canonical != expected:
            errors.append(f'{key}: incorrect canonical URL')
        if not any(urlsplit(link).hostname == 'scholar.google.com' and 'dwLadG8AAAAJ' in link
                   for link in page.links):
            errors.append(f'{key}: missing author Scholar profile link')
        for other in archive.citations:
            if other != key and f'{other}.html' not in page.links:
                errors.append(f'{key}: missing related navigation to {other}')
    if set(archive.downloads) != cited_files:
        errors.append('archive and research-page BibTeX downloads do not match')
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'PASS: {len(pages)} pages, {links} local links, '
          f'{len(archive.citations)} research pages and matching BibTeX records.')
    return 0


if __name__ == '__main__':
    sys.exit(check())
