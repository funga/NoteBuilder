#!/bin/bash
#ecoding=utf-8
import MySQLdb

conn = MySQLdb.connect("10.237.36.176","pecker_user","123456","test_mtr2",3202,'utf8')

cur = conn.cursor()
cur.execute('SELECT e.ikey FROM mtr_event e WHERE e.ikey IN (SELECT i.ikey FROM  mtr_issue i where i.update_date > "2017-03-24 00:00:00" AND i.create_date > date_sub(NOW(),INTERVAL 90 DAY )) AND e.remark LIKE "创建%"')
data = cur.fetchone()
print data
