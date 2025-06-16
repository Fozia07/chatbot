import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import chainlit as cl

load_dotenv()
tracing_disabled=True
 

#Reference: https://ai.google.dev/gemini-api/docs/openai
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,)


run_config = RunConfig(
    model=model,
    model_provider=provider,)


agent1 = Agent(
     name="Assistant", 
     instructions="You are a helpful assistant", 
     model=model)
   


@cl.on_chat_start
async def handle_chat_start():
        cl.user_session.set("history",[])
        await cl.Message(content="hello how can i assist you today").send()

@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    result = await Runner.run(
         agent1, 
         input=history,
         run_config =run_config,        
    )
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()
            