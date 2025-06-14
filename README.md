# So sánh hiệu năng B-tree và Array

Dự án này thực hiện so sánh hiệu năng giữa cấu trúc dữ liệu B-tree và Array trong các thao tác cơ bản như thêm, sửa, xóa và tìm kiếm.

## Cài đặt

1. Clone repository về máy:
```bash
git clone https://github.com/anhngocdang2723/btree-array-comparison.git
```

2. Di chuyển vào thư mục dự án:
```bash
cd btree-array-comparison
```

3. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Sử dụng

Chạy chương trình bằng lệnh:
```bash
python main.py
```

### Các chức năng chính

1. **Chạy Kiểm tra Hiệu năng**
   - So sánh tốc độ thực hiện các thao tác giữa B-tree và Array
   - Hỗ trợ chế độ tuần tự và đồng thời
   - Xuất kết quả ra file để phân tích

2. **Kiểm tra Trực tiếp**
   - Thêm mới dữ liệu
   - Cập nhật dữ liệu
   - Xóa dữ liệu
   - Tìm kiếm dữ liệu
   - Lưu cấu trúc cây B-tree
   - Tải cấu trúc cây B-tree
   - Xem danh sách cây đã lưu

### Cấu trúc thư mục

```
btree-array-comparison/
├── main.py              # File chính để chạy chương trình
├── requirements.txt     # Các thư viện cần thiết
├── module/             # Thư mục chứa các module
│   ├── btree.py        # Cài đặt B-tree
│   ├── comparison.py   # So sánh hiệu năng
│   └── ...
├── saved_trees/        # Thư mục lưu cấu trúc cây
└── Results/            # Thư mục chứa kết quả kiểm tra
```

### Dữ liệu mẫu

Chương trình hỗ trợ các tập dữ liệu có kích thước khác nhau:
- customers-1000.csv
- customers-10000.csv
- customers-100000.csv
- customers-1000000.csv
- customers-2000000.csv

Lưu ý: Bạn cần tạo thư mục `data` và đặt các file CSV vào đó.

### Lưu ý

1. Thư mục `saved_trees` sẽ được tạo tự động khi bạn lưu cấu trúc cây B-tree
2. Thư mục `Results` sẽ được tạo tự động khi bạn chạy kiểm tra hiệu năng
3. Các file kết quả được lưu dưới dạng JSON và có thể được phân tích sau
