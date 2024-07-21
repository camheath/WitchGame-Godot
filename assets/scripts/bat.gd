extends Area2D
class_name Enemy

@export var batSpeed: int = 5


func _physics_process(delta):
	position.x -= batSpeed
	if position.x < -100:
		queue_free()
