import os
from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .nodes import (
    CareerCoachState,
    greeting_node,
    router_node,
    discovery_node,
    validation_node,
    synthesis_node,
    enrichment_node,
    matching_node,
    ranking_node,
    explanation_node,
    action_node,
    route_after_validation
)

"""
def create_graph():
    
    Create the 10-node career coach LangGraph workflow
    
    Flow:
    START → greeting → router → discovery → validation
              ↑                                ↓
              └────────── (loop back) ─────────┤
                                               ↓
                                          synthesis → enrichment
                                               ↓
                                          matching → ranking → explanation
                                               ↓
                                            action → END
    
    
    # Initialize the graph with state
    workflow = StateGraph(CareerCoachState)
    
    # ========================================================================
    # ADD ALL 10 NODES
    # ========================================================================
    
    # Phase 1: Discovery (4 nodes)
    workflow.add_node("greeting", greeting_node)
    workflow.add_node("router", router_node)
    workflow.add_node("discovery", discovery_node)
    workflow.add_node("validation", validation_node)
    
    # Phase 2: Analysis (2 nodes)
    workflow.add_node("synthesis", synthesis_node)
    workflow.add_node("enrichment", enrichment_node)
    
    # Phase 3: Recommendation (3 nodes)
    workflow.add_node("matching", matching_node)
    workflow.add_node("ranking", ranking_node)
    workflow.add_node("explanation", explanation_node)
    
    # Phase 4: Action (1 node)
    workflow.add_node("action", action_node)
    
    # ========================================================================
    # DEFINE EDGES (Flow between nodes)
    # ========================================================================
    
    # Entry point
    workflow.set_entry_point("greeting")
    
    # Phase 1: Discovery loop
    workflow.add_edge("greeting", "router")
    workflow.add_edge("router", "discovery")
    workflow.add_edge("discovery", END)

    
    
    # Conditional: Continue discovery or proceed to synthesis?
    workflow.add_conditional_edges(
        "validation",
        route_after_validation,
        {
            "router": "router",        # Need more info - go back to router
            "synthesis": "synthesis"   # Enough info - move to synthesis
        }
    )
    
    # Phase 2: Analysis flow
    workflow.add_edge("synthesis", "enrichment")
    workflow.add_edge("enrichment", "matching")
    
    # Phase 3: Recommendation flow
    workflow.add_edge("matching", "ranking")
    workflow.add_edge("ranking", "explanation")
    workflow.add_edge("explanation", "action")
    
    # Phase 4: End
    workflow.add_edge("action", END)
    
    # ========================================================================
    # COMPILE GRAPH
    # ========================================================================
    
    # Add memory for conversation persistence
    #memory = MemorySaver()
    graph = workflow.compile()
    
    return graph

"""

