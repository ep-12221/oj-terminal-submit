from setuptools import setup, find_packages

def parse_requirements(filename):
    """读取 requirements.txt 文件，并返回依赖列表"""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="oj-submission-tool",  # 项目名称
    version="0.1",
    packages=find_packages(),  # 查找并包含所有包
    install_requires=parse_requirements('requirements.txt'),  # 动态读取 requirements.txt
    entry_points={  # 命令行工具入口
        'console_scripts': [
            'oj-submit = oj_submission_tool.main:cli',  # 命令行工具入口
        ],
    },
    include_package_data=True,  # 确保包含配置文件等
    long_description=open('README.md').read(),  # 读取并包括README
)
