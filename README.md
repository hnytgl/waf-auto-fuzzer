# waf-auto-fuzzer

自动化WAF策略fuzz与绕过脚本生成工具

## 功能简介

1. 自动fuzz现有WAF防护策略，检测拦截/通过规则；
2. 根据fuzz结果自动生成绕过编码脚本（payload变形/编码）；
3. 结果反馈可用以优化和提升WAF策略。

## 使用说明

1. 安装依赖

```bash
pip install requests
```

2. 运行主脚本

```bash
python waf_auto_fuzz.py
```

3. 按照提示输入待测URL和参数名，脚本会自动fuzz并输出绕过结果，同时生成可复用的`waf_bypass_script.py`脚本。

## 可扩展性

- 支持自行扩展payload和编码方式；
- 可用于集成CI/CD安全流程，或与WAF策略运维联动。

## License

MIT
