import tkinter as tk
import turtle
import random

class RunawayGame:
    def __init__(self, canvas, runner, chaser, coin_, catch_radius=25):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.coin_ = coin_
        self.catch_radius2 = catch_radius ** 2
        self.coin_total = 0
        self.time_left = 20  # 20초 타이머 설정

        # Ghost와 Pacman 이미지의 상대 경로 설정 (스크립트 실행 디렉토리 기준)
        self.canvas.register_shape('4주차 과제/ghost.gif')
        self.canvas.register_shape('4주차 과제/pacman.gif')

        # Initialize runner and chaser with GIFs
        self.runner.shape('4주차 과제/ghost.gif')
        self.runner.penup()

        self.chaser.shape('4주차 과제/pacman.gif')
        self.chaser.penup()

        self.coin_.shape('circle')
        self.coin_.color('yellow')
        self.coin_.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

        # Timer display
        self.timer_turtle = turtle.RawTurtle(canvas)
        self.timer_turtle.hideturtle()
        self.timer_turtle.penup()
        self.timer_turtle.color('white')
        self.timer_turtle.setpos(-300, 300)

        # Draw initial timer
        self.update_timer()
        self.update_coin_counter()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def coin_is_catched(self):
        p = self.coin_.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        # Chaser는 사용자 입력에 따라 움직임

        is_catched = self.is_catched()
        coin_is_catched = self.coin_is_catched()
        
        # 코인 카운터 업데이트
        if coin_is_catched:
            self.coin_total += 1
            self.coin_.random_pos()  # 코인 새 위치로 이동
            self.update_coin_counter()  # 코인 카운터 업데이트

        # Update timer
        self.time_left -= self.ai_timer_msec / 1000  # 타이머 감소
        self.update_timer()

        if self.time_left <= 0 or is_catched:
            self.end_game()
        elif self.coin_total == 10:  # 코인 총 획득량에 따른 종료 조건
            self.end_game()
        else:
            self.canvas.ontimer(self.step, self.ai_timer_msec)

    def update_timer(self):
        self.timer_turtle.clear()
        self.timer_turtle.write(f'Time left: {int(self.time_left)}', align='left', font=('Arial', 16, 'normal'))

    def update_coin_counter(self):
        self.drawer.setpos(-300, 250)  # 위치 수정
        self.drawer.clear()
        self.drawer.write(f'Coins collected: {self.coin_total}', align='left', font=('Arial', 16, 'normal'))

    def end_game(self):
        self.canvas.getcanvas().winfo_toplevel().destroy()
        print(f'Final Score: {self.coin_total}')  # 최종 점수 출력

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass  # AI 동작 없음

class RandomCoin(turtle.RawTurtle):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.canvas = canvas
        self.hideturtle()
        self.penup()
        self.random_pos()

    def random_pos(self):
        x = random.randint(-300, 300)
        y = random.randint(-300, 300)
        self.goto(x, y)
        self.dot(20, 'yellow')
        self.canvas.ontimer(self.random_pos, 5000)

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        # Chaser는 방향키 입력에 따라 움직임
        pass  # ManualMover가 키 입력을 받으므로 여기선 비워둡니다.

if __name__ == '__main__':
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor('black')

    runner = RandomMover(screen)  # 역할 할당
    chaser = ManualMover(screen)  # Chaser는 ManualMover로 변경
    coin_ = RandomCoin(screen)
    game = RunawayGame(screen, runner, chaser, coin_)
    game.start()
    screen.mainloop()
