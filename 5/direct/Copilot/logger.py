def log_error(message: str):
    with open("error_log.txt", mode="a", encoding="utf-8") as log_file:
        log_file.write(message + '\n')