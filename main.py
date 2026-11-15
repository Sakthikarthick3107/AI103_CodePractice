from src.basic_openai_connect.openai_connect import OpenAiConnect
from src.tools_using.codeinterpret_tool import CodeInterpretTool

tool_use = CodeInterpretTool()
tool_use.get_response()