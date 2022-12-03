1. Tách ra thành các file với các chức năng
    main: Luồng chơi chính
    rules: Luật chơi 
    UI: Giao diện
    AI: Trí tuệ nhân tạo
2. Thay vì dùng turn là Boolean(true,false) thì đổi sang 'w' or 'b'
3. Thống nhất gọi tọa độ (hàng,cột) theo ma trận 2 chiều tương tự chess_state, trừ khi dùng hàm đồ họa 
4. Tối ưu hóa và đơn giản hóa các hàm
5. Đánh giá tổng giá trị bàn cờ thông qua giá trị của quân cờ + giá trị quân cờ tại vị trí hiện tại của nó

#Bug:
1. Sau khi undo bước nhập thành thì k nhập thành 