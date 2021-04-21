clear

set seed 123

import delimited /path_to_file/olympics.csv #change to winter, summer here

gen log_gdpc = log(gdpc)

#summary statistics for years 
estpost tabstat log_gdpc post finstability politstability freedom, by(year) statistics(mean sd median min max) columns(statistics) listwise

#ols
regr log_gdpc post, robust
esttab, se
----------------------------
                      (1)   
                 log_gdpc   
----------------------------
post                0.837***
                  (0.175)   

_cons               9.394***
                  (0.144)   
----------------------------
N                     120   
----------------------------
Standard errors in parentheses
* p<0.05, ** p<0.01, *** p<0.001


regr log_gdpc post subtype finstability politstability freedom, robust
esttab, se
----------------------------
                      (1)   
                 log_gdpc   
----------------------------
post                0.590***
                 (0.0902)   

subtype            -0.437***
                 (0.0936)   

finstability      -0.0366***
                (0.00639)   

politstabi~y        0.348***
                 (0.0888)   

freedom            0.0532***
                (0.00508)   

_cons               6.784***
                  (0.326)   
----------------------------
N                     120   
----------------------------
Standard errors in parentheses
* p<0.05, ** p<0.01, *** p<0.001


#one-way fixed effects 

xtset id year

xtreg log_gdpc post, fe vce(cluster id)
esttab, se
----------------------------
                      (1)   
                 log_gdpc   
----------------------------
post                0.469   
                  (0.201)   

_cons               9.581***
                  (0.103)   
----------------------------
N                     120   
----------------------------
Standard errors in parentheses
* p<0.05, ** p<0.01, *** p<0.001
￼

xtreg log_gdpc post subtype finstability politstability freedom, fe vce(cluster id)
esttab, se
----------------------------
                      (1)   
                 log_gdpc   
----------------------------
post                0.473   
                  (0.217)   

subtype                 0   
                      (.)   

finstability      0.00803   
                 (0.0350)   

politstabi~y        0.136   
                  (0.152)   

freedom           -0.0152   
                 (0.0428)   

_cons               10.43*  
                  (2.988)   
----------------------------
N                     120   
----------------------------
Standard errors in parentheses
* p<0.05, ** p<0.01, *** p<0.001

#two-way fixed effects
xtreg log_gdpc i.year post, fe vce(cluster id)
esttab, se

----------------------------
                      (1)   
                 log_gdpc   
----------------------------
2002.year               0   
                      (.)   

2003.year           0.153** 
                 (0.0302)   

2004.year           0.314***
                 (0.0573)   

2005.year           0.433** 
                 (0.0904)   

2006.year           0.556** 
                  (0.133)   

2007.year           0.715** 
                  (0.159)   

2008.year           0.821** 
                  (0.197)   

2009.year           0.724** 
                  (0.192)   

2010.year           0.814*  
                  (0.243)   

2011.year           0.924*  
                  (0.277)   

2012.year           0.914*  
                  (0.293)   

2013.year           0.937*  
                  (0.303)   

2014.year           0.938*  
                  (0.299)   

2015.year           0.788*  
                  (0.258)   

2016.year           0.769*  
                  (0.259)   

post               0.0162   
                  (0.215)   

_cons               9.159***
                  (0.144)   
----------------------------
N                     120   
----------------------------
Standard errors in parentheses
* p<0.05, ** p<0.01, *** p<0.001


xtreg log_gdpc i.year post subtype finstability politstability freedom, fe vce(cluster id)
esttab, se
----------------------------
                      (1)   
                 log_gdpc   
----------------------------
2002.year               0   
                      (.)   

2003.year           0.194   
                  (0.142)   

2004.year           0.365   
                  (0.216)   

2005.year           0.507   
                  (0.215)   

2006.year           0.577*  
                  (0.203)   

2007.year           0.754*  
                  (0.243)   

2008.year           0.880*  
                  (0.266)   

2009.year           0.789*  
                  (0.291)   

2010.year           0.885*  
                  (0.329)   

2011.year           1.036*  
                  (0.359)   

2012.year           1.030*  
                  (0.353)   

2013.year           1.043*  
                  (0.364)   

2014.year           1.036*  
                  (0.365)   

2015.year           0.867*  
                  (0.328)   

2016.year           0.874*  
                  (0.330)   

post              0.00528   
                  (0.201)   

subtype                 0   
                      (.)   

finstability       0.0228   
                 (0.0223)   

politstabi~y        0.173   
                  (0.316)   

freedom            0.0173   
                 (0.0317)   

_cons               7.640*  
                  (2.266)   
----------------------------
N                     120   
----------------------------
Standard errors in parentheses
* p<0.05, ** p<0.01, *** p<0.001


#lead lag table
xtreg log_gdpc i.year lead_14 -lead_1 lag_1-lag_14, fe vce(cluster id)

ssc install coefplot

coefplot, keep(lead_14 lead_13 lead_12 lead_11 lead_10 lead_9 lead_8 lead_7 lead_6 lead_5 lead_4 lead_3 lead_2 lead_1 lag_1 lag_2 lag_3 lag_4 lag_5 lag_6 lag_7 lag_8 lag_9 lag_10 lag_11 lag_12 lag_13 lag_14) xlabel(, angle(vertical)) yline(0) xline(14.5) vertical msymbol(D) mfcolor(white) ciopts(lwidth(*2) lcolor(*.5)) mlabel format(%9.2f) mlabposition(12) mlabgap(*2) mlabsize(vsmall) ytitle(Log of GDP per capita)
￼
#graphing
xtline log_gdpc, overlay t(year) i(country) legend() scheme(s2mono) ytitle(Log of GDP per capita)  xline(2002, lcolor(blue) lpattern(dash) lwidth(0.2)) xline(2004, lcolor(red) lpattern(dash) lwidth(0.2)) xline(2006, lcolor(blue) lpattern(dash) lwidth(0.2)) xline(2008, lcolor(red) lpattern(dash) lwidth(0.2)) xline(2010, lcolor(blue) lpattern(dash) lwidth(0.2)) xline(2012, lcolor(red) lpattern(dash) lwidth(0.2)) xline(2014, lcolor(blue) lpattern(dash) lwidth(0.2)) xline(2016, lcolor(red) lpattern(dash) lwidth(0.2))
