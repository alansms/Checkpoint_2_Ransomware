import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from twilio.rest import Client
from cryptography.fernet import Fernet
from PIL import Image

# Inicializa a aplicação Flask
app = Flask(__name__)
app.secret_key = "super_secret_key"  # Chave secreta para sessões

# Credenciais do Twilio para envio de SMS
account_sid = 'xxxxxxxxxxx'
auth_token = 'xxxxxxxxx'
twilio_phone_number = 'xxxxxxx'

client = Client(account_sid, auth_token)  # Inicializa o cliente Twilio

# Caminhos dos arquivos e pastas
KEY_FILE = 'pasta_alvo/key.rans'  # Arquivo que armazena a chave de criptografia
TEXT_FILE = 'pasta_alvo/documento.txt'  # Arquivo original de texto
ENC_TEXT_FILE = 'pasta_alvo/documento_cript.txt'  # Arquivo de texto criptografado
GIF_FILE = 'static/real.gif'  # GIF original
ENC_GIF_FILE = 'static/real.gif.enc'  # Arquivo do GIF criptografado
ICON_FILE = 'static/trava.png'  # Ícone a ser exibido na interface

# Gera e salva uma chave de criptografia
def generate_key():
    key = Fernet.generate_key()  # Gera uma nova chave usando Fernet
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)  # Salva a chave em um arquivo
    print(f"Chave gerada: {key.decode()}")
    return key

# Carrega a chave do arquivo key.rans
def load_key():
    try:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()  # Lê a chave do arquivo
            print(f"Chave carregada: {key.decode()}")
            return key
    except FileNotFoundError:
        flash("Erro: Arquivo de chave não encontrado.")  # Mensagem de erro se o arquivo não for encontrado
        return None

# Criptografa o conteúdo de um arquivo e salva no arquivo de destino
def encrypt_file(file_path, enc_file_path, key):
    print(f"Criptografando arquivo: {file_path}")
    fernet = Fernet(key)  # Inicializa o objeto Fernet com a chave
    with open(file_path, 'rb') as file:
        original = file.read()  # Lê o conteúdo do arquivo original
    encrypted = fernet.encrypt(original)  # Criptografa o conteúdo
    with open(enc_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)  # Salva o conteúdo criptografado
    print(f"Arquivo criptografado com sucesso: {enc_file_path}")

# Descriptografa o conteúdo de um arquivo criptografado e recria o arquivo original
def decrypt_file(enc_file_path, file_path, key):
    print(f"Descriptografando arquivo: {enc_file_path}")
    fernet = Fernet(key)  # Inicializa o objeto Fernet com a chave
    try:
        with open(enc_file_path, 'rb') as encrypted_file:
            encrypted = encrypted_file.read()  # Lê o conteúdo criptografado
        decrypted = fernet.decrypt(encrypted)  # Descriptografa o conteúdo
        with open(file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted)  # Salva o arquivo descriptografado
        print(f"Arquivo {file_path} recriado com sucesso")
    except Exception as e:
        print(f"Erro ao descriptografar: {e}")  # Mensagem de erro em caso de falha

# Função para descriptografar o GIF
def decrypt_gif(enc_file_path, file_path, key):
    try:
        decrypt_file(enc_file_path, file_path, key)  # Descriptografa o GIF criptografado
        with Image.open(file_path) as img:
            img.verify()  # Verifica se a imagem é válida
        print("Imagem descriptografada com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao descriptografar a imagem: {e}")
        return False

# Função para ler o conteúdo criptografado de um arquivo para exibir no frontend
def read_encrypted_content(enc_file_path, key):
    fernet = Fernet(key)  # Inicializa o objeto Fernet com a chave
    with open(enc_file_path, 'rb') as file:
        encrypted_content = file.read()  # Lê o conteúdo criptografado
    return fernet.decrypt(encrypted_content).decode()  # Retorna o conteúdo descriptografado como string

# Rota inicial para exibir a página principal
@app.route('/')
def index():
    key = load_key()  # Carrega a chave
    encrypted_text = "O documento está criptografado. Insira a chave para descriptografá-lo."
    return render_template('index.html', encrypted_text=encrypted_text)

# Rota para descriptografar o arquivo de texto e a imagem
@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()  # Recebe dados JSON da requisição
    input_key = data.get('key').strip()  # Obtém a chave inserida pelo usuário
    stored_key = load_key()  # Carrega a chave armazenada

    # Debug: Verificar se as chaves são iguais
    print(f"Chave armazenada: {stored_key.decode() if stored_key else 'Nenhuma'}")
    print(f"Chave inserida: {input_key}")

    if stored_key and input_key.encode().strip() == stored_key.strip():  # Verifica se a chave está correta
        try:
            # Descriptografa o arquivo de texto
            decrypt_file(ENC_TEXT_FILE, TEXT_FILE, stored_key)

            # Descriptografa o GIF
            success_gif = decrypt_gif(ENC_GIF_FILE, GIF_FILE, stored_key)

            if success_gif:
                decrypted_text = read_encrypted_content(ENC_TEXT_FILE, stored_key)
                return jsonify(success=True, message="Seus arquivos foram descriptografados com sucesso!",
                               decrypted_text=decrypted_text)
            else:
                return jsonify(success=False, error="Falha ao descriptografar a imagem.")
        except Exception as e:
            print(f"Erro ao descriptografar: {e}")
            return jsonify(success=False, error=str(e))
    else:
        print("Chave incorreta.")
        return jsonify(success=False)

# Rota para enviar a chave por SMS
@app.route('/send_key', methods=['POST'])
def send_key():
    phone_number = request.form['phone_number'].strip()  # Obtém o número de telefone do formulário
    phone_number = f"+55{phone_number}"  # Formata o número para o padrão brasileiro
    key = load_key()  # Carrega a chave
    if key:
        try:
            message = client.messages.create(
                body=f"Sua chave de descriptografia é: {key.decode()}",
                from_=twilio_phone_number,
                to=phone_number
            )
            flash(f"Mensagem enviada para {phone_number} com sucesso.")  # Mensagem de sucesso
        except Exception as e:
            flash(f"Erro ao enviar a chave: {e}")  # Mensagem de erro ao enviar
    else:
        flash("Erro ao enviar mensagem. Arquivo de chave não encontrado.")
    return redirect(url_for('index'))  # Redireciona para a página inicial

if __name__ == '__main__':
    # Verifica se a chave já existe e criptografa os arquivos se necessário
    if not os.path.exists(KEY_FILE):
        key = generate_key()  # Gera uma nova chave se não existir
        encrypt_file(TEXT_FILE, ENC_TEXT_FILE, key)  # Criptografa o arquivo de texto
        encrypt_file(GIF_FILE, ENC_GIF_FILE, key)  # Criptografa o arquivo GIF
        print(f"Arquivos criptografados com sucesso. Chave: {key.decode()}")
    else:
        key = load_key()  # Se a chave existir, carrega-a

    app.run(debug=True, port=5007, host='0.0.0.0')  # Inicia o servidor Flask