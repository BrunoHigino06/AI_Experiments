import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class AgentRuntime:

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5-nano"
        )

        self.context_path = (
            BASE_DIR
            / "backend"
            / "experiments"
            / "office_promotion"
            / "context.txt"
        )

        self.world_path = (
            BASE_DIR
            / "backend"
            / "experiments"
            / "office_promotion"
            / "world.json"
        )

        self.decision_prompt_path = (
            BASE_DIR
            / "backend"
            / "prompts"
            / "agent_decision.txt"
        )

        self.planner_prompt_path = (
            BASE_DIR
            / "backend"
            / "prompts"
            / "action_planner.txt"
        )

    def decide(self, perception: dict) -> dict:

        print()
        print("================================")
        print(f"PERCEPÇÃO DO {self.agent_id}")
        print("================================")
        print(json.dumps(
            perception,
            ensure_ascii=False,
            indent=2
        ))
        print("================================")

        # ==========================================
        # CARREGAR CONTEXTO DO EXPERIMENTO
        # ==========================================

        with open(
            self.context_path,
            "r",
            encoding="utf-8"
        ) as file:
            experiment_context = file.read()

        # ==========================================
        # CARREGAR WORLD
        # ==========================================

        with open(
            self.world_path,
            "r",
            encoding="utf-8"
        ) as file:
            world = json.load(file)

        # ==========================================
        # LLM 1 — DECISION MAKER
        # ==========================================

        with open(
            self.decision_prompt_path,
            "r",
            encoding="utf-8"
        ) as file:
            decision_prompt = file.read()

        decision_prompt = decision_prompt.replace(
            "{{agent_id}}",
            self.agent_id
        )

        decision_prompt = decision_prompt.replace(
            "{{perception}}",
            json.dumps(
                perception,
                ensure_ascii=False,
                indent=2
            )
        )

        decision_input = f"""
{decision_prompt}

CONTEXTO DO EXPERIMENTO:

{experiment_context}

MUNDO CONHECIDO:

{json.dumps(
    world,
    ensure_ascii=False,
    indent=2
)}
"""

        response = self.client.responses.create(
            model=self.model,
            input=decision_input
        )

        decision = json.loads(
            response.output_text
        )

        print()
        print("================================")
        print(f"DECISÃO DO {self.agent_id}")
        print("================================")
        print(json.dumps(
            decision,
            ensure_ascii=False,
            indent=2
        ))

        # ==========================================
        # LLM 2 — ACTION PLANNER
        # ==========================================

        with open(
            self.planner_prompt_path,
            "r",
            encoding="utf-8"
        ) as file:
            planner_prompt = file.read()

        planner_input = planner_prompt

        # ==========================================
        # IDENTIDADE DO AGENTE
        # ==========================================

        planner_input = planner_input.replace(
            "{{agent}}",
            self.agent_id
        )

        # ==========================================
        # INTENÇÃO
        # ==========================================

        planner_input = planner_input.replace(
            "{{intent}}",
            decision.get("decision", "")
        )

        # ==========================================
        # OBJETIVO
        # ==========================================

        planner_input = planner_input.replace(
            "{{goal}}",
            decision.get("goal", "")
        )

        # ==========================================
        # PLANO DE ALTO NÍVEL
        # ==========================================

        planner_input = planner_input.replace(
            "{{plan}}",
            json.dumps(
                decision.get("plan", []),
                ensure_ascii=False,
                indent=2
            )
        )

        # ==========================================
        # WORLD
        #
        # O WORLD é a fonte de verdade sobre
        # entidades, objetos, locais e seus IDs.
        # ==========================================

        planner_input = planner_input.replace(
            "{{world_state}}",
            json.dumps(
                world,
                ensure_ascii=False,
                indent=2
            )
        )

        # ==========================================
        # PERCEPÇÃO ATUAL
        #
        # Mostra o que o agente está percebendo
        # neste momento.
        # ==========================================

        planner_input = planner_input.replace(
            "{{perception}}",
            json.dumps(
                perception,
                ensure_ascii=False,
                indent=2
            )
        )

        # ==========================================
        # CAPACIDADES DO AGENTE
        # ==========================================

        capabilities = [
            "move",
            "talk",
            "interact",
            "pickup",
            "drop",
            "read",
            "write",
            "use",
            "save"
        ]

        planner_input = planner_input.replace(
            "{{capabilities}}",
            json.dumps(
                capabilities,
                ensure_ascii=False,
                indent=2
            )
        )

        # ==========================================
        # CHAMAR LLM 2
        # ==========================================

        planner_response = self.client.responses.create(
            model=self.model,
            input=planner_input
        )

        planned_actions = json.loads(
            planner_response.output_text
        )

        # ==========================================
        # MOSTRAR PLANO EXECUTÁVEL
        # ==========================================

        print()
        print("================================")
        print(f"PLANO EXECUTÁVEL DO {self.agent_id}")
        print("================================")
        print(json.dumps(
            planned_actions,
            ensure_ascii=False,
            indent=2
        ))

        # ==========================================
        # RESULTADO FINAL
        # ==========================================

        return {
            "decision": decision,
            "plan": planned_actions
        }