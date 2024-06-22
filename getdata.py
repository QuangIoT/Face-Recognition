import os
import cv2
import sqlite3


# Hàm thêm thông tin người dùng vào CSDL
def insert(id, cap, face_cascade, face_images_folder):
    conn = sqlite3.connect("detect person/FaceDataBase.db")
    
    # Kiểm tra xem id đã tồn tại trong CSDL chưa
    cursor = conn.execute("SELECT * FROM Person WHERE ID=?", (id,))
    isRecordExist = cursor.fetchone() is not None

    if not isRecordExist:
        # Nếu id chưa tồn tại, thêm mới
        name = input("Enter Name: ")
        query = "INSERT INTO Person(ID, Name) VALUES (?, ?)"
        conn.execute(query, (id, name))
        print("Them thong tin nguoi dung thanh cong.")
    else:
        print("ID da ton tai. Khong the them thong tin nguoi dung.")

    conn.commit()
    conn.close()

    # Nếu ID đã tồn tại, không thêm ảnh và thoát
    if isRecordExist:
        return

    sample_number = 0

    while sample_number < 20:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sample_number += 1

            # Lưu ảnh với định dạng: User.[id].[sample_number].jpg
            img_path = os.path.join(face_images_folder, f'User.{id}.{sample_number}.jpg')
            cv2.imwrite(img_path, img[y:y + h, x:x + w])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('img', img)
        cv2.waitKey(100)  # Delay 100 milliseconds between frames

    print("Qua trinh luu anh ket thuc.")
    cv2.destroyAllWindows()


# Hàm cập nhật thông tin của người dùng và lưu thêm hình ảnh khuôn mặt
def update(id, cap, face_cascade, face_images_folder):
    conn = sqlite3.connect("detect person/FaceDataBase.db")
    
    # Kiểm tra xem id đã tồn tại trong CSDL chưa
    cursor = conn.execute("SELECT * FROM Person WHERE ID=?", (id,))
    isRecordExist = cursor.fetchone() is not None

    if isRecordExist:
        # Nếu id chưa tồn tại, thêm mới
        name = input("Enter Name: ")
        query = "UPDATE Person SET Name=? WHERE ID=?"
        conn.execute(query, (id, name))
        print("Cap nhap thong tin nguoi dung thanh cong.")
    else:
        print("ID khong ton tai. Khong the cap nhap thong tin nguoi dung")

    conn.commit()
    conn.close()

    # Nếu ID đã tồn tại, không thêm ảnh và thoát
    if not isRecordExist:
        return

    sample_number = 0

    while sample_number < 20:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sample_number += 1

            # Lưu ảnh với định dạng: User.[id].[sample_number].jpg
            img_path = os.path.join(face_images_folder, f'User.{id}.{sample_number}.jpg')
            cv2.imwrite(img_path, img[y:y + h, x:x + w])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('img', img)
        cv2.waitKey(100)  # Delay 100 milliseconds between frames

    print("Quá trình lưu ảnh kết thúc.")
    cv2.destroyAllWindows()

# Hám xóa thông tin người dùng
def delete(id, face_images_folder):
    # Kết nối tới CSDL SQL
    conn = sqlite3.connect("detect person/FaceDataBase.db")
    cursor = conn.cursor() 

    # Kiểm tra xem ID có tồn tại trong CSDL SQL hay không
    cursor.execute("SELECT * FROM Person WHERE ID=?", (id,))
    user = cursor.fetchone() is not None

    if user:
        # Xóa thông tin người dùng khỏi CSDL SQL
        cursor.execute("DELETE FROM Person WHERE ID=?", (id,))
        conn.commit()
        conn.close()

        # Xóa các tệp tin ảnh liên quan
        for file in os.listdir(face_images_folder):
            if file.startswith(f'User.{id}.'):
                file_path = os.path.join(face_images_folder, file)
                os.remove(file_path)
        
        print(f"Da xoa thong tin nguoi dung voi ID {id} va cac anh lien quan.")
    else:
        print(f"Khong tim thay nguoi dung voi ID {id}.")
        return
    
# Hàm tìm kiến thông tin của người dùng
# def search(id, name):
#     # Kết nối tới CSDL SQL
#     conn = sqlite3.connect("detect person/FaceDataBase.db")
#     cursor = conn.cursor()

#     if id is not None:
#         # Tìm kiếm theo ID
#         id = input("Nhap ID")
#         cursor.execute("SELECT * FROM Person WHERE ID=?", (id,))
#     elif name is not None:
#         # Tìm kiếm theo tên
#         name = input("Nhap Name")
#         cursor.execute("SELECT * FROM Person WHERE Name=?", (name,))

#     result = cursor.fetchall()

#     if result:
#         print("Kết quả tìm kiếm:")
#         for row in result:
#             print(f"ID: {row[0]}, Name: {row[1]}")
#     else:
#         print("Không tìm thấy kết quả.")

#     conn.close()

    

# Khởi tạo bộ phát hiện khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Khởi tạo camera
cap = cv2.VideoCapture(0)

# Thư mục lưu trữ ảnh khuôn mặt
face_images_folder = 'detect person/data_face'

# Tạo thư mục lưu ảnh nếu chưa tồn tại
if not os.path.exists(face_images_folder):
    os.makedirs(face_images_folder)

# Gọi hàm menu để bắt đầu chương trình
while True:
    print("1. Them moi thong tin nguoi dung")
    print("2. Cap nhat thong tin nguoi dung")
    print("3. Xoa thong tin nguoi dung")
    print("4. Tìm kiem thong tin nguoi dung")
    print("0. Thoát")

    choice = input("Chon 1 lua chong (1/2/3): ")

    if choice == '1':
        print("Them moi thong tin nguoi dung")
        id = input('Nhap ID: ')
        insert(id, cap, face_cascade, face_images_folder)
        break

    elif choice == '2':
        print("Cap nhat thong tin nguoi dung")
        id = input('Nhap ID: ')
        update(id, cap, face_cascade, face_images_folder)
        break

    elif choice =='3':
        print("Xoa thong tin nguoi dung")
        id = input("Nhap ID: ")
        delete(id, face_images_folder)
        break

    # elif choice == '4':
    #     print ("Tìm kiếm thông tin người dùng")
    
    #     search()
    #     break

    elif choice == '0':
        print("Ket thuc")
        break

    else:
        print("Lua chon ko hop le. Vui chon cai khac.")