def old_create_graph():
    """
    Create the 10-node career coach LangGraph workflow
    
    Flow:
    START → [greeting OR router] → discovery → END (wait for user)
    
    After enough questions:
    START → synthesis → enrichment → matching → ranking → explanation → action → END
    """
    
    # Initialize the graph with state
    workflow = StateGraph(CareerCoachState)
    
    # ========================================================================
    # ADD ALL 10 NODES
    # ========================================================================
    
    # Phase 1: Discovery (4 nodes)
    workflow.add_node("greeting", greeting_node)
    workflow.add_node("router", router_node)
    workflow.add_node("discovery", discovery_node)
    workflow.add_node("validation", validation_node)
    
    # Phase 2: Analysis (2 nodes)
    workflow.add_node("synthesis", synthesis_node)
    workflow.add_node("enrichment", enrichment_node)
    
    # Phase 3: Recommendation (3 nodes)
    workflow.add_node("matching", matching_node)
    workflow.add_node("ranking", ranking_node)
    workflow.add_node("explanation", explanation_node)
    
    # Phase 4: Action (1 node)
    workflow.add_node("action", action_node)
    
    # ========================================================================
    # DEFINE EDGES (Flow between nodes)
    # ========================================================================
    
    # Conditional entry point - only greet on first message
    def should_greet(state: CareerCoachState) -> str:
        """Only show greeting on first interaction"""
        questions_asked = state.get("questions_asked", 0)
        phase = state.get("phase", "greeting")
        
        # If no questions asked yet, greet
        if questions_asked == 0:
            return "greeting"
        
        # If we're in recommendation phase, go to matching
        if phase == "recommendation":
            return "matching"
        
        # If we're in synthesis phase, go to synthesis
        if phase == "synthesis":
            return "synthesis"
        
        # Otherwise, continue with router for next question
        return "router"
    
    workflow.set_conditional_entry_point(
        should_greet,
        {
            "greeting": "greeting",
            "router": "router",
            "matching": "matching",
            "synthesis": "synthesis"
        }
    )
    
    # Phase 1: Discovery flow
    workflow.add_edge("greeting", "router")
    workflow.add_edge("router", "discovery")
    workflow.add_edge("discovery", END)  # Stop after each question to wait for user input
    
    # Phase 2: Analysis flow (when manually triggered or after enough questions)
    workflow.add_edge("synthesis", "enrichment")
    workflow.add_edge("enrichment", "matching")
    
    # Phase 3: Recommendation flow
    workflow.add_edge("matching", "ranking")
    workflow.add_edge("ranking", "explanation")
    workflow.add_edge("explanation", "action")
    
    # Phase 4: End
    workflow.add_edge("action", END)
    
    # ========================================================================
    # COMPILE GRAPH
    # ========================================================================
    
    graph = workflow.compile()
    
    return graph

def create_graph():
    """
    Create the 10-node career coach LangGraph workflow
    """
    
    # Initialize the graph with state
    workflow = StateGraph(CareerCoachState)
    
    # ========================================================================
    # ADD ALL 10 NODES
    # ========================================================================
    
    # Phase 1: Discovery (4 nodes)
    workflow.add_node("greeting", greeting_node)
    workflow.add_node("router", router_node)
    workflow.add_node("discovery", discovery_node)
    workflow.add_node("validation", validation_node)
    
    # Phase 2: Analysis (2 nodes)
    workflow.add_node("synthesis", synthesis_node)
    workflow.add_node("enrichment", enrichment_node)
    
    # Phase 3: Recommendation (3 nodes)
    workflow.add_node("matching", matching_node)
    workflow.add_node("ranking", ranking_node)
    workflow.add_node("explanation", explanation_node)
    
    # Phase 4: Action (1 node)
    workflow.add_node("action", action_node)
    
    # ========================================================================
    # DEFINE EDGES (Flow between nodes)
    # ========================================================================
    
    # Conditional entry point - only greet on first message
    def should_greet(state: CareerCoachState) -> str:
        """Only show greeting on first interaction"""
        questions_asked = state.get("questions_asked", 0)
        phase = state.get("phase", "greeting")
        
        if questions_asked == 0:
            return "greeting"
        
        if phase == "synthesis":
            return "synthesis"
        
        if phase == "recommendation":
            return "matching"
        
        return "router"
    
    workflow.set_conditional_entry_point(
        should_greet,
        {
            "greeting": "greeting",
            "router": "router",
            "matching": "matching",
            "synthesis": "synthesis"
        }
    )
    
    # Phase 1: Discovery flow
    workflow.add_edge("greeting", "router")
    workflow.add_edge("router", "discovery")
    
    # CRITICAL CHANGE: After discovery, check if we should continue or move to synthesis
    def working_should_continue_discovery(state: CareerCoachState) -> str:
        """Decide if we need more questions or should analyze"""
        questions_asked = state.get("questions_asked", 0)
        
        
        # After 6 questions, move to synthesis
        if questions_asked >= 6:
            return "synthesis"
        else:
            return "end"  # End and wait for next user message
        
    def should_continue_discovery(state: CareerCoachState) -> str:
        """Decide if we need more questions or should analyze"""
        questions_asked = state.get("questions_asked", 0)
        current_focus = state.get("current_focus")
    
        print(f"[DECISION] Questions: {questions_asked}, Focus: {current_focus}")  # Debug
    
        # If router says no more focus, move to synthesis
        if current_focus is None:
            return "synthesis"
        else:
            return "end"
    
    workflow.add_conditional_edges(
        "discovery",
        should_continue_discovery,
        {
            "synthesis": "synthesis",  # Go to synthesis
            "end": END  # Stop and wait for user
        }
    )
    
    # Phase 2: Analysis flow
    workflow.add_edge("synthesis", "enrichment")
    workflow.add_edge("enrichment", "matching")
    
    # Phase 3: Recommendation flow
    workflow.add_edge("matching", "ranking")
    workflow.add_edge("ranking", "explanation")
    workflow.add_edge("explanation", "action")
    
    # Phase 4: End
    workflow.add_edge("action", END)
    
    # ========================================================================
    # COMPILE GRAPH
    # ========================================================================
    graph = workflow.compile()
    
    return graph


