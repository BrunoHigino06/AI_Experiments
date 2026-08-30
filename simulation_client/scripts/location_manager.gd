extends Node2D

func get_location_position(location_name: String) -> Vector2:
	var location = get_node("../Locations/" + location_name)
	return location.global_position
