# users/managers.py
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, name, phone, password):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            name=name,
            phone=phone
        )

        user.set_password(password)  # 🔐 hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password):
        user = self.create_user(email, name, phone, password)

        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True

        user.save(using=self._db)
        return user