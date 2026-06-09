# =============================================================
#  HỆ THỐNG QUẢN LÝ KHO MÁU RIKKEI HOSPITAL
#  Blood Bank Management System
# =============================================================
# Lưu ý kỹ thuật: Dùng ký tự "|" làm phân cách thay vì "-"
# vì nhóm máu âm (A-, B-, O-, AB-) chứa ký tự "-", nếu dùng
# "-" làm phân cách sẽ gây lỗi khi split().

# Dữ liệu khởi tạo mẫu (List of Strings, phân cách bằng "|")
blood_inventory = [
    "BL001|Nguyen Van A|O+|250|31/12/2026",
    "BL002|Tran Thi B|A-|350|15/11/2026",
    "BL003|Le Van C|AB+|250|20/10/2026"
]


# -------------------------------------------------------------
# HELPER FUNCTION
# -------------------------------------------------------------

def find_bag_index(inventory, bag_id):
    """Tìm index của túi máu theo mã. Trả về index hoặc -1."""
    bag_id = bag_id.strip().upper()
    for i in range(len(inventory)):
        parts = inventory[i].split("|")
        if parts[0] == bag_id:
            return i
    return -1


# -------------------------------------------------------------
# CHỨC NĂNG 1: XEM DANH SÁCH TÚI MÁU TRONG KHO
# -------------------------------------------------------------

def display_inventory(inventory):
    """In bảng toàn bộ kho máu và tổng thể tích hiện có."""
    if len(inventory) == 0:
        print("Kho máu hiện chưa có túi máu nào.")
        return

    print("--- DANH SÁCH KHO MÁU ---")
    print(f"{'Mã Túi':<7}| {'Người Hiến':<17}| {'Nhóm Máu':<9}| {'Thể Tích':<9}| Ngày Hết Hạn")
    print("-" * 62)

    tong_the_tich = 0
    for record in inventory:
        parts       = record.split("|")
        ma          = parts[0]
        ten         = parts[1]
        nhom_mau    = parts[2]
        the_tich    = int(parts[3])
        han_su_dung = parts[4]
        tong_the_tich += the_tich
        print(f"{ma:<7}| {ten:<17}| {nhom_mau:<9}| {the_tich} ml   | {han_su_dung}")

    print("-" * 62)
    print(f"Tổng thể tích máu trong kho: {tong_the_tich} ml.")


# -------------------------------------------------------------
# CHỨC NĂNG 2: NHẬP TÚI MÁU MỚI
# -------------------------------------------------------------

def add_blood_bag(inventory):
    """Nhập túi máu mới, chuẩn hóa dữ liệu và lưu vào kho."""
    print("--- NHẬP TÚI MÁU MỚI ---")

    # Nhập và kiểm tra mã túi máu
    ma_tui = input("Nhập mã túi máu mới: ").strip().upper()
    if len(ma_tui) == 0:
        print("Lỗi: Mã túi máu không được để trống!")
        return
    if find_bag_index(inventory, ma_tui) != -1:
        print(f"Lỗi: Mã túi máu {ma_tui} đã tồn tại! Vui lòng nhập mã khác.")
        return

    # Nhập và kiểm tra tên người hiến
    ten = input("Nhập tên người hiến: ").strip().title()
    if len(ten) == 0:
        print("Lỗi: Tên người hiến không được để trống!")
        return

    # Nhập nhóm máu
    nhom_mau = input("Nhập nhóm máu: ").strip().upper()
    if len(nhom_mau) == 0:
        print("Lỗi: Nhóm máu không được để trống!")
        return

    # Nhập và kiểm tra thể tích
    the_tich_raw = input("Nhập thể tích (ml): ").strip()
    if not the_tich_raw.isdigit() or int(the_tich_raw) <= 0:
        print("Lỗi: Thể tích phải là số nguyên lớn hơn 0!")
        return

    # Nhập ngày hết hạn
    han_su_dung = input("Nhập ngày hết hạn (DD/MM/YYYY): ").strip()
    if len(han_su_dung) == 0:
        print("Lỗi: Ngày hết hạn không được để trống!")
        return

    # Ghép chuỗi bằng join() và thêm vào kho
    new_record = "|".join([ma_tui, ten, nhom_mau, the_tich_raw, han_su_dung])
    inventory.append(new_record)
    print(f"Thành công: Đã nhập túi máu {ma_tui} vào kho!")
    print("Sau khi chuẩn hóa, dữ liệu được lưu vào list là:")
    print(new_record)


