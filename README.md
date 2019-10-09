# Food-recommended Bot

## Source
- IG
- Dcard
- PTT

## Task:10/8-10/14@Source recongnize
Crews | Assignment
------| ----------
John | - MongoDB <br>- Ptt 
Joy | - Dcard
Derek | - PTT
Angel | - Dcard
明 | - PTT
榮 | - Dcard

## Useful Resources 
> IG scraper : <https://github.com/rarcega/instagram-scraper> <br>
> Instagram-robot : <https://www.bnext.com.tw/article/53299/make-a-robot-instagram-influencer-for-free-lunch> <br>
> 記者快抄(PTT自動撰寫新聞) : <http://news.ptt.cc><br>
> Ptt-web-crawler : <https://github.com/jwlin/ptt-web-crawler><br>
> Dcard-crawler : <https://github.com/leVirve/dcard-spider>

## Concept
To be continued...

## Reference 

|參考專案|BB102:Yummy Bike|AB105:吃飯趣|CB104吃貨戰情室|<mark>專題人頭組-1008<mark>|論文參考:深度學習的美食推薦平台|
|:--|:--|:--|:--|:--|:--|
|系統流程|PyETL|PyETL|PyETL|PyETL||
||DB-Mongo DB|DB-Mongo DB|DB-Mongo DB|DB-Mongo DB|DB-Mongo DB|
||||DB-MySQL||PostgreSQL|
||||ELK(資料監控)|||
||Textmining|Textmining|Textmining|Textmining||
|||||影像辨識(TensorFlow-CNN)|影像辨識(TensorFlow/Keras-CNN)|
||推薦系統|推薦系統||推薦系統|推薦系統|
|||Docker|Docker|||
||Hadoop|Hadoop|Hadoop|Hadoop|GCP(Google Cloud Platform)運算|
||Spark||Spark|Spark||
||AWS(異地備份)|AWS(異地備份)|AWS(Line Bot Server)|AWS||
||Node.js(視覺化)|Django|Flask & Kafka|自動撰文+ig發文|Node.js(網站)|
|||ChotBot|Line bot|||
|資料探勘|前處理-jieba斷詞|TF-IDF|jieba斷詞|||
||前處理-stopword||stopword|||
||前處理-Word2Vec||TF-IDF|||
||摘要-TF-IDF||Word2Vec|||
||摘要-TextRank||SVD|||
||分類-Bayes||分群:K-Means||分群:KNN|
||分類-KNN||分群評量-平均側影法||使用者評分正規化:Z-Score|
||分類-Rocchio||||評分參考價值:遺忘曲線|
||分類-SVM|||||
||情緒分析-自製字典|||||
||情緒分析-分組標準化|||||
||推薦系統-協同過濾-基於item|協同過濾-基於item|協同過濾-基於user||協同過濾+TesorFlow-RNN混合推薦|
||相關性檢驗-餘弦相似度|MSE-確定數據擬合度|協同過濾-基於item|||
||SimRank的結果當成推薦依據|餘弦相似度結果當成推薦依據|餘弦相似度|||
||||RMSE|||
