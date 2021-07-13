# Convertible_Bond_Monitor
设置定时任务，每天抓取最新的可转债信息，并通过 sct.ftqq.com 推送到微信

## 使用方法
安装依赖项：
```
pip3 install requests datetime
```

在 [sct.ftqq.com](https://sct.ftqq.com) 扫码登录并获得 SendKey。然后在[消息通道](https://sct.ftqq.com/forward)中配置好你想要的消息通道，并做好测试，确保该 SendKey 可以将消息送达。

接着将 `config-sample.py` 复制并更名为 `config.py`，接着将你的 SendKey 填入其中，注意不要更改文件的格式。

最后在终端中运行：
```
python3 main.py
```

## 定时推送
- Linux：
  终端中运行 `crontab -e`，在文件末尾加上一行（注意换成实际的路径）
  ```
  0 9 * * * python3 /path/to/Convertible_Bond_Monitor/main.py
  ```

- Windows:
  见[Win10设置定时运行任务](https://zhuanlan.zhihu.com/p/115187442)

- macOS:
  新建一个 plist 文件，内容如下（**删掉注释**）
  ```
  <?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
  <plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.github.the-eric-kwok.Convertible_Bond_Monitor</string>
    <key>ProgramArguments</key>
    <array>
      <string>/usr/bin/python3</string>  //注意此处应更改为机器上实际的 python3 解释器路径
      <string>/path/to/Convertible_Bond_Monitor/main.py</string>  //注意此处应更改为实际的项目路径
    </array>
    <key>StartCalendarInterval</key>
    <dict>
          <key>Minute</key>
          <integer>0</integer>
          <key>Hour</key>
          <integer>9</integer>
      </dict>
  </dict>
  </plist>
  ```
  将这个文件更名为 `com.github.the-eric-kwok.Convertible_Bond_Monitor.plist` 并放到 `~/Library/LaunchAgent/` 下，然后运行
  ```
  launchctl load ~/Library/LaunchAgents/com.github.the-eric-kwok.Convertible_Bond_Monitor.plist
  launchctl list | grep "com.github.the-eric-kwok.Convertible_Bond_Monitor"  # 若出现结果则意味着加载成功
  # 测试启动
  launchctl start com.github.the-eric-kwok.Convertible_Bond_Monitor  # 若收到通知则运行正常
  ```
