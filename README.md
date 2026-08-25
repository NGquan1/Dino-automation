# Chrome Dino Automation QA Bot

Python bot tự động chơi Chrome Dino bằng `mss`, OpenCV và PyAutoGUI. Project được tổ chức theo hướng Automation QA: tách detector, controller và test độc lập.

## Cấu trúc

```text
main.py          # Vòng lặp capture và gửi phím
detector.py      # Phát hiện obstacle bằng contour
controller.py    # Quyết định jump/duck
config.py        # Cấu hình vùng quét
tests/            # Unit tests
```

## Cài đặt

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Chạy bot

1. Mở Chrome và vào `chrome://dino`.
2. Căn vị trí game theo các vùng trong `config.py`.
3. Chạy:

```powershell
python main.py
```

Dừng bot bằng `Ctrl+C`.

Để căn vùng quét, đổi `debug_mode` thành `True` trong `config.py`, chạy lại bot và nhấn `q` để thoát.

## Chạy test

```powershell
python -m pytest -q
```

Test chạy không cần mở Chrome, bao gồm detector, bounding box, lọc nhiễu và logic jump/duck.

## Lưu ý

Bot hiện dành cho Windows và dùng tọa độ màn hình cố định. Vui lòng không upload thư mục `venv/` lên Git.
