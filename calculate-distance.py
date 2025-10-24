import time
import random

# شبیه‌ساز GPIO
class FakeGPIO:
    BCM = "BCM"
    OUT = "OUT"
    IN = "IN"

    def init(self):
        self.mode = None
        self.pins = {}

    def setmode(self, mode):
        self.mode = mode

    def setup(self, pin, mode):
        self.pins[pin] = mode

    def output(self, pin, value):
        if pin in self.pins and self.pins[pin] == self.OUT:
            print(f"Pin {pin} set to {value}")

    def input(self, pin):
        if pin in self.pins and self.pins[pin] == self.IN:
            # شبیه‌سازی دریافت پالس (به صورت تصادفی)
            return random.choice([0, 1])
        return 0

    def cleanup(self):
        print("GPIO cleaned up")

# استفاده از شبیه‌ساز
GPIO = FakeGPIO()

# تنظیمات پایه‌ها
TRIG = 23  # پایه Trigger
ECHO = 24  # پایه Echo

# تنظیمات GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        # ارسال پالس
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # شبیه‌سازی زمان دریافت پالس
        pulse_start = time.time()
        time.sleep(0.01)  # شبیه‌سازی زمان انتظار برای پالس
        pulse_end = time.time()

        # محاسبه فاصله
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # تبدیل زمان به فاصله (سانتی‌متر)
        distance = round(distance, 2)

        # نمایش فاصله
        print(f"Distance: {distance} cm")

        # تأخیر قبل از اندازه‌گیری بعدی
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()