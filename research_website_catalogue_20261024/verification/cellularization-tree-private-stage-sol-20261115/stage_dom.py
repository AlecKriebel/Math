"""New closed grammar for this pair. Iframe raw text is explicitly empty."""
from html.parser import HTMLParser
from collections import Counter


class ClosedDocument(HTMLParser):
    VOID = {"meta", "link", "br", "hr"}
    ALLOWED = {"html", "head", "body", "title", "meta", "link", "script", "a", "header", "nav", "p", "main", "article", "h1", "h2", "section", "iframe", "ul", "li", "footer", "hr", "br", "span"}
    PARENTS = {"html": {None}, "head": {"html"}, "body": {"html"}, "title": {"head"}, "meta": {"head"}, "link": {"head"}, "script": {"head"},
        "main": {"body"}, "article": {"main"}, "header": {"body", "article"}, "nav": {"header"}, "footer": {"body"},
        "section": {"article"}, "h1": {"header"}, "h2": {"section"}, "ul": {"section"}, "li": {"ul"}, "iframe": {"section"},
        "p": {"header", "section", "footer", "li"}, "span": {"p"}, "a": {"body", "p", "nav", "li"}, "br": {"li", "p"}, "hr": {"footer"}}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.counts = Counter(); self.attrs = []; self.links = []; self.metas = []; self.link_elements = []
        self.scripts = []; self.title = ""; self.visible = []; self.iframe_data = []; self.ids = set(); self.doctype = 0
        self.head_closed = False; self.body_closed = False

    def need(self, ok, why):
        if not ok:
            raise ValueError("closed DOM: " + why)

    def handle_decl(self, decl):
        self.need(decl.lower() == "doctype html" and not self.stack and not self.counts, "single initial HTML doctype")
        self.doctype += 1

    def handle_startendtag(self, tag, attrs):
        self.need(tag in self.VOID, "self-closing nonvoid element")
        self.handle_starttag(tag, attrs)

    def handle_starttag(self, tag, attrs):
        parent = self.stack[-1] if self.stack else None
        self.need(tag in self.ALLOWED, "unknown/inert structural tag " + tag)
        self.need(parent in self.PARENTS[tag], "invalid parent " + str(parent) + " for " + tag)
        self.need(not self.body_closed and not (tag == "head" and self.head_closed), "closed document/head cannot reopen")
        self.need(tag != "body" or self.head_closed, "head must finish before body")
        a = dict(attrs); self.need(len(a) == len(attrs), "duplicate attributes")
        self.need(not any(k.startswith("on") or k in {"style", "hidden", "inert", "aria-hidden", "srcdoc"} for k in a), "hiding/executable attribute")
        allowed = {"html": {"lang"}, "meta": {"charset", "name", "property", "content"}, "link": {"rel", "href"}, "script": {"type"},
            "a": {"href", "download", "target", "rel", "class"}, "nav": {"aria-label"}, "main": {"id"}, "section": {"id"},
            "iframe": {"class", "loading", "src", "title"}, "p": {"class"}, "span": {"class"}}.get(tag, set())
        self.need(set(a) <= allowed, "unexpected attributes on " + tag)
        if "class" in a:
            self.need((tag, a["class"]) in {("a", "skip-link"), ("iframe", "paper-pdf"), ("p", "site-title"), ("p", "copyright"), ("span", "entry-meta")}, "unapproved CSS class")
        if "id" in a:
            self.need(a["id"] not in self.ids, "duplicate id"); self.ids.add(a["id"])
        if tag in {"html", "head", "body", "main", "article", "h1", "title", "iframe"}:
            self.need(self.counts[tag] == 0, "single " + tag)
        if tag == "html": self.need(a == {"lang": "en"}, "English root")
        if tag == "main": self.need(a == {"id": "main"}, "visible skip target")
        if tag == "script":
            self.need(a == {"type": "application/ld+json"}, "only inert JSON-LD head script")
            self.scripts.append("")
        if tag == "iframe":
            self.need(a.get("class") == "paper-pdf" and a.get("loading") == "lazy" and len(a) == 4 and a.get("title"), "complete visible native reader")
        if tag == "a":
            href = a.get("href", "")
            self.need(href.startswith(("https://", "/", "assets/", "#")), "unsafe/empty link")
            self.links.append(a)
            if a.get("class") == "skip-link": self.need(parent == "body" and a.get("href") == "#main", "only outer skip-link may use offscreen CSS")
        if tag == "meta": self.metas.append(a)
        if tag == "link": self.link_elements.append(a)
        self.attrs.append((tag, a)); self.counts[tag] += 1
        if tag not in self.VOID: self.stack.append(tag)

    def handle_endtag(self, tag):
        self.need(self.stack and self.stack[-1] == tag, "balanced explicit close " + tag)
        self.stack.pop()
        if tag == "head": self.head_closed = True
        if tag == "body": self.body_closed = True

    def handle_data(self, data):
        parent = self.stack[-1] if self.stack else None
        if parent == "iframe":
            self.need(not data.strip(), "iframe contents must be empty; no hidden article")
            self.iframe_data.append(data)
        elif parent == "script": self.scripts[-1] += data
        elif parent == "title": self.title += data
        elif "body" in self.stack: self.visible.append(data)
        else: self.need(not data.strip(), "text outside visible body/head title")

    def handle_comment(self, data):
        self.need(False, "comments are outside this exact approved grammar")

    def unknown_decl(self, data):
        self.need(False, "unknown declaration")

    def finish(self, text):
        self.feed(text); self.close()
        self.need(not self.stack and self.doctype == 1 and self.head_closed and self.body_closed, "complete closed document")
        self.need(all(self.counts[t] == 1 for t in ("html", "head", "body", "main", "article", "h1", "title", "iframe")), "required unique document/article/reader")
        return self
