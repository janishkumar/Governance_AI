"""
Career Coach Agent Nodes

10-node hybrid architecture with LangChain message integration
"""

import os
import json
import re
from typing import TypedDict, Optional, Annotated, List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# LangChain message types
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph.message import add_messages

load_dotenv()

# LLM Setup
USE_LLM = False
llm = None

try:
    from langchain_openai import ChatOpenAI
    if os.getenv("OPENAI_API_KEY"):
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        USE_LLM = True
except Exception as e:
    print(f"LLM initialization failed: {e}")
    USE_LLM = False


# Import prompts
from . import prompts


# ============================================================================
# STATE DEFINITION
# ============================================================================

class CareerCoachState(TypedDict):
    # Conversation - using LangChain messages for Studio compatibility
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Discovery tracking
    phase: str  # "greeting" | "discovery" | "synthesis" | "recommendation" | "action" | "completed"
    questions_asked: int
    current_focus: Optional[str]  # "interests" | "skills" | "workstyle" | None
    
    # User profile (builds over time)
    user_profile: Dict  # {interests: [], skills: [], work_style: [], constraints: []}
    insights: List[str]
    profile_completeness: float  # 0.0 to 1.0
    
    # Recommendations
    career_matches: List[Dict]  # All matches
    top_recommendations: List[Dict]  # Top 3 with detailed reasoning
    
    # Action plan
    action_plan: Optional[Dict]
    
    # Internal routing
    _routing_decision: Optional[str]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_latest_human_message(state: CareerCoachState) -> str:
    """Extract the most recent human message content"""
    messages = state.get("messages", [])
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return msg.content if isinstance(msg.content, str) else str(msg.content)
    return ""


def parse_json_response(content: str) -> Any:
    """Parse JSON from LLM response, handling markdown code blocks"""
    try:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r'^```(?:json)?\n', '', cleaned)
            cleaned = re.sub(r'\n```$', '', cleaned)
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Content: {content}")
        return {}


def calculate_profile_completeness(user_profile: Dict) -> float:
    """Calculate how complete the user profile is (0.0 to 1.0)"""
    score = 0.0
    
    if user_profile.get("interests") and len(user_profile["interests"]) > 0:
        score += 0.35
    if user_profile.get("skills") and len(user_profile["skills"]) > 0:
        score += 0.35
    if user_profile.get("work_style") and len(user_profile["work_style"]) > 0:
        score += 0.20
    if user_profile.get("constraints") and len(user_profile["constraints"]) > 0:
        score += 0.10
    
    return min(score, 1.0)


# ============================================================================
# PHASE 1: DISCOVERY NODES
# ============================================================================

def greeting_node(state: CareerCoachState) -> CareerCoachState:
    """
    Node 1: Welcome the user (NO LLM - instant)
    """
    
    # Check if this is a returning user
    user_profile = state.get("user_profile", {})
    if user_profile and user_profile.get("interests"):
        # Returning user
        previous_insights = ", ".join(user_profile.get("interests", [])[:2])
        greeting = prompts.FOLLOWUP_GREETING.format(previous_insights=previous_insights)
    else:
        # New user
        greeting = prompts.INITIAL_GREETING
    
    # Update state with AI message
    return {
        **state,
        "messages": [AIMessage(content=greeting)],
        "phase": "discovery",
        "questions_asked": 0,
        "current_focus": None,
    }

""""
def router_node(state: CareerCoachState) -> CareerCoachState:    
    user_profile = state.get("user_profile", {})
    questions_asked = state.get("questions_asked", 0)
    
    # Determine what we're missing
    has_interests = user_profile.get("interests") and len(user_profile["interests"]) > 0
    has_skills = user_profile.get("skills") and len(user_profile["skills"]) > 0
    has_workstyle = user_profile.get("work_style") and len(user_profile["work_style"]) > 0
    
    # Priority order: interests → skills → workstyle
    if not has_interests or questions_asked < 2:
        focus = "interests"
    elif not has_skills or questions_asked < 4:
        focus = "skills"
    elif not has_workstyle or questions_asked < 6:
        focus = "workstyle"
    else:
        focus = None  # Ready to move on
    
    return {
        **state,
        "current_focus": focus,
    }
"""

