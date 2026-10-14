import json

def make_cell(cell_type, source, execution_count=None):
    if cell_type == "markdown":
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": [s + "\n" for s in source.split("\n")]
        }
    elif cell_type == "code":
        return {
            "cell_type": "code",
            "execution_count": execution_count,
            "metadata": {},
            "outputs": [],
            "source": [s + "\n" for s in source.split("\n")]
        }

cells = []

# Title & Overview
cells.append(make_cell("markdown", """# Thực Hành HDFS và Apache Hadoop Trên Google Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/duykhanhworking22-spec/hadoop-hdfs-colab/blob/main/HDFS_Hadoop_Google_Colab.ipynb)

---

## Mục tiêu và phạm vi
Notebook này cung cấp hướng dẫn thực hành triển khai mô hình **Hadoop HDFS Pseudo-Distributed** (NameNode và DataNode cùng chạy trên một runtime) trực tiếp trên nền tảng **Google Colab**.

Nội dung bao gồm:
1. Cài đặt và cấu hình cụm Hadoop 3.5.0 trên môi trường Linux Ubuntu của Colab.
2. Khởi tạo và quản lý các Hadoop daemon (NameNode, DataNode) qua lệnh hdfs --daemon.
3. Khai thác hệ thống tệp phân tán HDFS qua CLI (mkdir, put, ls, cat, head, tail, cp, mv, du, df, get, rm).
4. Kiểm tra cấu trúc block vật lý và tình trạng toàn cụm (hdfs fsck, dfsadmin -report).
5. Chạy ứng dụng tính toán MapReduce WordCount truyền thống.
6. (Mở rộng) Xử lý dữ liệu doanh thu E-Commerce với Hadoop Streaming MapReduce bằng Python.

---

Lưu ý:
- Môi trường Google Colab là tạm thời: Dữ liệu trong thư mục /content sẽ được làm mới khi ngắt kết nối phiên làm việc.
- Format NameNode duy nhất một lần: Chỉ thực hiện lệnh format NameNode lúc khởi tạo ban đầu. Không format lại khi cụm đã có dữ liệu để tránh lỗi lệch Cluster ID.
"""))

# Section A
cells.append(make_cell("markdown", """## Phần A: Cài đặt Hadoop và Thiết lập Môi trường
Kiểm tra môi trường Java có sẵn trên Colab, tải bộ cài Hadoop 3.5.0 và thiết lập biến môi trường."""))

cells.append(make_cell("code", """# Bước A1 & A2: Kiểm tra Java runtime
!java -version"""))

cells.append(make_cell("code", """# Bước A3: Cài đặt JDK headless nếu môi trường chưa có Java (Tùy chọn)
# !apt-get update -qq && !apt-get install -y openjdk-21-jdk-headless"""))

cells.append(make_cell("code", """# Bước A4 & A5: Tải bộ cài Hadoop 3.5.0 và giải nén vào /content
!wget -q https://archive.apache.org/dist/hadoop/common/hadoop-3.5.0/hadoop-3.5.0.tar.gz -O /content/hadoop-3.5.0.tar.gz
!tar -xzf /content/hadoop-3.5.0.tar.gz -C /content
!ls -ld /content/hadoop-3.5.0"""))

cells.append(make_cell("code", """# Bước A6 & A7: Thiết lập biến môi trường trong Notebook và hadoop-env.sh
import os, subprocess

# Xác định vị trí JAVA_HOME tự động trên máy Colab
java_home = subprocess.check_output(
    "dirname $(dirname $(readlink -f $(which java)))",
    shell=True, text=True
).strip()

os.environ["JAVA_HOME"] = java_home
os.environ["HADOOP_HOME"] = "/content/hadoop-3.5.0"
os.environ["PATH"] += ":/content/hadoop-3.5.0/bin:/content/hadoop-3.5.0/sbin"

print("JAVA_HOME   =", os.environ["JAVA_HOME"])
print("HADOOP_HOME =", os.environ["HADOOP_HOME"])

# Khai báo JAVA_HOME vào file cấu hình hadoop-env.sh
hadoop_env = "/content/hadoop-3.5.0/etc/hadoop/hadoop-env.sh"
with open(hadoop_env, "a") as f:
    f.write(f"\\nexport JAVA_HOME={os.environ['JAVA_HOME']}\\n")

print("Da cap nhat hadoop-env.sh thanh cong!")"""))

cells.append(make_cell("code", """# Bước A8: Kiểm tra Hadoop CLI
!hadoop version"""))

