class ResearchAgent:
    def __init__(self, rag_pipeline):
        self.rag = rag_pipeline

    def run(self, query):
        return self.rag.generate(query)


class CriticAgent:
    def evaluate(self, answer, contexts):
        score = sum(1 for ctx in contexts if ctx[:20] in answer)
        return {"faithfulness_score": score / len(contexts)}


class SynthesizerAgent:
    def synthesize(self, research_output, critique):
        return {
            "final_answer": research_output["answer"],
            "faithfulness_score": critique["faithfulness_score"],
            "tokens_used": research_output["tokens_used"],
        }


class AgentOrchestrator:
    def __init__(self, research_agent, critic_agent, synthesizer_agent):
        self.research_agent = research_agent
        self.critic_agent = critic_agent
        self.synthesizer_agent = synthesizer_agent

    def handle_query(self, query):
        research = self.research_agent.run(query)
        critique = self.critic_agent.evaluate(
            research["answer"], research["contexts"]
        )
        final = self.synthesizer_agent.synthesize(research, critique)
        return final
