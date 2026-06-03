import socket
import threading
import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 5555))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)

print(f"⚔️ Server running on port {PORT}")
print("Waiting for 2 players...\n")

players = []
names = []
hp = [30, 30]
turn = 0

def send_all(msg):
    for p in players:
        try:
            p.send(msg.encode())
        except:
            pass

def handle_player(conn, player_id):
    global turn

    conn.send("Enter your name: ".encode())
    name = conn.recv(1024).decode().strip()
    names.append(name)

    conn.send(f"Welcome {name}! Waiting for opponent...\n".encode())

    while len(players) < 2:
        pass

    conn.send("Both players connected! Fight begins!\n".encode())

    while True:
        if turn % 2 != player_id:
            continue

        conn.send("\nYour move (attack / heal / defend): ".encode())
        move = conn.recv(1024).decode().lower().strip()

        opponent = 1 - player_id

        if move == "attack":
            dmg = 5
            hp[opponent] -= dmg
            send_all(f"\n💥 {names[player_id]} attacks for {dmg} damage!")

        elif move == "heal":
            heal = 4
            hp[player_id] += heal
            send_all(f"\n💖 {names[player_id]} heals for {heal} HP!")

        elif move == "defend":
            send_all(f"\n🛡️ {names[player_id]} defends!")

        else:
            conn.send("Invalid move!\n".encode())
            continue

        send_all(f"\n📊 HP: {names[0]}={hp[0]} | {names[1]}={hp[1]}\n")

        if hp[0] <= 0 or hp[1] <= 0:
            winner = names[0] if hp[0] > 0 else names[1]
            send_all(f"\n🏆 {winner} wins the battle!")
            break

        turn += 1


while len(players) < 2:
    conn, addr = server.accept()
    print("Connected:", addr)
    players.append(conn)

    threading.Thread(target=handle_player, args=(conn, len(players)-1)).start()