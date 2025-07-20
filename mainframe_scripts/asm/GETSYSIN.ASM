GETSYSIN  CSECT
         USING *,15
         ST    14,12(13)
         LR    12,15
         LA    2,BUFF
         WTO   'Collecting data'
         SR    0,0
         BR    14
BUFF     DC    CL80' ' 
         END   GETSYSIN