def working_router_node(state: CareerCoachState) -> CareerCoachState:
    """
    Node 2: Decide what information to gather next (NO LLM - instant)
    
    Uses a simple rotation strategy to cover different areas:
    - Questions 1-2: Interests (what excites them)
    - Questions 3-4: Skills (what they're good at)
    - Questions 5-6: Work style (how they like to work)
    - Question 7+: Ready to analyze
    """
    
    questions_asked = state.get("questions_asked", 0)
    
    # Simple rotation strategy - ask about different areas
    # This ensures we don't get stuck asking only about guitar
    
    if questions_asked < 2:
        # First 2 questions: explore interests
        focus = "interests"
    elif questions_asked < 4:
        # Next 2 questions: explore skills
        focus = "skills"
    elif questions_asked < 6:
        # Next 2 questions: explore work style preferences
        focus = "workstyle"
    else:
        # After 6 questions, ready to analyze
        focus = None
    
    return {
        **state,
        "current_focus": focus,
    }

def router_node(state: CareerCoachState) -> CareerCoachState:
    """
    Node 2: Decide what information to gather next (NO LLM - instant)
    """
    
    questions_asked = state.get("questions_asked", 0)
    
    print(f"[ROUTER] Questions asked: {questions_asked}")  # Debug log
    
    # After 6 questions asked, we're done
    if questions_asked >= 6:
        focus = None
    elif questions_asked < 2:
        focus = "interests"
    elif questions_asked < 4:
        focus = "skills"
    elif questions_asked < 6:
        focus = "workstyle"
    else:
        focus = None
    
    return {
        **state,
        "current_focus": focus,
    }


def old_working_but_not_fine_discovery_node(state: CareerCoachState) -> CareerCoachState:
    """
    Node 3: Ask contextual questions (LLM CALL ~2s)
    """
    
    if not USE_LLM or llm is None:
        return {
            **state,
            "messages": [AIMessage(content=prompts.FALLBACK_NO_LLM)],
            "questions_asked": state.get("questions_asked", 0) + 1,  # ← INCREMENT HERE
        }
    
    # Get context
    current_focus = state.get("current_focus", "interests")
    messages = state.get("messages", [])
    
    # Format recent conversation (last 5 messages)
    recent_messages = messages[-5:] if len(messages) > 5 else messages
    conversation_context = "\n".join([
        f"{msg.__class__.__name__}: {msg.content}" 
        for msg in recent_messages
    ])
    
    user_profile = prompts.format_user_profile(state.get("user_profile", {}))
    questions_asked = state.get("questions_asked", 0)
    
    # Build prompt with focus area
    focus_guidance = {
        "interests": "Focus on what excites them, what they're passionate about in entertainment.",
        "skills": "Focus on their abilities, what they're good at or want to learn.",
        "workstyle": "Focus on how they like to work (solo/team, structured/flexible, technical/creative)."
    }
    
    user_prompt = prompts.DISCOVERY_USER_PROMPT.format(
        conversation_context=conversation_context,
        user_profile=user_profile,
        questions_asked=questions_asked
    )
    
    # Add focus guidance
    user_prompt += f"\n\nCurrent focus area: {current_focus}\n{focus_guidance.get(current_focus, '')}"
    
    try:
        response = llm.invoke([
            SystemMessage(content=prompts.DISCOVERY_SYSTEM),
            HumanMessage(content=user_prompt)
        ])
        
        next_question = response.content.strip()
        
        return {
            **state,
            "messages": [AIMessage(content=next_question)],
            "questions_asked": questions_asked + 1,  # ← INCREMENT HERE TOO
        }
        
    except Exception as e:
        print(f"Error in discovery_node: {e}")
        return {
            **state,
            "messages": [AIMessage(content=prompts.FALLBACK_DISCOVERY)],
            "questions_asked": questions_asked + 1,  # ← AND HERE
        }
    