# Section B
cells.append(make_cell("markdown", """## Phần B: Cấu hình HDFS Pseudo-Distributed
Tạo thư mục dữ liệu cục bộ và ghi các tệp XML cấu hình (core-site.xml, hdfs-site.xml, mapred-site.xml)."""))

cells.append(make_cell("code", """# Bước B1: Tạo thư mục lưu metadata NameNode và block DataNode
!mkdir -p /content/hadoop_data/namenode
!mkdir -p /content/hadoop_data/datanode
!ls -ld /content/hadoop_data/*"""))

cells.append(make_cell("code", """# Bước B2: Cấu hình core-site.xml (Chỉ định NameNode tại localhost:9000)
%%writefile /content/hadoop-3.5.0/etc/hadoop/core-site.xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>"""))

cells.append(make_cell("code", """# Bước B3: Cấu hình hdfs-site.xml (Replication = 1, đường dẫn lưu trữ metadata và block)
%%writefile /content/hadoop-3.5.0/etc/hadoop/hdfs-site.xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///content/hadoop_data/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///content/hadoop_data/datanode</value>
    </property>
</configuration>"""))

cells.append(make_cell("code", """# Bước B4: Cấu hình mapred-site.xml (Chạy MapReduce ở chế độ local)
%%writefile /content/hadoop-3.5.0/etc/hadoop/mapred-site.xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>local</value>
    </property>
</configuration>"""))

cells.append(make_cell("code", """# Bước B5: Kiểm tra các giá trị cấu hình thực tế
!hadoop getconf -confKey fs.defaultFS
!hadoop getconf -confKey dfs.replication
!hadoop getconf -confKey mapreduce.framework.name"""))

# Section C
cells.append(make_cell("markdown", """## Phần C: Khởi tạo và Khởi động Dịch vụ HDFS
Format NameNode lần đầu và khởi động hai tiến trình daemon: NameNode và DataNode."""))

cells.append(make_cell("code", """# Bước C1: Format NameNode (Lưu ý: Chỉ chạy duy nhất một lần khi khởi tạo lab)
!hdfs namenode -format -force"""))

cells.append(make_cell("code", """# Bước C2, C3 & C4: Khởi động NameNode, DataNode và kiểm tra tiến trình Java
!hdfs --daemon start namenode
!hdfs --daemon start datanode
!jps"""))

cells.append(make_cell("code", """# Bước C5 & C6: Kiểm tra báo cáo DataNode và namespace HDFS
!hdfs dfsadmin -report
!hdfs dfs -ls /"""))

# Section D
cells.append(make_cell("markdown", """## Phần D: Khai thác và Quản trị HDFS CLI
Thực hành các thao tác quản trị tệp tin và thư mục trên HDFS."""))

cells.append(make_cell("code", """# Bước D1: Tạo cây thư mục làm việc trên HDFS
!hdfs dfs -mkdir -p /user/student/input
!hdfs dfs -mkdir -p /user/student/output
!hdfs dfs -ls -R /user/student"""))

cells.append(make_cell("code", """# Bước D2 & D3: Tạo tệp dữ liệu mẫu tại Colab và đưa lên HDFS (-put)
!printf "Hanoi,1200\\nDanang,850\\nHCM,1700\\nHanoi,950\\n" > /content/sales.txt
!cat /content/sales.txt

# Upload vào HDFS
!hdfs dfs -put -f /content/sales.txt /user/student/input/
!hdfs dfs -ls -h /user/student/input"""))

cells.append(make_cell("code", """# Bước D4, D5 & D6: Đọc tệp trực tiếp từ HDFS (-cat, -head, -tail)
!hdfs dfs -cat /user/student/input/sales.txt
!hdfs dfs -head /user/student/input/sales.txt
!hdfs dfs -tail /user/student/input/sales.txt"""))

cells.append(make_cell("code", """# Bước D7 & D8: Sao chép (-cp) và Đổi tên / Di chuyển (-mv) trong HDFS
!hdfs dfs -cp /user/student/input/sales.txt /user/student/input/sales_backup.txt
!hdfs dfs -mv /user/student/input/sales_backup.txt /user/student/input/sales_2026.txt
!hdfs dfs -ls /user/student/input"""))

cells.append(make_cell("code", """# Bước D9: Kiểm tra dung lượng tệp (-du) và dung lượng toàn hệ thống (-df)
!hdfs dfs -du -h /user/student/input
!hdfs dfs -df -h /"""))

