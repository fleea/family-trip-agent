from typing import Dict, List, cast

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain.chat_models import init_chat_model

from profiler.utils.configuration import Configuration
from profiler.state import State

from profiler.utils.tools import TripFormatter


async def intake_formatter(
        state: State, config: RunnableConfig
) -> Dict[str, List[AIMessage]]:
    """Standardize the completed trip intake information."""
    configuration = Configuration.from_runnable_config(config)
    model = init_chat_model(configuration.model, temperature=0).with_structured_output(TripFormatter)

    system_message = (
        "Format the trip details into a standardized JSON structure. "
        "Include all relevant information from the conversation history."
    )

    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )
    return {"messages": [response]}