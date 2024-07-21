extends Area2D

@export var batSpeed: int = 5


func _physics_process(delta):
	position.x -= batSpeed
	if position.x < -100:
		queue_free()