cells.append(make_cell("code", """# Bước D10: Tải tệp từ HDFS về máy cục bộ Colab (-get)
!rm -f /content/sales_downloaded.txt
!hdfs dfs -get /user/student/input/sales.txt /content/sales_downloaded.txt
!cat /content/sales_downloaded.txt"""))

cells.append(make_cell("code", """# Bước D11: Xóa tệp trên HDFS (-rm)
!hdfs dfs -rm /user/student/input/sales_2026.txt
!hdfs dfs -ls /user/student/input"""))

# Section E
cells.append(make_cell("markdown", """## Phần E: Kiểm tra Block và Sức khỏe HDFS
Khảo sát cách HDFS lưu trữ block vật lý và tình trạng toàn vẹn dữ liệu."""))

cells.append(make_cell("code", """# Bước E1: Kiểm tra thông tin block của tệp sales.txt
!hdfs fsck /user/student/input/sales.txt -files -blocks -locations"""))

cells.append(make_cell("code", """# Bước E2 & E3: Kiểm tra sức khỏe toàn bộ HDFS và báo cáo chi tiết
!hdfs fsck /
!hdfs dfsadmin -report"""))

# Section F
cells.append(make_cell("markdown", """## Phần F: Thực thi MapReduce WordCount với Input/Output trên HDFS
Chạy bài toán MapReduce đếm tần suất từ mẫu bằng thư viện tích hợp sẵn của Hadoop."""))

cells.append(make_cell("code", """# Bước F1 & F2: Tạo input văn bản đưa lên HDFS và dọn dẹp thư mục output cũ
!printf "hadoop big data hadoop mapreduce\\nbig data analytics hadoop\\n" > /content/words.txt
!hdfs dfs -mkdir -p /user/student/wordcount/input
!hdfs dfs -put -f /content/words.txt /user/student/wordcount/input/

# Xóa output cũ nếu có (bắt buộc vì MapReduce không ghi đè thư mục đã tồn tại)
!hdfs dfs -rm -r -f /user/student/wordcount/output"""))

cells.append(make_cell("code", """# Bước F3: Thực thi job MapReduce WordCount
!hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /user/student/wordcount/input /user/student/wordcount/output"""))

cells.append(make_cell("code", """# Bước F4: Đọc kết quả WordCount từ HDFS
!hdfs dfs -cat /user/student/wordcount/output/part-r-00000"""))

# Section G: Advanced Streaming MapReduce with Python
cells.append(make_cell("markdown", """## Phần G (Mở rộng): Hadoop Streaming MapReduce với Python và Dữ liệu E-Commerce
Phân tích giao dịch từ tệp orders_2026_09.csv để tổng hợp tổng doanh thu theo ngành hàng (category) với trạng thái SUCCESS."""))

cells.append(make_cell("code", """# Bước G1: Tạo mapper_revenue.py
%%writefile /content/mapper_revenue.py
#!/usr/bin/env python3
import sys, csv

reader = csv.DictReader(sys.stdin)
for row in reader:
    if row.get("status") == "SUCCESS":
        category = row["category"]
        amount = int(row["amount"])
        print(f"{category}\\t{amount}")"""))

cells.append(make_cell("code", """# Bước G2: Tạo reducer_revenue.py
%%writefile /content/reducer_revenue.py
#!/usr/bin/env python3
import sys

current_key = None
current_sum = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\\t")
    if len(parts) != 2:
        continue
    key, value = parts[0], int(parts[1])
    
    if current_key == key:
        current_sum += value
    else:
        if current_key is not None:
            print(f"{current_key}\\t{current_sum}")
        current_key = key
        current_sum = value

if current_key is not None:
    print(f"{current_key}\\t{current_sum}")"""))

cells.append(make_cell("code", """# Bước G3: Chuẩn bị dữ liệu orders_2026_09.csv và đưa lên HDFS
import os

if not os.path.exists("/content/orders_2026_09.csv"):
    with open("/content/orders_2026_09.csv", "w", encoding="utf-8") as f:
        f.write("transaction_id,order_date,order_time,province,category,channel,quantity,unit_price,amount,status,shipping_days\\n")
        f.write("TX000001,2026-09-30,02:25:00,Ha Noi,Beauty,web,1,294947,294947,SUCCESS,2\\n")
        f.write("TX000002,2026-09-23,23:58:00,Da Nang,Grocery,mobile,1,265514,265514,SUCCESS,3\\n")
        f.write("TX000003,2026-09-05,15:38:00,Ha Noi,Electronics,partner,1,12741238,12741238,SUCCESS,3\\n")
        f.write("TX000004,2026-09-09,18:01:00,Hai Phong,Electronics,mobile,1,8846997,8846997,SUCCESS,4\\n")
        f.write("TX000005,2026-09-12,10:20:00,HCM,Beauty,web,2,500000,1000000,CANCELLED,1\\n")
        f.write("TX000006,2026-09-15,11:30:00,HCM,Grocery,mobile,3,100000,300000,SUCCESS,2\\n")
    print("Da tao orders_2026_09.csv mau!")

# Upload dữ liệu lên HDFS
!hdfs dfs -mkdir -p /user/student/orders/input
!hdfs dfs -put -f /content/orders_2026_09.csv /user/student/orders/input/
!hdfs dfs -ls /user/student/orders/input"""))

