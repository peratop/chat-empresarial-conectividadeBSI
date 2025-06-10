# **Sistema de Chat Industrial**  

## **Descrição**  
Um servidor de chat em **Python** que utiliza o protocolo **TCP** para comunicação entre múltiplos clientes em uma rede industrial. Os operadores podem se conectar, enviar mensagens em tempo real e receber mensagens de outros usuários.  

---

## **Pré-requisitos**  
- **Python 3.x** instalado  
- Acesso a uma rede local (ou `localhost` para testes locais)  

---

## **Como Executar**  

### **1. Iniciar o Servidor**  
Abra um terminal e execute:  
```bash
python servidor.py
```
**Saída esperada:**  
```
Iniciando Servidor de Chat Industrial  
[SERVIDOR] Ouvindo em 127.0.0.1:10500  
```

### **2. Conectar Clientes**  
Abra **outros terminais** (um para cada operador) e execute:  
```bash
python clientes_chat.py
```
**Saída esperada:**  
```
Digite seu nome para login: [NomeDoOperador]
Conectado como [NomeDoOperador]. ID: [ID]
Digite 'SAIR' para desconectar ou sua mensagem para enviar ao chat.
```

### **3. Enviar Mensagens**  
- Digite mensagens no terminal do cliente e pressione **Enter** para enviar.  
- Todos os clientes conectados receberão a mensagem no formato:  
  ```
  [NomeDoOperador]: [Mensagem]
  ```
- Para sair, digite **`SAIR`** e pressione **Enter**.  

---

## **Tecnologias Utilizadas**  
- **Linguagem:** Python 3.x  
- **Protocolo:** TCP/IP  
- **Bibliotecas:** `socket`, `threading`  

---

## **Observações**  
- O servidor suporta múltiplas conexões simultâneas.  
- Mensagens são transmitidas em **broadcast** (todos recebem).  
- Para encerrar o servidor, pressione **`Ctrl+C`** no terminal onde ele está rodando.  

**Equipe:** Diego Nunes, Gustavo H Schott, Leonardo Pereira, Milena Ferraz 🚀