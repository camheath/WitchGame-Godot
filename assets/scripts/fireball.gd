extends Area2D
class_name  PlayerProjectile
signal fbDead

var speed = 7

func _physics_process(delta):
	position.x += speed
	if position.x > 1000:
		fbDead.emit()
		queue_free()
