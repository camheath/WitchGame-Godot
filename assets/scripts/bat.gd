extends Area2D
class_name Enemy

static var score

@export var batSpeed: int = 3
@onready var animation_player: AnimationPlayer = $AnimationPlayer


func _physics_process(_delta):
	position.x -= batSpeed * Globals.playerScale
	if position.x < -100:
		queue_free()



func _on_area_entered(area: Area2D) -> void:
	if area is PlayerProjectile:
		area.fbDead.emit()
		area.queue_free()
		Globals.score += 100
		animation_player.play("Die")
