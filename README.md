# 🐘 Thực Hành HDFS & Apache Hadoop Trên Google Colab

Dự án cung cấp bộ tài liệu, mã nguồn và Notebook hoàn chỉnh để triển khai, vận hành và thực hành cụm **Apache Hadoop HDFS (Mô hình Pseudo-Distributed)** trực tiếp trên nền tảng đám mây **Google Colab**.

---

## 📂 Cấu trúc Repository

```text
.
├── HDFS_Hadoop_Google_Colab.ipynb         # Notebook chính chạy toàn bộ bài thực hành trên Colab
├── Huong_dan_HDFS_Hadoop_tren_Google_Colab.docx # Tài liệu hướng dẫn gốc dạng văn bản
├── mapper_revenue.py                      # Python Mapper cho bài toán Hadoop Streaming (Doanh thu)
├── reducer_revenue.py                     # Python Reducer cho bài toán Hadoop Streaming (Doanh thu)
├── orders_2026_09.csv                     # Bộ dữ liệu giao dịch thương mại điện tử mẫu
├── transactions_sample.txt                # Bộ dữ liệu giao dịch tài chính mẫu cho bài lab tổng hợp
├── build_notebook.py                      # Mã nguồn Python tự động khởi tạo/cập nhật Notebook .ipynb
├── .gitignore                             # Danh sách loại trừ các file log, dữ liệu tạm, checkpoints
└── README.md                              # Hướng dẫn chi tiết dự án
```

---

## 🎯 Nội dung Thực hành trong Notebook

Notebook `HDFS_Hadoop_Google_Colab.ipynb` được chia thành các phần khoa học, dễ tiếp thu:

1. **Phần A - Cài đặt Hadoop & Thiết lập Môi trường**:
   - Kiểm tra OpenJDK.
   - Tải và giải nén Apache Hadoop 3.5.0 chính thức.
   - Cấu hình động `JAVA_HOME`, `HADOOP_HOME` và biến môi trường `PATH`.
2. **Phần B - Cấu hình HDFS Pseudo-Distributed**:
   - Tạo thư mục dữ liệu `namenode` và `datanode`.
   - Cấu hình tệp `core-site.xml` (`fs.defaultFS = hdfs://localhost:9000`).
   - Cấu hình tệp `hdfs-site.xml` (`dfs.replication = 1`).
   - Cấu hình tệp `mapred-site.xml` (chế độ `local`).
3. **Phần C - Khởi tạo & Vận hành HDFS Daemons**:
   - Khởi tạo metadata NameNode (`hdfs namenode -format -force`).
   - Khởi chạy các tiến trình daemon nền (`namenode`, `datanode`) không phụ thuộc SSH.
   - Kiểm tra các tiến trình Java bằng `jps` và xem báo cáo cụm với `hdfs dfsadmin -report`.
4. **Phần D - Khai thác & Quản trị HDFS CLI**:
   - Các lệnh thao tác tệp phân tán: `mkdir`, `put`, `ls`, `cat`, `head`, `tail`, `cp`, `mv`, `du`, `df`, `get`, `rm`.
5. **Phần E - Khảo sát Block Vật lý & Sức khỏe Cụm**:
   - Kiểm tra block ID, vị trí block của tệp tin qua `hdfs fsck ... -files -blocks -locations`.
   - Kiểm tra tính toàn vẹn của toàn bộ namespace HDFS.
6. **Phần F - Xử lý Dữ liệu MapReduce WordCount**:
   - Chạy job WordCount mẫu sử dụng JAR tích hợp sẵn của Hadoop với input/output trực tiếp trên HDFS.
7. **Phần G - (Mở Rộng) Hadoop Streaming MapReduce với Python**:
   - Ứng dụng phân tích dữ liệu đơn hàng `orders_2026_09.csv`.
   - Chạy `mapper_revenue.py` và `reducer_revenue.py` qua `hadoop-streaming.jar` để tính tổng doanh thu theo ngành hàng (category) với trạng thái `SUCCESS`.
8. **Phần H - Quản trị Vòng đời Dịch vụ**:
   - Dừng và khởi động lại dịch vụ HDFS mà không làm mất dữ liệu.
9. **Phần I - Bảng Tra cứu Xử lý Lỗi (Troubleshooting)**.

