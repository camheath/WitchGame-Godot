extends Area2D
class_name Enemy

@export var batSpeed: int = 5


func _physics_process(_delta):
	position.x -= batSpeed
	if position.x < -100:
		queue_free()



func _on_area_entered(area: Area2D) -> void:
	if area is PlayerProjectile:
		area.fbDead.emit()
		area.queue_free()
		queue_free()
