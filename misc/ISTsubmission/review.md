# Review

Alternative titles: 

1. Using Neural Networks to Detect and Emulate Execution Traces of Simple Algorithms
2. Classification and Emulation of Sorting Algorithms using Neural Networks
3. Using Neural Networks for Learning to Detect and Emulate Sorting Algorithms based on their Execution Traces
4. Neural Networks Learn to Detect and Emulate Sorting Algorithms from Images of their Execution Traces


## 1. Overview and Structure

1. Introduction and Motivation
2. Background on Program Induction
3. Image of Algorithm
4. Program Classification
5. Pattern Detection in Sequences
6. Algorithm Prediction and Behavior Emulation
7. Discussion and Related Research
8. Conclusions
9. Future Work and Applications
10. Acknowledgement

### Steps in review (Planning 3.75/4):

1. **Fix minor and medium feedback items (2/2 done)**
2. **Read suggested papers (2/2 done)**
3. **Discuss changes with co-author (2/2 done)**
	- abstract/introduction more concise wrt to the paper overview - Bipin
	- point out feedback wrt to the paper overview - Catalin
	- discuss about taking out Section 1 (introduction), reinsert references - Bipin
	- discuss about reorganizing & renaming sections - Catalin
4. **Restructure, more major feedback items (6/8 done)**
	- address each major feedback item separately
	- so far here we have 5 major points

	- **abstract, introduction & objective for 1st reviewer (2/2 done)**
	- **link to software visualization for 2nd reviewer (2/2 done)**
	- **restructure & renaming for 1st reviewer (4/4 done)**
	- **ambitious claims for 2nd reviewer (2/2 done)**

	- **It is very important to make clear what is the problem you are trying to solve, that is not covered in other works. (1st reviewer)**
	- **The research problem is not presented. (1st reviewer)**
	- It is important to add more context and motivation based on literature review. Then, present the problem in a concise way. Finally, present the goal of the work. (1st reviewer) - DONE
	- There is a mix between definitions and what is your work. You should separate this better. Give definitions from others and add references. Then present what is you study. (1st reviewer) - DONE

	- method part in abstract rephrasing R1
	- changes throughout the rest of the abstract
	- add reads for point 3 C1
	- rephrasing to emphasize execution traces

	- comment out section 1 - done
	- rename sections at the beginning - done
	- take care of related research section, split discussion - done
	- rename sections at the end - done
	- identify important commented references & reinsert them - done
	- fix other issues caused by restructure - done

	- introduction
	- program induction and definitions
	- learning theory (eduction in programming)
	- execution traces in software & visualization


## 2. Small Issues

1. fix "of of"
2. labels with two ":"
3. rephrase "Array does not - the data does" ???? -> However, the input data does not have an influence on the strategy of the algorithm while reversing an array.
4. fix "of a program - [5]" -> of a program [5]
5. fix reference to tables 1, 5, 6 & 8
6. fix "Heapsort in 7? What is this seven?"
7. proof reading
8. legend for fix types
9. re-representation -> This allows showcasing different set-ups complexities and improvements based on the data representation type and by designing better models of program induction.
10. "The type of a new previously unseen program can be predicted", explain why is this important -> This could prove relevant in deciding what type of problem the program solves and which aspects of the input data have a higher influence on the output data of the program.
11. Review the way you add some references. How you cite them, according to the template of the paper. E.g. [6] presents…. -> Authors' names [6] present(s)… -> improved way of citing ( *Author's Names* [Number])
12. fixes bibliography

## 3. Suggested Reads

1. Ma, K. L. (2007). Machine learning to boost the next generation of visualization technology

2. Hayes, J. H., Li, W., & Rahimi, M. (2014). Weka meets TraceLab: Toward convenient classification: Machine learning for requirements engineering problems

3. F. Fittkau, S. Finke, W. Hasselbring and J. Waller, "Comparing Trace Visualizations for Program Comprehension through Controlled Experiments,"

- a programmer receives a task: eg. to refactor or understand a login process
- compare 2 visualization programs
- metrics are:
	- time spent on task (minutes)
	- corectness of solution (points)
- the tasks were quite interesting here
- extravis vs exploreviz

4. H. N. Huang, E. Verbeek, D. German, M. Storey and M. Salois, "Atlantis: Improving the Analysis and Visualization of Large Assembly Execution Traces,"

- assembly traces are broadly used for identifying software vulnerabilities
- link to paper on malware by Pascanu
- trace start point - end point memory delta
- query instructions in a trace

5. M. D. Shah and S. Z. Guyer, "Critical Section Investigator: Building Story Visualizations with Program Traces,"

- detecting performance problems
- which methods contribute to overall program's execution time

6. City Metaphor

- CodeCity 
- ExplorViz
- CodeCity - the original work

7. Traces

Analyze program vulnerability, performance problems, comprehesibility

- Extravis - software
- Atlantis - assembly
- Critical Section Investigator - java 

On one hand program representation and visualization have an effect how comprehensible the program is and thus how efficient someone could be to perform a task on it. On the other hand traces prove efficient for detecting vulnerabilities and performance issues.


## 4. Major Issues

1. **Abstract & Introduction (reviewer 1)**
	- 1st page of review, blue comments - Bipin
	- for myself, need to revise literature and define problem + show objective based on literature

2. **Objective (reviewer 1)**
	- objective is to find how to model algorithms using neural networks
	- start from the sensorimotor view (moving objects around)
	- programs are similar to moving objects around
	- neural networks are in fact programs (eg. recognizing a face)
	- but these programs are not hardcoded
	- can we use them to infer more abstract programs?

3. **Link to Visualization (reviewer 2)**
	- all suggested reads go here

## 5. Comments in Overleaf and other Ideas

1C. Catalin C1: this sounds too abstract and vague, maybe stick to predicting program classes and future steps for sorting algorithms and other simple problems such as reversing, swapping intervals, heaps and binary search trees by observing their execution traces. - rephrase

1R. We begin by classifying execution traces of algorithms working on a finite array of numbers that are swapped according to some rules. Next we focus on detecting patterns of a specific class of programs inside a larger set of programs. This is then extended to emulation of algorithms and combination of various programs in order to obtain novel programs and also achieve program optimization. 

METHOD (extension to objective) R1
-> 

1F. We begin by classifying execution traces of algorithms working on a finite array of numbers, such as various sorting and data structures algorithms. Next we experiment with detecting sub-program patterns inside the trace sequence of a larger program. The last step is to predict future steps in the execution of various sorting algorithms. More specifically, we try to emulate their behavior by observing their execution traces. Finally, we discuss generalizations to other classes of programs, such as 1-D Cellular Automata.

2C. Define Experiments for Cellular Automata - practical (check notebook for some ideas)

3C. Whole view: trace, program, code city, etc... - make a diagram - visual

4C. Catalin C2: incorporate nicely all the literature you know on computer programs and software visualization

POINT 3 (extension to suggested reads) C1
-> 

4F. Analysing program traces has seen success in the areas of identifying methods which contribute to an overall's program execution time \textit{Shah \& Guyer} and detecting software vulnerabilities in \textit{Huang et al.}. Although the term traces is not explicitly used in the study presented by \textit{Pascanu et al.}, the approach of classifying malware based on the executed instructions and predicting the next API calls, is implicitly also analysing a program trace.... (rephrased afterwards)

(34 greens + 10 blues) 44/140