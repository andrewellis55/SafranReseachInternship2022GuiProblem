# Safran Research Internship 2022 GUI Problem

## Problem Statement
A hollow tube geometry, subject to bending and axial loads is optimized to be as light as possible while meeting or exceeding specified safety margins. A TubeComponent module was created to determine minimum cross-sectional area of the tube given input parameters.

### Inputs and Outputs
The inputs for this problem are:
- Axial Force
- Bending Moment
- Constraints:
    - Thickness Lower Bound
    - Safety Margins Lower Bound

The outputs are:
- Inner Diameter
- Outer Diameter
- Thickness
- Safety Margins

### Deliverables
Develop a simple GUI mock-up based on the **tubeopt.py** module provided that allows users to enter the input parameters given above and display the resulting geometry (inner diameter, outer diameter) that minimizes the area given the inputs. You can develop this GUI using a python framework, or create a mock up using Figma, Power Point, or even a hand sketch.

This problem is to test your ability to think of how the code you develop will be ported to a front end and deployed to users. The mockup should be clear on what the design intentions are and any interactivity can be easily explained.

At Safran we use a tool called [Dash](https://dash.plotly.com/) to develop out front end for the George tool.

## Dependancies
To run the TubeOpt module, the following python libraries should be installed
- openmdao.api
- numpy

Note that running or interfacing with the provided code is optional. This is a design challenge, not a coding one.

When we develop real GUIs at Safran, we also install:
- dash
- dash_bootstrap_components
- plotly

as required.

## API Examples

```python
from tubeopt import TubeOptimization

# initializing TubeOptimization Class
tubeopt = TubeOptimization(
    axial_force=10e3,           # N
    bending_moment=5e3          # N*m
)

flag, (inner_diam, outer_diam, thickness, safety_margins) = \
    tubeopt.optimize(
        minimim_safety_margin=0.05,  # Unitless
        minimum_thickness=3          # mm
)

print(f'Inner Diameter: {inner_diam} mm')
print(f'Outer Diameter: {outer_diam} mm')
print(f'Thickness: {thickness} mm')    
print(f'Safety Margin: {safety_margins}')
print(f'Optimization Converged Succesfully: {flag}')

```

## Requirements
* UI Mockup or interface using Dash

## Evaluation Criteria
* Is the user interface intuitive to use, is it clear to users what they need to to in order to produce the desired result
* How would errors handled in the interface
* Is the interface accessible (e.g. legible fonts, spacing between components)