# -------------------------------------------------------------
# CHỨC NĂNG 3: GIA HẠN / SỬA NGÀY HẾT HẠN
# -------------------------------------------------------------

def update_expiry(inventory):
    """Cập nhật ngày hết hạn của túi máu theo mã."""
    print("--- GIA HẠN / SỬA NGÀY HẾT HẠN ---")

    # Nhập và kiểm tra mã túi máu
    ma_tui = input("Nhập mã túi máu cần cập nhật: ").strip().upper()
    if len(ma_tui) == 0:
        print("Lỗi: Mã túi máu không được để trống!")
        return

    index = find_bag_index(inventory, ma_tui)
    if index == -1:
        print(f"Lỗi: Không tìm thấy túi máu {ma_tui} trong kho!")
        return

    # Nhập ngày hết hạn mới
    han_moi = input("Nhập ngày hết hạn mới: ").strip()
    if len(han_moi) == 0:
        print("Lỗi: Ngày hết hạn không được để trống!")
        return

    # Tách → sửa index 4 → ghép lại → gán đè (String Immutable)
    parts    = inventory[index].split("|")
    parts[4] = han_moi
    inventory[index] = "|".join(parts)
    print(f"Thành công: Đã cập nhật ngày hết hạn cho túi máu {ma_tui}!")


# -------------------------------------------------------------
# CHỨC NĂNG 4: XUẤT / HỦY TÚI MÁU
# -------------------------------------------------------------

def remove_blood_bag(inventory):
    """Xuất hoặc hủy túi máu khỏi kho theo mã."""
    print("--- XUẤT / HỦY TÚI MÁU ---")

    # Nhập và kiểm tra mã túi máu
    ma_tui = input("Nhập mã túi máu cần xuất/hủy: ").strip().upper()
    if len(ma_tui) == 0:
        print("Lỗi: Mã túi máu không được để trống!")
        return

    index = find_bag_index(inventory, ma_tui)
    if index == -1:
        print(f"Lỗi: Không tìm thấy túi máu {ma_tui} trong kho!")
        return

    inventory.pop(index)
    print(f"Thành công: Đã xuất túi máu {ma_tui} khỏi kho!")


# -------------------------------------------------------------
# MAIN — VÒNG LẶP CHÍNH
# -------------------------------------------------------------

def main():
    """Hàm chính: hiển thị menu và điều hướng đến các chức năng."""
    while True:
        print("\n=== HỆ THỐNG QUẢN LÝ KHO MÁU RIKKEI ===")
        print("1. Xem danh sách túi máu trong kho")
        print("2. Nhập túi máu mới")
        print("3. Gia hạn / Sửa ngày hết hạn")
        print("4. Xuất / Hủy túi máu")
        print("5. Thoát chương trình")
        print("========================================")

        lua_chon = input("Chọn chức năng (1-5): ").strip()

        if lua_chon == "1":
            display_inventory(blood_inventory)
        elif lua_chon == "2":
            add_blood_bag(blood_inventory)
        elif lua_chon == "3":
            update_expiry(blood_inventory)
        elif lua_chon == "4":
            remove_blood_bag(blood_inventory)
        elif lua_chon == "5":
            print("Cảm ơn bác sĩ đã sử dụng hệ thống. Hẹn gặp lại!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng nhập số từ 1-5!")


main()