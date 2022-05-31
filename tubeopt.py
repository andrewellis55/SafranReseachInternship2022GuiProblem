import openmdao.api as om
import numpy as np


class _TubeComponent(om.ExplicitComponent):

    def __init__(self, axial_force, bending_moment,
                 thickness_lower_bound=1, safety_margin_lower_bound=0):
        super().__init__()
        self._axial_force = axial_force  # N
        self._bending_moment = bending_moment  # N*m
        self._thickness_lower_bound = thickness_lower_bound  # mm
        self._safety_margin_lower_bound = safety_margin_lower_bound  # Unitless

    def setup(self):

        # Inputs
        self.add_input('inner_diam', val=.060, units='m')
        self.add_input('outer_diam', val=.100, units='m')
        self.add_design_var('inner_diam', lower=0.005, upper=0.5)
        self.add_design_var('outer_diam', lower=0.01, upper=0.6)

        # Outputs
        self.add_output('area', units='m**2')
        self.add_output('thickness', units='m')
        self.add_output('safety_margins', units='unitless')
        self.add_output('diam_over_thickness', units='unitless')

        # Constraints
        self.add_constraint('thickness', lower=self._thickness_lower_bound/1000)
        self.add_constraint('safety_margins', lower=self._safety_margin_lower_bound)
        self.add_constraint('diam_over_thickness', lower=2, upper=25)

        # Area
        self.add_objective('area')

    def compute(self, inputs, outputs):
        # Inputs
        inner_diam, outer_diam = inputs['inner_diam'], inputs['outer_diam']

        # Section Properties
        area = 0.25*np.pi*(outer_diam**2-inner_diam**2)
        thickness = (outer_diam - inner_diam)/2
        diam_over_thickness = outer_diam / thickness
        moment_of_inertia = np.pi/4*((outer_diam/2)**4 - (inner_diam/2)**4)
        radius = outer_diam/2

        # Stress Components
        axial_stress = self._axial_force/area
        bending_stress = self._bending_moment*radius/moment_of_inertia

        # Combined Stresses
        tensile_stress = np.sqrt((axial_stress + bending_stress)**2 + 0.001)

        # Yield Strength
        tensile_yield = 350e6  # Pa

        # Margins
        safety_margin = tensile_yield/tensile_stress - 1

        # Outputs
        outputs['area'] = area
        outputs['thickness'] = thickness
        outputs['safety_margins'] = safety_margin
        outputs['diam_over_thickness'] = diam_over_thickness


class TubeOptimization():
    '''
    Optimizes a Hollow Steel Tube subject to an axial force and bending moment
    to minimize the area

    Parameters
    ----------
        axial_force: float
            Axial force in N
        bending_moment: float
            Bending moment in N*m

    '''

    def __init__(self, axial_force, bending_moment):

        self.axial_force = axial_force  # N
        self.bending_moment = bending_moment  # N*m

    def optimize(self, minimim_safety_margin=0, minimum_thickness=1):

        # Creates Optimization Problem
        problem = om.Problem()
        model = problem.model

        # Adds Tube Component
        model.add_subsystem('tube', _TubeComponent(
            axial_force=self.axial_force,
            bending_moment=self.bending_moment,
            thickness_lower_bound=minimum_thickness,
            safety_margin_lower_bound=minimim_safety_margin
        ), promotes=['*'])

        # Sets up the Problem and Optimizer (called a driver)
        problem.setup()
        problem.driver = om.ScipyOptimizeDriver()
        model.approx_totals()

        # Runs the Optimization
        flag = problem.run_driver()

        # Prints Details of the optimization
        # problem.list_problem_vars(
        #     desvar_opts=['lower', 'upper'],
        #     cons_opts=['lower', 'upper'],
        #     print_arrays=False,
        # )

        inner_diam = round(problem.get_val('inner_diam', units='mm')[0], 3)
        outer_diam = round(problem.get_val('outer_diam', units='mm')[0], 3)
        thickness = round(problem.get_val('thickness', units='mm')[0], 3)
        safety_margins = round(problem.get_val('safety_margins', units='unitless')[0], 4)

        return not flag, (inner_diam, outer_diam, thickness, safety_margins)


if __name__ == '__main__':

    # Example use of class

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
