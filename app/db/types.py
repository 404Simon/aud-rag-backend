from sqlalchemy.types import UserDefinedType


class VECTOR(UserDefinedType):
    def get_col_spec(self):
        return "VECTOR(512)"
