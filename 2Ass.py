import sys, re               # To access some of the python module


class Game:
    def __init__(self):
        self.size = 8
        self.space_balence = self.size ** 2
        self.now_player = 0
        self.next_player = 1
        self.players = [{'name': 'Ali', 'tokens': [28, 37], 'tick': '  ', 'nickname': 'first player'},
                        {'name': 'Samer', 'tokens': [29, 36], 'tick': '@@', 'nickname': 'second player'}]

    def show_menu(self):
        choice = input("""::::Welcome to O'Neillo Game::::
        ================================                                
        1. New Game                                                                        
        2. Restore a Game
        3. Quit


        Select a number from the menu : """)
        return choice

    def new_Game(self):
        print("A new Game::")
        for player in self.players:
            player['name'] = ''
            while player['name'] == "":
                player['name'] = input("Insert the {} name: ".format(player['nickname']))
        for player in self.players:
            print("Hi {} your are \' {} \' ".format(player['name'], player['tick']))
        print("Let's play!")

    def save_Game(self):
        Save = input("Do you want to save the game? (y/n): ")
        if Save == 'n' or Save == 'N':
            sys.exit(-1)
        FileName = input("Enter File Name: ")
        File = open('{}.txt'.format(FileName), 'w+')
        for player in self.players:
            File.write('name : {}'.format(player['name']))
            File.write('\n')
            Tokens = ['{}'.format(x) for x in player['tokens']]
            File.write('tokens : {}'.format(','.join(Tokens)))
            File.write('\n')
        File.write('now_player : {}'.format(self.now_player))
        File.write('\n')
        File.write('next_player : {}'.format(self.next_player))
        File.close()

    def restore_Game(self):
        FileName = input("Enter File Name: ")
        File = open('{}.txt'.format(FileName), 'r')
        Data = File.read()
        Names = re.findall('name : (.+)', Data)
        Tokens = re.findall('tokens : (.+)', Data)
        self.now_player = int(re.findall('now_player : (.+)', Data)[0])
        self.next_player = int(re.findall('next_player : (.+)', Data)[0])
        for i in range(2):
            self.players[i]['name'] = Names[i]
            tokens = [int(i) for i in '{}'.format(Tokens[i]).split(',')]
            self.players[i]['tokens'] = tokens
        self.printBoard_2d()

    def printBoard_2d(self):
        # Header #
        for player in self.players:
            print("Number of tokens for player {} :\' {} \' : {}".format(player['name'], player['tick'],
                                                                         len(player['tokens'])))
        # Body #
        print("   ", " ----" * self.size)
        print("   ", "|", end=" ")
        for num in range(1, self.size ** 2 + 1):
            if num in self.players[0]['tokens']:
                print(self.players[0]['tick'], "|", end=" ")
            elif num in self.players[1]['tokens']:
                print(self.players[1]['tick'], "|", end=" ")
            else:
                print('{:0>2}'.format(num), "|", end=" ")
            if num % self.size == 0:
                print()
                print("   ", " ----" * self.size)
                if num != self.size ** 2:
                    print("   ", "|", end=" ")
        # Footer #
        print("No of space balence : {}".format(self.space_balence))
        print("press Q or q to quit from the current game")
        selected = input(
            "{} turn, please select one number from the board :".format(self.players[self.now_player]['name']))
        return selected

    def get_Borders(self):
        Top = [x for x in range(1, self.size + 1)]
        Right = [x for x in range(self.size, self.size ** 2 + 1, self.size)]
        Btm = [x for x in range(self.size ** 2, self.size ** 2 - self.size, -1)]
        Left = [x for x in range(1, self.size ** 2, self.size)]
        Right_Left = list(map(lambda x, y: (x, y), Right, Left))
        Top_Btm = list(map(lambda x, y: (x, y), Top, Btm))
        Boreders = Top + Right + Btm + Left
        return Boreders, Right_Left, Top_Btm

    def use_selected(self, selected):
        # Check if not used
        my_tokens = self.players[self.now_player]['tokens']
        next_tokens = self.players[self.next_player]['tokens']
        # Left_stop = selected - (self.size - 1)
        # Right_stop = Left_stop + self.size - 1
        Top_stop = selected % self.size
        if Top_stop == 0:
            Top_stop = self.size
        Btm_stop = self.size ** 2 - (self.size - Top_stop)
        Boreders, Right_Left, Top_Btm = self.get_Borders()
        Right_stop, Left_stop = [x for x in Right_Left if x[0] >= selected and x[1] <= selected][0]
        if selected in self.players[0]['tokens'] + self.players[1]['tokens']:
            return False
        wined_tokens = []
        # Horizantal tokens
        Moves = [1, -1]
        for move in Moves:
            x = selected + move
            win_Group = []
            while x >= Left_stop and x <= Right_stop:
                if x in next_tokens:
                    win_Group.append(x)
                elif x in my_tokens:
                    wined_tokens += win_Group
                    break
                else:
                    win_Group = []
                    break
                x += move

        # Vertical tokens
        Moves = [self.size, -self.size]
        for move in Moves:
            x = selected + move
            win_Group = []
            while x >= Top_stop and x <= Btm_stop:
                if x in next_tokens:
                    win_Group.append(x)
                elif x in my_tokens:
                    wined_tokens += win_Group
                    break
                else:
                    win_Group = []
                    break
                x += move

        # Daigonal tokens
        Moves = [self.size + 1, self.size - 1, -(self.size + 1), -(self.size - 1)]
        for move in Moves:
            x = selected + move
            win_Group = []
            while x not in Boreders:

                if x in next_tokens:
                    win_Group.append(x)
                elif x in my_tokens:
                    wined_tokens += win_Group
                    break
                else:
                    win_Group = []
                    break
                x += move
        for num in wined_tokens:
            self.players[self.next_player]['tokens'].remove(num)
            self.players[self.now_player]['tokens'].append(num)
        self.players[self.now_player]['tokens'].append(selected)
        return True

    def Next_player(self):
        if self.now_player == 0:
            self.next_player = 0
            self.now_player = 1
        else:
            self.next_player = 1
            self.now_player = 0


Project = Game()
while True:
    choice = Project.show_menu()
    if choice == '1':
        Project.new_Game()
        while True:
            selected = Project.printBoard_2d()
            if selected == 'q' or selected == 'Q':
                Project.save_Game()
                sys.exit(-1)
            selected = int(selected)
            Project.use_selected(selected)
            Project.Next_player()
    elif choice == '2':
        Project.restore_Game()
    elif choice == '3':
        sys.exit(-1)
while True:
    selected = Project.printBoard_2d()
    Project.use_selected(selected)
    Project.Next_player()