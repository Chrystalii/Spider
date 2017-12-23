# coding=utf-8

import pymysql

def insert(fourthpage_title, names_lists_insert, value_lists_insert,thirdpage_id):

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

        "INSERT INTO attribute(title,attribute_name,attribute_value,title_id) VALUES (%s,%s,%s,%s)",
        (fourthpage_title, names_lists_insert, value_lists_insert,thirdpage_id))
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
