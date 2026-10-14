# Hướng dẫn thực hành HDFS Hadoop trên Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/duykhanhworking22-spec/hadoop-hdfs-colab/blob/main/HDFS_Hadoop_Google_Colab.ipynb)

## Hướng dẫn chạy trên Google Colab

1. Nhấp vào biểu tượng **Open In Colab** ở trên hoặc truy cập trực tiếp theo đường dẫn:
   https://colab.research.google.com/github/duykhanhworking22-spec/hadoop-hdfs-colab/blob/main/HDFS_Hadoop_Google_Colab.ipynb

2. Trên thanh menu của Google Colab, chọn **Runtime** -> **Run all** (hoặc nhấn tổ hợp phím **Ctrl + F9**) để thực thi toàn bộ bài thực hành từ đầu đến cuối một cách tự động.

3. Hoặc có thể thực thi từng ô lệnh (Cell) theo thứ tự từ trên xuống dưới để theo dõi chi tiết từng nội dung:
   - Phần A: Cài đặt Apache Hadoop 3.5.0 và thiết lập biến môi trường (JAVA_HOME, HADOOP_HOME, PATH).
   - Phần B: Cấu hình hệ thống HDFS Pseudo-Distributed (core-site.xml, hdfs-site.xml, mapred-site.xml).
   - Phần C: Khởi tạo NameNode và khởi động các tiến trình nền NameNode, DataNode.
   - Phần D: Khai thác và thao tác dữ liệu qua HDFS CLI (mkdir, put, ls, cat, head, tail, cp, mv, du, df, get, rm).
   - Phần E: Kiểm tra cấu trúc block vật lý và tình trạng toàn vẹn hệ thống (fsck, dfsadmin).
   - Phần F: Thực thi bài toán MapReduce WordCount với input và output lưu trữ trên HDFS.
   - Phần G: Thực thi bài toán Hadoop Streaming MapReduce với Python (tính doanh thu theo ngành hàng từ dữ liệu orders_2026_09.csv).
   - Phần H: Dừng và khởi động lại dịch vụ HDFS.
   - Phần I: Bảng tra cứu và xử lý các lỗi thường gặp.

## Lưu ý khi thực hiện

- Toàn bộ mã nguồn, cấu hình và dữ liệu mẫu đã được xây dựng tự động trong Notebook. Người học hoặc người chấm bài không cần tải hay cài đặt thêm phần mềm trên máy cá nhân.
- Lệnh format NameNode (hdfs namenode -format) chỉ được chạy duy nhất một lần ở bước khởi tạo ban đầu. Không chạy lại lệnh này khi DataNode đã có dữ liệu để tránh lỗi lệch Cluster ID.
- Google Colab là môi trường runtime tạm thời, các tệp trong thư mục /content sẽ được làm mới khi phiên làm việc bị ngắt kết nối.
