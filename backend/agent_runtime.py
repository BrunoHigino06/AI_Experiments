class AgentRuntime:

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def decide(self, perception: dict) -> dict:

        print()
        print("================================")
        print(f"PERCEPÇÃO DO {self.agent_id}")
        print(perception)
        print("================================")

        return {
            "decision": "Vou para a cozinha.",
            "goal": "ir até a cozinha",
            "action": {
                "type": "move",
                "target": "kitchen"
            }
        }