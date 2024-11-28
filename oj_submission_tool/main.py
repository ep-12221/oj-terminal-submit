import click
import os
from submission.submitter import submit_code
from problem.fetcher import fetch_problem
from session_manager import OJSessionManager

# 存储当前OJ设置和登录状态的全局变量
current_oj = None
logged_in = False

@click.group()
def cli():
    """命令行工具"""
    pass

@click.command()
@click.argument('file')
@click.option('--pid', default=None, help='题号（PID）')
@click.option('--lang', default=None, help='语言（LANG）')
def submit(file, pid, lang):
    """提交代码到OJ"""
    if not current_oj:
        print("请设置OJ！")
        return

    if not pid:
        print("请指定题号（PID）！")
        return

    if not lang:
        print("请指定语言（LANG）！")
        return

    # 调用提交函数
    submit_code(file, pid, lang, current_oj)

@click.command()
@click.option('--oj', default=None, help='设置OJ平台')
def set(oj):
    """设置OJ平台和登录状态"""
    global current_oj
    if oj:
        current_oj = oj
        print(f"已设置OJ为 {oj}")
    elif logged_in:
        logout()
    else:
        print("没有设置OJ，请使用 --oj 选项设置OJ。")

@click.command()
@click.option('--pid', required=True, help='题号（PID）')
def fetch(pid):
    """抓取题目"""
    if not current_oj:
        print("请设置OJ！")
        return
    
    fetch_problem(pid, current_oj)

@click.command()
def login():
    """登录OJ"""
    global logged_in
    if logged_in:
        print("您已经登录！")
        return
    
    
    logged_in = True
    print("登录成功！")

@click.command()
def logout():
    """登出OJ"""
    global logged_in
    if not logged_in:
        print("您没有登录！")
        return

    OJSessionManager.logout()
    logged_in = False
    print("登出成功！")

# 将命令添加到CLI组
cli.add_command(submit)
cli.add_command(set)
cli.add_command(fetch)
cli.add_command(login)
cli.add_command(logout)

if __name__ == '__main__':
    cli()
