### Step-by-Step Explanation

---

#### **1. Set up a Virtual Environment**
```bash
python3 -m venv venv
```
This creates a virtual environment named `venv`. Virtual environments isolate Python dependencies for a project, ensuring they don’t conflict with system-wide packages or other projects.

---

#### **2. Install Django**
```bash
pip install django
```
This installs Django into the virtual environment, allowing you to create and manage Django projects.

---

#### **3. Create a Django Project**
```bash
django-admin startproject random_posts
```
This creates a new Django project named `random_posts`. It includes default configurations like `settings.py`, `urls.py`, and other essential files.

---

#### **4. Create an App**
```bash
cd random_posts
django-admin startapp posts_app
```
An app (`posts_app`) is created within the project. Apps in Django are modular components, making it easier to scale and organize the project.

---

#### **5. Register the App in `settings.py`**
```python
INSTALLED_APPS = [
    ...
    "posts_app",
]
```
Django uses `INSTALLED_APPS` to identify the apps it should use. By adding `posts_app` here, Django includes it in the project for database migrations and other functionalities.

---

#### **6. Create the `CustomUser` Model**

**Code:**
```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
```
- **`AbstractUser`**: It provides Django's default user functionalities (username, email, password, etc.) but allows customization by adding new fields or modifying existing ones.
- **`timezone`**: Handles time zones for fields like `created_at`.

**Why Use `AbstractUser`?**
- It’s flexible: You can extend the default user model by adding custom fields like `bio` and `sex`.
- It avoids replacing the default user model entirely (`BaseUser`), which requires building all user-related features from scratch.

---

#### **Fields in `CustomUser`:**

1. **`SEX_CHOICES`**:
   ```python
   SEX_CHOICES = [("M", "Male"), ("F", "Female")]
   ```
   A tuple of options used in the `sex` field to enforce consistency (Male/Female).

2. **`phone_number`**:
   ```python
   phone_number = models.CharField(max_length=20, blank=True, null=True)
   ```
   Stores the user’s phone number. It is optional (`blank=True`, `null=True`).

3. **`age`**:
   ```python
   age = models.PositiveBigIntegerField(blank=True, null=True)
   ```
   Stores the user’s age. It’s a positive integer field allowing large values.

4. **`bio`**:
   ```python
   bio = models.TextField(blank=True)
   ```
   Allows users to add a personal biography. Optional (`blank=True`).

5. **`email`**:
   ```python
   email = models.EmailField(unique=True)
   ```
   Ensures every user has a unique email address, avoiding duplicates.

6. **`sex`**:
   ```python
   sex = models.CharField(choices=SEX_CHOICES, max_length=10)
   ```
   Restricts the value to predefined choices (`M` or `F`).

---

#### **7. Create the `Post` Model**

**Purpose**: Represents content created by users (e.g., social media posts).

**Fields:**

1. **`VISIBILITY_CHOICES`**:
   ```python
   VISIBILITY_CHOICES = [('public', 'Public'), ('private', 'Private')]
   ```
   Defines options for visibility. Posts can be visible to everyone or private.

2. **`user`**:
   ```python
   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_posts")
   ```
   - Establishes a relationship between `Post` and `CustomUser`.
   - If a user is deleted, all their posts are also deleted (`on_delete=models.CASCADE`).
   - The `related_name="user_posts"` allows accessing a user’s posts using `user.user_posts.all()`.

3. **`content`**:
   ```python
   content = models.TextField()
   ```
   Stores the main text content of the post.

4. **`categories`**:
   ```python
   categories = models.CharField(max_length=100)
   ```
   Allows categorization of posts (e.g., "Technology", "Lifestyle").

5. **`visibility`**:
   ```python
   visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
   ```
   Determines if the post is public or private.

6. **`created_at`**:
   ```python
   created_at = models.DateTimeField(default=timezone.now)
   ```
   Automatically records the date and time the post was created.

7. **`image`**:
   ```python
   image = models.ImageField(upload_to="post_image/", blank=True, null=True)
   ```
   - Allows users to upload an image for the post.
   - Images are stored in the `post_image/` directory under `MEDIA_ROOT`.

---

#### **8. Configure the Custom User Model**
```python
AUTH_USER_MODEL = 'posts_app.CustomUser'
MEDIA_URL = '/media/'
```
- `AUTH_USER_MODEL` tells Django to use `CustomUser` instead of the default `User` model.
- `MEDIA_URL` specifies the base URL for serving media files (like uploaded images).

