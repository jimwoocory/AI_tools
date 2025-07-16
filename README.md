# 本地大语言模型调用客户端

这是一个可以在本地调用多个语言模型API的客户端程序，支持豆包、OpenAI等模型，提供统一的调用接口和友好的网页界面。

## 功能特点

- 支持多个语言模型的配置和切换
- 统一的调用接口，简化不同模型的使用差异
- 可调整温度、最大令牌数等生成参数
- 直观的网页交互界面

## 安装和使用

### 1. 克隆仓库
git clone https://github.com/your-username/llm-local-client.git
cd llm-local-client
### 2. 安装依赖
pip install -r requirements.txt
### 3. 配置API密钥

在`models_config.json`中填入你实际的API密钥：
{
    "doubao": {
        "api_base": "https://api.doubao.com/v1",
        "api_key": "your_doubao_api_key",
        ...
    },
    "openai-gpt-3.5": {
        "api_base": "https://api.openai.com/v1",
        "api_key": "your_openai_api_key",
        ...
    }
}
### 4. 运行程序
python llm_client.py
### 5. 访问网页界面

程序启动后，在浏览器中打开显示的URL（通常是`http://localhost:7860`），即可使用网页界面与各模型交互。

## 添加更多模型

如果你想添加其他模型，只需在`models_config.json`中添加新的模型配置，并在`LLMClient`类中添加对应的API调用方法。

## 注意事项

- API密钥是敏感信息，请不要将包含真实密钥的配置文件上传到公共仓库
- 不同模型的API可能有不同的调用限制和费用，请参考各模型的官方文档    
