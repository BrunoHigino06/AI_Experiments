extends Node

@onready var command_handler = $"../CommandHandler"

var socket := WebSocketPeer.new()
var url := "ws://127.0.0.1:8000/ws"
var state_sent := false


func _ready():
	print("Conectando ao backend...")
	socket.connect_to_url(url)


func _process(_delta):
	socket.poll()

	var state = socket.get_ready_state()

	if state == WebSocketPeer.STATE_OPEN:

		if not state_sent:
			send_agent_states()
			state_sent = true

		while socket.get_available_packet_count() > 0:
			var message = socket.get_packet().get_string_from_utf8()

			print("Mensagem recebida do backend: ", message)

			var json = JSON.parse_string(message)

			if json is Dictionary:
				if json.get("type", "") == "command":
					command_handler.execute_command(json.get("data", {}))


func send_agent_states():
	var agents = $"../Agents".get_children()

	for agent in agents:
		if agent.has_method("get_state"):
			var state = agent.get_state()

			socket.send_text(JSON.stringify({
				"type": "agent_state",
				"data": state
			}))
