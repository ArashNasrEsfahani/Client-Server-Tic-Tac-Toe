import socket
import threading
import pickle
import tkinter as tk
from tkinter import messagebox
import time

class TicTacToe:
    def __init__(self, size, current_player, is_server=False):
        self.size = size
        self.connected_houses = 3 if size in [3, 4] else 4
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = current_player
        self.is_server = is_server 
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        
        for i in range(size):
            for j in range(size):
                self.buttons[i][j] = tk.Button(self.root, text='', font=('normal', 20), width=6, height=2,
                                               command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i + 3, column=j)

    

    def run(self):
        self.root.mainloop()
        
class TicTacToeClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.board_size = 3
        self.connected_houses = 3
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
        

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        server_info = pickle.loads(self.client_socket.recv(1024))
        self.board_size = server_info["board_size"]
        self.current_player = server_info["current_player"]
        self.connected_houses = server_info["connected_houses"]
        print(f"Connected to server with {self.board_size}x{self.board_size} board")
        
    
    def init_gui(self, size ,current_player, is_server=False):
        self.size = size
        self.connected_houses = 3 if size in [3, 4] else 4
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = current_player
        self.is_server = is_server 
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        
        for i in range(size):
            for j in range(size):
                self.buttons[i][j] = tk.Button(self.root, text='', font=('normal', 20), width=6, height=2,
                                               command=lambda row=i, col=j: self.send_moveg(row, col))
                self.buttons[i][j].grid(row=i + 3, column=j)

        if is_server and self.serv_flag == False:
            self.start_server()
            self.serv_flag = True
            
        self.root.mainloop()
    
    def send_moveg(self, row, col):
        move = {"row": row, "col": col, "plyr": self.current_player }
        self.client_socket.send(pickle.dumps(move))
        
            
    def send_move(self, move):
        self.client_socket.send(pickle.dumps(move))
        
    def handle_game_over(self, winner):
        if winner == self.current_player:
            print(f"\nCongratulations! You won!")
            print(f"Next Round: \n")
            self.update_board_gui()
        else:
            print(f"\nGame over. Player {winner} won.")
            print(f"Next Round: \n")
            self.update_board_gui()
        
    def receive_messages(self):
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            message = pickle.loads(data)
            if "game_over" in message and message["game_over"]:
                winner = message.get("winner", None)
                self.handle_game_over(winner)
            elif "board" in message:
                self.board = message["board"]
                self.update_board_gui()
                print(self.board)
            else:
                pass
            
    def update_board_gui(self):
        # Schedule the update of the board in the main GUI thread
        self.root.after(0, self.update_board_gui_helper)

    def update_board_gui_helper(self):
        # Actual update of the GUI components based on the updated board
        for i in range(self.size):
            for j in range(self.size):
                color = 'red' if self.current_player == 'X' else 'blue'
                self.buttons[i][j].config(text=self.board[i][j], fg=color)

    # def send_messages(self):
    #     while True:
    #         input_str = input("Enter 'row' and 'col' separated by space: ")
    #         st = input_str.split()
    #         values[0] = int(st[0])
    #         values[1] = int(st[1])
    #         if 0 <= values[0] <= client.board_size and 0 <= values[1] <= client.board_size:
    #             move = {"row": (values[0] - 1), "col": (values[1] - 1), "plyr": values[2]}
    #             client.send_move(move)
    #         else:
    #             print("Wrong Input.")
        
if __name__ == "__main__":
    client = TicTacToeClient("127.0.0.1", 5555)
    # values = [None] * 3
    # values[2] = client.current_player
    
    listener_thread = threading.Thread(target=client.init_gui, args=(client.board_size, client.current_player, False))
    sender_thread = threading.Thread(target=client.receive_messages)
    
    listener_thread.start()
    sender_thread.start()

    listener_thread.join()
    sender_thread.join()