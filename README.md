# OverRide-Server
This is the server &amp; package repo of a OverRapid mod that I made a while back. Open to all since the dev abandoned the game and is no longer adding new content.

这是Project OverRide的服务器和包体仓库。Project OverRide是一个基于OverRapid的模组，由于原开发者长期未更新内容，现公开。

<details>
<summary>English</summary>
<br>

## Why OverRide

This mod brings comprehensive feature updates, content, and bug fixes to the base game.

This non-exaustive list describes some of those.

-	Added 14 removed songs (Lag train, rainshower, happy?, cancer, chaotic, after white, overprocess, unfactual factory, euphoric planet, dawn, sudden noise, night ocean fantasy, Metatron rebirth, hymn for U).

-   Support for all 32 Arcane charts.

-	Added 3 removed BGAs (xmas17, cosmic, decryptor).

-	Added 2 removed Companions (doge, xmas17).

-	Added 1 removed Gear (xmas17).

-   Improved localization for all languages, and the game is localized to Simplified Chinese. (by improve, I mean that most image-based texts are changed to code based for better resolution and easier update. Korean and Japanese is mostly done by Google Translate, which is not ideal)

-   Ability to connect to server directly (without proxy software)

-   iOS, Android, and PC support.

-   "Invisible Note" and speed up/down (0.8x - 1.2x) playstyle

-   Added 10 achievements from season challenge 1.

-	Added removed BGE for Outer Space.

-	Officially supports project OverWrite (Missed charts for old songs) and save optimization.

-	Added Hadron Kollider 4kpro (converted from 6k, very hard), and BGE support for all difficulties for H1V3.

-	Revamped song unlock mechanism. Packs can be unlocked via RP and more songs are added to the level-up mechanism.

-	Optimized and refactored game logic, removed redundant code, and optimized client and server assets.

-	Added ability to restore save file via UID input at name prompt. Removed social OAUTH function.

-   Supports download all charts and offsets via freeplay console.

-   All functionality except leaderboard, download, ratings ranking, and PVP works offline. (must be connected at least once)

-   Remade login client user flow. User need to create username first before downloading files.

-   Ability to disable account creation, and ban user from server.

-	Removed source code compilation and song encryption.

-   Fixed multiple issues with TKR skin and allow detailed opacity customization through settings - BGA Opacity, and expanded the applicable song for Lanota BGE.

-   TKR theme has been improved - switch over and check it out!

-   Added Render The Over Stage theme (old application theme) that supports all modern features.

-   Built in full fanmade chart support. Import on server, play on client solo or multiplayer immediately.

-   General bug fixes.

## The Server

Download the code and asset, unzip the asset in the server root directory.

## The Asset

There are three folders of assets that you must set up before the server is functional.

They are all placed under the server root directory.

`OverRapid`: Contains music, chart, BGA, and config files. They are stable, and incremental.

`OverRide`: Skeleton folder for fanmade content. Typically, you don't need to mess with it.

`Resource`: Contains basic assets, such as images, movies, and transition audios. This is volatile, and the content inside can shift around as version progress.

Below are the Google Drive and Baidu Drive link to a folder, containing two zip files.

Download and unzip some or all of them to the root directory.

If this is your first time setting the server up, download both zip files.

If you are here for an upgrade, only download the `Resources` `素材包2` pack, delete the original `Resources` folder, and overwrite any conflicting files.

