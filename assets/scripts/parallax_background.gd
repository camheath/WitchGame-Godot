extends ParallaxBackground
@export var scrollSpeed: int = 4
@onready var player: Area2D = $"../Player"
var total = 0

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _physics_process(delta):
	scroll_base_offset.x -= scrollSpeed * Globals.playerScale
	total += delta
	if total > 1:
		total -= 1
		Globals.score += (int(10 * Globals.playerScale)/5)*5
