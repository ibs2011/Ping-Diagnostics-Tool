import sys

def print_percentage_text(text, percentage):
    # 1. Clamp the percentage between 0 and 100 to prevent errors
    percentage = max(0, min(100, percentage))
    
    val = percentage / 100.0

    if val < 0.5:
        red = int((val / 0.5) * 127)
        green = int(255 - (val / 0.5) * 128)
    else:
        red = int(127 + ((val - 0.5) / 0.5) * 3) 
        green = int(127 - ((val - 0.5) / 0.5) * 127)
        
    blue = 0
    print(f"\033[38;2;{red};{green};{blue}m{text}\033[0m")


def draw_progress_bar(percentage):
    percentage = max(0, min(100, percentage))
    val = percentage / 100.0
    
    if val < 0.5:
        red = int((val / 0.5) * 127)
        green = int(255 - (val / 0.5) * 128)
    else:
        red = int(127 + ((val - 0.5) / 0.5) * 3) 
        green = int(127 - ((val - 0.5) / 0.5) * 127)
    blue = 0

    bar_length = 20
    filled_length = int(bar_length * percentage // 100)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    sys.stdout.write(f"\r\033[K\033[38;2;{red};{green};{blue}m[{bar}] {percentage}%\033[0m")
    sys.stdout.flush()