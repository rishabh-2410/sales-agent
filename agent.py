import asyncio

from context import INSTRUCTIONS1, INSTRUCTIONS2, INSTRUCTIONS3, SALES_MANAGER_INSTRUCTIONS, AGENT_AS_TOOL_DESCRIPTION
from tools import send_email_tool
from dotenv import load_dotenv

from agents import Agent, Runner, trace, ModelSettings

load_dotenv(override=True)
MODEL_NAME = "gpt-5.4-mini"




sales_agent1 = Agent(name="Professional Sales Agent", instructions=INSTRUCTIONS1, model=MODEL_NAME)
sales_agent2 = Agent(name="Humorous Sales Agent", instructions=INSTRUCTIONS2, model=MODEL_NAME)
sales_agent3 = Agent(name="Executive Sales Agent", instructions=INSTRUCTIONS3, model=MODEL_NAME)

tool1 = sales_agent1.as_tool(tool_name="sales_email_writer_1", tool_description=AGENT_AS_TOOL_DESCRIPTION)
tool2 = sales_agent2.as_tool(tool_name="sales_email_writer_2", tool_description=AGENT_AS_TOOL_DESCRIPTION)
tool3 = sales_agent3.as_tool(tool_name="sales_email_writer_3", tool_description=AGENT_AS_TOOL_DESCRIPTION)

tools = [tool1, tool2, tool3, send_email_tool]


require_tool = ModelSettings(tool_choice="required")

sales_manager = Agent(name="Sales Sender", instructions=SALES_MANAGER_INSTRUCTIONS, model=MODEL_NAME, tools=tools, model_settings=require_tool)

message = "Write a cold sales email"

# async def chat(message: str) -> str:
#     with trace("Sales selection workflow with sending"):
#         results = await asyncio.gather(
#             Runner.run(sales_agent1, message),
#             Runner.run(sales_agent2, message),
#             Runner.run(sales_agent3, message),
#         )
#         outputs = [result.final_output for result in results]

#         emails = "Cold sales emails:\n\n" + "\n\nEmail:\n\n".join(outputs)

#         response = await Runner.run(sales_sender, emails)

#         print(f"Final response:\n{response.final_output}")


async def work(task: str) -> str:
    with trace("Sales manager"):
        result = await Runner.run(sales_manager, task)



if __name__ == "__main__":
    asyncio.run(work("Write a cold email"))


    