---

#### **9. Migrations**
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
- **`makemigrations`**: Detects changes in models and creates migration files.
- **`migrate`**: Applies migrations to the database, creating the necessary tables.

---

#### **10. Register Models in `admin.py`**
```python
from django.contrib import admin
from .models import Post, CustomUser

admin.site.register(CustomUser)
admin.site.register(Post)
```
This allows you to manage `CustomUser` and `Post` models in the Django admin interface.

---

#### **11. Create Superuser**
```bash
python3 manage.py createsuperuser
```
This creates an admin user who can log into the admin site to manage users and posts.

---

#### **12. Run the Development Server**
```bash
python3 manage.py runserver
```
Starts the development server at `http://127.0.0.1:8000/`.

---

### Why Extend `AbstractUser`?

1. **Flexibility**:
   - Add fields like `phone_number`, `bio`, and `sex`.
   - Modify existing behavior while keeping built-in authentication.

2. **Reusability**:
   - Avoid recreating user-related features like login, password management, and permissions.

3. **Scalability**:
   - A clean, extensible base for future enhancements (e.g., more fields, methods).

---

#### **Django Admin**
Once you navigate to `http://127.0.0.1:8000/admin`, you can:
1. Create and manage users with custom fields (`CustomUser`).
2. Add posts linked to specific users (`Post`). 

This setup is highly customizable and suitable for real-world applications like blogs or social media platforms.

## **blank vs null**
In Django, `blank=True` and `null=True` are options used in model field definitions. Although they might seem similar, they have distinct purposes:

---

### 1. **`blank=True`**  
- **Purpose**: Controls whether a field is required in **forms**.
- **Effect**:
  - If `blank=True`, the field can be left empty when filling out forms in the Django admin or when using forms programmatically (e.g., `ModelForm`).
  - If `blank=False` (default), the field is required in forms.

---

### 2. **`null=True`**  
- **Purpose**: Determines if a database column can store `NULL` values.
- **Effect**:
  - If `null=True`, the database column for this field will allow `NULL` values.
  - If `null=False` (default), the field must have a value, and `NULL` is not allowed in the database.

---

### **Key Differences**

| Feature                  | `blank=True`                     | `null=True`                 |
|--------------------------|-----------------------------------|-----------------------------|
| **Use in Forms**         | Allows the field to be empty.    | Does not affect forms.      |
| **Use in Database**      | Does not affect the database.    | Allows storing `NULL`.      |
| **When to Use**          | Use when validating form input.  | Use for database constraints. |
| **Default Behavior**     | `blank=False` (field required).  | `null=False` (no `NULL`).   |

---

### **Examples**

#### **Scenario 1: `blank=True, null=True`**
```python
phone_number = models.CharField(max_length=15, blank=True, null=True)
```
- Forms: The `phone_number` field is optional.
- Database: If no value is provided, the database will store `NULL`.

#### **Scenario 2: `blank=True, null=False`**
```python
bio = models.TextField(blank=True, null=False)
```
- Forms: The `bio` field is optional.
- Database: If no value is provided, an empty string (`""`) is stored instead of `NULL`.

#### **Scenario 3: `blank=False, null=True`**
```python
age = models.PositiveIntegerField(blank=False, null=True)
```
- Forms: The `age` field is required.
- Database: If no value is provided, `NULL` is stored.

#### **Scenario 4: `blank=False, null=False`**
```python
username = models.CharField(max_length=150, blank=False, null=False)
```
- Forms: The `username` field is required.
- Database: The database does not allow `NULL` values.

---

### **Why Use Both?**

- Use **`blank=True`** when you want a field to be optional in forms.
- Use **`null=True`** when you want to allow the database to store `NULL` values.

---

### Example Use Cases

1. **String Fields (e.g., `CharField`, `TextField`)**:
   - Use `blank=True, null=False`.
   - Storing `""` (an empty string) is more common than `NULL` for text fields.
   - Example: A `bio` field left empty should store `""`, not `NULL`.

2. **Non-String Fields (e.g., `IntegerField`, `DateField`)**:
   - Use `blank=True, null=True`.
   - Storing `NULL` is more natural for non-string data types when the value is unknown or optional.

---

### Summary Rule of Thumb:
- **String fields**: Typically use `blank=True, null=False`.
- **Non-string fields**: Typically use `blank=True, null=True`.

By understanding when and where to apply these options, you can better handle form validation and database constraints in your Django models.