# Project Overview

This project implements a learning agent system that decides which tools to call based on a user query — for example:

Weather lookup tool

Research / information lookup tool

## The agent is designed to make mistakes in early runs, receive feedback, and then improve its behavior over time by learning from past execution traces.

# This demonstrates:

tool-routing logic

mistake detection

memory-driven learning

feedback-based adaptation

stronger rules emerging from repeated mistakes

# System Architecture (Agent Workflow)
<p align="center">
  <img src="https://raw.githubusercontent.com/Pratyush-Basu/self-improving-tool-agent/main/system_architecture_diagram.png" width="750">
</p>

Roles of Each Component
Component	Responsibility
agent_node -	Decides routing → which tool(s) to call
tool_node -	Executes tools in routed order
summary_node -	Combines results into final answer
evaluate_node -	Detects mistakes and logs them
learn_node -	Saves learning to persistent memory
memory.py -	Stores mistake counts + generates rules

The agent improves across runs because memory persists between executions.

# Learning & Feedback Logic

The agent initially behaves imperfectly — it may:

skip a required tool

only call one tool in a multi-query

call tools in the wrong order

The evaluator detects mistakes such as:

missed_weather

missed_research

incomplete_multi_query

wrong_order_research_first

These mistakes are stored in mistakes_log.json.

Memory converts mistakes → learning rules

After mistakes occur, memory.get_reminders() generates soft rules:

Always use research tool for queries mentioning research / AI / news

Always use weather tool for weather / temperature

Multi-intent queries with “and” → must use both tools

If the same mistake repeats enough times (e.g., wrong order), it escalates into a:

# STRICT RULE
Research MUST run before Weather when both appear


From that point onward, the agent enforces ordered execution:

used:research → used:weather


This demonstrates progressive adaptation, not hard-coded logic.


# How to Run
python main.py


The script runs multiple cycles so you can observe:

early mistakes

feedback

learning behavior improving each run

# What This Demonstrates (Interview Explanation)

This project is not just calling tools — it demonstrates a:

feedback-driven, self-correcting agent that evolves routing rules based on execution outcomes.

# Key capabilities shown:

persistent learning via memory

mistake classification

adaptive routing

rule generalization

strict-rule enforcement after repeated failure

This aligns with modern agentic AI patterns used in tool-calling systems.
