# OverRide-Server
This is the server &amp; package repo of a OverRapid mod that I made a while back. Open to all since the dev abandoned the game and is no longer adding new content.

## The Server

Download the code and asset, unzip the asset in the server root directory.

## The Asset

There are two folders of assets that you must download before the server is functional.

They are all placed under the server root directory.

`OverRapid`: Contains music, chart, BGA, and config files. They are stable, and incremental.

`Resource`: Contains basic assets, such as images, movies, and transition audios. This is volatile, and the content inside can shift around as version progress.

Below are the Google Drive and Baidu Drive link to a folder, containing two zip files.

Download and unzip some or all of them to the root directory.

If this is your first time setting the server up, download both zip files.

If you are here for an upgrade, only download the `Resources` `素材包2` pack, delete the original `Resources` folder, and overwrite any conflicting files.

V4 Asset: [Google Drive](https://drive.google.com/drive/folders/1jR37N2wi6M1l0Eq1QeO-UkVtXPd-vkJt?usp=sharing) [Baidu Drive](https://pan.baidu.com/s/1jhzKBP3zP0dnfgcsLS1xGQ Code: AAAA)

After this, follow the Manual.

## The Client

Simply download the client, install/sideload, and run. Follow the UI to enter the `http(s)://HOST:PORT/`, and click continue.

Note. The package released carries the same security level as the official packages, from the official stores. Don't snoop around, but certainly have fun!

## Manual

<details>
<summary>Click to expand</summary>
<br>

### Preface

Please join QQ group (511974777) to report issues. It is not encouraged to use the private server to play the official content. Help will not be provided for this.

### Server Setup and Connection

Download the server and respective platform's installation package from the group files.

Unzip the server to your PC or MAC (referred to as the machine) and install the application package to your mobile device (referred to as the device). Linux users should help themselves lol

Android package has been renamed and icon replaced to allow better distinction with the official client. You need jailbroken devices and tools such as trollstore to install on iOS.

Install ```python``` and ```pip``` on your machine. To install ```pip``` on MAC, you can use

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

Note that MAC uses ```python3```. Code examples in this document will use the default of Windows, which is ```python```. After the installation, install dependencies using ```pip install requirements.txt```

After it is installed, make sure your machine and device are under the same subnetwork, say, wifi. Open ```cmd``` on PC and type ```ipconfig```. Open ```terminal``` on MAC and type ```ifconfig```.

Use the output to find the machine's subnet IPV4. Open ```config.py``` inside the server folder and change the IP address to the one you just got. Change the port as you please.
 
Open cmd in the server directory and type ```python 5002.py```. Wait a moment. Once the server started, Open the app on your device.

In the Connection UI, enter the server's ```http://ip:port/``` according to the specification.

Click OK, and enter a username, or an existing 24-digit ```UID``` (covered in the "Advanced" section).

Download all the resources and enter the game.

### Advanced

#### Log in using ```UID```:

Use if you have registered before and would like to set up a new device with it.

Go to the settings page on your old device. Click the "Account" text under the "Account Settings" header 4 times. Your ```UID``` will be displayed and can be saved via screenshot. Go to the new device, enter the ```UID``` on the username page, and click OK.

You can also find the ```UID``` by opening ```player.db``` using ```DB Browser```.

#### Disable registration

Set ```REGISTRATION``` in ```config.py``` to ```False```. Account can only be restored via UID after this is turned off.

#### Ban user

Open ```player.db``` using ```DB Browser``` and go to the specific player. change the ```banned``` value. 0 means not banned. 1 means the user cannot change their nickname nor submit scores to leaderboard. If the value is a string, the user will be prompted the string as the reason of their ban, and the client will close after the the text prompt is shown (after intro video is done).

#### Reset leaderboard

clear the ```rank``` table of the database.


</details>

## 使用手册

<details>
<summary>点击放大</summary>
<br>

### 前言

如有错漏敬请加群（511974777）联系。不鼓励使用私服游玩官曲的行为。不会提供这方面的帮助。

### 搭建服务器和连接


群文件下载服务器，下载对应平台的安装包。

PC 或 MAC（统称主机）解压服务器，linux 自己去搞（

设备安装下载好的安装包。 Android 已修改包名和图标，不会和官方冲突。iOS 需要 trollstore 之类的 jailbroken 工具。

主机安装 ```python```，安装 ```pip```。MAC 安装 ```pip``` 可使用

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

注意 MAC 默认为 ```python3```。往后的示例默认用 windows 的默认，即 ```python```。安装完成后 ```pip install requirements.txt```

安装完成后，设备和主机确认在同一子网下，例如 wifi。

PC 打开 ```cmd``` 输入 ```ipconfig```。MAC 打开 ```terminal``` 输入 ```ifconfig```。进而找到本机的子网 IPV4。
主机打开服务器文件夹的 ```config.py``` 修改 IP 地址。Port 也可以更改。

服务器文件夹内 ```cmd``` 输入 ```python 5002.py```，等一小会。跑起来之后，设备打开程序.

接下来的连接窗口，按照格式输入服务器的 ```http://ip:port/```

点击 OK，输入用户名或已有的 24 位 ```UID```（高级操作章节）。下载资源，进入游戏。

### 高级操作

#### 使用 ```UID``` 登录：

你之前注册过账号，并想用这个账号在新设备上玩。

进入老设备的设置页面。点击 账号设置 下的标题文字 账号 4 次。```UID``` 将显示，可以截屏保存。在新的设备上的登陆界面输入 ```UID```，点击确认。

你也可以用```DB Browser```打开```player.db```来寻找```UID```。

#### 关闭注册

把```config.py```里的```REGISTRATION```设成```False```。如果关闭，只能通过UID恢复已有账号来开始游戏。

#### 封禁用户

用```DB Browser```打开```player.db```。找到该用户。修改```banned```数值。0代表不封禁。1代表禁止昵称修改并禁止排行榜分数上传。如果数值是字符串，玩家在开场视频结束后将被提示封禁，该字符串将显示给玩家，作为封禁理由。客户端将会关闭。

#### 重置排行榜

清除```rank```数据库表。

</details>
