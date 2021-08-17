import datetime

def test_submit_code4(N, case_path, ans_path):

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
  subnets = {}
  servers = {}
  subnet_ans = []
  server_ans = []

  # subnetsとserversのデータを作成
  for checked_datetime, address, response_time in log: # 確認日時, サーバアドレス, 応答結果
    i = address.find('/')
    network_address = address[:i]

    if network_address not in subnets:

      # subnest: サブネット内のサーバアドレスをkeyにもつdict
      # isFailure: サブネットが故障状態であるかのフラグ
      # datetime: サブネット内のサーバが最初にタイムアウトになった確認日時
      subnets[network_address] = {'subnet': {}, 'isFailure': False, 'datetime': ''}

    if address not in subnets[network_address]['subnet']:

      # count: 連続でタイムアウトになった回数
      # datetime: 最初にタイムアウトになった確認日時
      subnets[network_address]['subnet'][address] = {'count': 0, 'datetime': ''}

    if address not in servers:
      
      # count: 連続でタイムアウトになった回数
      # datetime_list: 最初にタイムアウトになった確認日時
      servers[address] = {'count': 0, 'datetime': ''}


  # 本処理
  for checked_datetime, address, response_time in log: # 確認日時, サーバアドレス, 応答結果
    i = address.find('/')
    network_address = address[:i]

    subnet = subnets[network_address]['subnet']

    if response_time == '-':

      # サブネットの処理
      if not subnet[address]['datetime']:
        subnet[address]['datetime'] = get_datetime()

      subnet[address]['count'] += 1
      if not subnets[network_address]['isFailure']:

        # 故障状態かを判定するフラグ
        isFailure = True

        # サブネットが故障状態になった時に1番最初にタイムアウトしたサーバの確認日時を入れる変数
        failure_datetime = get_datetime()

        for ip_address in subnet:

          # サブネット内のサーバが１つでもN回以上タイムアウトしていなければサブネットの故障状態フラグを下げ、
          # そうでなければフラグを立てる
          if subnet[ip_address]['count'] < N:
            isFailure = False
            failure_datetime = ''
            break
          
          # 1番最初にタイムアウトしたサーバの確認日時を設定
          if subnet[ip_address]['datetime'] < failure_datetime:
            failure_datetime = subnet[ip_address]['datetime']
        
        subnets[network_address]['isFailure'] = isFailure
        subnets[network_address]['datetime'] = failure_datetime

      # サーバの処理
      servers[address]['count'] += 1
      if not servers[address]['datetime']:
        servers[address]['datetime'] = get_datetime()
    else:

      # サブネットの処理
      if subnets[network_address]['isFailure']:
        failure_period = subnets[network_address]['datetime'] + ' ~ ' + get_datetime()
        subnet_ans.append([network_address, failure_period])

      # サブネットの状態を初期化
      subnets[network_address]['datetime'] = ''
      subnets[network_address]['isFailure'] = False

      for ip_address in subnet.keys():
        subnet[ip_address]['count'] = 0
        subnet[ip_address]['datetime'] = ''

      # サーバの処理
      if servers[address]['count'] >= N:
        failure_period = servers[address]['datetime'] + ' ~ ' + get_datetime()
        server_ans.append([address, failure_period])

      # サーバの状態を初期化
      servers[address]['count'] = 0
      servers[address]['datetime'] = ''

  # 故障期間が求められなかった故障状態のサブネットを探索
  for network_address in subnets.keys():
    if subnets[network_address]['isFailure']:
      failure_period = subnets[network_address]['datetime'] + ' ~ -'
      subnet_ans.append([network_address, failure_period])
    
  # 故障期間が求められなかった故障状態のサーバを探索
  for address, server in servers.items():
    if server['count'] >= N:
      failure_period = server['datetime'] + ' ~ -'
      server_ans.append([address, failure_period])
  
  test_ans = [['Subnet failure']] + subnet_ans + [['Server failure']] + server_ans
  judge = test_ans == model_ans

  return judge
