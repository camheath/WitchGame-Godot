extends Node
var time = 0.0
var interval = 2
var batScene = preload("res://assets/scenes/bat.tscn")
var fireballScene = preload("res://assets/scenes/fireball.tscn")
@onready var player: Area2D = $"../Player"
var fbCount = 0

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	time += delta
	if time > interval:
		time -= interval
		interval *= .99
		var batInstance = batScene.instantiate()
		add_child(batInstance)
		batInstance.position.x = 1000
		batInstance.position.y = randi_range(0, 800)
	if Input.is_action_just_pressed("shoot") && fbCount < 6:
		fbCount += 1
		var fireballInstance = fireballScene.instantiate()
		add_child(fireballInstance)
		fireballInstance.fbDead.connect(dead)
		fireballInstance.position.x = player.position.x
		fireballInstance.position.y = player.position.y

func dead():
	fbCount -= 1
