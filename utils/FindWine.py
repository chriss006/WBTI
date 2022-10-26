class FindWine:
    def __init__(self, db):
        self.db = db


    def search_red_wine(self, wineid):
        # wineid, winetype으로 와인 검색
        sql = f"SELECT * FROM data_redwine WHERE wineid = {wineid}"
        result = self.db.execute(sql)
        return result

    def search_white_wine(self, wineid):
        # wineid, winetype으로 와인 검색
        sql = f"SELECT * FROM data_white WHERE wineid = {wineid}"
        result = self.db.execute(sql)
        return result

    # 답변 검색
    def search_answer(self, id, info_list):
        # 질문 id를 sql문에 추가
        sql = f"SELECT answer FROM data_answer WHERE id = {id}"

        # 답변 출력
        answer = self.db.execute(sql)[0][0]

        if id == 13 or 15:
            answer = answer.replace('{wineid}', str(info_list[0]))
            answer = answer.replace('{winetype}', str(info_list[1]))
            answer = answer.replace('{winery}', str(info_list[2]))
            answer = answer.replace('{name}', str(info_list[3]))
            answer = answer.replace('{country}', str(info_list[4]))
            answer = answer.replace('{region}', str(info_list[5]))
            answer = answer.replace('{grape}', str(info_list[6]))
            answer = answer.replace('{rate}', str(info_list[7]))
            answer = answer.replace('{price}', str(info_list[8]))
            answer = answer.replace('{price_f}', str(info_list[9]))
            answer = answer.replace('{topic1}', str(info_list[10]))
            answer = answer.replace('{topic2}', str(info_list[11]))
            answer = answer.replace('{bold}', str(info_list[12]))
            answer = answer.replace('{tannic}', str(info_list[13]))
            answer = answer.replace('{sweet}', str(info_list[14]))
            answer = answer.replace('{acidic}', str(info_list[15]))
            answer = answer.replace('{link}', str(info_list[16]))
            answer = answer.replace('{img}', str(info_list[17]))

        return answer

