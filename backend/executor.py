class Executor:

    def __init__(self, world_state):
        self.world_state = world_state

    # ==========================================
    # EXECUTAR AÇÃO
    # ==========================================

    def execute(self, agent_id: str, action: dict):

        action_type = action.get("action")

        if action_type == "move":
            return self._move(agent_id, action)

        if action_type == "talk":
            return self._talk(agent_id, action)

        if action_type == "pickup":
            return self._pickup(agent_id, action)

        if action_type == "drop":
            return self._drop(agent_id, action)

        if action_type == "use":
            return self._use(agent_id, action)

        if action_type == "read":
            return self._read(agent_id, action)

        if action_type == "write":
            return self._write(agent_id, action)

        if action_type == "save":
            return self._save(agent_id, action)

        return {
            "success": False,
            "error": f"Ação desconhecida: {action_type}"
        }

    # ==========================================
    # MOVE
    # ==========================================

    def _move(self, agent_id, action):

        target = action.get("target")

        agent = self.world_state.get_agent(agent_id)

        if agent is None:
            return {
                "success": False,
                "error": f"Agente inexistente: {agent_id}"
            }

        if not self.world_state.location_exists(target):
            return {
                "success": False,
                "error": f"Local inexistente: {target}"
            }

        current_location = agent.get("location")

        if current_location == target:
            return {
                "success": True,
                "action": "move",
                "agent_id": agent_id,
                "target": target,
                "message": "O agente já está neste local."
            }

        success = self.world_state.set_agent_location(
            agent_id,
            target
        )

        return {
            "success": success,
            "action": "move",
            "agent_id": agent_id,
            "target": target
        }

    # ==========================================
    # TALK
    # ==========================================

    def _talk(self, agent_id, action):

        target = action.get("target")

        agent = self.world_state.get_agent(agent_id)

        if agent is None:
            return {
                "success": False,
                "error": f"Agente inexistente: {agent_id}"
            }

        target_agent = self.world_state.get_agent(target)

        if target_agent is None:
            return {
                "success": False,
                "error": f"Agente alvo inexistente: {target}"
            }

        if agent_id == target:
            return {
                "success": False,
                "error": "Um agente não pode conversar consigo mesmo."
            }

        agent_location = agent.get("location")
        target_location = target_agent.get("location")

        if agent_location != target_location:
            return {
                "success": False,
                "error": (
                    f"Os agentes não estão no mesmo local. "
                    f"{agent_id} está em '{agent_location}' "
                    f"e {target} está em '{target_location}'."
                )
            }

        return {
            "success": True,
            "action": "talk",
            "agent_id": agent_id,
            "target": target,
            "location": agent_location
        }

    # ==========================================
    # PICKUP
    # ==========================================

    def _pickup(self, agent_id, action):

        object_id = action.get("target")

        agent = self.world_state.get_agent(agent_id)

        if agent is None:
            return {
                "success": False,
                "error": f"Agente inexistente: {agent_id}"
            }

        object_state = self.world_state.get_object(object_id)

        if object_state is None:
            return {
                "success": False,
                "error": f"Objeto inexistente: {object_id}"
            }

        # ==========================================
        # VERIFICAR SE O OBJETO PODE SER MOVIDO
        # ==========================================

        properties = self._get_object_properties(object_id)

        if not properties.get("movable", False):
            return {
                "success": False,
                "error": (
                    f"O objeto {object_id} não pode ser movido."
                )
            }

        # ==========================================
        # VERIFICAR SE JÁ ESTÁ SENDO SEGURADO
        # ==========================================

        if object_state["held_by"] is not None:
            return {
                "success": False,
                "error": (
                    f"{object_id} já está sendo segurado."
                )
            }

        # ==========================================
        # VERIFICAR LOCALIZAÇÃO
        # ==========================================

        if object_state["location"] != agent["location"]:
            return {
                "success": False,
                "error": (
                    f"O objeto {object_id} não está no mesmo "
                    f"local que o agente."
                )
            }

        # ==========================================
        # PEGAR OBJETO
        # ==========================================

        success = self.world_state.set_object_held_by(
            object_id,
            agent_id
        )

        if success:
            self.world_state.set_agent_holding(
                agent_id,
                object_id
            )

        return {
            "success": success,
            "action": "pickup",
            "agent_id": agent_id,
            "target": object_id
        }

    # ==========================================
    # DROP
    # ==========================================

    def _drop(self, agent_id, action):

        object_id = action.get("object")
        target = action.get("target")

        if object_id is None:
            return {
                "success": False,
                "error": "Ação drop requer 'object'."
            }

        if target is None:
            return {
                "success": False,
                "error": "Ação drop requer 'target'."
            }

        agent = self.world_state.get_agent(agent_id)

        if agent is None:
            return {
                "success": False,
                "error": f"Agente inexistente: {agent_id}"
            }

        object_state = self.world_state.get_object(object_id)

        if object_state is None:
            return {
                "success": False,
                "error": f"Objeto inexistente: {object_id}"
            }

        # ==========================================
        # VERIFICAR SE O AGENTE ESTÁ SEGURANDO
        # ==========================================

        if agent["holding"] != object_id:
            return {
                "success": False,
                "error": (
                    f"O agente {agent_id} não está "
                    f"segurando {object_id}."
                )
            }

        # ==========================================
        # DESTINO PRECISA SER UM LOCAL
        # ==========================================

        if not self.world_state.location_exists(target):
            return {
                "success": False,
                "error": f"Local inexistente: {target}"
            }

        # ==========================================
        # O AGENTE PRECISA ESTAR NO LOCAL
        # ==========================================

        if agent["location"] != target:
            return {
                "success": False,
                "error": (
                    f"O agente não está no local onde "
                    f"pretende soltar o objeto."
                )
            }

        # ==========================================
        # SOLTAR OBJETO
        # ==========================================

        success = self.world_state.set_object_location(
            object_id,
            target
        )

        if success:
            self.world_state.set_agent_holding(
                agent_id,
                None
            )

        return {
            "success": success,
            "action": "drop",
            "agent_id": agent_id,
            "object": object_id,
            "target": target
        }

    # ==========================================
    # USE
    # ==========================================

    def _use(self, agent_id, action):

        target = action.get("target")

        agent = self.world_state.get_agent(agent_id)

        if agent is None:
            return {
                "success": False,
                "error": f"Agente inexistente: {agent_id}"
            }

        object_state = self.world_state.get_object(target)

        if object_state is None:
            return {
                "success": False,
                "error": f"Objeto inexistente: {target}"
            }

        properties = self._get_object_properties(target)

        if not properties.get("usable", False):
            return {
                "success": False,
                "error": (
                    f"O objeto {target} não pode ser usado."
                )
            }

        if object_state["location"] != agent["location"]:
            return {
                "success": False,
                "error": (
                    f"O objeto {target} não está no mesmo "
                    f"local que o agente."
                )
            }

        return {
            "success": True,
            "action": "use",
            "agent_id": agent_id,
            "target": target
        }

    # ==========================================
    # READ
    # ==========================================

    def _read(self, agent_id, action):

        target = action.get("target")

        agent = self.world_state.get_agent(agent_id)

        if agent is None:
            return {
                "success": False,
                "error": f"Agente inexistente: {agent_id}"
            }

        object_state = self.world_state.get_object(target)

        if object_state is None:
            return {
                "success": False,
                "error": f"Objeto inexistente: {target}"
            }

        properties = self._get_object_properties(target)

        if not properties.get("readable", False):
            return {
                "success": False,
                "error": (
                    f"O objeto {target} não pode ser lido."
                )
            }

        if object_state["location"] != agent["location"]:
            return {
                "success": False,
                "error": (
                    f"O objeto {target} não está no mesmo "
                    f"local que o agente."
                )
            }

        return {
            "success": True,
            "action": "read",
            "agent_id": agent_id,
            "target": target
        }

    # ==========================================
    # WRITE
    # ==========================================

    def _write(self, agent_id, action):

        target = action.get("target")

        agent = self.world_state.get_agent(agent_id)

        if agent is None:
            return {
                "success": False,
                "error": f"Agente inexistente: {agent_id}"
            }

        object_state = self.world_state.get_object(target)

        if object_state is None:
            return {
                "success": False,
                "error": f"Objeto inexistente: {target}"
            }

        properties = self._get_object_properties(target)

        if not properties.get("writable", False):
            return {
                "success": False,
                "error": (
                    f"O objeto {target} não pode ser escrito."
                )
            }

        if object_state["location"] != agent["location"]:
            return {
                "success": False,
                "error": (
                    f"O objeto {target} não está no mesmo "
                    f"local que o agente."
                )
            }

        return {
            "success": True,
            "action": "write",
            "agent_id": agent_id,
            "target": target
        }

    # ==========================================
    # SAVE
    # ==========================================

    def _save(self, agent_id, action):

        agent = self.world_state.get_agent(agent_id)

        if agent is None:
            return {
                "success": False,
                "error": f"Agente inexistente: {agent_id}"
            }

        return {
            "success": True,
            "action": "save",
            "agent_id": agent_id
        }

    # ==========================================
    # PROPRIEDADES DO OBJETO
    # ==========================================

    def _get_object_properties(self, object_id):

        for obj in self.world_state.world.get("objects", []):

            if obj.get("id") == object_id:
                return obj.get("properties", {})

        return {}