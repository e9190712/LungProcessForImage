# LungProcessForImage
LungSegmentationForNpy.py:

輸入為一系列Dicom Format的病人肺部CT，此圖像經由標準化、Kmeans OR Cmeans、高級形態學處理、放大主要像素到邊界等四個步驟來做LungSegmentation，最後儲存成npy格式(數量與CT相等)。

***如果要用Kmeans處理請選擇 1，Cmeans選擇 2，Kmeans有用高級形態學來處理，Cmeans則沒有，這邊可以自己改動***


plot.py:

單純用來show出npy Format的圖像。
