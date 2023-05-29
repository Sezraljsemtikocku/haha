from game import Game

game = Game()

while game.running:
    game.curr_menu.display_menu()
    game.game_loop()

#TODO:
#fix the mouse going into the fucking floor - KINDA FIXED ?????? (its ok if we dont find any better fix)
#fix the cat going into the fucking walls
#fix the cat going into fucking orbit
#fix the funny-ahh physics