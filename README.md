# 正方2017版教务系统课表导出工具
导出到 iCalender 文件  
> 如有帮助，请 Star；如有问题，请提 issue；如有不爽，请提 PR
### 用法
    1. 将 kbSourceJson 修改为你课表源文件([获取方式](#获取课表源文件))的地址
    2. 将 classBegintime 修改为你学校的作息表
    3. 类 WhenWhoWhere 中 firstDay 改为第一周周一的日期
    4. 类 WhenWhoWhere 中 genname() 的返回值可改可不改(仅对Google Calender做了测试)
    5. 运行，可在当前目录下得到 classTable.ics 文件
### 效果图：
![Calender.App](https://i.imgur.com/GUFA1iT.png)
### 获取课表源文件
登录教务系统后，依次进入 信息查询 -> 推荐课表打印 -> 查询 -> 打开开发者工具(F12 或 ⌘ + ⌥ + I) -> 将 /kbdy/bjkbdy_cxBjKb.html 请求得到的 json 文件保存
![DevTools](https://i.imgur.com/1iHOubo.png)
### 本软件针对的教务系统截图
![教务系统首页截图](https://i.imgur.com/vL0frqv.png)
### TODO
- [ ] 基于面向对象重构
- [ ] 自动登录