extends ParallaxBackground

@export var scrollSpeed: int = 4
@onready var player: Area2D = $"../Player"

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _physics_process(delta):
	scroll_base_offset.x -= scrollSpeed * (pow(1 + (player.position.x / 100), .6))
