from langgraph.graph import StateGraph

def build_graph(research_agent, critic_agent, synthesizer_agent):
    workflow = StateGraph()

    workflow.add_node("research", research_agent.run)
    workflow.add_node("critic", critic_agent.evaluate)
    workflow.add_node("synthesize", synthesizer_agent.synthesize)

    workflow.set_entry_point("research")
    workflow.add_edge("research", "critic")
    workflow.add_edge("critic", "synthesize")

    return workflow.compile()
