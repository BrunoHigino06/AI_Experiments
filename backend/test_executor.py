import json
from pathlib import Path

from world_state import WorldState
from executor import Executor
from agent_runtime import AgentRuntime
from event_system import EventSystem


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
# CRIAR EVENT SYSTEM
# ==========================================

event_system = EventSystem()

# ==========================================
# CRIAR AGENT RUNTIME
# ==========================================

agent_id = "agent_001"

runtime = AgentRuntime(agent_id)


# ==========================================
# PERCEPÇÃO INICIAL
# ==========================================

perception = {
    "location": "office",

    "visible_agents": [
        "lidia",
        "carlos"
    ],

    "known_agents": [
        "lidia",
        "carlos",
        "tais"
    ],

    "nearby": [
        "chair_1",
        "desk_1",
        "computer_1",
        "kitchen"
    ]
}


# ==========================================
# LOOP DO AGENTE
# ==========================================

MAX_TURNS = 10

for turn in range(1, MAX_TURNS + 1):

    print()
    print("################################")
    print(f"TURNO {turn}")
    print("################################")


    # ======================================
    # AGENTE PENSA
    # ======================================

    result = runtime.decide(perception)

    decision = result["decision"]
    plan = result["plan"]

    print()
    print("DECISÃO:")
    print(
        json.dumps(
            decision,
            ensure_ascii=False,
            indent=2
        )
    )


    # ======================================
    # VERIFICAR PLANO
    # ======================================

    steps = plan.get("steps", [])

    if not steps:

        print()
        print("O agente não possui ações para executar.")

        break


    # ======================================
    # PEGAR APENAS A PRIMEIRA AÇÃO
    # ======================================

    action = steps[0]

    print()
    print("AÇÃO ESCOLHIDA:")
    print(
        json.dumps(
            action,
            ensure_ascii=False,
            indent=2
        )
    )


    # ======================================
    # EXECUTAR
    # ======================================

    result = executor.execute(
        agent_id,
        action
    )

    print()
    print("RESULTADO DA EXECUÇÃO:")

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )
    )


    # ======================================
    # CRIAR EVENTO
    # ======================================

    event = event_system.action_result(
        agent_id,
        action,
        result
    )

    print()
    print("EVENTO GERADO:")

    print(
        json.dumps(
            event,
            ensure_ascii=False,
            indent=2
        )
    )


    # ======================================
    # SUCESSO
    # ======================================

    if result.get("success"):

        print()
        print("AÇÃO EXECUTADA COM SUCESSO.")

        # Atualizar percepção básica
        perception["location"] = (
            world_state
            .get_agent(agent_id)
            .get("location")
        )

        continue

    # ======================================
    # FALHA
    # ======================================

    print()
    print("AÇÃO FALHOU.")

    print()
    print("GERANDO EVENTO...")


    event = event_system.action_result(
        agent_id,
        action,
        result
    )

    perception["last_event"] = event

    print(
        json.dumps(
            event,
            ensure_ascii=False,
            indent=2
        )
    )


    # ======================================
    # NOVA PERCEPÇÃO
    # ======================================

    perception["last_event"] = event

    print()
    print("NOVA PERCEPÇÃO:")

    print(
        json.dumps(
            perception,
            ensure_ascii=False,
            indent=2
        )
    )


    # ======================================
    # IMPORTANTE
    # ======================================
    #
    # Não executamos o restante do plano.
    #
    # O agente volta para o LLM e decide
    # novamente com base no que aconteceu.
    #

    print()
    print("O AGENTE DEVE TOMAR UMA NOVA DECISÃO.")


# ==========================================
# ESTADO FINAL
# ==========================================

print()
print("################################")
print("ESTADO FINAL")
print("################################")

print(
    json.dumps(
        world_state.get_state(),
        ensure_ascii=False,
        indent=2
    )
)