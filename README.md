## CP02 - Cyber - Ransomeware
## Aluno: Alan de Souza Maximiano da Silva 
## RM: 557088

### Objetivo:
### Criar uma simulação de Ransomware utilizando Python
### O código deve ser capaz de:
### • Criptografar uma pasta alvo
### • Exibir uma mensagem em tela informando do ataque
### • Salvar a chave de criptografia em um arquivo denominado "key.rans" na mesma
### pasta dos arquivos criptografados
### • Na tela informando o ataque deve existir um campo para inserir a chave e descriptografar os arquivos
### • Realizar a descriptografia dos arquivos na pasta após a chave ser inserida

# Ransomware Simulado

## Descrição do Projeto

Este projeto é uma implementação de um ransomware simulado utilizando Python. O objetivo é demonstrar como um ransomware pode criptografar arquivos em um diretório alvo e exibir uma mensagem ao usuário, informando sobre o ataque e solicitando uma chave para a descriptografia. Este projeto é apenas para fins educacionais e não deve ser utilizado de forma maliciosa.

## Funcionalidades

O código é capaz de realizar as seguintes ações:

- **Criptografar uma pasta alvo:** O ransomware pode ser configurado para criptografar todos os arquivos em um diretório específico.
  
- **Exibir uma mensagem em tela:** Ao finalizar a criptografia, uma interface é exibida ao usuário informando sobre o ataque e fornecendo detalhes sobre como proceder.

- **Salvar a chave de criptografia:** A chave usada para criptografar os arquivos é salva em um arquivo chamado `key.rans` na mesma pasta onde os arquivos criptografados estão localizados.

- **Campo para inserir a chave:** A interface do ransomware inclui um campo onde o usuário pode inserir a chave para descriptografar os arquivos.

- **Descriptografar arquivos:** Após inserir a chave correta, o ransomware descriptografa os arquivos previamente criptografados.

## Estrutura do Projeto


## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu_usuario/ransomware_simulado.git
   cd ransomware_simulado
   pip install flask twilio cryptography pillow
   python app.py
   
# CP-02

```bash
CP-02/
├── pasta_alvo/                    # Pasta contendo os arquivos a serem criptografados
│   ├── documento.txt              # Arquivo original a ser criptografado
│   ├── documento_cript.txt        # Arquivo de texto criptografado
│   └── key.rans                   # Arquivo contendo a chave de criptografia
│
├── static/                        # Pasta contendo arquivos estáticos
│   ├── real.gif                   # GIF original
│   ├── real.gif.enc               # GIF criptografado
│   └── trava.png                  # Ícone de “trava” usado na interface
│
├── templates/                     # Pasta contendo templates HTML
│   └── index.html                 # Arquivo HTML que exibe a interface do usuário
│
└── app.py                         # Código principal do ransomware

