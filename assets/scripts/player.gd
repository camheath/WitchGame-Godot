extends Area2D

@export var speed: int = 15
var health = 10
signal healthChange
@onready var sfx_hurt: AudioStreamPlayer = $SFX_Hurt


func _physics_process(delta):
	if Input.is_action_pressed("left"):
		position.x -= int(speed * 1.2)
		if position.x < 48:
			position.x = 48
	if Input.is_action_pressed("right"):
		position.x += speed
		if position.x > 860:
			position.x = 860
	if Input.is_action_pressed("up"):
		position.y -= speed
		if position.y < 56:
			position.y = 56
	if Input.is_action_pressed("down"):
		position.y += speed
		if position.y > 584:
			position.y = 584


func _on_area_entered(area: Area2D) -> void:
	if area is Enemy:
		health -= 1
		healthChange.emit()
		area.queue_free()
		sfx_hurt.play()