cells.append(make_cell("code", """# Bước G4: Chạy Hadoop Streaming MapReduce với Python
# Cấp quyền thực thi cho 2 script Python
!chmod +x /content/mapper_revenue.py /content/reducer_revenue.py

# Dọn dẹp output cũ
!hdfs dfs -rm -r -f /user/student/orders/output

# Xác định file JAR hadoop-streaming
import glob
streaming_jars = glob.glob("/content/hadoop-3.5.0/share/hadoop/tools/lib/hadoop-streaming-*.jar")
streaming_jar = streaming_jars[0] if streaming_jars else ""
print("Streaming JAR:", streaming_jar)

# Thực thi Hadoop Streaming Job
!hadoop jar $streaming_jar \\
    -files /content/mapper_revenue.py,/content/reducer_revenue.py \\
    -mapper "python3 mapper_revenue.py" \\
    -reducer "python3 reducer_revenue.py" \\
    -input /user/student/orders/input/orders_2026_09.csv \\
    -output /user/student/orders/output"""))

cells.append(make_cell("code", """# Bước G5: Xem kết quả thống kê doanh thu theo Category từ HDFS
!hdfs dfs -cat /user/student/orders/output/part-00000"""))

# Section H
cells.append(make_cell("markdown", """## Phần H: Dừng và Khởi động lại HDFS
Tạm dừng phiên làm việc hoặc khởi động lại trong cùng runtime mà không làm mất dữ liệu."""))

cells.append(make_cell("code", """# Bước H1: Dừng các daemon
!hdfs --daemon stop datanode
!hdfs --daemon stop namenode
!jps"""))

cells.append(make_cell("code", """# Bước H2: Khởi động lại (Lưu ý: Không chạy lệnh format)
!hdfs --daemon start namenode
!hdfs --daemon start datanode
!jps
!hdfs dfs -ls /user/student"""))

# Section I
cells.append(make_cell("markdown", """## Phần I: Bảng tra cứu xử lý lỗi (Troubleshooting)

| Tình trạng lỗi | Nguyên nhân | Cách khắc phục |
| :--- | :--- | :--- |
| localhost:9000 Connection refused | NameNode chưa chạy hoặc đã bị dừng | Chạy !hdfs --daemon start namenode rồi kiểm tra lại bằng !jps |
| !jps chỉ có NameNode, không có DataNode | DataNode khởi động chậm hoặc lỗi ghi block | Chạy !hdfs --daemon start datanode hoặc kiểm tra log bằng !tail -n 80 /content/hadoop-3.5.0/logs/*datanode*.log |
| Cluster ID mismatch | Chạy lại lệnh hdfs namenode -format khi DataNode đang giữ ID cũ | Dừng daemon, xóa sạch thư mục /content/hadoop_data/*, format lại từ đầu |
| Output directory already exists | Thư mục đầu ra MapReduce đã tồn tại | Xóa thư mục output trước: !hdfs dfs -rm -r -f <đường_dẫn_output> |
| hadoop: command not found | Mất biến môi trường khi restart runtime | Chạy lại Cell thiết lập JAVA_HOME, HADOOP_HOME và PATH ở Phần A |
| Cgroup memory/cpu controller path warning | Cảnh báo tài nguyên container của Google Colab | Cảnh báo vô hại, không ảnh hưởng đến hoạt động của Hadoop |
"""))

notebook = {
    "cells": cells,
    "metadata": {
        "colab": {
            "name": "HDFS_Hadoop_Google_Colab.ipynb",
            "provenance": [],
            "toc_visible": True
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

with open("HDFS_Hadoop_Google_Colab.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=2)

print("Da cap nhat xong tệp HDFS_Hadoop_Google_Colab.ipynb!")
