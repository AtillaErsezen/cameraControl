import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from threading import Thread
from queue import Queue
from PIL import Image, ImageTk
import time

class HandGestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.screen_w, self.screen_h = pyautogui.size()
        self.running = False
        self.gesture_actions = {
            'click': 'fist',
            'right_click': 'peace',
            'double_click': 'three_fingers',
            'scroll_up': 'thumb_up',
            'scroll_down': 'thumb_down'
        }
        self.last_click_time = 0

    def detect_gesture(self, landmarks):
        thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP]

        # Fist detection
        if all(tip.y > landmarks[self.mp_hands.HandLandmark.THUMB_MCP].y 
               for tip in [index_tip, middle_tip, ring_tip, pinky_tip]):
            return 'fist'
        
        # Peace sign detection
        if index_tip.y < middle_tip.y and ring_tip.y > middle_tip.y and pinky_tip.y > middle_tip.y:
            return 'peace'
        
        # Three fingers detection
        if index_tip.y < middle_tip.y and middle_tip.y < ring_tip.y and pinky_tip.y > ring_tip.y:
            return 'three_fingers'
        
        # Thumb gestures
        thumb_up = thumb_tip.y < landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y
        thumb_down = thumb_tip.y > landmarks[self.mp_hands.HandLandmark.PINKY_TIP].y
        if thumb_up: return 'thumb_up'
        if thumb_down: return 'thumb_down'
        
        return 'none'

    def run(self, queue):
        self.running = True
        while self.running:
            success, img = self.cap.read()
            if not success:
                continue

            img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
            results = self.hands.process(img)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks = hand_landmarks.landmark
                    gesture = self.detect_gesture(landmarks)
                    
                    # Mouse movement
                    index_x = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                    index_y = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                    screen_x = int(index_x * self.screen_w)
                    screen_y = int(index_y * self.screen_h)
                    pyautogui.moveTo(screen_x, screen_y, duration=0.1)
                    
                    # Action handling
                    current_time = time.time()
                    for action, trigger_gesture in self.gesture_actions.items():
                        if gesture == trigger_gesture:
                            if action == 'click':
                                pyautogui.click()
                                self.last_click_time = current_time
                            elif action == 'right_click':
                                pyautogui.rightClick()
                            elif action == 'double_click' and (current_time - self.last_click_time) < 0.5:
                                pyautogui.doubleClick()
                            elif action == 'scroll_up':
                                pyautogui.scroll(100)
                            elif action == 'scroll_down':
                                pyautogui.scroll(-100)
                            break

            queue.put(img)
        self.cap.release()

class App:
    def __init__(self, root):
        self.root = root
        self.controller = HandGestureController()
        self.queue = Queue()
        
        self.setup_ui()
        self.update()
        
    def setup_ui(self):
        self.root.title("Hand Gesture Mouse Controller")
        
        # Video feed
        self.video_label = tk.Label(self.root)
        self.video_label.pack()
        
        # Control buttons
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(self.btn_frame, text="Start", command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(self.btn_frame, text="Stop", command=self.stop)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Gesture mapping
        self.gesture_frame = tk.Frame(self.root)
        self.gesture_frame.pack(pady=10)
        
        self.action_vars = {}
        for i, (action, gesture) in enumerate(self.controller.gesture_actions.items()):
            label = tk.Label(self.gesture_frame, text=f"{action.replace('_', ' ').title()}:")
            label.grid(row=i, column=0, padx=5, pady=2)
            
            var = tk.StringVar(value=gesture)
            self.action_vars[action] = var
            
            dropdown = tk.OptionMenu(self.gesture_frame, var, 
                                   'fist', 'peace', 'three_fingers', 
                                   'thumb_up', 'thumb_down')
            dropdown.grid(row=i, column=1, padx=5, pady=2)

    def start(self):
        if not self.controller.running:
            self.controller.gesture_actions = {
                action: var.get() 
                for action, var in self.action_vars.items()
            }
            self.thread = Thread(target=self.controller.run, args=(self.queue,))
            self.thread.start()

    def stop(self):
        self.controller.running = False

    def update(self):
        while not self.queue.empty():
            img = self.queue.get()
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img = cv2.resize(img, (640, 480))
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.root.after(10, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()