def discovery_node(state: CareerCoachState) -> CareerCoachState:
    """
    Node 3: Ask contextual questions (LLM CALL ~2s)
    """
    
    current_focus = state.get("current_focus")
    
    # If no focus, we're done with discovery
    if current_focus is None:
        print("[DISCOVERY] No focus set, skipping question")
        return state  # Don't ask a question, just pass through
    
    if not USE_LLM or llm is None:
        return {
            **state,
            "messages": [AIMessage(content=prompts.FALLBACK_NO_LLM)],
            "questions_asked": state.get("questions_asked", 0) + 1,
        }
    
    # Get context
    messages = state.get("messages", [])
    
    # Format recent conversation (last 5 messages)
    recent_messages = messages[-5:] if len(messages) > 5 else messages
    conversation_context = "\n".join([
        f"{msg.__class__.__name__}: {msg.content}" 
        for msg in recent_messages
    ])
    
    user_profile = prompts.format_user_profile(state.get("user_profile", {}))
    questions_asked = state.get("questions_asked", 0)
    
    # Build prompt with focus area
    focus_guidance = {
        "interests": "Focus on what excites them, what they're passionate about in entertainment.",
        "skills": "Focus on their abilities, what they're good at or want to learn.",
        "workstyle": "Focus on how they like to work (solo/team, structured/flexible, technical/creative)."
    }
    
    user_prompt = prompts.DISCOVERY_USER_PROMPT.format(
        conversation_context=conversation_context,
        user_profile=user_profile,
        questions_asked=questions_asked
    )
    
    # Add focus guidance
    user_prompt += f"\n\nCurrent focus area: {current_focus}\n{focus_guidance.get(current_focus, '')}"
    
    try:
        response = llm.invoke([
            SystemMessage(content=prompts.DISCOVERY_SYSTEM),
            HumanMessage(content=user_prompt)
        ])
        
        next_question = response.content.strip()
        
        return {
            **state,
            "messages": [AIMessage(content=next_question)],
            "questions_asked": questions_asked + 1,
        }
        
    except Exception as e:
        print(f"Error in discovery_node: {e}")
        return {
            **state,
            "messages": [AIMessage(content=prompts.FALLBACK_DISCOVERY)],
            "questions_asked": questions_asked + 1,
        }


def validation_node(state: CareerCoachState) -> CareerCoachState:
    """
    Node 4: Check if we have enough info (NO LLM - instant)
    """
    
    questions_asked = state.get("questions_asked", 0)
    user_profile = state.get("user_profile", {})
    
    # Calculate completeness
    completeness = calculate_profile_completeness(user_profile)
    
    # Decision logic
    if questions_asked >= 5 and completeness >= 0.6:
        routing_decision = "proceed_to_synthesis"
        phase = "synthesis"
    elif questions_asked >= 8:
        # Max questions reached, move forward anyway
        routing_decision = "proceed_to_synthesis"
        phase = "synthesis"
    else:
        # Need more discovery
        routing_decision = "continue_discovery"
        phase = "discovery"
    
    return {
        **state,
        "profile_completeness": completeness,
        "phase": phase,
        "_routing_decision": routing_decision,
    }


# ============================================================================
# PHASE 2: ANALYSIS NODES
# ============================================================================

def synthesis_node(state: CareerCoachState) -> CareerCoachState:
    """
    Node 5: Extract structured insights from conversation (LLM CALL ~2s)
    """
    
    if not USE_LLM or llm is None:
        return {
            **state,
            "user_profile": {"interests": [], "skills": [], "work_style": [], "constraints": []},
            "insights": [],
        }
    
    # Format full conversation for analysis
    messages = state.get("messages", [])
    conversation = "\n".join([
        f"{msg.__class__.__name__}: {msg.content}"
        for msg in messages
    ])
    
    # Build analysis prompt
    user_prompt = prompts.ANALYSIS_USER_PROMPT.format(
        conversation=conversation
    )
    
    try:
        response = llm.invoke([
            SystemMessage(content=prompts.ANALYSIS_SYSTEM),
            HumanMessage(content=user_prompt)
        ])
        
        insights = parse_json_response(response.content)
        
        # Flatten insights for easy checking
        all_insights = []
        for key in ["interests", "skills", "work_style"]:
            all_insights.extend(insights.get(key, []))
        
        return {
            **state,
            "user_profile": insights,
            "insights": all_insights,
        }
        
    except Exception as e:
        print(f"Error in synthesis_node: {e}")
        return {
            **state,
            "user_profile": {"interests": [], "skills": [], "work_style": [], "constraints": []},
            "insights": [],
        }


def enrichment_node(state: CareerCoachState) -> CareerCoachState:
    """
    Node 6: Add metadata and structure to profile (NO LLM - instant)
    """
    
    user_profile = state.get("user_profile", {})
    
    # Add metadata
    enriched_profile = {
        **user_profile,
        "created_at": datetime.now().isoformat(),
        "completeness_score": state.get("profile_completeness", 0.0),
        "total_questions": state.get("questions_asked", 0),
        "insight_count": len(state.get("insights", []))
    }
    
    return {
        **state,
        "user_profile": enriched_profile,
        "phase": "recommendation",
    }


# ============================================================================
# PHASE 3: RECOMMENDATION NODES
# ============================================================================

