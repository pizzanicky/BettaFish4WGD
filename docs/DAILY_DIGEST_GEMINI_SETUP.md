# Daily Digest - Google Gemini API 配置指南

## 📝 更新说明

Daily Digest 功能已从使用 `INSIGHT_ENGINE` 配置改为使用 **Google Gemini API**。

---

## 🔧 配置步骤

### 1. 获取 Google Gemini API Key

1. 访问 **Google AI Studio**: https://aistudio.google.com/apikey
2. 使用 Google 账号登录
3. 点击 **"Create API Key"** 或 **"获取API密钥"**
4. 复制生成的 API Key

### 2. 配置环境变量

在 `/Users/winola/WGDInsight/.env` 文件中添加：

```bash
# Google Gemini for Daily Digest
GOOGLE_API_KEY=your_api_key_here
GOOGLE_MODEL_NAME=gemini-2.0-flash-exp
```

**可用的模型选项：**
- `gemini-2.0-flash-exp` - 最新实验版本（推荐，速度快）
- `gemini-1.5-pro` - 稳定版本
- `gemini-1.5-flash` - 快速版本
- `gemini-exp-1206` - 实验版本

### 3. 重启应用

如果在 Docker 中运行：
```bash
docker-compose restart
```

---

## 🔄 代码变更

### 修改的文件

#### 1. **DailyDigest/core.py**

**变更前：**
```python
from InsightEngine.llms.base import LLMClient

class SimpleLLM:
    def __init__(self):
        api_key = settings.INSIGHT_ENGINE_API_KEY
        base_url = settings.INSIGHT_ENGINE_BASE_URL
        model_name = settings.INSIGHT_ENGINE_MODEL_NAME
        self.client = LLMClient(api_key=api_key, model_name=model_name, base_url=base_url)
    
    def chat(self, prompt: str) -> str:
        return self.client.invoke(system_prompt="You are a helpful assistant.", user_prompt=prompt)
```

**变更后：**
```python
import google.generativeai as genai

class SimpleLLM:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        model_name = os.getenv("GOOGLE_MODEL_NAME", "gemini-2.0-flash-exp")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def chat(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
```

#### 2. **.env.example**

添加了新的配置项：
```bash
# Google Gemini for Daily Digest（获取API Key：https://aistudio.google.com/apikey）
GOOGLE_API_KEY=
# Google Gemini模型名称，如gemini-2.0-flash-exp, gemini-1.5-pro等
GOOGLE_MODEL_NAME=gemini-2.0-flash-exp
```

---

## ✅ 优势

### 为什么选择 Google Gemini？

1. **免费额度充足**
   - 每分钟 15 个请求（免费层）
   - 每天 1500 个请求
   - 对于 Daily Digest 使用场景完全足够

2. **性能优秀**
   - `gemini-2.0-flash-exp` 速度极快
   - 支持长上下文（最多 1M tokens）
   - 适合处理大量社交媒体帖子

3. **成本低**
   - 免费层即可满足日常使用
   - 付费版本价格也比 OpenAI 便宜

4. **稳定性好**
   - Google 官方 API
   - 全球可用（中国大陆需要代理）

---

## 🧪 测试

运行 Daily Digest 测试：

```bash
# 在容器内
python3 -c "from DailyDigest.core import run_digest_generation; print(run_digest_generation('TSLA', 24))"
```

或通过 Streamlit 界面：
```bash
streamlit run SingleEngineApp/daily_digest_streamlit_app.py
```

---

## 📊 预期日志输出

**成功初始化：**
```
[SimpleLLM] Initialized Google Gemini: gemini-2.0-flash-exp
```

**生成摘要时：**
```
[SimpleLLM] Sending request to gemini-2.0-flash-exp
Generating summary for 'TSLA'...
Prompt length: 5234 characters
[SimpleLLM] Received response (1523 chars)
LLM call took 2.34 seconds
```

---

## ⚠️ 常见问题

### 1. 错误：`GOOGLE_API_KEY is not configured`

**原因**：`.env` 文件中没有配置 `GOOGLE_API_KEY`

**解决**：
```bash
# 在 .env 文件中添加
GOOGLE_API_KEY=your_actual_api_key_here
```

### 2. 错误：`API key not valid`

**原因**：API Key 无效或已过期

**解决**：
1. 检查 API Key 是否正确复制（没有多余空格）
2. 在 Google AI Studio 重新生成新的 API Key

### 3. 错误：`Resource has been exhausted`

**原因**：超过了免费层的速率限制

**解决**：
- 等待一分钟后重试
- 或升级到付费版本

### 4. 在中国大陆无法访问

**原因**：Google API 在中国大陆被墙

**解决**：
- 配置 HTTP 代理
- 或使用香港/海外服务器

---

## 🔐 安全提示

1. **不要提交 API Key 到 Git**
   - `.env` 文件已在 `.gitignore` 中
   - 确保不要将 API Key 硬编码到代码中

2. **定期轮换 API Key**
   - 建议每 3-6 个月更换一次

3. **监控使用量**
   - 在 Google AI Studio 查看使用统计
   - 设置使用量警报

---

## 📚 参考资源

- **Google AI Studio**: https://aistudio.google.com/
- **Gemini API 文档**: https://ai.google.dev/docs
- **Python SDK 文档**: https://ai.google.dev/api/python/google/generativeai
- **定价信息**: https://ai.google.dev/pricing

---

## 🎯 总结

Daily Digest 现在使用 **Google Gemini API**，配置步骤：

1. ✅ 获取 API Key：https://aistudio.google.com/apikey
2. ✅ 配置 `.env` 文件
3. ✅ 重启应用
4. ✅ 测试功能

**不再需要配置：**
- ❌ `INSIGHT_ENGINE_API_KEY`
- ❌ `INSIGHT_ENGINE_BASE_URL`
- ❌ `INSIGHT_ENGINE_MODEL_NAME`

这些配置仍然保留在 `.env.example` 中，供其他功能使用。
