#!/usr/bin/env python3
"""Produce the Claude Artifact variant of index.html.

The artifact host wraps published pages in its own <!doctype>/<head>/<body>,
so the hosted copy ships page content only. Everything else is identical.

    python3 build-artifact.py [output.html]
"""
import re
import sys

SRC = 'index.html'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'acro-fpv.artifact.html'

html = open(SRC, encoding='utf-8').read()
html = re.sub(r'^<!DOCTYPE html>\s*\n<html lang="en">\s*\n<head>\s*\n', '', html)
html = re.sub(r'<meta charset="utf-8">\s*\n', '', html)
html = re.sub(r'<meta name="viewport"[^>]*>\s*\n', '', html)
html = html.replace('</head>\n<body>\n', '')
html = html.replace('</body>\n</html>\n', '')

for tag in ('<!DOCTYPE', '<html', '</html>', '<head>', '</head>', '<body>', '</body>'):
    if tag in html:
        sys.exit('error: wrapper tag %s survived the strip' % tag)
if not html.startswith('<title>'):
    sys.exit('error: output must start with <title>')

open(OUT, 'w', encoding='utf-8').write(html)
print('wrote %s (%d bytes)' % (OUT, len(html)))
