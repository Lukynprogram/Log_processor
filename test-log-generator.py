import random

base_timestamp = 1157689312.049  # Starting timestamp
time_increment = 0.018727  # Time increment per event
log_lines = []

for i in range(100):
    timestamp = base_timestamp + i * time_increment
    response_header_size = random.randint(1000, 6000)
    client_ip = f"10.105.{random.randint(20, 50)}.{random.randint(100, 255)}"
    http_response = f"TCP_MISS/{random.choice([200, 302, 304])}"
    response_size = random.randint(500, 20000)
    http_method = random.choice(["GET", "POST", "CONNECT"])
    url = f"http://{random.choice(['www.example.com', 'login.yahoo.com', 'www.goonernews.com', 'www.google.com'])}/"
    username = random.choice(["-", "badeyek", "adeolaegbedokun"])
    access_type = f"DIRECT/{random.randint(60, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    response_type = random.choice(["text/html", "image/jpeg", "image/gif", "-"])

    log_line = f"{timestamp:.3f}\t{response_header_size}\t{client_ip}\t{http_response}\t{response_size}\t{http_method}\t{url}\t{username}\t{access_type}\t{response_type}"
    log_lines.append(log_line)

log_output = "\n".join(log_lines)
print(log_output)
