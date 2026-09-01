extends Node

@onready var location_manager = $"../LocationManager"
@onready var agents_container = get_node("/root/Main/world/Agents")


func execute_command(command: Dictionary):
	print("Comando recebido: ", command)

	var action = command.get("action", {})

	if action is not Dictionary:
		return

	var action_type = action.get("type", "")
	var target = action.get("target", "")
	var agent_id = command.get("agent_id", "")

	if action_type == "move":
		var agent = find_agent_by_id(agent_id)

		if agent == null:
			print("Agent não encontrado: ", agent_id)
			return

		move_agent(agent, target)


func find_agent_by_id(agent_id: String) -> CharacterBody2D:
	for agent in agents_container.get_children():
		if agent.get("agent_id") == agent_id:
			return agent

	return null


func move_agent(agent: CharacterBody2D, location_name: String):
	var destination = location_manager.get_location_position(location_name)

	agent.move_to(destination)