V4 Asset: [Google Drive](https://drive.google.com/drive/folders/1jR37N2wi6M1l0Eq1QeO-UkVtXPd-vkJt?usp=sharing) [Baidu Drive](https://pan.baidu.com/s/1jhzKBP3zP0dnfgcsLS1xGQ Code: AAAA)

After this, follow the Manual.

## Manual

<details>
<summary>Click to expand</summary>
<br>

### Preface

Please join QQ group (511974777) or use the issues section to report server and client issues.

### Server Setup and Connection

Download the server and respective platform's installation package from the group files/github release.

Unzip the server to your PC or MAC (referred to as the machine) and install the application package to your mobile device (referred to as the device). ~~Linux users should help themselves lol~~

Android package has been renamed and icon replaced to allow better distinction with the official client. You need jailbroken devices and tools such as trollstore to install on iOS.

Install ```python``` and ```pip``` on your machine. To install ```pip``` on MAC, you can use

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

Note that MAC uses ```python3```. Code examples in this document will use the default of Windows, which is ```python```. After the installation, install dependencies using ```pip install requirements.txt```

After it is installed, make sure your machine and device are under the same subnetwork, such as wifi. Open ``cmd`` on PC and type ``ipconfig``. Open ``terminal`` on MAC and type ``ifconfig``.

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

#### Adding currency

Currently, the game grants unlimited currency. In case that was changed in the future, you can issue a redemption code in the database with the following `item`: `[{"item": "rp", "value": "99999"}]`.

#### Disable registration

Set ```REGISTRATION``` in ```config.py``` to ```False```. Account can only be restored via UID after this is turned off.

#### Ban user

Open ```player.db``` using ```DB Browser``` and go to the specific player. change the ```banned``` value. 0 means not banned. 1 means the user cannot change their nickname nor submit scores to leaderboard. If the value is a string, the user will be prompted the string as the reason of their ban, and the client will close after the the text prompt is shown (after intro video is done).

#### Reset leaderboard

clear the ```rank``` table of the database.


</details>

## Fanmade

`OverRide` uses `BMS` charting specification. Audio playbacks are overwritten (keysound will not work, and the sound files specified within the chart file is ignored). Channel 0, 1, 2 are the left 3 lanes, 3, 4 are scratch lanes for left and right, and 5, 6, 7 are the right 3 lanes. Speed changes can be specified using BMS's built in `bpm` channel, horizontal white lines are defined in channel 9.

Chart reversals require special flag `0B` and `0C` - the effect is enabled for two songs (`miserable` and `tkr`) on the official listing, and all charts on the fanmade listing.

Two ways to make charts:

1.	Use OSU! Mania to make 8k or 6k charts and convert the ```.osu``` file to ```.bms```. The conversion tool is in the group file. Note: Use text editor to remove negative value ```TimingPoint``` from the ```.osu``` charts, or the tool will report error. After conversion, use a text editor to replace all ```ZZ``` to ```01```. After that, open the ```.bms``` chart with ```pBMsc``` to fix and modify. The chart should not contain non-01 value.

2.	Use Malody to make 8k or 6k charts and convert the file to ```.osu```, then convert to `bms`. [code](https://github.com/Jakads/malody2osu)

// I will leave the actual charting to the professionals

You should have a ```mp3``` file and ```bms``` charts.

Make a ```id``` string for the song. Don't worry about collisions, as ```importer``` can address these. Find a thumbnail and name it ```id.jpg/png```.
Rename the charts to ```id_difficulty.bms```. Supported difficulties are ```EL,EX,PR,LPR,EL4,EX4,PR4```

Place charts to ```note``` folder. Place the thumbnail to ```thumbs``` folder. Place the music to ```music``` folder.
 
That's it for files. Next, let's modify ```manifest.json```.

```
[
  {
    "id": 1, // Ignore
    "title": "Music Name", // Music title
    "artist": "Music Artist", //Musician
    "isJapanese": false,	//Use Japanese display mode
    "bpm": 167,	//bpm number
    "sync_6k": "0/0/0/-1400", //Chart offset values. 6k: EL,EX,LPR,PR. 4k: EL,EX,PR.
    "sync_4k": "0/0/0",
    "diff_6k": "0/0/0/18",	// Chart difficulty。If not charted, use 0.
    "diff_4k": "0/0/0",
    "charter_6k": "-/-/-/charterA", //Charter information
    "charter_4k": "-/-/-",
    "mp3": "song",	//Song ID.
    "preview": "-1/-1", //Start time of 2 music previews, in seconds.
    "bga": "-1400/24/3559" // Delete this line if no BGA is available
    }
]
```

If you wish to make BGA, see section below. If not, delete the ```bga``` field.

That's it for the manifest. Select all files and folders, and compress to ```zip```. See "Adding Charts" section for chart importing.

#### Importer File Checking

`importer` will conduct basic check for the zip file. If the check is passed, only the necessary files will be copied to the server. 5 checks are conducted:

0. At least one chart should be defined in config.

Example: `diff_6k` and `diff_4k` not all zeroes.

1.	A correctly named jpg or png should be in the thumbs folder.

Example: If the song ID is ```test```, a ```test.jpg``` or ```test.png``` should exist.

2.	The correctly named mp3 should be in the music folder.

Example: If the song ID is ```test```, a ```test.mp3``` should exist.

3.	If the manifest contains bga section, the bga zip file should be in the bga folder.

Example: If the song ID is ```test``` and has a ```bga``` section in manifest, a ```test.zip``` should exist.
 
4.	If the manifest does not have bga, there should not be a bga zip file in the bga folder.

Example: If song ID ```test``` does not have ```bga``` section in manifest, ```test.zip``` should not exist. Note: Did you forget to add the bga to manifest?

5.	All difficulties specified in the manifest should have a corresponding note file in the note folder.

Example: Song ID is ```test``` and manifest specifies multiple non-zero difficulties. All charts should exist.

### Making BGA

Download the MP4 from YouTube or other platforms. 360p is enough.

Put the video in the folder from the archive. Remember to ```pip install opencv-python```

Open ```cmd``` in the directory and type ```python v2b.py```

Follow the instructions. ```fps``` are typically 15 or 24. After the frames are extracted, go to the output folder and remove the black frame at the start and end to save some space.

ZIP all the images and fill the ```bga``` section of the manifest.

The 1st number is the millisecond offset. The 2nd number is the frame rate. The 3rd number is the frame number of the last frame.

Add the zip archive to the bga directory.

### Addendium for OverRide

In addition to the respective github repo, the tooling is also available in the `tools` folder. There is also this minimal client-server setup for fanmade charting specifically [Fanmade Server](https://github.com/qwerfd2/OverRapid-Fanmade-Server/)

That project is technically separate from Project OverRide, since that one is specifically designed for fanmade and carries some merit for that purpose (minimal server and client asset, essential assets are local, server only used for fanmade assets delivery, no official content), although it still requires a server to be set up (flask, not starlette).

Note: Although the fanmade chart package format is the exact same, the `importer.py` from the fanmade repo is NOT COMPATIBLE with Project OverRide. Project OverRide requires several additional considerations during implementation (collision with official listing and local assets, asset cleanup, compatibility with official manifest format), which means that although the tooling does the same thing, they way they achieved it is very different.

When importing a chart, you do not need to worry about:

1. The `mp3` value colliding with the official listing - everything is stored in either a different location or uses a different format;

2. Residual local assets if a fanmade song is deleted server-side - music, chart, and bga are automatically deleted if the manifest change is detected;

Note that the game client never had a way to customize per-song sync offset. That is done exclusively server-side, via `OverRide/playmanifest.json`.

`CNG`/`ARC`/`BRK` Difficulty is not supported for fanmade charts.

</details>

<details>
<summary>中文</summary>
<br>

## 为什么要OverRide

这个魔改带来了全新功能更新，内容，和bug修复。
如下是不全面的列表，描述了一些功能。

-   添加14首移除曲目 (Lag train, rainshower, happy?, cancer, chaotic, after white, overprocess, unfactual factory, euphoric planet, dawn, sudden noise, night ocean fantasy, Metatron rebirth, hymn for U)。

-   支持全部32个Arcane谱面。

-	添加3个移除的BGA (xmas17, cosmic, decryptor)。

-	添加2个移除的头像 (doge, xmas17)。

-	添加1个移除的皮肤 (xmas17)。

-   优化所有语言的本地化，支持简体中文。(优化是指把原版的文字图片替换成了代码，以获得清晰度并降低修改难度。日语和韩语是用Google翻译的 - 不是很理想)

-   可以直连私服，不需要中继软件。

-   iOS, 安卓, 和 PC 支持。

-   "隐形音符" 和加减速 (0.8x - 1.2x) 玩法。

-   添加了10个来自季节挑战的。。。挑战。

-	添加了 Outer Space 的BGE.

-	官方支持 Project OverWrite 和存档优化功能。

-	添加了Hadron Kollider的4k难度（超难），和H1V3的全难度特效支持。

-	重做解歌系统。曲包可用RP解锁，玩家等级解锁添加更多曲目。

-	优化游戏逻辑，删除无用代码，优化服务器和安装包资源。

-	支持通过UID恢复存档。移除社交媒体OAUTH功能。

-   支持通过FP控制台下载所有谱面和偏移值。

-   除了分数排行榜，文件下载，评级排行榜，和PVP，所有功能离线均可用。(必须先联网下载全部数据)

-   重做客户端登录流程。用户需要先起名才能下载资源。

-   可以关闭账号注册功能，也可以封禁用户。

-	移除歌曲文件加密和源码编译。

-   修复TKR皮肤的若干问题，透明度可通过BGA透明度自定义，调整Lanota BGE受用的曲目。

-   TKR重制-快切换过去看看吧！

-   添加Render The Over Stage主题（老版本主题），支持全部新功能。

-   内置完备的自制谱支持。服务器导入，立刻在客户端单机或多人游玩。

-   修复Bug。

## 服务器

下载所有代码和资源，把资源解压到服务器根目录。

## 资源

在服务器可用前，有三个需要配置的文件夹。

都位于根目录下。


`OverRapid`: 包括音乐，谱面，BGA，和配置文件。稳定，可以版本更新。

`OverRide`: 自制内容的初始文件夹。不需要担心。

`Resource`: 包括基础素材，比如图像，视频，和音频。不稳定，可能出现很多变化。

如下Google Drive和百度网盘链接指向一个文件夹，包括两个zip文档。

根据需求，下载一个或全部并解压到服务器根目录。

如果这是你第一次配置服务器，全部下载。

如果你是来这里更新的，那么可以仅下载`Resources` `素材包2`。把老的`Resources`文件夹删掉，覆盖任何冲突内容。

V4 Asset: [Google Drive](https://drive.google.com/drive/folders/1jR37N2wi6M1l0Eq1QeO-UkVtXPd-vkJt?usp=sharing) [Baidu Drive](https://pan.baidu.com/s/1jhzKBP3zP0dnfgcsLS1xGQ Code: AAAA)

之后，跟随使用手册配置。

## 使用手册

<details>
<summary>点击放大</summary>
<br>

### 前言

如有错漏敬请加群（511974777）联系。欢迎使用Github Issues汇报服务器及客户端错误。

### 搭建服务器和连接


群文件或Github Release下载服务器，下载对应平台的安装包。

PC 或 MAC（统称主机）解压服务器，~~linux 自己去搞（~~

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

#### 添加货币

目前，游戏给予无限货币。若以后发生改变，可以使用兑换码机制来添加货币。在数据库添加一个兑换码，`item`为`[{"item": "rp", "value": "99999"}]`。

#### 关闭注册

把```config.py```里的```REGISTRATION```设成```False```。如果关闭，只能通过UID恢复已有账号来开始游戏。

#### 封禁用户

用```DB Browser```打开```player.db```。找到该用户。修改```banned```数值。0代表不封禁。1代表禁止昵称修改并禁止排行榜分数上传。如果数值是字符串，玩家在开场视频结束后将被提示封禁，该字符串将显示给玩家，作为封禁理由。客户端将会关闭。

#### 重置排行榜

清除```rank```数据库表。

</details>

## 自制

```OverRide``` 使用 ```BMS``` 谱面格式。音频播放不可用（按键音不可用，谱面文件内的音频被无视）。0, 1, 2 轨为左侧 3 轨，3, 4 为左右划键，5, 6, 7 为右侧 3 轨。变速可在谱面内通过`BPM`轨设定，水平白线通过9轨设定。

谱面倒退可以通过 ```0B``` 和 ```0C``` 来指定 - 官方列表只有两首可以使用（`miserable` 和 `tkr`），自制没有限制。

目前的两个制谱方式：
 
1.	通过 OSU! Mania 制 8k/6k 谱并将 ```.osu``` 文件转至 ```.bms```。转码工具在群文件里。注意事项：提前用文本编辑器删除负值 ```TimingPoint```，否则工具会报错。转码后用文本编辑器将所有 ```ZZ``` 变成 01. 之后用 ```pBMsc``` 打开 ```bms``` 进行修改修复并保存。谱面内不应出现非 01 的值。

2.	通过 Malody 制 8k/6k 谱并将谱面转至 ```.osu```, 再使用上述方法转至 `bms`. [代码](https://github.com/Jakads/malody2osu)

//具体制谱思路让专业的来写（

现在，你应该有歌曲的 ```mp3``` 音乐文件，和 ```bms``` 谱面。

给歌曲定个 ```id``` 字符串。不用担心和别人重名，如果使用 ```importer``` 导入会自动解决。找到歌曲的封面并重命名为 歌曲 ```id.jpg/png```.
将谱面重命名为 ```id_难度.bms```，支持的难度为 ```EL,EX,PR,LPR,EL4,EX4,PR4```.
谱面放到 ```note``` 文件夹。歌曲封面放到 ```thumbs```。音乐文件放到 ```music```。不要放无关的文件。至此，文件安放完毕。接下来要修改 ```manifest.json```.

```
[
  {
    "id": 1, // 无视
    "title": "Music Name", // 曲名
    "artist": "Music Artist", //曲师
    "isJapanese": false,	//是否用日语模式显示 
    "bpm": 167,	//bpm 数字
    "sync_6k": "0/0/0/-1400", //谱面偏移值. 6k: EL,EX,LPR,PR. 4k: EL,EX,PR.
    "sync_4k": "0/0/0",
    "diff_6k": "0/0/0/18",	// 谱面难度。如果没有谱面填 0.
    "diff_4k": "0/0/0",
    "charter_6k": "-/-/-/charterA", //谱师信息
    "charter_4k": "-/-/-",
    "mp3": "song",	//歌曲 ID。
    "preview": "-1/-1", //两段音乐 preview 开始时间，以秒计
    "bga": "-1400/24/3559" //如曲目没有BGA删除此行
  }
]

```

如果想做 BGA 可以参考下方。如果不想做必须删除 ```bga``` 行。

至此，```manifest``` 编辑完成。全选所有文件夹和 ```manifest.json```，压缩成 ```zip```。
 
导入可以参考“添加谱面”章节。

### Importer 文件检查


```importer``` 会对包体进行基本检查。如果检查通过，只会将需要的文件拷贝到服务器里。总共检查 5 项内容：

0. 配置文件中至少要有一个谱面难度。

举例：`diff_4k`和`diff_6k`不能全是0.

1.	至少一个正确命名的 jpg 或 png 图片应该在 thumbs 文件夹里。

举例：如果歌曲 ID：```test```，```test.jpg``` 或者 ```test.png``` 应该存在。

2.	正确命名的 MP3 文件应该在 music 文件夹里。

举例：如果歌曲 ID：```test```，```test.mp3``` 应该存在。

3.	如果 manifest 里有 bga，则 bga 压缩包应该在 bga 文件夹里。

举例：如果歌曲 ID：```test``` 且 manifest 里有 ```bga``` 行，```test.zip``` 应该存在。

4.	如果 manifest 里没有 ```bga``` 而 ```bga``` 文件夹里存在 ```bga``` 压缩包。虽然不会出现错误程序也会提示。

举例：歌曲 ID：```test``` 且 manifest 里没有 ```bga``` 行，而 ```test.zip``` 存在。是不是忘写进 manifest 了？

5.	写进 manifest 的谱面难度应该都在 note 文件夹里。

举例：歌曲 ID：```test``` 且 manifest 里写明有多个非 0 难度，而 ```note``` 里缺少谱面。


### 制作 BGA

油管或者其他平台下载视频 MP4 文件。清晰度只要是 360p 以上就行。

将视频文件放到解压的文件夹里。记得 ```pip install opencv-python```

文件夹内 ```cmd``` 输入 ```python v2b.py```

根据提示操作，一般 ```fps``` 为 15 或 24. 完成后进入文件夹，删除黑屏的帧来节省空间。
 
所有图片压 zip 包，填写 manifest 里的 ```bga```。

第一个数字为毫秒偏移。第二个数字为帧率。第三个数字为最后一帧的数字。将压好的 zip 包放到 ```bga``` 文件夹里。


### OverRide附加内容

上面描述的工具既可以在他们自己的仓库下载，也可以在本仓库的`tools`文件夹找到。还有一个更袖珍的客户端-服务器方案，专为自制谱设计。[自制服务器](https://github.com/qwerfd2/OverRapid-Fanmade-Server/)

这个项目之所以和OverRide区分开，是因为它专为自制设计，有些独有的优势（最小化客户端和服务器资源，必要资源内置无需下载，服务器仅用作自制文件运输，无官方内容），尽管这个方案仍需要一个服务器（`flask`而不是`starlette`）

提示：尽管自制导入的文件完全一样，自制服务器的`importer.py`不可和此项目的`importer.py`混用。在这里，有一些特殊的考量（和官方列表和文件的冲突，资源清理，列表兼容），导致具体实施完全不同。

在导入时，不需要担心：

1. `mp3`和官方重叠 - 所有文件和配置都要么存在不同的地方，要么使用了不同的格式；

2. 服务器删曲后本地资源留存 - 当列表变化到达本地，音乐，谱面，和bga将被自动删除；

注意，客户端从没有具体谱面偏移调整保存的能力 - 这是服务器端功能，需要通过修改`OverRide/playmanifest.json`来实现。

自制不支持 `CNG`/`ARC`/`BRK` 难度。

</details>
