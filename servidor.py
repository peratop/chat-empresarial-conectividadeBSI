import socket
import threading

# Dados dos clientes: {id: {"socket": socket, "addr": addr, "nome": nome}}
clientes_conectados = {}
clientes_lock = threading.Lock()
proximo_id = 1

HOST = '127.0.0.1' # Conecta na localhost
PORT = 10500  # Porta única para o chat

def broadcast(mensagem, remetente_id=None): # Cria o bradcast simples para gerenciar diversos clientes de maneira limpa
    with clientes_lock:
        for cliente_id, cliente_info in clientes_conectados.items():
            if remetente_id is None or cliente_id != remetente_id:
                try:
                    cliente_info["socket"].send(mensagem.encode('utf-8'))
                except Exception as e:
                    print(f"[ERRO] Ao enviar para cliente {cliente_id}: {e}")
                    remove_cliente(cliente_id)

def remove_cliente(cliente_id):
    with clientes_lock:
        if cliente_id in clientes_conectados:
            cliente_info = clientes_conectados.pop(cliente_id)
            try:
                cliente_info["socket"].close()
            except:
                pass
            print(f"[INFO] Cliente {cliente_id} ({cliente_info['nome']}) desconectado.")
            broadcast(f"[SERVIDOR] {cliente_info['nome']} saiu do chat.", cliente_id)

def handle_cliente(conn_socket, addr):
    global proximo_id
    cliente_id = None
    
    try:
        # Receber identificação do cliente
        data = conn_socket.recv(1024).decode('utf-8').strip()
        if not data.startswith("LOGIN:"):
            conn_socket.send(b"ERRO: Protocolo invalido. Use 'LOGIN:<seu_nome>'")
            return
            
        nome = data.split(":")[1]
        with clientes_lock:
            cliente_id = proximo_id
            proximo_id += 1
            clientes_conectados[cliente_id] = {
                "socket": conn_socket,
                "addr": addr,
                "nome": nome
            }
        
        print(f"[INFO] Cliente {cliente_id} ({nome}) conectado de {addr[0]}:{addr[1]}")
        conn_socket.send(f"OK:{cliente_id}".encode('utf-8'))
        broadcast(f"[SERVIDOR] {nome} entrou no chat.", cliente_id)
        
        # Loop principal para receber mensagens
        while True:
            data = conn_socket.recv(1024).decode('utf-8').strip()
            if not data:
                break
                
            if data.upper() == "SAIR":
                conn_socket.send(b"Desconectando...")
                break
                
            print(f"[MSG] {nome} ({cliente_id}): {data}")
            broadcast(f"[{nome}]: {data}", cliente_id)
            
    except Exception as e:
        print(f"[ERRO] Cliente {addr}: {e}")
    finally:
        if cliente_id:
            remove_cliente(cliente_id)
        conn_socket.close()

def start_server():
    listening_socket = None
    try:
        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listening_socket.bind((HOST, PORT))
        listening_socket.listen(5)
        print(f"[SERVIDOR] Ouvindo em {HOST}:{PORT}")
        
        while True:
            client_conn, addr = listening_socket.accept()
            thread = threading.Thread(target=handle_cliente, args=(client_conn, addr))
            thread.start()
            
    except Exception as e:
        print(f"[ERRO CRITICO] Servidor: {e}")
    finally:
        if listening_socket:
            listening_socket.close()
        print("[SERVIDOR] Desligando...")

if __name__ == "__main__":
    print ('Iniciando chat da empresa - Anelim Co')
    print ('Seja respeitoso e direto, evite poluir o chat, se necessário considere ligar para o ramal do setor desejado')
    print ('Quaisquer mensagens que configurem algum tipo de assédio SERÃO encaminhadas para o RH')
    start_server()