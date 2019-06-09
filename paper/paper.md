---
link-citations: true
reference-section-title: Bibliography
papersize: a4
documentclass: templates/sig-alternate
title: Does Hick’s Law apply to multi-touch gestures?
author:
- name: Max Mustermann, Bla bla, Bla bla bla
  affiliation: "HCI Research Class Summer 2019 Hasso Plattner Institute Potsdam Germany"
  email: "{firstName.lastName}@student.hpi.uni-potsdam.de"
- name: Max Mustermann
  affiliation: "HCI Research Class Summer 2019 Hasso Plattner Institute Potsdam Germany"
  email: Max.Mustermann@student.hpi.uni-potsdam.de
geometry: "left=2cm,right=2cm,top=1.5cm,bottom=2cm"
---

## Abstract

Does Hick’s Law apply to multi-touch gestures? **this skeleton was obviously taken from a very different paper called drag-and-pop, but we thought you would find some of the elements useful to get a first idea about structure and wording . Hope this helps!** **Please use this template and all its Microsoft-Word based formatting. Thanks!**

## User study

The purpose of this first study was to verify that snap-and-go indeed helps users align objects, to explore the impact of attractor strength on task time, and to compare snap-and-go with traditional snapping.

## Task

The participants’ task was to drag the knob of a slider to a highlighted target location as quickly as possible. Figure 1 shows the apparatus, which consisted of a horizontal slider with a single highlighted target location, which in some conditions was complemented with an attractor (see below). For each trial the slider was reinitialized to the shown state; target distance and attractor, however, were varied.
Task time was counted from the moment the knob was picked up until the moment the knob was successfully aligned and the participant had released the mouse button. Each trial required successful alignment, so in cases where participants released the knob anywhere but over the target, they needed to pick it up again to complete the trial.

Figure 1: The apparatus. The user’s task was to align the slider knob located at the left with the target located at the right.
Alignment required pixel precision. To make that possible the knob was provided with the visuals shown in Figure 2a. To prevent the mouse pointer from occluding the target, participants were encouraged to drag the mouse slightly downwards while dragging the knob (Figure 2c).

## Interfaces

There were three main interface conditions, namely traditional snapping and snap-and-go, implementing the two snapping functionalities illustrated by **Figure** as well as no snapping.

Figure 2: Close-up of the knob reaching the target: A black dash at the bottom of the knob helped visually verify alignment. (b) Attractors used “light bulb” visuals and came in four sizes. (c) Dragging the knob into an attractor caused it to light up.
In the no snapping condition, the target consisted only of the vertical red line shown in Figure 2a. In the snapping conditions, the target was complemented with an attractor, turning the target into a snap location. Attractors behaved differently depending on the snapping condition, but offered the same visuals, a “light bulb” located below the slider (Figure 2b and c). In their inactive state light bulbs were black, but turned to bright green when the knob was captured. To inform participants during the study about the current attractor strengths, the width of the bulb on screen reflected the width of the attractor in motor space (Figure 2a). Interface conditions thus differed in interactive behavior and visuals.

## Experimental design

The study design was within subjects 2 x 4 x 4 (Snapping Technique x Attractor Width x Target Distance) with 8 repetitions for each cell. Distances were 100, 200, 400, and 800 pixels, and Widths 5, 10, 18, and 34 pixels. In addition, participants performed 2 blocks of trials with snapping off at each distance. For each trial, we recorded task completion time and error, i.e., number of times the participant dropped the knob before aligning it properly. Interface order, distances, and sizes were counterbalanced.
Participants received training upfront and at the beginning of each block. The study took about 35 min per participant.

## Apparatus

The experiment was run on a PC running WindowsXP with an 18” LCD monitor, at a resolution of 1280x1024 pixels and 60Hz refresh rate, and driven by an nVidia graphics card. The interface used in this study was implemented in Macromedia Flash; its functioning was briefly described in the Implementation section of this paper. The optical Microsoft IntelliMouse was set to a medium mouse speed and participants were allowed to adjust it prior to the beginning of the study.

## Participants

Three volunteers, (XX male) between the ages of XX and XX were recruited from XXXX. XX were right-handed. 

## Hypotheses

We had one hypothesis: Participants would perform faster in the smaller, individual gesture sets compared to the combined gesture set.

## Results

**Remember all the effort I put into teaching you about raw data? Now is your time to become creative** Figure 3 shows the raw data
[some clever chart you come up with]
Figure 3: Raw data
Figure 4 shows the raw data **in some other clever way, to allow the teaching team to understand what I got and to allow them to assess whether the following stats are plausible**
[some clever chart you come up with]
Figure 4: Raw data
To correct for the skewing common to human response time data we based our analyses on the median response time across repetitions for each participant for each cell. 

Figure 5: Task time by snapping technique and attractor width across all distances (+/- standard error of the mean).
Snapping vs. no snapping: We compared the most conservative case for the two snapping conditions (attractor size = 5) against no snapping for each distance. We performed a 3 x 4 (Snapping Technique x Target Distance) within subjects analysis of variance. There were significant main effects for both Snapping Technique, F(2,16)=66.3, p<<0.01 and for Target Distance, F(3,24)=20.19, p<<0.01. Planned comparisons of no snapping vs. traditional snapping and vs. snap-and-go were also significant, $F(1,8)=76.7, p<<0.001$ and $F(1,8)=61.5, p<<0.01$ respectively.
Snap-and-go vs. traditional snapping: We performed a 2 x 4 x 4 (Snapping Technique x Attractor Width x Target Distance) within subjects analysis of variance. We found significant main effects for each factor. As expected, traditional snapping was faster than snap-and-go F(1,8)=24.0, p<0.01. Also as expected, differences were fairly small, ranging from $3\%$ for attractor widths 5 and 10 to 14% for attractor width 34 (Figure 5)
Impact of attractor width and distance on task time: Not surprisingly, there were significant effects for Attractor Width, F(3,24)=97.6, p<<0.01 and for Target Distance, $F(3,24)=224.4, p<<0.01$; performance improved as attractor width increased and as target distance decreased. There were no significant interactions. Given the similarity to Fitts’ Law experiments, we compared user performance against the Fitts Index of Difficulty (ID), a metric that combines target width and movement distance into one measure of acquisition difficulty []. Figure 6 plots mean movement time for each ID for the two snapping techniques. The regression of movement time against ID for each snapping technique was:

\mathchardef\mhyphen="2D
\begin{align}
\mathrm{Snapping}: 	&\mathrm{MT}=0.265 + 0.19*ID, r^2=0.75 \nonumber\\
\mathrm{Snap \mhyphen and \mhyphen go}: 	&\mathrm{MT}=0.487 + 0.159*ID, r^2=0.59 \nonumber
\end{align}
Figure 6: Fitts analysis of task times.
Note that the main divergence is at very low indices of difficulty. Once the task gets harder (e.g., longer movements, smaller attractor sizes) performance in the two techniques begins to converge.
Error rates were generally low, indicating that the target and knob visuals did allow participants to visually validate alignment sufficiently well. Differences in the error rates for the three different snapping conditions were non significant (No Snapping: 6.1%, Traditional Snapping: 3.7%, Snap-and-Go: 2.6%).
Across snapping methods, eight of nine participants indicated a preference for the stronger 34 and 18 width attractors; one participant preferred the weakest attractor strength included in the study (5).

## Discussion

**what do you conclude based on what you found?**

## Conclusions

**Conclusions goes here**