### **What is Logging in Django?**

**Logging** in Django is the process of tracking events that happen when the Django application is running. It allows developers to monitor, debug, and understand the behavior of their application by recording information about requests, errors, warnings, or other significant events.

Django's logging system is built on Python's built-in **`logging`** module, providing a flexible and robust framework for logging messages and managing logs.

---

### **Why Do We Need Logging?**

1. **Debugging**: Logs help in diagnosing issues by recording errors, exceptions, and unusual behavior in the application.
2. **Monitoring**: Logs allow developers or system administrators to monitor the performance and health of an application.
3. **Error Tracking**: Log files capture critical errors, enabling quick identification and resolution of issues.
4. **Auditing**: Logs can be used to track user actions, requests, or security events for compliance or analysis.
5. **Performance Optimization**: By analyzing logs, developers can identify bottlenecks and improve application performance.

---

### **How Logging Works in Django**

Django's logging system consists of **loggers**, **handlers**, and **formatters**.

1. **Logger**: The entry point for logging messages. It determines which log messages are processed based on the log level.
2. **Handler**: Defines where the log messages are sent (e.g., console, file, email).
3. **Formatter**: Specifies the layout and structure of the log message (e.g., timestamp, log level, message).
4. **Log Level**: Determines the severity of a log message. Messages below the configured level are ignored.

---

### **Log Levels in Django**

Django uses the following standard log levels, in increasing order of severity:

| Log Level | Numeric Value | Purpose                                      |
|-----------|---------------|----------------------------------------------|
| `DEBUG`   | 10            | Detailed information for diagnosing problems.|
| `INFO`    | 20            | General information about the application's flow. |
| `WARNING` | 30            | Indicates a potential problem or unusual behavior.|
| `ERROR`   | 40            | Records serious errors that need attention. |
| `CRITICAL`| 50            | Very severe errors that may prevent the application from running. |

---


---

### **1. LOGGING Configuration in `settings.py`**

The `LOGGING` dictionary sets up logging behavior in Django project.

#### **1.1 Basic Structure**

```python
LOGGING = {
    "version": 1,
    'disable_existing_loggers': False,
```
- **`"version": 1`**: This specifies the logging configuration version. Always set it to `1` for Django projects.
- **`'disable_existing_loggers': False`**: Ensures existing loggers (including Django’s default loggers) are not disabled. If set to `True`, it would ignore existing loggers.

---

#### **1.2 Formatters**

Formatters define how log messages are displayed.

```python
"formatters": {
    "verbose": {
        'format': '{levelname} {asctime} {module} {message}',
        'style': '{',
    },
    "simple": {
        'format': '{asctime} {levelname} {message}',
        'style': '{',
    }
},
```
- **`verbose`**:
  - Displays detailed log information.
  - **`format`**: Specifies the log message format.
    - **`{levelname}`**: Logging level (e.g., INFO, WARNING, ERROR).
    - **`{asctime}`**: Timestamp of when the log was recorded.
    - **`{module}`**: The Python module where the log was triggered.
    - **`{message}`**: The actual log message.
  - **`style: '{'`**: Uses the `{}` format style for log messages.

- **`simple`**:
  - A simpler log format without module details.
  - Includes timestamp, log level, and message.

---

#### **1.3 Handlers**

Handlers determine where log messages are sent (e.g., console, file).

```python
'handlers': {
    'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'simple',
    },
    'file': {
        'class': 'logging.FileHandler',
        'filename': os.path.join(BASE_DIR, 'info_log', 'info.log'),
        'formatter': 'verbose',
    },
    'file_app': {
        'class': 'logging.FileHandler',
        'filename': os.path.join(BASE_DIR, 'info_log', 'info_app.log'),
        'formatter': 'verbose',
    },
},
```

- **`console`**:
  - Sends log messages to the console (terminal).
  - Uses the **`simple`** formatter.

- **`file`**:
  - Writes logs to a file named `info.log` in the `info_log` directory.
  - Uses the **`verbose`** formatter.

- **`file_app`**:
  - Writes logs to a separate file, `info_app.log`, specifically for the `posts_app` logger.
  - Also uses the **`verbose`** formatter.

---

#### **1.4 Loggers**

Loggers define which messages are handled and where they are sent.

```python
"loggers": {
    "django": {
        "handlers": ["console", "file"],
        "level": "INFO",
        "propagate": True
    },
    "posts_app": {
        "handlers": ["console", "file_app"],
        "level": "INFO",
        "propagate": True
    }
}
```

- **`"django"` Logger**:
  - **`handlers`: ["console", "file"]**: Sends log messages to both the console and the `info.log` file.
  - **`level`: "INFO"`**: Logs all messages at **INFO** level or higher (INFO, WARNING, ERROR, CRITICAL).
  - **`propagate: True`**: Allows log messages to propagate to higher-level loggers (like the root logger).

- **`"posts_app"` Logger**:
  - This is a custom logger specific to your `posts_app` application.
  - **`handlers`: ["console", "file_app"]**: Sends log messages to the console and the `info_app.log` file.
  - **`level`: "INFO"`**: Logs messages at INFO level or higher.
  - **`propagate: True`**: If set to `False`, messages will **not** propagate to the root logger.

---

### **2. Logger in the Views**

The `logger` instance in your views is configured to use the **`posts_app` logger** defined in the `LOGGING` settings.

```python
logger = logging.getLogger("posts_app")
```
- **`logging.getLogger("posts_app")`**: This retrieves the logger named `"posts_app"` from the logging configuration.
- Since `"posts_app"` has **INFO** level and two handlers (`console` and `file_app`), messages logged here will:
  1. Print to the console.
  2. Write to the file `info_app.log` in the `info_log` directory.

---

### **3. Log Messages in Views**

Let’s analyze how the logger works in each view.

---

#### **3.1 HomePageView**

```python
logger.info(f"The home page is visited by {request.user}")
```
- When a user visits the home page:
  - The logger logs an **INFO** level message.
  - Example message in `info_app.log`:
    ```
    INFO 2024-06-17 10:30:00 views The home page is visited by user123
    ```
- This message will also appear in the console due to the `console` handler.

---

#### **3.2 UserRegisterView**

```python
logger.info(f"total users {CustomUser.objects.count()}")
```
- When a new user registers:
  - The logger logs the current count of total users.
  - Example message:
    ```
    INFO 2024-06-17 10:32:15 views total users 10
    ```

---

#### **3.3 UserLoginView**

```python
logger.info(f"{user.username} logged in")
```
- When a user successfully logs in:
  - The logger logs an **INFO** message with the username.
  - Example:
    ```
    INFO 2024-06-17 10:35:00 views user123 logged in
    ```

---

#### **3.4 UserLogoutView**

```python
logger.warning(f"{request.user.username} logged out")
```
- When a user logs out:
  - The logger logs a **WARNING** level message.
  - Example:
    ```
    WARNING 2024-06-17 10:40:00 views user123 logged out
    ```
- **Why WARNING?**:
  - Logging a logout as a warning might be intentional to highlight user sign-outs.

---

### **4. Summary**

- **Loggers**:  
  - `"posts_app"` is a custom logger that logs messages to the console and the `info_app.log` file.
  - Messages with level **INFO** or higher are logged.

- **Handlers**:
  - Console: Displays logs in the terminal.
  - File: Saves logs to `info_app.log` for the `posts_app` logger.

- **Views**:
  - `logger.info` and `logger.warning` are used to log important events (visits, logins, logouts, etc.).

- **Benefit**:
  - By having a custom logger for `posts_app`, you can isolate logs related to this app for easier debugging and monitoring.