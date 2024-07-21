extends Label
@onready var player: Area2D = $"../Player"

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	text = "Health: "+str(player.health)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_player_health_change() -> void:
	text = "Health: "+str(player.health)