# Create the graph instance
graph = create_graph()




# ============================================================================
# HELPER FUNCTIONS FOR RUNNING THE GRAPH
# ============================================================================

def initialize_state() -> CareerCoachState:
    """Initialize a fresh conversation state"""
    return {
        "messages": [],
        "phase": "greeting",
        "questions_asked": 0,
        "current_focus": None,
        "user_profile": {},
        "insights": [],
        "profile_completeness": 0.0,
        "career_matches": [],
        "top_recommendations": [],
        "action_plan": None,
        "_routing_decision": None
    }

graph= create_graph()

def run_career_coach(user_message: str, thread_id: str = "default") -> dict:
    """
    Run the career coach with a user message
    
    Args:
        user_message: The user's input
        thread_id: Unique identifier for this conversation thread
    
    Returns:
        dict with assistant's response and updated state
    """
    
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Get current state or initialize
        current_state = graph.get_state(config)
        
        if current_state and current_state.values:
            state = current_state.values
        else:
            state = initialize_state()
        
        # Add user message to state
        state["messages"].append({
            "role": "user",
            "content": user_message
        })
        
        # Run the graph
        final_state = None
        for event in graph.stream(state, config, stream_mode="values"):
            final_state = event
        
        # Get assistant's last message
        if final_state and final_state.get("messages"):
            # Find last assistant message
            for msg in reversed(final_state["messages"]):
                if msg["role"] == "assistant":
                    return {
                        "response": msg["content"],
                        "state": final_state,
                        "phase": final_state.get("phase", "unknown"),
                        "recommendations": final_state.get("top_recommendations", [])
                    }
        
        return {
            "response": "I'm having trouble processing that. Can you try again?",
            "state": state,
            "phase": state.get("phase", "unknown"),
            "recommendations": []
        }
        
    except Exception as e:
        print(f"Error running graph: {e}")
        return {
            "response": "Sorry, I encountered an error. Please try again.",
            "state": state if 'state' in locals() else initialize_state(),
            "phase": "error",
            "recommendations": []
        }


def run_career_coach_stream(user_message: str, thread_id: str = "default"):
    """
    Stream the career coach responses for real-time UI updates
    
    Args:
        user_message: The user's input
        thread_id: Unique identifier for this conversation thread
    
    Yields:
        Events from the graph execution with state updates
    """
    
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Get current state or initialize
        current_state = graph.get_state(config)
        
        if current_state and current_state.values:
            state = current_state.values
        else:
            state = initialize_state()
        
        # Add user message
        state["messages"].append({
            "role": "user",
            "content": user_message
        })
        
        # Stream events
        for event in graph.stream(state, config, stream_mode="values"):
            # Yield each state update
            yield {
                "messages": event.get("messages", []),
                "phase": event.get("phase", "unknown"),
                "questions_asked": event.get("questions_asked", 0),
                "profile_completeness": event.get("profile_completeness", 0.0),
                "top_recommendations": event.get("top_recommendations", [])
            }
            
    except Exception as e:
        print(f"Error in stream: {e}")
        yield {
            "messages": [{
                "role": "assistant",
                "content": "Sorry, I encountered an error."
            }],
            "phase": "error",
            "questions_asked": 0,
            "profile_completeness": 0.0,
            "top_recommendations": []
        }


