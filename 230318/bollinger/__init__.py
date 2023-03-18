import pandas as pd
import numpy as np

# 1번 함수 생성
def first(_df, _col, _time) :
    # 결측치와 이상치를 제거
    result = _df[~_df.isin([np.nan, np.inf, -np.inf]).any(1)]
    # 기준이 되는 컬럼을 제외한 나머지 컬럼을 삭제
    result = result.loc[:, [_col]]
    # 이동 평균선, 상단 밴드, 하단 밴드 생성
    result["Center"] = result[_col].rolling(20).mean()
    result["Ub"] = result["Center"] + (2 * result[_col].rolling(20).std())
    result["Lb"] = result["Center"] - (2 * result[_col].rolling(20).std())

    # 시작 시간부터 마지막 데이터까지 필터링
    result = result.loc[_time :]

    # 결과를 리턴
    return result

# 2번 함수
# 거래 내역을 추가하는 함수
def second(_df) :
    # Trade 컬럼을 생성 -> 값은 ""
    result = _df
    result["Trade"] = ""
    # 기준이 되는 컬럼의 이름은 가변
    # 위치는 변하지 않기 때문에
    # 기준이 되는 컬럼은 첫번째
    col = result.columns[0]

    # Trade에 내역 추가
    for i in result.index :
        # 기준이 되는 컬럼이 상단 밴드보다 큰 경우
        if result.loc[i, col] > result.loc[i, "Ub"] :
            if result.shift(1).loc[i, "Trade"] == "buy" : 
                result.loc[i, "Trade"] = ""
            else : 
                result.loc[i, "Trade"] = ""
        # 기준이 되는 컬럼이 하단 밴드보다 작은 경우
        if result.loc[i, col] < result.loc[i, "Lb"] :
            if result.shift(1).loc[i, "Trade"] == "buy" : 
                result.loc[i, "Trade"] = "buy"
            else : 
                result.loc[i, "Trade"] = "buy"
        # 기준이 되는 컬럼이 하단 밴드와 상단 밴드 사이에 존재하는 경우
        if result.loc[i, col] >= result.loc[i, "Lb"] and result.loc[i, col] <= result.loc[i, "Ub"] :
            if result.shift(1).loc[i, "Trade"] == "buy" : 
                result.loc[i, "Trade"] = "buy"
            else : 
                result.loc[i, "Trade"] = ""
    return result


# 3번 함수
# 수익율을 계산하는 함수
def third(_df) : 
    result = _df
    # Return 컬럼을 생성 -> 값 1
    result["Return"] = 1
    # 기준이 되는 컬럼은 columns[0]
    col = result.columns[0]
    # 수익율, 구매 가격, 판매 가격 변수 생성
    rtn = 1.0
    buy = 0.0
    sell = 0.0
    
    # 수익율을 계산하는 반복문
    for i in result.index :
       # 구매 가격 확인
       if result.shift(1).loc[i, "Trade"] == "" and result.loc[i, "Trade"] == "buy" :
           buy = result.loc[i, col]
           print("구매 일 :", i, "구매 가격 :", buy)
           # 판매 가격 확인
       elif result.shift(1).loc[i, "Trade"] == "buy" and result.loc[i, "Trade"] == "" :
           sell = result.loc[i, col]
           # 수익율 계산
           rtn = (sell - buy) / buy +1
           # 수익율을 Return 컬럼에 대입
           result.loc[i, "Return"] = rtn
           print("판매일 :", i, "판매 가격 :", sell, "수익율 :", round(rtn, 4))
    
        # 구매 가격과 판매 가격을 초기화
       if result.loc[i, "Trade"] == "" : 
           buy = 0.0
           sell = 0.0
    # 누적 수익률


    # 수익율 변수 생성
    acc_rtn = 1.0

    for i in result.index :
        rtn = result.loc[i, "Return"]
        acc_rtn *= rtn
        result.loc[i, "Acc_rtn"] = acc_rtn

    print("누적 수익율 :", round(acc_rtn, 4))

    return result
