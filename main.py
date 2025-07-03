from graphics import Canvas
import time
import random
import math

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600
PADDLE_Y = CANVAS_HEIGHT - 30
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 15
BALL_RADIUS = 10

BRICK_GAP = 5
BRICK_WIDTH = (CANVAS_WIDTH - BRICK_GAP*9) / 10
BRICK_HEIGHT = 10
NBRICKS = 10
ROWS = 10
INITIAL_VELOCITY = 2
START_X = 250
START_Y = 300
DELAY = 0.0001
LIVES = 3

COLORS = ["red", "red", "orange", "orange", "yellow", "yellow", "green", "green", "cyan", "cyan"]

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    bricks = create_bricks(canvas)
    paddle = create_paddle(canvas)
    ball = create_ball(canvas)

    score = 0
    lives = LIVES
    #Code to create Score & Lives in top left hand corner of canvas
    score_text = canvas.create_text(10, 10, text=f"Score: {score}", font="Arial", font_size=16, color="blue")
    lives_text = canvas.create_text(10, 30, text=f"Lives: {lives}", font="Arial", font_size=16, color="blue")

    #
    x_velocity = INITIAL_VELOCITY
    y_velocity = INITIAL_VELOCITY
    ball_x = START_X
    ball_y = START_Y

    canvas.moveto(ball, ball_x, ball_y)
    

    while lives > 0:
        # Bounce off left/right walls
        if ball_x <= 0 or ball_x + BALL_RADIUS * 2 >= CANVAS_WIDTH:
            x_velocity *= -1

        # Bounce off top
        if ball_y <= 0:
            y_velocity *= -1

        # Ball movement
        ball_x += x_velocity
        ball_y += y_velocity
        canvas.moveto(ball, ball_x, ball_y)

        # Paddle movement
        mouse_x = canvas.get_mouse_x()
        new_x = max(0, min(mouse_x - PADDLE_WIDTH // 2, CANVAS_WIDTH - PADDLE_WIDTH))
        canvas.moveto(paddle, new_x, PADDLE_Y)

        # Collision detection
        canvas.coords(ball)
        colliders = canvas.find_overlapping(ball_x, ball_y, ball_x + 2 * (BALL_RADIUS), ball_y + 2 * (BALL_RADIUS))

        for obj in colliders:
            if obj == ball:
                continue
            if obj == paddle:
                y_velocity = -abs(y_velocity)
                break
            elif obj in bricks:
                canvas.delete(obj)
                bricks.remove(obj)
                y_velocity *= -1
                score += 1
                canvas.change_text(score_text, f"Score: {score}")
                break
            if len(bricks) == 0:
                canvas.draw_text("You Win!", CANVAS_WIDTH/2 - 40, CANVAS_HEIGHT/2, "green")
                time.sleep(3)
                return
            last_speed_milestone = 0
            # Speed up every 5 bricks
            if score % 5 == 0 and score != 0 and score != last_speed_milestone:
                    x_velocity *= 1.2
                    y_velocity *= 1.2
                    last_speed_milestone = score

                    # Display "Speed Up!" message
                    speed_text = canvas.create_text(
                        CANVAS_WIDTH/2, CANVAS_HEIGHT/2, 
                        text="Speed Up!", font="Arial", size=24, color="red"
                    )
                    time.sleep(1)
                    canvas.delete(speed_text)
                    break


        # Ball falls below bottom
        if ball_y + BALL_RADIUS * 2 >= CANVAS_HEIGHT:
            lives -= 1
            canvas.change_text(lives_text, f"Lives: {lives}")
            if lives > 0:
                # Reset ball position
                ball_x = START_X
                ball_y = START_Y
                x_velocity = INITIAL_VELOCITY
                y_velocity = INITIAL_VELOCITY
                canvas.moveto(ball, ball_x, ball_y)
                
            else:
                canvas.create_text(CANVAS_WIDTH/2 - 75, CANVAS_HEIGHT/2, "Game Over","Arial",30, "red")
                break

        time.sleep(DELAY)

def create_bricks(canvas):
    #Added a list for all the bricks and loop to create them in different rows
    bricks = []
    for row in range(ROWS):
        color = COLORS[row]
        y1 = (row + 3) * BRICK_HEIGHT * 2
        y2 = y1 + BRICK_HEIGHT
        for col in range(NBRICKS):
            x1 = col * (BRICK_WIDTH + BRICK_GAP)
            x2 = x1 + BRICK_WIDTH
            brick = canvas.create_rectangle(x1, y1, x2, y2, color)
            bricks.append(brick)
    return bricks

def create_paddle(canvas):
    x1 = (CANVAS_WIDTH - PADDLE_WIDTH) / 2
    x2 = x1 + PADDLE_WIDTH
    y1 = PADDLE_Y
    y2 = y1 + PADDLE_HEIGHT
    return canvas.create_rectangle(x1, y1, x2, y2, "black")

def create_ball(canvas):
    return canvas.create_oval(START_X, START_Y, START_X + BALL_RADIUS * 2, START_Y + BALL_RADIUS * 2)
    

if __name__ == '__main__':
    main()