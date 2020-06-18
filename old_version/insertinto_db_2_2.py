# coding=utf-8

import pymysql

def insert(thirdpage_url_id, thirdpage_id):

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

        "INSERT INTO relationship(source,destination) VALUES (%s,%s)",
        (thirdpage_url_id, thirdpage_id))
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
