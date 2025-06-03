from module.comparison import DataStructureComparison
import time
import os
from module.result_exporter import ResultExporter

def run_comparison(file_path, operations=1000, concurrent=False, max_workers=4):
    print(f"\nĐang chạy so sánh với tập dữ liệu: {os.path.basename(file_path)}")
    print("=" * 50)
    
    start_time = time.time()
    comparison = DataStructureComparison()
    
    # Load data
    print("Đang tải dữ liệu...")
    comparison.load_data(file_path)
    load_time = time.time() - start_time
    print(f"Thời gian tải dữ liệu: {load_time:.2f} giây")
    
    # Run benchmarks
    print("\nĐang chạy kiểm tra hiệu năng...")
    results = comparison.benchmark_operations(operations, concurrent, max_workers)
    
    # Export results
    exporter = ResultExporter()
    dataset_info = {
        "file_path": file_path,
        "size": len(comparison.array_data),
        "fields": comparison.data_columns
    }
    benchmark_config = {
        "concurrent": concurrent,
        "operations": operations,
        "max_workers": max_workers
    }
    result_file = exporter.export_benchmark_results(dataset_info, benchmark_config, results)
    print(f"\nKết quả đã được xuất ra file: {result_file}")
    
    return results

def select_dataset():
    """Cho phép người dùng chọn tập dữ liệu từ các file có sẵn"""
    datasets = [
        "data/customers-1000.csv",
        "data/customers-10000.csv",
        "data/customers-100000.csv",
        "data/customers-1000000.csv",
        "data/customers-2000000.csv"
    ]
    
    print("\nCác tập dữ liệu có sẵn:")
    for i, dataset in enumerate(datasets, 1):
        if os.path.exists(dataset):
            print(f"{i}. {os.path.basename(dataset)}")
    
    while True:
        try:
            choice = int(input("\nChọn số thứ tự tập dữ liệu: "))
            if 1 <= choice <= len(datasets):
                selected = datasets[choice - 1]
                if os.path.exists(selected):
                    return selected
                else:
                    print("Không tìm thấy file dữ liệu đã chọn!")
            else:
                print("Lựa chọn không hợp lệ!")
        except ValueError:
            print("Vui lòng nhập một số hợp lệ!")

def get_benchmark_options():
    """Lấy cấu hình kiểm tra hiệu năng từ người dùng"""
    print("\nTùy chọn kiểm tra hiệu năng:")
    print("1. Tuần tự (thực hiện từng thao tác một)")
    print("2. Đồng thời (thực hiện nhiều thao tác cùng lúc)")
    
    while True:
        try:
            choice = int(input("\nChọn chế độ kiểm tra (1-2): "))
            if choice in [1, 2]:
                concurrent = (choice == 2)
                max_workers = 4  # Giá trị mặc định
                
                if concurrent:
                    try:
                        workers = int(input("Nhập số luồng xử lý đồng thời (mặc định=4): ") or "4")
                        if workers > 0:
                            max_workers = workers
                    except ValueError:
                        print("Sử dụng giá trị mặc định 4 luồng")
                
                try:
                    ops = int(input("Nhập số lượng thao tác (Enter để dùng mặc định=1000): ") or "1000")
                    if ops > 0:
                        return concurrent, max_workers, ops
                except ValueError:
                    print("Sử dụng giá trị mặc định 1000 thao tác")
                
                return concurrent, max_workers, 1000
            else:
                print("Lựa chọn không hợp lệ!")
        except ValueError:
            print("Vui lòng nhập một số hợp lệ!")

