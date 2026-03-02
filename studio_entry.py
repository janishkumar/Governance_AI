#from app.graph import graph

# Export for LangGraph Studio
#graph_chat = graph()

"""
Entry point for LangGraph Studio
This file is used by LangGraph Studio to load the graph
"""

from app.graph import graph

# Create the graph for LangGraph Studio
graph_chat = graph

# Export for studio
__all__ = ['graph', 'graph_chat', 'initialize_state']