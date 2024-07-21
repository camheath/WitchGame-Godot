extends Node

var batScene = preload("res://assets/scenes/bat.tscn")

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	var batInstance = batScene.instantiate()
	add_child(batInstance)
	batInstance.position.x = 1000
	batInstance.position.y = randi_range(0, 800)
