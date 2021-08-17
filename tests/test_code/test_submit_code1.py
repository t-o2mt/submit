import datetime

def test_submit_code1(case_path, ans_path):

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

  # テストケースやモデルアンサーを読み込む
  def get_data(path):
    result = []
    f = open(path)
    datalist = f.readlines()
    for data in datalist:
      l = list(map(str, data.split(',')))
      l[-1] = l[-1].strip('\n')
      result.append(l)
    f.close()

    return result
  
  log = get_data(case_path)
  model_ans = get_data(ans_path)
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
      if servers[address]['count'] >= 1:
        failure_period = servers[address]['datetime'] + ' ~ ' + get_datetime()
        ans.append([address, str(failure_period)])

      # サーバの状態を初期化
      servers[address]['count'] = 0
      servers[address]['datetime'] = ''

  for address, server in servers.items():
    if server['count'] >= 1:
      failure_period = server['datetime'] + ' ~ -'
      ans.append([address, failure_period])

  judge = ans == model_ans

  return judge