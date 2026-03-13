# GOD FILE — Document Search Engine

## Overview

The GOD FILE is a self-contained HTML search engine that indexes every document in the BroyhillGOP platform. Version 4 contains 4,071 files across 83 categories.

## Stats

- **4,071 files** indexed
- **83 categories** (E00 through E58 + infrastructure categories)
- **File types:** 833 Markdown, 420 SQL, plus DOCX, PPTX, HTML, Python, JSON, CSV
- **Searchable fields:** filename, category, file type, tags
- **Update frequency:** Real-time via GOD FILE update script

## Architecture

The GOD FILE is a single HTML file (`GOD_FILE_INDEX_V4.html`) containing:
- Embedded JSON array: `const F=[...]` with 4,071 file metadata objects
- Category definitions: `const CATS={...}` mapping 83 ecosystem codes
- Full-text search engine in vanilla JavaScript
- Filter controls for file type, source folder, and category
- Responsive grid layout with color-coded file type badges

## File Metadata Schema

Each entry in the `F` array:
```json
{
  "n": "filename.ext",
  "s": 12345,
  "m": 1710288000,
  "t": "md",
  "c": "E20",
  "tags": "brain intelligence scoring"
}
```

## Access

- **Live URL:** https://broyhill.github.io/broyhillgop-index/
- **GitHub repo:** https://github.com/broyhill/broyhillgop-index
- **Local path:** GOD_FILE_INDEX_V4.html in the project root
