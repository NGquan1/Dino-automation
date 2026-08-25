import cv2
import numpy as np
import mss
import time
import pyautogui
import ctypes

from config import DEFAULT_SETTINGS, Region, Settings
from controller import Action, Controller, ObstacleType, Observation
from detector import detect_obstacle

# Fix lỗi DPI của Windows
try:
    ctypes.windll.user32.SetProcessDPIAware()
except Exception:
    pass

# ================================================
# TỌA ĐỘ BOX DƯỚI (MÀU ĐỎ) - Canh xương rồng và chim thấp -> NHẢY
# ================================================
def resize_to_show(img, max_width=1280, max_height=720):
    height, width = img.shape[:2]
    scale_w = max_width / width
    scale_h = max_height / height
    scale = min(scale_w, scale_h, 1)
    if scale < 1:
        return cv2.resize(img, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)
    return img

def is_obstacle_detected(frame_roi, threshold: int = DEFAULT_SETTINGS.detection_threshold):
    return detect_obstacle(frame_roi, threshold=threshold) is not None

def capture_bgr(sct, region: Region):
    screenshot = np.array(sct.grab(region.as_mss_monitor()))
    return cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)


def main(settings: Settings = DEFAULT_SETTINGS):
    if settings.debug_mode:
        print("DEBUG MODE ON: Display 2 detection boxes.")
    else:
        print("BOT IS RUNNING...")
        time.sleep(settings.startup_delay_seconds)

    with mss.mss() as sct:
        monitor_full = sct.monitors[1]
        last_action_time = 0
        controller = Controller()

        try:
            while True:
                if settings.debug_mode:
                    # --- CHẾ ĐỘ CĂN CHỈNH ---
                    img_grab = np.array(sct.grab(monitor_full))
                    frame = cv2.cvtColor(img_grab, cv2.COLOR_BGRA2BGR)
                    
                    # Vẽ Box Trên (Màu Xanh lá - BGR: 0, 255, 0)
                    top = settings.top_region
                    cv2.rectangle(frame, (top.left, top.top), (top.left + top.width, top.top + top.height), (0, 255, 0), 2)
                    
                    # Vẽ Box Dưới (Màu Đỏ - BGR: 0, 0, 255)
                    bottom = settings.bottom_region
                    cv2.rectangle(frame, (bottom.left, bottom.top), (bottom.left + bottom.width, bottom.top + bottom.height), (0, 0, 255), 2)
                    
                    frame_preview = resize_to_show(frame)
                    cv2.imshow("Dino Debug", frame_preview)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    # --- CHẾ ĐỘ CHẠY THẬT ---
                    current_time = time.monotonic()
                    
                    # Kiểm tra cooldown (tránh spam phím)
                    if current_time - last_action_time > settings.action_cooldown_seconds:
                        
                        # Ưu tiên 1: Quét chim bay ngang đầu trước
                        img_top = capture_bgr(sct, settings.top_region)
                        top_obstacle = detect_obstacle(img_top, settings.detection_threshold)
                        if top_obstacle is not None:
                            observation = Observation(ObstacleType.FLYING, int(top_obstacle.x))
                            action = controller.choose_action(observation)
                            if action == Action.DUCK:
                                print(">> Flying detected -> Dodge!")
                                pyautogui.keyDown("down")
                                try:
                                    time.sleep(settings.duck_duration_seconds)
                                finally:
                                    pyautogui.keyUp("down")
                                last_action_time = time.monotonic()
                                continue
                        
                        # Ưu tiên 2: Quét xương rồng/chim thấp
                        img_bottom = capture_bgr(sct, settings.bottom_region)
                        bottom_obstacle = detect_obstacle(img_bottom, settings.detection_threshold)
                        if bottom_obstacle is not None:
                            observation = Observation(ObstacleType.LOW, int(bottom_obstacle.x))
                            action = controller.choose_action(observation)
                            if action == Action.JUMP:
                                print(">> Obstacle detected -> Jump!")
                                pyautogui.press("space")
                                last_action_time = time.monotonic()

        except KeyboardInterrupt:
            print("\nBot stopped!")
            
        finally:
            pyautogui.keyUp("down")
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()