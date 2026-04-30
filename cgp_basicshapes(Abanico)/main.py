import tkinter as tk

root = tk.Tk()
root.title("Breakout Game")
root.resizable(False, False)

canvas = tk.Canvas(root, width=500, height=400, bg="white")
canvas.pack()

# ---------------------------
# REQUIRED SHAPES (TOP)
# ---------------------------
canvas.create_rectangle(20, 20, 120, 70, fill="blue")
canvas.create_oval(150, 20, 250, 70, fill="red")
canvas.create_line(20, 90, 300, 90, width=3)

# ---------------------------
# VARIABLES
# ---------------------------
dx = 3
dy = -3
running = False

# Paddle
paddle = canvas.create_rectangle(200, 350, 300, 360, fill="black")

# Ball
ball = canvas.create_oval(240, 200, 260, 220, fill="green")

# Score
score = 0
score_text = canvas.create_text(400, 20, text="Score: 0", font=("Arial", 12))

# Blocks list
blocks = []

def create_blocks():
    for row in range(3):
        for col in range(5):
            x1 = 50 + col * 80
            y1 = 120 + row * 30
            x2 = x1 + 60
            y2 = y1 + 20
            block = canvas.create_rectangle(x1, y1, x2, y2, fill="orange")
            blocks.append(block)

create_blocks()

# ---------------------------
# CONTROLS
# ---------------------------
def move_left(event):
    if running:
        canvas.move(paddle, -20, 0)

def move_right(event):
    if running:
        canvas.move(paddle, 20, 0)

root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

# ---------------------------
# GAME LOOP
# ---------------------------
def update():
    global dx, dy, score, running

    if not running:
        return

    canvas.move(ball, dx, dy)
    pos = canvas.coords(ball)

    # Wall bounce
    if pos[0] <= 0 or pos[2] >= 500:
        dx = -dx
    if pos[1] <= 100:
        dy = -dy

    # Paddle collision
    paddle_pos = canvas.coords(paddle)
    if pos[3] >= paddle_pos[1] and pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
        dy = -dy

    # Block collision
    for block in blocks[:]:
        block_pos = canvas.coords(block)
        if pos[2] >= block_pos[0] and pos[0] <= block_pos[2] and pos[3] >= block_pos[1] and pos[1] <= block_pos[3]:
            canvas.delete(block)
            blocks.remove(block)
            dy = -dy
            score += 1
            canvas.itemconfig(score_text, text="Score: " + str(score))
            break

    # Win
    if not blocks:
        canvas.create_text(250, 200, text="YOU WIN!", fill="green", font=("Arial", 20))
        running = False
        return

    # Game Over
    if pos[3] >= 400:
        canvas.create_text(250, 200, text="GAME OVER", fill="red", font=("Arial", 20))
        running = False
        return

    root.after(20, update)

# ---------------------------
# BUTTON FUNCTIONS
# ---------------------------
def start_game():
    global running
    if not running:
        running = True
        update()

def pause_game():
    global running
    running = False

def restart_game():
    global dx, dy, score, running

    running = False

    # Reset ball
    canvas.coords(ball, 240, 200, 260, 220)

    # Reset paddle
    canvas.coords(paddle, 200, 350, 300, 360)

    # Reset score
    score = 0
    canvas.itemconfig(score_text, text="Score: 0")

    # Remove old blocks
    for block in blocks:
        canvas.delete(block)
    blocks.clear()

    # Recreate blocks
    create_blocks()

# ---------------------------
# BUTTONS
# ---------------------------
frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="Start", command=start_game).pack(side="left")
tk.Button(frame, text="Pause", command=pause_game).pack(side="left")
tk.Button(frame, text="Restart", command=restart_game).pack(side="left")


canvas.create_text(250, 380, text="Abanico, Aldrean D.", font=("Arial", 12))

root.mainloop()