
---

### **Settings: `MEDIA_URL` and `MEDIA_ROOT`**

```python
MEDIA_URL = '/media/'
```

- **Purpose**: Defines the base URL for accessing media files (like uploaded images). Files stored in the `MEDIA_ROOT` directory will be accessible via the `MEDIA_URL` endpoint.

In `urls.py`:

```python
urlpatterns = [
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- **Purpose**:
  - `static()` is used to serve media files during **development** (when `DEBUG=True`).
  - This allows uploaded media (e.g., post images) to be accessible via `/media/` while testing.
  - In production, you typically configure your web server (e.g., Nginx, Apache) to serve media files directly instead of relying on Django.

---

### **Validators**

In `validators.py`:

1. **Custom Validation Functions**:
   Each function ensures user-provided data adheres to specific rules.

   - **`validate_email(value)`**:
     Ensures the email does not end with `.mars` or `.jp`. Rejects emails from these "domains" with a validation error.

   - **`validate_username(value)`**:
     Ensures the username is at least 5 characters long. Raises an error otherwise.

   - **`validate_no_bad_words(value)`**:
     Prohibits certain words (`dog`, `cat`, `fish`, `popcorn`) in the provided value. Useful for filtering inappropriate or unwanted content.

   - **`validate_age(value)`**:
     Ensures the age is between 14 and 100, preventing very young or unrealistic ages.

   - **`validate_post_length(value)`**:
     Validates that a post’s content has a minimum length of 20 characters.

---

### **Models**

#### **`CustomUser` Model**

This is a custom user model that extends Django’s built-in `AbstractUser`. It inherits basic functionality (e.g., username, email, password handling) and adds additional fields and behavior.

1. **Fields**:
   - **`phone_number`**: Optional contact information for the user.
   - **`age`**: Enforces age validation via `validate_age`.
   - **`bio`**: Stores a user’s biography and is validated for bad words.
   - **`email`**: Enforces uniqueness and restricts certain domains using `validate_email`.
   - **`sex`**: Allows users to select a gender from predefined choices (`Male`, `Female`).

2. **Methods**:
   - **`__str__`**: Returns the username when the object is represented as a string.
   - **`save()`**:
     - Hashes the password if it hasn’t already been hashed.
     - Capitalizes the first and last names before saving.
   - **`clean()`**:
     - Performs additional validation on the username (e.g., minimum length) when the model is cleaned.

3. **Meta Class**:
   - Used to define **model-level metadata** such as database table names, default ordering, verbose names, etc.
   - **Attributes**:
     - `ordering = ['username', 'age']`: Default ordering of query results by `username` (ascending) and then by `age`.
     - `db_table = 'random_posts_users'`: Custom database table name.
     - `verbose_name` and `verbose_name_plural`: Specifies human-readable names for the model in the admin panel.

---

#### **`Post` Model**

Represents posts created by users, with content and optional images.

1. **Fields**:
   - **`user`**: A foreign key linking the post to a specific user (i.e., the post's author).
   - **`content`**: The body of the post, validated for bad words and minimum length.
   - **`categories`**: A string field that can categorize the post (validated for bad words).
   - **`visibility`**: A choice field that determines whether the post is public or private.
   - **`created_at`**: Stores the timestamp of when the post was created.
   - **`image`**: An optional image field that saves uploaded images in the `post_image/` directory.

2. **Methods**:
   - **`__str__`**:
     - Returns a readable description of the post, including the author's username and the creation timestamp.
   - **`save()`**:
     - Ensures uploaded images are resized to a maximum dimension of `300x300`. This helps optimize storage and loading times.

3. **Meta Class**:
   - **Attributes**:
     - `ordering = ['-created_at']`: Orders posts by creation date in descending order.
     - `db_table = 'posts'`: Specifies the database table name.
     - `verbose_name` and `verbose_name_plural`: User-friendly names for the model in the admin panel.

---

### **Meta Class in Django**

The **`Meta` class** is a nested class within a Django model that defines model-level options. These options control various behaviors, such as how the model interacts with the database or how it is displayed in the admin.

#### Common Meta Options:
1. **`db_table`**:
   - Specifies the name of the database table. If not provided, Django generates a name automatically (e.g., `appname_modelname`).

2. **`ordering`**:
   - Defines the default order of query results.
   - Example: `['-created_at']` orders by descending creation date.

3. **`verbose_name` / `verbose_name_plural`**:
   - Specifies human-readable names for the model in singular and plural forms.

4. **`unique_together`**:
   - Enforces uniqueness constraints across multiple fields.
   - Example: `unique_together = ('user', 'categories')` ensures no duplicate user-category pairs.

5. **`indexes`**:
   - Specifies database indexes to optimize query performance.
   - Example:
     ```python
     indexes = [
         models.Index(fields=['user', 'created_at']),
     ]
     ```

---

### Why Add the `MEDIA_URL` and Serve Static Media?

- **Purpose of `MEDIA_URL`**:
  - It is necessary to allow users to upload media files (e.g., profile pictures or post images).
  - Configuring `MEDIA_URL` and `MEDIA_ROOT` ensures the uploaded files are accessible during development.

- **Why Use `static()` in `urls.py`?**:
  - During development, Django does not serve media files automatically.
  - Adding `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` makes uploaded media accessible via `MEDIA_URL`.

---

This configuration ensures a robust setup for handling user authentication, validation, and content management in a Django application.