"""Define an agent that will take intake from the client and format the output in a standardized way

Works with a chat model with tool calling search tool.
"""
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from profiler.configuration import Configuration
from profiler.state import InputState, State
from profiler.tools import SEARCH_TOOL, FORMATTER_TOOL
from profiler.node import intake_formatter, intake_worker
from profiler.edge import route_model_output

builder = StateGraph(State, input=InputState, config_schema=Configuration)

# Define the two nodes we will cycle between
builder.add_node("intake_worker", intake_worker)
builder.add_node("tools", ToolNode([SEARCH_TOOL]))
builder.add_node("intake_formatter", intake_formatter)

# Set the entrypoint as `intake_worker`
# This means that this node is the first one called
builder.add_edge("__start__", "intake_worker")

builder.add_conditional_edges(
    "intake_worker",
    route_model_output,
)

# Add a normal edge from `tools` to `call_model`
# This creates a cycle: after using tools, we always return to the model
builder.add_edge("tools", "intake_worker")
builder.add_edge("intake_formatter", "__end__")
# Compile the builder into an executable graph
# You can customize this by adding interrupt points for state updates
graph = builder.compile(
    interrupt_before=[],  # Add node names here to update state before they're called
    interrupt_after=[],  # Add node names here to update state after they're called
)
graph.name = "Travel Intake Worker"  # This customizes the name in LangSmith
