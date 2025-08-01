1.安装git
2.验证是否安装成功
git --version
3.配置git
git config --global user.name "yourname"
git config --global user.email "你的GitHub注册邮箱"
4.检查配置是否成功
git config --list | findstr "user"
5.创建一个本地仓库
mkdir myproject
cd myproject
touch README.md
6.初始化仓库
git init  # 会在当前目录生成.git隐藏文件夹
ls -la    # 查看是否生成.git目录（Mac/Linux）
dir /a    # Windows查看隐藏目录
7.创建.ignore文件
touch .gitignore
8.在.gitignore文件中添加要忽略的文件或文件夹
# 忽略所有 .txt 文件
*.txt
# 忽略名为 secret.txt 的文件
secret.txt
# 忽略名为 .env 的文件
.env
# 忽略名为 node_modules 的文件夹
node_modules/
# 忽略名为 build 的文件夹
build/
# 忽略名为 dist 的文件夹
9.提交文件到仓库
git add .            # 添加所有文件到暂存区
git status           # 检查状态（应显示绿色文件）
git commit -m "首次提交：完成基础功能"  # 提交到本地仓库
10.创建远程仓库
在GitHub上创建一个新的仓库（repository）
11.关联本地仓库和远程仓库
# 复制HTTPS地址（在仓库创建后的页面）
git remote add origin https://github.com/你的用户名/python-demo.git
# 验证是否关联成功
git remote -v  # 应显示fetch/push地址
12.推送本地仓库到远程仓库
git push -u origin main  # 首次推送时需要-u参数
13.检查GitHub仓库
刷新仓库页面 → 应看到main.py和.gitignore文件
点击main.py → 确认代码内容正确
14.克隆远程仓库到本地
git clone https://github.com/你的用户名/python-demo.git
15.创建分支
git checkout -b add-chapter2  # 创建并切换到名为add-chapter2的分支
16.合并
正常合并
git checkout main       # 回到主分支
git merge your-feature  # 合并你的修改
冲突解决
git checkout main       # 回到主分支
git merge your-feature  # 合并你的修改
git status              # 查看冲突文件
# 如果你们俩都改了同一行代码...
CONFLICT (content): Merge conflict in hello.py
特殊合并
git merge --no-ff your-feature  # 强制保留合并记录
11

