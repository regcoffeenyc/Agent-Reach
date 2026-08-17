#!/usr/bin/env python3
"""
Build a WordPress eXtended RSS (WXR) import file from the markdown in content/.

Run:
    python3 sites/goderdzimetreveli.com/tools/build_wxr.py

Output:
    sites/goderdzimetreveli.com/import/goderdzi-metreveli.wxr.xml

Then, on the WordPress install:
    wp plugin install wordpress-importer --activate
    wp import goderdzi-metreveli.wxr.xml --authors=create

No third-party dependencies. The markdown converter implements only the subset
actually used by this content — headings, paragraphs, lists, tables, blockquotes,
emphasis, links, inline code, horizontal rules, fenced code, and raw HTML
passthrough for the .gm-firsthand / .gm-pending callout blocks. It is not a
general-purpose markdown implementation and is not meant to be.

Front matter recognised (a small YAML subset, one key per line):
    title, slug, id_key, type, lang, template, cluster, category, parent,
    menu_order, date, last_reviewed, seo_title, meta_description,
    primary_keyword, excerpt, translation_of, is_profile_page,
    cs_location, cs_period, cs_role, cs_scope
"""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OUT = ROOT / "import" / "goderdzi-metreveli.wxr.xml"

SITE_URL = "https://goderdzimetreveli.com"
AUTHOR_LOGIN = "gmetreveli"
AUTHOR_NAME = "Goderdzi Metreveli"
AUTHOR_EMAIL = "editor@goderdzimetreveli.com"

FIRST_ID = 100

TEMPLATE_FILES = {
    "pillar": "page-templates/pillar.php",
    "case-study": "page-templates/case-study.php",
    "wide": "page-templates/wide.php",
    # front-page and blog-index are assigned in Settings > Reading, not by template.
    "front-page": "",
    "blog-index": "",
    "default": "",
}

CATEGORY_NAMES = {
    "regenerative-agriculture": "Regenerative agriculture",
    "almond-orchards": "Almond orchards",
    "soil-preparation": "Soil preparation",
    "irrigation-infrastructure": "Irrigation and infrastructure",
    "processing-export": "Processing and export",
}

META_FIELDS = (
    "seo_title",
    "meta_description",
    "primary_keyword",
    "last_reviewed",
    "is_profile_page",
    "cs_location",
    "cs_period",
    "cs_role",
    "cs_scope",
)


# ---------------------------------------------------------------------------
# Front matter
# ---------------------------------------------------------------------------

