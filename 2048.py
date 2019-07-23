import curses#���ڷ�װʵ�����ն��޹صĿ���̨����������
from random import randrange, choice#�������������е�һ��ֵ�������б�Ԫ����ַ����������
from collections import defaultdict#���Բ���ʼ�����ֵ�

actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']#�������������˳�
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']#��Ч����wasdqr��Сд
action_dict = dict((zip(letter_codes), actions * 2))#������������Ϊ

def get_user_action(keyboard):
    char = "N"
    while char not in action_dict:
        char = keyboard.getch()
    return action_dict[char]

#����ת��
def transpose(field):
    return [list(row) for row in field]

#������ת�������
def invert(field):
    return [row[::-1] for row in field]

class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height = height#��
        self.width = width#��
        self.win_value = 2048#���ط���
        self.score = 0#��ǰ����
        self.highscore = 0#��߷���
        self.reset()#��������
    def spawn(self):
        #�������2����4
        new_element = 4 if randrange(100) > 89 else 2
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element
    def reset(self):
        #��������
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()
    def move(self, direction):
         #һ������ϲ�
        def move_row_left(row):
            def tighten(row):#����ɢ�ķ�0��Ԫ����һ��
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row
            def merge(row):#���ٽ�Ԫ�ؽ��кϲ�
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
            #�ȼ���һ���ٺϲ��ټ���һ��
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
    def draw(self, screen):#������Ϸ����
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '       (R)Restart   (Q)Exit   '
        gameover_string = 'GAME OVER'
        win_string = 'You Win!'
        def cast(string):
            screen.addstr(string + '\n')
        #����ˮƽ�ָ���
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
    def move_is_possible(self, direction):#�ж��ܷ��ƶ�
        def row_is_left_movable(row):
            def change(i):
                if row[i] == 0 and row[i + 1] != 0:#�����ƶ�
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:#���Ժϲ�
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
def main (stdscr):#���߼�
    def init():
        #������Ϸ����
        game_field.reset()
        return 'Game'
    def not_game(state):
        #������Ӯ����
        game_field.draw(stdscr)
        #��ȡ�û������action, �ж����������ǽ���
        action = get_user_action(stdscr)
        reponses = defaultdict(lambda : state)#Ĭ�ϵ�ǰ����û����Ϊһֱѭ��
        reponses['Restart'], reponses['Exit'] = 'Init', 'Exit'#��Ӧ��ͬ��Ϊת����ͬ״̬
        return reponses[action]
    def game():
        #������ǰ����
        game_field.draw(stdscr)
        #��ȡ�û�����õ�action
        action = get_user_action(stdscr)
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        #if �ɹ��ƶ���һ��
        if game_field.move(action):
            if game_field.is_win:
                return 'Win'
            if game_field.is_gameover:
                return 'Gameover'
        return 'Game'
    state_actions = {'Iint': init, 'Win': lambda : not_game('Win'), 'Gameover': lambda :not_game('Gameover'),'Game': game}
    curses.use_default_colors()
    #�����ս�״̬���Ϊ2048
    game_field = GameField(win = 2048)
    state = 'Iint'
    #״̬����ʼѭ��
    while state != 'Exit':
        state = state_actions[state]()
    #ӵ����ѭ��ֱ�������Ч���뷵�ض�Ӧ��Ϊ
curses.wrapper(main)