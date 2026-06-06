# WAF Auto Fuzzer

自动化 WAF 绕过探测与指纹识别工具。

## 功能

- **17 类攻击 payload** — SQLi, XSS, 命令注入, 路径穿越, SSRF, RCE, XXE, SSTI, LDAP, Open Redirect 等
- **18 种编码/变形** — URL 编码, 双重编码, HTML 实体, Unicode, Base64, 注释注入, 大小写混淆, Null Byte 等
- **多 HTTP 方法** — GET, POST, PUT, Cookie 注入, Header 注入
- **并发 FUZZ** — 多线程快速扫描
- **WAF 指纹识别** — 自动识别 Cloudflare, ModSecurity, AWS WAF, F5, Akamai, Imperva, Sucuri 等 15+ 种 WAF
- **结果输出** — JSON / CSV / HTML 报告
- **绕过脚本生成** — 自动生成可复用的 Python 绕过脚本
- **代理支持** — 支持 Burp Suite 等中间人代理
- **断点信号处理** — Ctrl+C 安全中断

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

```bash
# 基本用法：GET 参数 fuzz
python waf_fuzz.py -t "http://target.com/search?q=" -p q

# POST 表单 fuzz
python waf_fuzz.py -t "http://target.com/login" -m POST -p username

# 仅测试 SQLi 和 XSS
python waf_fuzz.py -t "http://target.com/search?q=" -p q -c sqli xss

# 仅用 URL 编码
python waf_fuzz.py -t "http://target.com/search?q=" -p q -e urlencode base64

# 通过 Burp 代理
python waf_fuzz.py -t "http://target.com" -p q --proxy http://127.0.0.1:8080

# 保存结果并生成绕过脚本
python waf_fuzz.py -t "http://target.com" -p q -o result.json --generate-script

# Cookie 注入测试
python waf_fuzz.py -t "http://target.com" -m COOKIE -p session_id

# Header 注入测试
python waf_fuzz.py -t "http://target.com" -m HEADER -p X-Forwarded-For

# 完整 HTML 报告
python waf_fuzz.py -t "http://target.com" -p q -o result.json --html-report report.html --bypass-report bypass.txt
```

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-t, --target` | 必填 | 目标 URL |
| `-p, --param` | q | 参数名 |
| `-m, --method` | GET | HTTP 方法 (GET/POST/PUT/COOKIE/HEADER) |
| `-d, --data-param` | 同 -p | POST 参数名 |
| `-c, --categories` | 全部 | 测试分类 (sqli xss cmdi traversal ssrf rce xxe ssti ldap redirect) |
| `-e, --encodings` | 全部 | 编码方式 |
| `--threads` | 10 | 并发线程数 |
| `--delay` | 0 | 请求间延迟(秒) |
| `--timeout` | 10 | 超时(秒) |
| `--proxy` | — | 代理地址 |
| `--header` | — | 自定义请求头 |
| `--user-agent-rotate` | — | 轮换 UA |
| `--no-verify` | — | 跳过 SSL 验证 |
| `--follow-redirects` | — | 跟随重定向 |
| `-o, --output` | — | 输出文件 (.json/.csv) |
| `--html-report` | — | HTML 报告路径 |
| `--bypass-report` | — | 绕过摘要报告路径 |
| `--generate-script` | — | 生成绕过脚本 waf_bypass.py |
| `--dry-run` | — | 仅显示测试计划 |

## 项目结构

```
waf_fuzz.py           # CLI 入口
waf_fuzz/
├── __init__.py       # 版本信息
├── payloads.py       # 所有攻击 payload 定义
├── encoders.py       # 编码/变形引擎
├── detector.py       # WAF 检测与指纹识别
├── fuzzer.py         # 多线程 FUZZ 引擎
├── bypass.py         # 绕过脚本生成器
└── output.py         # JSON/CSV/HTML 输出
```

## 编码方式

| 名称 | 说明 |
|------|------|
| raw | 原始 payload |
| urlencode | URL 编码 |
| double_urlencode | 双重 URL 编码 |
| html_escape | HTML 实体编码 |
| unicode | Unicode 编码 |
| swapcase | 大小写反转 |
| inline_comment | 内联注释注入 |
| hex | 十六进制转义 |
| base64 | Base64 编码 |
| unicode_url | Unicode + URL 编码 |
| tab_replace | Tab 替换空格 |
| null_byte | Null Byte 注入 |
| mixed_case | 大小写混合 |
| reverse | 字符串反转 |
| javascript_escape | JavaScript 十六进制转义 |
| sql_comment | SQL 注释插入 |
| overlong_utf8 | 过长 UTF-8 编码（用于目录遍历） |

## WAF 指纹识别库

支持 15+ 种 WAF 识别：Cloudflare, ModSecurity, AWS WAF, F5 BIG-IP, Akamai, Imperva, Sucuri, Barracuda, Fortinet, Azure WAF, Cisco ACE, Alibaba Cloud, SafeDog, DDoS-Guard, Wordfence。

## 免责声明

本工具仅供授权的安全评估使用。在未获得系统所有者书面授权的情况下使用本工具是非法的。作者对任何滥用行为不承担责任。
