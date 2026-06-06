"""编码/变形引擎 — 对 payload 应用各种绕过编码。"""

import base64
import urllib.parse


def encode_payload(payload):
    """Apply all encoding transformations to a payload.

    Returns list of (name, encoded_string).
    """
    encodings = []
    encodings.append(("raw", payload))
    encodings.append(("urlencode", urllib.parse.quote(payload)))
    encodings.append(("double_urlencode", urllib.parse.quote(urllib.parse.quote(payload))))
    encodings.append(("html_escape", html_escape(payload)))
    encodings.append(("unicode", unicode_escape(payload)))
    encodings.append(("swapcase", payload.swapcase()))
    encodings.append(("inline_comment", inline_comment(payload)))
    encodings.append(("hex", hex_escape(payload)))
    encodings.append(("base64", base64.b64encode(payload.encode()).decode()))
    encodings.append(("unicode_url", urllib.parse.quote(unicode_escape(payload))))
    encodings.append(("tab_replace", payload.replace(" ", "\t")))
    encodings.append(("newline_replace", payload.replace(" ", "\n")))
    encodings.append(("null_byte", null_byte(payload)))
    encodings.append(("mixed_case", mixed_case(payload)))
    encodings.append(("reverse", payload[::-1]))
    encodings.append(("javascript_escape", js_escape(payload)))
    # Bypass-specific
    encodings.append(("sql_comment", sql_comment_insert(payload)))
    encodings.append(("overlong_utf8", overlong_utf8(payload)))
    return encodings


def html_escape(s):
    return s.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&#39;").replace("&", "&amp;")


def unicode_escape(s):
    return "".join(f"\\u{ord(c):04x}" for c in s)


def hex_escape(s):
    return "".join(f"\\x{ord(c):02x}" for c in s)


def inline_comment(s):
    return s.replace(" ", "/**/")


def null_byte(s):
    return s + "%00"


def mixed_case(s):
    """Random-ish case alternation."""
    return "".join(
        c.upper() if i % 2 == 0 else c.lower()
        for i, c in enumerate(s)
    )


def js_escape(s):
    return "".join(f"\\x{ord(c):02x}" for c in s)


def sql_comment_insert(s):
    """Insert /**/ between every character for SQL keyword bypass."""
    return "/**/".join(s)


def overlong_utf8(s):
    """Overlong UTF-8 encoding for '/', '..' etc."""
    result = ""
    for c in s:
        if ord(c) < 128:
            # Encode as overlong 2-byte UTF-8
            result += f"%c0%{80 + (ord(c) >> 6):02x}%80%{ord(c) & 0x3f:02x}"
        else:
            result += c
    return result


def encode_methods():
    """Return list of available encoding method names."""
    return [
        "raw", "urlencode", "double_urlencode", "html_escape",
        "unicode", "swapcase", "inline_comment", "hex", "base64",
        "unicode_url", "tab_replace", "null_byte",
        "mixed_case", "reverse", "javascript_escape",
        "sql_comment", "overlong_utf8",
    ]
