import datetime
import collections

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
m, t = map(int, input().split())
log = []
while True:
  s = str(input())
  if not s:
    break
  l = list(map(str, s.split(',')))
  log.append(l)

servers = {}
failure_ans = []
overload_ans = []

# 本処理
for checked_datetime, address, response_time in log: # 確認日時, サーバアドレス, 応答結果
  if address not in servers:

    # timeout_count: 連続でタイムアウトになった回数
    # response_count: 応答が返ってきた回数
    # response_que: 直近m回までの応答時間を格納するキュー
    # response_avg: 直近m回までの応答時間の合計値
    # timeout_datetime: 最初にタイムアウトになった確認日時
    # overload_datetime: 最初に過負荷状態になった確認日時
    servers[address] = {
      'timeout_count': 0,
      'response_count': 0,
      'response_que': collections.deque([]),
      'response_sum': 0.0,
      'timeout_datetime': '',
      'overload_datetime': ''
    }

  # 故障についての処理
  if response_time == '-':
    servers[address]['timeout_count'] += 1
    if servers[address]['timeout_count'] == N:
      servers[address]['timeout_datetime'] = get_datetime()
  else:
    if servers[address]['timeout_count'] >= N:
      failure_period = servers[address]['timeout_datetime'] + ' ~ ' + get_datetime()
      failure_ans.append([address, failure_period])

    # 過負荷についての処理
    servers[address]['response_count'] += 1
    response_time = int(response_time)
    servers[address]['response_que'].append(response_time)

    if servers[address]['response_count'] == m:
      servers[address]['response_sum'] = sum(servers[address]['response_que'])

    if servers[address]['response_count'] > m:
      pop_time = servers[address]['response_que'].popleft()
      servers[address]['response_sum'] += (response_time - pop_time)

    avg = servers[address]['response_sum'] / m

    if avg > t:
      if not servers[address]['overload_datetime']:
        servers[address]['overload_datetime'] = get_datetime()
    else:
      if servers[address]['overload_datetime']:
        overload_period = servers[address]['overload_datetime'] + ' ~ ' + get_datetime()
        overload_ans.append([address, overload_period])
        servers[address]['overload_datetime'] = ''

    # サーバの状態を初期化
    servers[address]['timeout_count'] = 0
    servers[address]['timeout_datetime'] = ''

# 期間が求められなかった故障、過負荷状態のサーバを探索
for address, server in servers.items():
  if server['timeout_count'] >= N:
    failure_period = server['timeout_datetime'] + ' ~ -'
    failure_ans.append([address, failure_period])

  if server['response_count'] >= m and server['response_sum'] / m > t:
    overload_period = server['overload_datetime'] + ' ~ -'
    overload_ans.append([address, overload_period])

print('Failure')
for address, failure_period in failure_ans:
  print(address + ',' + failure_period)

print('Overload')
for address, overload_period in overload_ans:
  print(address + ',' + overload_period)