import curses#用于封装实现与终端无关的控制台的输入和输出
from random import randrange, choice#随机输出递增数列的一个值，返回列表元组或字符串的随机项
from collections import defaultdict#可以不初始化的字典

actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']#上下左右重置退出
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']#有效输入wasdqr大小写
action_dict = dict((zip(letter_codes), actions * 2))#关联输入与行为

def get_user_action(keyboard):
    char = "N"
    while char not in action_dict:
        char = keyboard.getch()
    return action_dict[char]

#矩阵转置
def transpose(field):
    return [list(row) for row in field]

#矩阵逆转非逆矩阵
def invert(field):
    return [row[::-1] for row in field]

class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height = height#高
        self.width = width#宽
        self.win_value = 2048#过关分数
        self.score = 0#当前分数
        self.highscore = 0#最高分数
        self.reset()#棋盘重置
    def spawn(self):
        #随机生成2或者4
        new_element = 4 if randrange(100) > 89 else 2
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element
    def reset(self):
        #重置棋盘
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()
    def move(self, direction):
         #一行向左合并
        def move_row_left(row):
            def tighten(row):#把零散的非0单元挤到一起
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row
            def merge(row):#对临近元素进行合并
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 *row[i]
                        pair = False
                    else:
                        new_row.append(row[i])
                assert  len(new_row) == len(row)
                return new_row
            #先挤到一块再合并再挤到一块
            return tighten(merge(tighten(row)))
        moves = {}
        moves['Left'] = lambda field:[move_row_left(row) for row in field]
        moves['Right'] = lambda field:invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field:transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field:transpose(moves['Right'](transpose(field)))
        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False
    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)
    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)
    def draw(self, screen):#绘制游戏界面
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '       (R)Restart   (Q)Exit   '
        gameover_string = 'GAME OVER'
        win_string = 'You Win!'
        def cast(string):
            screen.addstr(string + '\n')
        #绘制水平分割线
        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda : line)
            if not hasattr(draw_hor_separator, "counter"):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1
        def draw_row(row):
            cast(''.join('|{:^5}'.format(num) if num > 0 else '|      ' for num in row) + '|')
            screen.clear()
            cast('SCORE: ' + str(self.score))
            if 0 != self.highscore:
                cast('HIGHSCORE: ' + str(self.highscore))
            for row in self.field:
                draw_hor_separator()
                draw_row(row)
            draw_hor_separator()
            if self.is_win():
                cast(win_string)
            else:
                if self.is_gameover():
                    cast(gameover_string)
                else:
                    cast(help_string1)
            cast(help_string2)
    def move_is_possible(self, direction):#判断能否移动
        def row_is_left_movable(row):
            def change(i):
                if row[i] == 0 and row[i + 1] != 0:#可以移动
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:#可以合并
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1))
        check = {}
        check['Left'] = lambda  field: any(row_is_left_movable(row) for row in field)
        check['Right'] = lambda field: check['Left'](invert(field))
        check['Up'] = lambda field: check['Left'](transpose(field))
        check['Down'] = lambda field: check['Right'](transpose(field))
        if direction in check:
            return check[direction](self.field)
        else:
            return False
def main (stdscr):#主逻辑
    def init():
        #重置游戏棋盘
        game_field.reset()
        return 'Game'
    def not_game(state):
        #画出输赢界面
        game_field.draw(stdscr)
        #读取用户输入的action, 判断是重启还是结束
        action = get_user_action(stdscr)
        reponses = defaultdict(lambda : state)#默认当前界面没有行为一直循环
        reponses['Restart'], reponses['Exit'] = 'Init', 'Exit'#对应不同行为转换不同状态
        return reponses[action]
    def game():
        #画出当前棋盘
        game_field.draw(stdscr)
        #读取用户输入得到action
        action = get_user_action(stdscr)
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        #if 成功移动了一步
        if game_field.move(action):
            if game_field.is_win:
                return 'Win'
            if game_field.is_gameover:
                return 'Gameover'
        return 'Game'
    state_actions = {'Iint': init, 'Win': lambda : not_game('Win'), 'Gameover': lambda :not_game('Gameover'),'Game': game}
    curses.use_default_colors()
    #设置终结状态最大为2048
    game_field = GameField(win = 2048)
    state = 'Iint'
    #状态机开始循环
    while state != 'Exit':
        state = state_actions[state]()
    #拥塞加循环直到获得有效输入返回对应行为
curses.wrapper(main)