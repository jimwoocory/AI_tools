import json
import requests
import openai
import gradio as gr
from typing import Dict, Any, List, Tuple

class LLMClient:
    def __init__(self, config_path: str = "models_config.json"):
        self.config = self.load_config(config_path)
        self.models = list(self.config.keys())
        self.current_model = self.models[0] if self.models else None
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件 {config_path} 不存在，请检查路径。")
            return {}
            
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        return self.config.get(model_name, {})
        
    def generate(self, prompt: str, model_name: str = None, **kwargs) -> str:
        if model_name is None:
            model_name = self.current_model
            
        config = self.get_model_config(model_name)
        if not config:
            return f"错误：找不到模型 {model_name} 的配置。"
            
        model_type = config.get("model_type")
        try:
            if model_type == "doubao":
                return self._generate_doubao(prompt, config, **kwargs)
            elif model_type == "openai":
                return self._generate_openai(prompt, config, **kwargs)
            else:
                return f"错误：不支持的模型类型 {model_type}。"
        except Exception as e:
            return f"调用模型时出错：{str(e)}"
            
    def _generate_doubao(self, prompt: str, config: Dict[str, Any], **kwargs) -> str:
        # 豆包API调用实现
        api_base = config.get("api_base")
        api_key = config.get("api_key")
        params = config.get("parameters", {})
        params.update(kwargs)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": "doubao-pro",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": params.get("temperature", 0.7),
            "max_tokens": params.get("max_tokens", 2000)
        }
        
        response = requests.post(f"{api_base}/chat/completions", json=data, headers=headers)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API调用失败：{response.status_code} - {response.text}"
            
    def _generate_openai(self, prompt: str, config: Dict[str, Any], **kwargs) -> str:
        # OpenAI API调用实现
        openai.api_base = config.get("api_base")
        openai.api_key = config.get("api_key")
        model_name = config.get("model_name", "gpt-3.5-turbo")
        params = config.get("parameters", {})
        params.update(kwargs)
        
        messages = [{"role": "user", "content": prompt}]
        
        response = openai.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=params.get("temperature", 0.7),
            max_tokens=params.get("max_tokens", 2000)
        )
        
        return response.choices[0].message.content

def create_web_interface(client: LLMClient):
    def generate_response(prompt, model_name, temperature, max_tokens):
        return client.generate(
            prompt, 
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
    with gr.Blocks(title="多模型AI助手") as interface:
        gr.Markdown("# 多模型AI助手")
        
        with gr.Row():
            with gr.Column(scale=3):
                prompt_input = gr.Textbox(
                    label="输入问题", 
                    placeholder="请输入您的问题...", 
                    lines=5
                )
                submit_btn = gr.Button("提交")
                
            with gr.Column(scale=1):
                model_selector = gr.Dropdown(
                    label="选择模型",
                    choices=client.models,
                    value=client.models[0] if client.models else None
                )
                temperature_slider = gr.Slider(
                    label="温度", 
                    minimum=0.0, 
                    maximum=2.0, 
                    value=0.7, 
                    step=0.1
                )
                max_tokens_slider = gr.Slider(
                    label="最大令牌数", 
                    minimum=100, 
                    maximum=4000, 
                    value=2000, 
                    step=100
                )
                
        response_output = gr.Textbox(label="AI回复", lines=10)
        
        submit_btn.click(
            fn=generate_response,
            inputs=[prompt_input, model_selector, temperature_slider, max_tokens_slider],
            outputs=response_output
        )
        
    return interface

if __name__ == "__main__":
    client = LLMClient()
    interface = create_web_interface(client)
    interface.launch()    
