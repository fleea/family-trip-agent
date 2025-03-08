from datetime import datetime, timezone
from typing import Dict, List, cast

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain.chat_models import init_chat_model

from profiler.utils.configuration import Configuration
from profiler.state import InputState, State
from profiler.utils.tools import SEARCH_TOOL, FORMATTER_TOOL


async def intake_worker(
    state: State, config: RunnableConfig
) -> Dict[str, List[AIMessage]]:
    """Call the LLM powering our "agent".

    This function prepares the prompt, initializes the model, and processes the response.

    Args:
        state (State): The current state of the conversation.
        config (RunnableConfig): Configuration for the model run.

    Returns:
        dict: A dictionary containing the model's response message.
    """
    configuration = Configuration.from_runnable_config(config)

    # Initialize the model with tool binding. Change the model or add more tools here.
    model = init_chat_model(configuration.model, temperature=0).bind_tools([SEARCH_TOOL])

    # Format the system prompt. Customize this to change the agent's behavior.
    system_message = configuration.system_prompt.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    # Get the model's response
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )

    # Return the model's response as a list to be added to existing messages
    return {"messages": [response]}