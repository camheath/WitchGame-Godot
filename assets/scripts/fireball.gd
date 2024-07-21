extends Area2D
class_name  PlayerProjectile

var speed = 5

func _physics_process(delta):
	position.x += speed
	if position.x > 1000:
		queue_free()
