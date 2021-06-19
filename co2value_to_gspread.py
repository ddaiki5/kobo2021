from scd30_i2c import SCD30
import time
import gspread
import json
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定
credentials = ServiceAccountCredentials.from_json_keyfile_name('co2datasheet-fe0719027bca.json', scope)
 
gc = gspread.authorize(credentials)

SPREADSHEET_KEY = '1VAL9gU8JjSywUGrwPBCFWwzvSuto3BR3DTZmiBg9FMY'
 
worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('fromPi')

#scd30設定
scd30 = SCD30()

scd30.set_measurement_interval(2)
scd30.start_periodic_measurement()

time.sleep(2)

while True:
    x=0
    while x<1:
        if scd30.get_data_ready():
            m = scd30.read_measurement()
            if m is not None:
                co2, temp, rh = m[0], m[1], m[2]
                #print(f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
                x=1
        else:
            x=0
            time.sleep(0.2)
            
    worksheet.update_cell(2, 1, co2)
    worksheet.update_cell(2, 2, temp)
    worksheet.update_cell(2, 3, rh)

    time.sleep(900)
