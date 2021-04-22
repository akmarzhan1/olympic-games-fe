devtools::install_github("synth-inference/synthdid")
foo <- read.csv("C:/Users/albio/Downloads/olympics.csv")
dim(foo)
head(foo)

library(tidyr)
foo <- drop_na(foo)
dim(foo)

setup = panel.matrices(foo, unit = 2, time = 3, outcome = 8, treatment = 7)
setup

help(synthdid_estimate)


tau.hat = synthdid_estimate(setup$Y, setup$N0, setup$T0)
se = sqrt(vcov(tau.hat, method='placebo'))
sprintf('point estimate: %1.2f', tau.hat)
sprintf('95%% CI (%1.2f, %1.2f)', tau.hat - 1.96 * se, tau.hat + 1.96 * se)
plot(tau.hat)


tau.hat
summary(tau.hat)


se = sqrt(vcov(tau.hat, method='placebo'))
sprintf('point estimate: %1.2f', tau.hat)
sprintf('95%% CI (%1.2f, %1.2f)', tau.hat - 1.96 * se, tau.hat + 1.96 * se)

plot(tau.hat, se.method='placebo')

plot(tau.hat, overlay=.8, se.method='placebo')

tau.sc   = sc_estimate(setup$Y, setup$N0, setup$T0)
tau.did  = did_estimate(setup$Y, setup$N0, setup$T0)
estimates = list(tau.did, tau.sc, tau.hat)
names(estimates) = c('Diff-in-Diff', 'Synthetic Control', 'Synthetic Diff-in-Diff')

synthdid_plot(estimates, se.method='placebo')

synthdid_plot(estimates, facet.vertical=FALSE, 
              control.name='control', treated.name='Greece', 
              lambda.comparable=TRUE, se.method = 'none', 
              trajectory.linetype = 1, line.width=.75, effect.curvature=-.4,
              trajectory.alpha=.7, effect.alpha=.7, 
              diagram.alpha=1, onset.alpha=.7) + 
    theme(legend.position=c(.26,.07), legend.direction='horizontal', 
          legend.key=element_blank(), legend.background=element_blank(),
          strip.background=element_blank(), strip.text.x = element_blank())

synthdid_units_plot(estimates, se.method='none') + 
    theme(legend.background=element_blank(), legend.title = element_blank(), 
          legend.direction='horizontal', legend.position=c(.17,.07), 
	  strip.background=element_blank(), strip.text.x = element_blank())
