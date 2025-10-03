import smbus2
import time
import datetime

# ==========================================================
# CONFIGURAÇÕES GERAIS
# ==========================================================
I2C_BUS = 2  # Barramento I2C da Labrador (/dev/i2c-2)
try:
    bus = smbus2.SMBus(I2C_BUS)
except FileNotFoundError:
    print(f"Erro: Barramento I2C {I2C_BUS} não encontrado.")
    print("Verifique se o hardware está conectado corretamente e se o barramento I2C está habilitado.")
    exit()

# Arquivo de log
LOG_FILE = "/media/caninos/CARTAO M/dados_luminosidade.txt"

# ==========================================================
# SEÇÃO: SENSOR BH1750 (Luminosidade)
# ==========================================================
BH1750_ADDR = 0x23
BH1750_CMD = 0x10

def read_bh1750():
    try:
        data = bus.read_i2c_block_data(BH1750_ADDR, BH1750_CMD, 2)
        # Converte os 2 bytes em um valor de luminosidade
        lux = (data[0] << 8 | data[1]) / 1.2
        return lux
    except OSError as e:
        print(f"Erro de I/O ao ler o sensor BH1750: {e}")
        print("Verifique a conexão do sensor e o endereço I2C.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao ler o BH1750: {e}")
        return None

# ==========================================================
# FUNÇÃO MAIN
# ==========================================================
def main():
    print("Iniciando o datalogger do sensor de luminosidade BH1750.")
    print(f"Os dados serão salvos em: {LOG_FILE}")
    print("Pressione Ctrl+C para encerrar o programa.")

    try:
        while True:
            # Pega o timestamp atual formatado
            timestamp = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")

            # Lê o valor do sensor
            lux = read_bh1750()

            # Formata a string para exibição e gravação
            if lux is not None:
                log_line = f"[{timestamp}] Luminosidade: {lux:.2f} Lux"
            else:
                log_line = f"[{timestamp}] Luminosidade: Dados não disponíveis"

            # Imprime a leitura no console
            print(log_line)

            # Grava a leitura no arquivo de log
            try:
                with open(LOG_FILE, "a") as f:
                    f.write(log_line + "\n")
            except FileNotFoundError:
                print(f"Erro: O diretório ou arquivo de log não foi encontrado: {LOG_FILE}")
                print("Verifique se o cartão microSD está montado corretamente e o caminho está certo.")
                time.sleep(5)
            except Exception as e:
                print(f"Erro ao escrever no arquivo de log: {e}")


            time.sleep(1)

    except KeyboardInterrupt:
        print("\nLeitura encerrada pelo usuário.")
    finally:
        bus.close()
        print("Barramento I2C fechado.")

# ==========================================================
# PONTO DE ENTRADA DO SCRIPT
# ==========================================================
if __name__ == "__main__":
    main()