import os
import subprocess

subprocess.run(["allure", "generate", "./allure-results", "-o", "./allure-report", "--clean"])

if os.name == "posix":  # Для Unix-подобных систем
    subprocess.run(["xdg-open", "./allure-report/index.html"])
elif os.name == "nt":  # Для Windows
    subprocess.run(["allure", "serve"])
