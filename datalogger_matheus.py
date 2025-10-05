import smbus2
import time
import datetime
from periphery import I2C
import os

# CONFIGURAÇÕES GERAIS
I2C_BUS = 2  # Barramento I2C da Labrador (/dev/i2c-2)
LOG_INTERVAL_SECONDS = 60  # Intervalo de registro em segundos

# Caminho para o cartão SD. Os.path.join usado para compatibilidade
SD_CARD_PATH = "/media/caninos/CARTAO M" 
LOG_FILE = os.path.join(SD_CARD_PATH, "dados_sensores.txt")

# Inicializa o barramento principal
try:
    bus = smbus2.SMBus(I2C_BUS)
except FileNotFoundError:
    print(f"Erro: Barramento I2C {I2C_BUS} não encontrado. Verifique a configuração da Labrador.")
    exit()

# SENSOR BH1750 (Luminosidade)
BH1750_ADDR = 0x23
BH1750_CMD = 0x10  # Modo contínuo de alta resolução (1 Lux)

def read_bh1750():
    try:
        data = bus.read_i2c_block_data(BH1750_ADDR, BH1750_CMD, 2)
        lux = (data[0] << 8 | data[1]) / 1.2 # Converte para Lux (1.2 é o fator de conversão do datasheet)
        return lux
    except Exception as e:
        print(f"Erro ao ler BH1750: {e}")
        return None

# SENSOR AHT10 (Temperatura e Umidade)
AHT10_BUS_PATH = f"/dev/i2c-{I2C_BUS}"
AHT10_ADDRESS = 0x38
i2c_aht10 = I2C(AHT10_BUS_PATH)

def init_aht10():
    try:
        i2c_aht10.transfer(AHT10_ADDRESS, [I2C.Message([0xBE, 0x08, 0x00])]) # Comando de calibração
        time.sleep(0.02)  
        print("Sensor AHT10 inicializado.")
        return True
    except Exception as e:
        print(f"Erro ao inicializar AHT10: {e}")
        return False

def read_aht10():
    try:
        # 1. Dispara a medição
        i2c_aht10.transfer(AHT10_ADDRESS, [I2C.Message([0xAC, 0x33, 0x00])])
        time.sleep(0.08)  # Espera pela medição (mínimo 75ms)

        # 2. Lê os 6 bytes de dados
        read_msg = I2C.Message([0x00] * 6, read=True)
        i2c_aht10.transfer(AHT10_ADDRESS, [read_msg])
        data = read_msg.data

        # 3. Processa os dados conforme o datasheet
        # Formato: [Status, Umidade, Umidade, Umidade/Temp, Temp, Temp]
        hum_raw = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
        temp_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

        humidity = (hum_raw / 1048576) * 100
        temperature = (temp_raw / 1048576) * 200 - 50
        return temperature, humidity
    except Exception as e:
        print(f"Erro ao ler AHT10: {e}")
        return None, None # Retorna uma tupla para desempacotamento seguro

def main():
    print("Iniciando Datalogger...")
    
    # Verifica se o cartão SD está acessível
    if not os.path.isdir(SD_CARD_PATH):
        print(f"ERRO: O diretório do cartão SD '{SD_CARD_PATH}' não foi encontrado.")
        print("Verifique se o cartão está inserido e montado corretamente.")
        return 

    # Inicializa os sensores
    if not init_aht10():
        print("Não foi possível continuar sem o AHT10.")
        return

    print(f"Registrando dados em '{LOG_FILE}' a cada {LOG_INTERVAL_SECONDS} segundos.")
    print("Pressione Ctrl+C para encerrar.")

    try:
        while True:
            timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            lux = read_bh1750()
            temp, humid = read_aht10()

            lux_str = f"Luminosidade: {lux:.2f} Lux" if lux is not None else "Luminosidade: Falha na leitura"
            temp_str = f"Temperatura: {temp:.1f} C" if temp is not None else "Temperatura: Falha na leitura"
            humid_str = f"Umidade: {humid:.1f} %" if humid is not None else "Umidade: Falha na leitura"

            log_line = f"[{timestamp}] | {lux_str} | {temp_str} | {humid_str}"
            
            print(log_line)

            try:
                with open(LOG_FILE, "a") as f:
                    f.write(log_line + "\n")
            except Exception as e:
                print(f"ERRO CRÍTICO: Não foi possível escrever no arquivo '{LOG_FILE}'. {e}")

            time.sleep(LOG_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")
    finally:
        bus.close()
        i2c_aht10.close()
        print("Recursos I2C liberados.")

# PONTO DE ENTRADA DO SCRIPT
if __name__ == "__main__":
    main()