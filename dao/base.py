from abc import ABC, abstractmethod

class BaseDAO(ABC):
    @abstractmethod
    def insert_post(self, post_id, is_question, creation_date, body, tags, score, parent_id=None):
        pass

    @abstractmethod
    def insert_sql(self, post_id, sql_text):
        pass

    @abstractmethod
    def post_exists(self, post_id):
        pass

    @abstractmethod
    def get_next_new_sql(self, n):
        pass

    @abstractmethod
    def update_sql(self, id_sql, can_be_parsed, is_select, duplicate_tables):
        pass