import datetime
import pytz
import yaml
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, load_tool, tool, FinalAnswerTool

# Try importing GradioUI; fallback gracefully if the file is missing
try:
    from Gradio_UI import GradioUI
    HAS_GRADIO_UI = True
except ModuleNotFoundError:
    HAS_GRADIO_UI = False

@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """A tool that does nothing yet 
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"

final_answer = FinalAnswerTool()
model = InferenceClientModel(
    max_tokens=2096,
    temperature=0.5,
    model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
    custom_role_conversions=None,
)

# Load system prompt from prompts.yaml file
with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

# FIX: Removed grammar, planning_interval, name, description
agent = CodeAgent(
    model=model,
    tools=[final_answer],
    max_steps=6,
    verbosity_level=1,
    prompt_templates=prompt_templates
)

if HAS_GRADIO_UI:
    GradioUI(agent).launch()
else:
    print("Gradio_UI.py not found in this directory. Running test in terminal instead:")
    agent.run("What is the current time in UTC?")