# coding=utf-8

import pymysql

def insert(fourthpage_title, fourthpage_urloutput,fourthpage_content):

    conn = pymysql.connect(
        user='root',
        password='root',
        host='localhost',
        port=3306,
        database='baike_science',
        use_unicode=True,
        charset="utf8"
    )
    # 获取游标
    cur = conn.cursor()
    # 插入数据，注意看有变量的时候格式
    cur.execute('SET NAMES utf8mb4')
    cur.execute("SET CHARACTER SET utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    # cur.execute("SET character_set_client = gbk")
    # cur.execute("SET character_set_results = gbk")
    cur.execute(

        "INSERT INTO webpage(id,title,url,content) VALUES (%s,%s,%s,%s)",
        (fourthpage_title, fourthpage_urloutput,fourthpage_content))
    # 提交
    cur.close()
    conn.commit()
    # 关闭连接
    conn.close()

# 建表
# 写代码
# 测试
# 整合
# 程序中调用
