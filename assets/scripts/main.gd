extends Node2D
class_name Globals

static var score = 0
static var playerScale = 1

@onready var player: Area2D = $Player

func _physics_process(delta):
	playerScale = pow(1 + (player.position.x / 100), .6)
