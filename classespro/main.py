import hashlib
import uuid

class User:
    """
    Базовый класс, представляющий пользователя.
    """
    users = []

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = self.hash_password(password)
        self.session_token = None
        User.users.append(self)

    @staticmethod
    def hash_password(password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
    @staticmethod
    def check_password(stored_password, provided_password):
        password_hash, salt = stored_password.split(':')
        new_hash = hashlib.sha256(salt.encode() + provided_password.encode()).hexdigest()
        return password_hash == new_hash

    def get_details(self):
        return f"Пользователь: {self.username}, Email: {self.email}"

class Customer(User):
    """
    Класс, представляющий клиента, наследующий класс User.
    """
    def __init__(self, username, email, password, address):
        super().__init__(username, email, password)
        self.address = address

    def get_details(self):
        return f"Покупатель: {self.username}, Email: {self.email}, Адрес: {self.address}"

class Admin(User):
    """
    Класс, представляющий администратора, наследующий класс User.
    """
    def __init__(self, username, email, password, admin_level):
        super().__init__(username, email, password)
        self.admin_level = admin_level

    def get_details(self):
        return f"Admin: {self.username}, Email: {self.email}, Admin-Level: {self.admin_level}"

    @staticmethod
    def list_users():
        """
        Выводит список всех пользователей.
        """
        return [user.get_details() for user in User.users]    

    @staticmethod
    def delete_user(username):
        """
        Удаляет пользователя по имени пользователя.
        """
        for i, user in enumerate(User.users):
            if user.username == username:
                del User.users[i]
                return True
        return False

class AuthenticationService:
    """
    Сервис для управления регистрацией и аутентификацией пользователей.
    """
    def __init__(self):
        self.current_user = None

    def register(self, user_class, username, email, password, *args):
        """
        Регистрация нового пользователя.
        Проверяет уникальность имени пользователя и email.
        """
        for user in User.users:
            if user.username == username or user.email == email:
                return {"status": "error", "message": "Пользователь с указанным именем и/или e-mail уже зарегистрирован"}
        
        new_user = user_class(username, email, password, *args)
        return {"status": "success", "message": f"Пользователь: {new_user.get_details()} успешно зарегистрирован"}

    def login(self, username, password):
        """
        Аутентификация пользователя.
        Проверяет пароль и создает токен сессии.
        """
        for user in User.users:
            if user.username == username:
                if User.check_password(user.password_hash, password):
                    # Генерация токена сессии
                    user.session_token = uuid.uuid4().hex
                    self.current_user = user
                    return {"status": "success", "message": "Вход в систему успешно произведён", "session_token": user.session_token}
                else:
                    return {"status": "error", "message": "Неверные имя и/или пароль"}  # Собщения при несовпадении пароля
        return {"status": "error", "message": "Неверные имя и/или пароль"}              # или имени должны быть одинаковыми, чтобы исключить подбор пароля

    def logout(self):
        """
        Выход пользователя из системы.
        """
        if self.current_user:
            self.current_user.session_token = None
            self.current_user = None
            return {"status": "success", "message": "Выход успешно выполнен"}
        return {"status": "error", "message": "Системная ошибка"} # Такого не должно происходить или следует проглотить данную ошибку

    def get_current_user(self):
        """
        Возвращает текущего вошедшего пользователя.
        """
        if self.current_user:
            return {"status": "success", "user": self.current_user.get_details()}
        return {"status": "error", "message": "Нет активного пользователя"}

if __name__ == "__main__":
    auth_service = AuthenticationService()
    
    # Регистрация пользователей
    print("Регистрация пользователей:")
    print(auth_service.register(Customer, "user1", "user1@example.com", "password123", "Невский пр. 22"))
    print(auth_service.register(Customer, "user2", "user2@example.com", "password456", "Большой пр. П.С. 4"))
    print(auth_service.register(Admin, "admin1", "admin@example.com", "adminpass", "super"))
    
    # Попытка регистрации с существующим именем пользователя
    print(auth_service.register(Customer, "user1", "new@example.com", "password", "Address"))
    
    # Аутентификация
    print("\nАутентификация:")
    print(auth_service.login("user1", "password123"))  # Успешный вход
    print(auth_service.get_current_user())  # Проверка текущего пользователя
    
    # Неудачная аутентификация
    print(auth_service.login("user1", "qwertyuiop"))
    
    # Вход администратора
    print(auth_service.login("admin1", "adminpass"))
    print(auth_service.get_current_user())
    
    # Функции администратора
    print("\nАдминистративные функции:")
    print("Список пользователей:")
    print(Admin.list_users())
    
    print("\nУдаление пользователя:")
    print(Admin.delete_user("user2"))
    print("Обновленный список пользователей:")
    print(Admin.list_users())
    
    # Выход из системы
    print("\nВыход из системы:")
    print(auth_service.logout())
    print(auth_service.get_current_user())
