# TODO: Implement Admin Pages for Administrador Role


## Step 2: Add Category CRUD Views
- Add CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView to activos/views.py
- Ensure Admin permissions

## Step 3: Add URLs
- Add Category CRUD URLs to activos/urls.py
- Add user management URLs (user_list, user_create, user_update, user_reset_password) to activos/urls.py

## Step 4: Create Category Templates
- Create category_list.html, category_form.html, category_confirm_delete.html in activos/templates/activos/

## Step 5: Create User Management Templates
- Create user_list.html, user_form.html, reset_password.html in usuarios/templates/usuarios/

## Step 6: Update Admin Dashboard
- Update admin_dashboard.html with proper links to all features (assets, categories, locations, users, movements, reports)

## Step 7: Add Missing Report Views
- Add more export options if needed (e.g., CSV, more reports)

## Step 8: Update Navigation
- Ensure base.html has links for admin features

## Step 9: Test and Verify
- Run server, test login as Admin, check all links and permissions
