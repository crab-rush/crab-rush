"""Test minimal Arcade."""
import arcade


class TestWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Test", resizable=False)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_filled(400, 300, 800, 600, arcade.color.YELLOW)
        arcade.draw_text("CA MARCHE !", 400, 300, arcade.color.BLACK, 40, anchor_x="center")


if __name__ == "__main__":
    TestWindow().run()
