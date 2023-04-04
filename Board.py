from copy import deepcopy
import queue
import time
from random import randint, seed

MAX_COL = 4
MAX_ROW = 4
SHUFFLE = 50  # Parametros tuxaiothtas, oso pio megalo toso pio tuxaios pinakas

"""Ola ta parakatw xrhsimopoiountai gia IDS"""
nodes_created = set()  # Sunolo pou apothikeuei katastaseis pou exoun elegxthei
fringe = queue.LifoQueue()  # dhlwsh ths ouras pou tha xrhsimopoihsoume
node = []  # arxikopoihsh tou pinaka node
expanded = set()  # gia apothikeush katastasewn pou exoun hdh epektathei


class Board:

    def __init__(self):
        """Dhmiourgia enos board"""

        self.goal = [  # tha xrhsimopoihthei gia na elegxoume ama ftasame ston stoxo
            [" 1", " 2", " 3", " 4"],
            [" 5", " 6", " 7", " 8"],
            [" 9", "10", "11", "12"],
            ["13", "14", "15", "__"]
        ]
        self.board = deepcopy(self.goal)  # Antigrafh tou pinaka gia ton xrhsimopoihsoume ws arxikh katastash
        self.empty_location = [MAX_ROW - 1, MAX_COL - 1]  # Dhlwsh ths theshs tou kenou
        self.moves = {0: self.move_up, 1: self.move_down, 2: self.move_left,
                      3: self.move_right}  # Dhlwsh dictionary me tis kinhseis pou mporoume na kanoume

    def print_table(self):
        """Emfanish tou pinaka"""
        for i in range(MAX_ROW):
            for j in range(MAX_COL):
                print(self.board[i][j], end=" ")
            print("")

        return ""

    def start(self):
        # This function refreshes the screen.

        print("Welcome to game of 15")
        self.print_table()

        if self.goal == self.board:
            print("\nSorry, this is the goal state. Increase the SHUFFLE or try again!")
            return False
        return True

    def shuffle(self):
        """Anakateuei ton pinaka"""
        seed()
        for i in range(SHUFFLE):  # gia i ews shuffle(analoga ti parametro exoume balei sthn dhlwsh tou)
            m = randint(0, 3)  # epelekse tuxaia kai kane mia apo tis kinhseis, gia SHUFFLE fores
            self.moves[m](self.board, self.empty_location)

        """Metakinhse to keno terma katw deksia"""
        for i in range(MAX_COL):
            self.moves[1](self.board, self.empty_location)

        for i in range(MAX_ROW):
            self.moves[3](self.board, self.empty_location)

        """antigrafh ths arxikhs katastashs gia na thn xrhsimopoihsoume meta ston astar"""
        board_for_astar = deepcopy(self.board)

        return board_for_astar

    def dfs(self, max_depth):
        """lush me DFS"""
        global fringe, node, nodes_created, expanded

        if fringe.empty():  # elegxos an h oura einai adeia
            fringe.put({"board": self.board, "empty_location": self.empty_location, "path": [],
                        "depth": 0})  # an einai, bale mesa th riza

        node = fringe.get()  # pare to teleutaio stoixeio ths ouras

        node_list = [str(node["board"]), str(node["path"])]  # lista sthn opoia apothikeutai to board kai to path
        if str(node_list) not in nodes_created:  # an den uparxoun mesa sto searched den exoun ksana dhmiourghthei
            nodes_created.add(str(node_list))  # prosthhkh sto searched

        if node["board"] == self.goal:  # elegxoume an einai o stoxos
            print("\nSolution Found!")

            print("The path of the solution is", end="")  # Emfanish tou path ths lushs
            path = deepcopy(node["path"])
            for i in range(len(path)):
                if path[i] == 0:
                    print(" UP,", end="")
                elif path[i] == 1:
                    print(" DOWN,", end="")
                elif path[i] == 2:
                    print(" LEFT,", end="")
                else:
                    print(" RIGHT,", end="")

            print("\nThe number of nodes created is: " + str(len(nodes_created)))  # Emfanish tou plhthous twn komvwn

            return True

        if max_depth <= 0:  # elegxos se ti vathos eimaste
            return False

        hold_path = node["path"]  # krathse to path tou komvou prin ton epekthneis

        if str(node["board"]) not in expanded:  # An o komvos den exei epektathei, ton prosthetoume sto expanded
            expanded.add(str(node["board"]))  # Gia na mhn dhmiourghsoume epanalambanomenes katastaseis

        for child in self.expand_node(node["board"], node["empty_location"]):  # epektash komvou

            if str(child[0]) not in expanded:  # An o komvos den exei epektathei

                """
                 Prosthetoume to paidi sthn oura.
                 Gia path tou dinoume to hold_path(path tou gonea) + thn kinhsh pou ekane.
                 # Gia vathos tou dinoume to mhkos tou path tou gonea + 1
                """
                fringe.put(
                    {"board": child[0], "empty_location": child[1], "path": hold_path + [child[2]],
                     "depth": len(hold_path) + 1})

                if self.dfs(max_depth - 1):  # Trexoume ton dfs auth th fora gia to depth pou dwsame - 1
                    return True
        return False

    def ids(self, max_depth):

        global fringe, node, expanded

        start = time.time()
        fringe.put({"board": self.board, "empty_location": self.empty_location, "path": [],
                    "depth": 0})  # Prosthetoume th riza sthn oura

        """Anazhthsh epanalhptikhs ekbathunshs mexri na ftasoume to max depth"""
        for i in range(0, max_depth + 1):
            print("For DEPTH: " + str(i))  # gia na mas deixnei thn allagh vathous
            expanded = set()  # mhdenizoume to sunolo kathe fora, afou gia kathe epanalhpsh ksekinaei apo thn arxh
            if self.dfs(i):
                print("\nSolution found at Depth:" + str(i))  # tupwnei to vathos sto opoio brisketai h lysh
                print("Execution time(in seconds):", time.time() - start)
                return True
        else:
            print("Solution not found in this depth!")

    def astar(self, board):

        """Upologismos apostashs tou komvou apo thn telikh katastash tou"""

        def manhattan(board_for_distance):
            distance = 0
            for i in range(4):
                for j in range(4):
                    if board_for_distance[i][j] != "__":
                        x, y = divmod(int(board_for_distance[i][j]) - 1, 4)
                        distance += abs(x - i) + abs(y - j)
            return distance

        """Mas bohthaei na sortaroume ton pinaka ws pros to kostos"""

        def cost_sort(x):
            return x["f_cost"]

        start = time.time()

        open_nodes = []  # pinakas gia tous komvous pou den exoun epektathei
        closed_nodes = set()  # sunolo gia tous komvous pou epektathhkan

        open_nodes.append(  # bazoume sthn oura thn riza
            {"board": board, "empty_location": [3, 3], "f_cost": 0, "path": [], "depth": 0})

        while open_nodes:

            open_nodes.sort(key=cost_sort)  # kanoume sort ton pinaka, gia na epileksoume auton me to mikrotero kostos
            current_node = open_nodes.pop(0)  # ton bgazoume apo apo thn oura kai
            closed_nodes.add(str(current_node["board"]))  # ton prosthetoume stous closed

            """elegxos gia katastash stoxou"""
            if current_node["board"] == self.goal:
                print("\nSolution Found!")

                print("The path of the solution is", end="")  # Emfanish tou path ths lushs
                path = deepcopy(current_node["path"])
                for i in range(len(path)):
                    if path[i] == 0:
                        print(" UP,", end="")
                    elif path[i] == 1:
                        print(" DOWN,", end="")
                    elif path[i] == 2:
                        print(" LEFT,", end="")
                    else:
                        print(" RIGHT,", end="")

                print(
                    "\nThe number of nodes created is: " + str(
                        len(current_node) + len(open_nodes)))  # Emfanish tou plhthous twn komvwn
                print("\nSolution found at Depth:" + str(len(current_node["path"])))
                print("Execution time(in seconds):", time.time() - start)
                return True

            hold_path = current_node["path"]  # krathse to path tou komvou prin ton epekthneis
            for child in self.expand_node(current_node["board"], current_node["empty_location"]):  # epektash komvou
                if str(child[0]) in str(closed_nodes):  # an o komvos exei epektathei, agnohse thn epanalhpsh
                    continue

                h = manhattan(child[0])  # upologismos apostashs apo thn katastash stoxou
                """
                prosthetoume to paidi sthn oura.
                Gia path tou dinoume to hold_path(path tou gonea) + thn kinhsh pou ekane.
                Gia vathos tou dinoume to mhkos tou path tou gonea + 1
                Gia kostos thn apostash apo ton teliko stoxo + to mhkos tou path tou
                """
                open_nodes.append(
                    {"board": child[0], "empty_location": child[1], "f_cost": h + len(hold_path) + len([child[2]]),
                     "path": hold_path + [child[2]], "depth": len(hold_path) + 1})

    def move(self, board, empty_location, x, y):

        """Elegxos ths kinhshs"""

        if empty_location[0] + x < 0 or empty_location[0] + x > 3 or empty_location[1] + y < 0 or empty_location[
            # An bgainei ektos oriwn pinaka
            1] + y > 3:
            return board, empty_location  # epestrepse ton arxiko pinaka

        """Allagh twn stoixeiwn metaksu tous"""
        board[empty_location[0]][empty_location[1]], board[empty_location[0] + x][empty_location[1] + y] \
            = board[empty_location[0] + x][empty_location[1] + y], board[empty_location[0]][empty_location[1]]

        """Enhmerwsh ths theshs tou kenou"""
        empty_location[0] += x
        empty_location[1] += y

        return board, empty_location

    def move_up(self, board, empty_location):
        """Kinhsh panw"""
        return self.move(board, empty_location, -1, 0)

    def move_down(self, board, empty_location):
        """Kinhsh katw"""
        return self.move(board, empty_location, 1, 0)

    def move_left(self, board, empty_location):
        """Kinhsh aristera"""
        return self.move(board, empty_location, 0, -1)

    def move_right(self, board, empty_location):
        """Kinhsh deksia"""
        return self.move(board, empty_location, 0, 1)

    def expand_node(self, board, empty_location):

        successors_list = []  # lista epituxontwn, tha epistrafei
        board_list = [deepcopy(board), deepcopy(board), deepcopy(board),
                      deepcopy(board)]  # Dhmiougia listas gia tis 4 katastaseis (up, down, left, right)
        empty_location_list = [list(empty_location), list(empty_location), list(empty_location), list(
            empty_location)]  # Dhmiourgia listas gia tis tis theseis tou kenou autwn twn katastasewn

        """Ektelesh twn kinhsewn"""
        board_list[0], empty_location_list[0] = self.move_up(board_list[0], empty_location_list[0])
        board_list[1], empty_location_list[1] = self.move_down(board_list[1], empty_location_list[1])
        board_list[2], empty_location_list[2] = self.move_left(board_list[2], empty_location_list[2])
        board_list[3], empty_location_list[3] = self.move_right(board_list[3], empty_location_list[3])

        for i in range(4):  # elegxos twn kinhsewn
            if board_list[i] != board:  # an o pinakas einai diaforetikos apo auton pou dwsame
                successors_list.append(
                    [board_list[i], empty_location_list[i], i])  # ton prosthetoume sthn lista twn epituxontwn

        return successors_list
