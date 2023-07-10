### 개요
![Untitled](https://github.com/dinleo/NLP_TermP_2023/assets/81561645/7fe65b97-f2ad-4360-9318-9c362d8c7df8)

- 암호화폐 뉴스를 크롤링 후 토큰화 하여, 코인 가격으로 Labeling
- 이를 이용해 BERT 를 Fine Tuning 하여 모델을 생성한다.
- 해당 모델은 새로운 경제뉴스를 넣었을 때, 코인 가격을 예측 할 수 있다.

### 데이터셋

- Crypto News
     
    - from CBNC
- Coin Data
  
    - from TradingView

### 학습

- 토큰화
    - BertTokenizer, nltk
- 인코딩, 임베딩
    - Bert basic medel, torch
- 모델, 최적화
    - Feed-Forward Network, Adam
 
### 결과
![1](https://github.com/dinleo/NLP_TermP_2023/assets/81561645/37ad26eb-3637-4b2a-b483-f4664135a6e8)
