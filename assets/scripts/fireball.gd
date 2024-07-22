extends Area2D
class_name  PlayerProjectile
signal fbDead
@onready var sfx_fire: AudioStreamPlayer = $SFX_Fire

var speed = 7

func _ready() -> void:
	sfx_fire.play()

func _physics_process(delta):
	position.x += speed
	if position.x > 1000:
		fbDead.emit()
		queue_free()