def direct_test():
    """Chạy kiểm tra trực tiếp các thao tác"""
    # Select dataset
    file_path = select_dataset()
    comparison = DataStructureComparison()
    exporter = ResultExporter()
    
    print("\nĐang tải dữ liệu...")
    comparison.load_data(file_path)
    print("Tải dữ liệu thành công!")
    print(f"Kích thước tập dữ liệu: {len(comparison.array_data)} bản ghi")
    print(f"Các trường dữ liệu: {', '.join(comparison.data_columns)}")
    
    while True:
        print("\nChọn thao tác:")
        print("1. Thêm mới")
        print("2. Cập nhật")
        print("3. Xóa")
        print("4. Tìm kiếm")
        print("5. Lưu cây B-tree")
        print("6. Tải cây B-tree")
        print("7. Xem danh sách cây đã lưu")
        print("8. Quay lại menu chính")
        
        try:
            choice = int(input("\nNhập lựa chọn của bạn (1-8): "))
            
            if choice == 8:
                break
                
            if choice not in [1, 2, 3, 4, 5, 6, 7]:
                print("Lựa chọn không hợp lệ!")
                continue

            if choice == 5:  # Save B-tree
                name = input("Nhập tên để lưu cây B-tree: ")
                try:
                    filename = comparison.save_btree(name)
                    print(f"Đã lưu cây B-tree vào file: {filename}")
                except Exception as e:
                    print(f"Lỗi khi lưu cây B-tree: {str(e)}")
                continue

            if choice == 6:  # Load B-tree
                name = input("Nhập tên file cây B-tree cần tải: ")
                try:
                    comparison.load_btree(name)
                    print("Đã tải cây B-tree thành công!")
                except FileNotFoundError as e:
                    print(str(e))
                except Exception as e:
                    print(f"Lỗi khi tải cây B-tree: {str(e)}")
                continue

            if choice == 7:  # List saved trees
                saved_trees = comparison.list_saved_trees()
                if not saved_trees:
                    print("Chưa có cây B-tree nào được lưu!")
                else:
                    print("\nDanh sách cây B-tree đã lưu:")
                    for i, tree in enumerate(saved_trees, 1):
                        print(f"{i}. {tree}")
                continue
            
            # Get key for operation
            key = int(input("Nhập khóa (số nguyên): "))
            
            if choice == 1:  # Insert
                # Generate new data with all fields
                value = comparison.generate_test_data(key)
                print("\nDữ liệu được tạo để thêm mới:")
                for field, val in value.items():
                    print(f"{field}: {val}")
                
                print("\nĐang thực hiện thêm mới...")
                start_time = time.perf_counter()
                comparison.array_insert(key, value)
                array_time = time.perf_counter() - start_time
                
                start_time = time.perf_counter()
                comparison.btree.insert(key, value)
                btree_time = time.perf_counter() - start_time
                
                results = {
                    "array_time": array_time,
                    "btree_time": btree_time,
                    "data": value
                }
                
                # Export results
                dataset_info = {
                    "file_path": file_path,
                    "size": len(comparison.array_data),
                    "fields": comparison.data_columns
                }
                result_file = exporter.export_direct_test_results(dataset_info, "insert", key, results)
                print(f"\nKết quả đã được xuất ra file: {result_file}")
                
                print("\nKết quả:")
                print(f"Thời gian thêm mới vào mảng: {array_time:.6f} giây")
                print(f"Thời gian thêm mới vào B-tree: {btree_time:.6f} giây")
                
            elif choice == 2:  # Update
                # Generate new data for update
                new_value = comparison.generate_test_data(key)
                new_value['updated'] = True
                print("\nDữ liệu được tạo để cập nhật:")
                for field, val in new_value.items():
                    print(f"{field}: {val}")
                
                print("\nĐang thực hiện cập nhật...")
                start_time = time.perf_counter()
                success_array = comparison.array_update(key, new_value)
                array_time = time.perf_counter() - start_time
                
                start_time = time.perf_counter()
                success_btree = comparison.btree.update(key, new_value)
                btree_time = time.perf_counter() - start_time
                
                results = {
                    "array_time": array_time,
                    "btree_time": btree_time,
                    "success_array": success_array,
                    "success_btree": success_btree,
                    "data": new_value
                }
                
                # Export results
                dataset_info = {
                    "file_path": file_path,
                    "size": len(comparison.array_data),
                    "fields": comparison.data_columns
                }
                result_file = exporter.export_direct_test_results(dataset_info, "update", key, results)
                print(f"\nKết quả đã được xuất ra file: {result_file}")
                
                print("\nKết quả:")
                print(f"Thời gian cập nhật mảng: {array_time:.6f} giây")
                print(f"Thời gian cập nhật B-tree: {btree_time:.6f} giây")
                print(f"Cập nhật mảng thành công: {success_array}")
                print(f"Cập nhật B-tree thành công: {success_btree}")
                
            elif choice == 3:  # Delete
                print("\nĐang thực hiện xóa...")
                start_time = time.perf_counter()
                success_array = comparison.array_delete(key)
                array_time = time.perf_counter() - start_time
                
                start_time = time.perf_counter()
                success_btree = comparison.btree.delete(key)
                btree_time = time.perf_counter() - start_time
                
                results = {
                    "array_time": array_time,
                    "btree_time": btree_time,
                    "success_array": success_array,
                    "success_btree": success_btree
                }
                
                # Export results
                dataset_info = {
                    "file_path": file_path,
                    "size": len(comparison.array_data),
                    "fields": comparison.data_columns
                }
                result_file = exporter.export_direct_test_results(dataset_info, "delete", key, results)
                print(f"\nKết quả đã được xuất ra file: {result_file}")
                
                print("\nKết quả:")
                print(f"Thời gian xóa trong mảng: {array_time:.6f} giây")
                print(f"Thời gian xóa trong B-tree: {btree_time:.6f} giây")
                print(f"Xóa trong mảng thành công: {success_array}")
                print(f"Xóa trong B-tree thành công: {success_btree}")
                
            elif choice == 4:  # Search
                print("\nĐang thực hiện tìm kiếm...")
                start_time = time.perf_counter()
                array_result = comparison.array_search(key)
                array_time = time.perf_counter() - start_time
                
                start_time = time.perf_counter()
                btree_result = comparison.btree.search(key)
                btree_time = time.perf_counter() - start_time
                
                results = {
                    "array_time": array_time,
                    "btree_time": btree_time,
                    "array_result": array_result,
                    "btree_result": btree_result
                }
                
                # Export results
                dataset_info = {
                    "file_path": file_path,
                    "size": len(comparison.array_data),
                    "fields": comparison.data_columns
                }
                result_file = exporter.export_direct_test_results(dataset_info, "search", key, results)
                print(f"\nKết quả đã được xuất ra file: {result_file}")
                
                print("\nKết quả:")
                print(f"Thời gian tìm kiếm trong mảng: {array_time:.6f} giây")
                print(f"Thời gian tìm kiếm trong B-tree: {btree_time:.6f} giây")
                
                if array_result:
                    print("\nTìm thấy trong mảng:")
                    for field, val in array_result.items():
                        print(f"{field}: {val}")
                else:
                    print("Không tìm thấy trong mảng")
                    
                if btree_result:
                    print("\nTìm thấy trong B-tree:")
                    for field, val in btree_result.items():
                        print(f"{field}: {val}")
                else:
                    print("Không tìm thấy trong B-tree")
                
        except ValueError:
            print("Vui lòng nhập số hợp lệ!")
        except Exception as e:
            print(f"Đã xảy ra lỗi: {str(e)}")

def main():
    while True:
        print("\n=== Công cụ So sánh Cấu trúc Dữ liệu ===")
        print("1. Chạy Kiểm tra Hiệu năng")
        print("2. Kiểm tra Trực tiếp")
        print("3. Thoát")
        
        try:
            choice = int(input("\nNhập lựa chọn của bạn (1-3): "))
            
            if choice == 1:
                # Select dataset
                file_path = select_dataset()
                
                # Get benchmark options
                concurrent, max_workers, operations = get_benchmark_options()
                
                # Run benchmark
                results = run_comparison(file_path, operations, concurrent, max_workers)
                
            elif choice == 2:
                direct_test()
                
            elif choice == 3:
                print("\nTạm biệt!")
                break
                
            else:
                print("Lựa chọn không hợp lệ!")
                
        except ValueError:
            print("Vui lòng nhập một số hợp lệ!")

if __name__ == "__main__":
    main()
