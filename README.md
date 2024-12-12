# Documentação do Protocolo e Funcionamento do Jogo Connect 4

## Propósito do Software

O software implementa o jogo **Connect 4** em um formato multiplayer, onde dois jogadores se conectam ao servidor para competir. O servidor gerencia o estado do jogo, valida as jogadas e fornece feedback em tempo real aos jogadores. Cada jogador tenta alinhar quatro fichas consecutivas em uma grade 7x6, seja horizontalmente, verticalmente ou diagonalmente.

---

## Motivação da Escolha do Protocolo de Transporte

O protocolo de transporte utilizado é o **TCP** (Transmission Control Protocol). Essa escolha foi feita devido à necessidade de uma comunicação confiável, sequencial e sem perda de mensagens. O TCP garante que todos os eventos do jogo sejam entregues e processados na ordem correta, mantendo a integridade e a sincronização entre o servidor e os clientes.

---

## Estrutura do Projeto

### Diretórios e Arquivos

- **jogador1.py**: Implementa o cliente do Jogador 1, permitindo a conexão com o servidor, envio de jogadas e recepção das atualizações do jogo.
- **jogador2.py**: Implementa o cliente do Jogador 2, com funcionalidades idênticas ao jogador 1.
- **servidor.py**: Implementa o servidor, que gerencia o estado do jogo, processa as jogadas dos jogadores e transmite respostas apropriadas.
- **connect_4.py**: Contém a lógica principal do jogo, incluindo a inicialização do tabuleiro, validação de jogadas e determinação de vitória ou empate.
- **README.md**: Documentação do projeto.

### Interação entre os Arquivos

1. **servidor.py**: Atende como ponto central da lógica do jogo, recebendo as jogadas de ambos os jogadores, processando a lógica contida em `connect_4.py` e enviando as respostas apropriadas aos clientes.
2. **jogador1.py** e **jogador2.py**: São clientes que se conectam ao servidor para enviar comandos (como jogadas) e receber atualizações do jogo, com base no estado processado pelo servidor.
3. **connect_4.py**: Uma biblioteca importada pelo servidor que encapsula a lógica do jogo, garantindo que todas as validações de jogadas, atualizações no tabuleiro e condições de vitória/empate sejam gerenciadas de forma centralizada.

### Diagrama de Interação

```plaintext
  Jogador 1                Servidor                 Jogador 2
     |                         |                       |
     | --- Enviar jogada ----> |                       |
     |                         |                       |
     | <---- Atualizar estado --|--- Enviar estado --->|
     |                         |                       |
     | ---- Receber status ----|<--- Jogada enviada --|
```

O diagrama acima mostra a troca de mensagens entre os clientes (jogador1.py e jogador2.py) e o servidor (servidor.py). O servidor processa cada jogada usando a lógica de `connect_4.py`, atualiza o estado do jogo e transmite a informação para os jogadores. O fluxo de mensagens garante que ambos os clientes estejam sincronizados com o estado atual do jogo.


---

## Como Executar

### Requisitos Mínimos de Funcionamento

- **Python 3.6** ou superior.
- Módulos: `socket` (para comunicação em rede) e `threading` (para conexões simultâneas).

### Como Instalar

Clone o repositório do projeto para a sua máquina local:

```bash
git clone https://github.com/murilopmaia/Redes1_Projeto.git
cd Redes1_Projeto
```

Configure o IP e a porta no arquivo `servidor.py` e nos arquivos dos jogadores (`jogador1.py` e `jogador2.py`), substituindo o valor de `HOST` pelo seu endereço IP local. Para verificar o IP:

No Windows:

```bash
ipconfig
```

No Linux/Mac:

```bash
ifconfig
```

Substitua o valor de `PORT` se o padrão estiver em uso.

### Executando o Servidor

1. Navegue até o diretório raiz do projeto:
   ```bash
   cd Redes1_Projeto
   ```
2. Execute o servidor:
   ```bash
   python servidor.py
   ```

### Executando os Clientes

1. Em terminais separados, execute os jogadores:
   - Jogador 1:
     ```bash
     python jogador1.py
     ```
   - Jogador 2:
     ```bash
     python jogador2.py
     ```

---

## Protocolo de Comunicação

O jogo utiliza sockets TCP para a comunicação entre o servidor e os clientes. O protocolo segue uma estrutura clara para garantir o funcionamento do jogo:

### Mensagens Trocadas

- **Servidor para Clientes:**

  - Mensagem de boas-vindas e instruções do jogo.
  - Atualizações do estado do tabuleiro após cada jogada.
  - Mensagens de erro para jogadas inválidas (coluna cheia ou entrada inválida).
  - Declaração de vitória, empate ou continuação do jogo.

- **Clientes para Servidor:**

  - Coordenadas da jogada no formato de coluna (0 a 6).

### Estrutura de Mensagens

1. **Mensagem de Boas-vindas:**

   - Formato: `"Bem-vindo ao Connect 4! O jogo começará em breve."`

2. **Mensagem de Jogada:**

   - Cliente para Servidor: `"2"` (representando a coluna escolhida).
   - Servidor para Cliente: `"Jogada registrada. Atualizando tabuleiro..."`

3. **Mensagem de Vitória ou Empate:**

   - Formato: `"Vitória do Jogador X!"` ou `"Empate!"`

4. **Mensagem de Erro:**

   - Formato: `"Erro: Coluna cheia ou entrada inválida. Tente novamente."`

---

## Funcionamento do Software

### Servidor

1. **Inicialização:**

   - Cria um socket TCP/IP.
   - Vincula o socket ao IP e à porta especificados.
   - Escuta conexões de clientes.

2. **Gerenciamento de Conexões:**

   - Aceita dois clientes.
   - Cria threads para gerenciar cada cliente simultaneamente.

3. **Controle do Jogo:**

   - Gerencia o estado do tabuleiro e valida jogadas.
   - Informa aos clientes sobre o progresso do jogo.
   - Determina o vencedor ou empate e finaliza o jogo.

4. **Desconexão:**

   - Fecha a conexão após o término do jogo.

### Clientes

1. **Inicialização:**

   - Conectam-se ao servidor via socket TCP/IP.

2. **Interação com o Servidor:**

   - Recebem mensagens do servidor.
   - Enviam jogadas.
   - Exibem o estado atualizado do tabuleiro.

3. **Desconexão:**

   - Fecham a conexão após o término do jogo.

---

## Colaboradores

- Murilo Maia
- Beatriz Oliveira
- Alice Valero
- Júlia Ramos

