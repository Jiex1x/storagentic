
import os
from openai import OpenAI

# 设置环境变量（你也可以放在 .env 文件里）
os.environ["OPENAI_API_KEY"] = "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"  # ← 替换成你的真实 key
os.environ["OPENAI_PROJECT_ID"] = "proj_UGu1URvT5lfvk5iasr38ha8w"  # ← 替换成你的真实 project_id

print("✅ 正在初始化 OpenAI 客户端...")

# 初始化客户端（新版 SDK 不需要传入参数，直接读取环境变量）
client = OpenAI()

print("✅ 客户端初始化成功，准备请求模型列表...")

try:
    models = client.models.list()
    print("🎯 API key 有效，以下是可用模型列表：")
    for m in models.data:
        print("📌", m.id)
except Exception as e:
    print("❌ API key 测试失败: ", e)