def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Split a file into (front matter dict, body)."""
    if not text.startswith("---"):
        return {}, text

    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    raw = text[3:end]
    body = text[end + 4:].lstrip("\n")

    meta: dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        meta[key.strip()] = value

    return meta, body


# ---------------------------------------------------------------------------
# Markdown → HTML (deliberately minimal; see module docstring)
# ---------------------------------------------------------------------------

INLINE_CODE = re.compile(r"`([^`]+)`")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")


def inline(text: str) -> str:
    """Inline markdown. Raw HTML in the source is passed through untouched."""
    placeholders: list[str] = []

    def stash(match: re.Match[str]) -> str:
        placeholders.append(match.group(0))
        return f"\x00{len(placeholders) - 1}\x00"

    # Protect existing HTML tags so escaping does not mangle them.
    text = re.sub(r"</?[A-Za-z][^>]*>", stash, text)

    text = html.escape(text, quote=False)

    text = INLINE_CODE.sub(lambda m: f"<code>{m.group(1)}</code>", text)
    text = LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', text)
    text = BOLD.sub(lambda m: f"<strong>{m.group(1)}</strong>", text)
    text = ITALIC.sub(lambda m: f"<em>{m.group(1)}</em>", text)

    def restore(match: re.Match[str]) -> str:
        return placeholders[int(match.group(1))]

    return re.sub(r"\x00(\d+)\x00", restore, text)


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_divider(line: str) -> bool:
    stripped = line.strip().strip("|")
    return bool(stripped) and set(stripped.replace("|", "")) <= set("-: ")


def convert(body: str) -> str:
    """Convert the markdown subset to HTML."""
    lines = body.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Blank
        if not stripped:
            i += 1
            continue

        # HTML comment — drop editorial notes from published output.
        if stripped.startswith("<!--"):
            while i < n and "-->" not in lines[i]:
                i += 1
            i += 1
            continue

        # Raw HTML block (the .gm-firsthand / .gm-pending callouts).
        if stripped.startswith("<div"):
            depth = 0
            block: list[str] = []
            while i < n:
                cur = lines[i]
                depth += len(re.findall(r"<div\b", cur)) - len(re.findall(r"</div>", cur))
                block.append(cur)
                i += 1
                if depth <= 0:
                    break
            # Recursively convert the inner markdown, keeping the wrapper.
            opening = block[0]
            closing = block[-1]
            innards = "\n".join(block[1:-1])
            out.append(opening)
            out.append(convert(innards))
            out.append(closing)
            continue

        # Fenced code
        if stripped.startswith("```"):
            i += 1
            code: list[str] = []
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            body_text = html.escape("\n".join(code), quote=False)
            out.append(f"<pre><code>{body_text}</code></pre>")
            continue

        # Horizontal rule
        if re.fullmatch(r"-{3,}", stripped):
            out.append("<hr />")
            i += 1
            continue

        # Heading
        heading = re.match(r"(#{1,6})\s+(.*)", stripped)
        if heading:
            level = len(heading.group(1))
            # An H1 in the body would collide with the template's page title.
            level = max(level, 2)
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        # Table
        if stripped.startswith("|") and i + 1 < n and is_divider(lines[i + 1]):
            header = split_row(stripped)
            i += 2
            rows: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            parts = ["<figure class=\"wp-block-table\"><table>", "<thead><tr>"]
            parts += [f"<th>{inline(c)}</th>" for c in header]
            parts.append("</tr></thead><tbody>")
            for row in rows:
                parts.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
            parts.append("</tbody></table></figure>")
            out.append("".join(parts))
            continue

        # Blockquote
        if stripped.startswith(">"):
            quoted: list[str] = []
            while i < n and (lines[i].strip().startswith(">") or lines[i].strip() == ""):
                if lines[i].strip() == "":
                    # A blank line ends the quote unless the next line continues it.
                    if i + 1 < n and lines[i + 1].strip().startswith(">"):
                        quoted.append("")
                        i += 1
                        continue
                    break
                quoted.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append(f"<blockquote>{convert(chr(10).join(quoted))}</blockquote>")
            continue

        # Unordered list
        if re.match(r"[-*]\s+", stripped):
            items = collect_list(lines, i, ordered=False)
            out.append(render_list(items, "ul"))
            i = items[-1][1] + 1
            continue

        # Ordered list
        if re.match(r"\d+\.\s+", stripped):
            items = collect_list(lines, i, ordered=True)
            out.append(render_list(items, "ol"))
            i = items[-1][1] + 1
            continue

        # Paragraph — gather until a blank line or a block-level construct.
        para: list[str] = []
        while i < n:
            cur = lines[i]
            cs = cur.strip()
            if not cs:
                break
            if (cs.startswith(("#", ">", "|", "```", "<div", "<!--"))
                    or re.fullmatch(r"-{3,}", cs)
                    or re.match(r"[-*]\s+", cs)
                    or re.match(r"\d+\.\s+", cs)):
                break
            para.append(cs)
            i += 1
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")

    return "\n\n".join(p for p in out if p.strip())


def collect_list(lines: list[str], start: int, ordered: bool) -> list[tuple[str, int]]:
    """Collect list item texts with the index of the last line consumed."""
    pattern = r"\d+\.\s+" if ordered else r"[-*]\s+"
    items: list[tuple[str, int]] = []
    i = start
    n = len(lines)

    while i < n:
        cs = lines[i].strip()
        if re.match(pattern, cs):
            text = re.sub(pattern, "", cs, count=1)
            i += 1
            # Continuation lines: indented and not a new item.
            while i < n:
                nxt = lines[i]
                if not nxt.strip():
                    break
                if re.match(r"[-*]\s+|\d+\.\s+", nxt.strip()):
                    break
                if not nxt.startswith((" ", "\t")):
                    break
                text += " " + nxt.strip()
                i += 1
            items.append((text, i - 1))
        elif not cs and i + 1 < n and re.match(pattern, lines[i + 1].strip()):
            i += 1
        else:
            break

    return items or [("", start)]


def render_list(items: list[tuple[str, int]], tag: str) -> str:
    body = "".join(f"<li>{inline(text)}</li>" for text, _ in items if text)
    return f"<{tag}>{body}</{tag}>"


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

@dataclass
class Item:
    path: Path
    meta: dict[str, str]
    body: str
    post_id: int = 0
    parent_id: int = 0
    key: str = ""
    slug: str = ""
    slug_path: str = ""
    metas: dict[str, str] = field(default_factory=dict)

    @property
    def post_type(self) -> str:
        return self.meta.get("type", "page")

    @property
    def title(self) -> str:
        return self.meta.get("title", self.path.stem)


def load_items() -> list[Item]:
    items: list[Item] = []
    for path in sorted(CONTENT.rglob("*.md")):
        # Biographies are reference copy, not pages.
        if "bios" in path.parts:
            continue
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        if not meta.get("title"):
            print(f"  skip (no title): {path.relative_to(ROOT)}")
            continue
        items.append(Item(path=path, meta=meta, body=body))
    return items


def assign(items: list[Item]) -> None:
    """Assign IDs, keys and slug paths."""
    for offset, item in enumerate(items):
        item.post_id = FIRST_ID + offset
        raw_slug = item.meta.get("slug", "")
        item.slug_path = raw_slug.strip("/")
        item.slug = item.slug_path.split("/")[-1] if item.slug_path else ""
        item.key = item.meta.get("id_key") or item.slug_path or item.path.stem

    by_path = {i.slug_path: i for i in items if i.slug_path}
    by_key = {i.key: i for i in items}

    for item in items:
        # Explicit parent field (case studies under /projects/).
        parent_slug = item.meta.get("parent", "").strip("/")
        if parent_slug and parent_slug in by_path:
            item.parent_id = by_path[parent_slug].post_id
            continue
        # Implicit parent from a nested slug path (/ka/shesakheb/).
        if "/" in item.slug_path:
            prefix = item.slug_path.rsplit("/", 1)[0]
            if prefix in by_path:
                item.parent_id = by_path[prefix].post_id

    # Resolve translation pairing to post IDs.
    for item in items:
        target = item.meta.get("translation_of", "").strip()
        if not target:
            continue
        other = by_key.get(target)
        if other is None:
            print(f"  warning: translation_of '{target}' not found "
                  f"({item.path.relative_to(ROOT)})")
            continue
        item.metas["_gm_translation_of"] = str(other.post_id)

    # Remaining meta.
    for item in items:
        for key in META_FIELDS:
            value = item.meta.get(key, "").strip()
            if value:
                item.metas[f"_gm_{key}"] = value

        item.metas["_gm_lang"] = item.meta.get("lang", "en")

        template = TEMPLATE_FILES.get(item.meta.get("template", "default"), "")
        if template:
            item.metas["_wp_page_template"] = template


# ---------------------------------------------------------------------------
# WXR
# ---------------------------------------------------------------------------

def cdata(text: str) -> str:
    return "<![CDATA[" + text.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def postmeta(key: str, value: str) -> str:
    return (
        "\t\t<wp:postmeta>\n"
        f"\t\t\t<wp:meta_key>{cdata(key)}</wp:meta_key>\n"
        f"\t\t\t<wp:meta_value>{cdata(value)}</wp:meta_value>\n"
        "\t\t</wp:postmeta>\n"
    )


def render_item(item: Item) -> str:
    date = item.meta.get("date", "2026-08-17")
    pub = f"{date} 09:00:00"
    content = convert(item.body)
    excerpt = item.meta.get("excerpt", "")
    menu_order = item.meta.get("menu_order", "0")

    parts = [
        "\t<item>\n",
        f"\t\t<title>{cdata(item.title)}</title>\n",
        f"\t\t<link>{SITE_URL}/{item.slug_path}</link>\n",
        f"\t\t<dc:creator>{cdata(AUTHOR_LOGIN)}</dc:creator>\n",
        f"\t\t<guid isPermaLink=\"false\">{SITE_URL}/?p={item.post_id}</guid>\n",
        f"\t\t<description></description>\n",
        f"\t\t<content:encoded>{cdata(content)}</content:encoded>\n",
        f"\t\t<excerpt:encoded>{cdata(excerpt)}</excerpt:encoded>\n",
        f"\t\t<wp:post_id>{item.post_id}</wp:post_id>\n",
        f"\t\t<wp:post_date>{cdata(pub)}</wp:post_date>\n",
        f"\t\t<wp:post_date_gmt>{cdata(pub)}</wp:post_date_gmt>\n",
        "\t\t<wp:comment_status>closed</wp:comment_status>\n",
        "\t\t<wp:ping_status>closed</wp:ping_status>\n",
        f"\t\t<wp:post_name>{cdata(item.slug)}</wp:post_name>\n",
        "\t\t<wp:status>publish</wp:status>\n",
        f"\t\t<wp:post_parent>{item.parent_id}</wp:post_parent>\n",
        f"\t\t<wp:menu_order>{menu_order}</wp:menu_order>\n",
        f"\t\t<wp:post_type>{cdata(item.post_type)}</wp:post_type>\n",
        "\t\t<wp:post_password></wp:post_password>\n",
        "\t\t<wp:is_sticky>0</wp:is_sticky>\n",
    ]

    category = item.meta.get("category", "").strip()
    if category and item.post_type == "post":
        name = CATEGORY_NAMES.get(category, category.replace("-", " ").capitalize())
        parts.append(
            f'\t\t<category domain="category" nicename="{xml_escape(category)}">'
            f"{cdata(name)}</category>\n"
        )

    for key, value in item.metas.items():
        parts.append(postmeta(key, value))

    parts.append("\t</item>\n")
    return "".join(parts)


def render_categories() -> str:
    out = []
    for slug, name in CATEGORY_NAMES.items():
        out.append(
            "\t<wp:category>\n"
            f"\t\t<wp:category_nicename>{cdata(slug)}</wp:category_nicename>\n"
            "\t\t<wp:category_parent></wp:category_parent>\n"
            f"\t\t<wp:cat_name>{cdata(name)}</wp:cat_name>\n"
            "\t</wp:category>\n"
        )
    return "".join(out)


def build(items: list[Item]) -> str:
    head = f"""<?xml version="1.0" encoding="UTF-8" ?>
