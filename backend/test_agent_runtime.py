from agent_runtime import AgentRuntime


runtime = AgentRuntime("agent_001")


perception = {
    "internal_state": {
        "hunger": 20,
        "energy": 90,
        "fatigue": 10,
        "stress": 15
    },
    "environment": {
        "location": "office",
        "nearby": [
            "desk",
            "chair_1",
            "chair_2",
            "kitchen",
            "computer"
        ]
    },
    "known_agents": []
}


result = runtime.decide(perception)


print()
print("================================")
print("RESULTADO FINAL")
print("================================")
print(result)