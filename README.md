"# q9web" 
├── App    # App应用程序 Flask对象
│   ├── MobileApp  # 分块的手机APP模块，后台模块
│   │   ├── __init__.py  # Admin模块初始化文件，创建admin蓝图对象
│   │   ├── models.py  # 数据库模型文件
│   │   └── views.py  # 逻辑控制文件
│   ├── freeswitch # 分块的freeswitch模块， 前台模块
│   │   ├── __init__py  # Index模块初始文件，创建index蓝图对象
│   │   ├── models.py  # 数据库模型文件
│   │   └── views.py  # 逻辑控制文件
│   └── __init__.py  # App模块初始化文件，主要对db和app创建的方法
├── config.py  # 项目配置文件
├── manager.py  # 项目启动文件
├── static  # 静态文件
├── templates  # 模板文件
├── test  # 测试文件放置位置
└── utils  # 工具文件
    ├── functions.py
    └── __init__.py