import os
import sys
import traceback
from openai import OpenAI
from app.core.knowledge_base.storage_info import STORAGE_UNITS, STORAGE_TIPS, LOCATION_FEATURES


class StorageAssistant:
    def __init__(self):
        """Initialize storage assistant"""
        api_key = os.getenv('OPENAI_API_KEY')
        project_id = os.getenv('OPENAI_PROJECT_ID')
        if not api_key:
            raise ValueError("❌ No OpenAI API key found in environment variables")
        if not project_id:
            raise ValueError("❌ No OpenAI Project ID found in environment variables")

        print(f"🔑 Initializing OpenAI client with API key: {api_key[:8]}...")

        try:
            # ✅ 初始化 OpenAI 客户端
            self.client = OpenAI(
                api_key=api_key,
                project=project_id
            )
            print("✅ Successfully initialized OpenAI client")
        except Exception as e:
            print(f"❌ Error initializing OpenAI client: {str(e)}")
            print(traceback.format_exc())
            raise

        # 历史对话上下文
        self.context = []

        # 系统提示词
        self.system_prompt = f"""
        You are a professional storage facility customer service assistant. You can:
        1. Answer questions about storage unit sizes, prices, and availability
        2. Help customers choose suitable storage solutions
        3. Handle booking and inquiry requests
        4. Provide storage-related advice and best practices

        You have access to the following storage unit information:
        {STORAGE_UNITS}

        Storage tips you can provide:
        {STORAGE_TIPS}

        Facility features and services:
        {LOCATION_FEATURES}

        Always maintain a professional, friendly, and helpful attitude.
        Keep responses concise and provide personalized recommendations based on customer needs.
        """

    def get_response(self, message):
        """Get assistant response"""
        self.context.append({"role": "user", "content": message})

        try:
            print("\n📤 Sending request to OpenAI API...")
            print(f"User message: {message}")
            print(f"Context length: {len(self.context)}")

            # ✅ 向 OpenAI 发送消息请求
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # 使用 gpt-4o-mini 模型
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *self.context
                ],
                temperature=0.7,
                max_tokens=1000
            )

            print("✅ Received response from OpenAI API")

            assistant_message = response.choices[0].message.content
            print(f"🤖 Assistant response: {assistant_message}")

            self.context.append({"role": "assistant", "content": assistant_message})

            # 控制上下文长度
            if len(self.context) > 10:
                self.context = self.context[-10:]

            return assistant_message

        except Exception as e:
            print(f"\n❌ Error getting response: {str(e)}", file=sys.stderr)
            print(f"Error type: {type(e)}", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)

            # 打印 response body（如果有）
            if hasattr(e, 'response'):
                print("Response error:", getattr(e.response, 'text', 'No response text'), file=sys.stderr)

            return "Sorry, I cannot process your request at the moment. Please try again later."
