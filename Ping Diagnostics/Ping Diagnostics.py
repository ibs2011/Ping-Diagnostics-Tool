import subprocess
import platform
import os
import time

# Attempt to import Colour; fall back to standard text formatting if not found
try:
    from Colour import print_percentage_text
except ImportError:
    def print_percentage_text(text, percentage):
        print(text, end="")

def get_ping(host="1.1.1.1"):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    try:
        # cp1252 handles standard Windows console outputs securely
        response = subprocess.run(command, capture_output=True, text=True, encoding='cp1252', timeout=3)
        return response.stdout
    except subprocess.TimeoutExpired:
        return "Request timed out."

def make_inline_bar(percentage):
    percentage = max(0, min(100, percentage))
    val = percentage / 100.0
    if val < 0.5:
        red = int((val / 0.5) * 127)
        green = int(255 - (val / 0.5) * 128)
    else:
        red = int(127 + ((val - 0.5) / 0.5) * 3) 
        green = int(127 - ((val - 0.5) / 0.5) * 127)
    blue = 0
    bar_length = 15
    filled_length = int(bar_length * percentage // 100)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    return f"\033[38;2;{red};{green};{blue}m[{bar}]\033[0m"

def draw_header_box(iterations=None, total=300):
    """Helper function to keep header alignment completely identical across screens."""
    raw_header = "|-- P I N G        D I A G N O S T I C S --|"
    print(" " * 10 + " " + "_" * (len(raw_header) - 2))
    print(" " * 10 + f"\033[1m{raw_header}\033[0m")
    print(" " * 10 + "|" + "_" * (len(raw_header) - 2) + "|")
    print(" " * 15 + "\033[1;35mDeveloped by Ibrahim Khan • v1.0\033[0m")
    if iterations is not None:
        print(f"Diagnostics Run: {iterations} / {total}\n")
    else:
        print()

def update(host):
    host = host.strip()
    network = "Connecting..."
    pingSum = 0
    pingHighest = 0
    pingLowest = float("inf")
    latencySpikes = 0
    spikeSum = 0
    currLine = 0
    spikeLine = 0
    spikePrevLine = 0
    spikeSumInterval = 0
    furtherstSpikeCluster = 0
    lowestSpikeCluster = float('inf')
    data_loss = 0 
    a = 300
    
    for iterations in range(1, a + 1):
        # Clear screen and draw headers BEFORE waiting for the slow ping command
        os.system("cls" if platform.system().lower() == "windows" else "clear")
        draw_header_box(iterations, a)
        
        # Trigger the 1-second ping wait step safely
        raw_output = get_ping(host)
        lines = raw_output.splitlines()
        
        # Scan console output lines dynamically to locate core feedback data
        target_line = ""
        for l in lines:
            l_low = l.lower()
            if "reply from" in l_low or "timed out" in l_low or "unreachable" in l_low or "failure" in l_low:
                target_line = l
                break
        
        # Fallback tracking if line reads completely empty
        if not target_line:
            data_loss += 1
            is_dropped = True
            target_line = "Request timed out (Malformed system response)."
        else:
            if "timed out" in target_line.lower() or "unreachable" in target_line.lower() or "failure" in target_line.lower():
                data_loss += 1
                is_dropped = True
            else:    
                is_dropped = False
                currLine += 1
                parts = target_line.split()
                
                # Capture host address dynamically from active output text
                if len(parts) >= 3 and parts[0].lower() == "reply" and parts[1].lower() == "from":
                    network = parts[2].replace(":", "")
                
                # Locate the time data point dynamically rather than guessing position arrays
                time_part = next((p for p in parts if "time=" in p or "time<" in p), None)
                if time_part:
                    try:
                        if "<" in time_part:
                            ping = 1
                        else:
                            ping = int(time_part.split("=")[1].replace("ms", ""))

                        pingSum += ping

                        if ping > pingHighest:
                            pingHighest = ping

                        if ping < pingLowest:
                            pingLowest = ping

                        if ping > 100:
                            latencySpikes += 1
                            spikeSum += ping

                            spikePrevLine = spikeLine
                            spikeLine = currLine
                            
                            # CRASH FIX: Only calculate difference if there was a previous spike to compare against
                            if spikePrevLine > 0:
                                spikeDiff = (spikeLine - spikePrevLine)

                                if spikeDiff > furtherstSpikeCluster:
                                    furtherstSpikeCluster = spikeDiff

                                if spikeDiff < lowestSpikeCluster:
                                    lowestSpikeCluster = spikeDiff

                                spikeSumInterval += spikeDiff
                    except (IndexError, ValueError):
                        pass

        # Metrics math calculated securely using successful ping filters
        successful_pings = iterations - data_loss
        averagePing = pingSum / successful_pings if successful_pings > 0 else 0
        
        if latencySpikes > 0:
            averageSpike = spikeSum / latencySpikes
            # CRASH FIX: Only average intervals if we actually have intervals tracked
            spikeAverageInterval = spikeSumInterval / (latencySpikes - 1) if latencySpikes > 1 else 0
        else:
            averageSpike = 0
            spikeAverageInterval = 0

        data_loss_percentage = (data_loss / iterations) * 100
        spike_coverage_percentage = (latencySpikes / iterations) * 100

        max_ping_rating = (pingHighest / 300.0) * 100
        ping_rating = (ping / 300.0) * 100 if not is_dropped else 0
        avg_ping_rating = (averagePing / 100.0) * 100
        min_ping_rating = (0 if pingLowest == float("inf") else pingLowest / 50.0) * 100

        print(f"\033[1mIPV4: \033[34m{network}\033[0m\n")

        if is_dropped:
            print(f"Current Ping: {make_inline_bar(100)} \033[31mTIMEOUT\033[0m\n")
        else:
            print(f"Current Ping: {make_inline_bar(ping_rating)} ", end="")
            print_percentage_text(f"{ping}ms", ping_rating)
            print()
            
        print("-"*50)
        print(f"\033[34m\033[1mRaw Line: \033[0m")
        print(f"\033[1m{target_line}\033[0m")
        print("-"*50)
        
        print(f"Max Ping: {make_inline_bar(max_ping_rating)} ", end="")
        print_percentage_text(f"{pingHighest}ms", max_ping_rating)
        
        display_min = 0 if pingLowest == float("inf") else pingLowest
        print(f"Min Ping: {make_inline_bar(min_ping_rating)} ", end="")
        print_percentage_text(f"{display_min}ms", min_ping_rating)
        
        print(f"Data lost: {make_inline_bar(data_loss_percentage)} ", end="")
        print_percentage_text(f"{data_loss_percentage:.2f}%", data_loss_percentage)
        
        print(f"\nLatency Spikes Count (>100ms): \033[1m{latencySpikes}\033[0m")
        print(f"Latency Spikes Coverage (>100ms): {make_inline_bar(spike_coverage_percentage)} ", end="")
        print_percentage_text(f"{spike_coverage_percentage:.2f}%", spike_coverage_percentage)
        
        print(f"Latency Spike Average (>100ms): \033[1m{averageSpike:.2f}ms\033[0m")
        
        # CRASH FIX: Display safely as strings ONLY during final terminal printing
        show_interval = f"{spikeAverageInterval:.2f} check(s) / interval" if latencySpikes > 1 else "N/A"
        show_lowest = f"{lowestSpikeCluster} check(s)" if (latencySpikes > 1 and lowestSpikeCluster != float('inf')) else "N/A"
        show_furthest = f"{furtherstSpikeCluster} check(s)" if latencySpikes > 1 else "N/A"
        
        print(f"Latency Spike Interval Average: \033[1m{show_interval}\033[0m")
        print(f"Closest Spike Difference: \033[1m{show_lowest}\033[0m")
        print(f"Furthest Spike Difference: \033[1m{show_furthest}\033[0m")
        
        print(f"\nAverage Ping: {make_inline_bar(avg_ping_rating)} ", end="")
        print_percentage_text(f"{averagePing:.2f}ms", avg_ping_rating)
        
        print(f"Objects Counted: \033[1m{iterations}\033[0m")
        
        time.sleep(1)

# Runtime initialization block
if __name__ == "__main__":
    os.system("cls" if platform.system().lower() == "windows" else "clear")
    draw_header_box()
    user_host = input("Enter host address to test (e.g., 1.1.1.1 or google.com): ")
    if not user_host.strip():
        user_host = "1.1.1.1"
    update(user_host)
