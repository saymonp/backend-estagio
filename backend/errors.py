class AppError(Exception):
    code = 400

    def set_code(self, new_code):
        self.code = new_code
        return self
