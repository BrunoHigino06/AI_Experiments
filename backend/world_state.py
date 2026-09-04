import copy


class WorldState:

    def __init__(self, world: dict):
        self.world = copy.deepcopy(world)

        self.agent_states = {}
        self.object_states = {}

        self._initialize()

    def _initialize(self):

        # ==========================================
        # AGENTES
        # ==========================================

        for agent in self.world.get("agents", []):

            agent_id = agent["id"]

            self.agent_states[agent_id] = {
                "location": agent.get("location"),
                "holding": None
            }

        # ==========================================
        # OBJETOS
        # ==========================================

        for obj in self.world.get("objects", []):

            object_id = obj["id"]

            self.object_states[object_id] = {
                "location": obj.get("location"),
                "held_by": None,
                "position": None
            }

    # ==========================================
    # AGENTES
    # ==========================================

    def get_agent(self, agent_id: str):

        return self.agent_states.get(agent_id)

    def set_agent_location(
        self,
        agent_id: str,
        location_id: str
    ):

        if agent_id not in self.agent_states:
            return False

        self.agent_states[agent_id]["location"] = location_id

        return True

    def set_agent_holding(
        self,
        agent_id: str,
        object_id: str | None
    ):

        if agent_id not in self.agent_states:
            return False

        self.agent_states[agent_id]["holding"] = object_id

        return True

    # ==========================================
    # OBJETOS
    # ==========================================

    def get_object(self, object_id: str):

        return self.object_states.get(object_id)

    def set_object_location(
        self,
        object_id: str,
        location_id: str
    ):

        if object_id not in self.object_states:
            return False

        self.object_states[object_id]["location"] = location_id
        self.object_states[object_id]["held_by"] = None

        return True

    def set_object_held_by(
        self,
        object_id: str,
        agent_id: str
    ):

        if object_id not in self.object_states:
            return False

        self.object_states[object_id]["held_by"] = agent_id

        return True

    # ==========================================
    # ENTIDADES
    # ==========================================

    def entity_exists(self, entity_id: str):

        if entity_id in self.agent_states:
            return True

        if entity_id in self.object_states:
            return True

        for location in self.world.get("locations", []):

            if location["id"] == entity_id:
                return True

        return False

    # ==========================================
    # VERIFICAR LOCAL
    # ==========================================

    def location_exists(self, location_id: str):

        for location in self.world.get("locations", []):

            if location["id"] == location_id:
                return True

        return False

    # ==========================================
    # ESTADO COMPLETO
    # ==========================================

    def get_state(self):

        return {
            "agents": copy.deepcopy(
                self.agent_states
            ),
            "objects": copy.deepcopy(
                self.object_states
            )
        }