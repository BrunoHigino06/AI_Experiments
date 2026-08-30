extends CharacterBody2D

@export var agent_id: String = "agent_001"

@onready var navigation_agent: NavigationAgent2D = $NavigationAgent2D

var target_position: Vector2
var moving := false
var speed := 100.0

func _ready():
	if navigation_agent == null:
		return

	navigation_agent.path_desired_distance = 5.0
	navigation_agent.target_desired_distance = 5.0


func move_to(destination: Vector2):
	target_position = destination
	moving = true

	if navigation_agent == null:
		moving = false
		return

	navigation_agent.target_position = destination

func _physics_process(_delta):
	if not moving or navigation_agent == null:
		return

	if navigation_agent.is_navigation_finished():
		velocity = Vector2.ZERO
		moving = false
		return

	var next_position = navigation_agent.get_next_path_position()
	if next_position == Vector2.ZERO:
		return

	var direction = global_position.direction_to(next_position)
	velocity = direction * speed
	move_and_slide()