<!--
  WordPress eXtended RSS import for goderdzimetreveli.com
  Generated by tools/build_wxr.py from content/*.md — do not hand-edit.
  Regenerate with:  python3 sites/goderdzimetreveli.com/tools/build_wxr.py
-->
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
	<title>Goderdzi Metreveli</title>
	<link>{SITE_URL}</link>
	<description>Regenerative Agriculture and Almond Farming</description>
	<language>en-US</language>
	<wp:wxr_version>1.2</wp:wxr_version>
	<wp:base_site_url>{SITE_URL}</wp:base_site_url>
	<wp:base_blog_url>{SITE_URL}</wp:base_blog_url>
	<wp:author>
		<wp:author_id>1</wp:author_id>
		<wp:author_login>{cdata(AUTHOR_LOGIN)}</wp:author_login>
		<wp:author_email>{cdata(AUTHOR_EMAIL)}</wp:author_email>
		<wp:author_display_name>{cdata(AUTHOR_NAME)}</wp:author_display_name>
		<wp:author_first_name>{cdata('Goderdzi')}</wp:author_first_name>
		<wp:author_last_name>{cdata('Metreveli')}</wp:author_last_name>
	</wp:author>
"""
    return head + render_categories() + "".join(render_item(i) for i in items) + "</channel>\n</rss>\n"


def main() -> int:
    if not CONTENT.is_dir():
        print(f"error: content directory not found at {CONTENT}")
        return 1

    items = load_items()
    if not items:
        print("error: no content files found")
        return 1

    assign(items)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(items), encoding="utf-8")

    pages = sum(1 for i in items if i.post_type == "page")
    posts = sum(1 for i in items if i.post_type == "post")
    en = sum(1 for i in items if i.meta.get("lang") == "en")
    ka = sum(1 for i in items if i.meta.get("lang") == "ka")
    paired = sum(1 for i in items if "_gm_translation_of" in i.metas)

    print(f"wrote {OUT.relative_to(ROOT.parent.parent)}")
    print(f"  {len(items)} items — {pages} pages, {posts} posts")
    print(f"  {en} English, {ka} Georgian, {paired} translation pairings")
    print(f"  {OUT.stat().st_size:,} bytes")
    print()
    print("Import with:")
    print("  wp plugin install wordpress-importer --activate")
    print(f"  wp import {OUT.name} --authors=create")
    print()
    print("Then, in Settings > Reading, set the static front page to 'Goderdzi")
    print("Metreveli' and the posts page to 'Articles and Insights'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
