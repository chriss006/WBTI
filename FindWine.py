

class FindWine:
    def __init__(self, db):
        self.db = db

    # id를 입력하면 와인 정보(name, country, winery, sweet, bold, acidic, tannic, price_f, link, img) 출력해서 각 변수에 할당

    # 검색 쿼리 생성
    def _make_query(self, id, type):
        sql = f"SELECT * FROM {type} WHERE wineid = {id}"
        return sql

    # 와인 검색
    def search(self, id, type):
        # wineid, winetype으로 와인 검색
        sql = f'SELECT * FROM {type} WHERE wineid = {id}'
        result = self.db.execute(sql)
        return result