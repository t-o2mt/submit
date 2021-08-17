import datetime

# 確認日時をdatetime表記で返す
def get_datetime():
  year = int(checked_datetime[:4])
  month = int(checked_datetime[4:6])
  day = int(checked_datetime[6:8])
  hour = int(checked_datetime[8:10])
  minute = int(checked_datetime[10:12])
  second = int(checked_datetime[12:])

  return str(datetime.datetime(
    year=year, month=month, 
    day=day, hour=hour, 
    minute=minute, second=second
  ))

N = int(input())
log = []
while True:
  s = str(input())
  if not s:
    break
  l = list(map(str, s.split(',')))
  log.append(l)

servers = {}
ans = []

for checked_datetime, address, response_time in log: # 確認日時, サーバアドレス, 応答結果
  if address not in servers:

    # count: 連続でタイムアウトになった回数
    # datetime: 最初にタイムアウトになった確認日時
    servers[address] = {'count': 0, 'datetime': ''}

  if response_time == '-':
    servers[address]['count'] += 1

    if servers[address]['count'] == 1:
      servers[address]['datetime'] = get_datetime()
  else:
    if servers[address]['count'] >= N:

      failure_period = servers[address]['datetime'] + ' ~ ' + get_datetime()
      ans.append([address, failure_period])

    # サーバの状態を初期化
    servers[address]['count'] = 0
    servers[address]['datetime'] = ''

# 故障期間が求められなかった故障状態のサーバを探索
for address, server in servers.items():
  if server['count'] >= N:
    failure_period = server['datetime'] + ' ~ -'
    ans.append([address, failure_period])

for address, failure_period in ans:
  print(address + ',' + failure_period)