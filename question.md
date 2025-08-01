问题1：
    git push -u origin main
    报错，提示：error: src refspec main does not match any
解决方案：
    git branch -a
    如果本地显示 * master，而远程只有 main，就是这个问题，需要修改本地分支名
    git branch -m master main # 将master重命名为main
    git push -u origin main # 重新推送
问题2：
    git branch -m master main    # 将master重命名为main
    git push -u origin main 
    运行以上命令后，网页端登录github后，终端没反应
解决方案：
     强制终端响应
    按几次 回车键（可能卡在隐藏的输入提示）
    尝试 Ctrl+C 中断后重新执行命令
问题3：
    dir /a
    dir : 找不到路径“D:\a”，因为该路径不存在。
    所在位置 行:1 字符: 1
解决方案：
    检查当前目录是否正确
    可以使用 cd 命令切换到正确的目录
    例如：cd D:\myproject
