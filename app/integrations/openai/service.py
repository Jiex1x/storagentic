"""OpenAI service for chat functionality."""

import os
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service class for OpenAI integration."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        logger.info("🔑 Initializing OpenAI client with API key: %s...", api_key[:10])
        self.client = OpenAI(api_key=api_key)
        logger.info("✅ Successfully initialized OpenAI client")
        
    def get_chat_response(self, message: str) -> str:
        """Get response from OpenAI chat completion."""
        try:
            # 构建系统提示词
            system_prompt = """你是一个专业的仓储助手，可以帮助用户：
            1. 选择合适大小的仓储单元
            2. 回答关于仓储服务的问题
            3. 提供预约和查询服务
            请用专业、友好的语气回答用户的问题。"""
            
            # 创建对话
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            # 提取回答
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error("Error getting chat response: %s", str(e))
            raise 