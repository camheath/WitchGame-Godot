extends Area2D

@export var speed: int = 20

func _physics_process(delta):
	if Input.is_action_pressed("left"):
		position.x -= speed
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
	#position.x += scrollSpeed
