import json
from pathlib import Path

from world_state import WorldState
from executor import Executor
from agent_runtime import AgentRuntime


BASE_DIR = Path(__file__).resolve().parent

world_path = (
    BASE_DIR
    / "experiments"
    / "office_promotion"
    / "world.json"
)


# ==========================================
# CARREGAR WORLD
# ==========================================

with open(
    world_path,
    "r",
    encoding="utf-8"
) as file:
    world = json.load(file)


# ==========================================
# CRIAR WORLD STATE
# ==========================================

world_state = WorldState(world)


# ==========================================
# CRIAR EXECUTOR
# ==========================================

executor = Executor(world_state)


# ==========================================
# CRIAR AGENT RUNTIME
# ==========================================

agent_id = "agent_001"

runtime = AgentRuntime(agent_id)


# ==========================================
# PERCEPÇÃO DO AGENTE
# ==========================================

perception = {
    "location": "office",
    "nearby": [
        "chair_1",
        "chair_2",
        "desk_1",
        "kitchen"
    ]
}


# ==========================================
# MOSTRAR ESTADO INICIAL
# ==========================================

print()
print("================================")
print("ESTADO INICIAL")
print("================================")

print(
    json.dumps(
        world_state.get_state(),
        ensure_ascii=False,
        indent=2
    )
)


# ==========================================
# AGENTE PENSA
# ==========================================

result = runtime.decide(perception)


decision = result["decision"]
plan = result["plan"]


# ==========================================
# MOSTRAR DECISÃO
# ==========================================

print()
print("================================")
print("DECISÃO GERADA PELO AGENTE")
print("================================")

print(
    json.dumps(
        decision,
        ensure_ascii=False,
        indent=2
    )
)


# ==========================================
# MOSTRAR PLANO
# ==========================================

print()
print("================================")
print("PLANO GERADO PELO AGENTE")
print("================================")

print(
    json.dumps(
        plan,
        ensure_ascii=False,
        indent=2
    )
)


# ==========================================
# EXECUTAR PLANO
# ==========================================

steps = plan.get("steps", [])


for index, action in enumerate(steps, start=1):

    print()
    print("================================")
    print(f"EXECUTANDO PASSO {index}")
    print("================================")

    print(
        json.dumps(
            action,
            ensure_ascii=False,
            indent=2
        )
    )

    result = executor.execute(
        agent_id,
        action
    )

    print()
    print("RESULTADO:")

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )
    )


# ==========================================
# ESTADO FINAL
# ==========================================

print()
print("================================")
print("ESTADO FINAL")
print("================================")

print(
    json.dumps(
        world_state.get_state(),
        ensure_ascii=False,
        indent=2
    )
)