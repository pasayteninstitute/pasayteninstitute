# Bug Walk Demo


### About
Based on a problem from a Martin Gardner book, this is a cute exercise in constrained dynamics and planar geometry. 

The original incarnation involves four bugs at the vertices of a square.


### How to use the Code

The quickest way to run this code is to pick a number greater than 3, and instantiate the RegularBugWalk class,

`square = RegularBugWalk(4)`

which will automatically perform the relevant calculation. To see the trajectories of the individual bugs, use the .plot() 
method.

`square.plot()`

The parent class, BugWalk, allows you to insert whatever vertices you like as a list of ordered tuple pairs. The calculation is 
not yet performed. To run the calculation you'll need to use the .walk() method. That method takes an optional argument - an 
integer number of steps - which definites the scope of the computation. The bigger the number of points - or the further they are 
from each other - the more interations you'll probably want.

RegularBugWalk automatically determines the appropriate number of steps, owing to the logarithmic curve structure of this problem 
on a regular polygon.

### Other Remarks and TODO

We will update this codebase with an animation option, which helps explore how the bugs move on their trajectories, covering more 
ground initially, and taking smaller steps as they approach each other.

For a regular polygon, the distance the bugs move before meeting is the distance originally are from each other: the length of 
each of the regular polygon's sides. For simplicity of calcualtion, we elected to generate these polygons as inscribed on the 
unit circle. Thus, the length of the individual sides depends on the number of vertices.


### References

The late Martin Gardner's puzzles can be found on the eponymous website: https://martin-gardner.org/PuzzleBooks.html.

Details about the logarithmic curves can be found on Wikipedia: https://en.wikipedia.org/wiki/Logarithmic_spiral