def matching_node(state: CareerCoachState) -> CareerCoachState:
    """
    Node 7: Match user profile to career paths (LLM CALL ~2s)
    """
    
    if not USE_LLM or llm is None:
        return {
            **state,
            "career_matches": [],
        }
    
    from .career_data import get_career_paths
    
    user_profile = state.get("user_profile", {})
    career_paths = get_career_paths()
    
    # Format for prompt
    user_profile_str = prompts.format_user_profile(user_profile)
    career_paths_str = prompts.format_career_paths(career_paths)
    
    # Build recommendation prompt
    user_prompt = prompts.RECOMMENDATION_USER_PROMPT.format(
        user_profile=user_profile_str,
        career_paths=career_paths_str
    )
    
    try:
        response = llm.invoke([
            SystemMessage(content=prompts.RECOMMENDATION_SYSTEM),
            HumanMessage(content=user_prompt)
        ])
        
        recommendations = parse_json_response(response.content)
        
        # Ensure it's a list
        if not isinstance(recommendations, list):
            recommendations = []
        
        return {
            **state,
            "career_matches": recommendations,
        }
        
    except Exception as e:
        print(f"Error in matching_node: {e}")
        return {
            **state,
            "career_matches": [],
        }


def ranking_node(state: CareerCoachState) -> CareerCoachState:
    """
    Node 8: Score and rank career matches (NO LLM - instant)
    """
    
    career_matches = state.get("career_matches", [])
    
    # Sort by fit_score
    sorted_matches = sorted(
        career_matches, 
        key=lambda x: x.get("fit_score", 0), 
        reverse=True
    )
    
    # Take top 3
    top_3 = sorted_matches[:3]
    
    return {
        **state,
        "top_recommendations": top_3,
    }


def explanation_node(state: CareerCoachState) -> CareerCoachState:
    """
    Node 9: Generate detailed explanations for top 3 (PASS-THROUGH for MVP)
    
    Note: matching_node already provides reasoning, so this is a pass-through.
    In future, could enhance explanations here with another LLM call.
    """
    
    # Pass-through for MVP
    return state


# ============================================================================
# PHASE 4: ACTION NODE
# ============================================================================

def action_node(state: CareerCoachState) -> CareerCoachState:
    """
    Node 10: Create actionable next steps (LLM CALL ~2s)
    """
    
    if not USE_LLM or llm is None:
        return {
            **state,
            "messages": [AIMessage(content="Here are some next steps you can take!")],
            "phase": "completed",
        }
    
    top_recommendations = state.get("top_recommendations", [])
    
    # Format recommendations
    recommendations_summary = prompts.format_recommendations_summary(top_recommendations)
    
    # Build action plan prompt
    user_prompt = prompts.ACTION_USER_PROMPT.format(
        recommendations_summary=recommendations_summary
    )
    
    try:
        response = llm.invoke([
            SystemMessage(content=prompts.ACTION_SYSTEM),
            HumanMessage(content=user_prompt)
        ])
        
        action_plan = response.content.strip()
        
        # Store action plan
        action_plan_data = {
            "content": action_plan,
            "created_at": datetime.now().isoformat()
        }
        
        # Build recommendations message
        rec_message = "Based on our conversation, here are your top career matches:\n\n"
        for i, rec in enumerate(top_recommendations, 1):
            rec_message += f"**{i}. {rec.get('path', 'Unknown')}** (Fit: {rec.get('fit_score', 0):.0%})\n"
            rec_message += f"{rec.get('reasoning', '')}\n\n"
        
        # Return with both messages
        return {
            **state,
            "action_plan": action_plan_data,
            "messages": [
                AIMessage(content=rec_message),
                AIMessage(content=action_plan)
            ],
            "phase": "completed",
        }
        
    except Exception as e:
        print(f"Error in action_node: {e}")
        return {
            **state,
            "messages": [AIMessage(content="Great! Start exploring these paths and take action on your dreams!")],
            "phase": "completed",
        }


# ============================================================================
# CONDITIONAL ROUTING FUNCTIONS
# ============================================================================

def route_after_validation(state: CareerCoachState) -> str:
    """
    Route after validation node
    """
    decision = state.get("_routing_decision", "continue_discovery")
    
    if decision == "proceed_to_synthesis":
        return "synthesis"
    else:
        return "router"  # Go back to router for more discovery


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'CareerCoachState',
    'greeting_node',
    'router_node',
    'discovery_node',
    'validation_node',
    'synthesis_node',
    'enrichment_node',
    'matching_node',
    'ranking_node',
    'explanation_node',
    'action_node',
    'route_after_validation',
]