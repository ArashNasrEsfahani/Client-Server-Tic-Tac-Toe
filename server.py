import socket
import threading
import pickle
import tkinter as tk
from tkinter import ttk

class TicTacToe:
    def __init__(self, size, is_server=True, serv_flag = False):
        self.size = size
        self.connected_houses = 3 if size in [3, 4] else 4
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'
        self.is_server = is_server 
        self.serv_flag = serv_flag
        self.state = 'c'
        
        if is_server and self.serv_flag == False:
            self.start_server()
            self.serv_flag = True

    def make_move(self, row, col, is_sever):

        if self.is_server and is_sever:
            return

        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            
            if self.check_winner(row, col):
                self.state = 'o'
                print(f"Player {self.current_player} wins!")

            elif self.is_board_full():
                print("It's a draw!")
                self.state = 'o'

            else:
                pass
            
            self.current_player = 'O' if self.current_player == 'X' else 'X'
              

    def check_winner(self, row, col):
        # Check for a winner in the row
        if self.check_line(self.board[row]):
            return True

        # Check for a winner in the column
        if self.check_line([self.board[i][col] for i in range(self.size)]):
            return True

        # Check for a winner in the main diagonal
        if row == col and self.check_line([self.board[i][i] for i in range(self.size)]):
            return True

        # Check for a winner in the anti-diagonal
        if row + col == self.size - 1 and self.check_line([self.board[i][self.size - 1 - i] for i in range(self.size)]):
            return True

        return False

    def check_line(self, line):
        # Helper method to check if there are connected houses in a line
        count = 0
        for cell in line:
            if cell == self.current_player:
                count += 1
                if count == self.connected_houses:
                    return True
            else:
                count = 0

        return False

    def is_board_full(self):
        return all(self.board[i][j] != ' ' for i in range(self.size) for j in range(self.size))

    def reset_game(self):
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.state = 'c'
                
        self.current_player = 'O' if self.current_player == 'X' else 'X'


    def start_server(self):
        server_thread = threading.Thread(target=self.initialize_server)
        server_thread.start()

    def initialize_server(self):
        host = "127.0.0.1"
        port = 5555
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sockets = []
        lock = threading.Lock()

        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, lock, client_sockets))
            client_thread.start()

    def handle_client(self, client_socket, lock, client_sockets):
        with lock:
            client_sockets.append(client_socket)

        
        client_socket.send(pickle.dumps({"board_size": self.size, "current_player": self.current_player, "connected_houses": self.connected_houses}))
        self.current_player = 'O' if self.current_player == 'X' else 'O'

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = pickle.loads(data)
                if message['plyr'] == self.current_player:
                    self.make_move(message['row'], message['col'], False)
                    
                    if self.state == 'o':
                        # Game over, notify all clients
                        self.current_player = 'O' if self.current_player == 'X' else 'X'
                        game_over_message = {"game_over": True, "winner": self.current_player}
                        self.current_player = 'O' if self.current_player == 'X' else 'X'
                        for socket in client_sockets:
                            socket.send(pickle.dumps(game_over_message))
                        self.reset_game()
                    
                else: 
                    print("Wrong Turn.")
                    
                client_socket.send(pickle.dumps(self.state))
                
                updated_state = {"board": self.board}
                print(updated_state)
                
                for socket in client_sockets:
                    socket.send(pickle.dumps(updated_state))
                

            except Exception as e:
                print(f"Error: {e}")
                break

        with lock:
            client_sockets.remove(client_socket)
            client_socket.close()
            
            
def get_grid_size():
    global sizei
    options = [3, 4, 5]  # Predefined grid sizes

    # Create the main window
    root = tk.Tk()
    root.title("Grid Size Selection")

    # Create a dropdown menu
    label = tk.Label(root, text="Select grid size:")
    label.pack(pady=10)

    selected_size = tk.StringVar(root)
    selected_size.set(options[0])  # set the default value

    size_dropdown = ttk.Combobox(root, values=options, textvariable=selected_size)
    size_dropdown.pack(pady=10)

    # Function to handle button click
    def ok_button_click():
        global sizei
        sizei = int(selected_size.get())
        root.destroy()

    # Create an OK button
    ok_button = tk.Button(root, text="OK", command=ok_button_click)
    ok_button.pack(pady=10)

    # Start the main loop
    root.wait_window()

    return sizei  
    
    
    
global player_num
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  
    sizei = get_grid_size()
    root.destroy()
    player_num = 0
    game = TicTacToe(sizei, is_server=True, serv_flag = False)