def start_new_conversation(thread_id: str = "default") -> dict:
    """
    Start a brand new conversation (runs greeting node)
    
    Args:
        thread_id: Unique identifier for this conversation thread
    
    Returns:
        dict with initial greeting and state
    """
    
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Initialize fresh state
        state = initialize_state()
        
        # Run just the greeting node
        final_state = None
        for event in graph.stream(state, config, stream_mode="values"):
            final_state = event
            # Stop after greeting
            if final_state.get("phase") == "discovery":
                break
        
        # Get the greeting message
        if final_state and final_state.get("messages"):
            greeting_msg = final_state["messages"][-1]["content"]
            return {
                "response": greeting_msg,
                "state": final_state,
                "phase": "discovery"
            }
        
        return {
            "response": "Hello! I'm your career discovery coach. What interests you about entertainment?",
            "state": state,
            "phase": "discovery"
        }
        
    except Exception as e:
        print(f"Error starting conversation: {e}")
        return {
            "response": "Hello! I'm your career discovery coach. What interests you about entertainment?",
            "state": initialize_state(),
            "phase": "discovery"
        }


def get_conversation_history(thread_id: str = "default") -> dict:
    """
    Get the full conversation history for a thread
    
    Args:
        thread_id: The conversation thread ID
    
    Returns:
        The current state with full conversation
    """
    
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        current_state = graph.get_state(config)
        if current_state and current_state.values:
            return {
                "messages": current_state.values.get("messages", []),
                "user_profile": current_state.values.get("user_profile", {}),
                "recommendations": current_state.values.get("top_recommendations", []),
                "phase": current_state.values.get("phase", "unknown"),
                "completeness": current_state.values.get("profile_completeness", 0.0)
            }
        else:
            return {
                "messages": [],
                "user_profile": {},
                "recommendations": [],
                "phase": "new",
                "completeness": 0.0
            }
    except Exception as e:
        print(f"Error getting history: {e}")
        return {
            "messages": [],
            "user_profile": {},
            "recommendations": [],
            "phase": "error",
            "completeness": 0.0
        }


def reset_conversation(thread_id: str = "default") -> bool:
    """
    Reset/clear a conversation thread
    
    Args:
        thread_id: The conversation thread ID to reset
    
    Returns:
        bool indicating success
    """
    
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Create fresh state
        fresh_state = initialize_state()
        
        # Update state (this effectively resets it)
        graph.update_state(config, fresh_state)
        
        return True
    except Exception as e:
        print(f"Error resetting conversation: {e}")
        return False


def get_graph_visualization():
    """
    Get a text representation of the graph structure
    (Useful for debugging and documentation)
    """
    
    return """
    Career Coach Graph Structure (10 Nodes):
    
    START
      ↓
    [greeting] - Welcome user
      ↓
    [router] - Decide what to ask about
      ↓
    [discovery] - Ask contextual question (LLM)
      ↓
    [validation] - Check if enough info
      ↓
      ├─ Need more? → back to [router]
      │
      └─ Enough info?
          ↓
        [synthesis] - Extract insights (LLM)
          ↓
        [enrichment] - Add metadata
          ↓
        [matching] - Match to careers (LLM)
          ↓
        [ranking] - Sort by fit score
          ↓
        [explanation] - Enhance reasoning (LLM)
          ↓
        [action] - Create action plan (LLM)
          ↓
        END
    
    LLM Nodes: discovery, synthesis, matching, explanation, action (5 total)
    Logic Nodes: greeting, router, validation, enrichment, ranking (5 total)
    """


# ============================================================================
# EXPORT MAIN GRAPH
# ============================================================================

__all__ = [
    "graph",
    "run_career_coach",
    "run_career_coach_stream",
    "start_new_conversation",
    "get_conversation_history",
    "reset_conversation",
    "get_graph_visualization"
]


"""

---

## **Key Features:**

### **1. Complete 10-Node Flow:**
```
greeting → router → discovery → validation
             ↑________________________↓ (loop)
                                     ↓
synthesis → enrichment → matching → ranking → explanation → action → END
"""