---

## 🚀 Hướng dẫn Đẩy Dự Án Lên GitHub

Nếu bạn muốn đưa thư mục này lên GitHub cá nhân, hãy mở **PowerShell** hoặc **Terminal** tại thư mục này và chạy các lệnh sau:

### 1. Khởi tạo Git và Commit
```bash
# Khởi tạo repository cục bộ
git init

# Thêm tất cả các file vào khu vực chuẩn bị
git add .

# Tạo commit đầu tiên
git commit -m "feat: initial commit with Hadoop HDFS Colab notebook, scripts, and sample datasets"
```

### 2. Liên kết với Repository trên GitHub
1. Truy cập [GitHub](https://github.com), đăng nhập và chọn **New Repository** (đặt tên ví dụ: `hadoop-hdfs-google-colab`).
2. Không cần chọn tạo sẵn README hay .gitignore (vì ta đã có sẵn).
3. Chạy lệnh liên kết và đẩy code lên:

```bash
# Đổi tên nhánh mặc định thành main (nếu chưa)
git branch -M main

# Thêm remote GitHub (thay <USERNAME> và <REPO_NAME> bằng của bạn)
git remote add origin https://github.com/<USERNAME>/<REPO_NAME>.git

# Đẩy mã nguồn lên GitHub
git push -u origin main
```

---

## 🌐 Cách Mở Trực Tiếp Notebook Trên Google Colab

Sau khi đẩy mã nguồn lên GitHub, bạn hoặc bất kỳ ai đều có thể mở và chạy trực tiếp Notebook bằng đường dẫn sau:

```text
https://colab.research.google.com/github/<USERNAME>/<REPO_NAME>/blob/main/HDFS_Hadoop_Google_Colab.ipynb
```

*(Chỉ cần thay `<USERNAME>` và `<REPO_NAME>` bằng tên tài khoản và tên kho lưu trữ của bạn).*

---

## 📋 Bảng Tra Cứu Lệnh HDFS Thường Dùng

| Mục đích | Cú pháp lệnh |
| :--- | :--- |
| **Liệt kê tệp/thư mục** | `hdfs dfs -ls /path` |
| **Tạo thư mục** | `hdfs dfs -mkdir -p /path` |
| **Đẩy tệp từ Local lên HDFS** | `hdfs dfs -put -f local_file /hdfs/path/` |
| **Đọc nội dung tệp** | `hdfs dfs -cat /hdfs/path/file` |
| **Tải tệp từ HDFS về Local** | `hdfs dfs -get /hdfs/path/file local_path` |
| **Sao chép trong HDFS** | `hdfs dfs -cp src_hdfs dst_hdfs` |
| **Di chuyển / Đổi tên** | `hdfs dfs -mv src_hdfs dst_hdfs` |
| **Xóa tệp** | `hdfs dfs -rm /hdfs/path/file` |
| **Xóa thư mục (đệ quy)** | `hdfs dfs -rm -r /hdfs/path/` |
| **Kiểm tra dung lượng tệp/thư mục** | `hdfs dfs -du -h /hdfs/path` |
| **Kiểm tra dung lượng HDFS** | `hdfs dfs -df -h /` |
| **Báo cáo tình trạng cụm / DataNode** | `hdfs dfsadmin -report` |
| **Khảo sát Block và vị trí lưu trữ** | `hdfs fsck /path/file -files -blocks -locations` |

---

## ⚠️ Lưu ý Quan trọng khi sử dụng Colab
1. **Chỉ Format NameNode 1 lần duy nhất**: Không chạy lại lệnh `hdfs namenode -format` khi DataNode đang có dữ liệu, vì điều này làm mất đồng bộ `Cluster ID` gây lỗi DataNode không khởi động được.
2. **Cảnh báo Cgroup của JVM**: Các thông báo `[warning][os,container]...` do cơ chế cgroup container của Google Colab gây ra, **hoàn toàn vô hại** và không ảnh hưởng đến cụm HDFS.
3. **Môi trường tạm thời (Ephemeral)**: Khi Colab ngắt phiên (disconnect/reset runtime), các tệp trong `/content` sẽ bị xóa. Khi bắt đầu phiên mới, bạn chỉ cần chạy lại từ **Phần A** để dựng lại cụm.
