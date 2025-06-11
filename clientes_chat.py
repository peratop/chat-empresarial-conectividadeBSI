import socket
import threading

HOST = '127.0.0.1'
PORT = 10500

def receber_mensagens(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                print("\nConexão encerrada pelo servidor.")
                break
            print(f"\n{data}\nDigite sua mensagem: ", end="")
        except Exception as e:
            print(f"\nErro ao receber mensagem: {e}")
            break

def main():
    nome = input("Utilize seu nome para login: ").strip()
    if not nome:
        print("Nome inválido!")
        return
        
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        sock.send(f"LOGIN:{nome}".encode('utf-8'))
        
        resposta = sock.recv(1024).decode('utf-8')
        if resposta.startswith("ERRO"):
            print(resposta)
            return
            
        print(f"Conectado como {nome}. ID: {resposta.split(':')[1]}")
        print("Digite 'SAIR' para desconectar ou sua mensagem para enviar ao chat.")
        
        # Thread para receber mensagens
        recv_thread = threading.Thread(target=receber_mensagens, args=(sock,))
        recv_thread.daemon = True
        recv_thread.start()
        
        # Loop principal para enviar mensagens
        while True:
            mensagem = input("Digite sua mensagem: ").strip()
            if not mensagem:
                continue
                
            sock.send(mensagem.encode('utf-8'))
            if mensagem.upper() == "SAIR":
                break
                
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        sock.close()
        print("Desconectado.")

if __name__ == "__main__":
    main()