clear

set seed 111

import delimited /Users/akmarzhan/Downloads/ss154_data_collection/olympics.csv 

gen log_gdp = log(gdp)

esttab, modelwidth(10 20) cell((mean(label(Mean)) sd(par label(Standard Deviation)))) label nomtitle nonumber

----------------------------------------------------
                           Mean   Standard Deviation
----------------------------------------------------
log_gdp                28.29461           (1.174835)
Host                   .0666667           (.2504897)
Freedom                64.50917           (11.12917)
FinStability           14.16443           (7.328822)
PolitStability         .1103984           (.6358766)
Subtype                      .5           (.5020964)
----------------------------------------------------
Observations                120                     
----------------------------------------------------

regr log_gdp host, robust
----------------------------
                      (1)   
                  log_gdp   
----------------------------
host               0.0845   
                  (0.378)   

_cons               28.29***
                  (0.112)   
----------------------------
N                     120   
----------------------------
Standard errors in parentheses
* p<0.05, ** p<0.01, *** p<0.001
￼
regr log_gdp host subtype finstability politstability freedom, robust
----------------------------
                      (1)   
                  log_gdp   
----------------------------
host                0.153   
                  (0.200)   

subtype           -0.0366   
                  (0.152)   

finstability        0.106***
                 (0.0107)   

politstabi~y       -0.805***
                  (0.175)   

freedom            0.0473***
                 (0.0101)   

_cons               23.84***
                  (0.596)   
----------------------------
N                     120   
----------------------------
Standard errors in parentheses
* p<0.05, ** p<0.01, *** p<0.001

￼

xtset id year

xtreg log_gdp host, fe vce(cluster id)

----------------------------
                      (1)   
                  log_gdp   
----------------------------
host               0.0845   
                 (0.0954)   

_cons               28.29***
                (0.00636)   
----------------------------
N                     120   
----------------------------
Standard errors in parentheses
* p<0.05, ** p<0.01, *** p<0.001
￼

xtreg log_gdp host subtype finstability politstability freedom, fe vce(cluster id)
----------------------------
                      (1)   
                  log_gdp   
----------------------------
host               0.0837   
                 (0.0944)   

subtype                 0   
                      (.)   

finstability      0.00162   
                 (0.0425)   

politstabi~y       0.0613   
                  (0.172)   

freedom           -0.0303   
                 (0.0464)   

_cons               30.22***
                  (3.084)   
----------------------------
N                     120   
----------------------------
Standard errors in parentheses
* p<0.05, ** p<0.01, *** p<0.001
￼

xtreg log_gdp i.year host, fe vce(cluster id)
----------------------------
                      (1)   
                  log_gdp   
----------------------------
host                0.104   
                  (0.102)   

_cons               27.58***
                  (0.135)   
----------------------------
N                     120   
----------------------------
Standard errors in parentheses
* p<0.05, ** p<0.01, *** p<0.001
￼

* subtype omitted 
xtreg log_gdp i.year host subtype finstability politstability freedom, fe vce(cluster id)
----------------------------
                      (1)   
                  log_gdp   
----------------------------
host                0.130   
                  (0.103)   

subtype                 0   
                      (.)   

finstability       0.0235   
                 (0.0216)   

politstabi~y        0.211   
                  (0.310)   

freedom            0.0185   
                 (0.0358)   

_cons               25.95***
                  (2.510)   
----------------------------
N                     120   
----------------------------
Standard errors in parentheses
* p<0.05, ** p<0.01, *** p<0.001
￼

xtreg log_gdp i.year lead_14 -lead_1 lag_1-lag_14, fe vce(cluster id)

ssc install coefplot

coefplot, keep(lead_14 lead_13 lead_12 lead_11 lead_10 lead_9 lead_8 lead_7 lead_6 lead_5 lead_4 lead_3 lead_2 lead_1 lag_1 lag_2 lag_3 lag_4 lag_5 lag_6 lag_7 lag_8 lag_9 lag_10 lag_11 lag_12 lag_13 lag_14) xlabel(, angle(vertical)) yline(0) xline(14.5) vertical msymbol(D) mfcolor(white) ciopts(lwidth(*2) lcolor(*.5)) mlabel format(%9.2f) mlabposition(12) mlabgap(*2) mlabsize(vsmall) title(Log of GDP)
￼
