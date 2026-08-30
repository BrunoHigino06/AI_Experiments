extends Node


@onready var location_manager = $"../LocationManager"


func move_agent(agent: CharacterBody2D, location_name: String):
	if agent == null:
		return

	var destination = location_manager.get_location_position(location_name)
	agent.move_to(destination)


func execute_command(command: Dictionary):
	var agent_id = command.get("agent_id", "")
	var action = command.get("action", "")
	var target = command.get("target", "")

	print("Comando recebido: ", command)

	if action == "move":
		var agent = get_agent_by_id(agent_id)
		move_agent(agent, target)


func get_agent_by_id(id: String):
	for agent in $"../Agents".get_children():
		if agent.agent_id == id:
			return agent

	return null
	
