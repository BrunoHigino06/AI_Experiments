class EventSystem:

    def __init__(self):
        self.events = []
        self.next_event_id = 1

    # ==========================================
    # CRIAR EVENTO
    # ==========================================

    def create_event(
        self,
        event_type: str,
        agent_id: str,
        data: dict
    ):

        event = {
            "id": f"event_{self.next_event_id:04d}",
            "type": event_type,
            "agent_id": agent_id,
            "data": data
        }

        self.next_event_id += 1

        self.events.append(event)

        return event

    # ==========================================
    # EVENTO DE AÇÃO
    # ==========================================

    def action_result(
        self,
        agent_id: str,
        action: dict,
        result: dict
    ):

        if result.get("success"):

            return self.create_event(
                event_type="action_completed",
                agent_id=agent_id,
                data={
                    "action": action,
                    "result": result
                }
            )

        return self.create_event(
            event_type="action_failed",
            agent_id=agent_id,
            data={
                "action": action,
                "result": result
            }
        )

    # ==========================================
    # TODOS OS EVENTOS
    # ==========================================

    def get_events(self):

        return list(self.events)

    # ==========================================
    # LIMPAR EVENTOS
    # ==========================================

    def clear(self):

        self.events.clear()